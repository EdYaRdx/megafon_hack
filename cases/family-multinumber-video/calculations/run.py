"""Read pinned machine OCR, validate against the visually reviewed PDF, calculate bounds."""
import hashlib
import json
import platform
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PDF_SHA = '558d2c665caa4f4954135c8bbfb69d791e398dcdc5b625d5ded7bdb2d0eb0fa5'
pdf = ROOT / 'inputs/brief.pdf'
assert hashlib.sha256(pdf.read_bytes()).hexdigest() == PDF_SHA
p3path = ROOT / 'sources/S-001-ocr/page-03.txt'
p9path = ROOT / 'sources/S-001-ocr/page-09.txt'
p3 = p3path.read_text(encoding='utf-8')
p9 = p9path.read_text(encoding='utf-8')

def numeric_lines(text):
    result = []
    for line in text.splitlines():
        if not re.fullmatch(r'[\d %]+', line.strip()):
            break
        result.append(int(re.sub(r'\D', '', line)))
    return result

baseline_and_target = numeric_lines(p3.split('\nизменений\n', 1)[1])
assert len(baseline_and_target) == 10, baseline_and_target
baseline, target = baseline_and_target[:5], baseline_and_target[5:]
estimate = numeric_lines(p3.split('\nОценка\n', 1)[1])
assert len(estimate) == 5, estimate
# Assertions are extraction QA against page-03.png, not substitutes for source inputs.
assert baseline == [279, 5000, 8000, 1000, 45]
assert target == [285, 8000, 12000, 2000, 60]
assert estimate == [275, 4000, 6500, 800, 42]
market_match = re.search(r'доступны\s+(\d+) тыс\. домохозяйств и (\d+) тыс\. владельцев', p3)
family_base, owner_base = (int(x) * 1000 for x in market_match.groups())
rate = int(re.search(r'ставка\s*[—–-]\s*(\d+) руб', p9).group(1))
gap_rub = (target[0] - baseline[0]) * 1_000_000
result = {
    'kind': 'conditional bounds; NOT demand/effect forecasts',
    'python': platform.python_version(),
    'pdf_sha256': PDF_SHA,
    'inputs': [{'path': str(p.relative_to(ROOT)), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in (pdf, p3path, p9path)],
    'source_locators': {'baseline_target_estimate': 'S-001 PDF p3 table, OCR page-03; visually checked', 'rate': 'S-001 PDF p9 retention paragraph'},
    'baseline': dict(zip(['gross_profit_mrub','active_families','connected_families','connected_owners','activation14_pct'],baseline)),
    'target': dict(zip(['gross_profit_mrub','active_families','connected_families','connected_owners','activation14_pct'],target)),
    'gross_profit_gap_rub': gap_rub,
    'additional_paid_number_months_zero_new_direct_costs_and_other_contribution': gap_rub // rate,
    'profit_rate_rub_per_additional_paid_number_month': rate,
    'family_additional_vs_baseline': target[2] - baseline[2],
    'family_net_additions_vs_start': target[2] - estimate[2],
    'owner_additional_vs_baseline': target[3] - baseline[3],
    'owner_net_additions_vs_start': target[3] - estimate[3],
    'active_additional_vs_baseline': target[1] - baseline[1],
    'baseline_active_share': baseline[1] / baseline[2],
    'target_active_share': target[1] / target[2],
    'target14_vs_baseline_pp': target[4] - baseline[4],
    'family_target_share_of_available_base': target[2] / family_base,
    'owner_target_share_of_available_base': target[3] / owner_base,
    'family_active_at_target_connections_if_share_unchanged': target[2] * baseline[1] / baseline[2],
    'active_gap_remaining_if_share_unchanged': target[1] - target[2] * baseline[1] / baseline[2],
    'month_ceiling_if_entitled_start_Q2_per_number': 9,
    'month_ceiling_if_entitled_start_Q3_per_number': 6,
    'month_ceiling_if_entitled_start_Q4_per_number': 3,
    'formula': 'GP=279000000+500*M+O-C; M_required=max(0,(6000000+C-O)/500); investment I separate; payback when cumulative(500*M_q+O_q-C_q)>=I_cumulative',
    'missing_rules': 'missing, mismatched OCR or hash => stop; no imputation; no people-to-number conversion',
    'rounding': 'exact integer differences; shares full precision, display to 2 decimals; actual count requirement ceil when noninteger',
}
output = ROOT / 'calculations/results.json'
output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(result, ensure_ascii=False, indent=2))
