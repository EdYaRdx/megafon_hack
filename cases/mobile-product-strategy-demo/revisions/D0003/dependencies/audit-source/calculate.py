"""Independent arithmetic review; prints results, never changes published inputs."""
import hashlib
import json
import math
from fractions import Fraction as F
from pathlib import Path

here = Path(__file__).resolve().parent
case = here.parents[1]
pins = {
    'inputs/R0002-scenario.json': '7fe5197b2dc67425bf70ac234e690c1d51ed45886c1e5d06e65feaa811f0ae80',
    'calculations/results.json': '1b89ee79e5bb1610ab8792e67b3bec093555dd3ac73cbfedcbe1606cd0367221',
    'calculations/R0002/results.json': '99dd19cf32d85014b342f8f79060cfcdfd3bfbbc15fd1b0c5e51b79119313fc1',
    'calculations/R0002/calculate.py': '80bd387028ee8df81c8d7ddf119ca5aad8d99934beb47c2847ef0b698dd11714',
    'inputs/Пример брифа.pdf': '558d2c665caa4f4954135c8bbfb69d791e398dcdc5b625d5ded7bdb2d0eb0fa5',
}
for name, expected in pins.items():
    if hashlib.sha256((case / name).read_bytes()).hexdigest() != expected:
        raise ValueError('Pinned input changed: ' + name)
x = json.loads((case / 'inputs/R0002-scenario.json').read_bytes())
b = json.loads((case / 'calculations/results.json').read_bytes())
old = json.loads((case / 'calculations/R0002/results.json').read_bytes())
rate = F(b['profit_boundary']['rub_per_extra_paid_number_month'])
usual, target = b['table']['plan_no_change'], b['table']['plan_target']
gap = F(target['gross_profit_million_rub'] - usual['gross_profit_million_rub']) * 1000000
D, O = F(x['new_direct_cost_rub_sensitivity']), F(x['other_incremental_contribution_rub'])
required = max(F(0), (gap + D - O) / rate)
monthly = {m: 0 for m in range(1, 13)}
cohorts = []
for c in x['cohorts']:
    numbers = c['families'] * x['eligible_numbers_per_family']
    months = list(range(c['start_month'] + 1, 13))
    if not 1 <= c['start_month'] <= 12 or numbers < 0:
        raise ValueError('Invalid hypothetical cohort')
    for m in months:
        monthly[m] += numbers
    cohorts.append(dict(start_month=c['start_month'], families=c['families'], numbers=numbers,
                        counted_months=months, opportunity_number_months=numbers * len(months)))
capacity = sum(monthly.values())
if capacity <= 0 or required > capacity:
    raise ValueError('Required months exceed absolute hypothetical capacity')
weighted_gap = required / capacity
p0_limit = 1 - weighted_gap
quarter_capacity = [sum(monthly[m] for m in range(3*q+1, 3*q+4)) for q in range(4)]
uniform = [F(v) * weighted_gap for v in quarter_capacity]

def allocate(order):
    remaining = required
    values = [F(0)] * 4
    for q in order:
        values[q] = min(remaining, F(quarter_capacity[q]))
        remaining -= values[q]
    if remaining:
        raise ValueError('Witness allocation incomplete')
    return values

profiles = {}
for name, values in [('implicit_uniform_gap_in_R0002', uniform),
                     ('earliest_capacity_only_witness', allocate(range(4))),
                     ('latest_capacity_only_witness', allocate(reversed(range(4))))]:
    assert sum(values) == required
    assert all(0 <= v <= cap for v, cap in zip(values, quarter_capacity))
    profiles[name] = {'extra_paid_number_months_by_quarter': [float(v) for v in values],
                      'gross_rub_before_D_by_quarter': [float(v * rate) for v in values],
                      'annual_extra_paid_number_months': float(sum(values))}
assert capacity == old['total_opportunity_number_months']
assert required == F(str(old['required_extra_paid_number_months']))
for i, row in enumerate(old['quarterly']):
    assert math.isclose(float(uniform[i]), row['required_extra_paid_number_months'])
    assert math.isclose(float(uniform[i] * rate), row['gross_contribution_before_new_direct_cost_rub'])
rows = [dict(metric=k, source_no_change=v, source_target=target[k],
             independent_A_forecast='UNKNOWN', source_target_gap=target[k]-v,
             R0002_goal_seeking_value=next(r['conditional_target_scenario'] for r in old['five_kpi_forecast'] if r['metric']==k))
        for k, v in usual.items()]
print(json.dumps({
    'status': 'ARITHMETIC_REVIEW_NOT_CUSTOMER_OBSERVATIONS', 'pinned_inputs_sha256': pins,
    'cohorts': cohorts, 'monthly_opportunity_number_months': monthly,
    'quarter_opportunity_number_months': quarter_capacity,
    'capacity_number_months': capacity, 'required_extra_paid_number_months': float(required),
    'required_weighted_gap_fraction': str(weighted_gap),
    'required_weighted_gap_percentage_points': float(weighted_gap * 100),
    'maximum_weighted_usual_paid_probability_fraction': str(p0_limit),
    'maximum_weighted_usual_paid_probability_percent': float(p0_limit * 100),
    'capacity_constraint': 'M <= sum_ct N_c*(1-p_usual_ct) = C*(1-pbar_usual); pbar weights N_c over exactly counted cohort-month cells',
    'interpretation': 'Necessary condition only. C=88000 and D=1000000 are hypothetical. At equality p_A must reach1 in all positive-weight cells to attain M. Preventability, eligibility, timing, uptake and causal effect remain UNKNOWN. Uniform cell gap additionally requires p_usual_ct <=1-gap in every affected cell.',
    'timing_profiles_not_forecasts': profiles,
    'timing_limitations': 'Witnesses only satisfy absolute capacity and annual sum; actual baseline curves, causal/persistence constraints and D/I timing are UNKNOWN. No witness is selected as expected or practically feasible.',
    'quarterly_actual_or_expected_profit': 'UNKNOWN; requires cell-specific effect timing and O/D/I schedules, and source annual baseline has no quarterly split',
    'kpi_reclassification': rows,
    'owner_gap': target['connected_owners_eoy'] - usual['connected_owners_eoy'],
    'year3_path': 'UNKNOWN; C_y=C_(y-1)+new_y-exits_y; active_y=C_y*active_share_y. No identified new/exits/share/cost path supports doubling.',
    'formulas': ['M_required=max(0,(target_GP-usual_GP+D-O)/rate)', 'C=sum(families*eligible_numbers*(12-start_month))',
                 'pbar_usual=sum(N_c*p_usual_ct)/C', 'pbar_usual<=1-M_required/C',
                 'M_q=sum_(ct in q) N_c*(p_A_ct-p_usual_ct)', 'delta_GP_q=rate*M_q+O_q-D_q; compare cumulative delta_GP with cumulative I'],
    'units': 'RUB; additional paid NUMBER-months; probability, percent and percentage points separately; KPI counts unique families/owners',
    'rounding': 'Exact Fraction internally; display percent to2decimals; 84.09 is rounded, strict comparison uses37/44',
    'missing_error_rules': 'Fail on pinned hash mismatch, invalid capacity, inconsistent reconstruction. Never replace unknown payment curves, effort, rates, harm thresholds or effect with numeric defaults.'
}, ensure_ascii=False, indent=2))
