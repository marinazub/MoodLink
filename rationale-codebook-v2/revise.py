import json,pathlib,collections,re,hashlib,csv
P=pathlib.Path(__file__).parent;ROOT=P.parents[1];PR=ROOT/'rationale-codebook-validation'
old=json.loads((ROOT/'outputs/rationale-only-codebook-20261006/analysis.json').read_text())
raw=json.loads((PR/'data/rationale_cases.json').read_text())
b={c['case']:c for c in json.loads((PR/'coding/coder_B.json').read_text())}
meta=json.loads((P/'action_metadata.json').read_text());review=json.loads((P/'critic_review.json').read_text());candidates=json.loads((P/'critic_candidates.json').read_text())
challenged=[candidates[i] for i in review['candidate_indices']]
bycase=collections.defaultdict(list)
for r in challenged:bycase[r['case']].append(r)
cb=[c for c in old['codebook'] if c['code']!='U']
for c in cb:
 if c['code']=='A01':c['include']+=' Apply systematically to every paired case; do not restrict this code to worked examples.'
cb=[{'code':'D01','name':'Assignment–abstention sufficiency contrast','family':'Action / design','definition':'One model assigns a construct and the other supplies no assignment; under the stated coding rule this is an intended sufficient-versus-insufficient evidence contrast within evaluated packets.','include':'Original one-model-only categories, excluding standalone questions. Distinguish explicit opposite No Match from user-described category provenance when the opposite row is absent.','exclude':'Both models assigned; a No Match row alongside another assignment; verified processing failure. Does not prove identical packet exposure or identify the exact rejected inference.','anchor':'See restricted local evidence workbook.'},
 {'code':'R01','name':'Assignment justification challenged by critic','family':'Action / explanation / review','definition':'The coder assigns a construct, while critic_rationale explicitly contests that mapping or an essential part of its justification.','include':'Critic says required actor, process, referent, temporal state or boundary is not established; also includes a challenged substantive rationale claim.','exclude':'Ordinary scope caveats with an otherwise supported mapping; an explicit technical error; criticism inferred only from a decision/status column. A challenge does not establish that the critic is correct.','anchor':'See restricted local evidence workbook.'},
 {'code':'Q01','name':'Question','family':'Unit exclusion','definition':'The coded unit itself is a standalone interviewer question or request for an answer, rather than substantive participant evidence.','include':'Inspect unit text solely for this classification. Mark Question and exclude it from substantive threshold comparisons.','exclude':'Answers dependent on prior question context (M01); reported questions inside participant answers; declarative What was missing/What made it easier clauses.','anchor':'See restricted local evidence workbook.'}]+cb
names={c['code']:c['name'] for c in cb};evidence=[];units=[];source=[]
fields=['rationale','critic_rationale','critic_coverage_rationale'];letters=dict(zip(fields,['L','O','T']))
def short(text):
 words=list(re.finditer(r'\S+',text));start=0
 hit=re.search(r'does not|doesn.t|cannot|incorrect|too vague|overinterpret|not supported|not evidence|weak|specul|lacks',text,re.I)
 if hit and len(words)>40:
  idx=next(i for i,w in enumerate(words) if w.end()>hit.start());start=max(0,min(idx-5,len(words)-40))
 return text[words[start].start():words[min(start+40,len(words))-1].end()]
