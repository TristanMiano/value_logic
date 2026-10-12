// Codex (GPT-6). DEVELOPMENT. Post-exposure two-level design proposals.
import fs from 'node:fs';import crypto from 'node:crypto';import assert from 'node:assert/strict';
import {F,add,sub,mul,div,cmp,serial} from './rationals.mjs';
const out=process.argv[2];assert(out&&!fs.existsSync(out));const input=fs.readFileSync('censor02.json'),obj=JSON.parse(input),H=obj.H,D=65536;
const sum=a=>a.reduce(add,F(0)),num=a=>Number(a[0])/Number(a[1]),sq=a=>mul(a,a),eq=(a,b)=>assert(cmp(a,b)===0),grid=a=>F((a[0]*BigInt(D))/a[1],D);
const rows=[];let proposalCount=0;
for(const c of obj.cases){
 const total=c.raw_runtime_weights.reduce((a,b)=>a+b,0),law=c.raw_runtime_weights.map(x=>F(x,total)),w=Array.from({length:H},(_,i)=>mul(F(c.c),sum(law.slice(i)))),W=w.map((_,i)=>sum(w.slice(i))),K=F(...c.work),r=F(...c.endpoint_rate);
 const increments=Array.from({length:H+1},(_,t)=>Array.from({length:H},(_,i)=>F(i>t?0:i===t?c.V-c.c:-c.c))),m=Array.from({length:H},(_,i)=>sum(increments.map((v,t)=>mul(law[t],v[i]))));
 for(const f of c.values){
  const A=f.nested.A.map(v=>F(...v)),intrinsic=F(...f.nested.intrinsic),endpoint=F(...f.endpoint_variance),b=f.forecast==='zero'?Array.from({length:H},()=>F(0)):f.forecast==='oracle'?m:m.map(v=>mul(F(-1),v));
  let best={cut:1,x:r,y:r,work:K,variance:endpoint};const proposals=[];
  for(let l=1;l<H;l++){
   if(cmp(mul(A[l],W[0]),mul(A[0],W[l]))>=0)continue;
   const wp=sub(W[0],W[l]),wt=W[l],a=sub(A[0],A[l]),bt=A[l];if(cmp(bt,F(0))===0)continue;
   const scale=Math.sqrt(num(mul(a,wp)))+Math.sqrt(num(mul(bt,wt))),xp=Math.min(1,num(K)*Math.sqrt(num(div(a,wp)))/scale),x=F(Math.floor(D*xp),D);
   const allowable=grid(div(sub(K,mul(wp,x)),wt)),y=cmp(allowable,x)<0?allowable:x;if(cmp(y,F(0))<=0)continue;
   const work=add(mul(wp,x),mul(wt,y));assert(cmp(work,K)<=0);assert(cmp(x,F(1))<=0&&cmp(y,x)<=0);
   const variance=add(intrinsic,sub(add(div(a,x),div(bt,y)),A[0])),p={cut:l+1,x,y,work,variance};proposals.push(p);proposalCount++;
   if(cmp(variance,best.variance)<0)best=p;
  }
  const q=Array.from({length:H},(_,i)=>i<best.cut-1?best.x:best.y),cap=[sub(F(1),q[0]),...q.slice(0,-1).map((v,i)=>sub(v,q[i+1])),q[H-1]];
  let mean=F(0),second=F(0);for(let t=0;t<=H;t++)for(let C=0;C<=H;C++){
   let z=sum(b);for(let i=0;i<C;i++)z=add(z,div(sub(increments[t][i],b[i]),q[i]));const p=mul(law[t],cap[C]);mean=add(mean,mul(p,z));second=add(second,mul(p,sq(z)));
  }
  eq(sub(second,sq(mean)),best.variance);eq(mean,F(...f.nested.mu));
  rows.push({index:c.index,forecast:f.forecast,work_budget:K,endpoint_variance:endpoint,selected:best,variance_ratio:num(div(best.variance,endpoint)),proposals});
 }
}
const sources=Object.fromEntries(['rationals.mjs','censor_repair.mjs'].map(f=>[f,crypto.createHash('sha256').update(fs.readFileSync(new URL(f,import.meta.url))).digest('hex')]));
const summary=Object.fromEntries(['zero','oracle','reversed'].map(f=>{const r=rows.filter(x=>x.forecast===f);return [f,{cases:r.length,improved:r.filter(x=>cmp(x.selected.variance,x.endpoint_variance)<0).length,min_variance_ratio:Math.min(...r.map(x=>x.variance_ratio)),mean_variance_ratio:r.reduce((s,x)=>s+x.variance_ratio,0)/r.length}];}));
fs.writeFileSync(out,JSON.stringify({status:'complete',evidence:'DEVELOPMENT; post-exposure supplied-law repair',contributor:'Codex (GPT-6)',sources,input_sha256:crypto.createHash('sha256').update(input).digest('hex'),D,proposalCount,summary,rows},(_,v)=>serial(v),2)+'\n');console.log(JSON.stringify({proposalCount,summary}));
