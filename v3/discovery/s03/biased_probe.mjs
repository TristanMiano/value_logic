// Codex (GPT-6). DEVELOPMENT. Exact profiles and source-conditional decisions.
import fs from 'node:fs';import crypto from 'node:crypto';import assert from 'node:assert/strict';
import {F,add,sub,mul,div,cmp,max,serial} from './rationals.mjs';
import {compile,recover,value,planValue} from './biased_tree.mjs';
const out=process.argv[2];assert(out&&!fs.existsSync(out));const seed=77149,start=process.hrtime.bigint();let state=seed;
const rand=n=>{state^=state<<13;state^=state>>>17;state^=state<<5;return (state>>>0)%n;};
const eq=(a,b)=>assert(cmp(a,b)===0),sum=a=>a.reduce(add,F(0)),abs=a=>cmp(a,F(0))<0?mul(F(-1),a):a;
function source(n,shape){return {parent:Array.from({length:n},(_,v)=>v?(shape==='path'?v-1:shape==='star'?0:shape==='binary'?(v-1)>>1:rand(v)):-1),b:Array.from({length:n},()=>F(rand(5),4)),c:Array.from({length:n},()=>F(rand(17),16)),r:Array.from({length:n},()=>F(1+rand(16),8))};}
function bellman(input){
 const n=input.parent.length,m=n-1,weights=[],spin=[];
 for(let world=0;world<2**m;world++){
  let p=F(1);const s=[1];for(let v=1;v<n;v++){const bit=(world>>(v-1))&1,e=bit?-1:1;s[v]=s[input.parent[v]]*e;p=mul(p,div(add(F(1),mul(F(e),input.b[v])),F(2)));}weights.push(p);spin.push(s);
 }
 const cache=new Map();let states=0;
 function go(mask,bits){
  const key=mask+','+bits;if(cache.has(key))return cache.get(key);states++;
  const worlds=weights.map((p,w)=>({p,w})).filter(z=>(z.w&mask)===bits&&cmp(z.p,F(0))>0),mass=sum(worlds.map(z=>z.p));
  let best=sum(input.r.map((r,v)=>mul(r,div(abs(sum(worlds.map(z=>mul(z.p,F(spin[z.w][v]))))),mass))));
  for(let i=0;i<m;i++)if(!(mask&(1<<i))){let score=mul(F(-1),input.c[i+1]);for(let bit=0;bit<2;bit++){
   const p=sum(worlds.filter(z=>((z.w>>i)&1)===bit).map(z=>z.p));if(cmp(p,F(0))>0)score=add(score,mul(div(p,mass),go(mask|(1<<i),bits|(bit<<i))));
  }best=max(best,score);}cache.set(key,best);return best;
 }
 return {value:go(0,0),states};
}
const cases=[];let subsetChecks=0,requestChecks=0,bellmanStates=0;
for(let k=0;k<28;k++){
 const n=2+rand(7),input=source(n,'random'),compiled=compile(input),p=compiled.profiles[0];
 let xs=[...Array.from({length:17},(_,i)=>F(i,16)),...p.map(t=>t.lo)];for(let i=0;i<p.length;i++)xs.push(div(add(p[i].lo,i+1<p.length?p[i+1].lo:F(1)),F(2)));
 xs.sort(cmp);xs=xs.filter((x,i)=>!i||cmp(x,xs[i-1])!==0);let previous=[];const requests=[];
 for(const x of xs){
  let best=null,largest=0;for(let mask=0;mask<2**(n-1);mask++){
   const selected=Array.from({length:n-1},(_,i)=>i+1).filter(v=>mask&(1<<(v-1))),v=planValue(input,selected,x);subsetChecks++;
   if(best===null||cmp(v,best)>0){best=v;largest=mask;}else if(cmp(v,best)===0)largest|=mask;
  }
  const selected=recover(input,compiled,x);eq(value(p,x),best);eq(planValue(input,selected,x),best);
  const mask=selected.reduce((m,v)=>m|(1<<(v-1)),0);assert(mask===largest);assert(previous.every(v=>selected.includes(v)));previous=selected;requestChecks++;requests.push({x,value:best,selected});
 }
 let full=null;if(k<10){full=bellman(input);eq(full.value,value(p,F(1)));bellmanStates+=full.states;}
 cases.push({index:k,input,profile:p,pieces_by_node:compiled.profiles.map(p=>p.length),requests,bellman:full});
}
const large=[];for(const shape of ['path','star','binary']){
 const t0=process.hrtime.bigint(),input=source(256,shape),t1=process.hrtime.bigint(),compiled=compile(input),t2=process.hrtime.bigint();
 const xs=Array.from({length:128},(_,i)=>F(i+1,128));let checksum=F(0);for(const x of xs)checksum=add(checksum,value(compiled.profiles[0],x));const t3=process.hrtime.bigint();
 const plans=xs.map(x=>recover(input,compiled,x)),t4=process.hrtime.bigint();for(let i=0;i<xs.length;i++)eq(planValue(input,plans[i],xs[i]),value(compiled.profiles[0],xs[i]));const t5=process.hrtime.bigint();
 let coldChecksum=F(0);for(const x of xs)coldChecksum=add(coldChecksum,value(compile(input).profiles[0],x));const t6=process.hrtime.bigint();eq(checksum,coldChecksum);
 large.push({shape,n:256,input,root_profile:compiled.profiles[0],total_pieces:compiled.profiles.reduce((s,p)=>s+p.length,0),source_ns:Number(t1-t0),compile_ns:Number(t2-t1),value_queries_ns:Number(t3-t2),plan_recovery_ns:Number(t4-t3),plan_check_ns:Number(t5-t4),cold_profiles_ns:Number(t6-t5),checksum,selected_counts:plans.map(p=>p.length)});
}
const sources=Object.fromEntries(['rationals.mjs','biased_tree.mjs','biased_probe.mjs'].map(f=>[f,crypto.createHash('sha256').update(fs.readFileSync(new URL(f,import.meta.url))).digest('hex')]));
const summary={cases:cases.length,subsetChecks,requestChecks,bellmanStates,large:large.map(x=>({shape:x.shape,root_pieces:x.root_profile.length,total_pieces:x.total_pieces,compile_ms:x.compile_ns/1e6,value_queries_ms:x.value_queries_ns/1e6,plan_recovery_ms:x.plan_recovery_ns/1e6,plan_check_ms:x.plan_check_ns/1e6,cold_profiles_ms:x.cold_profiles_ns/1e6}))};
fs.writeFileSync(out,JSON.stringify({status:'complete',evidence:'DEVELOPMENT',contributor:'Codex (GPT-6)',node:process.version,seed,sources,summary,cases,large,elapsed_ns:Number(process.hrtime.bigint()-start)},(_,v)=>serial(v),2)+'\n');console.log(JSON.stringify(summary));
