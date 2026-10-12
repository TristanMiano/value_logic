// Codex (GPT-6). DEVELOPMENT. Exact finite nested-truncation screen.
import fs from 'node:fs';import crypto from 'node:crypto';import assert from 'node:assert/strict';
import {F,add,sub,mul,div,cmp,serial} from './rationals.mjs';
const out=process.argv[2];assert(out&&!fs.existsSync(out));const seed=61357,H=6,start=process.hrtime.bigint();let state=seed;
const rand=n=>{state^=state<<13;state^=state>>>17;state^=state<<5;return (state>>>0)%n;};
const sum=a=>a.reduce(add,F(0)),sq=a=>mul(a,a),eq=(a,b)=>assert(cmp(a,b)===0);
const norm=a=>{const z=a.reduce((a,b)=>a+b,0);return a.map(x=>F(x,z));};
let conditionalChecks=0,contrastChecks=0,calibrationChecks=0;
function evaluate(D,law,cap,b,coeff){
 const h=b.length,q=Array.from({length:h},(_,i)=>sum(cap.slice(i+1))),lambda=q.map((q,i)=>sub(div(F(1),q),i?div(F(1),sum(cap.slice(i))):F(1)));
 const g=D.map(d=>sum(d.map((v,i)=>mul(v,coeff[i])))),mu=sum(g.map((v,t)=>mul(v,law[t]))),base=sum(b.map((v,i)=>mul(v,coeff[i])));
 const A=Array.from({length:h},()=>F(0));let second=F(0),extra=F(0);
 for(let t=0;t<D.length;t++){
  let mean=F(0),m2=F(0);
  for(let C=0;C<=h;C++){
   let z=base;for(let i=0;i<C;i++)z=add(z,div(mul(sub(D[t][i],b[i]),coeff[i]),q[i]));
   mean=add(mean,mul(cap[C],z));m2=add(m2,mul(cap[C],sq(z)));
  }
  eq(mean,g[t]);let predicted=F(0),tail=F(0);
  for(let i=h-1;i>=0;i--){tail=add(tail,mul(sub(D[t][i],b[i]),coeff[i]));const a=sq(tail);A[i]=add(A[i],mul(law[t],a));predicted=add(predicted,mul(lambda[i],a));}
  eq(sub(m2,sq(mean)),predicted);conditionalChecks++;second=add(second,mul(law[t],m2));extra=add(extra,mul(law[t],predicted));
 }
 const intrinsic=sub(sum(g.map((v,t)=>mul(law[t],sq(v)))),sq(mu)),variance=sub(second,sq(mu));eq(variance,add(intrinsic,extra));
 return {mu,variance,intrinsic,extra,A,q,lambda};
}
const cases=[];let nonmonotone=0,nestedWins=0,nestedLosses=0;
for(let k=0;k<24;k++){
 const raw=Array.from({length:H+1},()=>1+rand(9)),caps=Array.from({length:H+1},()=>1+rand(7)),law=norm(raw),cap=norm(caps),V=4+rand(17),c=1+rand(4);
 const D=Array.from({length:H+1},(_,t)=>Array.from({length:H},(_,i)=>F(i>t?0:(i===t?V-c:-c))));
 const m=Array.from({length:H},(_,i)=>sum(D.map((d,t)=>mul(law[t],d[i])))),coeff=Array.from({length:H},()=>F(1));
 const q=Array.from({length:H},(_,i)=>sum(cap.slice(i+1))),survival=Array.from({length:H},(_,i)=>sum(law.slice(i)));
 const work=sum(q.map((v,i)=>mul(F(c),mul(v,survival[i])))),fullWork=mul(F(c),sum(survival)),rate=div(work,fullWork);
 let directWork=F(0);for(let t=0;t<=H;t++)for(let C=0;C<=H;C++)directWork=add(directWork,mul(mul(law[t],cap[C]),F(c*Math.min(t+1,C))));eq(work,directWork);
 const endpoint=Array.from({length:H+1},()=>F(0));endpoint[0]=sub(F(1),rate);endpoint[H]=rate;
 const forecasts=[Array.from({length:H},()=>F(0)),m,m.map(v=>mul(F(-1),v))],values=[];
 const oracle=evaluate(D,law,cap,m,coeff);
 for(let j=0;j<forecasts.length;j++){
  const b=forecasts[j],v=evaluate(D,law,cap,b,coeff),e=evaluate(D,law,endpoint,b,coeff);
  let bias=F(0),tail=F(0);for(let i=H-1;i>=0;i--){tail=add(tail,sub(m[i],b[i]));bias=add(bias,mul(v.lambda[i],sq(tail)));}eq(sub(v.extra,oracle.extra),bias);calibrationChecks++;
  for(let i=0;i<H-1;i++)if(cmp(v.A[i],v.A[i+1])<0)nonmonotone++;
  const sign=cmp(v.variance,e.variance);if(sign<0)nestedWins++;if(sign>0)nestedLosses++;
  for(let a=0;a<=H;a++)for(let bcap=0;bcap<=H;bcap++){
   const d=Array.from({length:H},(_,i)=>F(Number(i<a)-Number(i<bcap)));evaluate(D,law,cap,b,d);contrastChecks++;
  }
  values.push({forecast:['zero','oracle','reversed'][j],nested:v,endpoint_variance:e.variance,comparison:sign<0?'nested_lower':sign>0?'endpoint_lower':'equal'});
 }
 cases.push({index:k,raw_runtime_weights:raw,raw_cap_weights:caps,V,c,work,fullWork,endpoint_rate:rate,values});
}
const negative=evaluate([[F(-1),F(1)]],[F(1)],[F(1,4),F(1,4),F(1,2)],[F(0),F(0)],[F(1),F(1)]);eq(negative.A[0],F(0));eq(negative.A[1],F(1));eq(negative.extra,F(2,3));
const sources=Object.fromEntries(['rationals.mjs','censor_probe.mjs','censor_probe_v2.mjs'].map(f=>[f,crypto.createHash('sha256').update(fs.readFileSync(new URL(f,import.meta.url))).digest('hex')]));
const result={status:'complete',evidence:'DEVELOPMENT; exact finite supplied-law screen',contributor:'Codex (GPT-6)',node:process.version,seed,H,sources,summary:{cases:cases.length,conditionalChecks,contrastChecks,calibrationChecks,nonmonotone_tail_pairs:nonmonotone,nestedWins,nestedLosses},negative_tail_example:negative,cases,elapsed_ms:Number(process.hrtime.bigint()-start)/1e6};
fs.writeFileSync(out,JSON.stringify(result,(_,v)=>serial(v),2)+'\n');console.log(JSON.stringify(result.summary));
