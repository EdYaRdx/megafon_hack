"""Recompute documentary bounds from pinned source bytes; never forecasts."""
import hashlib
import json
import math
import platform
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXPECTED = {
    'inputs/brief.pdf': '558d2c665caa4f4954135c8bbfb69d791e398dcdc5b625d5ded7bdb2d0eb0fa5',
    'sources/S-001-ocr/page-03.txt': '95c7e7fc2f2b4dc969f9ab052566d1a2fd3b5701f2ee9a72d12da1b0c727d667',
    'sources/S-001-ocr/page-09.txt': 'f18782ad9f6a5753a9f6f34ed497b0980a9ac8e7a2fdb1171997668ba5aec018',
    'calculations/results.json': 'af4cacd115a24fe34c1099d1a20e2de6ff4414fe41384aa3afa7f5a9675bdda2',
}
inputs = []
for name, expected in EXPECTED.items():
    digest = hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
    if digest != expected:
        raise ValueError(f'Input hash mismatch: {name}')
    inputs.append(dict(path=name, sha256=digest))
p3 = (ROOT / 'sources/S-001-ocr/page-03.txt').read_text(encoding='utf-8')
p9 = (ROOT / 'sources/S-001-ocr/page-09.txt').read_text(encoding='utf-8')
def numeric_block(text):
    values = []
    for line in text.splitlines():
        if not re.fullmatch(r'[\d %]+', line.strip()):
            break
        values.append(int(re.sub(r'\D', '', line)))
    return values
values = numeric_block(p3.split('\nизменений\n', 1)[1])
if len(values) != 10:
    raise ValueError('Unexpected table extraction')
baseline, target = values[:5], values[5:]
rate = int(re.search(r'ставка\s*[—–-]\s*(\d+) руб', p9).group(1))
old = json.loads((ROOT / 'calculations/results.json').read_text(encoding='utf-8'))
gap = (target[0] - baseline[0]) * 1_000_000
months = math.ceil(gap / rate)
if (gap, months, rate) != (old['gross_profit_gap_rub'], old['additional_paid_number_months_zero_new_direct_costs_and_other_contribution'], old['profit_rate_rub_per_additional_paid_number_month']):
    raise ValueError('Prior results differ from source recomputation')
scenarios = []
for quarter in (2, 3, 4):
    first_month = 3 * (quarter - 1) + 1
    horizon = 12 - first_month + 1
    scenarios.append(dict(
        assumed_start=f'01-{first_month:02d} of the fictional plan year',
        full_calendar_month_ceiling_per_number=horizon,
        necessary_distinct_numbers_at_unattainably_generous_full_incremental_months_each=math.ceil(months / horizon),
        formula='ceil(M_required / H); H = 12 - start_month + 1',
        assumptions='C=O=0; all numbers available on first day; every remaining month incremental vs control; no rollout, churn, delay or missing months',
        interpretation='outer necessary bound only, not sample size, target reach, realistic retention or sufficient condition',
    ))
result = dict(
    kind='documentary arithmetic and conditional feasibility bounds; NO empirical effect estimate',
    runtime=platform.python_version(), inputs=inputs,
    source_locators={'baseline_target': 'S-001 inputs/brief.pdf p3 table; saved image page-03.png visually rechecked', 'rate_and_rules': 'S-001 inputs/brief.pdf p9 How to calculate profit and payback; saved image page-09.png visually rechecked'},
    baseline_gp_rub=baseline[0] * 1_000_000, target_gp_rub=target[0] * 1_000_000,
    gap_rub=gap, rate_rub_per_additional_paid_number_month=rate,
    required_additional_paid_number_months_if_C_O_zero=months,
    formula='GP=279000000+500*M+O-C; target iff 500*M+O-C>=6000000; M and net O may be negative; C>=0; I separate',
    sensitivity='holding O fixed, each extra ruble C adds 1/500 required number-month; higher C worsens the bound; O must be net and evidenced, not assumed',
    timing_scenarios=scenarios,
    general_feasibility='M_upper=sum_i H_i for distinct eligible numbers; if 500*M_upper+O_upper-C_lower<6000000, annual goal impossible within that scope even at the optimistic envelope; passing is not evidence of likelihood',
    real_inputs={key:'UNKNOWN' for key in ['eligible_distinct_numbers','rollout_by_month','incremental_paid_share_by_month','C','O','I','baseline_paid_share','cluster_sample_size','recruitment_flow','critical_path','payback_date','effect_probability']},
    rounding='exact integer differences; necessary distinct-number bounds rounded upward; no rounding of invented effects',
    missing_error_rules='hash/extraction mismatch => fail; no imputation; families are not converted to numbers; no zero defaults for unknown C/O/M',
    denominator='one distinct eligible phone number per paid month; all originally included numbers retained in monthly cohort denominators, including group exits; no repeated-event duplication',
    verification='recomputed from pinned OCR, compared to prior saved results; critical table and rate visually checked against pinned page images; no field research run',
)
print(json.dumps(result, ensure_ascii=False, indent=2))
