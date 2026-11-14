#!/usr/bin/env python3
"""Check repository-facing Markdown targets and case JSON/JSONL syntax.

This is a maintenance harness, not a product behavior or schema validator.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_FILES = [
    ROOT / "README.md",
    ROOT / "AGENTS.md",
    ROOT / "docs",
    ROOT / "cases",
    ROOT / "references",
    ROOT / ".agents",
    ROOT / "prompts" / "first-run.md",
    ROOT / "research" / "README.md",
]
LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)\s]+)(?:\s+[^)]*)?\)")


def markdown_files() -> list[Path]:
    files: set[Path] = set()
    for item in MARKDOWN_FILES:
        if item.is_file() and item.suffix.lower() == ".md":
            files.add(item)
        elif item.is_dir():
            files.update(path for path in item.rglob("*.md") if ".git" not in path.parts)
    return sorted(files)


def check_markdown_links() -> list[str]:
    errors: list[str] = []
    for source in markdown_files():
        for line_number, line in enumerate(source.read_text(encoding="utf-8").splitlines(), 1):
            if line.lstrip().startswith("```"):
                continue
            for match in LINK.finditer(line):
                target = match.group(1).strip("<>")
                parsed = urlsplit(target)
                if parsed.scheme or target.startswith("//"):
                    continue
                path = unquote(parsed.path)
                destination = (source.parent / path).resolve() if path else source.resolve()
                if not destination.exists():
                    errors.append(f"{source.relative_to(ROOT)}:{line_number}: missing link target {path or '#'}")
    return errors


def check_case_json() -> list[str]:
    errors: list[str] = []
    result = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files", "-z", "--", "cases"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    tracked = (
        ROOT / path.decode("utf-8")
        for path in result.stdout.split(b"\0")
        if path.endswith((b".json", b".jsonl"))
    )
    for source in sorted(tracked):
        try:
            with source.open(encoding="utf-8") as handle:
                if source.suffix == ".json":
                    json.load(handle)
                else:
                    for line_number, line in enumerate(handle, 1):
                        if line.strip():
                            try:
                                json.loads(line)
                            except json.JSONDecodeError as error:
                                errors.append(f"{source.relative_to(ROOT)}:{line_number}: {error}")
        except (OSError, UnicodeError, json.JSONDecodeError) as error:
            errors.append(f"{source.relative_to(ROOT)}: {error}")
    return errors


def main() -> int:
    try:
        errors = check_markdown_links() + check_case_json()
    except subprocess.CalledProcessError as error:
        print(f"Repository integrity check: FAIL (git ls-files exited {error.returncode})")
        return 1
    if errors:
        print("Repository integrity check: FAIL")
        print("\n".join(errors))
        return 1
    print(f"Repository integrity check: PASS ({len(markdown_files())} Markdown files; indexed case JSON/JSONL syntax)")
    print("Scope: file targets only; no schema, hash, fragment, external-link, product, or host validation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
