import csv,json,random,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
d=json.loads((ROOT/'data/rationale_cases.json').read_text());cb=json.loads((ROOT/'protocol/codebook_definitions.json').read_text())
quota={'GPT6_Only_Assignments':27,'Medgemma_Only_Assignments':5,'Total_Construct_Match':4,'Partial_Construct_Match':30,'Different_Constructs':4}
rng=random.Random(20261006);chosen=[]
for tab,n in quota.items():
 pool=[c for c in d['cases'] if c['tab']==tab];chosen.extend(rng.sample(pool,n))
rng.shuffle(chosen)
key=[];cases=[];assignments=[];ratings=[]
# Fixed concealed mapping; keep mapping in coordinator key only.
models={'GPT-6':'Model X','medgemma':'Model Y'}
for i,c in enumerate(chosen,1):
 h=f'H{i:03}';tab=c['tab'];N=sum(x['tab']==tab for x in d['cases'])
 key.append({'human_case':h,'original_case':c['id'],'category':tab,'segment':c['segment'],'meaning_unit_index':c['mu_index'],'population_units':N,'sample_units':quota[tab],'design_weight':N/quota[tab]})
 cases.append({'human_case':h,'assignments':len(c['rows']),'models_present':', '.join(sorted(set(models[r['model']] for r in c['rows'])))})
 for j,r in enumerate(c['rows'],1):
  assignments.append({'human_case':h,'assignment_id':f'{h}-R{j:02}','model':models[r['model']],'assigned_construct':r['cfir_construct'],**{f:r[f] or '' for f in ['rationale','critic_rationale','critic_coverage_rationale']}})
 for code in cb:ratings.append({'human_case':h,'code':code['code'],'rating':'','evidence_assignment_ids':'','evidence_field':'','exact_quote':'','memo':'','reviewer':''})
for name,rows in [('coordinator_key',key),('cases',cases),('assignments',assignments),('ratings',ratings)]:
 with (ROOT/'human_validation'/f'{name}.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(ROOT/'human_validation/coordinator_model_key.json').write_text(json.dumps(models,indent=2))
(ROOT/'human_validation/packet.json').write_text(json.dumps({'codebook':cb,'cases':cases,'assignments':assignments,'ratings':ratings},ensure_ascii=False,indent=2))
print('70 blinded cases;',len(assignments),'assignments;',len(ratings),'blank ratings')
