'use strict';
// Bounded, checked resolution layers over actual input clauses.
const assert=require('node:assert/strict'),k=require('./retained.cjs');
function extract(source,depth,meter=new k.Meter(),caps={width:4,derived:256,candidates:50000}){
 k.admit(source,meter);const all=source.hard.map(c=>c.slice()),levels=all.map(()=>0),steps=[],known=new Set(all.map(k.canonical));let examined=0,stopped=null;
 outer:for(let right=0;right<all.length;right++)for(let left=0;left<right;left++){
  const level=Math.max(levels[left],levels[right])+1;if(level>depth)continue;
  for(const signed of all[left])if(all[right].includes(-signed)){
   if(examined>=caps.candidates){stopped='candidate_cap';break outer;}examined++;meter.pay('resolution_candidate',all[left].length+all[right].length+3);
   const pivot=Math.abs(signed),out=k.resolve(all[left],all[right],pivot);if(out.length===0||out.length>caps.width||out.some(x=>out.includes(-x))||known.has(k.canonical(out)))continue;
   if(steps.length>=caps.derived){stopped='derived_cap';break outer;}known.add(k.canonical(out));all.push(out);levels.push(level);steps.push({left,right,pivot,out});meter.pay('resolution_emit',out.length+3);
  }
 }
 const map=new Map(source.features.map((v,i)=>[v,i])),cuts=[];all.forEach((c,index)=>{meter.pay('cover_scan',c.length);if(c.every(v=>map.has(v)))cuts.push({clause:index,features:c.map(v=>map.get(v)).sort((a,b)=>a-b),rhs:1});});
 return k.seal({version:'s10-layered-v1',source_id:source.id,feature_map:source.features,steps,cuts,caps,depth,examined,stopped});
}
function parse(text,name){let n=null,count=null,hard=[],current=[];
 for(const line of text.split(/\r?\n/)){const s=line.trim();if(!s||s.startsWith('c'))continue;if(s.startsWith('%'))break;if(s.startsWith('p ')){const words=s.split(/\s+/);assert.equal(words[1],'cnf');n=Number(words[2]);count=Number(words[3]);continue;}for(const token of s.split(/\s+/)){const x=Number(token);assert(Number.isInteger(x));if(x===0){if(current.length){hard.push(current);current=[];}}else current.push(x);}}
 assert(n&&count!==null&&current.length===0);assert.equal(hard.length,count);return k.source(name,n,hard);
}
function propose(source,trial,meter=new k.Meter(),cap=200000){
 k.admit(source,meter);const degree=Array(source.variables).fill(0);for(const c of source.hard)for(const lit of c)degree[Math.abs(lit)-1]++;const order=degree.map((_,i)=>i).sort((i,j)=>trial===2?degree[i]-degree[j]||i-j:degree[j]-degree[i]||i-j),assignment=degree.map(()=>-1);let nodes=0,answer=null;
 function search(){if(++nodes>cap)throw new Error('Public-model proposal node cap');meter.pay('proposal_node',2);let all=true;
  for(const c of source.hard){let sat=false,open=false;for(const lit of c){const value=assignment[Math.abs(lit)-1];if(value<0)open=true;else if(Boolean(value)===(lit>0))sat=true;meter.pay('proposal_literal');}if(!sat&&!open)return false;if(!sat)all=false;}
  if(all){answer=assignment.reduce((mask,value,i)=>mask+((value===1||(value===-1&&trial===1))?2**i:0),0);return true;}
  const i=order.find(x=>assignment[x]===-1);assert(i!==undefined);const first=trial===1?1:trial===2?i%2:0;for(const value of [first,1-first]){assignment[i]=value;if(search())return true;}assignment[i]=-1;return false;
 }
 const found=search();if(!found)throw new Error('No source model found');k.modelFeatures(source,answer,meter);return {model:answer,nodes,trial,invoice:meter.record()};
}
module.exports={extract,parse,propose};
