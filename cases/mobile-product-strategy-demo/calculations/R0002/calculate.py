import hashlib
import json
from fractions import Fraction as F
from pathlib import Path

case=Path(__file__).resolve().parents[2]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
inputs=case/'inputs/R0002-scenario.json'
x=json.loads(inputs.read_text(encoding='utf-8'))
baseline=case/x['base_calculation_path']
if sha(baseline)!=x['base_calculation_sha256'] or sha(case/'inputs/Пример брифа.pdf')!=x['pdf_sha256']:
    raise ValueError('Pinned baseline/PDF mismatch')
b=json.loads(baseline.read_text(encoding='utf-8'))
usual=b['table']['plan_no_change']; targets=b['table']['plan_target']
rate=F(b['profit_boundary']['rub_per_extra_paid_number_month'])
D=F(x['new_direct_cost_rub_sensitivity']); O=F(x['other_incremental_contribution_rub'])
gap=F(targets['gross_profit_million_rub']-usual['gross_profit_million_rub'])*1000000
M=(gap+D-O)/rate
monthly={m:0 for m in range(1,13)}
cohorts=[]
for c in x['cohorts']:
    if not 1<=c['start_month']<=12 or c['families']<0: raise ValueError('Invalid cohort')
    numbers=c['families']*x['eligible_numbers_per_family']
    # First month excluded; later number-months are opportunity capacity, not paid months.
    months=list(range(c['start_month']+1,13))
    for m in months: monthly[m]+=numbers
    cohorts.append({**c,'eligible_numbers_assumed':numbers,'credited_months':months,'opportunity_number_months':numbers*len(months)})
capacity=sum(monthly.values())
if capacity<=0: raise ValueError('No within-year opportunity')
delta=M/capacity
if not 0<=delta<=1: raise ValueError('Goal exceeds absolute opportunity capacity')
stress=F(x['stress_increment_multiplier'])
rows=[]
for metric,value in usual.items():
    selected=targets[metric] if metric!='connected_owners_eoy' else value
    selected=F(selected)
    downside=F(value)+stress*(selected-F(value))
    if metric=='gross_profit_million_rub':
        downside=(F(value)*1000000+rate*M*stress+O-D)/1000000
    rows.append({'metric':metric,'no_change':value,'target':targets[metric],
                 'conditional_target_scenario':float(selected),'difference_from_no_change':float(selected-value),
                 'target_shortfall_conditional':float(F(targets[metric])-selected),
                 'stress_scenario':float(downside),'stress_difference_from_no_change':float(downside-value)})
quarter=[]; cumulative_M=F(0)
for q in range(1,5):
    opp=sum(monthly[m] for m in range((q-1)*3+1,q*3+1))
    paid=F(opp)*delta; cumulative_M+=paid
    quarter.append({'quarter':q,'opportunity_number_months':opp,'required_extra_paid_number_months':float(paid),
                    'gross_contribution_before_new_direct_cost_rub':float(paid*rate),
                    'cumulative_contribution_before_new_direct_cost_rub':float(cumulative_M*rate),
                    'cumulative_net_formula':f'{float(cumulative_M*rate)} - cumulative_D_RUB',
                    'development_payback_condition':'cumulative_I_RUB <= cumulative_contribution - cumulative_D_RUB; D/I schedule UNKNOWN'})
assert sum(c['families'] for c in cohorts)==targets['connected_groups_eoy']
assert sum(c['opportunity_number_months'] for c in cohorts)==capacity
assert sum(F(monthly[m])*delta for m in monthly)==M
print(json.dumps({
 'status':'ARITHMETIC_VERIFIED_NOT_EMPIRICAL_FORECAST',
 'input_path':str(inputs.relative_to(case)),'input_sha256':sha(inputs),
 'baseline_path':x['base_calculation_path'],'baseline_sha256':sha(baseline),'pdf_sha256':x['pdf_sha256'],
 'cohorts':cohorts,'monthly_opportunities':monthly,'total_opportunity_number_months':capacity,
 'required_extra_paid_number_months':float(M),'required_weighted_average_probability_gap':float(delta),
 'required_weighted_average_gap_percentage_points':float(delta*100),
 'probability_gap_interpretation':'Weighted average over later within-year number-months. Not an assumed constant probability, estimated effect or observed curve. Feasibility also requires sum(N*(1-Ppaid_usual)) >= M; usual curve UNKNOWN.',
 'annual_new_direct_cost_rub_sensitivity':int(D),'annual_other_contribution_rub':int(O),
 'annual_gross_contribution_before_new_cost_rub':float(rate*M),
 'annual_net_incremental_gp_rub':float(rate*M+O-D),
 'gp_rub_conditional':float(F(usual['gross_profit_million_rub'])*1000000+rate*M+O-D),
 'stress_extra_paid_months':float(M*stress),'stress_gp_rub':float(F(usual['gross_profit_million_rub'])*1000000+rate*M*stress+O-D),
 'no_effect_gp_rub_if_cost_incurred':float(F(usual['gross_profit_million_rub'])*1000000+O-D),
 'annual_development_investment_ceiling_rub_conditional':float(rate*M+O-D),
 'quarterly':quarter,'five_kpi_forecast':rows,
 'third_year_proposal':{'connected_families':targets['connected_groups_eoy']*x['year3_target_multiplier'],
                      'active_families':targets['active_groups_last_month']*x['year3_target_multiplier'],
                      'available_households_if_unchanged':b['available_market']['households'],
                      'penetration_percent':100*targets['connected_groups_eoy']*x['year3_target_multiplier']/b['available_market']['households'],
                      'status':'PROPOSED_UNAPPROVED_ORIENTIR_NOT_FORECAST'},
 'formulas':['GP_RUB=279000000+500*M+O-D','M_required=(6000000+D-O)/500',
             'opportunity=sum(cohort_families*2*(12-start_month)); no credit in entry month',
             'required_weighted_gap=M_required/opportunity','stress: family increments and M multiplied by 1/2; D fixed',
             'activation=first useful action within14days after group creation among all Q4-created groups, including unaccepted invites',
             'active_share=active_last_month/connected_at_year_end'],
 'units':'RUB; unique families/owners; additional paid NUMBER-months; percent/percentage points separately',
 'rounding':'Exact Fraction arithmetic internally, JSON decimal outputs; reports round gap to2decimals; no statistical uncertainty implied',
 'missing_and_error_rules':'Actual effect/cost/eligibility/curves remain UNKNOWN; fail on hash mismatch, invalid month, invalid capacity or inconsistent arithmetic; no invented statistical thresholds',
 'assumption_ids':[a['id'] for a in x['assumptions']]
},ensure_ascii=False,indent=2))
