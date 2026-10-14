'use strict';
const assert=require('node:assert/strict'),k=require('./retained.cjs');
function queries(relevant){return relevant.flatMap(i=>[{coordinate:i,kind:'true',domain:[0,4],lo0:-4,lo1:1,hi0:0,hi1:1},{coordinate:i,kind:'false',domain:[0,4],lo0:0,lo1:-1,hi0:4,hi1:-1}]);}
function interval(models,action,query,tolerance,meter=new k.Meter()){
 let lo=6*query.domain[0],hi=6*query.domain[1];const i=query.coordinate;
 for(const v of models){let other=0;for(let j=0;j<action.a.length;j++)if(j!==i){other+=4*Math.abs(action.a[j]-3*v.v[j]);meter.pay('affine_other_regret',4);}const d=action.a[i]-3*v.v[i],slope=d*(d>=0?query.hi1:query.lo1),base=other+d*(d>=0?query.hi0:query.lo0);meter.pay('affine_constraint',8);if(slope===0){if(base>tolerance)return null;}else{const endpoint=6*(tolerance-base)/slope;assert(Number.isInteger(endpoint));if(slope>0)hi=Math.min(hi,endpoint);else lo=Math.max(lo,endpoint);if(lo>hi)return null;}}
 return {lo,hi};
}
function cover(intervals,domain,meter=new k.Meter()){
 const sorted=intervals.slice().sort((a,b)=>a.lo-b.lo||b.hi-a.hi||a.action-b.action);meter.pay('affine_interval_sort',sorted.length*Math.ceil(Math.log2(sorted.length+1)));let frontier=6*domain[0],at=0;const chosen=[];
 while(frontier<6*domain[1]){let best=null;while(at<sorted.length&&sorted[at].lo<=frontier){if(!best||sorted[at].hi>best.hi)best=sorted[at];at++;meter.pay('affine_cover_scan',3);}if(!best||best.hi<=frontier)return {complete:false,frontier,chosen};chosen.push(best);frontier=best.hi;}return {complete:true,frontier,chosen};
}
function check(source,models,inventory,query,certificate,tolerance,meter=new k.Meter()){
 assert(certificate.complete);let frontier=6*query.domain[0];for(const r of certificate.chosen){assert(r.lo<=frontier&&r.hi>frontier);const action=inventory.actions[r.action];assert.equal(action.models.length,3);assert.equal(action.m,3);const vectors=action.models.map(mask=>k.modelFeatures(source,mask,meter)),counts=source.features.map((_,i)=>vectors.reduce((s,v)=>s+v[i],0));assert.deepEqual(counts,action.a);
  for(const t of [r.lo,r.hi])for(const v of models){let value=0;for(let i=0;i<action.a.length;i++){const d=action.a[i]-3*v.v[i],l=i===query.coordinate?6*query.lo0+query.lo1*t:-24,u=i===query.coordinate?6*query.hi0+query.hi1*t:24;assert(l<=u);value+=d*(d>=0?u:l);meter.pay('affine_interval_endpoint',8);}assert(value<=6*tolerance);}frontier=r.hi;
 }assert(frontier>=6*query.domain[1]);return true;
}
module.exports={queries,interval,cover,check};
