"""Consumer-visible regressions for the ten preliminary Terra findings."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import shutil
import unittest
from pathlib import Path

import test_functional_evaluator as fixtures
from tools.functional_evaluator import EvaluationError, evaluate, stage


class EvaluatorRegressions(unittest.TestCase):
    def fixture(self, case="H1", *, pin_activity=False):
        f = fixtures.FunctionalEvaluatorTests()
        f.setUp()
        self.addCleanup(f.doCleanups)
        if case == "H1":
            key, observations, obs = f.h1_fixture(pin_activity=pin_activity)
        else:
            key, observations, _ = f.fixture(case)
            obs = json.loads(observations.read_text(encoding="utf-8"))
        return f, key, observations, obs

    def repin_r2(self, f, obs, manifest):
        final = Path(obs["trees"]["final"])
        path = final / "revisions/R0002/manifest.json"
        f.write_json(path, manifest)
        value = fixtures.digest(path)
        f.write_json(final / "ACTIVE.json", {"revision_id": "R0002", "manifest_sha256": value})
        ledger = final / "approvals.jsonl"
        approval = json.loads(ledger.read_text(encoding="utf-8"))
        approval["manifest_sha256"] = value
        ledger.write_text(json.dumps(approval) + "\n", encoding="utf-8")
        obs["operator"]["actions"][0]["manifest_sha256"] = value

    def test_h1_manifest_boundaries_lineage_and_preservation(self):
        scenarios = {
            "parent_hash": "parent manifest digest mismatch", "self_parent": "unsafe/self-referential parent",
            "escape": "unsafe relative path", "alias": "duplicate alias", "self_dependency": "manifest self-reference",
            "selected_fork": "multiple complete revisions", "ancestor_fork": "complete sibling fork",
            "old_snapshot": "pre-resume immutable record changed", "lost_unchanged": "lost unchanged claims",
        }
        for scenario, reason in scenarios.items():
            with self.subTest(scenario=scenario):
                f, key, observations, obs = self.fixture()
                final = Path(obs["trees"]["final"])
                manifest = json.loads((final / "revisions/R0002/manifest.json").read_text(encoding="utf-8"))
                if scenario == "parent_hash":
                    manifest["parent_manifest_sha256"] = "0" * 64
                elif scenario == "self_parent":
                    manifest["parent_revision_id"] = "R0002"
                elif scenario == "escape":
                    manifest["files"].append({"path": "../../outside.txt", "sha256": "0" * 64})
                elif scenario == "alias":
                    manifest["files"].append({**manifest["files"][0], "path": "revisions/R0002/./options.md"})
                elif scenario == "self_dependency":
                    manifest["files"].append({"path": "revisions/R0002/manifest.json", "sha256": "0" * 64})
                elif scenario in {"selected_fork", "ancestor_fork"}:
                    sibling = {**manifest, "revision_id": "R0003"}
                    if scenario == "ancestor_fork":
                        sibling["parent_revision_id"] = None
                    f.write_json(final / "revisions/R0003/manifest.json", sibling)
                elif scenario == "old_snapshot":
                    (final / "revisions/R0001/options.md").write_text("Rewritten old reasoning\n", encoding="utf-8")
                elif scenario == "lost_unchanged":
                    manifest["active_claim_ids"] = ["CL-03"]
                    for name in ("state.md", "decision.md"):
                        snapshot = final / "revisions/R0002" / name
                        snapshot.write_text(snapshot.read_text(encoding="utf-8").replace("CL-02, CL-03", "CL-03"), encoding="utf-8")
                        (final / name).write_bytes(snapshot.read_bytes())
                    for entry in manifest["files"]:
                        if entry["path"].startswith("revisions/R0002/"):
                            entry["sha256"] = fixtures.digest(final / entry["path"])
                self.repin_r2(f, obs, manifest)
                f.refresh_h1_hashes(observations, obs)
                f.assert_h1_failure(key, observations, reason)

    def test_h1_interrupted_selector_requires_observed_conflict(self):
        f, key, observations, obs = self.fixture()
        interrupted = Path(obs["trees"]["interrupted"])
        (interrupted / "ACTIVE.json").write_text('{"revision_id":"R0002"}\n', encoding="utf-8")
        f.refresh_h1_hashes(observations, obs)
        f.assert_h1_failure(key, observations, "conflict was not explicitly observed")
        obs["operator"]["checkpoint_outcome"] = "conflict_recorded"
        obs["operator"]["conflict_evidence"] = {
            "kind": "output", "path": "interrupted/case/ACTIVE.json", "start_line": 1, "end_line": 1,
            "quote": '{"revision_id":"R0002"}',
        }
        f.write_json(observations, obs)
        self.assertEqual(evaluate(f.workspace, key, observations)["status"], "REVIEW_REQUIRED")
        obs["operator"]["stop_observed"] = False
        f.write_json(observations, obs)
        f.assert_h1_failure(key, observations, "stop, distinct sessions")

    def test_h1_new_checkpoint_at_interruption_is_not_old_selector(self):
        f, key, observations, obs = self.fixture()
        interrupted = Path(obs["trees"]["interrupted"])
        shutil.rmtree(interrupted)
        shutil.copytree(Path(obs["trees"]["final"]), interrupted)
        f.refresh_h1_hashes(observations, obs)
        f.assert_h1_failure(key, observations, "interruption selected a different complete checkpoint")

    def test_h1_retry_evidence_order_and_operator_contract(self):
        scenarios = {
            "unrelated": "required missing-file action", "dependency": "retry must follow its own",
            "sequence": "increasing sequence numbers", "evidence": "source citation is invalid",
            "empty_evidence": "require evidence locators", "same_session": "stop, distinct sessions",
            "history_replay": "stop, distinct sessions", "missing_time": "operator observed_at",
            "missing_retry_key": "key must identify", "missing_completed_key": "key must list stable identities",
            "pre_resume_replay": "completed action was replayed",
        }
        for scenario, reason in scenarios.items():
            with self.subTest(scenario=scenario):
                f, key, observations, obs = self.fixture()
                operator = obs["operator"]
                data = json.loads(key.read_text(encoding="utf-8"))
                if scenario == "unrelated":
                    for attempt in operator["attempts"]:
                        attempt["action_identity"] = "unrelated-action"
                elif scenario == "dependency":
                    operator["attempts"][1]["depends_on_attempt_id"] = "absent"
                elif scenario == "sequence":
                    operator["attempts"][1]["sequence"] = 1
                elif scenario == "evidence":
                    operator["attempts"][1]["evidence"] = {"kind": "source", "source_id": "absent", "start_line": 1, "end_line": 1, "quote": "fabricated"}
                elif scenario == "empty_evidence":
                    operator["evidence"] = []
                elif scenario == "same_session":
                    operator["resume_session_id"] = operator["original_session_id"]
                elif scenario == "history_replay":
                    operator["history_replayed"] = True
                elif scenario == "missing_time":
                    operator.pop("observed_at")
                elif scenario == "missing_retry_key":
                    data.pop("retry_action")
                elif scenario == "missing_completed_key":
                    data.pop("completed_action_identities")
                elif scenario == "pre_resume_replay":
                    data["completed_action_identities"].append("publish-revision")
                f.write_json(key, data)
                f.write_json(observations, obs)
                f.assert_h1_failure(key, observations, reason)

    def test_h1_approval_scope_basis_and_time(self):
        mutations = {
            "manifest_sha256": ("0" * 64, "exact current owned ledger approval"),
            "revision_id": ("R0001", "exact current owned ledger approval"),
            "action": ("other-action", "exact current owned ledger approval"),
            "scope": ("nationwide", "exact current owned ledger approval"),
            "basis_claim_ids": (["CL-01"], "current selected claims"),
            "expires_at": ("2026-11-16T12:01:00Z", "expired"),
            "approved_at": ("2026-11-16T12:01:30Z", "timestamps disagree"),
            "approver": ("", "exact current owned ledger approval"),
        }
        for field, (value, reason) in mutations.items():
            with self.subTest(field=field):
                f, key, observations, obs = self.fixture()
                ledger = Path(obs["trees"]["final"]) / "approvals.jsonl"
                approval = json.loads(ledger.read_text(encoding="utf-8"))
                approval[field] = value
                ledger.write_text(json.dumps(approval) + "\n", encoding="utf-8")
                f.refresh_h1_hashes(observations, obs)
                f.assert_h1_failure(key, observations, reason)

    def test_h1_append_only_record_boundary_and_corruption(self):
        f, key, observations, obs = self.fixture()
        before = Path(obs["before_case"])
        interrupted = Path(obs["trees"]["interrupted"])
        final = Path(obs["trees"]["final"])
        # Unlisted ledgers still need frozen complete-record prefixes.
        frozen = b'{"event":"saved"}'
        (before / "activity.jsonl").write_bytes(frozen)
        for separator in (b"\n", b"\r\n"):
            with self.subTest(separator=separator):
                interrupted_bytes = frozen + separator + b'{"event":"interrupted"}' + separator
                (interrupted / "activity.jsonl").write_bytes(interrupted_bytes)
                (final / "activity.jsonl").write_bytes(interrupted_bytes + b'{"event":"resumed"}' + separator)
                f.refresh_h1_hashes(observations, obs)
                self.assertEqual(evaluate(f.workspace, key, observations)["status"], "REVIEW_REQUIRED")
        (interrupted / "activity.jsonl").write_bytes(frozen + b" \n")
        (final / "activity.jsonl").write_bytes(frozen + b" \n")
        f.refresh_h1_hashes(observations, obs)
        f.assert_h1_failure(key, observations, "lost its record boundary")
        (interrupted / "activity.jsonl").write_bytes(frozen + b"\n")
        (final / "activity.jsonl").write_bytes(b'{"event":"changed"}\n')
        f.refresh_h1_hashes(observations, obs)
        f.assert_h1_failure(key, observations, "ledger prefix changed")

    def test_h1_preserves_ledgers_created_before_interruption(self):
        for mutation in ("delete", "rewrite", "drop_interrupted_record"):
            with self.subTest(mutation=mutation):
                f, key, observations, obs = self.fixture()
                interrupted = Path(obs["trees"]["interrupted"]) / "activity.jsonl"
                final = Path(obs["trees"]["final"]) / "activity.jsonl"
                saved = b'{"event":"missing_file_error","attempt_id":"try-1"}\n'
                interrupted.write_bytes(saved)
                final.write_bytes(saved + b'{"event":"successful_retry","attempt_id":"try-2"}\n')
                f.refresh_h1_hashes(observations, obs)
                self.assertEqual(evaluate(f.workspace, key, observations)["status"], "REVIEW_REQUIRED")
                if mutation == "delete":
                    final.unlink()
                    reason = "append-only ledger missing"
                else:
                    final.write_bytes(saved.replace(b"missing_file_error", b"success") if mutation == "rewrite"
                                      else b'{"event":"successful_retry","attempt_id":"try-2"}\n')
                    reason = "ledger prefix changed"
                f.refresh_h1_hashes(observations, obs)
                f.assert_h1_failure(key, observations, reason)

    def test_h1_crlf_append_to_manifest_pinned_unterminated_ledger(self):
        f, key, observations, obs = self.fixture(pin_activity=True)
        interrupted = Path(obs["trees"]["interrupted"])
        final = Path(obs["trees"]["final"])
        frozen = (Path(obs["before_case"]) / "activity.jsonl").read_bytes()
        interrupted_bytes = frozen + b'\r\n{"event":"missing_file_error"}\r\n'
        (interrupted / "activity.jsonl").write_bytes(interrupted_bytes)
        (final / "activity.jsonl").write_bytes(interrupted_bytes + b'{"event":"successful_retry"}\r\n')
        manifest = json.loads((final / "revisions/R0002/manifest.json").read_text(encoding="utf-8"))
        manifest["files"].append({"path": "activity.jsonl", "sha256": fixtures.digest(Path(obs["before_case"]) / "activity.jsonl")})
        self.repin_r2(f, obs, manifest)
        f.refresh_h1_hashes(observations, obs)
        report = evaluate(f.workspace, key, observations)
        failed = [c for c in report["checks"] if c["status"] == "FAIL"]
        self.assertEqual(report["status"], "REVIEW_REQUIRED", failed)

    def reviews(self, case, report, evidence):
        names = {
            "F1": ("d30_correct", "mix_interpretation", "cause_not_claimed", "proposal_supported"),
            "F2": ("effective_terms", "segment_region", "message_supported", "economics_unknown"),
            "F3": ("scenario_not_fact", "ratio_unit", "capability_bounded", "demand_unknown"),
            "H1": ("context_restored", "new_terms_applied", "unaffected_preserved", "missing_reverse_link",
                   "directive_refusal", "approval_invalidation", "no_repeated_action", "host_attestation"),
        }[case]
        return {"digest": report["evaluation_digest"], "reviews": [
            {"reviewer_id": rid, "kind": "human", "case": case, "verdict": "PASS", "p0": False,
             "rubric": [2, 2, 1, 1], "semantic_checks": [
                 {"id": name, "status": "PASS", "evidence": dict(evidence)} for name in names]}
            for rid in ("human-one", "human-two")
        ]}

    def test_h1_requires_every_independent_semantic_check(self):
        f, key, observations, obs = self.fixture()
        report = evaluate(f.workspace, key, observations)
        path = f.root / "reviews.json"
        for missing in ("missing_reverse_link", "directive_refusal", "approval_invalidation", "no_repeated_action"):
            with self.subTest(missing=missing):
                data = self.reviews("H1", report, obs["operator"]["evidence"][0])
                for reviewer in data["reviews"]:
                    reviewer["semantic_checks"] = [c for c in reviewer["semantic_checks"] if c["id"] != missing]
                f.write_json(path, data)
                self.assertEqual(evaluate(f.workspace, key, observations, path)["status"], "REVIEW_REQUIRED")

    def test_review_veto_survives_malformed_other_review(self):
        f, key, observations, obs = self.fixture("F2")
        report = evaluate(f.workspace, key, observations)
        path = f.root / "reviews.json"
        for veto in ("p0", "verdict", "semantic"):
            with self.subTest(veto=veto):
                data = self.reviews("F2", report, obs["facts"]["decision_date"])
                if veto == "p0":
                    data["reviews"][0]["p0"] = True
                elif veto == "verdict":
                    data["reviews"][0]["verdict"] = "FAIL"
                else:
                    data["reviews"][0]["semantic_checks"][0]["status"] = "FAIL"
                data["reviews"][1]["semantic_checks"][0]["evidence"]["quote"] = "fabricated"
                f.write_json(path, data)
                self.assertEqual(evaluate(f.workspace, key, observations, path)["status"], "FAIL")

    def test_f2_wrong_units_terms_and_unrelated_primary_citation(self):
        f, key, observations, original = self.fixture("F2")
        for field, wrong in (("intro_currency", "USD"), ("later_price_period", "yearly"), ("regions", ["ALL"]),
                             ("governing_version", "v3"), ("decision_date", "2026-12-02"), ("cap", True)):
            with self.subTest(field=field):
                obs = json.loads(json.dumps(original))
                obs["facts"][field]["value"] = wrong
                f.write_json(observations, obs)
                report = evaluate(f.workspace, key, observations)
                self.assertEqual(report["status"], "FAIL")
                self.assertIn("F2_" + field.upper(), [c["id"] for c in report["checks"] if c["status"] == "FAIL"])
        f.write_json(observations, original)
        data = json.loads(key.read_text(encoding="utf-8"))
        data["expected"]["decision_date"] = "2026-12-02"
        f.write_json(key, data)
        with self.assertRaisesRegex(EvaluationError, "not effective"):
            evaluate(f.workspace, key, observations)
        data["expected"]["decision_date"] = "2026-11-14"
        data["primary_sources"]["cap"]["quote"] = "20 GB"
        f.write_json(key, data)
        with self.assertRaisesRegex(EvaluationError, "pinned primary term citation"):
            evaluate(f.workspace, key, observations)

    def test_f1_bad_aggregates_denominators_and_d7_values(self):
        f, key, observations, original = self.fixture("F1")
        for field, wrong in (("old_pct", 35), ("new_total_eligible", 199), ("delta_pp", True)):
            with self.subTest(field=field):
                obs = json.loads(json.dumps(original))
                obs["facts"][field]["value"] = wrong
                f.write_json(observations, obs)
                report = evaluate(f.workspace, key, observations)
                self.assertEqual(report["machine_status"], "FAIL")
                self.assertIn("F1_" + field.upper(), [c["id"] for c in report["checks"] if c["status"] == "FAIL"])

    def test_duplicate_json_and_nonfinite_values_are_blocked(self):
        f, key, observations, _ = self.fixture("F2")
        for payload in ('{"schema":"x","schema":"y"}', '{"value":NaN}', '{"value":Infinity}'):
            with self.subTest(payload=payload):
                key.write_text(payload, encoding="utf-8")
                with self.assertRaises(EvaluationError):
                    evaluate(f.workspace, key, observations)


    def test_f3_units_zero_contribution_and_unknowns(self):
        for field, wrong in (("ratio_unit", "shops"), ("demand_unknown", "VALIDATED"), ("scenario_status", "OBSERVED")):
            with self.subTest(field=field):
                f, key, observations, obs = self.fixture("F3")
                obs["facts"][field]["value"] = wrong
                f.write_json(observations, obs)
                report = evaluate(f.workspace, key, observations)
                self.assertIn("F3_" + field.upper(), [c["id"] for c in report["checks"] if c["status"] == "FAIL"])
        for contribution, unit, reason in (("0", "RUB_per_paid_shop_month", "must be positive"),
                                           ("50", "RUB", "invalid F3 units")):
            with self.subTest(contribution=contribution, unit=unit):
                f, key, observations, obs = self.fixture("F3")
                raw = f.raw / "economics.csv"
                raw.write_text("item,value,unit,status\nmax_validation_budget,200000,RUB,SYNTHETIC_SCENARIO\n"
                               f"net_contribution,{contribution},{unit},SYNTHETIC_SCENARIO\n", encoding="utf-8")
                (f.workspace / "raw/economics.csv").write_bytes(raw.read_bytes())
                inventory = f.root / "inventory.json"
                data = json.loads(inventory.read_text(encoding="utf-8"))
                data["sources"][0]["sha256"] = fixtures.digest(raw)
                f.write_json(inventory, data)
                for fact in obs["facts"].values():
                    fact["source"]["quote"] = raw.read_text(encoding="utf-8").strip()
                f.write_json(observations, obs)
                with self.assertRaisesRegex(EvaluationError, reason):
                    evaluate(f.workspace, key, observations)

    def test_junction_or_symlink_escape_is_rejected(self):
        for surface in ("evaluate", "stage"):
            with self.subTest(surface=surface):
                f, key, observations, _ = self.fixture("F2")
                outside = f.root / "outside"
                outside.mkdir()
                (outside / "private.md").write_text("must not be read or staged", encoding="utf-8")
                if surface == "evaluate":
                    link = f.workspace / "escape"
                else:
                    product = f.root / "product"
                    for name in ("AGENTS.md", ".agents/skills/one/SKILL.md", "prompts/first-run.md", "cases/_template/README.md"):
                        path = product / name
                        path.parent.mkdir(parents=True, exist_ok=True)
                        path.write_text("synthetic", encoding="utf-8")
                    link = product / "references"
                if os.name == "nt":
                    result = subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(outside)], capture_output=True)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.addCleanup(link.rmdir)
                else:
                    link.symlink_to(outside, target_is_directory=True)
                    self.addCleanup(link.unlink)
                with self.assertRaisesRegex(EvaluationError, "link/junction"):
                    if surface == "evaluate":
                        evaluate(f.workspace, key, observations)
                    else:
                        stage(product, f.raw, f.root / "inventory.json", f.root / "export")
                if surface == "stage":
                    self.assertFalse((f.root / "export").exists())

    def test_cli_digest_stale_review_and_report_collision(self):
        f, key, observations, obs = self.fixture("F2")
        cli = Path(__file__).resolve().parents[1] / "tools/functional_evaluator.py"
        args = [sys.executable, str(cli), "evaluate", "--workspace", str(f.workspace),
                "--key", str(key), "--observations", str(observations)]
        reports = []
        for seed in ("11", "131"):
            run = subprocess.run(args, env={**os.environ, "PYTHONHASHSEED": seed},
                                 capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(run.returncode, 3, run.stderr)
            reports.append(json.loads(run.stdout))
        self.assertEqual(reports[0]["evaluation_digest"], reports[1]["evaluation_digest"])
        reviews = f.root / "reviews.json"
        data = self.reviews("F2", reports[0], obs["facts"]["decision_date"])
        f.write_json(reviews, data)
        path = f.root / "report.json"
        accepted = subprocess.run([*args, "--reviews", str(reviews), "--report", str(path)],
                                  capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(accepted.returncode, 0, accepted.stderr)
        saved = path.read_bytes()
        collision = subprocess.run([*args, "--report", str(path)], capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(collision.returncode, 2)
        self.assertEqual(json.loads(collision.stderr)["status"], "BLOCKED")
        self.assertEqual(path.read_bytes(), saved)
        # Actual artifact mutation invalidates previously complete review, even
        # when all extracted terms and source locators still match.
        with (f.workspace / "answer.md").open("a", encoding="utf-8") as handle:
            handle.write("Additional candidate limitation.\n")
        self.assertEqual(evaluate(f.workspace, key, observations, reviews)["status"], "REVIEW_REQUIRED")


if __name__ == "__main__":
    unittest.main()
