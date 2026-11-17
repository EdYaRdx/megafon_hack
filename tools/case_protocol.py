#!/usr/bin/env python3
"""Shared read-only checkpoint classifier and pre-selection compatibility check."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

PROTOCOL_ID = "checkpoint-v1"
CHECKPOINT_STATES = {"UNINITIALIZED", "CHECKPOINTING", "CHECKPOINTED"}
LEGACY_CASES = {
    "fresh-start-demo",
    "meal-planner-demo",
    "offer-terms-demo",
    "public-source-retention-smoke",
    "resume-failure-demo",
    "retention-demo",
    "retention-f1-demo",
    "service-launch-f3",
    "source-injection-demo",
    "unseen-shelf-alerts-20261114",
}
REQUIRED_SNAPSHOTS = {
    "options.md",
    "decision.md",
    "strategy-product.md",
    "strategy-communication.md",
    "test-plan.md",
    "state.md",
}
APPEND_ONLY_LEDGER_PATHS = frozenset(
    {
        "sources.jsonl",
        "evidence.jsonl",
        "claims.jsonl",
        "activity.jsonl",
        "approvals.jsonl",
    }
)
CLAIM_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]*$")


class ProtocolError(ValueError):
    """Raised when a case cannot be safely classified or resumed."""


def _json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ProtocolError(f"invalid or unreadable JSON: {path.name}") from error
    if not isinstance(value, dict):
        raise ProtocolError(f"expected JSON object: {path.name}")
    return value


def _sha256(path: Path) -> str:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError as error:
        raise ProtocolError(f"unreadable file: {path}") from error


def _is_json_object_record(record: bytes) -> bool:
    if not record:
        return False
    try:
        value = json.loads(record)
    except (UnicodeDecodeError, json.JSONDecodeError):
        return False
    return isinstance(value, dict)


def _append_only_ledger_prefix(path: Path, expected_sha256: str) -> bytes | None:
    """Return the exact checkpointed bytes at a complete JSONL record boundary."""
    try:
        data = path.read_bytes()
    except OSError as error:
        raise ProtocolError(f"unreadable file: {path}") from error

    digest = hashlib.sha256()
    if digest.hexdigest() == expected_sha256:
        return b""

    record_start = 0
    for position, byte in enumerate(data):
        if byte != 0x0A:
            continue
        record = data[record_start:position]
        if not _is_json_object_record(record):
            return False

        without_separator = digest.copy()
        without_separator.update(record)
        if without_separator.hexdigest() == expected_sha256:
            return data[:position]

        # CRLF is one record separator too. Preserve exact checkpoint bytes:
        # the frozen final JSON record may omit both bytes of that separator.
        if record.endswith(b"\r"):
            before_crlf = digest.copy()
            before_crlf.update(record[:-1])
            if before_crlf.hexdigest() == expected_sha256:
                return data[: position - 1]

        digest.update(record)
        digest.update(b"\n")
        if digest.hexdigest() == expected_sha256:
            return data[: position + 1]
        record_start = position + 1

    final_record = data[record_start:]
    if final_record and _is_json_object_record(final_record):
        digest.update(final_record)
        if digest.hexdigest() == expected_sha256:
            return data
    return None


def _validate_checkpoint_claims(prefix: bytes, active_claims: list[str]) -> None:
    """Validate claim identity and explicit selection against one pinned JSONL prefix."""
    claims: dict[str, dict] = {}
    for line_number, raw_record in enumerate(prefix.splitlines(), start=1):
        try:
            record = json.loads(raw_record)
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ProtocolError(f"invalid claim record in checkpoint ledger at line {line_number}") from error
        if not isinstance(record, dict):
            raise ProtocolError(f"invalid claim record in checkpoint ledger at line {line_number}")
        claim_id = record.get("id")
        if not isinstance(claim_id, str) or not CLAIM_ID.fullmatch(claim_id):
            raise ProtocolError(f"invalid claim ID in checkpoint ledger at line {line_number}")
        if claim_id in claims:
            raise ProtocolError(f"duplicate claim ID in checkpoint ledger: {claim_id}")
        supersedes = record.get("supersedes", [])
        if not isinstance(supersedes, list) or any(
            not isinstance(item, str) or not CLAIM_ID.fullmatch(item) for item in supersedes
        ) or len(supersedes) != len(set(supersedes)):
            raise ProtocolError(f"invalid supersedes list for claim: {claim_id}")
        if claim_id in supersedes:
            raise ProtocolError(f"claim supersedes itself: {claim_id}")
        claims[claim_id] = record

    if not prefix and active_claims:
        missing = active_claims[0]
        raise ProtocolError(f"active claim is absent from checkpoint claims ledger: {missing}")
    for claim_id in active_claims:
        if claim_id not in claims:
            raise ProtocolError(f"active claim is absent from checkpoint claims ledger: {claim_id}")

    parents: dict[str, list[str]] = {}
    for claim_id, record in claims.items():
        claim_parents = record.get("supersedes", [])
        for parent_id in claim_parents:
            if parent_id not in claims:
                raise ProtocolError(f"supersedes references missing claim ID: {parent_id}")
        parents[claim_id] = claim_parents

    ancestors: dict[str, set[str]] = {}
    for claim_id in claims:
        visited: set[str] = set()
        pending = list(parents[claim_id])
        while pending:
            parent_id = pending.pop()
            if parent_id == claim_id:
                raise ProtocolError("cycle in checkpoint claim supersedes graph")
            if parent_id in visited:
                continue
            visited.add(parent_id)
            pending.extend(parents[parent_id])
        ancestors[claim_id] = visited

    active = set(active_claims)
    if any(ancestors[claim_id] & active for claim_id in active_claims):
        raise ProtocolError("active claims conflict with supersedes graph")

    successors: dict[str, list[str]] = {claim_id: [] for claim_id in claims}
    for claim_id, claim_parents in parents.items():
        for parent_id in claim_parents:
            successors[parent_id].append(claim_id)
    for claim_id, direct_successors in successors.items():
        if len(direct_successors) > 1 and not any(
            successor == active_id or successor in ancestors[active_id]
            for active_id in active
            for successor in direct_successors
        ):
            raise ProtocolError(f"unresolved claim successor fork: {claim_id}")


def _markdown_selection(path: Path, label: str) -> tuple[str, list[str], str | None]:
    try:
        content = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise ProtocolError(f"missing or unreadable {label}") from error
    revision_match = re.search(
        r"(?m)^- (?:Active complete revision ID:|\*\*Revision:\*\*)\s*"
        r"`?(?P<revision>[A-Za-z0-9._-]+)`?"
        r"(?:\s+\(parent\s+`?(?P<inline_parent>[A-Za-z0-9._-]+)`?\))?\s*$",
        content,
    )
    claims_match = re.search(
        r"(?m)^- (?:Current claim IDs \(active successors only; match manifest\):|\*\*Active claim IDs:\*\*)\s*(.*?)\s*$",
        content,
    )
    if not revision_match or not claims_match:
        raise ProtocolError(f"{label} does not declare revision and active claims")
    raw_claims = claims_match.group(1).strip()
    claims = [] if raw_claims in {"", "none", "NONE", "[]"} else [item.strip().strip("`") for item in raw_claims.split(",")]
    if any(not CLAIM_ID.fullmatch(item) for item in claims) or len(claims) != len(set(claims)):
        raise ProtocolError(f"invalid active claims in {label}")

    parent_ids = re.findall(
        r"(?m)^- (?:Parent revision ID:|\*\*Parent revision:\*\*)\s*"
        r"`?([A-Za-z0-9._-]+)`?(?:\s+\([^\n]*\))?\s*$",
        content,
    )
    inline_parent = revision_match.group("inline_parent")
    if inline_parent is not None:
        parent_ids.append(inline_parent)
    if len(set(parent_ids)) > 1:
        raise ProtocolError(f"{label} declares conflicting parent revisions")
    return revision_match.group("revision"), claims, parent_ids[0] if parent_ids else None


def _check_protocol_id(path: Path, label: str) -> None:
    try:
        content = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise ProtocolError(f"missing or unreadable {label}") from error
    if not re.search(r"(?m)^- Case protocol: `checkpoint-v1`(?:\s|$)", content):
        raise ProtocolError(f"{label} does not repeat the protocol identity")


def _validate_revision(
    case_dir: Path,
    revision_id: str,
    *,
    expected_manifest_sha256: str | None = None,
    require_parent_digest: bool = False,
) -> dict:
    """Validate one immutable revision and its pinned dependencies."""
    revisions_dir = case_dir / "revisions"
    manifest_path = revisions_dir / revision_id / "manifest.json"
    if not manifest_path.is_file():
        raise ProtocolError("selected manifest is missing or hash-mismatched")
    if expected_manifest_sha256 is not None and _sha256(manifest_path) != expected_manifest_sha256:
        raise ProtocolError("selected manifest is missing or hash-mismatched")
    manifest = _json(manifest_path)
    if manifest.get("revision_id") != revision_id or manifest.get("status") != "COMPLETE":
        raise ProtocolError("selected manifest identity/status is invalid")
    parent_id = manifest.get("parent_revision_id")
    if parent_id is not None and (
        not isinstance(parent_id, str) or not re.fullmatch(r"[A-Za-z0-9._-]+", parent_id)
    ):
        raise ProtocolError("manifest parent revision ID is malformed")
    if require_parent_digest and parent_id in {".", ".."}:
        raise ProtocolError("manifest parent revision ID is malformed")
    manifest_path = revisions_dir / revision_id / "manifest.json"
    for other in revisions_dir.glob("*/manifest.json"):
        if other != manifest_path:
            sibling = _json(other)
            if sibling.get("status") == "COMPLETE" and sibling.get("parent_revision_id") == parent_id:
                raise ProtocolError("multiple complete revisions share a parent")
    if require_parent_digest:
        parent_hash = manifest.get("parent_manifest_sha256")
        if parent_id is None and parent_hash is not None:
            raise ProtocolError("root manifest must not declare a parent manifest hash")
        if parent_id is not None and (
            not isinstance(parent_hash, str) or not re.fullmatch(r"[0-9a-f]{64}", parent_hash)
        ):
            raise ProtocolError("successor manifest parent_manifest_sha256 is missing or malformed")
    active_claims = manifest.get("active_claim_ids")
    if not isinstance(active_claims, list) or any(not isinstance(item, str) or not CLAIM_ID.fullmatch(item) for item in active_claims) or len(active_claims) != len(set(active_claims)):
        raise ProtocolError("manifest active_claim_ids is missing, invalid, or ambiguous")
    files = manifest.get("files")
    if not isinstance(files, list):
        raise ProtocolError("manifest file list is missing")
    seen: set[str] = set()
    checkpoint_claim_prefix: bytes | None = None
    for entry in files:
        if not isinstance(entry, dict) or not isinstance(entry.get("path"), str) or not isinstance(entry.get("sha256"), str):
            raise ProtocolError("malformed manifest file entry")
        relative = Path(entry["path"])
        if relative.is_absolute() or ".." in relative.parts or entry["path"] in seen:
            raise ProtocolError("unsafe or duplicate manifest path")
        seen.add(entry["path"])
        target = case_dir / relative
        if not target.is_file():
            raise ProtocolError(f"missing or hash-mismatched dependency: {entry['path']}")
        actual_hash = _sha256(target)
        if entry["path"] in APPEND_ONLY_LEDGER_PATHS:
            prefix = _append_only_ledger_prefix(target, entry["sha256"])
            if prefix is None:
                raise ProtocolError(f"missing or hash-mismatched dependency: {entry['path']}")
            if entry["path"] == "claims.jsonl":
                checkpoint_claim_prefix = prefix
        elif actual_hash != entry["sha256"]:
            raise ProtocolError(f"missing or hash-mismatched dependency: {entry['path']}")
    required_paths = {f"revisions/{revision_id}/{name}" for name in REQUIRED_SNAPSHOTS}
    if not required_paths.issubset(seen):
        raise ProtocolError("manifest omits required revision snapshots")
    if active_claims and "claims.jsonl" not in seen:
        raise ProtocolError("manifest omits claims.jsonl required by active claims")
    if "claims.jsonl" in seen:
        _validate_checkpoint_claims(checkpoint_claim_prefix or b"", active_claims)
    for name in (f"revisions/{revision_id}/state.md", f"revisions/{revision_id}/decision.md"):
        if name.endswith("state.md"):
            _check_protocol_id(case_dir / name, "selected state snapshot")
        selected_revision, selected_claims, declared_parent = _markdown_selection(case_dir / name, "selected snapshot")
        if selected_revision != revision_id or selected_claims != active_claims:
            raise ProtocolError("selected snapshot disagrees with selected revision/active claims")
        if declared_parent is not None and declared_parent != parent_id:
            raise ProtocolError("selected snapshot parent revision disagrees with manifest")
    return manifest


def _validate_parent_chain(case_dir: Path, revision_id: str) -> None:
    """Validate every actual ancestor and the exact bytes pinned by each child."""
    seen: set[str] = set()
    child_id = revision_id
    child = _validate_revision(case_dir, child_id, require_parent_digest=True)
    while child.get("parent_revision_id") is not None:
        parent_id = child["parent_revision_id"]
        if parent_id in seen or parent_id == child_id:
            raise ProtocolError("cycle in revision parent chain")
        seen.add(child_id)
        parent_path = case_dir / "revisions" / parent_id / "manifest.json"
        actual_hash = _sha256(parent_path)
        if child.get("parent_manifest_sha256") != actual_hash:
            raise ProtocolError("parent manifest hash is missing or mismatched")
        child_id = parent_id
        child = _validate_revision(
            case_dir, child_id, expected_manifest_sha256=actual_hash, require_parent_digest=True
        )


def classify_case(case_dir: Path, *, repo_root: Path | None = None) -> str:
    """Return FRESH, CHECKPOINTED, or LEGACY; unsafe/ambiguous cases raise ProtocolError."""
    case_dir = Path(case_dir)
    repository = Path(repo_root).resolve() if repo_root is not None else Path(__file__).resolve().parents[1]
    if not case_dir.is_dir():
        raise ProtocolError("case directory is missing")
    marker_path = case_dir / "case-protocol.json"
    selector_path = case_dir / "ACTIVE.json"
    revisions_dir = case_dir / "revisions"
    revision_files = [path for path in revisions_dir.rglob("*") if path.is_file()] if revisions_dir.exists() else []
    manifest_paths = list(revisions_dir.glob("*/manifest.json")) if revisions_dir.exists() else []
    if not marker_path.exists():
        canonical_legacy_path = (repository / "cases" / case_dir.name).resolve()
        if case_dir.name in LEGACY_CASES and case_dir.resolve() == canonical_legacy_path and not selector_path.exists() and not manifest_paths:
            return "LEGACY"
        raise ProtocolError("case protocol identity is absent or case is not on the legacy allowlist")
    marker = _json(marker_path)
    if marker.get("protocol_id") != PROTOCOL_ID or marker.get("checkpoint_state") not in CHECKPOINT_STATES:
        raise ProtocolError("case protocol identity/state is unsupported or ambiguous")
    if not selector_path.exists() and not manifest_paths:
        if marker["checkpoint_state"] == "UNINITIALIZED" and not revision_files:
            return "FRESH"
        raise ProtocolError("checkpoint was started or selected artifacts are incomplete")
    if not selector_path.exists() or not manifest_paths:
        raise ProtocolError("selector or manifest is missing")
    selector = _json(selector_path)
    revision_id = selector.get("revision_id")
    manifest_hash = selector.get("manifest_sha256")
    if not isinstance(revision_id, str) or not re.fullmatch(r"[A-Za-z0-9._-]+", revision_id):
        raise ProtocolError("selector revision_id is missing or malformed")
    if not isinstance(manifest_hash, str):
        raise ProtocolError("selected manifest is missing or hash-mismatched")
    manifest_path = revisions_dir / revision_id / "manifest.json"
    manifest = _validate_revision(case_dir, revision_id, expected_manifest_sha256=manifest_hash)
    for name, label in (("state.md", "root state"), ("decision.md", "root decision")):
        if name == "state.md":
            _check_protocol_id(case_dir / name, label)
        selected_revision, selected_claims, declared_parent = _markdown_selection(case_dir / name, label)
        if selected_revision != revision_id or selected_claims != manifest["active_claim_ids"]:
            raise ProtocolError(f"{label} disagrees with selected revision/active claims")
        if declared_parent is not None and declared_parent != manifest.get("parent_revision_id"):
            raise ProtocolError(f"{label} parent revision disagrees with manifest")
    return "CHECKPOINTED"

def check_candidate(case_dir: Path, revision_id: str) -> dict[str, str]:
    """Validate a prospective selector with the shared consumer, without publishing it."""
    case_dir = Path(case_dir)
    if not re.fullmatch(r"[A-Za-z0-9._-]+", revision_id) or revision_id in {".", ".."}:
        raise ProtocolError("candidate revision ID is malformed")
    active = case_dir / "ACTIVE.json"
    marker = _json(case_dir / "case-protocol.json")
    if marker.get("protocol_id") != PROTOCOL_ID or marker.get("checkpoint_state") not in CHECKPOINT_STATES:
        raise ProtocolError("case protocol identity/state is unsupported or ambiguous")
    current_id = None
    if active.exists() or active.is_symlink():
        selected = _json(active)
        current_id = selected.get("revision_id")
        if not isinstance(current_id, str) or current_id in {".", ".."} or not re.fullmatch(r"[A-Za-z0-9._-]+", current_id):
            raise ProtocolError("selector revision_id is missing or malformed")
        selected_hash = selected.get("manifest_sha256")
        if not isinstance(selected_hash, str):
            raise ProtocolError("selected manifest is missing or hash-mismatched")
        _validate_revision(case_dir, current_id, expected_manifest_sha256=selected_hash)
    else:
        revision_entries = list((case_dir / "revisions").iterdir()) if (case_dir / "revisions").exists() else []
        if any(path.name != revision_id for path in revision_entries):
            raise ProtocolError("selector is missing while other revision artifacts exist")
        if marker.get("checkpoint_state") == "UNINITIALIZED":
            raise ProtocolError("first checkpoint must begin in CHECKPOINTING state")
    current = "FRESH" if current_id is None else "CHECKPOINTED"
    manifest_path = case_dir / "revisions" / revision_id / "manifest.json"
    selector = {"revision_id": revision_id, "manifest_sha256": _sha256(manifest_path)}
    manifest = _validate_revision(
        case_dir, revision_id, expected_manifest_sha256=selector["manifest_sha256"], require_parent_digest=True
    )
    entries = manifest.get("files")
    if isinstance(entries, list):
        for entry in entries:
            if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
                continue
            relative = Path(entry["path"])
            if relative.is_absolute() or ".." in relative.parts:
                continue
            dependency = case_dir / relative
            if dependency.resolve() == active.resolve() or (
                dependency.exists() and active.exists() and dependency.samefile(active)
            ):
                raise ProtocolError("candidate dependency aliases mutable ACTIVE.json")
    if current == "FRESH":
        if manifest.get("parent_revision_id") is not None:
            raise ProtocolError("first candidate must have a null parent")
    else:
        if revision_id != current_id and manifest.get("parent_revision_id") != current_id:
            raise ProtocolError("candidate must extend the selected ACTIVE revision")
    _validate_parent_chain(case_dir, revision_id)
    for name in REQUIRED_SNAPSHOTS:
        try:
            current_view = (case_dir / name).read_bytes()
            snapshot = (case_dir / "revisions" / revision_id / name).read_bytes()
        except OSError as error:
            raise ProtocolError(f"missing current root view: {name}") from error
        if current_view != snapshot:
            raise ProtocolError(f"root current view is stale: {name}")
    # Keep every other manifest and ledger: omitting them would hide forks/history.
    with tempfile.TemporaryDirectory(prefix="checkpoint-v1-") as temporary:
        staged = Path(temporary) / "case"
        shutil.copytree(case_dir, staged, symlinks=True)
        staged_selector = staged / "ACTIVE.json"
        staged_selector.unlink(missing_ok=True)
        staged_selector.write_text(json.dumps(selector), encoding="utf-8")
        if classify_case(staged) != "CHECKPOINTED":
            raise ProtocolError("candidate is not a complete checkpoint")
    return selector


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    classify = commands.add_parser("classify", help="classify the actual case without changing it")
    classify.add_argument("case", type=Path)
    candidate = commands.add_parser(
        "check-candidate", help="check a prospective selector in a temporary copy; do not publish"
    )
    candidate.add_argument("case", type=Path)
    candidate.add_argument("--revision", required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "classify":
            print(classify_case(args.case))
        else:
            selector = check_candidate(args.case, args.revision)
            print(json.dumps({"status": "VALIDATED_CANDIDATE", **selector}))
    except (ProtocolError, OSError, shutil.Error) as error:
        print(f"INCOMPLETE/CONFLICT: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
