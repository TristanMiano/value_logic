'use strict';
// Read-only source/receipt reconstruction, independent exhaustive regret oracle.
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict'),k=require('./retained.cjs'),complete=require('./complete.cjs');
const root=path.join(__dirname,process.argv[2]||'rc03'),design=JSON.parse(fs.readFileSync(path.join(root,'design.json'),'utf8'));
const totals={},counts={outputs:0,receipts:0,proofs:0,box_certificates:0,corners:0,controls:0},diag=new k.Meter(),units=[];
function truthModels(source){
 const models=[];
 for(let x=0;x<2**source.variables;x++){
  const feasible=source.hard.every(clause=>clause.some(lit=>(Math.floor(x/2**(Math.abs(lit)-1))%2)===Number(lit>0)));
  if(feasible)models.push({mask:x,v:source.features.map(i=>Math.floor(x/2**(i-1))%2)});
 }
 assert(models.length);return models;
}
function objective(v,z){let total=0;for(let i=0;i<v.length;i++)total+=v[i]*z[i];return total;}
for(const c of design.cases){const models=truthModels(c.source),features=new Map(models.map(x=>[x.mask,x.v]));
 for(const arm of design.arms){const folder=path.join(root,c.name,arm),summary=JSON.parse(fs.readFileSync(path.join(folder,'summary.json'),'utf8')),setup=JSON.parse(fs.readFileSync(path.join(folder,'setup.json'),'utf8')),bank=setup.bank;
  if(bank.receipt)k.checkExtraction(c.source,bank.receipt,diag);
  for(const a of bank.actions){const b=a.a.map(()=>0);let K=0;if(bank.receipt){assert.equal(a.cert.lambda.length,bank.receipt.cuts.length);a.cert.lambda.forEach((x,i)=>{assert(Number.isSafeInteger(x)&&x>=0);K+=x;for(const f of bank.receipt.cuts[i].features)b[f]+=x;});}assert.equal(K,a.cert.K);assert.deepEqual(b,a.cert.b);const av=a.a.map(()=>0);for(const mask of a.models){assert(features.has(mask));features.get(mask).forEach((x,i)=>av[i]+=x);}assert.deepEqual(av,a.a);}
  const rand=k.rng(c.seed);let feeSum=0,namedSum=setup.invoice.named_units,callSum=0,proofSum=0;
  for(let r=0;r<c.requests;r++){
   const hidden=c.source.features.map(()=>[0,2,4][Math.floor(rand()*3)]),row=JSON.parse(fs.readFileSync(path.join(folder,'r'+String(r).padStart(3,'0')+'.json'),'utf8')),known=c.source.features.map(()=>null);assert.equal(row.status,'complete');assert.equal(row.source_id,c.source.id);let fee=0,exportUnits=0,checkUnits=0;
   for(const [index,receipt] of row.receipts.entries()){k.checkSeal(receipt);assert.equal(receipt.request_id,row.request_id);assert.equal(receipt.source_id,c.source.id);assert.equal(receipt.sequence,index);const indices=receipt.query==='all'?known.map((_,i)=>i):[receipt.query];if(receipt.query!=='all')assert.equal(known[receipt.query],null);assert.equal(receipt.fee,receipt.query==='all'?c.C:c.fees[receipt.query]);assert.deepEqual(receipt.observations,indices.map(i=>[i,hidden[i]]));for(const i of indices)known[i]=hidden[i];fee+=receipt.fee;exportUnits+=8+4*indices.length;checkUnits+=12+5*indices.length;counts.receipts++;}
   assert.deepEqual(known,row.known);assert.equal(fee,row.physical_fee);assert(fee<=2*c.C);assert.equal(row.provider_invoice.categories.physical_receipt_export||0,exportUnits);assert.equal(row.invoice.categories.physical_receipt_check||0,checkUnits);
   for(const invoice of [row.invoice,row.provider_invoice])assert.equal(k.sum(Object.values(invoice.categories)),invoice.named_units);
   const masks=row.result.models,m=masks.length,a=known.map(()=>0);for(const mask of masks){assert(features.has(mask));features.get(mask).forEach((v,i)=>a[i]+=v);}
   if(row.result.kind==='retained'){
    const lo=known.map(x=>x===null?0:x),hi=known.map(x=>x===null?4:x),q=a.map((x,i)=>x*hi[i]+(m-x)*lo[i]);
    const exact=objective(a,hi)-Math.min(...models.map(x=>objective(x.v,q)));assert(exact<=row.result.regret_upper&&row.result.regret_upper<=c.tolerance);counts.box_certificates++;
    if(a.length<=4){let regret=0;k.product(known.map(x=>x===null?[0,4]:[x]),z=>{regret=Math.max(regret,objective(a,z)-m*Math.min(...models.map(x=>objective(x.v,z))));counts.corners++;});assert.equal(regret,exact);}
   }else{
    assert(known.every(x=>x!==null));const checked=complete.check(c.source,known,row.logical,row.request_id,diag);assert.equal(checked.optimum,Math.min(...models.map(x=>objective(x.v,known))));assert.equal(objective(a,known),m*checked.optimum);assert.equal(row.result.regret_upper,0);proofSum++;counts.proofs++;
   }
   if(r===0){assert.throws(()=>{const altered=structuredClone(row);altered.source_id='wrong';assert.equal(altered.source_id,c.source.id);});counts.controls++;if(row.receipts.length){const altered=structuredClone(row.receipts[0]);altered.fee++;assert.throws(()=>k.checkSeal(altered));counts.controls++;}}
   feeSum+=fee;namedSum+=row.invoice.named_units+row.provider_invoice.named_units;callSum+=row.receipts.length;counts.outputs++;
  }
  assert.equal(feeSum,summary.physical_fee);assert.equal(namedSum,summary.named_units);assert.equal(callSum,summary.audit_calls);assert.equal(proofSum,summary.actual_complete_calls);assert.equal(summary.outputs,c.requests);
  if(!totals[arm])totals[arm]={outputs:0,fee:0,named_units:0,setup:0,audit_calls:0,complete_calls:0};const t=totals[arm];t.outputs+=c.requests;t.fee+=feeSum;t.named_units+=namedSum;t.setup+=setup.invoice.named_units;t.audit_calls+=callSum;t.complete_calls+=proofSum;
  units.push({case:c.name,arm,source_sha256:k.sha(path.join(folder,'setup.json')),summary_sha256:k.sha(path.join(folder,'summary.json'))});console.log(c.name,arm,'checked');
 }
}
assert.deepEqual(totals.prefix,totals.ordinary_prefix);
k.save(path.join(root,'checked.json'),{status:'pass',stage:'read_only_reconstruction',contributor:'Codex (GPT-6)',created_utc:new Date().toISOString(),counts,totals,units,diagnostic:diag.record(),new_physical_purchases:0,new_complete_acquisitions:0,limitations:'Named invoices reconstructed from saved category counters; receipt export/check counts independently recomputed. Exhaustive original-source feature oracle checks every partial box; it is diagnostic, not available to the service.'});
console.log(JSON.stringify({counts,totals},null,2));
