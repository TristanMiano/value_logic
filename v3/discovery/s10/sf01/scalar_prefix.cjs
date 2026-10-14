'use strict';
const assert=require('node:assert/strict'),k=require('./retained52.cjs');
function compile(quota,queries,fees,C,meter=new k.Meter()){
 assert(Number.isSafeInteger(quota)&&quota>=0);const order=queries.map((_,i)=>i).sort((i,j)=>fees[i]-fees[j]||i-j),weights=[9000n,9000n,6001n],W=24001n;
 if(quota===0)return {quota,order:[],cutoff:0,numerator:'0',denominator:'1',rows:[]};
 let dist=Array(quota+1).fill(0n);dist[0]=1n;let den=1n,paid=0n,spent=0,bestNum=BigInt(C),bestDen=1n,cutoff=0;const rows=[];
 for(let j=0;j<order.length;j++){const fee=fees[order[j]];if(spent+fee>C)break;spent+=fee;const unresolved=den-dist[quota],next=Array(quota+1).fill(0n);for(let s=0;s<=quota;s++)for(let score=0;score<3;score++){next[Math.min(quota,s+score)]+=dist[s]*weights[score];meter.pay('scalar_convolution_transition',4);}paid=(paid+BigInt(fee)*unresolved)*W;den*=W;dist=next;const num=paid+BigInt(C)*(den-dist[quota]);meter.pay('scalar_prefix_comparison',8);if(num*bestDen<bestNum*den){bestNum=num;bestDen=den;cutoff=j+1;}rows.push({length:j+1,listed_fee:spent,numerator:String(num),denominator:String(den),survival:String(den-dist[quota])});}
 meter.pay('scalar_prefix_retention',order.length+rows.length*6+8);return {quota,order,cutoff,numerator:String(bestNum),denominator:String(bestDen),rows};
}
function score(a,kind,t,max=24000){assert(a===1||a===2);return Math.floor((kind==='true'?Math.min(a*(max-t),(3-a)*t):Math.min(a*t,(3-a)*(max-t)))/6000);}
module.exports={compile,score};
