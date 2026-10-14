'use strict';
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict'),k=require('./retained.cjs'),sg=require('./signed.cjs');
const root=path.join(__dirname,'sc01');
function prepare(){fs.mkdirSync(root);const inputs=[],small=JSON.parse(fs.readFileSync(path.join(__dirname,'rc01','design.json'),'utf8'));for(const source of small.sources){const old=JSON.parse(fs.readFileSync(path.join(__dirname,'rc01',source.name,'result.json'),'utf8'));inputs.push({name:source.name,source,models:old.actions.at(-1).models,external:false});}
 for(let i=1;i<=8;i++){const name='uf20-0'+i;inputs.push({name,source:JSON.parse(fs.readFileSync(path.join(__dirname,'uf01',name,'source.json'),'utf8')),models:JSON.parse(fs.readFileSync(path.join(__dirname,'uf01',name,'results.json'),'utf8')).proposals.map(p=>p.model),external:true});}
 const hashes=Object.fromEntries(['sc_screen.cjs','signed.cjs','retained.cjs','complete.cjs','sc01.md'].map(f=>[f,k.sha(path.join(__dirname,f))]));k.save(path.join(root,'design.json'),{stage:'DEVELOPMENT',contributor:'Codex (GPT-6)',created_utc:new Date().toISOString(),inputs,hashes});for(const f of Object.keys(hashes))fs.copyFileSync(path.join(__dirname,f),path.join(root,f));}
function run(name){const design=JSON.parse(fs.readFileSync(path.join(root,'design.json'),'utf8'));for(const [f,h]of Object.entries(design.hashes))assert.equal(k.sha(path.join(__dirname,f)),h);const index=design.inputs.findIndex(x=>x.name===name);assert(index>=0);const input=design.inputs[index],source=input.source,out=path.join(root,name);fs.mkdirSync(out);const m=input.models.length,menus=[input.models,...input.models.map(model=>Array(m).fill(model))],diagnostic=new k.Meter(),models=input.external?null:k.enumerate(source,diagnostic),rand=k.rng(8142500+index),rows=[];
 for(const [j,menu] of menus.entries()){
  const meter=new k.Meter(),a=k.counts(source,menu,meter),q=a.map(x=>4*x-4*(m-x)),request=name+':signed'+j,bound=sg.acquire(source,q,menu[0],request,meter);k.save(path.join(out,'proof'+j+'.json'),bound);const checkMeter=new k.Meter(),checked=sg.check(source,q,bound,request,checkMeter),cert=sg.cubes(source,bound,checkMeter);assert.equal(sg.lower(cert,q,diagnostic),checked.lower);let objectiveChecks=0,boxes=0,responses=0;
  for(let trial=0;trial<32;trial++){
   const weights=a.map(()=>Math.floor(rand()*13)-6),floor=sg.lower(cert,weights,diagnostic);if(models){const optimum=Math.min(...models.map(x=>k.sum(x.v.map((v,i)=>v*weights[i]))));assert(floor<=optimum);objectiveChecks++;}
   const known=a.map(()=>rand()<.4?[-4,-2,0,2,4][Math.floor(rand()*5)]:null),lo=known.map(x=>x===null?-4:x),hi=known.map(x=>x===null?4:x),values=sg.leafBounds(cert,a,m,lo,hi,diagnostic),upper=Math.max(...values),tau=Math.max(0,upper-Math.floor(rand()*7)),induced=a.map((x,i)=>x*hi[i]+(m-x)*lo[i]);assert.equal(upper,k.sum(a.map((x,i)=>x*hi[i]))-sg.lower(cert,induced,diagnostic));
   if(models){const exact=k.sum(a.map((x,i)=>x*hi[i]))-Math.min(...models.map(x=>k.sum(x.v.map((v,i)=>v*induced[i]))));assert(upper>=exact);}
   for(let i=0;i<a.length;i++)if(known[i]===null){const interval=sg.completion(cert,a,m,lo,hi,tau,i,diagnostic);for(const t of [-4,-2,0,2,4]){const l2=lo.slice(),u2=hi.slice();l2[i]=t;u2[i]=t;assert.equal(sg.closes(interval,a,m,lo,hi,i,t),Math.max(...sg.leafBounds(cert,a,m,l2,u2,diagnostic))<=tau);responses++;}}
   boxes++;
  }
  const controls=[];function reject(label,change){let bad=structuredClone(bound);change(bad);delete bad.id;bad=k.seal(bad);assert.throws(()=>sg.check(source,q,bad,request));controls.push(label);}
  reject('constant',x=>x.normalization.constant++);reject('flip_mask',x=>x.normalization.flipMask^=1);reject('original_source',x=>x.original_source_id='wrong');reject('feature_map',x=>x.normalization.source.features.reverse());
  rows.push({action:j,models:menu,a,initial_exact_regret:4*k.sum(a)-checked.lower,certificate:cert,provider:meter.record(),check_and_compile:checkMeter.record(),objectiveChecks,boxes,responses,controls});console.log(name,j,rows.at(-1).initial_exact_regret,cert.raw_leaves,cert.cubes.length,meter.total());
 }
 k.save(path.join(out,'results.json'),{status:'pass',name,external:input.external,rows,actual_complete_calls:rows.length,physical_audits:0,diagnostic:diagnostic.record()});}
if(process.argv[2]==='prepare')prepare();else run(process.argv[2]);
