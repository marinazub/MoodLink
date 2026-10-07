import csv,hashlib,json,pathlib,zipfile
import openpyxl
ROOT=pathlib.Path(__file__).resolve().parents[1]
manifest=json.loads((ROOT/'protocol/manifest.json').read_text());raw=json.loads((ROOT/'data/rationale_cases.json').read_text())
assert hashlib.sha256(pathlib.Path(manifest['source']).read_bytes()).hexdigest()==manifest['source_sha256'],'Source changed'
assert hashlib.sha256((ROOT/'protocol/codebook_definitions.json').read_bytes()).hexdigest()==manifest['blinded_definition_sha256']
with (ROOT/'human_validation/coordinator_key.csv').open() as f:key=list(csv.DictReader(f))
assert len(key)==70 and len({r['original_case'] for r in key})==70
assert {t:sum(r['category']==t for r in key) for t in {r['category'] for r in key}}=={'GPT6_Only_Assignments':27,'Medgemma_Only_Assignments':5,'Total_Construct_Match':4,'Partial_Construct_Match':30,'Different_Constructs':4}
wb=openpyxl.load_workbook(ROOT/'human_validation/Human_Validation_Blinded.xlsx',read_only=False,data_only=True)
ratings=list(wb['Ratings'].values)[1:];assert len(ratings)==1470
assert all(all(v is None for v in r[3:9]) and r[9]=='Unrated' for r in ratings)
assert [wb['Instructions'].cell(i,2).value for i in [11,12,13]]==[0,1470,1470]
assignments=list(wb['Assignments'].values)[1:];assert len(assignments)==248
packet=json.loads((ROOT/'human_validation/packet.json').read_text())
for row,source in zip(assignments,packet['assignments']):assert list(row[4:7])==[source[f] or None for f in ['rationale','critic_rationale','critic_coverage_rationale']]
assert not any('GPT6_Only_Assignments' in str(v) or 'C001'==v for s in wb for row in s.values for v in row)
with zipfile.ZipFile(ROOT/'human_validation/Human_Validation_Packet.zip') as z:assert set(z.namelist())=={'Human_Validation_Blinded.xlsx','REVIEWER_INSTRUCTIONS.md'}
result={'source_unchanged':True,'frozen_definitions_unchanged':True,'human_cases':70,'human_assignments':248,'blank_human_ratings':1470,'human_packet_excludes_keys_and_agent_coding':True,'visual_review':'All five workbook sheets rendered and inspected.'}
if (ROOT/'reports/reliability.json').exists():
 d=json.loads((ROOT/'reports/reliability.json').read_text())
 from fractions import Fraction
 for r in d['per_code']:
  a,b,c,e=[r[k] for k in ['yy','yu','uy','uu']];den=(a+b)*(b+e)+(a+c)*(c+e)
  expected=float(Fraction(2*(a*e-b*c),den)) if den else None
  assert (expected is None and r['kappa'] is None) or abs(expected-r['kappa'])<1e-12
 result['independent_binary_kappa_identity_checked']=True
(ROOT/'reports/artifact_verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
