// Codex (GPT-6). DEVELOPMENT. Exact supplied latent mixtures and receipt values.
import fs from 'node:fs';import crypto from 'node:crypto';import assert from 'node:assert/strict';
import {F,add,sub,mul,div,cmp,max,serial} from './rationals.mjs';
const out=process.argv[2];assert(out&&!fs.existsSync(out));const seed=53219,start=process.hrtime.bigint();let state=seed;
const rand=n=>{state^=state<<13;state^=state>>>17;state^=state<<5;return (state>>>0)%n;};
const sum=a=>a.reduce(add,F(0));const eq=(a,b)=>assert(cmp(a,b)===0);
function analyse(raw,V,c,H){
  const total=raw.reduce((a,b)=>a+b,0),prob=raw.map((_,i)=>F(i,4));let posterior=raw.map(w=>F(w,total)),spent=F(0),cutoff=null;
  const survival=[],hazards=[],values=[],variance=[];let identityChecks=0;
  for(let k=0;k<=H;k++){
    const s=sum(posterior);survival.push(s);values.push(sub(mul(F(V),sub(F(1),s)),mul(F(c),spent)));
    if(cmp(s,F(0))===0){hazards.push(null);variance.push(null);if(cutoff===null)cutoff=k;}
    else{
      const h=div(sum(posterior.map((w,i)=>mul(w,prob[i]))),s),second=div(sum(posterior.map((w,i)=>mul(w,mul(prob[i],prob[i])))),s),v=sub(second,mul(h,h));
      hazards.push(h);variance.push(v);if(cutoff===null&&cmp(mul(F(V),h),F(c))<=0)cutoff=k;
    }
    spent=add(spent,s);posterior=posterior.map((w,i)=>mul(w,sub(F(1),prob[i])));
  }
  if(cutoff===null)cutoff=H;cutoff=Math.min(cutoff,H);
  for(let k=0;k<H;k++)if(hazards[k]!==null&&hazards[k+1]!==null){
    eq(hazards[k+1],sub(hazards[k],div(variance[k],sub(F(1),hazards[k]))));assert(cmp(hazards[k+1],hazards[k])<=0);identityChecks++;
  }
  const optimal=values.reduce(max,F(0));eq(values[cutoff],optimal);
  let reconstructed=F(1);eq(reconstructed,survival[0]);
  for(let k=0;k<H;k++){reconstructed=sub(mul(sub(F(1),F(c,V)),reconstructed),div(sub(values[k+1],values[k]),F(V)));eq(reconstructed,survival[k+1]);}
  return {raw,V,c,H,survival,hazards,variance,values,cutoff,optimal,identityChecks};
}
const cases=[];for(let k=0;k<24;k++){const raw=Array.from({length:5},()=>rand(8));raw[rand(5)]+=1;cases.push(analyse(raw,1+rand(64),1+rand(15),16));}
const constant=analyse([0,0,2,0,0],10,2,6),mixture=analyse([1,0,0,0,1],10,2,6);
eq(constant.values[1],mixture.values[1]);eq(constant.hazards[1],F(1,2));eq(mixture.hazards[1],F(0));assert(constant.cutoff===6&&mixture.cutoff===1);
const sources={};for(const name of ['rationals.mjs','retry_probe.mjs'])sources[name]=crypto.createHash('sha256').update(fs.readFileSync(new URL(name,import.meta.url))).digest('hex');
const result={status:'complete',evidence:'DEVELOPMENT',contributor:'Codex (GPT-6)',node:process.version,seed,sources,cases,counterexample:{constant,mixture,pooled_effective_cost:F(4),mixture_expected_completion_cost:'infinite'},elapsed_ns:Number(process.hrtime.bigint()-start),limits:'Supplied latent mixtures and fixed receipt payoff. No source learning, general runtime-hazard claim or per-instance statistical validity inferred.'};
fs.writeFileSync(out,JSON.stringify(result,(_,x)=>serial(x),2)+'\n');console.log(JSON.stringify({status:result.status,cases:cases.length,identityChecks:cases.reduce((a,c)=>a+c.identityChecks,0),reconstructionChecks:cases.length*17,cutoffs:cases.map(c=>c.cutoff),counterexampleCutoffs:[constant.cutoff,mixture.cutoff],elapsed_ns:result.elapsed_ns}));