for c in raw['cases']:
 cid=c['id'];u0=next(u for u in old['units'] if u['case']==cid);mm=meta[cid];models={r['model'] for r in c['rows']};one=len(models)==1;question=cid in review['question_cases'];nm=[r for r in mm['rows'] if r['cfir_construct']=='No Match'];positive=[r for r in mm['rows'] if r['cfir_construct'] not in ['No Match',None]]
 mixed_models=sorted({r['model'] for r in nm}&{r['model'] for r in positive})
 codes=[x for x in b[cid]['codes'] if x!='U'];basis='Both models assigned'
 if question:codes=['Q01'];action='Question';basis='Unit-text audit'
 elif one:
  codes=['D01']+codes;assigning=next(iter(models));opposite='medgemma' if assigning=='GPT-6' else 'GPT-6';explicit=any(r['model']==opposite for r in nm)
  action=f'{assigning} assigns; {opposite} abstains by design';basis='Explicit opposite No Match' if explicit else 'Only-assignment category; opposite row absent'
 else:action='Both models assign; '+('mixed No Match record also present' if nm else 'compare chosen constructs')
 if bycase[cid] and not question:codes.append('R01')
 if one:
  interpretation='The assignment-versus-abstention action supports a difference in the evidence treated as sufficient under the stated protocol. The assigning rationale shows its mapping; the exact rejected step is not stated by the abstaining model.'
  if basis.startswith('Only'):interpretation+=' The abstention interpretation uses the user-described category provenance; this workbook does not contain an explicit opposite No Match row.'
 elif nm:interpretation='Both models have assignments. The extra No Match row must not be interpreted as global inability to code this unit; core/outcome export separation is a possible explanation requiring run provenance.'
 else:interpretation='Compare agreement in chosen labels separately from agreement in explanatory grounds and critic thresholds.'
 if mixed_models:interpretation+=' A '+', '.join(mixed_models)+' No Match row coexists with an assignment: inspect core versus outcome export origin rather than treating that model as globally abstaining.'
 if bycase[cid]:interpretation+=' At least one assigned label or essential justification is explicitly challenged by its critic.'
 mechanisms=[x for x in codes if x.startswith('M') and x!='M16']
 if mechanisms:interpretation+=' Recorded interpretive moves: '+ '; '.join(names[x] for x in mechanisms)+'.'
 units.append({'case':cid,'category':c['tab'],'segment':c['segment'],'mu_index':c['mu_index'],'question':'Question' if question else 'Not question','action':action,'action_basis':basis,'codes':list(dict.fromkeys(codes)),'gpt':u0['gpt'],'med':u0['med'],'critic_challenges':len(bycase[cid]),'critic_models':'; '.join(sorted({r['model'] for r in bycase[cid]})),'interpretation':interpretation,'legacy_memo':u0['note'],'mixed_record_models':'; '.join(mixed_models),'assignment_origins':'; '.join(dict.fromkeys(r['model']+': '+str(r['source_tab'])+' / '+str(r['construct_packet']) for r in positive)),'explicit_no_match_rows':'; '.join(f"{r['model']}: Combined_Outputs!J{r['source_row']}" for r in nm)})
 for r in c['rows']:source.append({'case':cid,**r,'review_note':'R01: critic challenges assignment/justification' if any(x['tab']==r['tab'] and x['row']==r['row'] for x in bycase[cid]) else 'No R01 observation recorded'})
 for ev in b[cid]['evidence']:
  if ev['code']=='U' or question:continue
  r=next(r for r in c['rows'] if r['tab']+'!'+r['cells'][ev['field']]==ev['source'])
  assert ev['quote'] in r[ev['field']] and len(ev['quote'].split())<=40
  evidence.append({'case':cid,'code':ev['code'],'layer':'Rationale interpretation','model':ev['model'],'construct':r['cfir_construct'],'field':ev['field'],'quote':ev['quote'],'full':r[ev['field']],'source':ev['source'],'note':'Carried forward from independent coder B after source identity check; not a new independent judgment.'})
 for r in bycase[cid]:
  q=short(r['critic_rationale']);assert q in r['critic_rationale'] and len(q.split())<=40
  evidence.append({'case':cid,'code':'R01','layer':'Proposal–review contrast','model':r['model'],'construct':r['cfir_construct'],'field':'critic_rationale','quote':q,'full':r['critic_rationale'],'source':r['tab']+'!'+r['cells']['critic_rationale'],'note':'New manual review: critic challenges assignment or essential justification; no decision/status column used.'})
 if one and not question:
  r=next(r for r in c['rows'] if r['rationale']);q=short(r['rationale'])
  evidence.append({'case':cid,'code':'D01','layer':'Action + design + assigning explanation','model':r['model'],'construct':r['cfir_construct'],'field':'rationale','quote':q,'full':r['rationale'],'source':r['tab']+'!'+r['cells']['rationale'],'note':basis+'. Assigning explanation is quoted; abstention meaning comes from prompts.py:46–63 and user-supplied provenance, not an invented No Match explanation.'})
 for r in nm:
  source.append({'case':cid,'tab':'Combined_Outputs','row':r['source_row'],'model':r['model'],'parent_segment_id':c['segment'],'meaning_unit_index':c['mu_index'],'cfir_construct':'No Match',**{f:r[f] for f in fields},'cells':{f:letters[f]+str(r['source_row']) for f in fields},'review_note':'Exported No Match; blank explanation fields retained. '+('Mixed with assignment from same model.' if not one else 'Intended insufficient-evidence action under protocol.')})
stats={'units':len(units),'positive_assignment_rows':len(raw['records']),'added_no_match_rows':len(source)-len(raw['records']),'question_cases':sum(u['question']=='Question' for u in units),'D01_cases':sum('D01' in u['codes'] for u in units),'explicit_abstention_cases':sum(u['action_basis']=='Explicit opposite No Match' for u in units),'category_only_cases':[u['case'] for u in units if u['action_basis'].startswith('Only-assignment')],'mixed_cases':[u['case'] for u in units if u['mixed_record_models']],'paired_mixed_cases':[u['case'] for u in units if 'mixed No Match' in u['action']],'R01_cases':len(bycase.keys() & {x['case'] for x in challenged}),'R01_assignments':len(challenged),'R01_by_model':dict(collections.Counter(r['model'] for r in challenged)),'evidence_excerpts':len(evidence),'code_counts':{code:sum(code in u['codes'] for u in units) for code in names}}
category=[]
for tab in dict.fromkeys(c['tab'] for c in raw['cases']):
 us=[u for u in units if u['category']==tab];rr=[r for r in challenged if r['tab']==tab]
 category.append({'category':tab,'units':len(us),'threshold_contrasts':sum('D01' in u['codes'] for u in us),'explicit_no_match':sum(u['action_basis']=='Explicit opposite No Match' for u in us),'critic_tension_cases':sum(u['critic_challenges']>0 for u in us),'challenged_assignments':len(rr),'questions':sum(u['question']=='Question' for u in us)})
