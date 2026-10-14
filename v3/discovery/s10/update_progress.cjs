'use strict';
// Reporting-only transformation; historical source row objects are unchanged.
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict'),k=require('./retained.cjs');
const directory=path.dirname(__dirname),md=path.join(directory,'recurrences.md'),js=path.join(directory,'recurrences.json');
let text=fs.readFileSync(md,'utf8');const data=JSON.parse(fs.readFileSync(js,'utf8'));
assert(!text.includes('| Audit fees |'),'One-time layout migration already applied');
const lines=text.split(/\r?\n/),indices=[];lines.forEach((s,i)=>{if(s.startsWith('|'))indices.push(i);});
assert.equal(indices.length,21);const old=indices.map(i=>lines[i]);
k.save(path.join(__dirname,'reporting_before.json'),{stage:'administration',research_credit_ns:0,markdown_sha256:k.sha(md),json_sha256:k.sha(js),original_table:old,source_base:'04e7f331f806b95b6671071c3f9d90edd0edeea3'});
const repair=s=>s.replaceAll('Ã—','×').replaceAll('â€“','–').replaceAll('Î”','Δ').replaceAll('â€¦','…').replaceAll('âˆ’','−');
const header=['Recurrence / recorded boundary','Research min','Cumulative min','Families (Δ)','Resource comparison scope','Audit fees','Counted computation','Ordinary-method comparison','272 edits: transport / broad / targeted','80 requests: outputs / cache / action cost','S28: outputs / plans / quotation / bill ratio','F01: ≥10% full-cost regions','Promotion forecast (80% minimum)','What changed'];
const table=['| '+header.join(' | ')+' |','| '+header.map((_,i)=>i>=1&&i<=3?'---:':'---').join(' | ')+' |'];
for(const raw of old.slice(2)){
 const c=raw.split('|').slice(1,-1).map(s=>repair(s.trim()));assert.equal(c.length,17);
 let scope='—',fee='—',compute='—',ordinary='See scoped finding';
 if(c[0].includes('s07/')){scope='S28 a03, 16 outputs; Oct 12';fee='14 audits / 14 audit-first; monetary tariff not established';compute='2,306,193 / 485,066 audit-first; **4.7544×**';ordinary='Audit-first uses fewer named units; same 14 audits and 14 complete calls';}
 if(c[0].includes('s08/')){
  scope='**bc02:** 512 outputs/arm, 4 fresh streams<br>**gc02:** 768 outputs/arm, 12 graphs; Oct 14';
  fee='**bc02: 2,886 vs 4,608 fallback; −37.37%**<br>gc02: 33,448 vs 35,584 fallback; −6.00%';
  compute='**bc02: 137,310 vs 152,022 fallback; −9.68%**<br>gc02: 4,640,221 vs 378,534 fallback; **+1,125.84%**';
  ordinary='**Identical ordinary controllers tie both metrics.** bc02 vs ordinary greedy cover: fee −1.74%, computation −12.79%';
  c[16]='Four-hour override. bc02 improves both recorded components against fallback; gc02 saves fees with much higher computation. The failed gc02 scan adds 6,595 fee and ≥18,576,219 named units outside these completed-arm comparisons. Matroid/group queries and six scalar proofs extend capability. No F01 rerun or promotion.';
 }
 const bundle=(ids,labels)=>ids.every(i=>c[i]==='—')?'—':ids.map((i,j)=>labels[j]+': '+c[i]).join('<br>');
 table.push('| '+[...c.slice(0,4),scope,fee,compute,ordinary,bundle([4,5,6],['Transport','Broad','Targeted']),bundle([7,8,9],['Outputs','Cache','Action cost']),bundle([10,11,12,13],['Outputs','Plans','Quotes','Ratio']),c[14],c[15],c[16]].join(' | ')+' |');
}
lines.splice(indices[0],indices.length,...table);text=repair(lines.join('\n'));
text=text.replace('separate columns because their measurements are not interchangeable.','separate labeled cells because their measurements are not interchangeable. Audit-fee and\ncounted-computation comparisons now have visible columns. These are scoped\ncomponents, not complete economic cost or elapsed runtime. Percent changes use\n(candidate − comparator) / comparator; negative is a saving. The same ordinary\nimplementation is shown explicitly even when it ties.');
text=text.replace('## Latest row: scope and evidence','## Resource columns: scope and evidence\n\nThe bc02 headline is **37.37% lower physical fee and 9.68% lower counted\ncomputation against anchor-only fallback**, for 512 outputs per arm. Both\ncomponents tie the ordinary-budget mirror. Against greedy cover, the savings\nare 1.74% and 12.79%. The broader gc02 comparison is adverse in computation,\nand its failed scan acquisition is an additional bill. Source, menus, caps,\nsetup, actual request counts, observation dates and failures are in\n[s08 progress](s08/progress_results.json) and [findings](s08/graph_cover_findings.md).\nThese findings concern different duties from S28 and do not alter F01.\n\n## Retained S28 scope and evidence');
const pct=(candidate,comparison)=>100*(candidate-comparison)/comparison;
data.visible_resource_metrics={prepared_by:'Codex (GPT-6)',prepared_date_utc:'2026-10-14',research_credit_ns:0,reason:'Author requested audit fee, counted computation and ordinary comparisons as visible progress metrics',historical_rows_unchanged:true,percent_convention:'100 * (candidate - comparison) / comparison; negative means lower cost',s08:{observation_date_utc:'2026-10-14',age_at_s08:0,bc02:{outputs_per_arm:512,streams:4,source:'s08/progress_results.json',source_sha256:k.sha(path.join(directory,'s08/progress_results.json')),candidate:{fee:2886,named_units:137310},fallback:{fee:4608,named_units:152022},ordinary_equivalent:{fee:2886,named_units:137310},ordinary_greedy:{fee:2937,named_units:157452},change_vs_fallback_percent:{fee:pct(2886,4608),named_units:pct(137310,152022)},change_vs_ordinary_equivalent_percent:{fee:0,named_units:0},change_vs_greedy_percent:{fee:pct(2886,2937),named_units:pct(137310,157452)}},gc02:{outputs_per_arm:768,graphs:12,candidate:{fee:33448,named_units:4640221},fallback:{fee:35584,named_units:378534},ordinary_equivalent:{fee:33448,named_units:4640221},change_vs_fallback_percent:{fee:pct(33448,35584),named_units:pct(4640221,378534)},additional_failed_scan:{fee:6595,named_units_lower_bound:18576219,incomplete_computation:'unknown'}}},unknowns:'Complete economic costs, native/host and storage terms remain unknown. Named units are implementation counters, not elapsed time.'};
fs.writeFileSync(md,text);k.save(js,data);
console.log(JSON.stringify(data.visible_resource_metrics.s08,null,2));
