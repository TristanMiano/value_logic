'use strict';
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const k=require('./retained.cjs'),p=require('./prefix.cjs');
const root=path.join(__dirname,'rc02');
if(process.argv[2]==='prepare'){
 fs.mkdirSync(root);const cases=[];for(const name of fs.readdirSync(path.join(__dirname,'rc01'))){const f=path.join(__dirname,'rc01',name,'result.json');if(!fs.existsSync(f))continue;const r=JSON.parse(fs.readFileSync(f,'utf8')),a=r.actions.at(-1);for(const quota of [2,6])cases.push({name:name+'_q'+quota,source:name,action:a,quota,skipped:quota>a.initial_bound});}
 k.save(path.join(root,'design.json'),{created_utc:new Date().toISOString(),stage:'DEVELOPMENT',contributor:'Codex (GPT-6)',cases,hashes:Object.fromEntries(['retained.cjs','prefix.cjs','rc02.cjs','rc02.md'].map(f=>[f,k.sha(path.join(__dirname,f))]))});for(const f of ['retained.cjs','prefix.cjs','rc02.cjs','rc02.md'])fs.copyFileSync(path.join(__dirname,f),path.join(root,f));
}else{
 const design=JSON.parse(fs.readFileSync(path.join(root,'design.json'),'utf8'));for(const [f,h] of Object.entries(design.hashes))assert.equal(k.sha(path.join(__dirname,f)),h);
 const rows=[];for(const c of design.cases){if(c.skipped){rows.push({name:c.name,skipped:'Quota exceeds initial bound'});continue;}
 const meter=new k.Meter(),diagnostic=new k.Meter(),a=c.action.a,m=c.action.m,n=a.length,cert=c.action.certificate,lo=a.map(()=>0),hi=a.map(()=>4),fees=a.map((_,i)=>1+i%3),C=Math.ceil(.75*k.sum(fees));
 const scores=a.map((_,i)=>[0,2,4].map(t=>k.auditScore(cert,a,m,lo,hi,i,t,meter))),plan=p.compile(scores,fees,c.quota,C,C,meter);
 let worlds=0,fee=0,finished=0,worst=0;const first=p.orders(scores,fees,diagnostic)[0],greedy=[];let budget=0;for(const i of first){if(budget+fees[i]>C)break;budget+=fees[i];greedy.push(i);}let greedyFee=0;
 k.product(a.map(()=>[0,1,2]),world=>{const r=p.evaluate(plan,fees,scores,world,diagnostic);fee+=r.fee;finished+=Number(!r.fallback);worst=Math.max(worst,r.fee);worlds++;greedyFee+=p.evaluate({...plan,sequence:greedy},fees,scores,world,diagnostic).fee;});
 assert.equal(BigInt(fee)*plan.expected.den,BigInt(worlds)*plan.expected.num);assert(plan.expected.num<=BigInt(C)*plan.expected.den);
 const row={name:c.name,n,quota:c.quota,C,fees,scores,plan:p.serial(plan),worlds,total_fee:fee,expected_fee:fee/worlds,anchor_expected_fee:C,greedy_expected_fee:greedyFee/worlds,completion_probability:finished/worlds,worst,compiler:meter.record(),diagnostic:diagnostic.record()};rows.push(row);console.log(c.name,(100*(C-fee/worlds)/C).toFixed(2)+'%',plan.sequence.join(','),meter.total());
 }k.save(path.join(root,'results.json'),{status:'pass',created_utc:new Date().toISOString(),rows,physical_audits:0});
}
