from __future__ import annotations

import hashlib
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from tools.case_protocol import ProtocolError, classify_case

REPO_ROOT = Path(__file__).resolve().parents[1]


SNAPSHOTS = (
    "options.md",
    "decision.md",
    "strategy-product.md",
    "strategy-communication.md",
    "test-plan.md",
    "state.md",
)


class CaseProtocolTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def marker(self, state: str = "UNINITIALIZED") -> None:
        (self.root / "case-protocol.json").write_text(
            json.dumps({"protocol_id": "checkpoint-v1", "checkpoint_state": state}), encoding="utf-8"
        )

    def complete_r1(self, claims: list[str] | None = None) -> None:
        claims = claims or ["CL-01"]
        revision_id = "R0001"
        revision_dir = self.root / "revisions" / revision_id
        revision_dir.mkdir(parents=True)
        files = []
        for name in SNAPSHOTS:
            if name == "state.md":
                data = f"- Case protocol: `checkpoint-v1`\n- Active complete revision ID: {revision_id}\n- Current claim IDs (active successors only; match manifest): {', '.join(claims)}\n"
            elif name == "decision.md":
                data = f"- **Revision:** {revision_id}\n- **Active claim IDs:** {', '.join(claims)}\n"
            else:
                data = f"snapshot {name}\n"
            (revision_dir / name).write_text(data, encoding="utf-8")
            files.append({"path": f"revisions/{revision_id}/{name}", "sha256": hashlib.sha256(data.encode()).hexdigest()})
        manifest = {
            "revision_id": revision_id,
            "parent_revision_id": None,
            "status": "COMPLETE",
            "active_claim_ids": claims,
            "files": files,
        }
        manifest_path = revision_dir / "manifest.json"
        manifest_bytes = json.dumps(manifest, separators=(",", ":")).encode()
        manifest_path.write_bytes(manifest_bytes)
        (self.root / "ACTIVE.json").write_text(
            json.dumps({"revision_id": revision_id, "manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest()}),
            encoding="utf-8",
        )
        claim_text = ", ".join(claims)
        (self.root / "state.md").write_text(
            f"- Case protocol: `checkpoint-v1`\n- Active complete revision ID: {revision_id}\n- Current claim IDs (active successors only; match manifest): {claim_text}\n",
            encoding="utf-8",
        )
        (self.root / "decision.md").write_text(
            f"- **Revision:** {revision_id}\n- **Active claim IDs:** {claim_text}\n", encoding="utf-8"
        )

    def test_copied_template_is_fresh_uninitialized_case(self) -> None:
        case_dir = self.root / "new-case"
        shutil.copytree(REPO_ROOT / "cases" / "_template", case_dir)
        self.root = case_dir
        (self.root / "brief.md").write_text("intake work can already exist", encoding="utf-8")
        self.assertEqual(classify_case(self.root), "FRESH")

    def test_marked_complete_r1_is_checkpointed_even_if_marker_write_was_interrupted(self) -> None:
        self.marker("CHECKPOINTING")
        self.complete_r1()
        self.assertEqual(classify_case(self.root), "CHECKPOINTED")

    def test_checkpointing_case_with_populated_roots_but_missing_selector_stops(self) -> None:
        self.marker("CHECKPOINTING")
        (self.root / "state.md").write_text("populated roots", encoding="utf-8")
        with self.assertRaises(ProtocolError):
            classify_case(self.root)

    def test_uninitialized_case_with_revision_artifact_stops(self) -> None:
        self.marker()
        (self.root / "revisions" / "R0001").mkdir(parents=True)
        (self.root / "revisions" / "R0001" / "state.md").write_text("partial", encoding="utf-8")
        with self.assertRaises(ProtocolError):
            classify_case(self.root)

    def test_unknown_missing_marker_is_not_legacy(self) -> None:
        (self.root / "state.md").write_text("legacy-looking content", encoding="utf-8")
        with self.assertRaises(ProtocolError):
            classify_case(self.root)

    def test_allowlisted_legacy_snapshot_remains_readable_as_legacy(self) -> None:
        legacy = self.root / "cases" / "retention-demo"
        legacy.mkdir(parents=True)
        (legacy / "state.md").write_text("historical state", encoding="utf-8")
        (legacy / "revisions").mkdir()
        (legacy / "revisions" / "state-r1.md").write_text("old snapshot", encoding="utf-8")
        self.assertEqual(classify_case(legacy, repo_root=self.root), "LEGACY")

    def test_same_basename_outside_canonical_cases_path_is_not_legacy(self) -> None:
        legacy_lookalike = self.root / "retention-demo"
        legacy_lookalike.mkdir()
        with self.assertRaises(ProtocolError):
            classify_case(legacy_lookalike)

    def test_manifest_hash_mismatch_stops(self) -> None:
        self.marker()
        self.complete_r1()
        (self.root / "revisions/R0001/options.md").write_text("tampered", encoding="utf-8")
        with self.assertRaises(ProtocolError):
            classify_case(self.root)

    def test_root_active_claim_mismatch_stops(self) -> None:
        self.marker()
        self.complete_r1()
        (self.root / "decision.md").write_text(
            "- **Revision:** R0001\n- **Active claim IDs:** CL-02\n", encoding="utf-8"
        )
        with self.assertRaises(ProtocolError):
            classify_case(self.root)

    def test_immutable_snapshot_claim_mismatch_stops_even_when_its_hash_is_updated(self) -> None:
        self.marker()
        self.complete_r1()
        manifest_path = self.root / "revisions/R0001/manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        snapshot = self.root / "revisions/R0001/decision.md"
        snapshot.write_text("- **Revision:** R0001\n- **Active claim IDs:** CL-02\n", encoding="utf-8")
        for entry in manifest["files"]:
            if entry["path"] == "revisions/R0001/decision.md":
                entry["sha256"] = hashlib.sha256(snapshot.read_bytes()).hexdigest()
        manifest_bytes = json.dumps(manifest, separators=(",", ":")).encode()
        manifest_path.write_bytes(manifest_bytes)
        (self.root / "ACTIVE.json").write_text(
            json.dumps({"revision_id": "R0001", "manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest()}),
            encoding="utf-8",
        )
        with self.assertRaises(ProtocolError):
            classify_case(self.root)

    def test_allowlisted_legacy_with_selector_stops(self) -> None:
        legacy = self.root / "cases" / "retention-demo"
        legacy.mkdir(parents=True)
        self.assertEqual(classify_case(legacy, repo_root=self.root), "LEGACY")
        (legacy / "ACTIVE.json").write_text("{}", encoding="utf-8")
        with self.assertRaises(ProtocolError):
            classify_case(legacy, repo_root=self.root)


if __name__ == "__main__":
    unittest.main()
