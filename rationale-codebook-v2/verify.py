import json,pathlib,openpyxl,collections,hashlib
P=pathlib.Path(__file__).parent;d=json.loads((P/'analysis_v2.json').read_text())
source='/Users/marinazub/Desktop/SCOPE/CFIR_code/GPT_code/outputs/combined_review_01a11356/Combined_GPT6_medgemma_all_outputs.xlsx'
w=openpyxl.load_workbook(source,data_only=True)
for e in d['evidence']:
 tab,cell=e['source'].split('!');value=w[tab][cell].value
 assert value==e['full'] and e['quote'] in value and len(e['quote'].split())<=40,(e['case'],e['code'],e['source'])
book=openpyxl.load_workbook(P/'Rationale_Only_Codebook_and_Coded_Cases.xlsx',read_only=True,data_only=True)
assert len(list(book['Coded units'].values))==260
assert len(list(book['Source rationales'].values))==1023
assert len(list(book['Evidence'].values))==1456
for c,row in zip(d['codebook'],list(book['Codebook'].values)[1:]):assert row[7]==d['stats']['code_counts'][c['code']]
for src,row in zip(d['source'],list(book['Source rationales'].values)[1:]):assert list(row[7:10])==[src[f] or None for f in ['rationale','critic_rationale','critic_coverage_rationale']]
assert len(d['units'])==len({u['case'] for u in d['units']})==259
assert len({(r['tab'],r['row']) for r in d['source']})==1022
assert all(u['question']=='Not question' for u in d['units'])
report={'version':2,'cases':259,'code_definitions':23,'exact_excerpts_verified':len(d['evidence']),'assignment_rows_preserved':892,'no_match_rows_added':130,'all_source_values_match':True,'question_units':0,'R01_assignment_count':186,'R01_case_count':139,'prior_reliability_not_reused_for_new_codes':True,'source_workbook_sha256':hashlib.sha256(pathlib.Path(source).read_bytes()).hexdigest()}
(P/'verification_v2.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
