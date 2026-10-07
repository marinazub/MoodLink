import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const d=JSON.parse(await fs.readFile(path.join(root,'human_validation/packet.json'),'utf8'));
const wb=Workbook.create();for(const n of ['Instructions','Codebook','Cases','Assignments','Ratings'])wb.worksheets.add(n);
const col=n=>{let s='';for(n++;n;n=Math.floor((n-1)/26))s=String.fromCharCode(65+(n-1)%26)+s;return s};
function table(name,headers,rows,widths){
 const s=wb.worksheets.getItem(name),last=rows.length+1,edge=col(headers.length-1);s.showGridLines=false;
 s.getRange(`A1:${edge}${last}`).values=[headers,...rows];const all=s.getRange(`A1:${edge}${last}`);
 all.format.font={name:'Arial',size:11,color:'#243247'};all.format.wrapText=true;all.format.verticalAlignment='top';
 widths.forEach((w,i)=>s.getRange(`${col(i)}1:${col(i)}${last}`).format.columnWidthPx=w);
 s.tables.add(`A1:${edge}${last}`,true,name+'Table').style='TableStyleMedium2';
 s.getRange(`A1:${edge}1`).format={fill:'#243E62',font:{name:'Arial',size:11,bold:true,color:'#FFFFFF'},wrapText:true,verticalAlignment:'center',rowHeight:58};
 rows.forEach((r,i)=>{const lines=Math.max(...r.map((x,j)=>String(x??'').split('\n').reduce((a,t)=>a+Math.max(1,Math.ceil(t.length/Math.max(8,(widths[j]-20)/7.7))),0)));s.getRange(`A${i+2}:${edge}${i+2}`).format.rowHeightPx=Math.min(545,Math.max(44,lines*19+20));});
 s.freezePanes.freezeRows(1);s.freezePanes.freezeColumns(1);return s;
}
const instructions=[
 ['Task','Independently code each of70 human cases against the21 frozen definitions. Do not view agent decisions or the coordinator key before saving initial ratings.'],
 ['Evidence','Read all assignment rows for the case. Use only rationale, critic_rationale, critic_coverage_rationale. Assigned construct labels are metadata.'],
 ['Values','yes = explicit documented mechanism; unclear = not established. Blank = unfinished, never equivalent to unclear.'],
 ['Paired evidence','A01/A02 compare Model X with Model Y for the same case. Coder and critic of one model do not count as paired models.'],
 ['For every yes','Enter assignment ID(s), field name(s), exact quote(s), and reviewer identifier. Each excerpt must be ≤40 words. Cite both models when comparison is required.'],
 ['For unclear','Enter unclear and your reviewer identifier. Notes on ambiguity are welcome.'],
 ['Scope caution','A critic can be wrong. Coverage of one assignment is not the coverage of a full model set. Missing comparator explanations cannot explain that model’s omission.'],
 ['How to work','Filter Ratings by case/code, and Assignments by human case. Save completed initial ratings under a new name. Record later adjudication separately.'],
 ['Data provenance','Blinded subset of the user-supplied comparison workbook; original identifiers, model identities, categories and locators are held in a separate coordinator key.'],
 ['Completed ratings',0],['Total ratings',1470],['Remaining ratings',1470]
];
const ins=table('Instructions',['Item','Instructions / progress'],instructions,[230,1050]);
table('Codebook',['Code','Name','Definition','Include when','Exclude / distinguish'],d.codebook.map(c=>[c.code,c.name,c.definition,c.include,c.exclude]),[85,280,480,450,450]);
table('Cases',['Human case','Assignment rows','Models present'],d.cases.map(c=>[c.human_case,c.assignments,c.models_present]),[130,160,280]);
table('Assignments',['Human case','Assignment ID','Masked model','Assigned construct (metadata)','rationale','critic_rationale','critic_coverage_rationale'],d.assignments.map(r=>[r.human_case,r.assignment_id,r.model,r.assigned_construct,r.rationale,r.critic_rationale,r.critic_coverage_rationale]),[115,150,125,310,850,1050,850]);
const names=Object.fromEntries(d.codebook.map(c=>[c.code,c.name]));
const rating=table('Ratings',['Human case','Code','Mechanism / pattern','Rating','Evidence assignment IDs','Evidence field(s)','Exact quote(s): ≤40 words each','Memo / additional excerpts','Reviewer ID','Completion'],d.ratings.map(r=>[r.human_case,r.code,names[r.code],'','','','','','','']),[115,85,280,115,240,260,640,580,170,205]);
rating.getRange('D2:I1471').format.fill='#FFF8DF';
rating.getRange('D2:D1471').dataValidation={rule:{type:'list',values:['yes','unclear']}};
const formulas=d.ratings.map((_,i)=>{const r=i+2;return [`=IF(D${r}="","Unrated",IF(AND(D${r}<>"yes",D${r}<>"unclear"),"Invalid rating",IF(I${r}="","Reviewer needed",IF(AND(D${r}="yes",OR(E${r}="",F${r}="",G${r}="")),"Evidence needed","Complete"))))`];});
rating.getRange('J2:J1471').formulas=formulas;
ins.getRange('B11').formulas=[['=COUNTIF(Ratings!J2:J1471,"Complete")']];
ins.getRange('B12').formulas=[['=COUNTA(Ratings!A2:A1471)']];
ins.getRange('B13').formulas=[['=B12-B11']];
wb.recalculate();
if(rating.getRange('J2').values[0][0]!=='Unrated')throw Error('Blank response incorrectly complete');
rating.getRange('D2').values=[['yes']];rating.getRange('I2').values=[['QA']];wb.recalculate();
if(rating.getRange('J2').values[0][0]!=='Evidence needed')throw Error('Missing evidence incorrectly complete');
rating.getRange('E2:G2').values=[['H001-R01','rationale',d.assignments[0].rationale.split(/\s+/).slice(0,20).join(' ')]];wb.recalculate();
if(rating.getRange('J2').values[0][0]!=='Complete'||ins.getRange('B11').values[0][0]!==1)throw Error('Complete rating not counted');
rating.getRange('D2:I2').values=[['','','','','','']];wb.recalculate();
if(ins.getRange('B11:B13').values.flat().join(',')!=='0,1470,1470')throw Error('QA not restored');
console.log((await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:10},summary:'Human packet formula scan'})).ndjson);
await fs.mkdir(path.join(root,'human_validation/qa'),{recursive:true});
for(const [sheetName,range] of [['Instructions','A1:B6'],['Codebook','A1:C4'],['Cases','A1:C5'],['Assignments','C1:F3'],['Ratings','A1:F4']]){
 const blob=await wb.render({sheetName,range,scale:1,format:'png'});await fs.writeFile(path.join(root,'human_validation/qa',sheetName+'.png'),new Uint8Array(await blob.arrayBuffer()));
}
await(await SpreadsheetFile.exportXlsx(wb)).save(path.join(root,'human_validation/Human_Validation_Blinded.xlsx'));
console.log('Human workbook saved; completion workflow tested and blank state restored.');
