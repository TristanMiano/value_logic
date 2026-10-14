'use strict';
// Exact integer prefix compiler and evaluator. Ordinary threshold policy.
const assert=require('node:assert/strict'),k=require('./retained.cjs');
function less(a,b){return a.num*b.den<b.num*a.den;}
function number(r){return Number(r.num)/Number(r.den);}
function record(r){return {numerator:r.num.toString(),denominator:r.den.toString(),decimal:number(r)};}
function distribution(scores,dist,quota,meter){const next=new Map();for(const [s,w] of dist)for(const d of scores){const t=Math.min(quota,s+d);next.set(t,(next.get(t)||0n)+w);meter.pay('prefix_convolution',4);}return next;}
function orders(scores,fees,meter){
 const n=scores.length,indices=Array.from({length:n},(_,i)=>i),means=scores.map(s=>k.sum(s)/s.length),positive=scores.map(s=>s.filter(x=>x>0).length/s.length);
 meter.pay('prefix_score_statistics',k.sum(scores.map(s=>3*s.length)));
 const result=[indices.slice().sort((i,j)=>means[j]/fees[j]-means[i]/fees[i]||i-j),indices.slice().sort((i,j)=>positive[j]/fees[j]-positive[i]/fees[i]||i-j),indices.slice().sort((i,j)=>fees[i]-fees[j]||i-j)];
 meter.pay('prefix_ordering',3*n*Math.max(1,Math.ceil(Math.log2(n+1))));return [...new Map(result.map(o=>[o.join(','),o])).values()];
}
function compile(scores,fees,quota,C,budget,meter=new k.Meter()){
 k.integer(quota);assert(quota<=10000);k.integer(C,1);k.integer(budget);assert(scores.length===fees.length);
 if(quota===0)return {sequence:[],expected:{num:0n,den:1n},quota,C,budget,examined:[],initially_complete:true};
 let best={num:BigInt(C),den:1n},sequence=[],selectedOrder=-1;const examined=[];
 for(const [oi,order] of orders(scores,fees,meter).entries()){
  let den=1n,dist=new Map([[0,1n]]),queryNum=0n,listed=0;const prefix=[];
  for(const i of order){
   if(listed+fees[i]>budget)break;
   listed+=fees[i];prefix.push(i);const factor=BigInt(scores[i].length),tail=den-(dist.get(quota)||0n);
   queryNum=(queryNum+BigInt(fees[i])*tail)*factor;den*=factor;
   dist=distribution(scores[i],dist,quota,meter);const expected={num:queryNum+BigInt(C)*(den-(dist.get(quota)||0n)),den};
   meter.pay('prefix_value_arithmetic',14);examined.push({order:oi,cutoff:prefix.length,listed_fee:listed,expected:record(expected),states:dist.size});
   if(less(expected,best)){best=expected;sequence=prefix.slice();selectedOrder=oi;}
  }
 }
 return {sequence,expected:best,quota,C,budget,selected_order:selectedOrder,examined,initially_complete:false};
}
function evaluate(plan,fees,scores,worldIndices,meter=new k.Meter()){
 let score=0,fee=0,queries=0;for(const i of plan.sequence){if(score>=plan.quota)break;score+=scores[i][worldIndices[i]];fee+=fees[i];queries++;meter.pay('prefix_runtime',4);}
 const fallback=score<plan.quota;if(fallback)fee+=plan.C;assert(fee<=plan.budget+plan.C);return {fee,queries,score,fallback};
}
function serial(plan){return {...plan,expected:record(plan.expected)};}
module.exports={compile,evaluate,orders,record,serial,number};
