import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const dir=path.dirname(fileURLToPath(import.meta.url));
const d=JSON.parse(await fs.readFile(`${dir}/analysis_v2.json`,'utf8'));
const wb=Workbook.create();
for(const n of ['Category findings','Codebook','Coded units','Evidence','Source rationales','Method'])wb.worksheets.add(n);
const col=n=>{let s='';for(n++;n;n=Math.floor((n-1)/26))s=String.fromCharCode(65+(n-1)%26)+s;return s};
function table(name,headers,rows,widths,start=1){
 const s=wb.worksheets.getItem(name),last=start+rows.length,edge=col(headers.length-1);s.showGridLines=false;
 s.getRange(`A${start}:${edge}${last}`).values=[headers,...rows];const all=s.getRange(`A${start}:${edge}${last}`);
 all.format.font={name:'Arial',size:11,color:'#243247'};all.format.wrapText=true;all.format.verticalAlignment='top';
 widths.forEach((w,i)=>s.getRange(`${col(i)}${start}:${col(i)}${last}`).format.columnWidthPx=w);
 s.tables.add(`A${start}:${edge}${last}`,true,name.replaceAll(' ','')+'Table').style='TableStyleMedium2';
 s.getRange(`A${start}:${edge}${start}`).format={fill:'#243E62',font:{name:'Arial',size:11,bold:true,color:'#FFFFFF'},wrapText:true,verticalAlignment:'center',rowHeight:62};
 rows.forEach((r,j)=>{const lines=Math.max(...r.map((x,i)=>String(x??'').split('\n').reduce((a,l)=>a+Math.max(1,Math.ceil(l.length/Math.max(8,(widths[i]-20)/7.7))),0)));s.getRange(`A${start+j+1}:${edge}${start+j+1}`).format.rowHeightPx=Math.min(545,Math.max(45,lines*19+20));});
 s.freezePanes.freezeRows(start);s.freezePanes.freezeColumns(1);return s;
}
const explanations={
 GPT6_Only_Assignments:'GPT assigns where MedGemma abstains under the evidence rule. Examine the GPT mapping, inferred steps, and whether its critic challenges the proposal.',
 Medgemma_Only_Assignments:'MedGemma assigns where GPT abstains under the evidence rule. Process, role and relationship extensions can make a match plausible to the assigning model.',
 Total_Construct_Match:'Shared labels may reflect shared substantive grounds or different sufficiency standards in the critic texts.',
 Partial_Construct_Match:'Common ground plus additional interpretive steps; some shared labels still receive different critic readings.',
 Different_Constructs:'Different aspects, targets or levels can lead to different labels. C248 has a mixed core/outcome export record; both models do assign.'
};
const cat=table('Category findings',['Original category','Units','D01: design-based contrast','Explicit opposite No Match','Cases with critic challenge','Question cases','Interpretation'],d.categories.map(c=>[c.category,c.units,c.threshold_contrasts,c.explicit_no_match,c.critic_tension_cases,c.questions,explanations[c.category]]),[265,90,165,170,170,115,730],10);
cat.getRange('A1').values=[['Version 2 — assignment actions, stated reasoning, and critic review']];cat.getRange('A1').format.font={name:'Arial',size:18,bold:true,color:'#243E62'};
for(const [row,text] of [[3,'No Match is the intended insufficient-evidence action within evaluated packets; it is not an absence of all analytical information.'],[4,'122 one-model-only contrasts; 120 corroborated by explicit opposite No Match rows. The exact rejected inference remains unreported.'],[5,'139 cases contain a documented assignment–critic tension. A challenge does not prove that the critic is correct.'],[6,'No standalone interviewer questions among these 259 units. Question-context dependence is coded separately (M01).'],[7,'Ten cases contain a core No Match alongside an outcome assignment. Exported No Match is not always global abstention.'],[8,'The previous agreement figures and human packet apply to version 1. The new action/review codes require fresh validation.']])cat.getRange(`A${row}`).values=[[text]];
cat.getRange('A3:G8').format.font={name:'Arial',size:11,color:'#44556B'};
const codes=d.codebook.map(c=>c.code);
table('Coded units',['Case','Original category','Unit type','Observed / design-interpreted action','Action corroboration','GPT assignments','MedGemma assignments','Revised codes','Challenged assignments','Critic-text model labels','Interpretation of action and explanation','Same-model No Match + assignment','Assignment export origin / packet','Explicit No Match source rows','Original analytic memo (historical)','Segment ID','Meaning unit index',...codes],d.units.map(u=>[u.case,u.category,u.question,u.action,u.action_basis,u.gpt,u.med,u.codes.join('; '),u.critic_challenges,u.critic_models,u.interpretation,u.mixed_record_models,u.assignment_origins,u.explicit_no_match_rows,u.legacy_memo,u.segment,u.mu_index,...codes.map(c=>u.codes.includes(c)?'yes':'unclear')]),[80,260,145,390,360,420,420,280,135,190,950,190,620,420,760,440,120,...codes.map(()=>95)]);
const cb=table('Codebook',['Code','Pattern / mechanism','Analytic layer','Definition','Include when','Exclude / distinguish','Worked anchor','Documented cases'],d.codebook.map(c=>[c.code,c.name,c.family,c.definition,c.include,c.exclude,c.anchor,d.stats.code_counts[c.code]]),[85,300,230,520,540,540,430,145]);
for(let i=0;i<codes.length;i++)cb.getRange(`H${i+2}`).formulas=[[`=COUNTIF('Coded units'!$${col(17+i)}$2:$${col(17+i)}$260,"yes")`]];
table('Evidence',['Case','Code','Evidence layer','Model label','Assigned construct','Permitted field','Exact excerpt (≤40 words)','Original source cell','Evidence interpretation / provenance','Full permitted source field'],d.evidence.map(e=>[e.case,e.code,e.layer,e.model,e.construct,e.field,e.quote,e.source,e.note,e.full]),[80,80,250,110,290,210,650,350,780,1000]);
table('Source rationales',['Case','Original tab','Original row','Model','Segment ID','Meaning unit index','Assigned construct / No Match','rationale','critic_rationale','critic_coverage_rationale','rationale cell','critic cell','coverage cell','Analyst review / action note'],d.source.map(r=>[r.case,r.tab,r.row,r.model,r.parent_segment_id,r.meaning_unit_index,r.cfir_construct,r.rationale??'',r.critic_rationale??'',r.critic_coverage_rationale??'',r.cells.rationale,r.cells.critic_rationale,r.cells.critic_coverage_rationale,r.review_note]),[80,260,95,110,440,110,300,850,1000,850,120,120,120,650]);
table('Method',['Item','Protocol / interpretation limit'],d.method,[255,1250]);
wb.recalculate();
for(let i=0;i<codes.length;i++)if(cb.getRange(`H${i+2}`).values[0][0]!==d.stats.code_counts[codes[i]])throw Error('Code count mismatch');
console.log((await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:10},summary:'Version2 formula scan'})).ndjson);
await fs.mkdir(`${dir}/qa`,{recursive:true});
for(const [sheetName,range] of [['Category findings','A10:G12'],['Codebook','A1:D4'],['Coded units','H52:K54'],['Evidence','F1:J3'],['Source rationales','G1:J3'],['Method','A1:B5']]){
 const blob=await wb.render({sheetName,range,scale:1,format:'png'});await fs.writeFile(`${dir}/qa/${sheetName.replaceAll(' ','_')}.png`,new Uint8Array(await blob.arrayBuffer()));
}
await(await SpreadsheetFile.exportXlsx(wb)).save(`${dir}/Rationale_Only_Codebook_and_Coded_Cases.xlsx`);
console.log('Revised workbook staged; all code count formulas reconciled.');
