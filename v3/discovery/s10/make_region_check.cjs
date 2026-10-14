'use strict';
// Build a new checker; preserve the earlier executed checker unchanged.
const fs=require('node:fs'),path=require('node:path');
let s=fs.readFileSync(path.join(__dirname,'check_lp02.cjs'),'utf8');
s=s.replaceAll("'lp02'","process.argv[2]||'rr01'").replace("'lp02:'+c.name","path.basename(root)+':'+c.name");
s=s.replace('let outputs=0,purchases=0,equivalences=0,covers=0,negativeControls=0;','let outputs=0,purchases=0,equivalences=0,covers=0,negativeControls=0,positiveRegions=0,negativeRegions=0,cacheHitsChecked=0;');
const begin=s.indexOf('function coverCheck('),end=s.indexOf('for(const c of design.cases)',begin);
s=s.slice(0,begin)+String.raw`
function component(x,y,l,u){return x===y?(x===0?2*Math.min(0,u):-2*Math.max(0,l)):Math.min(u,-l);}
function mapFor(before,q){const other=before[2*q.coordinate+(q.kind==='true'?1:0)];return q.kind==='true'?{coordinate:q.coordinate,max:24000,lo0:other===null?-24000:-other,lo1:1,hi0:other===null?0:-other,hi1:1}:{coordinate:q.coordinate,max:24000,lo0:other===null?0:other,lo1:-1,hi0:other===null?24000:other,hi1:-1};}
function contains(r,t){return r.kind==='positive'?r.lower<=6*t&&6*t<=r.upper:r.inequalities.every(x=>x.left_coefficient*t>x.right);}
function checkEntry(c,models,setup,e){
 k.checkSeal(e);assert.equal(e.source_id,c.source.id);assert.equal(e.key,c.source.id+':'+e.query_index+':'+e.before.map(x=>x===null?'_':x).join(','));
 const q=setup.queries[e.query_index],map=mapFor(e.before,q),{lo,hi}=box(e.before,c.source.features.length),r=e.region;assert.deepEqual(map,e.map);assert.equal(e.before[2*q.coordinate+(q.kind==='false'?1:0)],null);
 if(r.kind==='positive'){
  const a=counts(c.source,r.action.models);assert.deepEqual(a,r.action.a);assert(r.lower>=0&&r.upper<=144000&&r.lower<=r.upper);assert(Number.isInteger(r.lower)&&Number.isInteger(r.upper));
  for(const t of [r.lower,r.upper]){const l=lo.map(x=>6*x),u=hi.map(x=>6*x);l[q.coordinate]=6*map.lo0+map.lo1*t;u[q.coordinate]=6*map.hi0+map.hi1*t;assert(regret(models,a,l,u)<=36000*c.tolerance);}
 }else{
  assert.equal(r.kind,'negative');assert.deepEqual(r.query,map);assert.equal(r.pair.length,2);const [v,w]=r.pair.map(mask=>k.modelFeatures(c.source,mask,meter)),i=q.coordinate;
  assert.deepEqual(r.pair,r.indices.map(j=>models[j].mask));let other=0;for(let j=0;j<lo.length;j++)if(j!==i)other+=3*component(v[j],w[j],lo[j],hi[j]);assert.equal(r.other,other);
  const terms=v[i]===w[i]?(v[i]===0?[[0,0],[2*map.hi0,2*map.hi1]]:[[0,0],[-2*map.lo0,-2*map.lo1]]):[[map.hi0,map.hi1],[-map.lo0,-map.lo1]];
  assert.deepEqual(r.inequalities,terms.map(([b,a])=>({left_coefficient:3*a,right:12000*c.tolerance-other-3*b})));
  const samples=[0,12000,24000];for(const h of r.inequalities)if(h.left_coefficient!==0){const t=h.right/h.left_coefficient;for(const d of [-1,0,1])if(t+d>=0&&t+d<=24000)samples.push(t+d);}
  for(const t of samples)assert.equal(contains(r,t),other+3*component(v[i],w[i],map.lo0+map.lo1*t,map.hi0+map.hi1*t)>12000*c.tolerance);
 }
}
`+s.slice(end);
const oldStart=s.indexOf('if(setup.compiled&&setup.compiled.selected)'),oldEnd=s.indexOf('\n  let feeSum',oldStart);
s=s.slice(0,oldStart)+String.raw`const entries=lines(path.join(out,'cache.jsonl')),entryMap=new Map(entries.map(e=>[e.id,e]));assert.equal(entryMap.size,entries.length);for(const e of entries){checkEntry(c,models,setup,e);if(e.region.kind==='positive')positiveRegions++;else negativeRegions++;const bad=structuredClone(e);bad.source_id='wrong';assert.throws(()=>checkEntry(c,models,setup,bad));negativeControls++;}`+s.slice(oldEnd);
s=s.replace('for(let j=0;j<row.receipts.length;j++){const receipt=row.receipts[j];','for(let j=0;j<row.receipts.length;j++){const before=known.slice(),receipt=row.receipts[j];');
const anchor='fee+=receipt.fee;purchases++;';
s=s.replace(anchor,anchor+String.raw`
    const decision=row.decisions&&row.decisions[j];if(decision){assert.equal(decision.query,receipt.query);const resolution=decision.resolution;if(resolution&&resolution.entry){const e=entryMap.get(resolution.entry);assert(e);assert.deepEqual(e.before,before);assert.equal(e.query_index,receipt.query);assert(e.created_request<row.request||(e.created_request===row.request&&e.created_sequence<=j));const q=setup.queries[e.query_index],t=known[2*q.coordinate+(q.kind==='false'?1:0)];assert(contains(e.region,t));assert.equal(resolution.closes,e.region.kind==='positive');if(resolution.kind.endsWith('_hit')){assert(e.created_request<row.request||e.created_sequence<j);cacheHitsChecked++;}else{assert.equal(e.created_request,row.request);assert.equal(e.created_sequence,j);}}}
    for(const e of entries)if(e.created_request===row.request&&e.created_sequence===j){assert.deepEqual(e.before,before);assert.equal(e.query_index,receipt.query);}
`);
s=s.replace("if(arm==='contingent')baseline.push(behavior);if(arm==='ordinary_contingent')","if(arm===design.arms[0])baseline.push(behavior);if(arm===design.arms[1])");
s=s.replace('contingent_outputs:0,cache_hits:0,cache_misses:0','positive_hits:0,negative_hits:0,floor_skips:0,local_calls:0,cache_hits:0,cache_misses:0,cache_entries:0');
s=s.replace('outputs,purchases,equivalences,covers,negativeControls,totals','outputs,purchases,equivalences,positiveRegions,negativeRegions,cacheHitsChecked,negativeControls,totals');
s=s.replace('every stored winning cover checked on whole intervals via endpoints.','positive cache intervals checked at both endpoints; negative intervals checked algebraically from feasible witness pairs and strict boundaries; cache source, prior-information context and temporal provenance checked.');
fs.writeFileSync(path.join(__dirname,'check_regions.cjs'),s);
