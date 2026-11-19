from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.case_protocol import ProtocolError, classify_case
from tools.case_workspace import WorkspaceError, create_case, existing_case

ROOT = Path(__file__).resolve().parents[1]


class CaseWorkspaceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name)
        shutil.copytree(ROOT / "cases" / "_template", self.project / "cases" / "_template")

    def files(self, root: Path) -> dict[str, bytes]:
        return {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob("*") if p.is_file()}

    def test_new_case_copies_exact_template_and_remains_fresh_not_checkpointed(self) -> None:
        template = self.files(self.project / "cases" / "_template")
        result = create_case(self.project, "cases/retention-1234abcd")
        self.assertEqual(result, self.project / "cases" / "retention-1234abcd")
        self.assertEqual(self.files(result), template)
        self.assertEqual(classify_case(result), "FRESH")
        self.assertEqual((result / "approvals.jsonl").read_bytes(), b"")
        self.assertFalse((result / "ACTIVE.json").exists())
        self.assertEqual(self.files(self.project / "cases" / "_template"), template)

    def test_occupied_directory_or_file_is_never_merged_or_overwritten(self) -> None:
        for is_directory in (True, False):
            with self.subTest(directory=is_directory):
                target = self.project / "cases" / f"occupied-{int(is_directory)}"
                if is_directory:
                    target.mkdir()
                    (target / "private.txt").write_bytes(b"preserve")
                else:
                    target.write_bytes(b"preserve")
                before = self.files(self.project)
                with self.assertRaises(FileExistsError):
                    create_case(self.project, f"cases/{target.name}")
                self.assertEqual(self.files(self.project), before)

    def test_invalid_paths_cannot_create_or_select(self) -> None:
        before = self.files(self.project)
        invalid = ("", "cases", "cases/", "../escape", "cases/../escape", "/cases/x",
                   "C:/cases/x", "cases\\x", "cases/x/child", "cases/_template",
                   "cases/UPPER", "cases/a.b", "cases/a b", "cases/-x", "cases/я",
                   "cases/con", "cases/nul", "cases/com1", "cases/lpt9", "cases/x:ads",
                   "cases/" + "x" * 64)
        for case in invalid:
            for operation in (create_case, existing_case):
                with self.subTest(case=case, operation=operation.__name__):
                    with self.assertRaises(WorkspaceError):
                        operation(self.project, case)
        self.assertEqual(self.files(self.project), before)

    def test_existing_selection_is_read_only_and_does_not_certify_checkpoint(self) -> None:
        target = create_case(self.project, "cases/chosen")
        (self.project / "cases" / "neighbor").mkdir()
        (target / "case-protocol.json").write_bytes(b"broken marker")
        before = self.files(self.project)
        self.assertEqual(existing_case(self.project, "cases/chosen/"), target)
        with self.assertRaises(ProtocolError):
            classify_case(target)
        self.assertEqual(self.files(self.project), before)
        with self.assertRaises(WorkspaceError):
            existing_case(self.project, "cases/missing")
        self.assertFalse((self.project / "cases" / "missing").exists())

    def test_denied_write_stops_without_creating_case(self) -> None:
        # Deterministic permission denial; not a claim about Windows ACL setup.
        before = self.files(self.project)
        with patch.object(Path, "mkdir", side_effect=PermissionError("write denied")):
            with self.assertRaises(PermissionError):
                create_case(self.project, "cases/denied")
        self.assertFalse((self.project / "cases" / "denied").exists())
        self.assertEqual(self.files(self.project), before)

    def test_partial_copy_is_preserved_and_retry_cannot_merge(self) -> None:
        with patch("tools.case_workspace.shutil.copyfile", side_effect=OSError("copy interrupted")):
            with self.assertRaises(OSError):
                create_case(self.project, "cases/partial")
        self.assertTrue((self.project / "cases" / "partial").is_dir())
        with self.assertRaises(FileExistsError):
            create_case(self.project, "cases/partial")

    def test_interrupted_copy_cannot_be_resumed_as_fresh(self) -> None:
        real_copy = shutil.copyfile
        for failure in ("state.md", ".case-protocol.pending"):
            with self.subTest(failure=failure):
                case = f"cases/interrupted-{len(failure)}"
                target = self.project / case

                def interrupted_copy(source, destination, *args, **kwargs):
                    result = real_copy(source, destination, *args, **kwargs)
                    if Path(destination).name == failure:
                        raise OSError("copy failed after writing bytes")
                    return result

                with patch("tools.case_workspace.shutil.copyfile", interrupted_copy):
                    with self.assertRaises(OSError):
                        create_case(self.project, case)
                self.assertFalse((target / "case-protocol.json").exists())
                self.assertEqual(existing_case(self.project, case), target)
                with self.assertRaises(ProtocolError):
                    classify_case(target)
                with self.assertRaises(FileExistsError):
                    create_case(self.project, case)

    def test_competing_creator_wins_without_overwrite(self) -> None:
        real_mkdir = Path.mkdir
        target = self.project / "cases" / "race"

        def competing_mkdir(path: Path, *args, **kwargs):
            if path == target:
                real_mkdir(path)
                (path / "owner.txt").write_bytes(b"other creator")
            return real_mkdir(path, *args, **kwargs)

        with patch.object(Path, "mkdir", competing_mkdir):
            with self.assertRaises(FileExistsError):
                create_case(self.project, "cases/race")
        self.assertEqual(self.files(target), {"owner.txt": b"other creator"})

    def test_missing_template_does_not_leave_destination(self) -> None:
        shutil.rmtree(self.project / "cases" / "_template")
        with self.assertRaises(WorkspaceError):
            create_case(self.project, "cases/no-template")
        self.assertFalse((self.project / "cases" / "no-template").exists())

    def test_linked_case_or_template_is_rejected(self) -> None:
        outside = self.project / "outside"
        outside.mkdir()
        link = self.project / "cases" / "linked"
        try:
            link.symlink_to(outside, target_is_directory=True)
        except OSError as error:
            self.skipTest(f"Host cannot create symlinks: {error}")
        for operation in (create_case, existing_case):
            with self.assertRaises(WorkspaceError):
                operation(self.project, "cases/linked")
        template_link = self.project / "cases" / "_template" / "outside"
        template_link.symlink_to(outside, target_is_directory=True)
        with self.assertRaises(WorkspaceError):
            create_case(self.project, "cases/unsafe-template")
        self.assertFalse((self.project / "cases" / "unsafe-template").exists())
        self.assertEqual(self.files(outside), {})

    @unittest.skipUnless(sys.platform == "win32", "Windows junction boundary")
    def test_windows_junctions_cannot_redirect_case_or_template(self) -> None:
        outside = self.project / "outside"
        outside.mkdir()
        for link in (self.project / "cases" / "linked",
                     self.project / "cases" / "_template" / "linked"):
            result = subprocess.run(["cmd", "/d", "/c", "mklink", "/J", str(link), str(outside)],
                                    capture_output=True)
            if result.returncode:
                self.skipTest(f"Junction creation unavailable: {result.stderr!r}")
        for operation in (create_case, existing_case):
            with self.assertRaises(WorkspaceError):
                operation(self.project, "cases/linked")
        with self.assertRaises(WorkspaceError):
            create_case(self.project, "cases/unsafe-template")
        self.assertFalse((self.project / "cases" / "unsafe-template").exists())
        self.assertEqual(self.files(outside), {})

    def test_cli_reports_real_results_and_nonzero_stop(self) -> None:
        tools = self.project / "tools"
        tools.mkdir()
        script = tools / "case_workspace.py"
        shutil.copyfile(ROOT / "tools" / "case_workspace.py", script)
        created = subprocess.run([sys.executable, str(script), "create", "cases/cli"], capture_output=True, text=True)
        self.assertEqual(created.returncode, 0, created.stderr)
        self.assertEqual(json.loads(created.stdout)["case_root"], "cases/cli")
        self.assertEqual(json.loads(created.stdout)["status"], "CREATED")
        occupied = subprocess.run([sys.executable, str(script), "create", "cases/cli"], capture_output=True, text=True)
        self.assertEqual(occupied.returncode, 1)
        self.assertEqual(occupied.stdout, "")
        self.assertEqual(json.loads(occupied.stderr)["status"], "STOP")
        selected = subprocess.run([sys.executable, str(script), "existing", "cases/cli"], capture_output=True, text=True)
        self.assertEqual(selected.returncode, 0, selected.stderr)
        self.assertEqual(json.loads(selected.stdout)["status"], "EXISTS")


if __name__ == "__main__":
    unittest.main()
