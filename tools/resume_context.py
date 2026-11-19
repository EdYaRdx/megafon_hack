#!/usr/bin/env python3
"""Read-only checkpoint confirmation and unverified saved-work inventory."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import sys
from pathlib import Path, PureWindowsPath

from tools.case_protocol import ProtocolError, REQUIRED_SNAPSHOTS, classify_case
from tools.case_workspace import WorkspaceError, existing_case


def _plain(path: Path) -> os.stat_result:
    info = path.lstat()
    if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0):
        raise ProtocolError(f"link/reparse point not followed: {path.name}")
    return info


def _bounded(case: Path, relative: str) -> Path:
    windows = PureWindowsPath(relative)
    path = Path(relative)
    if path.is_absolute() or windows.drive or windows.root or "\\" in relative or ".." in path.parts:
        raise ProtocolError(f"unsafe case-relative path: {relative}")
    target = case / path
    for component in (*reversed(target.parents), target):
        if component == case or case in component.parents:
            try:
                _plain(component)
            except FileNotFoundError:
                break  # The shared classifier reports missing dependencies.
    return target


def _guard_protocol(case: Path) -> bytes | None:
    """Guard classifier inputs, not drafts: the shared classifier follows paths."""
    for name in ("case-protocol.json", "ACTIVE.json", "state.md", "decision.md"):
        _bounded(case, name)
    selector_path = case / "ACTIVE.json"
    selector_bytes = selector_path.read_bytes() if selector_path.exists() else None
    if selector_bytes is not None:
        try:
            selector = json.loads(selector_bytes)
        except (ValueError, UnicodeError):
            selector = None  # Leave protocol syntax decisions to classify_case.
        if isinstance(selector, dict) and isinstance(selector.get("revision_id"), str):
            _bounded(case, f"revisions/{selector['revision_id']}/manifest.json")
    revisions = _bounded(case, "revisions")
    if not revisions.exists():
        return selector_bytes
    pending = [revisions]
    manifests = []
    while pending:
        directory = pending.pop()
        for child in directory.iterdir():
            info = _plain(child)
            if stat.S_ISDIR(info.st_mode):
                pending.append(child)
            elif child.name == "manifest.json" and child.parent.parent == revisions:
                manifests.append(child)
    for path in manifests:
        try:
            manifest = json.loads(path.read_bytes())
        except (ValueError, UnicodeError):
            continue
        entries = manifest.get("files") if isinstance(manifest, dict) else None
        if isinstance(entries, list):
            for entry in entries:
                if isinstance(entry, dict) and isinstance(entry.get("path"), str):
                    _bounded(case, entry["path"])
    return selector_bytes


def _inventory_drafts(case: Path, unfinished: dict) -> None:
    def issue(path: Path, reason: str) -> None:
        unfinished["discovery"] = "incomplete"
        unfinished["issues"].append({"path": path.relative_to(case).as_posix(), "reason": reason})

    def visit(path: Path) -> None:
        relative = path.relative_to(case).as_posix()
        candidate = {"path": relative, "provenance": "drafts/", "status": "unverified", "relationship_to_selected": "unknown", "completeness": "unknown"}
        try:
            info = _plain(path)
            if stat.S_ISDIR(info.st_mode):
                candidate["kind"] = "directory"
                children = sorted(path.iterdir(), key=lambda item: item.name)
                if not children and path != drafts:
                    unfinished["drafts"].append(candidate)
                    issue(path, "empty directory; completeness unknown")
                for child in children:
                    visit(child)
            elif stat.S_ISREG(info.st_mode):
                candidate["kind"] = "file"
                unfinished["drafts"].append(candidate)
                content = path.read_bytes()
                candidate["bytes"] = len(content)
                candidate["sha256"] = hashlib.sha256(content).hexdigest()
                if not content:
                    issue(path, "empty candidate; completeness unknown")
            else:
                candidate["kind"] = "unknown"
                unfinished["drafts"].append(candidate)
                issue(path, "non-regular entry not read")
        except (OSError, ProtocolError) as error:
            if candidate not in unfinished["drafts"]:
                candidate["kind"] = "unknown"
                unfinished["drafts"].append(candidate)
            issue(path, str(error))

    drafts = case / "drafts"
    try:
        if not stat.S_ISDIR(_plain(drafts).st_mode):
            raise ProtocolError("drafts is not a directory; discovery unknown")
    except FileNotFoundError:
        return
    except (OSError, ProtocolError) as error:
        unfinished["drafts"].append({"path": "drafts", "provenance": "drafts/", "kind": "unknown", "status": "unverified", "relationship_to_selected": "unknown", "completeness": "unknown"})
        issue(drafts, str(error))
        return
    visit(drafts)


def inventory(project: Path, case: str) -> dict:
    """Classify the explicit case before discovering any unfinished candidates."""
    root = existing_case(project, case)
    selector_bytes = _guard_protocol(root)
    classification = classify_case(root, repo_root=project)
    report = {"case": case.rstrip("/"), "classification": classification, "confirmed": None, "unfinished": None}
    if classification != "CHECKPOINTED":
        return report
    if (root / "ACTIVE.json").read_bytes() != selector_bytes:
        raise ProtocolError("selector changed during classification; inventory not scanned")
    selector = json.loads(selector_bytes)
    revision = selector["revision_id"]
    manifest_bytes = (root / "revisions" / revision / "manifest.json").read_bytes()
    if hashlib.sha256(manifest_bytes).hexdigest() != selector["manifest_sha256"]:
        raise ProtocolError("manifest changed during classification; inventory not scanned")
    manifest = json.loads(manifest_bytes)
    report["confirmed"] = {"revision_id": revision, "manifest_sha256": selector["manifest_sha256"], "snapshots": {name: f"revisions/{revision}/{name}" for name in sorted(REQUIRED_SNAPSHOTS)}}
    unfinished = {"discovery": "complete", "drafts": [], "hints": [], "issues": [], "notice": "Candidates and hints are unverified, not selected or necessarily newer. Inspect provenance/content; no referenced paths were followed. Discovery is not an atomic snapshot."}
    report["unfinished"] = unfinished
    _inventory_drafts(root, unfinished)
    pinned = {entry["path"]: entry["sha256"] for entry in manifest["files"]}
    for name in ("state.md", "activity.jsonl"):
        path = root / name
        try:
            _bounded(root, name)
            content = path.read_bytes()
        except FileNotFoundError:
            if name == "activity.jsonl" and name not in pinned:
                continue
            unfinished["discovery"] = "incomplete"
            unfinished["issues"].append({"path": name, "reason": "missing; saved-work hints unknown"})
            continue
        except (OSError, ProtocolError) as error:
            unfinished["discovery"] = "incomplete"
            unfinished["issues"].append({"path": name, "reason": str(error)})
            continue
        expected = pinned[f"revisions/{revision}/state.md"] if name == "state.md" else pinned.get(name)
        if hashlib.sha256(content).hexdigest() == expected or (name == "activity.jsonl" and not content and expected is None):
            continue
        unfinished["hints"].append({"path": name, "provenance": "mutable state" if name == "state.md" else "activity ledger", "status": "unverified", "reason": "differs from selected snapshot" if name == "state.md" else "changed or unpinned activity; not proof of a later draft", "relationship_to_selected": "unknown"})
        if name == "activity.jsonl":
            for number, line in enumerate(content.splitlines(keepends=True), 1):
                try:
                    if not isinstance(json.loads(line), dict):
                        raise ValueError("partial or non-object record")
                except (ValueError, UnicodeError):
                    unfinished["discovery"] = "incomplete"
                    unfinished["issues"].append({"path": name, "line": number, "reason": "malformed/partial activity record; meaning unknown"})
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", help="explicit project-relative cases/<id>")
    args = parser.parse_args(argv)
    try:
        report = inventory(Path(__file__).resolve().parents[1], args.case)
    except (ProtocolError, WorkspaceError, OSError) as error:
        print(f"INCOMPLETE/CONFLICT: {error}", file=sys.stderr)
        return 1
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
