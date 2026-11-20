#!/usr/bin/env python3
"""One-off release packaging: derive an anonymized case, never rewrite its source.

Only the known three-revision demo is supported. Historical receipts retain source
hashes and results; they are NOT receipts for the derivative. No protocol changes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import tempfile
import re
from pathlib import Path

from tools.case_protocol import (
    APPEND_ONLY_LEDGER_PATHS, _append_only_ledger_prefix,
    check_candidate, classify_case,
)

REVISIONS = {"R0001": "D0001", "R0002": "D0002", "R0003": "D0003"}
EXPECTED_SOURCE = "8b23176b2975081d58721a1dd1cb695899caa29c5496a7ad8e44420cd820ced5"
EXPECTED_INVENTORY = "4c20a0e3e2821cded419618f45dd58d4db543c6c1cff4a7b7fe6e5163223bc62"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def encoded(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def export(source: Path, destination: Path) -> dict:
    source = source.resolve(strict=True)
    destination = destination.absolute()
    if destination.exists() or destination.is_symlink():
        raise ValueError("destination must not exist; never overwrite an export")
    destination = destination.resolve(strict=False)
    if source == destination or source in destination.parents:
        raise ValueError("export must not be inside its source")
    if classify_case(source) != "CHECKPOINTED":
        raise ValueError("source is not CHECKPOINTED")
    check_candidate(source, "R0003")
    selector = json.loads((source / "ACTIVE.json").read_bytes())
    if selector != {"revision_id": "R0003", "manifest_sha256": EXPECTED_SOURCE}:
        raise ValueError("this packager supports only the reviewed source checkpoint")

    # Read-only inventory before creating anything. No links, caches or raw sessions.
    original = {}
    for item in sorted(source.rglob("*")):
        if item.is_symlink() or item.is_junction():
            raise ValueError("links/junctions are not exportable")
        if item.is_file():
            relative = item.relative_to(source).as_posix()
            if any(part in {"__pycache__", ".git", ".local"} for part in item.relative_to(source).parts):
                raise ValueError("unexpected cache/private directory in source")
            original[relative] = item.read_bytes()
    before = {name: sha(data) for name, data in original.items()}
    inventory_bytes = json.dumps(before, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    if sha(inventory_bytes) != EXPECTED_INVENTORY:
        raise ValueError("source inventory differs from the reviewed release input")
    provenance = json.loads(original["inputs/provenance.json"])
    profile_match = re.search(r"[A-Za-z]:[/\\]Users[/\\]([^/\\]+)", provenance["original_path"])
    if not profile_match:
        raise ValueError("expected reviewed profile-path shape is absent")
    profile = profile_match.group(1)

    def text(value: str) -> str:
        # Both JSON-decoded paths and paths inside escaped stdout are covered.
        value = value.replace(profile, "<profile>")
        value = re.sub(r"[A-Za-z]:(?:[/\\]+)Users(?:[/\\]+)<profile>", "<USER_HOME>", value)
        value = re.sub(r"[A-Za-z]:(?:[/\\]+)Projects(?:[/\\]+)GitHub(?:[/\\]+)megafon_hack[-A-Za-z0-9_]*", "<WORKSPACE>", value)
        for old, new in REVISIONS.items():
            value = value.replace(f"revisions/{old}/", f"revisions/{new}/")
        value = re.sub(r"(?m)^(- Active complete revision ID: |\- \*\*Revision:\*\* )R000([123])(?=\s|$)", r"\g<1>D000\2", value)
        value = re.sub(r"(?m)^(- Parent revision ID: |\- \*\*Parent revision:\*\* )R000([123])(?=\s|$)", r"\g<1>D000\2", value)
        return value

    def strings(value: object) -> object:
        if isinstance(value, str):
            # Some receipts store serialized JSON in stdout, including escaped Unicode.
            try:
                nested = json.loads(value)
            except (ValueError, TypeError):
                return text(value)
            if isinstance(nested, (dict, list)):
                changed = strings(nested)
                return value if changed == nested else json.dumps(changed, ensure_ascii=False)
            return text(value)
        if isinstance(value, list):
            return [strings(item) for item in value]
        if isinstance(value, dict):
            return {key: strings(item) for key, item in value.items()}
        return value

    def transform(name: str, data: bytes) -> bytes:
        if name.endswith((".pdf", ".png")):
            return data  # Reviewed educational inputs remain exact source bytes.
        raw = data.decode("utf-8")
        if name.endswith(".jsonl"):
            # Preserve record boundaries and unchanged bytes, including historical prefixes.
            result = []
            for line in raw.splitlines(keepends=True):
                value = json.loads(line)
                changed = strings(value)
                result.append(line if changed == value else json.dumps(changed, ensure_ascii=False, separators=(",", ":")) + ("\n" if line.endswith("\n") else ""))
            return "".join(result).encode("utf-8")
        if name.endswith(".json"):
            value = json.loads(raw)
            changed = strings(value)
            if isinstance(changed, dict) and ("receipt" in name or name.startswith("receipts/")):
                changed = {**changed, "export_notice": "REDACTED SOURCE HISTORY ONLY; not an export execution receipt or approval."}
            return data if changed == value else encoded(changed)
        transformed = text(raw)
        if name.endswith(".md"):
            transformed = (
                "> ANONYMIZED DERIVATIVE. D0001–D0003 are not original R0001–R0003. "
                "Source-history receipts/approvals do not certify or authorize this export; "
                "see CASE-root EXPORT.md and export-map.json.\n\n" + transformed
            )
        return transformed.encode("utf-8")

    def renamed(name: str) -> str:
        for old, new in REVISIONS.items():
            name = name.replace(f"revisions/{old}/", f"revisions/{new}/")
        return name

    # The manifests' pinned scripts are historical inputs, not instructions to execute.
    omitted = {"research/checkpoint.py", "research/R0002-checkpoint.py"}
    outputs = {renamed(name): transform(name, data) for name, data in original.items()
               if name not in omitted and name != "ACTIVE.json" and not re.fullmatch(r"revisions/R000[123]/manifest.json", name)}
    outputs["README.md"] = (
        "# Mobile strategy — anonymized derivative\n\n"
        "This is a release export, NOT the original R0001–R0003. "
        "Read [EXPORT.md](EXPORT.md) before using any receipt or approval.\n\n"
        "D0001 → D0002 → D0003 has an independent hash chain. "
        "Original model use/cost and official PDF provenance remain UNKNOWN.\n\n"
        "- [Readable walkthrough](../../docs/contest-demo.md)\n"
        "- [Product strategy](strategy-product.md)\n"
        "- [Communication strategy](strategy-communication.md)\n"
        "- [Full five-part strategy](strategy.md)\n"
        "- [Decision](decision.md) · [Options](options.md) · [Validation plan](test-plan.md)\n"
        "- [Selected state](state.md) · [Source/export hash mapping](export-map.json)\n\n"
        "Resume from the repository root: `python -m tools.resume_context "
        "cases/mobile-product-strategy-demo`. Then follow the canonical resume Skill; "
        "read D0003 snapshots and inventory drafts separately. Do not run historical "
        "publication/recording scripts or reuse source approvals for this derivative.\n"
    ).encode("utf-8")
    outputs["EXPORT.md"] = (
        "# Derivative export boundary\n\n"
        "User authorized an anonymized derivative on 2026-11-20. "
        "The original case, receipts and R0001–R0003 were not edited. "
        "D0001–D0003 are packaging derivatives, not new research or the original revisions.\n\n"
        "Transformations: profile name/home and workstation checkout paths replaced "
        "with placeholders; revision-directory references and machine control lines "
        "mapped R0001–R0003 to D0001–D0003; manifests/parent hashes/selector recalculated. "
        "JSON receipt annotations distinguish redacted source history from new execution. "
        "The educational PDF and page PNGs are unchanged; organizer provenance UNKNOWN.\n\n"
        "`export-map.json` records source/export hashes and the independent chain. "
        "Source hashes in historical receipts, ledgers, drafts and approvals describe "
        "SOURCE bytes. Resolve transformed files through the mapping, not by treating "
        "the source receipt as a PASS on exported bytes. This mapping is an author's "
        "derivation record, not independent organizer authentication or proof of access "
        "to the private original. Original approvals do NOT bind D0001–D0003 and "
        "authorize no pilot, payment, contact or staffing action here.\n\n"
        "Full current ledgers preserve transformed historical record prefixes. "
        "Historical drafts remain separate, including stale and duplicate material; "
        "never choose by modification time. Historical mutation scripts are inert "
        "source artifacts, not a release launch procedure. Run only shared read-only "
        "checkpoint/inventory tools and reviewed calculation scripts.\n\n"
        "No credentials or raw host sessions are included. Redaction and visible "
        "educational inputs are not a complete DLP certificate. Distribution rights/"
        "official brief identity, video, screenshots and jury access remain release gates.\n"
    ).encode("utf-8")
    chain = []
    for old, new in REVISIONS.items():
        manifest_name = f"revisions/{old}/manifest.json"
        manifest = json.loads(original[manifest_name])
        manifest["revision_id"] = new
        manifest["parent_revision_id"] = REVISIONS.get(manifest["parent_revision_id"])
        if chain:
            manifest["parent_manifest_sha256"] = chain[-1]["export_manifest_sha256"]
        manifest["derivative_export"] = {"source_revision_id": old, "source_manifest_sha256": before[manifest_name],
                                         "notice": "Anonymized derivative, not the original checkpoint; source approvals do not transfer."}
        for entry in manifest["files"]:
            old_path = entry["path"]
            if old_path in APPEND_ONLY_LEDGER_PATHS:
                prefix = _append_only_ledger_prefix(source / old_path, entry["sha256"])
                if prefix is None:
                    raise ValueError("source ledger prefix is unavailable")
                entry["sha256"] = sha(transform(old_path, prefix))
            else:
                entry["sha256"] = sha(outputs[renamed(old_path)])
            entry["path"] = renamed(old_path)
        result = encoded(manifest)
        outputs[f"revisions/{new}/manifest.json"] = result
        chain.append({"source_revision_id": old, "source_manifest_sha256": before[manifest_name],
                      "export_revision_id": new, "export_manifest_sha256": sha(result)})

    for name, data in outputs.items():
        if name.endswith((".pdf", ".png")):
            continue  # Binary educational inputs require the separately documented review.
        value = data.decode("utf-8")
        if profile in value or re.search(r"[A-Za-z]:[/\\]+Users[/\\]+", value):
            raise ValueError(f"personal profile/path remains in export: {name}")
        if re.search(r"BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY|gh[pousr]_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{24,}", value):
            raise ValueError(f"credential-like content in export: {name}")

    destination.mkdir(parents=True, exist_ok=False)
    for name, data in outputs.items():
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    # The multi-revision gate needs a current selector in its disposable copy.
    # The real export is selected only after that gate succeeds.
    active = {"revision_id": "D0003", "manifest_sha256": chain[-1]["export_manifest_sha256"]}
    with tempfile.TemporaryDirectory(prefix="contest-export-gate-") as temporary:
        staged = Path(temporary) / "case"
        shutil.copytree(destination, staged)
        (staged / "ACTIVE.json").write_bytes(encoded(active))
        check_candidate(staged, "D0003")
    (destination / "ACTIVE.json").write_bytes(encoded(active))
    if classify_case(destination) != "CHECKPOINTED":
        raise ValueError("export did not classify CHECKPOINTED")
    if {item.relative_to(source).as_posix() for item in source.rglob("*") if item.is_file()} != set(before):
        raise ValueError("source inventory changed while exporting; do not publish this output")
    for name, digest in before.items():
        if sha((source / name).read_bytes()) != digest:
            raise ValueError("source changed while exporting; do not publish this output")
    files = [{"source_path": name, "source_sha256": before[name], "export_path": renamed(name),
              "export_sha256": sha(outputs[renamed(name)])}
             for name in sorted(original) if renamed(name) in outputs]
    report = {"format": "contest-derivative-v1", "source_checkpoint_sha256": EXPECTED_SOURCE,
              "scope": "Source history is not re-certified. Redacted receipts and approvals refer only to source history, never export execution.",
              "source_files_unchanged": len(before), "omitted_unpinned_scripts": sorted(omitted),
              "revision_mapping": chain, "files": files}
    (destination / "export-map.json").write_bytes(encoded(report))
    return {"status": "DERIVATIVE_CHECKPOINTED", "export_revision_id": "D0003", "export_manifest_sha256": active["manifest_sha256"],
            "source_files_unchanged": len(before), "export_files": len(outputs) + 2}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    print(json.dumps(export(args.source, args.destination), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
