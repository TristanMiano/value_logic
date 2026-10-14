'use strict';
const assert=require('node:assert/strict'),k=require('./retained.cjs'),dg=require('./diagram.cjs'),rm=require('./robust_menu.cjs'),ia=require('./interval_actions.cjs');
function find(source,diagram,models,initial,fees,tolerance,meter=new k.Meter(),limits={coordinates:6,probes:6}){
 const n=source.features.length,hi=Array(n).fill(4),base=dg.bound(diagram,initial.a,3,hi.map(()=>-4),hi,meter),zero=dg.evaluate(diagram,Array(n).fill(0),meter),relevant=zero.marginals.map((v,i)=>v.every(x=>x!==null)?i:null).filter(x=>x!==null);
 const order=relevant.map(i=>({i,gain:[-4,-2,0,2,4].reduce((s,t,j)=>s+[1,2,3,2,1][j]*(base.regret-dg.after(base,initial.a,3,hi,i,t,meter)),0)})).sort((a,b)=>fees[a.i]-fees[b.i]||b.gain-a.gain||a.i-b.i).slice(0,limits.coordinates).map(x=>x.i);meter.pay('guided_coordinate_order',relevant.length*relevant.length+8);
 const attempts=[];let selected=null;
 for(const i of order){const inventory={actions:[{models:initial.models,a:initial.a,m:3}]},rows=ia.intervals(models,inventory,tolerance,[i],meter).get(i),probes=[];let certificate=ia.cover(rows,meter);
  for(let probe=0;probe<limits.probes;probe++){
   if(certificate.complete)break;
   const t=2*certificate.frontier+1; // Twelfths: midpoint of first uncovered sixth-cell.
   assert(t>=-47&&t<=47&&Number.isInteger(t));
   const lo=Array(n).fill(-48),upper=Array(n).fill(48);lo[i]=t;upper[i]=t;const action=rm.best(models,lo,upper,meter);probes.push({t,denominator:12,kind:'exact_action',action,scaled_regret:action.regret});
   if(action.regret>12*tolerance){probes.at(-1).kind='uncoverable_witness';break;}
   const index=inventory.actions.length;inventory.actions.push({models:action.models,a:action.a,m:3});const intervals=ia.intervals(models,{actions:[inventory.actions[index]]},tolerance,[i],meter).get(i);rows.push(...intervals.map(r=>({...r,action:index})));certificate=ia.cover(rows,meter);
  }
  attempts.push({query:i,fee:fees[i],probes,inventory,intervals:rows,certificate});if(certificate.complete){ia.check(source,models,inventory,i,certificate,tolerance,meter);selected=attempts.at(-1);break;}
 }
 meter.pay('guided_policy_retention',attempts.reduce((s,a)=>s+12+a.inventory.actions.length*(n+5)+a.intervals.length*4,0));return {selected,attempts,order,limits};
}
module.exports={find};
