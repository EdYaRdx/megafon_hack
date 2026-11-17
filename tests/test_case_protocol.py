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

    def complete_r1(
        self, claims: list[str] | None = None, claim_records: list[dict] | None = None
    ) -> None:
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
            files.append({"path": f"revisions/{revision_id}/{name}", "sha256": hashlib.sha256((revision_dir / name).read_bytes()).hexdigest()})
        manifest = {
            "revision_id": revision_id,
            "parent_revision_id": None,
            "status": "COMPLETE",
            "active_claim_ids": claims,
            "files": files,
        }
        claims_path = self.root / "claims.jsonl"
        claim_records = claim_records or [
            {"id": claim_id, "text": f"Claim {claim_id}", "status": "DOCUMENTED", "evidence_ids": [], "supersedes": []}
            for claim_id in claims
        ]
        claims_bytes = b"\n".join(
            json.dumps(record, separators=(",", ":")).encode() for record in claim_records
        )
        if claim_records:
            claims_bytes += b"\n"
        claims_path.write_bytes(claims_bytes)
        manifest["files"].append(
            {"path": "claims.jsonl", "sha256": hashlib.sha256(claims_bytes).hexdigest()}
        )
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

    def republish_claims(self, records: list[dict]) -> None:
        claims_bytes = b"\n".join(
            json.dumps(record, separators=(",", ":")).encode() for record in records
        )
        if records:
            claims_bytes += b"\n"
        (self.root / "claims.jsonl").write_bytes(claims_bytes)
        manifest_path = self.root / "revisions/R0001/manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        for entry in manifest["files"]:
            if entry["path"] == "claims.jsonl":
                entry["sha256"] = hashlib.sha256(claims_bytes).hexdigest()
        manifest_bytes = json.dumps(manifest, separators=(",", ":")).encode()
        manifest_path.write_bytes(manifest_bytes)
        (self.root / "ACTIVE.json").write_text(
            json.dumps({"revision_id": "R0001", "manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest()}),
            encoding="utf-8",
        )

    def test_active_claim_missing_from_checkpoint_ledger_is_rejected(self) -> None:
        self.marker()
        self.complete_r1()
        claims_path = self.root / "claims.jsonl"
        # The active claim appears only after the exact empty prefix pinned by R1.
        claims_path.write_bytes(b'{"id":"CL-01","text":"late","status":"DOCUMENTED","supersedes":[]}\n')
        manifest_path = self.root / "revisions/R0001/manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        for entry in manifest["files"]:
            if entry["path"] == "claims.jsonl":
                entry["sha256"] = hashlib.sha256(b"").hexdigest()
        manifest_bytes = json.dumps(manifest, separators=(",", ":")).encode()
        manifest_path.write_bytes(manifest_bytes)
        (self.root / "ACTIVE.json").write_text(
            json.dumps({"revision_id": "R0001", "manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest()}),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(ProtocolError, "active claim is absent from checkpoint claims ledger: CL-01"):
            classify_case(self.root)

    def test_claim_ids_are_unique_in_checkpoint_prefix(self) -> None:
        self.marker()
        self.complete_r1()
        self.republish_claims([
            {"id": "CL-01", "status": "DOCUMENTED", "supersedes": []},
            {"id": "CL-01", "status": "CLAIMED", "supersedes": []},
        ])
        with self.assertRaisesRegex(ProtocolError, "duplicate claim ID in checkpoint ledger: CL-01"):
            classify_case(self.root)

    def test_active_claim_set_must_follow_supersedes_edges(self) -> None:
        self.marker()
        self.complete_r1(["CL-01", "CL-02"])
        self.republish_claims([
            {"id": "CL-01", "status": "DOCUMENTED", "supersedes": []},
            {"id": "CL-02", "status": "HYPOTHESIS", "supersedes": ["CL-01"]},
        ])
        with self.assertRaisesRegex(ProtocolError, "active claims conflict with supersedes graph"):
            classify_case(self.root)

    def test_valid_statuses_and_explicit_successor_selection_are_checkpointed(self) -> None:
        self.marker()
        self.complete_r1(
            ["CL-01", "CL-02", "CL-03"],
            claim_records=[
                {"id": "CL-01", "status": "CLAIMED", "supersedes": []},
                {"id": "CL-02", "status": "HYPOTHESIS", "supersedes": []},
                {"id": "CL-03", "status": "UNKNOWN", "supersedes": []},
            ],
        )
        self.assertEqual(classify_case(self.root), "CHECKPOINTED")

    def test_explicit_successor_selection_resolves_a_claim_fork(self) -> None:
        self.marker()
        self.complete_r1(
            ["CL-02"],
            claim_records=[
                {"id": "CL-01", "status": "DOCUMENTED", "supersedes": []},
                {"id": "CL-02", "status": "CLAIMED", "supersedes": ["CL-01"]},
                {"id": "CL-03", "status": "UNKNOWN", "supersedes": ["CL-01"]},
            ],
        )
        self.assertEqual(classify_case(self.root), "CHECKPOINTED")

    def test_canonical_claim_ids_are_checkpointed_and_claim_id_alias_is_rejected(self) -> None:
        self.marker("CHECKPOINTING")
        records = [
            {"id": "CL-01", "status": "DOCUMENTED", "supersedes": []},
            {"id": "CL-02", "status": "CLAIMED", "supersedes": ["CL-01"]},
        ]
        self.complete_r1(["CL-02"], claim_records=records)
        self.assertEqual(classify_case(self.root), "CHECKPOINTED")

        self.republish_claims(
            [
                {"claim_id": record["id"], "status": record["status"], "supersedes": record["supersedes"]}
                for record in records
            ]
        )
        with self.assertRaisesRegex(
            ProtocolError, "invalid claim ID in checkpoint ledger at line 1"
        ):
            classify_case(self.root)


    def test_unselected_claim_fork_is_rejected_even_if_parent_is_active(self) -> None:
        self.marker()
        self.complete_r1(
            ["CL-01"],
            claim_records=[
                {"id": "CL-01", "status": "DOCUMENTED", "supersedes": []},
                {"id": "CL-02", "status": "HYPOTHESIS", "supersedes": ["CL-01"]},
                {"id": "CL-03", "status": "CLAIMED", "supersedes": ["CL-01"]},
            ],
        )
        with self.assertRaisesRegex(ProtocolError, "unresolved claim successor fork: CL-01"):
            classify_case(self.root)

    def test_active_claim_requires_claims_ledger_dependency(self) -> None:
        self.marker()
        self.complete_r1()
        manifest_path = self.root / "revisions/R0001/manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["files"] = [entry for entry in manifest["files"] if entry["path"] != "claims.jsonl"]
        manifest_bytes = json.dumps(manifest, separators=(",", ":")).encode()
        manifest_path.write_bytes(manifest_bytes)
        (self.root / "ACTIVE.json").write_text(
            json.dumps({"revision_id": "R0001", "manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest()}),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(ProtocolError, "manifest omits claims.jsonl required by active claims"):
            classify_case(self.root)

    def test_checkpoint_rejects_unknown_supersedes_target(self) -> None:
        self.marker()
        self.complete_r1()
        self.republish_claims([
            {"id": "CL-01", "status": "DOCUMENTED", "supersedes": ["CL-02"]},
        ])
        with self.assertRaisesRegex(ProtocolError, "supersedes references missing claim ID: CL-02"):
            classify_case(self.root)

    def test_checkpoint_rejects_cycles_in_supersedes_graph(self) -> None:
        self.marker()
        self.complete_r1()
        self.republish_claims([
            {"id": "CL-01", "status": "DOCUMENTED", "supersedes": ["CL-02"]},
            {"id": "CL-02", "status": "HYPOTHESIS", "supersedes": ["CL-01"]},
        ])
        with self.assertRaisesRegex(ProtocolError, "cycle in checkpoint claim supersedes graph"):
            classify_case(self.root)

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

    def test_historical_checkpoint_survives_append_only_jsonl_growth(self) -> None:
        self.marker()
        self.complete_r1()
        manifest_path = self.root / "revisions/R0001/manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        ledger_paths = ("sources.jsonl", "evidence.jsonl", "activity.jsonl")
        original_ledgers = {}
        for name in ledger_paths:
            record = json.dumps({"id": f"{name}-R1"}, separators=(",", ":")).encode()
            (self.root / name).write_bytes(record)
            original_ledgers[name] = record
            manifest["files"].append(
                {"path": name, "sha256": hashlib.sha256(record).hexdigest()}
            )

        manifest_bytes = json.dumps(manifest, separators=(",", ":")).encode()
        manifest_path.write_bytes(manifest_bytes)
        (self.root / "ACTIVE.json").write_text(
            json.dumps(
                {
                    "revision_id": "R0001",
                    "manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
                }
            ),
            encoding="utf-8",
        )
        self.assertEqual(classify_case(self.root), "CHECKPOINTED")

        for name in ledger_paths:
            later_record = json.dumps(
                {"id": f"{name}-R2"}, separators=(",", ":")
            ).encode()
            with (self.root / name).open("ab") as ledger:
                ledger.write(b"\n" + later_record + b"\n")

        self.assertEqual(classify_case(self.root), "CHECKPOINTED")
        self.assertEqual(manifest_path.read_bytes(), manifest_bytes)
        for name, original in original_ledgers.items():
            self.assertTrue((self.root / name).read_bytes().startswith(original))
        for name in SNAPSHOTS:
            snapshot = self.root / "revisions/R0001" / name
            entry = next(
                item
                for item in manifest["files"]
                if item["path"] == f"revisions/R0001/{name}"
            )
            self.assertEqual(
                hashlib.sha256(snapshot.read_bytes()).hexdigest(), entry["sha256"]
            )

        sources = self.root / "sources.jsonl"
        current_sources = sources.read_bytes()
        sources.write_bytes(
            current_sources.replace(b"sources.jsonl-R1", b"sources.jsonl-X1", 1)
        )
        with self.assertRaisesRegex(ProtocolError, "hash-mismatched dependency: sources.jsonl"):
            classify_case(self.root)

        sources.write_bytes(original_ledgers["sources.jsonl"][:-1])
        with self.assertRaisesRegex(ProtocolError, "hash-mismatched dependency: sources.jsonl"):
            classify_case(self.root)

    def test_parent_annotations_must_match_manifest(self) -> None:
        self.marker()
        self.complete_r1()
        manifest_path = self.root / "revisions/R0001/manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["parent_revision_id"] = "R0002"
        for name, old, new in (
            (
                "state.md",
                "Active complete revision ID: R0001",
                "Active complete revision ID: R0001 (parent R0002)",
            ),
            (
                "decision.md",
                "**Revision:** R0001",
                "**Revision:** R0001 (parent R0002)",
            ),
        ):
            snapshot = self.root / "revisions/R0001" / name
            content = snapshot.read_text(encoding="utf-8").replace(old, new, 1)
            snapshot.write_text(content, encoding="utf-8")
            entry = next(
                item
                for item in manifest["files"]
                if item["path"] == f"revisions/R0001/{name}"
            )
            entry["sha256"] = hashlib.sha256(snapshot.read_bytes()).hexdigest()
            (self.root / name).write_text(content, encoding="utf-8")

        manifest_bytes = json.dumps(manifest, separators=(",", ":")).encode()
        manifest_path.write_bytes(manifest_bytes)
        (self.root / "ACTIVE.json").write_text(
            json.dumps(
                {
                    "revision_id": "R0001",
                    "manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
                }
            ),
            encoding="utf-8",
        )
        self.assertEqual(classify_case(self.root), "CHECKPOINTED")

        decision = self.root / "decision.md"
        decision.write_text(
            decision.read_text(encoding="utf-8").replace(
                "R0001 (parent R0002)", "R0001 (parent R0003)", 1
            ),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(ProtocolError, "parent revision disagrees with manifest"):
            classify_case(self.root)

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
