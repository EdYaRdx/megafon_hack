# F2 exploratory matched evaluation — run log

- **Fixture:** `cases/offer-terms-demo/` revision 1; synthetic only.
- **Decision date:** 2026-11-14.
- **Shared inputs:** frozen brief, promotion HTML, terms v2 and v3. Same fixed clarification supplied. No web access or extra source material requested.
- **Arms:** B0 ordinary chat; B1 structured prompt; A read-only file-agent workflow with `AGENTS.md` and five canonical skills.
- **Sessions:** three independent OMP task contexts; outputs anonymized as `run-17.md`, `run-28.md`, `run-43.md`. Private mapping: B0→17, B1→28, A→43. Harness task durations: B0 15.0 s, B1 26.8 s, A 46.0 s; not human-active time or total model latency.
- **Controls/limits:** role-specific prompts; same task tool. Actual model/version/provider identity and equivalent resource budgets are not exposed. A was read-only and did not publish files or perform state writes: this tests instructions/response quality, not full workflow execution. Arms ran concurrently; order was not randomized. No retries in returned responses; billing/token telemetry unavailable.
- **Observed usage:** model/provider, input/output tokens, human-active time, and billing cost: `UNKNOWN`. Task duration above is the only timing signal.
- **Independent scoring:** two separate LLM task contexts produced identical rubric totals: B0 3/8, B1 5/8, A 5/8; zero P0 in all. Reviewer model/provider identity and cross-family independence are UNKNOWN. See `review-1.md`, `review-2.md`, and `adjudication.md`. One unsupported-name review finding was checked against the source and rejected.
- **Evaluation status:** one frozen fixture, one run per arm; exploratory, not statistically meaningful, no agent superiority or release claim.
- **Critical safety:** fictional terms only; no real user communication, product decision, spend, or publication.