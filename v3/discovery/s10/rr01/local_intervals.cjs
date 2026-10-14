'use strict';
const k=require('./retained.cjs'),af=require('./affine_intervals.cjs'),la=require('./local_actions.cjs');
function find(source,models,initial,queries,fees,tolerance,meter=new k.Meter(),limits={queries:12,probes:6,passes:4}){
 const base=la.initialTable(models,meter),initialRegrets=models.map(v=>initial.a.reduce((s,a,i)=>s+4*Math.abs(a-3*v.v[i]),0)),rootRegret=Math.max(...initialRegrets);
 if(rootRegret<=tolerance)return {selected:null,initial_closes:true,attempts:[],limits};
 const candidates=queries.map((q,index)=>{let mean=0;for(const t of [0,2,4]){let worst=-Infinity;models.forEach((v,j)=>{const d=initial.a[q.coordinate]-3*v.v[q.coordinate],l=q.lo0+q.lo1*t,u=q.hi0+q.hi1*t;worst=Math.max(worst,initialRegrets[j]-4*Math.abs(d)+d*(d>=0?u:l));meter.pay('local_query_rank',8);});mean+=worst;}return {index,query:q,fee:fees[index],gain:3*rootRegret-mean};}).sort((a,b)=>a.fee-b.fee||b.gain-a.gain||a.index-b.index).slice(0,limits.queries);
 const attempts=[];let selected=null;
 for(const candidate of candidates){const query=candidate.query,inventory={actions:[initial]},first=af.interval(models,initial,query,tolerance,meter),intervals=first?[{...first,action:0}]:[],probes=[];let certificate=af.cover(intervals,query.domain,meter),seed=initial;
  for(let probe=0;probe<limits.probes&&!certificate.complete;probe++){const t=2*certificate.frontier+1,table=la.pointTable(models,base,query,t,12,meter),action=la.propose(models,table,seed,meter,limits.passes);probes.push({t,scale:12,action,kind:action.regret<=12*tolerance?'certifiable':'proposal_failed_unresolved'});if(action.regret>12*tolerance)break;const index=inventory.actions.length;inventory.actions.push(action);const row=af.interval(models,action,query,tolerance,meter);if(row)intervals.push({...row,action:index});certificate=af.cover(intervals,query.domain,meter);seed=action;}
  const attempt={...candidate,inventory,intervals,probes,certificate};attempts.push(attempt);if(certificate.complete){af.check(source,models,inventory,query,certificate,tolerance,meter);selected=attempt;break;}
 }
 meter.pay('local_interval_retention',attempts.reduce((s,a)=>s+10+a.inventory.actions.length*(source.features.length+5)+a.intervals.length*4,0));return {selected,attempts,initial_closes:false,limits};
}
module.exports={find};
