"""Score saved, unadjudicated human responses; blanks remain missing."""
import argparse,csv,json,pathlib,sys
from reliability import agreement
ROOT=pathlib.Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('responses',type=pathlib.Path);p.add_argument('--output',type=pathlib.Path,required=True);args=p.parse_args()
if args.responses.suffix.lower()=='.xlsx':
 import openpyxl
 w=openpyxl.load_workbook(args.responses,data_only=True,read_only=True);rows=list(w['Ratings'].values)
 responses=[dict(human_case=r[0],code=r[1],rating=r[3],evidence_assignment_ids=r[4],evidence_field=r[5],exact_quote=r[6],memo=r[7],reviewer=r[8]) for r in rows[1:]]
else:
 with args.responses.open() as f:responses=list(csv.DictReader(f))
with (ROOT/'human_validation/coordinator_key.csv').open() as f:key={r['human_case']:r for r in csv.DictReader(f)}
codes={c['code'] for c in json.loads((ROOT/'protocol/codebook_definitions.json').read_text())}
seen=set();valid=[]
for r in responses:
 pair=(r['human_case'],r['code']);assert pair not in seen,'Duplicate human case-code';seen.add(pair)
 assert pair[0] in key and pair[1] in codes,'Unknown human case/code'
 rating=(r.get('rating') or '').strip().lower()
 if not rating:continue
 assert rating in ['yes','unclear'],f'Invalid rating {pair}'
 assert r.get('reviewer'),f'Reviewer required {pair}'
 if rating=='yes':assert all(r.get(k) for k in ['evidence_assignment_ids','evidence_field','exact_quote']),f'Evidence required {pair}'
 valid.append((r['human_case'],r['code'],rating))
assert valid,'No completed ratings; blanks cannot be scored as unclear'
result={'completed':len(valid),'expected':1470,'missing':1470-len(valid),'comparisons':[],'note':'Human evidence presence checked; verbatim fidelity and interpretation require coordinator review. Weighted results use original category sampling weights. Partial responses can be biased.'}
for coder in ['A','B']:
 agent={r['case']:set(r['codes']) for r in json.loads((ROOT/f'coding/coder_{coder}.json').read_text())}
 for scope,cs in [('M01–M15',{f'M{i:02}' for i in range(1,16)}),('All21',codes)]:
  cc=[0]*4;weighted=[0.0]*4
  for hid,code,rating in valid:
   if code not in cs:continue
   a=code in agent[key[hid]['original_case']];b=rating=='yes';j={(True,True):0,(True,False):1,(False,True):2,(False,False):3}[(a,b)]
   cc[j]+=1;weighted[j]+=float(key[hid]['design_weight'])
  result['comparisons'].append({'agent':coder,'scope':scope,'unweighted':agreement(cc),'design_weighted':agreement(weighted)})
args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
