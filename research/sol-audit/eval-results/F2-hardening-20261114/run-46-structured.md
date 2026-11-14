# F2 run 46 — structured-compliance check (not the natural-prompt run)

## Decision memo — synthetic case, 2026-11-14

**Scope:** Fictional records only. This memo prepares decision support; it does not approve publication, spend, customer contact, launch, or a legal conclusion.

### Terms by effective date

- **Current, 2026-11-14:** The mock-up says “Unlimited for 299 ₽ per month,” “Available nationwide,” and “Start today” (S-001, `cases/offer-terms-demo/input/promo.html`, `#offer`, lines 4–7). But the terms effective 2026-11-01 apply only to **new customers in Region R**, cap included data at **20 GB per billing month**, restrict access after the cap, and charge **299 ₽/month for the first three billing months, then 499 ₽/month** (S-002, `cases/offer-terms-demo/input/terms-v2.md`, §4, lines 3–7). The supplied records therefore do not substantiate the mock-up’s unlimited, nationwide, or flat-price claims for the decision date (C-004; E-001–E-004).
- **Future, from 2026-12-01:** Published 2026-11-13, v3 adds **Region S**; it still applies only to new customers, retains the 20 GB cap and access restriction, and has the same two price phases. Until its effective date, earlier effective terms remain in force (S-003, `cases/offer-terms-demo/input/terms-v3.md`, §4, lines 3–7; C-003; E-003).

These are synthetic-document facts, not validation of real-world applicability or legal compliance.

### Unknowns that constrain the decision

Campaign economics, audience reach, eligibility totals, customer outcomes, legal applicability, and launch approval are **UNKNOWN** (C-005; `cases/offer-terms-demo/claims.jsonl`, line 5). No evidence establishes demand, preferred audience beyond stated eligibility, campaign cost, or whether a corrected offer is commercially viable.

### Options

1. **Revise for current terms; hold for approval.** Prepare internal copy limited to new customers in Region R and stating the cap, post-cap restriction, and both price phases. It matches the supplied current terms (S-002, §4); costs, benefits, and audience response are **UNKNOWN**. Risk: missing legal, operational, or commercial requirements; the strongest objection is that narrowing the offer may not support the intended campaign.
2. **Defer and prepare a future version.** Do not present Region S as eligible before 2026-12-01; prepare a separately dated draft for new customers in Regions R and S, with the same cap and price phases, subject to approval. Potential benefit is broader documented eligibility after that date; reach, economics, and readiness are **UNKNOWN**. Risk: delay or changes before effectiveness; the strongest objection is that waiting does not establish campaign value.
3. **СТАТУС-КВО — leave the mock-up unchanged, with no launch.** Preserve the supplied copy internally but do not publish, spend, or contact customers. Cost and benefit are **UNKNOWN**. This avoids an external action now, but leaves unsupported claims in the draft; it is not a viable publication choice on the supplied evidence. Revisit when corrected terms and human approval are available.
4. **Stop/close the campaign.** Withdraw the mock-up from consideration and take no further campaign action. This avoids proceeding on unverified campaign economics or approval; foregone value and closure cost are **UNKNOWN**. The strongest objection is that the records do not show the underlying offer lacks value. Reopen only with a newly approved brief and substantiated terms.

### Recommendation

**Do not approve the mock-up or launch.** Choose option 1 for internal preparation of a corrected, current-terms draft, while keeping publication and any external action on hold for human approval. This is the most directly supported next step: v2 is effective on the decision date, while v3 is not (S-002, §4, lines 3–7; S-003, §4, lines 3–7). Deliberately forgo the nationwide/unlimited/flat-299 framing because the supplied terms contradict it (S-001, `promo.html`, `#offer`, lines 4–7; S-002, §4, lines 6–7; C-004). Decision owner and approval timing are **UNKNOWN**.

### Communication fields

- **Audience / moment:** Proposed offer audience, if later approved: new customers in Region R considering the offer while the current terms apply. Actual audience and choice moment are **UNKNOWN**. Internal decision audience/channel: **UNKNOWN**.
- **Barrier:** Whether customers understand the Region R/new-customer eligibility, 20 GB monthly cap and restriction after the cap, and price increase after three billing months is **UNKNOWN**.
- **Evidence-linked draft, for internal review only:** “Для новых клиентов в регионе R: 20 ГБ в месяц. 299 ₽ в месяц первые три расчётных месяца, затем 499 ₽ в месяц. После исчерпания 20 ГБ доступ ограничивается.” Each term comes from S-002, §4, lines 6–7. Do not add “безлимитно,” “по всей стране,” or an unqualified “299 ₽ в месяц”; those claims are not supported for the current date (C-004).
- **Channel / next step:** External channel and next step are **UNKNOWN**; no external communication is authorized. Route the draft for internal human review through a channel the decision owner identifies.

### Validation plan — not ready to run

- **Question:** Does corrected copy communicate the documented current eligibility, data limit/post-cap restriction, and both price phases more accurately than the supplied mock-up?
- **Comparator:** Corrected draft versus the existing mock-up. Do not expose the unsupported mock-up to real customers; any real-audience comparison requires prior human approval and appropriate permissions.
- **Audience / sample:** **UNKNOWN**; define eligible audience, sampling method, and sample size before collection.
- **Primary metric:** Per arm, `readers correctly identifying all specified eligibility, data-limit/post-cap, and price-phase terms ÷ readers exposed to that arm`; comparison is corrected-copy rate minus comparator rate. Baseline, source of responses, and decision threshold are **UNKNOWN**.
- **Period:** **UNKNOWN**; set before collection.
- **Guardrails:** Misunderstanding of eligibility, cap/restriction, or later price; formulas, acceptable limits, and measurement method are **UNKNOWN** and must be set before collection.
- **Threshold / revisit:** **UNKNOWN**. The human decision owner must set thresholds and a review date before any test; if results miss the threshold or guardrails, revise or stop. No testing, customer contact, or publication is authorized.