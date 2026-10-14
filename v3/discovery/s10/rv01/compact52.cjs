'use strict';
const assert=require('node:assert/strict'),k=require('./retained52.cjs'),dg=require('./diagram52.cjs'),rm=require('./robust_menu.cjs'),la=require('./local_actions.cjs');
function interval(diagram,action,lo,hi,map,tolerance,meter=new k.Meter()){
 const i=map.coordinate,q=action.a.map((a,j)=>j===i?0:a*hi[j]+(3-a)*lo[j]),A=k.sum(action.a.map((a,j)=>j===i?0:a*hi[j]));meter.pay('compact_interval_objective',5*q.length);const marginal=dg.evaluate(diagram,q,meter).marginals[i],lines=[];
 if(marginal[0]!==null)lines.push({intercept:A+action.a[i]*map.hi0-marginal[0],slope:action.a[i]*map.hi1});
 if(marginal[1]!==null)lines.push({intercept:A-(3-action.a[i])*map.lo0-marginal[1],slope:-(3-action.a[i])*map.lo1});
 let lower=0,upper=6*map.max;for(const {intercept,slope}of lines){meter.pay('compact_interval_halfspace',8);if(slope===0){if(intercept>tolerance)return {region:null,lines};}else{const x=6*(tolerance-intercept)/slope;assert(Number.isSafeInteger(x));if(slope>0)upper=Math.min(upper,x);else lower=Math.max(lower,x);}}return {region:lower<=upper?{kind:'positive',lower,upper,action}:null,lines};
}
function pattern(known){return known.map(x=>x===null?'_':'x').join('');}
function neighborhood(action,known,upper,tolerance){assert(upper<=tolerance);return {action,anchor:known.slice(),pattern:pattern(known),upper,tolerance};}
function variation(record,known,meter=new k.Meter()){
 if(record.pattern!==pattern(known))return null;let extra=0;for(let i=0;i<record.action.a.length;i++){const t=known[2*i]===null?0:known[2*i]-record.anchor[2*i],f=known[2*i+1]===null?0:known[2*i+1]-record.anchor[2*i+1],delta=t-f,a=record.action.a[i];extra+=Math.max(a*delta,(a-3)*delta);meter.pay('neighborhood_coordinate',8);}return extra;
}
function hit(record,known,meter=new k.Meter()){const extra=variation(record,known,meter);return extra!==null&&record.upper+extra<=record.tolerance;}
function seedPool(source,diagram,meter=new k.Meter()){
 const pool=[],seen=new Set(),n=source.features.length;for(let trial=0;trial<8;trial++){const q=Array.from({length:n},(_,i)=>trial===0?0:trial===1?1:trial===2?-1:((i>>(trial-3))&1)?1:-1),ev=dg.evaluate(diagram,q,meter,false);if(!seen.has(ev.model)){seen.add(ev.model);pool.push({mask:ev.model,v:k.modelFeatures(source,ev.model,meter)});meter.pay('witness_pool_retention',n+2);}}return pool;
}
function propose(source,diagram,pool,lo,hi,incumbent,meter=new k.Meter(),rounds=2,cap=12){
 let action=incumbent||{models:Array(3).fill(pool[0].mask),a:pool[0].v.map(x=>3*x),m:3},evaluation=dg.bound(diagram,action.a,3,lo,hi,meter,false),best={...action,regret:evaluation.regret},steps=[];
 for(let round=0;round<rounds;round++){
  for(const mask of best.models)if(!pool.some(x=>x.mask===mask)&&pool.length<cap)pool.push({mask,v:k.modelFeatures(source,mask,meter)});
  const canSeed=best.models.every(mask=>pool.some(x=>x.mask===mask)),table=rm.pairwise(pool,lo,hi,meter),candidate=la.propose(pool,table,canSeed?best:null,meter,3),bound=dg.bound(diagram,candidate.a,3,lo,hi,meter,false);steps.push({models:candidate.models,regret:bound.regret,worst:bound.model});
  if(bound.regret<best.regret)best={...candidate,regret:bound.regret};
  if(pool.some(x=>x.mask===bound.model)||pool.length>=cap)break;
  pool.push({mask:bound.model,v:k.modelFeatures(source,bound.model,meter)});meter.pay('witness_pool_retention',lo.length+2);
 }
 return {action:best,steps,pool};
}
module.exports={interval,pattern,neighborhood,variation,hit,seedPool,propose};
