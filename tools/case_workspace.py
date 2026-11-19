#!/usr/bin/env python3
"""Case path validation and exclusive template copy; not an agent launcher.

The caller must obtain consent for the exact NEW path and host write permission.
This helper does not grant approval, classify checkpoints or execute Skills.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path


class WorkspaceError(ValueError):
    """The requested workspace operation is unsafe or ambiguous."""


def plain_directory(path: Path) -> None:
    # Junctions are not symlinks on Windows. Never traverse either kind.
    if path.is_symlink() or path.is_junction() or not path.is_dir():
        raise WorkspaceError(f"Expected a real directory, not a link: {path}")


def case_path(project: Path, case: str) -> Path:
    if not re.fullmatch(r"cases/[a-z0-9][a-z0-9-]{0,62}/?", case):
        raise WorkspaceError("Use project-relative cases/<id>: 1-63 lowercase ASCII letters, digits or hyphens")
    name = case.rstrip("/").split("/")[1]
    if name in {"con", "prn", "aux", "nul"} or re.fullmatch(r"(?:com|lpt)[0-9]", name):
        raise WorkspaceError("Reserved Windows directory name")
    project = project.resolve(strict=True)
    plain_directory(project / "cases")
    target = project / "cases" / name
    if target.is_symlink() or target.is_junction():
        raise WorkspaceError("Case root must not be a symlink or junction")
    return target


def existing_case(project: Path, case: str) -> Path:
    target = case_path(project, case)
    plain_directory(target)
    return target


def create_case(project: Path, case: str) -> Path:
    target = case_path(project, case)
    if target.exists():
        raise FileExistsError(f"Path is occupied; no merge or overwrite: {target}")
    template = target.parent / "_template"
    plain_directory(template)
    # Inspect the trusted template before reserving a destination. Copy only
    # regular files/directories, never external links or special files.
    for entry in template.rglob("*"):
        if entry.is_symlink() or entry.is_junction() or not (entry.is_file() or entry.is_dir()):
            raise WorkspaceError(f"Unsupported template entry: {entry}")
    marker = template / "case-protocol.json"
    if not marker.is_file():
        raise WorkspaceError("Template protocol marker is missing")
    # Exclusive mkdir closes the ordinary competing-creator race. Do not use
    # copytree(..., dirs_exist_ok=True), including after a failed partial copy.
    target.mkdir()
    for entry in template.iterdir():
        if entry.name == "case-protocol.json":
            continue
        destination = target / entry.name
        if entry.is_dir():
            shutil.copytree(entry, destination)
        else:
            shutil.copyfile(entry, destination)
    # Publish identity last, after even the marker copy has fully closed.
    # An interrupted copy must not look FRESH to the unchanged classifier.
    pending_marker = target / ".case-protocol.pending"
    shutil.copyfile(marker, pending_marker)
    pending_marker.rename(target / "case-protocol.json")
    return target


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("create", "existing"))
    parser.add_argument("case", help="Exact user-selected project-relative cases/<id>")
    args = parser.parse_args()
    project = Path(__file__).resolve().parents[1]
    try:
        operation = create_case if args.operation == "create" else existing_case
        target = operation(project, args.case)
    except (OSError, WorkspaceError) as error:
        print(json.dumps({"status": "STOP", "error": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 1
    print(json.dumps({"status": "CREATED" if args.operation == "create" else "EXISTS",
                      "case_root": target.relative_to(project).as_posix(),
                      "absolute_case_root": str(target)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
