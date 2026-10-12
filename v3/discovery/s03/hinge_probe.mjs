// Codex (GPT-6). DEVELOPMENT. Exact dependent-law lower-score screen.
import fs from 'node:fs';import crypto from 'node:crypto';import assert from 'node:assert/strict';
import {F,add,sub,mul,div,cmp,serial} from './rationals.mjs';
import {compile,recover,value,planValue} from './hinge_tree.mjs';
import {compile as productCompile,recover as productRecover,value as productValue} from './biased_tree.mjs';
const out=process.argv[2];assert(out&&!fs.existsSync(out));const seed=31873,start=process.hrtime.bigint();let state=seed;
const rand=n=>{state^=state<<13;state^=state>>>17;state^=state<<5;return (state>>>0)%n;},eq=(a,b)=>assert(cmp(a,b)===0),sum=a=>a.reduce(add,F(0));
function margins(raw,n){const total=raw.reduce((a,b)=>a+b,0);return [F(0),...Array.from({length:n-1},(_,i)=>F(2*raw.reduce((s,w,j)=>s+(((j>>i)&1)?w:0),0),total))];}
function actual(input,raw,selected,coins){
 const n=input.parent.length,total=raw.reduce((a,b)=>a+b,0),q=new Set(selected),path=[0],load=[F(0)];let score=F(0);
 for(let v=0;v<n;v++){
  if(v){path[v]=path[input.parent[v]]|(q.has(v)?0:1<<(v-1));load[v]=add(load[input.parent[v]],q.has(v)?F(0):input.error[v]);}
  if(!coins||cmp(load[v],F(1))<0){let agreement=0;for(let world=0;world<raw.length;world++){let bits=world&path[v],parity=0;while(bits){parity^=1;bits&=bits-1;}agreement+=raw[world]*(parity?-1:1);}score=add(score,mul(input.r[v],F(agreement,total)));}
  if(q.has(v))score=sub(score,input.c[v]);
 }return score;
}
let subsetChecks=0,requestChecks=0,guaranteeChecks=0;const cases=[];
function check(input,raw,index){
 const n=input.parent.length,compiled=compile(input),p=compiled.profiles[0];let zs=[...Array.from({length:17},(_,i)=>F(i,16)),...p.map(t=>t.lo)];
 for(let i=0;i<p.length;i++)zs.push(div(add(p[i].lo,i+1<p.length?p[i+1].lo:F(1)),F(2)));zs.sort(cmp);zs=zs.filter((z,i)=>!i||cmp(z,zs[i-1])!==0);
 let previous=Array.from({length:n-1},(_,i)=>i+1),minMargin=null,productOverstatements=0;const requests=[];
 for(const z of zs){let best=null,largest=0;
  for(let mask=0;mask<2**(n-1);mask++){
   const selected=Array.from({length:n-1},(_,i)=>i+1).filter(v=>mask&(1<<(v-1))),lower=planValue(input,selected,z);subsetChecks++;
   if(best===null||cmp(lower,best)>0){best=lower;largest=mask;}else if(cmp(lower,best)===0)largest|=mask;
   if(cmp(z,F(0))===0){const score=actual(input,raw,selected,true);assert(cmp(score,lower)>=0);const margin=sub(score,lower);if(minMargin===null||cmp(margin,minMargin)<0)minMargin=margin;guaranteeChecks++;}
  }
  const selected=recover(input,compiled,z),mask=selected.reduce((m,v)=>m|(1<<(v-1)),0);eq(value(p,z),best);eq(planValue(input,selected,z),best);assert(mask===largest);assert(selected.every(v=>previous.includes(v)));previous=selected;requestChecks++;requests.push({z,value:best,selected});
 }
 const prodInput={...input,b:input.error.map(e=>sub(F(1),e))},prod=productCompile(prodInput),prodPlan=productRecover(prodInput,prod,F(1)),robustPlan=recover(input,compiled,F(0));
 const robust={plan:robustPlan,lower:value(p,F(0)),actual:actual(input,raw,robustPlan,true)},product={plan:prodPlan,model:value(prod.profiles[0],F(1)),actual:actual(input,raw,prodPlan,false)};
 return {index,input,raw_world_weights:raw,root_profile:p,pieces_by_node:compiled.profiles.map(p=>p.length),min_guarantee_margin:minMargin,requests,robust,product,product_model_exceeds_actual:cmp(product.model,product.actual)>0};
}
for(let k=0;k<32;k++){
 const n=3+rand(5),raw=Array.from({length:2**(n-1)},()=>1+rand(7)),total=raw.reduce((a,b)=>a+b,0),maxMarg=Math.max(...Array.from({length:n-1},(_,i)=>raw.reduce((s,w,j)=>s+(((j>>i)&1)?w:0),0)));raw[0]+=Math.max(0,2*maxMarg-total);
 const input={parent:Array.from({length:n},(_,v)=>v?rand(v):-1),error:margins(raw,n),c:Array.from({length:n},()=>F(rand(17),16)),r:Array.from({length:n},()=>F(1+rand(8),4))};cases.push(check(input,raw,k));
}
const raw=[0,1,1,0,1,0,0,0],example=check({parent:[-1,0,1,2],error:margins(raw,4),c:[F(0),F(2,5),F(2,5),F(2,5)],r:[F(0),F(0),F(0),F(1)]},raw,'exactly_one_error');
eq(example.robust.lower,F(0));eq(example.robust.actual,F(0));eq(example.product.model,F(1,27));eq(example.product.actual,F(-1));
const sources=Object.fromEntries(['rationals.mjs','biased_tree.mjs','hinge_tree.mjs','hinge_probe.mjs'].map(f=>[f,crypto.createHash('sha256').update(fs.readFileSync(new URL(f,import.meta.url))).digest('hex')]));
const summary={cases:cases.length,subsetChecks,requestChecks,guaranteeChecks,product_model_exceeds_actual:cases.filter(c=>c.product_model_exceeds_actual).length,example:{robust:example.robust,product:example.product}};
fs.writeFileSync(out,JSON.stringify({status:'complete',evidence:'DEVELOPMENT; finite dependent laws and exact lower objectives',contributor:'Codex (GPT-6)',node:process.version,seed,sources,summary,cases,example,elapsed_ns:Number(process.hrtime.bigint()-start)},(_,v)=>serial(v),2)+'\n');console.log(JSON.stringify(summary,(_,v)=>serial(v)));
