import fs from 'node:fs';import crypto from 'node:crypto';import assert from 'node:assert/strict';
import {F,add,sub,mul,cmp,max,serial} from './rationals.mjs';import {macro,compile,policy} from './capped_tree.mjs';
const out=process.argv[2];assert(out&&!fs.existsSync(out));const seed=92741,start=process.hrtime.bigint();let state=seed;
const rand=n=>{state^=state<<13;state^=state>>>17;state^=state<<5;return (state>>>0)%n;};
function exactValue(prizes,anchors,edges,root,bits){
  if(root<0)return F(0);const adj=Array.from({length:prizes.length},()=>[]);edges.forEach(([u,v],j)=>{if((bits>>j)&1){adj[u].push([v,j]);adj[v].push([u,j]);}});
  const parent=Array(prizes.length).fill(null),order=[root];parent[root]=-1;
  for(const v of order)for(const [u] of adj[v])if(u!==parent[v]){parent[u]=v;order.push(u);}
  const values=Array(prizes.length);for(const v of order.toReversed()){
    let value=F(prizes[v]);for(const [u,j] of adj[v])if(parent[u]===v){const m=macro(edges[j][2]);value=add(value,sub(mul(F(m.a,m.d),values[u]),F(m.b,m.d)));}values[v]=value;
  }const a=macro(anchors[root]);return sub(mul(F(a.a,a.d),values[root]),F(a.b,a.d));
}
const cases=[];let enumerations=0;
for(let k=0;k<32;k++){
  const n=2+rand(6),prizes=Array.from({length:n},()=>1+rand(20)),make=()=>({p4:1+rand(4),k:1+rand(4),c:rand(12)}),anchors=Array.from({length:n},()=>rand(4)===0?null:make()),edges=Array.from({length:n-1},(_,i)=>[rand(i+1),i+1,make()]);
  const D=k%2===0?1000n:1000000000n,plan=compile(prizes,anchors,edges,D),chosen=policy(plan);let overall=F(0);const roots=[];
  for(let root=0;root<n;root++){
    let best=F(0);if(anchors[root]!==null)for(let bits=0;bits<(1<<edges.length);bits++){best=max(best,exactValue(prizes,anchors,edges,root,bits));enumerations++;}
    assert(cmp(F(plan.scores[root][0],D),best)<=0&&cmp(best,F(plan.scores[root][1],D))<=0);overall=max(overall,best);roots.push(best);
  }
  const bits=chosen.edges.reduce((a,j)=>a|(1<<j),0),achieved=exactValue(prizes,anchors,edges,chosen.root,bits);
  assert(cmp(achieved,F(plan.lower,D))>=0&&cmp(overall,F(plan.upper,D))<=0);
  cases.push({index:k,prizes,anchors,edges,D,rootValues:roots,lower:plan.lower,upper:plan.upper,chosen,achieved,scores:plan.scores});
}
const large=[];
for(const shape of ['path','star','random']){
  const n=4096;let t=process.hrtime.bigint();const prizes=Array.from({length:n},()=>1+rand(32)),make=()=>({p4:1+rand(4),k:1+rand(4),c:rand(17)}),anchors=Array.from({length:n},()=>rand(3)===0?null:make()),edges=Array.from({length:n-1},(_,j)=>[shape==='path'?j:shape==='star'?0:rand(j+1),j+1,make()]),source_ns=Number(process.hrtime.bigint()-t);
  t=process.hrtime.bigint();const plan=compile(prizes,anchors,edges,1000000000n),planning_ns=Number(process.hrtime.bigint()-t);t=process.hrtime.bigint();const chosen=policy(plan),policy_ns=Number(process.hrtime.bigint()-t);
  large.push({shape,prizes,anchors,edges,D:plan.D,lower:plan.lower,upper:plan.upper,scores:plan.scores,chosen,source_ns,planning_ns,policy_ns});
}
const sources={};for(const file of ['rationals.mjs','capped_tree.mjs','capped_probe.mjs'])sources[file]=crypto.createHash('sha256').update(fs.readFileSync(new URL(file,import.meta.url))).digest('hex');
const result={status:'complete',evidence:'DEVELOPMENT',contributor:'Codex (GPT-6)',node:process.version,seed,sources,cases,enumerations,large,elapsed_ns:Number(process.hrtime.bigint()-start),limits:'All-root optimum only within declared capped single-anchor outward-expansion class. Conditional success and fixed attempt-price bounds supplied, not learned or authenticated. Ordinary rerooting comparison is identical.'};
fs.writeFileSync(out,JSON.stringify(result,(_,v)=>serial(v),2)+'\n');console.log(JSON.stringify({status:result.status,cases:cases.length,enumerations,large:large.map(c=>({shape:c.shape,root:c.chosen.root,vertices:c.chosen.vertices.length,lower:Number(c.lower)/Number(c.D),interval_width:Number(c.upper-c.lower)/Number(c.D),source_ns:c.source_ns,planning_ns:c.planning_ns,policy_ns:c.policy_ns})),elapsed_ns:result.elapsed_ns}));
