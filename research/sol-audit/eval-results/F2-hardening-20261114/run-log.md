# F2 targeted post-hardening regression — run log

- **Case:** frozen synthetic F2 terms case, decision date 2026-11-14.
- **Prompt control:** same request and clarification as F2 B0/B1/A: “You may change the audience and wording. There is no other confirmation of the price or conditions.”
- **Treatment:** fresh OMP task context read current root `AGENTS.md`, skills for intake/evidence/options/communication/experiment design, and brief + source inputs. It was explicitly barred from prior output/reviews/key and case edits. This is an answer-only run, not a complete state-writing workflow; `sources.jsonl`, `evidence.jsonl`, and `claims.jsonl` were not in its permitted read set.
- **Output:** `run-44.md`; file-agent task duration 36.0s. Provider/model/version, human time, tokens, retries and billing are `UNKNOWN`.
- **Blind reviews:** two separate LLM task contexts scored the opaque output 6/8 and 7/8; see `review-1.md`, `review-2.md`, `adjudication.md`. Reviewer model/provider identity and cross-family independence are `UNKNOWN`; this is not human adjudication.
- **Adjudicated rubric:** four dimensions, 0–2 each: research/evidence; options/product; communication; validation. After hardening, exact local paths/locators and explicit hold/status quo plus stop/close options are present. Communication is incomplete (no audience/moment/barrier/channel); validation identifies a comparator and guardrails but omits metric formula/denominator, period and threshold, labeling these unknown.
- **Historical comparison:** prior F2 A response `F2-20261113/run-43.md` scored 5/8 on the same case, with status quo and validation detail gaps. New response scored 6/8 by integration adjudication; this one-run difference is exploratory only, not causal or statistical. Model/tool/resource equivalence is unknown.
- **P0:** none reported by reviewers. Terms are fictional; no legal, commercial, launch, or publication approval.
