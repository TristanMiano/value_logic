'use strict';
const assert=require('node:assert/strict'),k=require('./retained52.cjs'),G=1000;
function type(a,kind){assert(a===1||a===2);return (a-1)*2+(kind==='false'?1:0);}
function lower(histogram,confidence,meter=new k.Meter()){
 const n=k.sum(histogram);if(!n)return {n:0,radius:1000,b:0,tails:[0,0],weights:[1000,0,0]};let b=0,radius=0;
 if(confidence){const target=1600n*BigInt(n)*BigInt(n);while((1n<<BigInt(b))<target){b++;meter.pay('calibration_log_bound',2);}let lo=0n,hi=1000n;const rhs=7n*BigInt(b)*1000000n;while(20n*BigInt(n)*hi*hi<rhs)hi*=2n;while(lo<hi){const mid=(lo+hi)/2n;if(20n*BigInt(n)*mid*mid>=rhs)hi=mid;else lo=mid+1n;meter.pay('calibration_integer_root',7);}radius=Number(lo);}
 const first=Math.max(0,Math.floor((histogram[1]+histogram[2])*G/n)-radius),second=Math.min(first,Math.max(0,Math.floor(histogram[2]*G/n)-radius));meter.pay('calibration_tail_bounds',16);return {n,radius,b,tails:[first,second],weights:[G-first,first-second,second]};
}
function compile(quota,queries,fees,a,C,histograms,confidence,meter=new k.Meter()){
 const bounds=histograms.map(h=>lower(h,confidence,meter)),mixed=queries.map((q,i)=>a[q.coordinate]===1||a[q.coordinate]===2?i:null).filter(x=>x!==null),weights=i=>bounds[type(a[queries[i].coordinate],queries[i].kind)].weights,feeOrder=mixed.slice().sort((i,j)=>fees[i]-fees[j]||i-j),gainOrder=mixed.slice().sort((i,j)=>{const x=weights(i),y=weights(j);return (y[1]+2*y[2])*fees[i]-(x[1]+2*x[2])*fees[j]||i-j;}),orders=[];let bestNum=BigInt(quota===0?0:C),bestDen=1n,best=[];
 if(quota>0)for(const order of [feeOrder,gainOrder]){let dist=Array(quota+1).fill(0n);dist[0]=1n;let den=1n,paid=0n,spent=0;const rows=[];for(let j=0;j<order.length;j++){const fee=fees[order[j]];if(spent+fee>C)break;spent+=fee;const w=weights(order[j]).map(BigInt),unresolved=den-dist[quota],next=Array(quota+1).fill(0n);for(let score=0;score<=quota;score++)for(let d=0;d<3;d++){next[Math.min(quota,score+d)]+=dist[score]*w[d];meter.pay('learned_prefix_transition',4);}paid=(paid+BigInt(fee)*unresolved)*1000n;den*=1000n;dist=next;const num=paid+BigInt(C)*(den-dist[quota]);meter.pay('learned_prefix_compare',8);if(num*bestDen<bestNum*den){bestNum=num;bestDen=den;best=order.slice(0,j+1);}rows.push({length:j+1,numerator:String(num),denominator:String(den),listed_fee:spent});}orders.push({order,rows});}
 meter.pay('learned_prefix_retention',mixed.length*3+orders.reduce((s,o)=>s+o.rows.length*5,0)+48);return {quota,confidence,histograms:histograms.map(x=>x.slice()),bounds,orders,order:best,numerator:String(bestNum),denominator:String(bestDen)};
}
module.exports={type,lower,compile};
