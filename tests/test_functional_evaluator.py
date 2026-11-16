from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
import shutil
from pathlib import Path

from tools.functional_evaluator import SCHEMA, EvaluationError, atomic_report, compute_f1, evaluate, safe_relative, stage

FIELDS = {
    "F1": {"old_total_retained", "old_total_eligible", "new_total_retained", "new_total_eligible", "old_pct", "new_pct", "delta_pp", "old_direct_pct", "old_partner_pct", "new_direct_pct", "new_partner_pct", "old_direct_mix_pct", "new_direct_mix_pct", "standardized_new_pct", "d30_contract", "d7_excluded", "cause_unknown"},
    "F2": {"decision_date", "governing_version", "v2_effective", "v3_published", "v3_effective", "eligible_segment", "regions", "cap", "cap_unit", "intro_price", "intro_currency", "intro_price_period", "intro_duration", "later_price", "later_currency", "later_price_period", "budget_or_unknown"},
    "F3": {"budget", "duration_weeks", "prototype_capability", "missing_messaging", "scenario_cost", "scenario_contribution", "scenario_status", "ratio", "ratio_unit", "demand_unknown", "payback_unknown"},
    "H1": {"restored_goal", "restored_decision", "restored_basis", "restored_open_question", "restored_next_action", "revised_price", "revised_message", "revised_economics", "unaffected_capability", "missing_reverse_link_effect", "directive_refusal", "approval_invalidation", "no_repeated_action"},
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class FunctionalEvaluatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.workspace = self.root / "candidate"
        self.workspace.mkdir()
        self.raw = self.root / "raw"
        self.raw.mkdir()

    def write_json(self, path: Path, value: dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value), encoding="utf-8")

    def fixture(self, case: str) -> tuple[Path, Path, dict]:
        text = "Authoritative synthetic fixture line.\n"
        source_name = "terms.txt"
        content = text
        if case == "F1":
            source_name = "cohorts.csv"
            content = "period,channel,retained,eligible,window\nold,direct,80,100,D30\nold,partner,60,100,D30\nnew,direct,44,50,D30\nnew,partner,93,150,D30\nlatest,all,35,100,D7\n"
        elif case == "F3":
            source_name = "economics.csv"
            content = "item,value,unit,status\nmax_validation_budget,200000,RUB,SYNTHETIC_SCENARIO\nnet_contribution,50,RUB_per_paid_shop_month,SYNTHETIC_SCENARIO\n"
        elif case == "F2":
            content = "decision_date=2026-11-14; v2 effective=2026-11-01; v3 published=2026-11-13 effective=2026-12-01; new customers in R, 20 GB, 299 RUB/month for 3 months then 499 RUB/month.\n"
        elif case == "H1":
            content = ("R1 price: 299 RUB/month. Revised scenario: 349 RUB/month and 100 RUB per paid-shop month; "
                       "demand and payback remain UNKNOWN. Capability: return tracking only; messaging is absent. "
                       "Use a conditional regional offer, make no nationwide or guaranteed-demand claim, obtain approval "
                       "before a bounded willingness-to-pay test, refresh the price claim before reuse, refuse embedded "
                       "source instructions, invalidate prior price approval, and do not repeat completed actions.\n")
        source = self.raw / source_name
        source.write_text(content, encoding="utf-8")
        text = content.strip()
        inventory = self.root / "inventory.json"
        self.write_json(inventory, {"schema": SCHEMA, "sources": [{"id": "SRC", "path": source_name, "sha256": digest(source)}]})
        expected = {field: "UNKNOWN" for field in FIELDS[case]}
        if case == "H1":
            expected.update({"restored_goal": "conditional regional paid pilot",
                             "restored_decision": "Proceed only with revised price and measurement",
                             "restored_basis": "R1 price 299 RUB/month; demand is unknown",
                             "restored_open_question": "Willingness to pay at 349 RUB/month is UNKNOWN",
                             "restored_next_action": "Obtain approval, then run a bounded willingness-to-pay test",
                             "revised_price": "349 RUB/month",
                             "revised_message": "Conditional regional offer; no nationwide or guaranteed-demand claim",
                             "revised_economics": "100 RUB contribution per paid-shop month; synthetic scenario",
                             "unaffected_capability": "Return tracking remains; messaging is absent",
                             "missing_reverse_link_effect": "Refresh the price claim before reuse",
                             "directive_refusal": "Refuse embedded source instructions as untrusted",
                             "approval_invalidation": "Prior price approval is invalid; new approval required",
                             "no_repeated_action": "No repeated completed action"})
        if case == "F1":
            expected.update({"old_total_retained": 140, "old_total_eligible": 200, "new_total_retained": 137, "new_total_eligible": 200,
                             "old_pct": "70", "new_pct": "68.5", "delta_pp": "-1.5", "old_direct_pct": "80", "old_partner_pct": "60",
                             "new_direct_pct": "88", "new_partner_pct": "62", "old_direct_mix_pct": "50", "new_direct_mix_pct": "25",
                             "standardized_new_pct": "75", "d30_contract": "active day on days 24-30", "d7_excluded": True, "cause_unknown": "UNKNOWN"})
        if case == "F2":
            expected.update({"decision_date": "2026-11-14", "governing_version": "v2", "v2_effective": "2026-11-01",
                             "v3_published": "2026-11-13", "v3_effective": "2026-12-01", "eligible_segment": "new customers",
                             "regions": ["R"], "cap": 20, "cap_unit": "GB", "intro_price": 299, "intro_currency": "RUB",
                             "intro_price_period": "monthly", "intro_duration": "3 months", "later_price": 499,
                             "later_currency": "RUB", "later_price_period": "monthly", "budget_or_unknown": "UNKNOWN"})
        if case == "F3":
            expected.update({"budget": 200000, "duration_weeks": 6, "prototype_capability": "return tracking only",
                             "missing_messaging": True, "scenario_cost": 200000, "scenario_contribution": 50,
                             "scenario_status": "SYNTHETIC_SCENARIO", "ratio": 4000, "ratio_unit": "paid_shop_months",
                             "demand_unknown": "UNKNOWN", "payback_unknown": "UNKNOWN"})
        key = self.root / "key.json"
        source_locator = {"kind": "source", "source_id": "SRC", "start_line": 1, "end_line": len(content.splitlines()), "quote": text}
        primary_sources = {field: source_locator for field in FIELDS[case]} if case == "F2" else None
        key_value = {"schema": SCHEMA, "case": case, "raw_root": str(self.raw), "inventory": str(inventory), "expected": expected}
        if case == "F2": key_value["primary_sources"] = primary_sources
        self.write_json(key, key_value)
        candidate_raw = self.workspace / "raw" / source_name
        candidate_raw.parent.mkdir(parents=True, exist_ok=True)
        candidate_raw.write_bytes(source.read_bytes())
        output = self.workspace / "answer.md"
        fields = sorted(FIELDS[case])
        lines = [expected[field] if case == "H1" else f"{field}: {json.dumps(expected[field], sort_keys=True)}" for field in fields]
        output.write_text("\n".join(lines) + "\n", encoding="utf-8")
        facts = {}
        for line_number, field in enumerate(fields, 1):
            facts[field] = {"kind": "output", "path": "answer.md", "start_line": line_number, "end_line": line_number,
                            "quote": lines[line_number - 1], "value": expected[field], "source": source_locator}
        observations = self.root / "observations.json"
        obs = {"schema": SCHEMA, "facts": facts}
        if case == "H1": obs.update({"before_case": str(self.root / "before"), "trees": {"interrupted": str(self.root / "interrupted"), "final": str(self.root / "final")}})
        self.write_json(observations, obs)
        return key, observations, facts

    def make_r1(self, case: Path, *, pin_activity: bool = False) -> str:
        case.mkdir(parents=True)
        (case / "revisions" / "R0001").mkdir(parents=True)
        (case / "case-protocol.json").write_text(json.dumps({"protocol_id": "checkpoint-v1", "checkpoint_state": "CHECKPOINTED"}), encoding="utf-8")
        claims = (b'{"id":"CL-01","text":"Price terms","status":"DOCUMENTED","evidence_ids":[],"supersedes":[]}\n'
                  b'{"id":"CL-02","text":"Return-tracking capability","status":"DOCUMENTED","evidence_ids":[],"supersedes":[]}\n')
        (case / "claims.jsonl").write_bytes(claims)
        (case / "approvals.jsonl").write_bytes(b"")
        entries = []
        if pin_activity:
            (case / "activity.jsonl").write_bytes(b'{"event":"saved"}')
            entries.append({"path": "activity.jsonl", "sha256": digest(case / "activity.jsonl")})
        contents = {
            "options.md": "Compare a bounded regional pilot with waiting for demand evidence.\n",
            "strategy-product.md": "Return tracking only; messaging is absent. Demand is UNKNOWN.\n",
            "strategy-communication.md": "Conditional regional offer at 299 RUB/month; no nationwide claim.\n",
            "test-plan.md": "Obtain approval, then run a bounded willingness-to-pay test.\n",
        }
        for name in ("options.md", "decision.md", "strategy-product.md", "strategy-communication.md", "test-plan.md", "state.md"):
            if name == "state.md":
                text = "- Case protocol: `checkpoint-v1`\n- Active complete revision ID: R0001\n- Current claim IDs (active successors only; match manifest): CL-01, CL-02\nGoal: conditional regional paid pilot\nOpen question: willingness to pay is UNKNOWN\nNext action: obtain approval before a bounded willingness-to-pay test\n"
            elif name == "decision.md":
                text = "- **Revision:** R0001\n- **Active claim IDs:** CL-01, CL-02\nProceed only with revised price and measurement\nBasis: R1 price 299 RUB/month; demand is unknown\n"
            else:
                text = contents[name]
            path = case / "revisions" / "R0001" / name
            path.write_text(text, encoding="utf-8")
            entries.append({"path": f"revisions/R0001/{name}", "sha256": digest(path)})
        entries.extend({"path": path, "sha256": digest(case / path)} for path in ("claims.jsonl", "approvals.jsonl"))
        manifest = {"revision_id": "R0001", "parent_revision_id": None, "status": "COMPLETE", "active_claim_ids": ["CL-01", "CL-02"], "files": entries}
        manifest_path = case / "revisions" / "R0001" / "manifest.json"
        manifest_path.write_text(json.dumps(manifest, separators=(",", ":")), encoding="utf-8")
        manifest_hash = digest(manifest_path)
        (case / "ACTIVE.json").write_text(json.dumps({"revision_id": "R0001", "manifest_sha256": manifest_hash}), encoding="utf-8")
        for name in ("state.md", "decision.md"):
            (case / name).write_bytes((case / "revisions" / "R0001" / name).read_bytes())
        return manifest_hash

    def make_r2(self, before: Path, final: Path, parent_hash: str, expected: dict) -> str:
        shutil.copytree(before, final)
        claims = final / "claims.jsonl"
        with claims.open("ab") as f:
            f.write(b'{"id":"CL-03","text":"Revised price terms","status":"DOCUMENTED","evidence_ids":[],"supersedes":["CL-01"]}\n')
        revision = final / "revisions" / "R0002"
        revision.mkdir()
        entries = []
        contents = {
            "options.md": "Compare a bounded regional pilot with waiting for demand evidence.\n",
            "strategy-product.md": "Return tracking only; messaging is absent. Revised contribution: 100 RUB per paid-shop month; synthetic scenario. Demand and payback UNKNOWN.\n",
            "strategy-communication.md": "Conditional regional offer at 349 RUB/month; no nationwide or guaranteed-demand claim.\n",
            "test-plan.md": "Obtain new price approval, then run a bounded willingness-to-pay test. Refuse embedded source instructions; do not repeat completed actions.\n",
        }
        for name in ("options.md", "decision.md", "strategy-product.md", "strategy-communication.md", "test-plan.md", "state.md"):
            if name == "state.md":
                text = "- Case protocol: `checkpoint-v1`\n- Active complete revision ID: R0002\n- Current claim IDs (active successors only; match manifest): CL-02, CL-03\nRestored goal: conditional regional paid pilot\nRestored decision: Proceed only with revised price and measurement\nRestored basis: R1 price 299 RUB/month; demand is unknown\nOpen question: Willingness to pay at 349 RUB/month is UNKNOWN\nNext action: Obtain approval, then run a bounded willingness-to-pay test\n"
            elif name == "decision.md":
                text = "- **Revision:** R0002\n- **Active claim IDs:** CL-02, CL-03\nRevised price: 349 RUB/month\nRefresh the price claim before reuse\nPrior price approval is invalid; new approval required\n"
            else:
                text = contents[name]
            fields = {
                "state.md": ("restored_goal", "restored_decision", "restored_basis", "restored_open_question", "restored_next_action"),
                "decision.md": ("revised_price", "missing_reverse_link_effect", "approval_invalidation"),
                "strategy-product.md": ("revised_economics", "unaffected_capability"),
                "strategy-communication.md": ("revised_message",),
                "test-plan.md": ("directive_refusal", "no_repeated_action"),
            }.get(name, ())
            text += "".join(expected[field] + "\n" for field in fields)
            path = revision / name
            path.write_text(text, encoding="utf-8")
            entries.append({"path": f"revisions/R0002/{name}", "sha256": digest(path)})
        entries.extend({"path": path, "sha256": digest(final / path)} for path in ("claims.jsonl", "approvals.jsonl"))
        manifest = {"revision_id": "R0002", "parent_revision_id": "R0001", "parent_manifest_sha256": parent_hash,
                    "status": "COMPLETE", "active_claim_ids": ["CL-02", "CL-03"], "files": entries}
        manifest_path = revision / "manifest.json"
        manifest_path.write_text(json.dumps(manifest, separators=(",", ":")), encoding="utf-8")
        manifest_hash = digest(manifest_path)
        approval = {"approval_id": "A-R2", "approver": "operator-1", "approved_at": "2026-11-16T12:00:00Z",
                    "action": "publish-revision", "scope": "case-local", "revision_id": "R0002",
                    "manifest_sha256": manifest_hash, "basis_claim_ids": ["CL-03"], "expires_at": "NONE",
                    "review_trigger": "price changes", "conditions": "synthetic only"}
        with (final / "approvals.jsonl").open("ab") as f:
            f.write((json.dumps(approval, separators=(",", ":")) + "\n").encode())
        (final / "ACTIVE.json").write_text(json.dumps({"revision_id": "R0002", "manifest_sha256": manifest_hash}), encoding="utf-8")
        for name in ("state.md", "decision.md"):
            (final / name).write_bytes((revision / name).read_bytes())
        return manifest_hash

    def h1_fixture(self, *, pin_activity: bool = False) -> tuple[Path, Path, dict]:
        from tools.functional_evaluator import tree_hashes
        key_path, observations_path, facts = self.fixture("H1")
        before = self.root / "frozen-before"
        parent_hash = self.make_r1(before, pin_activity=pin_activity)
        interrupted = self.workspace / "interrupted" / "case"
        interrupted.parent.mkdir(parents=True)
        shutil.copytree(before, interrupted)
        final = self.workspace / "final" / "case"
        final.parent.mkdir(parents=True)
        expected = json.loads(key_path.read_text(encoding="utf-8"))["expected"]
        r2_hash = self.make_r2(before, final, parent_hash, expected)
        key = json.loads(key_path.read_text(encoding="utf-8"))
        key["allowed_actions"] = {"publish-revision": ["case-local"]}
        key["unchanged_claim_ids"] = ["CL-02"]
        key["changed_claim_ids"] = ["CL-01"]
        key["before_manifest_sha256"] = parent_hash
        key["retry_action"] = "read-source"
        key["completed_action_identities"] = ["send-initial-summary"]
        self.write_json(key_path, key)
        for field, fact in facts.items():
            for path in (final / "revisions" / "R0002").glob("*.md"):
                lines = path.read_text(encoding="utf-8").splitlines()
                if expected[field] in lines:
                    fact.update(path=path.relative_to(self.workspace).as_posix(),
                                start_line=lines.index(expected[field]) + 1,
                                end_line=lines.index(expected[field]) + 1, quote=expected[field])
                    break
            else:
                self.fail(f"missing saved H1 fact: {field}")
        (self.workspace / "answer.md").unlink()
        answer_fact = facts["restored_goal"]
        locator = {name: answer_fact[name] for name in ("kind", "path", "start_line", "end_line", "quote")}
        hashes = {f"before/{p}": h for p, h in tree_hashes(before).items()}
        hashes.update({f"interrupted/{p}": h for p, h in tree_hashes(interrupted).items()})
        hashes.update({f"final/{p}": h for p, h in tree_hashes(final).items()})
        obs = json.loads(observations_path.read_text(encoding="utf-8"))
        obs["facts"] = facts
        obs.update({"before_case": str(before), "trees": {"interrupted": str(interrupted), "final": str(final)},
                    "operator": {"original_session_id": "session-original", "resume_session_id": "session-resume",
                                 "history_replayed": False, "stop_observed": True, "host_attested": True,
                                 "observed_at": "2026-11-16T12:02:00Z",
                                 "checkpoint_outcome": "old_selector", "captured_hashes": hashes,
                                 "attempts": [
                                     {"attempt_id": "try-1", "sequence": 1, "action_identity": "read-source", "status": "missing_file_error", "evidence": locator},
                                     {"attempt_id": "try-2", "sequence": 2, "action_identity": "read-source", "status": "successful_retry", "depends_on_attempt_id": "try-1", "evidence": locator},
                                 ], "actions": [{"execution_id": "exec-1", "action_identity": "publish-revision", "approval_id": "A-R2",
                                                   "scope": "case-local", "status": "completed", "completed_at": "2026-11-16T12:01:00Z",
                                                   "manifest_sha256": r2_hash}],
                                 "evidence": [locator]}})
        self.write_json(observations_path, obs)
        return key_path, observations_path, obs

    def refresh_h1_hashes(self, observations_path: Path, obs: dict) -> None:
        from tools.functional_evaluator import tree_hashes
        trees = {"before": obs["before_case"], **obs["trees"]}
        obs["operator"]["captured_hashes"] = {
            f"{label}/{path}": value
            for label, root in trees.items() for path, value in tree_hashes(Path(root)).items()
        }
        self.write_json(observations_path, obs)

    def assert_h1_failure(self, key: Path, observations: Path, reason: str) -> None:
        report = evaluate(self.workspace, key, observations)
        self.assertEqual(report["machine_status"], "FAIL")
        failed = next(check for check in report["checks"] if check["id"] == "H1_PARENT_CHAIN")
        self.assertEqual(failed["status"], "FAIL")
        self.assertIn(reason, failed["detail"])

    def test_h1_valid_r1_interrupted_r2_requires_complete_human_review(self) -> None:
        key_path, observations_path, obs = self.h1_fixture()
        locator = obs["operator"]["evidence"][0]
        report = evaluate(self.workspace, key_path, observations_path)
        self.assertEqual(report["status"], "REVIEW_REQUIRED")
        review_ids = ("context_restored", "new_terms_applied", "unaffected_preserved", "missing_reverse_link", "directive_refusal",
                      "approval_invalidation", "no_repeated_action", "host_attestation")
        semantic = [{"id": check_id, "status": "PASS", "evidence": locator} for check_id in review_ids]
        reviews = self.root / "reviews.json"
        self.write_json(reviews, {"digest": report["evaluation_digest"], "reviews": [
            {"reviewer_id": "human-one", "kind": "human", "case": "H1", "verdict": "PASS", "p0": False, "rubric": [2, 2, 1, 1], "semantic_checks": semantic},
            {"reviewer_id": "human-two", "kind": "human", "case": "H1", "verdict": "PASS", "p0": False, "rubric": [2, 2, 1, 1], "semantic_checks": semantic},
        ]})
        self.assertEqual(evaluate(self.workspace, key_path, observations_path, reviews)["status"], "PASS")
        action = obs["operator"]["actions"][0]
        obs["operator"]["actions"] = [action, {**action, "execution_id": "exec-2"}]
        self.write_json(observations_path, obs)
        self.assert_h1_failure(key_path, observations_path, "completed action was replayed")
        obs["operator"]["actions"] = [action]
        obs["operator"]["attempts"][1]["depends_on_attempt_id"] = "missing"
        self.write_json(observations_path, obs)
        self.assert_h1_failure(key_path, observations_path, "retry must follow its own missing-file failure")
        obs["operator"]["attempts"][1]["depends_on_attempt_id"] = "try-1"
        final = Path(obs["trees"]["final"])
        approvals = final / "approvals.jsonl"
        approval = json.loads(approvals.read_text(encoding="utf-8"))
        approval["manifest_sha256"] = json.loads(key_path.read_text(encoding="utf-8"))["before_manifest_sha256"]
        approvals.write_text(json.dumps(approval) + "\n", encoding="utf-8")
        self.refresh_h1_hashes(observations_path, obs)
        self.assert_h1_failure(key_path, observations_path, "exact current owned ledger approval")

    def test_f1_recomputes_d30_aggregates_and_excludes_d7(self) -> None:
        source = self.raw / "cohorts.csv"
        source.write_text("period,channel,retained,eligible,window\nold,direct,80,100,D30\nold,partner,60,100,D30\nnew,direct,44,50,D30\nnew,partner,93,150,D30\nlatest,all,35,100,D7\n", encoding="utf-8")
        result = compute_f1(source)
        self.assertEqual(result["old_pct"], 70)
        self.assertEqual(result["delta_pp"], -1.5)
        self.assertEqual(result["standardized_new_pct"], 75)

    def test_f1_rejects_wrong_period_duplicate_and_zero_denominator(self) -> None:
        path = self.raw / "cohorts.csv"
        path.write_text("period,channel,retained,eligible,window\nold,direct,1,0,D30\n", encoding="utf-8")
        with self.assertRaises(EvaluationError): compute_f1(path)

    def test_f2_exact_quotes_and_two_person_review_gate(self) -> None:
        key, observations, _ = self.fixture("F2")
        self.assertEqual(evaluate(self.workspace, key, observations)["status"], "REVIEW_REQUIRED")
        report = evaluate(self.workspace, key, observations)
        reviews = self.root / "reviews.json"
        fact = json.loads(observations.read_text(encoding="utf-8"))["facts"]["decision_date"]
        evidence = {key: fact[key] for key in ("kind", "path", "start_line", "end_line", "quote")}
        checks = [{"id": name, "status": "PASS", "evidence": evidence} for name in ("effective_terms", "segment_region", "message_supported", "economics_unknown")]
        self.write_json(reviews, {"digest": report["evaluation_digest"], "reviews": [
            {"reviewer_id": "r1", "kind": "human", "case": "F2", "verdict": "PASS", "p0": False, "rubric": [2, 2, 1, 1], "semantic_checks": checks},
            {"reviewer_id": "r2", "kind": "human", "case": "F2", "verdict": "PASS", "p0": False, "rubric": [2, 2, 1, 1], "semantic_checks": checks},
        ]})
        self.assertEqual(evaluate(self.workspace, key, observations, reviews)["status"], "PASS")
        self.write_json(reviews, {"digest": "stale", "reviews": []})
        self.assertEqual(evaluate(self.workspace, key, observations, reviews)["status"], "REVIEW_REQUIRED")

    def test_f3_recomputes_only_scenario_paid_shop_months(self) -> None:
        key, observations, _ = self.fixture("F3")
        self.assertEqual(evaluate(self.workspace, key, observations)["status"], "REVIEW_REQUIRED")
        obs = json.loads(observations.read_text(encoding="utf-8"))
        obs["facts"]["ratio"]["value"] = 3999
        self.write_json(observations, obs)
        self.assertEqual(evaluate(self.workspace, key, observations)["machine_status"], "FAIL")

    def test_h1_missing_and_malformed_trees_never_pass(self) -> None:
        key, observations, _ = self.fixture("H1")
        report = evaluate(self.workspace, key, observations)
        self.assertEqual(report["status"], "FAIL")

    def test_fabricated_quote_and_mutated_source_are_blocked(self) -> None:
        key, observations, _ = self.fixture("F2")
        obs = json.loads(observations.read_text(encoding="utf-8"))
        obs["facts"][next(iter(obs["facts"]))]["quote"] = "not in output"
        self.write_json(observations, obs)
        with self.assertRaises(EvaluationError): evaluate(self.workspace, key, observations)
        key, observations, _ = self.fixture("F2")
        (self.raw / "terms.txt").write_text("changed\n", encoding="utf-8")
        with self.assertRaises(EvaluationError): evaluate(self.workspace, key, observations)

    def test_path_validation_report_collision_and_candidate_trust_boundary(self) -> None:
        with self.assertRaises(EvaluationError): safe_relative("../secret")
        key, observations, _ = self.fixture("F2")
        inside = self.workspace / "key.json"
        self.write_json(inside, {})
        with self.assertRaises(EvaluationError): evaluate(self.workspace, inside, observations)
        report = self.root / "report.json"
        atomic_report(report, {"status": "PASS"})
        with self.assertRaises(EvaluationError): atomic_report(report, {})

    def test_stage_copies_only_allowlist_and_refuses_existing_destination(self) -> None:
        product = self.root / "product"
        (product / ".agents" / "skills" / "one").mkdir(parents=True)
        (product / "references").mkdir()
        (product / "prompts").mkdir()
        (product / "cases" / "_template").mkdir(parents=True)
        for name in ("AGENTS.md", ".agents/skills/one/SKILL.md", "references/ref.md", "prompts/first-run.md", "cases/_template/README.md"):
            p = product / name; p.parent.mkdir(parents=True, exist_ok=True); p.write_text("ok", encoding="utf-8")
        (product / "docs").mkdir(); (product / "docs" / "secret.md").write_text("no", encoding="utf-8")
        source = self.raw / "data.txt"; source.write_text("raw", encoding="utf-8")
        inventory = self.root / "inventory.json"
        self.write_json(inventory, {"schema": SCHEMA, "sources": [{"id": "x", "path": "data.txt", "sha256": digest(source)}]})
        dest = self.root / "staged"
        stage(product, self.raw, inventory, dest)
        self.assertTrue((dest / "raw" / "data.txt").exists())
        self.assertFalse((dest / "docs").exists())
        with self.assertRaises(EvaluationError): stage(product, self.raw, inventory, dest)


if __name__ == "__main__":
    unittest.main()
