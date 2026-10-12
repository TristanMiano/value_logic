// Codex (GPT-6). DEVELOPMENT. Post-exposure analytic diagnostic, no new sample.
import fs from 'node:fs';import crypto from 'node:crypto';import assert from 'node:assert/strict';
import {F,add,mul,div,cmp,serial} from './rationals.mjs';
const out=process.argv[2];assert(out&&!fs.existsSync(out));const input=fs.readFileSync('censor02.json'),obj=JSON.parse(input),sum=a=>a.reduce(add,F(0));
const rows=[];for(const c of obj.cases){
 const total=c.raw_runtime_weights.reduce((a,b)=>a+b,0),law=c.raw_runtime_weights.map(x=>F(x,total));
 const w=Array.from({length:obj.H},(_,i)=>mul(F(c.c),sum(law.slice(i)))),W=w.map((_,i)=>sum(w.slice(i)));
 for(const f of c.values){
  const A=f.nested.A.map(a=>F(...a)),fails=[];for(let i=1;i<W.length;i++)if(cmp(mul(A[i],W[0]),mul(A[0],W[i]))<0)fails.push(i+1);
  rows.push({index:c.index,forecast:f.forecast,endpoint_KKT_satisfied:fails.length===0,improving_cut_locations:fails,tail_variance_per_work:A.map((a,i)=>div(a,W[i]))});
 }
}
const sources=Object.fromEntries(['rationals.mjs','censor_diag.mjs'].map(f=>[f,crypto.createHash('sha256').update(fs.readFileSync(new URL(f,import.meta.url))).digest('hex')]));
const summary=Object.fromEntries(['zero','oracle','reversed'].map(f=>[f,{cases:rows.filter(r=>r.forecast===f).length,endpoint_optimal:rows.filter(r=>r.forecast===f&&r.endpoint_KKT_satisfied).length}]));
fs.writeFileSync(out,JSON.stringify({status:'complete',evidence:'DEVELOPMENT; post-exposure analytic diagnostic',contributor:'Codex (GPT-6)',sources,input_sha256:crypto.createHash('sha256').update(input).digest('hex'),summary,rows},(_,v)=>serial(v),2)+'\n');console.log(JSON.stringify(summary));