stats['categories']=category
method=[
 ['Version','Version2: action, explanation and review layers. Replaces U as the central result for one-model-only cases; retains the absence of a specific rejection explanation as a qualification.'],
 ['Research question','Which evidence-to-construct interpretations accompany assignment versus abstention, agreement, and different labels, and where do assignment and critic explanation diverge?'],
 ['No Match design','prompts.py:46–63 requires clear evidence, evaluates only the current packet, and specifies assignments:[] for insufficient evidence. No numerical cutoff is specified. D01 captures an intended qualitative sufficiency contrast.'],
 ['Export meaning','export_excel.py:367–381 writes No Match when a segment has no coding results; it is not necessarily model-returned text. Current code excludes interviewer questions and separates core versus outcome results before export.'],
 ['Export limitations','coding.py:212–214 skips parse-error results; coding.py:358 returns empty results after exhausted retries. A displayed No Match alone cannot distinguish valid abstention from every processing pathway. No case is labeled a technical failure without case-specific evidence. Current source code documents design, not verified historical run configuration.'],
 ['Packet limitation','Model evaluates current packet only. Same packet exposure and model-independent ground truth are not established by these exports; do not claim a globally stricter model or a numerical threshold.'],
 ['Evidence boundaries','Substantive mechanisms use only rationale, critic_rationale and critic_coverage_rationale. Assignment/No Match labels and category membership provide action metadata; prompt/export code and user clarification provide design context.'],
 ['Question exception','Meaning-unit text was reviewed solely to classify standalone questions under the user’s instruction. No standalone questions among259 units. M01 context dependence does not mean Question.'],
 ['Coding changes','A01 and all unchanged interpretation codes now use the completed systematic independent-coder B application. Original A decisions are retained in the historical archive, not silently changed. U is retired. D01, R01 and Q01 are new; R01 was manually reviewed from complete candidate critic text and supplemental error/boundary checks.'],
 ['Decision values','yes requires documented support. Unlisted interpretation codes remain unclear, not no. A critic challenge records disagreement with justification, not correctness.'],
 ['Mind versus action','Action = assignment/exported abstention. Stated interpretation = rationale. Review position = critic text. These are observable outputs, not access to hidden cognition or necessarily the same model instance acting as its own critic.'],
 ['Action corroboration','122 one-model-only category cases:120 have explicit opposite No Match rows. C033 and C120 rely on the user-described category provenance; no opposite row is present in Combined_Outputs. Ten cases contain a No Match row alongside an assignment by the same model, with outcomes recorded separately. Nine remain one-model-only across models; C248 has assignments from both and stays paired.'],
 ['Review changes',f"R01 records {len(challenged)} challenged assignments in {stats['R01_cases']} units. Ordinary limiting caveats were excluded unless they contest a mapping or essential justification. Critics can themselves make mistakes."],
 ['Coverage','C01 describes assignment-level partitioning of claims; C02 identifies differing coverage assessment scope. Do not equate either with a whole-model coverage failure.'],
 ['Validation status','The prior93.0% agreement / κ0.704 applies to the old codebook/application. It does not validate this revised23-code version or new R01/D01/Q01 decisions. Existing human packet and prior independent results remain historical; revised human/independent validation is pending.'],
 ['Source scope','259 cases from the five original categories;892 assignment rows preserved, with130 linked No Match rows added as action provenance (121 opposite/mixed-comparison rows plus9 assigning-model rows). No new source cases introduced.'],
 ['Quote audit',f"{len(evidence)} exact excerpts of at most40 words verified against allowed rationale fields. Action/design support is explicitly distinguished from these quotations."],
 ['Question rule','Standalone interviewer questions: Q01 only; exclude from substantive sufficiency counts. Answers mentioning questions or dependent on context: retain and consider M01.'],
 ['Reproducibility','Versioned source extract, code definitions, manual critic review indices and scripts retained with the revised analysis. The original workbook is backed up before replacement.']]
out={'version':2,'units':units,'codebook':cb,'evidence':evidence,'source':source,'stats':stats,'method':method,'categories':category}
(P/'analysis_v2.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));(P/'stats_v2.json').write_text(json.dumps(stats,indent=2))
with (P/'coded_cases_v2.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(units[0]));w.writeheader();w.writerows([{**u,'codes':'; '.join(u['codes'])} for u in units])
codebook='# Codebook v2: assignment, explanation and review\n\n'+ '\n\n'.join('**'+k+':** '+v for k,v in method[:11])+'\n\n## Definitions\n'
for c in cb:codebook+=f"\n### {c['code']} — {c['name']}\n\n{c['definition']}\n\n**Include:** {c['include']}\n\n**Exclude:** {c['exclude']}\n\n**Anchor:** {c['anchor']}\n"
(P/'Codebook_v2.md').write_text(codebook)
print(json.dumps(stats,indent=2))
