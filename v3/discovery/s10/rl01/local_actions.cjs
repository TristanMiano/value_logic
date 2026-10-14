'use strict';
// Ordinary coordinate-descent proposal over a complete checked model list.
const assert=require('node:assert/strict'),k=require('./retained.cjs');
function initialTable(models,meter=new k.Meter()) {return models.map(x=>models.map(y=>{let value=0;for(let i=0;i<x.v.length;i++){value+=4*Math.abs(x.v[i]-y.v[i]);meter.pay('local_pair_initial',4);}return value;}));}
function pointTable(models,base,query,t,scale,meter=new k.Meter()){
 const i=query.coordinate,l=scale*query.lo0+query.lo1*t,u=scale*query.hi0+query.hi1*t;assert(l<=u);return models.map((x,j)=>models.map((y,z)=>{const d=x.v[i]-y.v[i];meter.pay('local_pair_reprice',8);return scale*(base[j][z]-4*Math.abs(d))+d*(d>=0?u:l);}));
}
function propose(models,table,initial,meter=new k.Meter(),passes=4){
 const n=models.length,seed=initial?initial.models.map(mask=>{const i=models.findIndex(x=>x.mask===mask);assert(i>=0);return i;}):[0,Math.floor(n/2),n-1],seeds=[seed,[0,0,0],[n-1,n-1,n-1]],seen=new Set();let best=null;
 function objective(indices){let value=-Infinity;for(let j=0;j<n;j++){value=Math.max(value,table[indices[0]][j]+table[indices[1]][j]+table[indices[2]][j]);meter.pay('local_triple_competitor',4);}return value;}
 for(const start of seeds){if(seen.has(start.join(',')))continue;seen.add(start.join(','));let chosen=start.slice(),value=objective(chosen),used=0;
  for(;used<passes;used++){let improved=false;for(let copy=0;copy<3;copy++){let candidateValue=value,candidate=chosen;for(let i=0;i<n;i++){const proposed=chosen.slice();proposed[copy]=i;const objectiveValue=objective(proposed);meter.pay('local_candidate_compare',2);if(objectiveValue<candidateValue){candidateValue=objectiveValue;candidate=proposed;}}if(candidateValue<value){value=candidateValue;chosen=candidate;improved=true;}}if(!improved)break;}
  if(!best||value<best.regret)best={models:chosen.map(i=>models[i].mask),indices:chosen,a:models[0].v.map((_,i)=>chosen.reduce((s,j)=>s+models[j].v[i],0)),m:3,regret:value,passes:used};
 }
 meter.pay('local_action_export',models[0].v.length+8);return best;
}
module.exports={initialTable,pointTable,propose};
