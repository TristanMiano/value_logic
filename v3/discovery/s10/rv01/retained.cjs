'use strict';
// Source-bound retained cuts. Codex (GPT-6), DEVELOPMENT, 2026-10-14.
const crypto = require('node:crypto');
const fs = require('node:fs');
const assert = require('node:assert/strict');
const VERSION = 's10-retained-v1';
function canonical(x) {
  if (Array.isArray(x)) return '[' + x.map(canonical).join(',') + ']';
  if (x && typeof x === 'object') return '{' + Object.keys(x).sort().map(k => JSON.stringify(k)+':'+canonical(x[k])).join(',') + '}';
  return JSON.stringify(x);
}
function hash(x) { return crypto.createHash('sha256').update(canonical(x)).digest('hex'); }
function seal(x) { return {...x, id:hash(x)}; }
function checkSeal(x) { const {id,...rest}=x; assert.equal(id,hash(rest),'Object binding'); }
function save(file,x) { fs.writeFileSync(file,JSON.stringify(x,null,2)+'\n'); }
function sha(file) { return crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex'); }
function sum(xs) { return xs.reduce((a,b)=>a+b,0); }
function integer(x,lo=0) { assert(Number.isSafeInteger(x) && x>=lo,'Exact bounded integer required'); }
class Meter {
  constructor(){this.units={};}
  pay(name,n=1){integer(n);this.units[name]=(this.units[name]||0)+n;integer(this.units[name]);}
  total(){return sum(Object.values(this.units));}
  record(){return {named_units:this.total(),categories:{...this.units},native_cpu_memory_and_io_prices:'unknown'};}
}
function clause(c) { return [...new Set(c)].sort((a,b)=>a-b); }
function tautology(c) { const s=new Set(c);return c.some(x=>s.has(-x)); }
function admit(source,meter=new Meter()) {
  checkSeal(source);integer(source.variables,1);assert(source.variables<=26,'Bitmask limit');
  assert(Array.isArray(source.hard)&&source.hard.length>0);
  for(const c of source.hard){assert(c.length>0);assert.deepEqual(c,clause(c));assert(!tautology(c));for(const x of c){integer(Math.abs(x),1);assert(Math.abs(x)<=source.variables);}meter.pay('source_words',c.length+1);}
  assert(source.features.length>0);assert.equal(new Set(source.features).size,source.features.length);
  for(const f of source.features){integer(f,1);assert(f<=source.variables);}
  meter.pay('source_binding',source.features.length+source.variables+8);
  return source;
}
function modelFeatures(source,mask,meter=new Meter()) {
  integer(mask);assert(mask<2**source.variables);
  for(const c of source.hard){let ok=false;for(const lit of c){meter.pay('model_literal');if(Boolean(mask&(2**(Math.abs(lit)-1)))===(lit>0))ok=true;}assert(ok,'Original hard clause false');}
  meter.pay('model_features',source.features.length);
  return source.features.map(f=>Number(Boolean(mask&(2**(f-1)))));
}
function enumerate(source,meter=new Meter()) {
  const result=[];
  for(let mask=0;mask<2**source.variables;mask++){
    let good=true;
    for(const c of source.hard){let sat=false;for(const lit of c){meter.pay('enumeration_literal');if(Boolean(mask&(2**(Math.abs(lit)-1)))===(lit>0))sat=true;}if(!sat){good=false;break;}}
    if(good){result.push({mask,v:source.features.map(f=>Number(Boolean(mask&(2**(f-1)))))});meter.pay('enumeration_feature',source.features.length);}
  }
  assert(result.length>0,'Unsatisfiable source has no requested action');return result;
}
function resolve(a,b,pivot) {
  if(a.includes(pivot)&&b.includes(-pivot))return clause([...a.filter(x=>x!==pivot),...b.filter(x=>x!==-pivot)]);
  if(a.includes(-pivot)&&b.includes(pivot))return clause([...a.filter(x=>x!==-pivot),...b.filter(x=>x!==pivot)]);
  throw new Error('Resolution pivot absent');
}
function extract(source,meter=new Meter(),caps={width:4,derived:256,candidates:50000}) {
  admit(source,meter);const all=source.hard.map(c=>[...c]);const known=new Set(all.map(canonical));const steps=[];
  let examined=0,stopped=null;
  outer:for(let right=0;right<all.length;right++)for(let left=0;left<right;left++){
    for(const signed of all[left]){
      if(!all[right].includes(-signed))continue;
      if(examined>=caps.candidates){stopped='candidate_cap';break outer;}
      examined++;meter.pay('resolution_candidate',all[left].length+all[right].length+3);
      const pivot=Math.abs(signed),out=resolve(all[left],all[right],pivot);
      if(out.length===0||out.length>caps.width||tautology(out)||known.has(canonical(out)))continue;
      if(steps.length>=caps.derived){stopped='derived_cap';break outer;}
      known.add(canonical(out));all.push(out);steps.push({left,right,pivot,out});meter.pay('resolution_emit',out.length+3);
    }
  }
  const map=new Map(source.features.map((v,i)=>[v,i]));const cuts=[];
  all.forEach((c,index)=>{meter.pay('cover_scan',c.length);if(c.length&&c.every(v=>map.has(v)))cuts.push({clause:index,features:c.map(v=>map.get(v)).sort((a,b)=>a-b),rhs:1});});
  return seal({version:VERSION,source_id:source.id,feature_map:[...source.features],steps,cuts,caps,examined,stopped});
}
function checkExtraction(source,receipt,meter=new Meter()) {
  admit(source,meter);checkSeal(receipt);assert.equal(receipt.source_id,source.id);assert.deepEqual(receipt.feature_map,source.features);
  const all=source.hard.map(c=>[...c]);
  for(const s of receipt.steps){integer(s.left);integer(s.right);integer(s.pivot,1);assert(s.left<all.length&&s.right<all.length);const c=resolve(all[s.left],all[s.right],s.pivot);assert(!tautology(c)&&c.length>0);assert.deepEqual(c,s.out);meter.pay('resolution_check',2*(all[s.left].length+all[s.right].length)+s.out.length+6);all.push(c);}
  const map=new Map(source.features.map((v,i)=>[v,i]));
  for(const c of receipt.cuts){integer(c.clause);assert(c.clause<all.length);assert.equal(c.rhs,1);assert(all[c.clause].every(v=>map.has(v)));assert.deepEqual(c.features,all[c.clause].map(v=>map.get(v)).sort((a,b)=>a-b));meter.pay('cover_check',c.features.length+4);}
  meter.pay('extraction_retention_words',sum(receipt.steps.map(s=>s.out.length+3))+sum(receipt.cuts.map(c=>c.features.length+2))+8);
  return receipt.cuts;
}
function packing(cuts,q,meter=new Meter()) {
  const remaining=[...q],lambda=cuts.map(()=>0);
  const order=cuts.map((c,i)=>i).sort((i,j)=>cuts[i].features.length-cuts[j].features.length||i-j);
  meter.pay('packing_order',cuts.length*Math.max(1,Math.ceil(Math.log2(cuts.length+1))));
  for(const i of order){const c=cuts[i];let value=Math.min(...c.features.map(f=>remaining[f]));lambda[i]=value;for(const f of c.features)remaining[f]-=value;meter.pay('packing_update',2*c.features.length+2);}
  return lambda;
}
function dual(source,receipt,lambda,meter=new Meter()) {
  const cuts=checkExtraction(source,receipt,meter);assert.equal(lambda.length,cuts.length);const b=source.features.map(()=>0);let K=0;
  lambda.forEach((x,i)=>{integer(x);K+=x;for(const f of cuts[i].features)b[f]+=x;meter.pay('dual_combination',2*cuts[i].features.length+2);});
  b.forEach(x=>integer(x));integer(K);meter.pay('dual_retention_words',b.length+lambda.length+6);
  return seal({version:VERSION,source_id:source.id,extraction_id:receipt.id,lambda:[...lambda],b,K});
}
function counts(source,models,meter=new Meter()) {
  assert(models.length>0);const a=source.features.map(()=>0);for(const mask of models){const v=modelFeatures(source,mask,meter);v.forEach((x,i)=>a[i]+=x);}return a;
}
function bounds(cert,a,m,lo,hi,meter=new Meter()) {
  assert(a.length===cert.b.length&&a.length===lo.length&&a.length===hi.length);integer(m,1);
  let value=-cert.K;const h=[],q=[];
  for(let i=0;i<a.length;i++){integer(a[i]);assert(a[i]<=m);integer(lo[i]);integer(hi[i]);assert(lo[i]<=hi[i]);q.push(a[i]*hi[i]+(m-a[i])*lo[i]);h.push(Math.max(a[i]*hi[i],cert.b[i]-(m-a[i])*lo[i]));value+=h[i];meter.pay('bound_coordinate',8);}
  integer(value);return {raw:value,upper:Math.min(value,sum(a.map((x,i)=>x*hi[i]))),h,q};
}
function auditScore(cert,a,m,lo,hi,i,t,meter=new Meter()) {
  integer(i);assert(i<a.length);integer(t);assert(lo[i]<=t&&t<=hi[i],'Receipt outside admitted box');
  const prior=Math.max(a[i]*hi[i],cert.b[i]-(m-a[i])*lo[i]);
  const after=Math.max(a[i]*t,cert.b[i]-(m-a[i])*t);meter.pay('audit_score',9);assert(prior>=after);return prior-after;
}
function convolve(supports,scores,quota,meter=new Meter()) {
  integer(quota);assert(quota<=10000,'Prospective convolution cap');let dist=new Map([[0,1n]]),den=1n;
  for(let i=0;i<supports.length;i++){
    assert(supports[i].length===scores[i].length&&scores[i].length>0);const next=new Map();
    for(const [s,w] of dist)for(const d of scores[i]){integer(d);const t=Math.min(quota,s+d);next.set(t,(next.get(t)||0n)+w);meter.pay('convolution_transition',4);}
    dist=next;den*=BigInt(scores[i].length);
  }
  return {num:dist.get(quota)||0n,den,states:dist.size};
}
function rng(seed){let state=seed>>>0;return ()=>{state=(Math.imul(1664525,state)+1013904223)>>>0;return state/4294967296;};}
function product(arrays,fn,i=0,prefix=[]){if(i===arrays.length)return fn(prefix);for(const v of arrays[i])product(arrays,fn,i+1,[...prefix,v]);}
function source(name,n,hard,features=Array.from({length:n},(_,i)=>i+1)) {return seal({name,variables:n,features,hard:hard.map(clause)});}
module.exports={VERSION,canonical,hash,seal,checkSeal,save,sha,sum,integer,Meter,admit,modelFeatures,enumerate,resolve,extract,checkExtraction,packing,dual,counts,bounds,auditScore,convolve,rng,product,source};
