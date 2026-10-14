'use strict';
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');let s=fs.readFileSync(path.join(__dirname,'check_lp02.cjs'),'utf8');
s=s.replaceAll("'lp02'","'wt02'").replaceAll("'lp02:'","'wt02:'");
s=s.replace('let outputs=0,purchases=0,equivalences=0,covers=0,negativeControls=0;','let outputs=0,purchases=0,equivalences=0,covers=0,negativeControls=0,positiveRecords=0,negativeRecords=0,cacheHitsChecked=0;');
const gs=s.indexOf('function getModels'),ge=s.indexOf('function box',gs);
s=s.slice(0,gs)+String.raw`function getModels(c,setup){if(cache.has(c.source.id))return cache.get(c.source.id);const original=dg.check(c.source,read(path.join(root,'objects',setup.proof_object)),meter),diagram=tr.check(original,setup.transformed,meter),counts=[0n,1n];for(let i=2;i<diagram.nodes.length;i++)counts[i]=counts[diagram.nodes[i].low]+counts[diagram.nodes[i].high];const models=k.enumerate(c.source,meter);assert.equal(BigInt(models.length),counts[diagram.root]);cache.set(c.source.id,models);return models;}
`+s.slice(ge);
const a=s.indexOf('function coverCheck'),b=s.indexOf('for(const c of design.cases)',a);
s=s.slice(0,a)+String.raw`
function pattern(known){return known.map(x=>x===null?'_':'x').join('');}
function pairFloor(source,pair,known){const {lo,hi}=box(known,source.features.length),[v,w]=pair.map(p=>{assert.deepEqual(k.modelFeatures(source,p.mask,meter),p.v);return p.v;});let sum=0;for(let i=0;i<lo.length;i++)sum+=3*(v[i]===w[i]?(v[i]===0?2*Math.min(0,hi[i]):-2*Math.max(0,lo[i])):Math.min(hi[i],-lo[i]));return sum;}
function positiveBound(record,known){assert.equal(pattern(known),record.pattern);let extra=0;for(let i=0;i<record.action.a.length;i++){const d=(known[2*i]===null?0:known[2*i]-record.anchor[2*i])-(known[2*i+1]===null?0:known[2*i+1]-record.anchor[2*i+1]),a=record.action.a[i];extra+=Math.max(a*d,(a-3)*d);}return record.upper+extra;}
function checkEntry(c,models,e,arm){
 k.checkSeal(e);assert.equal(e.source_id,c.source.id);const known=e.kind==='positive'?e.record.anchor:e.known;assert.equal(e.key,arm==='exact_cache'?known.map(x=>x===null?'_':x).join(','):pattern(known));
 if(e.kind==='positive'){const r=e.record,a=counts(c.source,r.action.models);assert.deepEqual(a,r.action.a);assert.equal(pattern(r.anchor),r.pattern);const b=box(r.anchor,a.length);assert.equal(regret(models,a,b.lo,b.hi),r.upper);assert.equal(r.tolerance,6000*c.tolerance);assert(r.upper<=r.tolerance);}else{assert.equal(e.kind,'negative');assert(pairFloor(c.source,e.pair,e.known)>12000*c.tolerance);}
}
`+s.slice(b);
const st=s.indexOf('if(setup.compiled&&setup.compiled.selected)'),en=s.indexOf('\n  let feeSum',st);
s=s.slice(0,st)+String.raw`const entries=lines(path.join(out,'cache.jsonl')),entryMap=new Map(entries.map(e=>[e.id,e]));assert.equal(entryMap.size,entries.length);for(const e of entries){checkEntry(c,models,e,arm);if(e.kind==='positive')positiveRecords++;else negativeRecords++;let bad=structuredClone(e);if(bad.kind==='positive')bad.record.action.a[0]++;else bad.pair[0].v[0]^=1;delete bad.id;bad=k.seal(bad);assert.throws(()=>checkEntry(c,models,bad,arm));negativeControls++;}`+s.slice(en);
const anchor='fee+=receipt.fee;purchases++;';assert(s.includes(anchor));s=s.replace(anchor,anchor+String.raw`
    const decision=row.decisions[j];if(decision){assert.equal(decision.query,receipt.query);const resolution=decision.resolution;if(resolution.entry){const e=entryMap.get(resolution.entry);assert(e);assert(e.created_request<row.request||(e.created_request===row.request&&e.created_sequence<=j));if(e.kind==='positive'){assert(positiveBound(e.record,known)<=6000*c.tolerance);assert.equal(resolution.closes,true);}else{assert(pairFloor(c.source,e.pair,known)>12000*c.tolerance);assert.equal(resolution.closes,false);}if(arm==='exact_cache')assert.deepEqual(e.kind==='positive'?e.record.anchor:e.known,known);if(resolution.kind.endsWith('_hit')){assert(e.created_request<row.request||e.created_sequence<j);cacheHitsChecked++;}else{assert.equal(e.created_request,row.request);assert.equal(e.created_sequence,j);}}}
    for(const e of entries)if(e.created_request===row.request&&e.created_sequence===j)assert.deepEqual(e.kind==='positive'?e.record.anchor:e.known,known);
`);
s=s.replace("if(arm==='contingent')baseline.push(behavior);if(arm==='ordinary_contingent')","if(arm==='neighborhoods')baseline.push(behavior);if(arm==='ordinary_neighborhoods')");
s=s.replace('contingent_outputs:0,cache_hits:0,cache_misses:0','positive_hits:0,negative_hits:0,floor_skips:0,local_calls:0,cache_tests:0,cache_entries:0');
s=s.replace('outputs,purchases,equivalences,covers,negativeControls,totals','outputs,purchases,equivalences,positiveRecords,negativeRecords,cacheHitsChecked,negativeControls,totals');
s=s.replace('Source-complete model sets by checked diagrams and cardinality; direct latent-box regret for every output; every stored winning cover checked on whole intervals via endpoints.','Independent truth-enumerated source models matched checked diagram cardinality; direct latent-box regret for every output and positive anchor; feasible-witness pair bounds for negative records; every reuse checks source, pattern/value rules, and temporal provenance.');
fs.writeFileSync(path.join(__dirname,'check_witness.cjs'),s);
