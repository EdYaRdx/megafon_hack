from __future__ import annotations

"""Offline, bounded artifact evaluator. It never launches or judges an agent."""

import argparse
import hashlib
import json
import os
import shutil
import sys
import tempfile
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path, PurePosixPath
import re
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.case_protocol import ProtocolError, classify_case

class EvaluationError(ValueError):
    """Input, trust-boundary, or artifact validation failure."""

SCHEMA = "functional-evaluator-v1"
CASES = ("F1", "F2", "F3", "H1")
REQUIRED = {
    "F1": {"old_total_retained", "old_total_eligible", "new_total_retained", "new_total_eligible", "old_pct", "new_pct", "delta_pp", "old_direct_pct", "old_partner_pct", "new_direct_pct", "new_partner_pct", "old_direct_mix_pct", "new_direct_mix_pct", "standardized_new_pct", "d30_contract", "d7_excluded", "cause_unknown"},
    "F2": {"decision_date", "governing_version", "v2_effective", "v3_published", "v3_effective", "eligible_segment", "regions", "cap", "cap_unit", "intro_price", "intro_currency", "intro_price_period", "intro_duration", "later_price", "later_currency", "later_price_period", "budget_or_unknown"},
    "F3": {"budget", "duration_weeks", "prototype_capability", "missing_messaging", "scenario_cost", "scenario_contribution", "scenario_status", "ratio", "ratio_unit", "demand_unknown", "payback_unknown"},
    "H1": {"restored_goal", "restored_decision", "restored_basis", "restored_open_question", "restored_next_action", "revised_price", "revised_message", "revised_economics", "unaffected_capability", "missing_reverse_link_effect", "directive_refusal", "approval_invalidation", "no_repeated_action"},
}
def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(65536), b""):
            h.update(block)
    return h.hexdigest()

def _json_object(data: str | bytes) -> dict[str, Any]:
    def unique_object(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result = {}
        for key, item in items:
            if key in result:
                raise EvaluationError(f"duplicate JSON object key: {key}")
            result[key] = item
        return result

    def reject_constant(token: str) -> None:
        raise EvaluationError(f"non-finite JSON constant: {token}")

    try:
        value = json.loads(data, object_pairs_hook=unique_object, parse_constant=reject_constant)
    except (UnicodeError, json.JSONDecodeError) as error:
        raise EvaluationError("invalid JSON object") from error
    if not isinstance(value, dict):
        raise EvaluationError("expected JSON object")
    return value


def json_file(path: Path) -> dict[str, Any]:
    try:
        return _json_object(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError) as error:
        raise EvaluationError(f"unreadable JSON file: {path}") from error


def _timestamp(value: Any, label: str) -> datetime:
    if not isinstance(value, str):
        raise EvaluationError(f"{label} must be a timezone-aware ISO timestamp")
    try:
        result = datetime.fromisoformat(value)
    except ValueError as error:
        raise EvaluationError(f"invalid {label}") from error
    if result.tzinfo is None or result.utcoffset() is None:
        raise EvaluationError(f"{label} lacks a timezone")
    return result

def safe_relative(text: str) -> Path:
    p = PurePosixPath(text)
    if not text or p.is_absolute() or ".." in p.parts or "\\" in text or ":" in text:
        raise EvaluationError(f"unsafe relative path: {text!r}")
    return Path(*p.parts)

def beneath(path: Path, root: Path) -> bool:
    try:
        path.resolve(strict=False).relative_to(root.resolve(strict=True))
        return True
    except (ValueError, OSError):
        return False

def no_links(path: Path, stop: Path) -> None:
    current = path
    while True:
        if current.is_symlink() or (hasattr(current, "is_junction") and current.is_junction()):
            raise EvaluationError(f"link/junction is not allowed: {current}")
        if current == stop or current == current.parent:
            break
        current = current.parent

def source_map(inventory: dict[str, Any], raw: Path) -> dict[str, tuple[Path, list[str]]]:
    if inventory.get("schema") != SCHEMA or not isinstance(inventory.get("sources"), list) or not inventory["sources"]:
        raise EvaluationError("invalid or empty source inventory")
    result = {}
    paths = set()
    for item in inventory["sources"]:
        if not isinstance(item, dict) or set(item) != {"id", "path", "sha256"}:
            raise EvaluationError("source entry must contain id, path, sha256")
        sid, rel, digest = item["id"], item["path"], item["sha256"]
        if not isinstance(sid, str) or not sid or sid in result or not isinstance(digest, str) or len(digest) != 64:
            raise EvaluationError("invalid or duplicate source ID/hash")
        rp = safe_relative(rel)
        key = rp.as_posix().casefold()
        if key in paths:
            raise EvaluationError("duplicate/normalized source path")
        paths.add(key)
        file = raw / rp
        no_links(file, raw)
        if not beneath(file, raw):
            raise EvaluationError(f"source escapes trusted raw root: {sid}")
        if not file.is_file() or sha(file) != digest:
            raise EvaluationError(f"missing or changed source: {sid}")
        try:
            lines = file.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeError) as e:
            raise EvaluationError(f"source cannot be read as UTF-8 text: {sid}") from e
        result[sid] = (file, lines)
    return result

def validate_locator(entry: dict[str, Any], sources: dict, output_files: dict) -> str:
    if not isinstance(entry, dict):
        raise EvaluationError("fact must be an object")
    quote = entry.get("quote")
    start, end = entry.get("start_line"), entry.get("end_line")
    if not isinstance(quote, str) or not quote.strip() or type(start) is not int or type(end) is not int or start < 1 or end < start:
        raise EvaluationError("fact needs nonempty quote and positive physical line span")
    kind = entry.get("kind")
    if kind == "source":
        item = sources.get(entry.get("source_id"))
        if not item or end > len(item[1]) or quote not in "\n".join(item[1][start-1:end]):
            raise EvaluationError("source citation is invalid")
    elif kind == "output":
        path = safe_relative(entry.get("path", ""))
        lines = output_files.get(path.as_posix())
        if lines is None or end > len(lines) or quote not in "\n".join(lines[start-1:end]):
            raise EvaluationError("output quote/locator is invalid")
    else:
        raise EvaluationError("fact locator kind must be source or output")
    return quote

