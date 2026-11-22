import csv,json,sys,hashlib,platform
from pathlib import Path
from fractions import Fraction as F
p=Path(sys.argv[1]); raw=p.read_bytes(); rows=list(csv.DictReader(raw.decode('utf-8-sig').splitlines()))
assert len(rows)==6
mature=[];excluded=[]
for line,r in enumerate(rows,2):
    n=int(r['eligible_users']); assert n>0
    if r['is_mature']!='true' or int(r['days_observed'])<30 or r['returned_d30']=='' or r['reported_retention_percent']=='':
        excluded.append({'csv_line':line,'month':r['cohort_month'],'segment':r['acquisition_segment'],'eligible_users':n,'reason':'immature and outcomes missing; missing is not zero','ratio_percent':None});continue
    k=int(r['returned_d30']); rate=F(k,n); reported=F(r['reported_retention_percent'])
    assert 0<=k<=n and rate*100==reported
    mature.append(dict(line=line,month=r['cohort_month'],segment=r['acquisition_segment'],n=n,k=k,rate=rate,reported=reported))
months=sorted(set(r['month'] for r in mature)); assert months==['2026-01','2026-02']
out={'source_path':p.as_posix(),'source_sha256':hashlib.sha256(raw).hexdigest(),'runtime':platform.python_version(),'interpretation':'Ratios of supplied counts only; authoritative D30 contract UNKNOWN','monthly':{},'segments':{},'excluded':excluded}
for month in months:
    rr=[r for r in mature if r['month']==month];n=sum(r['n'] for r in rr);k=sum(r['k'] for r in rr)
    out['monthly'][month]={'csv_lines':[r['line'] for r in rr],'eligible_users':n,'returned_d30':k,'pooled_count_ratio_percent':float(F(k,n)*100),'unweighted_mean_reported_percent':float(sum(r['reported'] for r in rr)/len(rr)),'paid_share_percent':float(F(next(r['n'] for r in rr if r['segment']=='paid'),n)*100)}
for seg in ['paid','organic']:
    rr=[next(r for r in mature if r['month']==m and r['segment']==seg) for m in months]
    out['segments'][seg]={'csv_lines':[r['line'] for r in rr],'count_ratio_percent':[float(r['rate']*100) for r in rr],'delta_percentage_points':float((rr[1]['rate']-rr[0]['rate'])*100)}
jan=[r for r in mature if r['month']==months[0]];feb=[r for r in mature if r['month']==months[1]]
jan_rate=F(sum(r['k'] for r in jan),sum(r['n'] for r in jan));feb_rate=F(sum(r['k'] for r in feb),sum(r['n'] for r in feb))
fixed=sum(F(j['n'],sum(r['n'] for r in jan))*next(f['rate'] for f in feb if f['segment']==j['segment']) for j in jan)
out['descriptive_january_reference_decomposition']={'jan_weights_feb_rates_percent':float(fixed*100),'within_segment_term_pp':float((fixed-jan_rate)*100),'mix_term_at_feb_rates_pp':float((feb_rate-fixed)*100),'total_delta_pp':float((feb_rate-jan_rate)*100),'identity_holds':(fixed-jan_rate)+(feb_rate-fixed)==feb_rate-jan_rate,'limitations':'Sequential January-reference arithmetic identity, not causal attribution; order-dependent'}
out['formulas']={'ratio':'100 * sum(returned_d30) / sum(eligible_users)','reported_mean':'sum(reported_retention_percent)/number_of_rows, shown only to expose weighting difference','fixed_mix':'sum(Jan segment eligible / Jan all eligible * Feb segment returned / Feb segment eligible) * 100','within':'fixed_mix_percent - Jan pooled_percent','mix':'Feb pooled_percent - fixed_mix_percent'}
out['rules']={'rounding':'Exact Fraction arithmetic, float display for terminating values; units percent and percentage points','missing':'Never impute blank outcomes to zero; March has no calculated ratio','maturity':'Use only rows explicitly true AND days_observed>=30 AND supplied complete outcomes; this checks supplied flags, not validity of metric contract','duplicate_check':'Each month/segment key must be unique'}
assert len({(r['cohort_month'],r['acquisition_segment']) for r in rows})==len(rows)
print(json.dumps(out,ensure_ascii=False,indent=2))
