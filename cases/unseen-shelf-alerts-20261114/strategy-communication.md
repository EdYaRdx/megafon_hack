# Communication strategy — R2, internal, pending human decision

## Audience and moment

The only justified audience/channel is the fictional internal ShelfSignal product team considering next-sprint scope; actual decision owner and review channel are `UNKNOWN` (brief.md:9–14). No external communication is authorized.

## Barrier to understanding or choice

The vendor digest states “40% fewer stockouts” and “14 opens out of 18 alerts,” but offers no supporting methods and conflicts with the CSV's 13 opened records (S-004, `input/vendor-export.html:6–8`; S-002, `input/pilot-alerts.csv:1–7`; E-003/E-004; C-003/C-009). A further barrier is treating six stores/18 alert records as representative or causal despite selected, non-randomized, two-week pilot design (S-003, `input/pilot-protocol.md:5–11`; E-002).

## Key message and supporting proof

**Internal message:** “The supplied fictional pilot is descriptive only: 13/18 alert records were opened and six orders were recorded within seven days. It does not show that alerts caused orders or reduced stockouts. Keep the next step human-gated and read-only; learn what user task, if any, merits testing before committing to automation. In this fictional R2 scenario, any future supplier-order submission requires explicit human confirmation for each order (S-007/E-007/C-010); this is not real policy or approval.”

Support: CSV rows 2–7 summed deterministically in E-003; study limitations in E-002; capability boundary in E-001; synthetic per-order confirmation constraint in S-007/E-007/C-010. This is not a claim about actual bookstore behavior.

## Product capability / condition supporting each promise

- Permissible factual description: prototype is documented as manual stock entry plus low-stock display (S-001, `input/concept-note.md:7–9`; C-001). It currently has no supplier connection, messaging/alerts, automated ordering or availability guarantee.
- Any future statement of impact requires a defined stockout measure and valid comparative evidence; neither exists (`UNKNOWN`, C-004).
- The 40% benefit statement is withheld, not repeated as a supported fact (C-003).

## Channel role and rationale

Internal written decision memo only, to support owner review. Actual recipient, channel, and timing remain `UNKNOWN`; no message has been sent. Public, customer, supplier, launch, or marketing channels are out of scope.

## Claims to withhold or qualify

Do not say “40% fewer stockouts,” “stores want automatic ordering,” that alerts drove orders, or that alerts prevented stockouts. The vendor's 14/18 figure conflicts with the CSV; report both provenance and discrepancy, with CSV count 13/18, rather than silently reconciling. Keep all synthetic figures explicitly labeled as scenario data. GOV.UK is method guidance, not evidence for demand or impact (S-005/E-005/C-007/C-009).