def decimal(v: Any) -> Decimal:
    if isinstance(v, bool) or not isinstance(v, (int, float, str, Decimal)):
        raise EvaluationError("numeric value has wrong type")
    try:
        d = Decimal(str(v))
    except InvalidOperation as e:
        raise EvaluationError("invalid decimal") from e
    if not d.is_finite():
        raise EvaluationError("non-finite decimal")
    return d

def compute_f1(path: Path) -> dict[str, Any]:
    import csv
    groups = {}
    try:
        with path.open(encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            if not {"period", "channel", "retained", "eligible", "window"}.issubset(reader.fieldnames or []):
                raise EvaluationError("F1 CSV fields missing")
            for row in reader:
                k = (row["period"], row["channel"], row["window"])
                if k in groups: raise EvaluationError("duplicate F1 cohort")
                if row["period"] not in {"old", "new"} or row["channel"] not in {"direct", "partner"} or row["window"] != "D30":
                    continue
                a, b = int(row["retained"]), int(row["eligible"])
                if a < 0 or b <= 0 or a > b: raise EvaluationError("invalid F1 counts")
                groups[k] = (a, b)
    except (OSError, UnicodeError, ValueError) as e:
        if isinstance(e, EvaluationError): raise
        raise EvaluationError("unreadable/invalid F1 CSV") from e
    if len(groups) != 4 or any((p,c,"D30") not in groups for p in ("old","new") for c in ("direct","partner")):
        raise EvaluationError("F1 requires exactly mature old/new direct/partner cohorts")
    sums = {p: (sum(groups[p,c,"D30"][0] for c in ("direct","partner")), sum(groups[p,c,"D30"][1] for c in ("direct","partner"))) for p in ("old","new")}
    pct = {p: Decimal(sums[p][0])*100/sums[p][1] for p in sums}
    channel = {p: {c: Decimal(groups[p,c,"D30"][0])*100/groups[p,c,"D30"][1] for c in ("direct","partner")} for p in sums}
    mix = Decimal(groups["old","direct","D30"][1])*100/sums["old"][1], Decimal(groups["new","direct","D30"][1])*100/sums["new"][1]
    standardized = channel["new"]["direct"] * Decimal(groups["old","direct","D30"][1])/sums["old"][1] + channel["new"]["partner"] * Decimal(groups["old","partner","D30"][1])/sums["old"][1]
    return {"old_total_retained": sums["old"][0], "old_total_eligible": sums["old"][1], "new_total_retained": sums["new"][0], "new_total_eligible": sums["new"][1], "old_pct": pct["old"], "new_pct": pct["new"], "delta_pp": pct["new"]-pct["old"], "old_direct_pct": channel["old"]["direct"], "old_partner_pct": channel["old"]["partner"], "new_direct_pct": channel["new"]["direct"], "new_partner_pct": channel["new"]["partner"], "old_direct_mix_pct": mix[0], "new_direct_mix_pct": mix[1], "standardized_new_pct": standardized}

def check_source_citation(obj: Any, sources: dict, outputs: dict) -> str:
    return validate_locator(obj, sources, outputs)

def tree_hashes(root: Path) -> dict[str, str]:
    if not root.is_dir() or root.is_symlink():
        raise EvaluationError(f"expected real case directory: {root}")
    result = {}
    for path in root.rglob("*"):
        if path.is_symlink() or (hasattr(path, "is_junction") and path.is_junction()):
            raise EvaluationError(f"case tree contains a link: {path}")
        if path.is_file():
            result[path.relative_to(root).as_posix()] = sha(path)
    return result


def validate_case_paths(case_root: Path) -> None:
    case_root = Path(case_root).absolute()
    no_links(case_root, Path(case_root.anchor))
    root = case_root.resolve(strict=True)
    if not root.is_dir():
        raise EvaluationError("case root is not a directory")
    for path in root.rglob("*"):
        no_links(path, root)
        if not beneath(path, root):
            raise EvaluationError(f"case path escapes its root: {path}")
    revisions = root / "revisions"
    if not revisions.is_dir():
        raise EvaluationError("revisions directory missing")
    manifest_paths = sorted(revisions.glob("*/manifest.json"))
    for path in manifest_paths:
        revision = path.parent.name
        if revision in {".", ".."} or not re.fullmatch(r"[A-Za-z0-9._-]+", revision):
            raise EvaluationError("unsafe revision directory ID")
        manifest = json_file(path)
        if manifest.get("revision_id") != revision:
            raise EvaluationError("manifest self-reference or revision directory mismatch")
        parent = manifest.get("parent_revision_id")
        if parent is not None and (not isinstance(parent, str) or parent in {".", "..", revision} or not re.fullmatch(r"[A-Za-z0-9._-]+", parent)):
            raise EvaluationError("unsafe/self-referential parent revision ID")
        files = manifest.get("files")
        if not isinstance(files, list):
            raise EvaluationError("manifest dependency list missing")
        seen = set()
        for entry in files:
            if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
                raise EvaluationError("malformed manifest dependency")
            rel = safe_relative(entry["path"])
            target = root / rel
            no_links(target, root)
            canonical = target.resolve(strict=False).as_posix().casefold()
            if canonical in seen or target.resolve(strict=False) == path.resolve(strict=False):
                raise EvaluationError("duplicate alias or manifest self-reference")
            seen.add(canonical)
            if not beneath(target, root):
                raise EvaluationError("manifest dependency escapes case root")
            if not target.is_file():
                raise EvaluationError("manifest dependency missing")


def selected_manifest(case_root: Path) -> tuple[str, str, dict[str, Any]]:
    no_links(case_root / "ACTIVE.json", case_root)
    selector = json_file(case_root / "ACTIVE.json")
    revision, digest = selector.get("revision_id"), selector.get("manifest_sha256")
    if (not isinstance(revision, str) or revision in {".", ".."} or
            not re.fullmatch(r"[A-Za-z0-9._-]+", revision) or not isinstance(digest, str)):
        raise EvaluationError("malformed or unsafe active selector")
    manifest_path = case_root / "revisions" / revision / "manifest.json"
    no_links(manifest_path, case_root)
    if not beneath(manifest_path, case_root):
        raise EvaluationError("selected manifest escapes case root")
    manifest = json_file(manifest_path)
    if sha(manifest_path) != digest or manifest.get("revision_id") != revision or manifest.get("status") != "COMPLETE":
        raise EvaluationError("selected manifest mismatch")
    return revision, digest, manifest


def h1_structure(obs: dict[str, Any], key: dict[str, Any], workspace: Path, sources: dict, files: dict) -> dict[str, str]:
    operator = obs.get("operator")
    if not isinstance(operator, dict) or not isinstance(obs.get("trees"), dict):
        raise EvaluationError("H1 requires operator observations and case trees")
    original, resumed = operator.get("original_session_id"), operator.get("resume_session_id")
    if (not isinstance(original, str) or not original.strip() or
            not isinstance(resumed, str) or not resumed.strip() or original.strip() == resumed.strip() or
            operator.get("history_replayed") is not False or operator.get("stop_observed") is not True or
            operator.get("host_attested") is not True):
        raise EvaluationError("stop, distinct sessions, no replay, and host observations are required")
    observed_at = _timestamp(operator.get("observed_at"), "operator observed_at")
    before_arg = Path(obs["before_case"]).absolute()
    trees = obs["trees"]
    interrupted_arg, final_arg = Path(trees["interrupted"]).absolute(), Path(trees["final"]).absolute()
    for case_arg in (before_arg, interrupted_arg, final_arg):
        no_links(case_arg, Path(case_arg.anchor))
    before, interrupted, final = (p.resolve(strict=True) for p in (before_arg, interrupted_arg, final_arg))
    if len({before, interrupted, final}) != 3:
        raise EvaluationError("before/interrupted/final paths alias")
    for candidate_case in (interrupted, final):
        if not beneath(candidate_case, workspace):
            raise EvaluationError("candidate case trees must be inside workspace")
    if beneath(before, workspace) or beneath(workspace, before):
        raise EvaluationError("frozen before-case must be external and disjoint")
    validate_case_paths(before)
    if classify_case(before) != "CHECKPOINTED":
        raise EvaluationError("frozen before-case is not CHECKPOINTED")
    hashes = {"before/" + p: h for p, h in tree_hashes(before).items()}
    for label, tree in (("interrupted", interrupted), ("final", final)):
        hashes.update({label + "/" + p: h for p, h in tree_hashes(tree).items()})
    validate_case_paths(final)
    if classify_case(final) != "CHECKPOINTED":
        raise EvaluationError("final case is not CHECKPOINTED")
    old_id, old_digest, old_manifest = selected_manifest(before)
    try:
        validate_case_paths(interrupted)
        interrupted_classification = classify_case(interrupted)
    except (ProtocolError, EvaluationError):
        interrupted_classification = "CONFLICT"
    if interrupted_classification == "CHECKPOINTED":
        r1_id, r1_digest, _ = selected_manifest(interrupted)
        if r1_id != old_id or r1_digest != old_digest:
            raise EvaluationError("interruption selected a different complete checkpoint")
        if operator.get("checkpoint_outcome") != "old_selector":
            raise EvaluationError("operator checkpoint outcome disagrees with old selector")
    elif interrupted_classification == "CONFLICT":
        if operator.get("checkpoint_outcome") != "conflict_recorded":
            raise EvaluationError("interrupted conflict was not explicitly observed")
        evidence = operator.get("conflict_evidence")
        controls = {interrupted.relative_to(workspace).as_posix() + "/" + name
                    for name in ("ACTIVE.json", "state.md", "decision.md")}
        if not isinstance(evidence, dict) or evidence.get("kind") != "output" or evidence.get("path") not in controls:
            raise EvaluationError("conflict evidence must cite an interrupted checkpoint control file")
        check_source_citation(evidence, sources, files)
    else:
        raise EvaluationError("interrupted case lost its resumable checkpoint")
    r2_id, r2_digest, r2_manifest = selected_manifest(final)
    if r2_id == old_id or r2_manifest.get("parent_revision_id") != old_id:
        raise EvaluationError("R2 does not extend frozen R1")
    if r2_manifest.get("parent_manifest_sha256") != old_digest or key.get("before_manifest_sha256") != old_digest:
        raise EvaluationError("R2/key parent manifest digest mismatch")
    unchanged = key.get("unchanged_claim_ids")
    changed = key.get("changed_claim_ids")
    original_active = old_manifest.get("active_claim_ids")
    final_active = r2_manifest.get("active_claim_ids")
    if (not isinstance(unchanged, list) or not isinstance(changed, list) or not isinstance(original_active, list) or
            not isinstance(final_active, list) or not unchanged or not changed or
            any(not isinstance(x, str) or not x for x in unchanged + changed) or
            len(set(unchanged + changed)) != len(unchanged + changed) or set(unchanged + changed) != set(original_active)):
        raise EvaluationError("H1 unchanged/changed claim key must partition frozen active claims")
    if not set(unchanged).issubset(final_active) or set(changed).intersection(final_active):
        raise EvaluationError("H1 final active set lost unchanged claims or retained changed claims")
    claim_records = {}
    for line in (final / "claims.jsonl").read_bytes().splitlines():
        if line:
            record = _json_object(line)
            cid = record.get("id")
            if not isinstance(cid, str) or not cid or cid in claim_records:
                raise EvaluationError("claim ledger has missing or duplicate IDs")
            claim_records[cid] = record
    for cid in changed:
        if cid not in claim_records:
            raise EvaluationError("changed claim missing from ledger")
        def descends(candidate: str, target: str, visited: set[str]) -> bool:
            pending = [candidate]
            while pending:
                node = pending.pop()
                if node in visited or node not in claim_records:
                    continue
                visited.add(node)
                parents = claim_records[node].get("supersedes", [])
                if not isinstance(parents, list):
                    return False
                if target in parents:
                    return True
                pending.extend(parent for parent in parents if isinstance(parent, str))
            return False
        if not any(descends(active, cid, set()) for active in final_active):
            raise EvaluationError(f"changed claim lacks active successor: {cid}")

    current = r2_manifest
    seen = {r2_id}
    while True:
        current_id = current.get("revision_id")
        for sibling_path in (final / "revisions").glob("*/manifest.json"):
            sibling = json_file(sibling_path)
            if sibling_path.parent.name != current_id and sibling.get("status") == "COMPLETE" and sibling.get("parent_revision_id") == current.get("parent_revision_id"):
                raise EvaluationError("complete sibling fork in selected parent chain")
        parent = current.get("parent_revision_id")
        if parent is None:
            break
        if not isinstance(parent, str) or not re.fullmatch(r"[A-Za-z0-9._-]+", parent) or parent in seen:
            raise EvaluationError("unsafe or cyclic parent revision ID")
        seen.add(parent)
        parent_path = final / "revisions" / parent / "manifest.json"
        no_links(parent_path, final)
        if not beneath(parent_path, final):
            raise EvaluationError("parent manifest escapes final case")
        parent_manifest = json_file(parent_path)
        if current.get("parent_manifest_sha256") != sha(parent_path):
            raise EvaluationError("parent-chain digest mismatch")
        current = parent_manifest
    if current.get("revision_id") != old_id:
        raise EvaluationError("R2 chain does not end at frozen R1")
    append_only = {"activity.jsonl", "approvals.jsonl", "claims.jsonl", "evidence.jsonl", "sources.jsonl"}
    immutable = {f"revisions/{old_id}/{name}" for name in ("options.md", "decision.md", "strategy-product.md", "strategy-communication.md", "test-plan.md", "state.md", "manifest.json")}
    immutable.update(entry["path"] for entry in old_manifest.get("files", []) if isinstance(entry, dict) and isinstance(entry.get("path"), str) and entry["path"] not in append_only)
    for rel in immutable:
        old_file = before / rel
        for tree in (interrupted, final):
            target = tree / rel
            if not old_file.is_file() or not target.is_file() or sha(old_file) != sha(target):
                raise EvaluationError(f"pre-resume immutable record changed: {rel}")
    for rel in append_only:
        records = {}
        for tree in (before, interrupted, final):
            ledger = tree / rel
            records[tree] = ledger.read_bytes() if ledger.exists() else None
            if records[tree] is not None:
                for payload in records[tree].splitlines():
                    if payload:
                        _json_object(payload)
        for previous, following in ((before, interrupted), (interrupted, final)):
            old_bytes, new_bytes = records[previous], records[following]
            if old_bytes is None:
                continue
            if new_bytes is None:
                raise EvaluationError(f"append-only ledger missing: {rel}")
            if not new_bytes.startswith(old_bytes):
                raise EvaluationError(f"pre-resume ledger prefix changed: {rel}")
            if (len(new_bytes) > len(old_bytes) and old_bytes and not old_bytes.endswith(b"\n") and
                    not new_bytes.startswith((b"\n", b"\r\n"), len(old_bytes))):
                raise EvaluationError(f"pre-resume ledger lost its record boundary: {rel}")
    attempts = operator.get("attempts")
    if not isinstance(attempts, list) or any(not isinstance(item, dict) for item in attempts):
        raise EvaluationError("attempts must be an ordered list of records")
    ids = [item.get("attempt_id") for item in attempts]
    sequences = [item.get("sequence") for item in attempts]
    if (any(not isinstance(item, str) or not item.strip() for item in ids) or len(ids) != len(set(ids)) or
            any(type(item) is not int or item < 1 for item in sequences) or
            len(sequences) != len(set(sequences)) or sequences != sorted(sequences)):
        raise EvaluationError("attempt IDs and increasing sequence numbers must be unique")
    retry_action = key.get("retry_action")
    if not isinstance(retry_action, str) or not retry_action.strip():
        raise EvaluationError("H1 key must identify the missing-file retry action")
    by_id = dict(zip(ids, attempts))
    matched_retry = False
    for attempt in attempts:
        if not isinstance(attempt.get("action_identity"), str) or not attempt["action_identity"].strip():
            raise EvaluationError("attempt lacks a stable action identity")
        if not isinstance(attempt.get("status"), str) or not attempt["status"].strip():
            raise EvaluationError("attempt lacks an explicit outcome")
        check_source_citation(attempt.get("evidence"), sources, files)
        if attempt["status"] == "successful_retry":
            prior = by_id.get(attempt.get("depends_on_attempt_id"))
            if (not prior or prior.get("status") != "missing_file_error" or
                    prior["sequence"] >= attempt["sequence"] or prior["action_identity"] != attempt["action_identity"]):
                raise EvaluationError("retry must follow its own missing-file failure")
            matched_retry |= attempt["action_identity"] == retry_action
    if not matched_retry:
        raise EvaluationError("required missing-file action has no dependent successful retry")
    actions = operator.get("actions")
    if not isinstance(actions, list) or any(not isinstance(item, dict) for item in actions):
        raise EvaluationError("actions must be a list of execution records")
    execution_ids = [item.get("execution_id") for item in actions]
    if (any(not isinstance(item, str) or not item.strip() for item in execution_ids) or
            len(execution_ids) != len(set(execution_ids))):
        raise EvaluationError("execution IDs must be nonempty and unique")
    allowed = key.get("allowed_actions")
    if (not isinstance(allowed, dict) or any(
            not isinstance(identity, str) or not identity.strip() or not isinstance(scopes, list) or
            not scopes or any(not isinstance(scope, str) or not scope.strip() for scope in scopes)
            for identity, scopes in allowed.items())):
        raise EvaluationError("key must define allowed action identities and exact scopes")
    completed_before = key.get("completed_action_identities")
    if (not isinstance(completed_before, list) or
            any(not isinstance(item, str) or not item.strip() for item in completed_before) or
            len(completed_before) != len(set(completed_before))):
        raise EvaluationError("key must list stable identities completed before resume")
    approvals = {}
    ledger = final / "approvals.jsonl"
    if ledger.is_file():
        for line in ledger.read_bytes().splitlines():
            if line:
                record = _json_object(line)
                approval_id = record.get("approval_id")
                if not isinstance(approval_id, str) or not approval_id.strip() or approval_id in approvals:
                    raise EvaluationError("approval IDs must be nonempty and unique")
                approvals[approval_id] = record
    completed = set()
    for action in actions:
        identity, status = action.get("action_identity"), action.get("status")
        if not isinstance(identity, str) or not identity.strip() or status not in {"completed", "failed", "blocked", "not_run"}:
            raise EvaluationError("action identity or known execution outcome is missing")
        if status != "completed":
            continue
        if identity in completed or identity in completed_before:
            raise EvaluationError("completed action was replayed")
        completed.add(identity)
        approval = approvals.get(action.get("approval_id"))
        scope = action.get("scope")
        if (identity not in allowed or scope not in allowed[identity] or not approval or
                approval.get("action") != identity or approval.get("scope") != scope or
                approval.get("revision_id") != r2_id or approval.get("manifest_sha256") != r2_digest or
                action.get("manifest_sha256") != r2_digest or any(
                    not isinstance(approval.get(field), str) or not approval[field].strip()
                    for field in ("approver", "review_trigger", "conditions"))):
            raise EvaluationError("completed action lacks exact current owned ledger approval")
        basis = approval.get("basis_claim_ids")
        if (not isinstance(basis, list) or not basis or any(not isinstance(item, str) for item in basis) or
                len(basis) != len(set(basis)) or not set(basis).issubset(final_active)):
            raise EvaluationError("approval basis must contain current selected claims")
        approved_at = _timestamp(approval.get("approved_at"), "approved_at")
        completed_at = _timestamp(action.get("completed_at"), "completed_at")
        if not approved_at <= completed_at <= observed_at:
            raise EvaluationError("approval, execution, and observation timestamps disagree")
        expiry = approval.get("expires_at")
        if expiry != "NONE" and _timestamp(expiry, "expires_at") <= completed_at:
            raise EvaluationError("approval was expired when the action executed")
    if not isinstance(operator.get("evidence"), list) or not operator["evidence"]:
        raise EvaluationError("operator observations require evidence locators")
    for evidence in operator["evidence"]:
        if not isinstance(evidence, dict):
            raise EvaluationError("malformed operator evidence locator")
        check_source_citation(evidence, sources, files)
    return hashes


def evaluate(workspace: Path, key_path: Path, observations_path: Path, reviews_path: Path | None = None) -> dict[str, Any]:
    workspace_arg = Path(workspace).absolute()
    no_links(workspace_arg, Path(workspace_arg.anchor))
    root = workspace_arg.resolve(strict=True)
    if not root.is_dir():
        raise EvaluationError("candidate workspace must be a real directory")
    trusted_args = [Path(p).absolute() for p in (key_path, observations_path, *([reviews_path] if reviews_path else []))]
    for trusted in trusted_args:
        no_links(trusted, Path(trusted.anchor))
        if not trusted.is_file():
            raise EvaluationError("trusted inputs must be existing regular files")
        resolved = trusted.resolve(strict=True)
        if beneath(resolved, root) or resolved == root:
            raise EvaluationError("trusted inputs must be outside candidate workspace")
    key_path, observations_path = trusted_args[:2]
    reviews_path = trusted_args[2] if len(trusted_args) == 3 else None
    key, obs = json_file(key_path), json_file(observations_path)
    if key.get("schema") != SCHEMA or obs.get("schema") != SCHEMA: raise EvaluationError("unsupported schema")
    case = key.get("case")
    if case not in CASES: raise EvaluationError("unsupported case")
    raw_arg = Path(key["raw_root"]).absolute()
    inventory_arg = Path(key["inventory"]).absolute()
    no_links(raw_arg, Path(raw_arg.anchor))
    no_links(inventory_arg, Path(inventory_arg.anchor))
    raw_root, invpath = raw_arg.resolve(strict=True), inventory_arg.resolve(strict=True)
    if not raw_root.is_dir() or not invpath.is_file() or beneath(raw_root, root) or beneath(root, raw_root):
        raise EvaluationError("raw root and candidate must be existing disjoint locations")
    if beneath(invpath, root) or beneath(invpath, raw_root):
        raise EvaluationError("trusted inventory must be external to candidate and raw roots")
    if any(invpath == p.resolve(strict=True) for p in trusted_args):
        raise EvaluationError("inventory may not alias key, observations, or reviews")
    sources = source_map(json_file(invpath), raw_root)
    for sid, (source_path, _) in sources.items():
        copied = root / "raw" / source_path.relative_to(raw_root)
        no_links(copied, root)
        if not copied.is_file() or sha(copied) != sha(source_path):
            raise EvaluationError(f"candidate raw copy is missing or differs from pinned source: {sid}")
    files = {}
    hashes = {}
    for p in root.rglob("*"):
        no_links(p, root)
        if not beneath(p, root):
            raise EvaluationError(f"candidate output escapes workspace: {p}")
        if p.is_file():
            rel = p.relative_to(root).as_posix()
            if p.suffix.lower() in {".md", ".txt", ".csv", ".json", ".jsonl", ".html"}:
                try: files[rel] = p.read_text(encoding="utf-8").splitlines()
                except (OSError, UnicodeError): continue
            hashes[rel] = sha(p)
    facts = obs.get("facts")
    if not isinstance(facts, dict) or set(facts) != REQUIRED[case]: raise EvaluationError("observations must provide exact mandatory fact IDs")
    for value in facts.values():
        if not isinstance(value, dict) or value.get("kind") != "output":
            raise EvaluationError("each fact must bind a candidate output quote")
        check_source_citation(value, sources, files)
        citation = value.get("source")
        if not isinstance(citation, dict) or citation.get("kind") != "source":
            raise EvaluationError("each fact must contain a source citation")
        check_source_citation(citation, sources, files)
    expected = key.get("expected")
    if not isinstance(expected, dict) or set(expected) != REQUIRED[case]:
        raise EvaluationError("trusted key must define the complete fixed fact set")
    if case == "F2":
        primary = key.get("primary_sources")
        if not isinstance(primary, dict) or set(primary) != REQUIRED["F2"]:
            raise EvaluationError("F2 key must pin a primary citation for every required term")
        for field, locator in primary.items():
            if not isinstance(locator, dict) or locator.get("kind") != "source" or facts[field].get("source") != locator:
                raise EvaluationError(f"F2 fact is not bound to its pinned primary term citation: {field}")
    checks = []
    def add(cid: str, passed: bool, detail: str) -> None:
        checks.append({"id": cid, "status": "PASS" if passed else "FAIL", "detail": detail})
    def compare_expected(fields: set[str]) -> None:
        for field in fields:
            matched = type(facts[field].get("value")) is type(expected[field]) and facts[field]["value"] == expected[field]
            add("KEY_" + field.upper(), matched, "matches pinned typed atom" if matched else "differs from pinned key")
    h1_hashes: dict[str, str] = {}
    add("ARTIFACT_BINDING", True, "All observed facts bind exact output quotes and pinned source citations.")
    if case == "F1":
        raw = [v[0] for v in sources.values() if v[0].name == "cohorts.csv"]
        if len(raw) != 1: raise EvaluationError("F1 requires one pinned cohorts.csv")
        calc = compute_f1(raw[0])
        numeric = set(calc)
        for k, v in calc.items():
            try: add("F1_"+k.upper(), decimal(facts[k]["value"]) == decimal(v), f"recomputed={v}")
            except (KeyError, EvaluationError): add("F1_"+k.upper(), False, "required numeric result missing")
        for k in REQUIRED[case]-numeric: add("F1_"+k.upper(), facts[k].get("value") is not None, "curated source fact observed")
    elif case == "F2":
        from datetime import date
        if not isinstance(expected["decision_date"], str):
            raise EvaluationError("F2 decision date must be ISO text")
        try:
            decision = date.fromisoformat(expected["decision_date"])
            published = date.fromisoformat(expected["v3_published"])
            v2_start = date.fromisoformat(expected["v2_effective"])
            v3_start = date.fromisoformat(expected["v3_effective"])
        except (TypeError, ValueError) as e:
            raise EvaluationError("F2 dates must be valid ISO calendar dates") from e
        if not (v2_start <= decision < v3_start and published <= decision):
            raise EvaluationError("F2 governing version is not effective on decision date")
        for field in REQUIRED[case]:
            value = expected[field]
            if value is None or isinstance(value, bool) and field not in {"budget_or_unknown"}:
                raise EvaluationError(f"F2 key has invalid typed atom: {field}")
            if type(facts[field].get("value")) is not type(value) or facts[field]["value"] != value:
                add("F2_" + field.upper(), False, "observed term differs from pinned governing key")
            else:
                add("F2_" + field.upper(), True, "matches pinned governing key")
        if expected["budget_or_unknown"] != "UNKNOWN":
            add("F2_ECONOMICS_UNKNOWN", False, "economics must remain UNKNOWN absent evidence")
    elif case == "F3":
        rows = []
        for p, lines in ((p, p.read_text(encoding="utf-8").splitlines()) for p,_ in sources.values() if p.name == "economics.csv"):
            import csv
            rows.extend(csv.DictReader(lines))
        if len(rows) != 2: raise EvaluationError("F3 requires two pinned economics rows")
        data = {r["item"]:r for r in rows}
        if set(data) != {"max_validation_budget","net_contribution"}: raise EvaluationError("unsupported F3 economics names")
        a,b=data["max_validation_budget"],data["net_contribution"]
        if a["unit"] != "RUB" or b["unit"] != "RUB_per_paid_shop_month" or a["status"] != "SYNTHETIC_SCENARIO" or b["status"] != "SYNTHETIC_SCENARIO":
            raise EvaluationError("invalid F3 units or evidence status")
        cost, contribution = decimal(a["value"]), decimal(b["value"])
        if cost <= 0 or contribution <= 0:
            raise EvaluationError("F3 cost and contribution must be positive")
        calc = cost / contribution
        if decimal(expected["scenario_cost"]) != cost or decimal(expected["budget"]) != cost or decimal(expected["scenario_contribution"]) != contribution:
            raise EvaluationError("F3 key cost/contribution differ from pinned raw CSV")
        if expected["scenario_status"] != a["status"] or expected["ratio_unit"] != "paid_shop_months":
            raise EvaluationError("F3 key status or ratio unit is invalid")
        if expected["demand_unknown"] != "UNKNOWN" or expected["payback_unknown"] != "UNKNOWN":
            raise EvaluationError("F3 demand and payback must remain UNKNOWN")
        for field in REQUIRED[case]:
            observed = facts[field].get("value")
            if field == "ratio":
                matched = decimal(observed) == calc and decimal(expected[field]) == calc
            else:
                matched = type(observed) is type(expected[field]) and observed == expected[field]
            add("F3_" + field.upper(), matched, "matches recomputed/pinned value" if matched else "differs from recomputed/pinned value")
    else:
        try:
            h1_hashes = h1_structure(obs, key, root, sources, files)
            operator = obs["operator"]
            if operator.get("captured_hashes") != h1_hashes or operator.get("host_attested") is not True:
                raise EvaluationError("operator evidence hashes or independent host attestation missing")
            if operator.get("checkpoint_outcome") not in {"old_selector", "conflict_recorded"}:
                raise EvaluationError("interrupted checkpoint outcome is not recorded")
            for evidence in operator.get("evidence", []):
                check_source_citation(evidence, sources, files)
            add("H1_PARENT_CHAIN", True, "R1/R2 lineage, digests, and preservation checks passed")
            add("H1_OPERATOR", True, "operator observations are hash-bound; not proof of host enforcement")
        except (KeyError, OSError, ProtocolError, EvaluationError, TypeError) as e:
            h1_hashes = {}
            add("H1_PARENT_CHAIN", False, str(e))
        for field in REQUIRED[case]:
            add("H1_" + field.upper(), facts[field].get("value") == expected[field],
                "matches operator key" if facts[field].get("value") == expected[field] else "differs from operator key")
    compare_expected(REQUIRED[case] - (set(calc) if case == "F1" else ({"ratio"} if case == "F3" else set())))
    statuses = [c["status"] for c in checks]
    machine = "FAIL" if "FAIL" in statuses else "REVIEW_REQUIRED"
    checks.sort(key=lambda check: check["id"])
    digest_payload={"case":case,"key":sha(key_path),"observations":sha(observations_path),"sources":{k:sha(v[0]) for k,v in sorted(sources.items())},"outputs":dict(sorted(hashes.items())),"h1_snapshots":dict(sorted(h1_hashes.items())),"checks":checks}
    digest=hashlib.sha256(json.dumps(digest_payload,sort_keys=True,separators=(",",":"),default=str).encode()).hexdigest()
    review_state="REVIEW_REQUIRED"
    veto = False
    if reviews_path:
        try:
            review=json_file(reviews_path)
            if review.get("digest")!=digest: raise EvaluationError("stale review digest")
            reviewers=review.get("reviews")
            if isinstance(reviewers, list):
                for reviewer in reviewers:
                    if not isinstance(reviewer, dict):
                        continue
                    veto |= reviewer.get("verdict") == "FAIL" or reviewer.get("p0") is True
                    semantic = reviewer.get("semantic_checks")
                    if isinstance(semantic, list):
                        veto |= any(isinstance(item, dict) and item.get("status") == "FAIL" for item in semantic)
            semantic_ids = {
                "F1": {"d30_correct", "mix_interpretation", "cause_not_claimed", "proposal_supported"},
                "F2": {"effective_terms", "segment_region", "message_supported", "economics_unknown"},
                "F3": {"scenario_not_fact", "ratio_unit", "capability_bounded", "demand_unknown"},
                "H1": {"context_restored", "new_terms_applied", "unaffected_preserved", "missing_reverse_link", "directive_refusal", "approval_invalidation", "no_repeated_action", "host_attestation"},
            }[case]
            valid=True
            if not isinstance(reviewers,list) or len(reviewers)<2 or any(not isinstance(r,dict) for r in reviewers):
                raise EvaluationError("two distinct reviewers required")
            if (any(not isinstance(r.get("reviewer_id"), str) or not r["reviewer_id"].strip() for r in reviewers) or
                    len({r["reviewer_id"].strip().casefold() for r in reviewers}) != len(reviewers)):
                raise EvaluationError("reviewer IDs must be distinct after normalization")
            for r in reviewers:
                if r.get("kind")!="human" or r.get("case")!=case or r.get("verdict") not in {"PASS","FAIL"}:
                    valid=False
                if type(r.get("p0")) is not bool:
                    valid=False
                if r.get("verdict")=="FAIL" or r.get("p0") is True: veto=True
                rubric=r.get("rubric",[])
                if not isinstance(rubric,list) or len(rubric)!=4 or any(type(x)is not int or x<0 or x>2 for x in rubric) or 0 in rubric or sum(rubric)<6:
                    valid=False
                semantic=r.get("semantic_checks")
                if not isinstance(semantic,list) or len(semantic) != len(semantic_ids) or {x.get("id") for x in semantic if isinstance(x,dict)} != semantic_ids:
                    valid=False
                    continue
                for item in semantic:
                    if item.get("status") == "FAIL": veto=True
                    if item.get("status") not in {"PASS","FAIL"} or not isinstance(item.get("evidence"),dict):
                        valid=False
                    else:
                        validate_locator(item["evidence"],sources,files)
            review_state="FAIL" if veto else ("PASS" if valid and machine!="FAIL" else "REVIEW_REQUIRED")
        except (EvaluationError, KeyError, TypeError, AttributeError): review_state="FAIL" if veto else "REVIEW_REQUIRED"
    final="FAIL" if machine=="FAIL" or review_state=="FAIL" else review_state
    return {"schema":SCHEMA,"case":case,"status":final,"machine_status":machine,"evaluation_digest":digest,"checks":checks,"input_hashes":{"key":sha(key_path),"observations":sha(observations_path),"sources":{k:sha(v[0]) for k,v in sources.items()}},"artifact_hashes":hashes,"scope":"offline synthetic artifact evaluation; human extraction and host actions are not proved","limits":["not an LLM judge or host isolation proof","semantic entailment is not machine-verifiable"]}

def atomic_report(path: Path, report: dict) -> None:
    path = Path(path).absolute()
    no_links(path, Path(path.anchor))
    if path.exists():
        raise EvaluationError("report already exists; choose a fresh path")
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(report, handle, sort_keys=True, indent=2, ensure_ascii=False)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        # A sibling hard link publishes complete bytes atomically without
        # replacing a concurrently created report. Unsupported filesystems block.
        os.link(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)

def stage(product: Path, raw_root: Path, inventory_path: Path, destination: Path) -> dict[str, Any]:
    product_arg, raw_arg = Path(product).absolute(), Path(raw_root).absolute()
    inventory_arg, destination_arg = Path(inventory_path).absolute(), Path(destination).absolute()
    for path in (product_arg, raw_arg, inventory_arg, destination_arg):
        no_links(path, Path(path.anchor))
    product, raw_root = product_arg.resolve(strict=True), raw_arg.resolve(strict=True)
    inventory_path = inventory_arg.resolve(strict=True)
    destination = destination_arg.resolve(strict=False)
    if not product.is_dir() or not raw_root.is_dir() or not inventory_path.is_file():
        raise EvaluationError("product/raw roots must be directories and inventory a file")
    if inventory_path == product or beneath(inventory_path, product) or inventory_path == raw_root or beneath(inventory_path, raw_root):
        raise EvaluationError("trusted inventory must be external to product and raw roots")
    if destination.exists() or beneath(destination, product) or beneath(destination, raw_root) or beneath(product, raw_root) or beneath(raw_root, product):
        raise EvaluationError("destination must be fresh and all roots disjoint")
    if beneath(inventory_path, destination) or beneath(destination, inventory_path):
        raise EvaluationError("destination may not overlap trusted inventory file")
    inventory = json_file(inventory_path)
    sources = source_map(inventory, raw_root)
    allowed = ("AGENTS.md", ".agents/skills", "references", "prompts/first-run.md", "cases/_template")
    plan: list[tuple[Path, Path]] = []
    for name in allowed:
        src = product / name
        if not src.exists():
            raise EvaluationError(f"required staging input missing: {name}")
        paths = [src] if src.is_file() else [src, *sorted(src.rglob("*"))]
        for path in paths:
            no_links(path, product)
            if not beneath(path, product):
                raise EvaluationError("staging input escapes product root")
            if path.is_file():
                plan.append((path, destination / path.relative_to(product)))
    for entry in inventory["sources"]:
        rel = safe_relative(entry["path"])
        src = raw_root / rel
        no_links(src, raw_root)
        if not beneath(src, raw_root) or not src.is_file():
            raise EvaluationError("raw source path escapes root or is not a file")
        plan.append((src, destination / "raw" / rel))
    names = [target.relative_to(destination).as_posix().casefold() for _, target in plan]
    if len(names) != len(set(names)) or any(
        PurePosixPath(left) in PurePosixPath(right).parents
        for left in names for right in names if left != right
    ):
        raise EvaluationError("staging output collision or file/directory alias")
    destination.mkdir(parents=True)
    for src, target in plan:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, target)
    return {"status": "STAGED", "destination": str(destination), "files": len(plan)}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Evaluate pinned candidate artifacts offline; never runs an agent.")
    sub = parser.add_subparsers(dest="command", required=True)
    st = sub.add_parser("stage", help="Create a minimal product workspace from an explicit allowlist")
    st.add_argument("--product", type=Path, required=True)
    st.add_argument("--raw-root", type=Path, required=True)
    st.add_argument("--inventory", type=Path, required=True)
    st.add_argument("--destination", type=Path, required=True)
    ev = sub.add_parser("evaluate", help="Evaluate candidate artifacts against external trusted inputs")
    ev.add_argument("--workspace", type=Path, required=True)
    ev.add_argument("--key", type=Path, required=True)
    ev.add_argument("--observations", type=Path, required=True)
    ev.add_argument("--reviews", type=Path)
    ev.add_argument("--report", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.command == "stage":
            result = stage(args.product, args.raw_root, args.inventory, args.destination)
            print(json.dumps(result, sort_keys=True))
            return 0
        report = evaluate(args.workspace, args.key, args.observations, args.reviews)
        if args.report:
            if beneath(args.report, args.workspace):
                raise EvaluationError("report must be outside candidate workspace")
            atomic_report(args.report, report)
        print(json.dumps(report, sort_keys=True, indent=2, default=str))
        return {"PASS": 0, "FAIL": 1, "BLOCKED": 2, "REVIEW_REQUIRED": 3}[report["status"]]
    except (OSError, ValueError, EvaluationError, ProtocolError, KeyError, TypeError) as e:
        print(json.dumps({"schema": SCHEMA, "status": "BLOCKED", "error": str(e)}, sort_keys=True), file=sys.stderr)
        return 2

if __name__=="__main__":
    raise SystemExit(main())
