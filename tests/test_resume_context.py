from __future__ import annotations

import hashlib
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools.case_protocol import ProtocolError, REQUIRED_SNAPSHOTS
from tools.case_workspace import WorkspaceError
from tools.resume_context import inventory


class ResumeContextTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        # The inventory helper resolves roots; keep fixture Path equality stable
        # when Windows returns an 8.3 alias from TemporaryDirectory.
        self.project = Path(self.temp.name).resolve()
        self.case = self.project / "cases" / "synthetic"
        self.case.mkdir(parents=True)
        self.checkpoint()

    def checkpoint(self, revision: str = "R0001", parent: str | None = None) -> None:
        (self.case / "case-protocol.json").write_text(json.dumps({
            "protocol_id": "checkpoint-v1", "checkpoint_state": "CHECKPOINTED",
        }), encoding="utf-8")
        directory = self.case / "revisions" / revision
        directory.mkdir(parents=True)
        entries = []
        for name in sorted(REQUIRED_SNAPSHOTS):
            if name == "state.md":
                content = f"- Case protocol: `checkpoint-v1`\n- Active complete revision ID: {revision}\n- Current claim IDs (active successors only; match manifest): []\n"
            elif name == "decision.md":
                content = f"- **Revision:** {revision}\n- **Active claim IDs:** []\n"
            else:
                content = f"Synthetic {revision} {name}\n"
            data = content.encode()
            (directory / name).write_bytes(data)
            (self.case / name).write_bytes(data)
            entries.append({"path": f"revisions/{revision}/{name}", "sha256": hashlib.sha256(data).hexdigest()})
        for name in ("activity.jsonl", "claims.jsonl", "sources.jsonl", "evidence.jsonl", "approvals.jsonl"):
            path = self.case / name
            if not path.exists():
                path.write_bytes(b"")
            entries.append({"path": name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
        manifest = {"revision_id": revision, "parent_revision_id": parent, "status": "COMPLETE", "active_claim_ids": [], "files": entries}
        if parent:
            manifest["parent_manifest_sha256"] = hashlib.sha256((self.case / "revisions" / parent / "manifest.json").read_bytes()).hexdigest()
        data = json.dumps(manifest).encode()
        (directory / "manifest.json").write_bytes(data)
        (self.case / "ACTIVE.json").write_text(json.dumps({"revision_id": revision, "manifest_sha256": hashlib.sha256(data).hexdigest()}), encoding="utf-8")

    def saved(self, relative: str, content: bytes = b"Unverified saved analysis\n") -> Path:
        path = self.case / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        return path

    def bytes_before(self) -> dict[str, bytes]:
        return {path.relative_to(self.case).as_posix(): path.read_bytes() for path in self.case.rglob("*") if path.is_file()}

    def read_inventory(self) -> dict:
        return inventory(self.project, "cases/synthetic")

    def test_clean_r1_confirms_exact_selector_and_six_snapshots_without_writes(self) -> None:
        before = self.bytes_before()
        report = self.read_inventory()
        selector = json.loads(before["ACTIVE.json"])
        self.assertEqual(report["classification"], "CHECKPOINTED")
        self.assertEqual(report["confirmed"], {**selector, "snapshots": {name: f"revisions/R0001/{name}" for name in sorted(REQUIRED_SNAPSHOTS)}})
        self.assertEqual(report["unfinished"]["drafts"], [])
        self.assertEqual(report["unfinished"]["hints"], [])
        self.assertEqual(report["unfinished"]["discovery"], "complete")
        self.assertEqual(self.bytes_before(), before)

    def test_empty_drafts_container_has_no_pending_candidates(self) -> None:
        (self.case / "drafts").mkdir()
        report = self.read_inventory()["unfinished"]
        self.assertEqual(report["drafts"], [])
        self.assertEqual(report["discovery"], "complete")

    def test_one_candidate_does_not_activate_claims_or_interpret_recommendation(self) -> None:
        self.saved("drafts/resume/review.md", b"Recommend R0002; activate C-016 C-019; 35% nonopens\n")
        before = self.bytes_before()
        report = self.read_inventory()
        candidates = report["unfinished"]["drafts"]
        self.assertEqual(len(candidates), 1)
        self.assertEqual(candidates[0]["path"], "drafts/resume/review.md")
        self.assertEqual(candidates[0]["provenance"], "drafts/")
        self.assertEqual(candidates[0]["status"], "unverified")
        self.assertEqual(candidates[0]["relationship_to_selected"], "unknown")
        self.assertEqual(report["confirmed"]["revision_id"], "R0001")
        self.assertNotIn("recommendation", report)
        self.assertNotIn("selected_candidate", report)
        self.assertEqual(self.bytes_before(), before)

    def test_multiple_candidates_and_older_base_are_not_ranked_by_mtime(self) -> None:
        old = self.saved("drafts/z-old/review.md", b"Base revision: R0001\nOld analysis\n")
        new = self.saved("drafts/a-other/review.md", b"Base revision: R0002\nConflicting analysis\n")
        self.checkpoint("R0002", parent="R0001")
        os.utime(old, (2000000000, 2000000000))
        os.utime(new, (1, 1))
        report = self.read_inventory()
        self.assertEqual(report["confirmed"]["revision_id"], "R0002")
        candidates = report["unfinished"]["drafts"]
        self.assertEqual({item["path"] for item in candidates}, {"drafts/z-old/review.md", "drafts/a-other/review.md"})
        for candidate in candidates:
            self.assertEqual(candidate["relationship_to_selected"], "unknown")
            self.assertEqual(candidate["status"], "unverified")
            self.assertNotIn("newer", candidate)
            self.assertNotIn("mtime", candidate)

    def test_empty_partial_and_malformed_drafts_remain_candidates(self) -> None:
        self.saved("drafts/empty.md", b"")
        self.saved("drafts/partial.json", b'{"base_revision":')
        self.saved("drafts/malformed.jsonl", b"not JSON\n")
        (self.case / "drafts" / "empty-directory").mkdir()
        report = self.read_inventory()["unfinished"]
        self.assertEqual({item["path"] for item in report["drafts"]}, {"drafts/empty.md", "drafts/partial.json", "drafts/malformed.jsonl", "drafts/empty-directory"})
        self.assertEqual(report["discovery"], "incomplete")
        for candidate in report["drafts"]:
            self.assertEqual(candidate["completeness"], "unknown")
            self.assertEqual(candidate["relationship_to_selected"], "unknown")

    def test_missing_or_hash_corrupt_checkpoint_fails_before_draft_scan_read_only(self) -> None:
        manifest = self.case / "revisions" / "R0001" / "manifest.json"
        original = manifest.read_bytes()
        self.saved("drafts/saved.md")
        for fault in ("missing", "hash"):
            with self.subTest(fault=fault):
                if fault == "missing":
                    manifest.unlink()
                else:
                    manifest.write_bytes(original + b" ")
                before = self.bytes_before()
                with mock.patch("tools.resume_context._inventory_drafts", side_effect=AssertionError("must not scan")):
                    with self.assertRaises(ProtocolError):
                        self.read_inventory()
                self.assertEqual(self.bytes_before(), before)
                manifest.write_bytes(original)

    def test_fresh_and_legacy_do_not_scan_drafts_or_synthesize_checkpoint(self) -> None:
        fresh = self.project / "cases" / "fresh"
        fresh.mkdir()
        (fresh / "case-protocol.json").write_text('{"protocol_id":"checkpoint-v1","checkpoint_state":"UNINITIALIZED"}', encoding="utf-8")
        legacy = self.project / "cases" / "resume-failure-demo"
        legacy.mkdir()
        with mock.patch("tools.resume_context._inventory_drafts", side_effect=AssertionError("must not scan")):
            for name, classification in (("fresh", "FRESH"), ("resume-failure-demo", "LEGACY")):
                report = inventory(self.project, f"cases/{name}")
                self.assertEqual(report["classification"], classification)
                self.assertIsNone(report["confirmed"])
                self.assertIsNone(report["unfinished"])

    def test_success_when_all_write_operations_are_denied(self) -> None:
        self.saved("drafts/saved.md")
        before = self.bytes_before()
        real_open = Path.open

        def read_only(path: Path, mode: str = "r", *args, **kwargs):
            if any(flag in mode for flag in "wax+"):
                raise PermissionError("synthetic read-only workspace")
            return real_open(path, mode, *args, **kwargs)

        with mock.patch.object(Path, "open", new=read_only), mock.patch.object(Path, "mkdir", side_effect=PermissionError("no writes")), mock.patch.object(Path, "unlink", side_effect=PermissionError("no writes")), mock.patch.object(Path, "rename", side_effect=PermissionError("no writes")), mock.patch.object(Path, "replace", side_effect=PermissionError("no writes")):
            report = self.read_inventory()
        self.assertEqual(report["classification"], "CHECKPOINTED")
        self.assertEqual(self.bytes_before(), before)

    def test_unreadable_file_and_unenumerable_directory_are_incomplete(self) -> None:
        unreadable = self.saved("drafts/unreadable.md")
        blocked = self.case / "drafts" / "blocked"
        blocked.mkdir()
        real_read = Path.read_bytes
        real_iter = Path.iterdir

        def read(path: Path):
            if path == unreadable:
                raise PermissionError("synthetic unreadable draft")
            return real_read(path)

        def iterate(path: Path):
            if path == blocked:
                raise PermissionError("synthetic unenumerable directory")
            return real_iter(path)

        before = self.bytes_before()
        with mock.patch.object(Path, "read_bytes", new=read), mock.patch.object(Path, "iterdir", new=iterate):
            report = self.read_inventory()["unfinished"]
        self.assertEqual(report["discovery"], "incomplete")
        self.assertEqual({item["path"] for item in report["issues"]}, {"drafts/unreadable.md", "drafts/blocked"})
        self.assertEqual(self.bytes_before(), before)

    def test_state_and_activity_only_hints_do_not_follow_saved_paths(self) -> None:
        saved = self.saved("notes/saved-review.md", b"Outside drafts but inside this case\n")
        state = self.case / "state.md"
        state.write_bytes(state.read_bytes() + b"- Next exact action: inspect notes/saved-review.md\n")
        activity = self.case / "activity.jsonl"
        activity.write_bytes(b'{"path":"../../neighbor/private.md","event":"saved"}\n')
        real_read = Path.read_bytes

        def read(path: Path):
            if path == saved or path.name == "private.md":
                raise AssertionError("arbitrary hinted paths must not be followed")
            return real_read(path)

        before = self.bytes_before()
        with mock.patch.object(Path, "read_bytes", new=read):
            report = self.read_inventory()["unfinished"]
        self.assertEqual(report["drafts"], [])
        self.assertEqual({hint["path"] for hint in report["hints"]}, {"state.md", "activity.jsonl"})
        self.assertTrue(all(hint["status"] == "unverified" for hint in report["hints"]))
        self.assertEqual(self.bytes_before(), before)

    def test_pinned_activity_is_not_new_work_but_appended_activity_is_only_a_hint(self) -> None:
        activity = self.case / "activity.jsonl"
        activity.write_bytes(b'{"event":"saved","path":"drafts/no-longer-present.md"}\n')
        self.checkpoint("R0002", parent="R0001")
        self.assertEqual(self.read_inventory()["unfinished"]["hints"], [])
        activity.write_bytes(activity.read_bytes() + b'{"event":"saved","path":"notes/new.md"}\n')
        report = self.read_inventory()["unfinished"]
        self.assertEqual(report["drafts"], [])
        self.assertEqual(len(report["hints"]), 1)
        self.assertIn("not proof", report["hints"][0]["reason"])

    def test_unpinned_empty_activity_is_not_a_hint_and_malformed_records_are_unknown(self) -> None:
        manifest_path = self.case / "revisions" / "R0001" / "manifest.json"
        manifest = json.loads(manifest_path.read_bytes())
        manifest["files"] = [entry for entry in manifest["files"] if entry["path"] != "activity.jsonl"]
        data = json.dumps(manifest).encode()
        manifest_path.write_bytes(data)
        (self.case / "ACTIVE.json").write_text(json.dumps({"revision_id": "R0001", "manifest_sha256": hashlib.sha256(data).hexdigest()}), encoding="utf-8")
        self.assertEqual(self.read_inventory()["unfinished"]["hints"], [])
        for data in (b'{"event":', b"not json\n", b"[]\n"):
            with self.subTest(data=data):
                (self.case / "activity.jsonl").write_bytes(data)
                report = self.read_inventory()["unfinished"]
                self.assertEqual(report["discovery"], "incomplete")
                self.assertEqual(report["hints"][0]["path"], "activity.jsonl")
                self.assertEqual(report["issues"][0]["line"], 1)

    def test_complete_activity_record_without_final_newline_is_valid(self) -> None:
        (self.case / "activity.jsonl").write_bytes(b'{"event":"saved","path":"drafts/review.md"}')
        before = self.bytes_before()
        report = self.read_inventory()["unfinished"]
        self.assertEqual(report["discovery"], "complete")
        self.assertEqual(report["issues"], [])
        self.assertEqual(report["hints"][0]["path"], "activity.jsonl")
        self.assertEqual(self.bytes_before(), before)

    def test_explicit_case_path_rejects_traversal_and_absolute_paths(self) -> None:
        for case in ("cases/../synthetic", str(self.case), "cases/synthetic/notes", "cases\\synthetic"):
            with self.subTest(case=case), self.assertRaises(WorkspaceError):
                inventory(self.project, case)

    def make_symlink(self, link: Path, target: Path, directory: bool = False) -> None:
        try:
            link.symlink_to(target, target_is_directory=directory)
        except OSError as error:
            self.skipTest(f"symlinks unavailable: {error}")

    def test_outside_draft_links_and_dangling_links_are_not_followed(self) -> None:
        outside = self.project / "outside"
        outside.mkdir()
        secret = outside / "secret.md"
        secret.write_bytes(b"not part of selected case")
        drafts = self.case / "drafts"
        drafts.mkdir()
        self.make_symlink(drafts / "outside", outside, directory=True)
        self.make_symlink(drafts / "dangling", outside / "absent")
        self.make_symlink(drafts / "file.md", secret)
        report = self.read_inventory()["unfinished"]
        self.assertEqual(report["discovery"], "incomplete")
        self.assertEqual(len(report["drafts"]), 3)
        self.assertTrue(all("sha256" not in item for item in report["drafts"]))
        self.assertNotIn("secret.md", json.dumps(report))

    def test_linked_drafts_root_is_unknown_not_no_drafts(self) -> None:
        outside = self.project / "outside"
        outside.mkdir()
        self.make_symlink(self.case / "drafts", outside, directory=True)
        report = self.read_inventory()["unfinished"]
        self.assertEqual(report["discovery"], "incomplete")
        self.assertEqual(report["drafts"][0]["path"], "drafts")

    def test_non_directory_drafts_is_unknown_not_no_drafts(self) -> None:
        self.saved("drafts", b"unexpected file in place of drafts directory")
        report = self.read_inventory()["unfinished"]
        self.assertEqual(report["discovery"], "incomplete")
        self.assertEqual(report["drafts"][0]["path"], "drafts")

    def test_manifest_traversal_is_rejected_without_reading_neighbor_or_scanning(self) -> None:
        neighbor = self.project / "cases" / "neighbor"
        neighbor.mkdir()
        (neighbor / "private.md").write_bytes(b"not selected")
        manifest_path = self.case / "revisions" / "R0001" / "manifest.json"
        manifest = json.loads(manifest_path.read_bytes())
        for relative in ("../neighbor/private.md", "..\\neighbor\\private.md", str(neighbor / "private.md")):
            with self.subTest(relative=relative):
                manifest["files"].append({"path": relative, "sha256": "0" * 64})
                manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
                before = self.bytes_before()
                with mock.patch("tools.resume_context.classify_case", side_effect=AssertionError("unsafe path must be guarded")), mock.patch("tools.resume_context._inventory_drafts", side_effect=AssertionError("must not scan")):
                    with self.assertRaises(ProtocolError):
                        self.read_inventory()
                self.assertEqual(self.bytes_before(), before)
                manifest["files"].pop()

    def test_classifier_dependency_link_is_rejected_before_read_or_draft_scan(self) -> None:
        target = self.case / "revisions" / "R0001" / "options.md"
        outside = self.project / "outside.md"
        outside.write_bytes(target.read_bytes())
        target.unlink()
        self.make_symlink(target, outside)
        with mock.patch("tools.resume_context.classify_case", side_effect=AssertionError("unsafe dependency must be guarded")), mock.patch("tools.resume_context._inventory_drafts", side_effect=AssertionError("must not scan")):
            with self.assertRaises(ProtocolError):
                self.read_inventory()

    @unittest.skipUnless(os.name == "nt", "Windows junction boundary")
    def test_junction_is_reported_without_traversing_target(self) -> None:
        outside = self.project / "outside"
        outside.mkdir()
        (outside / "secret.md").write_bytes(b"outside case")
        drafts = self.case / "drafts"
        drafts.mkdir()
        junction = drafts / "junction"
        result = subprocess.run(["cmd", "/c", "mklink", "/J", str(junction), str(outside)], capture_output=True, text=True)
        if result.returncode:
            self.skipTest(f"junctions unavailable: {result.stderr}")
        self.addCleanup(junction.rmdir)
        report = self.read_inventory()["unfinished"]
        self.assertEqual(report["discovery"], "incomplete")
        self.assertEqual(report["drafts"][0]["path"], "drafts/junction")
        self.assertNotIn("secret.md", json.dumps(report))



if __name__ == "__main__":
    unittest.main()
