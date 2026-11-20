"""Deterministic arithmetic from the pinned PDF derivatives; no effect forecast."""
import hashlib
import json
import re
from pathlib import Path

CASE = Path(__file__).resolve().parents[1]
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
provenance = json.loads((CASE / 'inputs/provenance.json').read_text(encoding='utf-8'))
pdf = CASE / provenance['case_copy']
if sha(pdf) != provenance['sha256']:
    raise ValueError('Pinned PDF hash mismatch')
page3 = CASE / 'inputs/brief-extracted/page-03.txt'
page9 = CASE / 'inputs/brief-extracted/page-09.txt'
page8 = CASE / 'inputs/brief-extracted/page-08.txt'
text3 = page3.read_text(encoding='utf-8')
rows = [x.strip() for x in text3.splitlines() if re.fullmatch(r'\d[\d\s]*(?:%|9/0)?', x.strip())]
if len(rows) != 20:
    raise ValueError(f'Expected exactly 20 table entries, got {len(rows)}')
# Column order verified visually against original PDF page 3, recorded in provenance.
# The only OCR correction is 45 9/0 -> 45 percent; raw string retained below.
nums = [int(re.sub(r'\s|%|9/0', '', x)) for x in rows]
names = ['gross_profit_million_rub', 'active_groups_last_month', 'connected_groups_eoy',
         'connected_owners_eoy', 'activation_14d_percent']
columns = ['base_plan', 'base_estimate', 'plan_no_change', 'plan_target']
table = {col: dict(zip(names, nums[i*5:(i+1)*5])) for i, col in enumerate(columns)}
text9 = page9.read_text(encoding='utf-8')
rate_matches = re.findall(r'ставка\s*[—–-]\s*(\d+)\s*руб', text9)
if len(rate_matches) != 1:
    raise ValueError('Could not uniquely extract educational margin rate')
rate = int(rate_matches[0])
market_match = re.search(r'доступны\s+(\d+)\s*тыс\.\s*домохозяйств\s+и\s+(\d+)\s*тыс\.\s*владельцев', text3)
if not market_match:
    raise ValueError('Available market extraction failed')
families, owners = (int(x)*1000 for x in market_match.groups())
b, e, n, t = (table[x] for x in columns)
gap_rub = (t[names[0]] - n[names[0]]) * 1_000_000
family_activity_base = n[names[1]] / n[names[2]]
family_activity_target = t[names[1]] / t[names[2]]
result = {
 'purpose': 'Учебные разрывы и условия достижимости; не прогноз эффекта и не реальные данные оператора',
 'source': {'pdf': provenance['case_copy'], 'pdf_sha256': sha(pdf),
            'locators': ['PDF стр. 3, таблица исходных показателей и доступные рынки', 'PDF стр. 9, ставка и граница решения'],
            'derivative_hashes': {str(p.relative_to(CASE)): sha(p) for p in [page3,page9,page8]},
            'raw_table_cells': rows, 'ocr_corrections': ['45 9/0 interpreted as 45 %, visually verified on PDF page 3']},
 'table': table,
 'base_shortfall': {k:b[k]-e[k] for k in names},
 'target_minus_no_change': {k:t[k]-n[k] for k in names},
 'available_market': {'households':families,'owners':owners},
 'family_net_additions': {'no_change':n[names[2]]-e[names[2]], 'target':t[names[2]]-e[names[2]], 'increment_over_no_change':t[names[2]]-n[names[2]]},
 'owner_net_additions': {'no_change':n[names[3]]-e[names[3]], 'target':t[names[3]]-e[names[3]], 'increment_over_no_change':t[names[3]]-n[names[3]]},
 'penetration_percent': {'families_no_change':100*n[names[2]]/families,'families_target':100*t[names[2]]/families,'owners_no_change':100*n[names[3]]/owners,'owners_target':100*t[names[3]]/owners},
 'activity': {'no_change_share':family_activity_base,'target_share':family_activity_target,'difference_percentage_points':100*(family_activity_target-family_activity_base),'growth_due_to_connections_at_unchanged_share':(t[names[2]]-n[names[2]])*family_activity_base,'remaining_active_groups_due_to_share_change':t[names[1]]-t[names[2]]*family_activity_base},
 'profit_boundary': {'gap_rub':gap_rub,'rub_per_extra_paid_number_month':rate,'extra_paid_number_months_if_other_contribution_and_new_direct_cost_zero':gap_rub/rate,'formula':'M_required = max(0, (6_000_000 + new_direct_cost_RUB - other_incremental_gross_contribution_RUB) / 500)','unit':'additional paid number-months within plan year; never household-months','sensitivity_grid_not_a_forecast':[{'hypothetical_new_direct_cost_rub':c,'other_contribution_rub':0,'required_extra_paid_number_months':(gap_rub+c)/rate} for c in [0,1_000_000,3_000_000]]},
 'rules': {'rounding':'full float precision in JSON; percentage displays may round to 2 decimals; integer requirements round upward if operationally indivisible','missing':'unknown effect, costs, take-up, retention, recruitment and statistical parameters are not replaced with numbers','failures':'mismatched PDF hash, ambiguous extraction or wrong cell count raises and returns nonzero'},
 'formulas': ['shortfall = base_plan - base_estimate','target_gap = plan_target - plan_no_change','connected_end = connected_start + new_connected - exited','active_share = active_groups_last_month / connected_groups_eoy','penetration = connected_eoy / available_unique_market','gross_profit = 279_000_000 + 500 * sum(number_paid_treatment_minus_counterfactual_by_month) + other_incremental_contribution - new_direct_cost','investment_ceiling_at_T = cumulative_incremental_profit_after_direct_cost_through_T; development is separate','paid_months = sum_cohort sum_month(exposed_numbers_in_cohort * (P_paid_new - P_paid_usual)); truncate at year end']
}
assert result['family_net_additions']['target'] - result['family_net_additions']['no_change'] == result['family_net_additions']['increment_over_no_change']
assert result['activity']['growth_due_to_connections_at_unchanged_share'] + result['activity']['remaining_active_groups_due_to_share_change'] == t[names[1]] - n[names[1]]
print(json.dumps(result, ensure_ascii=False, indent=2))
