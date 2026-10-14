'use strict';
const assert=require('node:assert/strict'),k=require('./retained.cjs');
function actions(models,meter=new k.Meter(),cap=50000){const unique=new Map();let triples=0;for(let i=0;i<models.length;i++)for(let j=i;j<models.length;j++)for(let z=j;z<models.length;z++){assert(++triples<=cap);const a=models[0].v.map((_,t)=>models[i].v[t]+models[j].v[t]+models[z].v[t]),key=a.join(',');meter.pay('interval_action_counts',3*a.length+2);if(!unique.has(key)){unique.set(key,{a,m:3,models:[models[i].mask,models[j].mask,models[z].mask]});meter.pay('interval_action_retention',a.length+5);}}return {triples,actions:[...unique.values()]};}
function intervals(models,inventory,tolerance,relevant,meter=new k.Meter()){
 const perFeature=new Map(relevant.map(i=>[i,[]]));
 for(const [actionIndex,action]of inventory.actions.entries()){
  const initial=models.map(v=>{let r=0;for(let i=0;i<action.a.length;i++){r+=4*Math.abs(action.a[i]-3*v.v[i]);meter.pay('interval_competitor_initial',4);}return r;});
  for(const i of relevant){let lo=-24,hi=24,possible=true;for(let j=0;j<models.length;j++){const d=action.a[i]-3*models[j].v[i],base=initial[j]-4*Math.abs(d);meter.pay('interval_constraint',7);if(d===0){if(base>tolerance){possible=false;break;}}else{const end=6*(tolerance-base)/d;assert(Number.isInteger(end));if(d>0)hi=Math.min(hi,end);else lo=Math.max(lo,end);if(lo>hi){possible=false;break;}}}if(possible){perFeature.get(i).push({lo,hi,action:actionIndex});meter.pay('interval_emit',4);}}
 }
 return perFeature;
}
function cover(intervals,meter=new k.Meter()){
 const sorted=intervals.slice().sort((a,b)=>a.lo-b.lo||b.hi-a.hi||a.action-b.action);meter.pay('interval_sort_budget',sorted.length*Math.ceil(Math.log2(sorted.length+1)));let frontier=-24,at=0;const chosen=[];
 while(frontier<24){let best=null;while(at<sorted.length&&sorted[at].lo<=frontier){if(best===null||sorted[at].hi>best.hi)best=sorted[at];at++;meter.pay('interval_cover_scan',3);}if(!best||best.hi<=frontier)return {complete:false,frontier,chosen,gap_to:at<sorted.length?sorted[at].lo:24};chosen.push(best);frontier=best.hi;}
 return {complete:true,frontier,chosen};
}
function check(source,models,inventory,query,certificate,tolerance,meter=new k.Meter()){
 assert(certificate.complete);let frontier=-24;for(const row of certificate.chosen){assert(Number.isInteger(row.lo)&&Number.isInteger(row.hi));assert(row.lo<=frontier&&row.hi>frontier);const action=inventory.actions[row.action];assert(action);for(const mask of action.models)k.modelFeatures(source,mask,meter);
  for(const t of [row.lo,row.hi])for(const v of models){let r=0;for(let i=0;i<action.a.length;i++){const d=action.a[i]-3*v.v[i];r+=i===query?d*t:24*Math.abs(d);meter.pay('interval_endpoint_check',5);}assert(r<=6*tolerance);}
  frontier=row.hi;
 }assert(frontier>=24);return true;
}
module.exports={actions,intervals,cover,check};
