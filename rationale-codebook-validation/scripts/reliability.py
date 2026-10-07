"""Compare unchanged original and independently coded yes/unclear decisions."""
import csv,json,math,pathlib,collections,random
ROOT=pathlib.Path(__file__).resolve().parents[1]

def agreement(counts):
 yy,yu,uy,uu=counts;n=sum(counts)
 if not n:return dict(n=0,yy=yy,yu=yu,uy=uy,uu=uu,agreement=None,expected=None,kappa=None,positive_agreement=None)
 po=(yy+uu)/n;pe=((yy+yu)*(yy+uy)+(uy+uu)*(yu+uu))/(n*n)
 return dict(n=n,yy=yy,yu=yu,uy=uy,uu=uu,A_yes=yy+yu,B_yes=yy+uy,agreement=po,expected=pe,kappa=(po-pe)/(1-pe) if pe<1 else None,positive_agreement=2*yy/(2*yy+yu+uy) if 2*yy+yu+uy else None)

def counts(pairs):
 out=[0]*4
 for a,b in pairs:out[{(True,True):0,(True,False):1,(False,True):2,(False,False):3}[(bool(a),bool(b))]]+=1
 return out

def main():
 a={x['case']:x for x in json.loads((ROOT/'coding/coder_A.json').read_text())}
 b={x['case']:x for x in json.loads((ROOT/'coding/coder_B.json').read_text())}
 raw=json.loads((ROOT/'data/rationale_cases.json').read_text());cases={c['id']:c for c in raw['cases']}
 codes=[c['code'] for c in json.loads((ROOT/'protocol/codebook_definitions.json').read_text())]
 assert set(a)==set(b)==set(cases) and len(a)==259,'All259 independently coded cases required'
 lookup={f"{r['tab']}!{cell}":(r[f],f,r['model']) for r in raw['records'] for f,cell in r['cells'].items()}
 quote_checks=0
 for cid,row in b.items():
  assert len(row['codes'])==len(set(row['codes'])) and set(row['codes'])<=set(codes)
  supported=set()
  for e in row['evidence']:
   text,field,model=lookup[e['source']]
   assert e['field']==field and e['model']==model and e['quote'] in text and len(e['quote'].split())<=40,(cid,e)
   assert any(r['tab']+'!'+r['cells'][field]==e['source'] for r in cases[cid]['rows']),(cid,'wrong case')
   assert e['code'] in row['codes'];supported.add(e['code']);quote_checks+=1
  assert supported==set(row['codes']),(cid,'missing evidence',set(row['codes'])-supported)
 def calc(ids,cs):return agreement(counts((code in a[cid]['codes'],code in b[cid]['codes']) for cid in ids for code in cs))
 ids=list(a);paired=[cid for cid in ids if a[cid]['comparison']=='Paired'];mechanisms=[f'M{i:02}' for i in range(1,16)]
 scopes=[('Primary: M01–M15, paired cases',paired,mechanisms),('M01–M15, all cases',ids,mechanisms),('All21 codes, all cases',ids,codes),('All codes except A01 and U',ids,[c for c in codes if c not in ['A01','U']])]
 summary=[]
 for name,subset,cs in scopes:summary.append({'scope':name,'cases':len(subset),'codes':len(cs),**calc(subset,cs)})
 # Segment cluster bootstrap for the primary descriptive summary.
 segments=sorted(set(cases[cid]['segment'] for cid in paired));byseg={s:calc([c for c in paired if cases[c]['segment']==s],mechanisms) for s in segments}
 rng=random.Random(20261006);boot=[]
 for _ in range(2000):
  cc=[0]*4
  for seg in rng.choices(segments,k=len(segments)):
   for j,k in enumerate(['yy','yu','uy','uu']):cc[j]+=byseg[seg][k]
  k=agreement(cc)['kappa']
  if k is not None:boot.append(k)
 boot.sort();summary[0]['kappa_cluster_bootstrap_95']=[boot[int(.025*(len(boot)-1))],boot[int(.975*(len(boot)-1))]]
 percode=[{'code':c,**calc(ids,[c])} for c in codes]
 bycategory=[{'category':tab,**calc([cid for cid in ids if cases[cid]['tab']==tab],mechanisms)} for tab in dict.fromkeys(c['tab'] for c in cases.values())]
 ae=json.loads((ROOT/'coding/coder_A_evidence.json').read_text())
 arefs={(cid,code):'; '.join(dict.fromkeys(e['source'] for e in ae if e['case']==cid and code in e['codes'])) for cid in ids for code in codes}
 mismatches=[];matrix=[]
 for cid in ids:
  for code in codes:
   av='yes' if code in a[cid]['codes'] else 'unclear';bv='yes' if code in b[cid]['codes'] else 'unclear'
   row={'case':cid,'category':cases[cid]['tab'],'segment':cases[cid]['segment'],'code':code,'coder_A':av,'coder_B':bv}
   matrix.append(row)
   if av!=bv:mismatches.append({**row,'A_memo':a[cid]['note'],'A_evidence':arefs[(cid,code)],'B_memo':b[cid]['memo'],'B_evidence':'; '.join(e['source'] for e in b[cid]['evidence'] if e['code']==code)})
 result={'summary':summary,'per_code':percode,'by_category_M01_M15':bycategory,'exact_set_agreement_all_codes':sum(set(a[c]['codes'])==set(b[c]['codes']) for c in ids)/len(ids),'exact_set_agreement_M01_M15':sum(set(a[c]['codes'])&set(mechanisms)==set(b[c]['codes'])&set(mechanisms) for c in ids)/len(ids),'quote_checks_B':quote_checks,'mismatch_count':len(mismatches),'bootstrap_segments':len(segments),'bootstrap_replicates':2000}
 (ROOT/'reports/reliability.json').write_text(json.dumps(result,indent=2))
 for name,rows in [('per_code',percode),('by_category',bycategory),('decision_matrix',matrix),('disagreements',mismatches)]:
  with (ROOT/'reports'/f'{name}.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 def pct(x):return f'{100*x:.1f}%' if x is not None else 'undefined'
 def val(x):return f'{x:.3f}' if x is not None else 'undefined'
 report='# Independent-agent reliability\n\nOriginal coder A compared with fresh agent B; no adjudication or changes to A. Ratings are documented yes versus unclear, not present versus absent.\n\n| Scope | Cases × codes | Agreement | Cohen κ | Positive agreement |\n|---|---:|---:|---:|---:|\n'
 for r in summary:report+=f"| {r['scope']} | {r['cases']} × {r['codes']} | {pct(r['agreement'])} | {val(r['kappa'])} | {pct(r['positive_agreement'])} |\n"
 lo,hi=summary[0]['kappa_cluster_bootstrap_95'];report+=f'\nPrimary descriptive 95% segment-bootstrap interval for κ: {lo:.3f}–{hi:.3f}; 2,000 resamples of {len(segments)} parent segments. This does not make these cases independent interviews.\n'
 report+='\n## Per-code agreement\n\n| Code | Mechanism / pattern | A yes | B yes | Both yes | A only | B only | Both unclear | Agreement | κ | Positive agreement |\n|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|\n'
 names={c['code']:c['name'] for c in json.loads((ROOT/'protocol/codebook_definitions.json').read_text())}
 for r in percode:report+=f"| {r['code']} | {names[r['code']]} | {r['A_yes']} | {r['B_yes']} | {r['yy']} | {r['yu']} | {r['uy']} | {r['uu']} | {pct(r['agreement'])} | {val(r['kappa'])} | {pct(r['positive_agreement'])} |\n"
 report+='\n## Category comparison, M01–M15\n\n| Category | Decisions | Agreement | κ |\n|---|---:|---:|---:|\n'
 for r in bycategory:report+=f"| {r['category']} | {r['n']} | {pct(r['agreement'])} | {val(r['kappa'])} |\n"
 report+=f"\nWhole-case exact code-set agreement: {pct(result['exact_set_agreement_all_codes'])} for all21 codes; {pct(result['exact_set_agreement_M01_M15'])} for M01–M15. The complete mismatch file contains {len(mismatches)} case-code disagreements. All {quote_checks} B evidence excerpts passed exact source-substring and locator checks.\n"
 report+='''\n## Review priorities

The lowest reproducibility among the main interpretive codes occurs for **M08 (different claim/aspect emphasized, κ=0.293)**, **M12 (time/actuality boundary, κ=0.404)**, and **M13 (word/referent substitution, κ=0.458)**. The coverage-scope code **C02 (κ=0.347)** also needs boundary clarification. B records substantially more positives for each, which warrants reviewing the threshold rather than assuming either coder is right. These are priorities for adjudication after initial human ratings are saved.

M10 and M16 have perfect observed agreement but only three and one shared positive cases respectively; this is weak evidence of general reproducibility. A01's very low κ=0.026 reflects the original illustrative versus fresh systematic use and should not be interpreted as a model disagreement rate. The frozen original decisions remain untouched.

## Interpretation and limitations

A01 was illustrative in the original pass, whereas B applies the definition systematically; its discrepancy is partly procedural, so it is separate from the primary mechanism summary. U is determined by missing comparator data and M16 is a technical-message flag. Easy agreement on those flags should not stand in for interpretive reproducibility. High percent agreement can reflect many jointly unclear decisions; positive agreement and per-code κ expose this.

The original pass was iterative and focused on salient observations; B is a fresh systematic pass. This is a reproducibility audit of that existing analysis, not a preplanned blind two-coder study. A separate agent is not a separate model family or a human. Definitions and cases were shared; original coded examples and decisions were withheld. A comparison-unit clarification was sent after the first batch. No coded case answers were supplied.

Cohen κ uses observed and marginal expected agreement, following [scikit-learn’s official definition](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.cohen_kappa_score.html). Blank human responses must be treated as missing, never converted into unclear. Human validation is prepared but has not occurred.
'''
 (ROOT/'reports/Agreement_report.md').write_text(report)
 print(json.dumps(summary,indent=2));print('B quote checks:',quote_checks)
if __name__=='__main__':main()
