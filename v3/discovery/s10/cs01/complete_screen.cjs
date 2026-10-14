'use strict';
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict'),k=require('./retained.cjs'),complete=require('./complete.cjs');
const root=path.join(__dirname,'cs01');fs.mkdirSync(root);for(const f of ['complete.cjs','complete_screen.cjs','retained.cjs'])fs.copyFileSync(path.join(__dirname,f),path.join(root,f));
const design=JSON.parse(fs.readFileSync(path.join(__dirname,'rc01','design.json'),'utf8'));
k.save(path.join(root,'design.json'),{stage:'DEVELOPMENT',contributor:'Codex (GPT-6)',time_utc:new Date().toISOString(),sources:design.sources.map(s=>s.id),weights:'four seeded integral objectives in 0..4 for every source',seed:8142200,purpose:'independently checked actual complete proof provider versus finite enumeration',paid_service:false});
const rows=[];for(const [si,s] of design.sources.entries()){
 const diag=new k.Meter(),models=k.enumerate(s,diag),rand=k.rng(8142200+si);
 for(let j=0;j<4;j++){const w=s.features.map(()=>Math.floor(rand()*5)),request=s.name+'_'+j,meter=new k.Meter(),receipt=complete.acquire(s,w,models[0].mask,request,meter),checker=new k.Meter(),checked=complete.check(s,w,receipt,request,checker),actual=Math.min(...models.map(x=>k.sum(x.v.map((v,i)=>v*w[i]))));assert.equal(checked.optimum,actual);
 const controls=[];function reject(label,fn){assert.throws(fn);controls.push(label);}reject('request',()=>complete.check(s,w,receipt,request+'x'));reject('objective',()=>complete.check(s,w.map((x,i)=>i?x:x+1),receipt,request));let bad=structuredClone(receipt);bad.budget=bad.lower;delete bad.id;bad=k.seal(bad);reject('lower_budget',()=>complete.check(s,w,bad,request));let broken=structuredClone(receipt);broken.proof=['bound'];broken.proof_nodes=1;broken.lower=0;broken.budget=-1;broken.model=0;delete broken.id;broken=k.seal(broken);if(checked.optimum>0||!models.some(x=>x.mask===0))reject('bad_witness',()=>complete.check(s,w,broken,request));
 k.save(path.join(root,request+'.json'),receipt);rows.push({request,optimum:actual,provider_units:meter.total(),check_units:checker.total(),controls,proof_nodes:receipt.proof_nodes});}
 console.log(s.name,'checked');
}k.save(path.join(root,'results.json'),{status:'pass',rows,actual_complete_proofs:rows.length,physical_audits:0});
