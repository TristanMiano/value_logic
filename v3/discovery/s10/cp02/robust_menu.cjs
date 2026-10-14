'use strict';
// Exact finite ordinary three-copy minimax selection after charged enumeration.
const assert=require('node:assert/strict'),k=require('./retained.cjs');
function enumerate(diagram,source,meter=new k.Meter(),cap=64){
 const result=[];function walk(id,mask){meter.pay('diagram_model_path');if(id===0)return;if(id===1){assert(result.length<cap,'Model cap');const v=k.modelFeatures(source,mask,meter);result.push({mask,v});meter.pay('diagram_model_emit',v.length+2);return;}const node=diagram.nodes[id],variable=diagram.order[node.depth];walk(node.low,mask);walk(node.high,mask+2**(variable-1));}walk(diagram.root,0);assert(result.length);assert.equal(new Set(result.map(x=>x.mask)).size,result.length);return result;
}
function pairwise(models,lo,hi,meter=new k.Meter()){
 return models.map(x=>models.map(y=>{let value=0;for(let i=0;i<x.v.length;i++){const d=x.v[i]-y.v[i];value+=d*(d>=0?hi[i]:lo[i]);meter.pay('pairwise_regret_coordinate',4);}return value;}));
}
function best(models,lo,hi,meter=new k.Meter(),cap=50000){
 const table=pairwise(models,lo,hi,meter);let value=Infinity,triple=null,examined=0;
 for(let i=0;i<models.length;i++)for(let j=i;j<models.length;j++)for(let z=j;z<models.length;z++){
  assert(++examined<=cap,'Triple cap');let worst=-Infinity;for(let t=0;t<models.length;t++){worst=Math.max(worst,table[i][t]+table[j][t]+table[z][t]);meter.pay('robust_triple_competitor',4);}if(worst<value){value=worst;triple=[i,j,z];}meter.pay('robust_triple_comparison',2);
 }
 const masks=triple.map(i=>models[i].mask),a=models[0].v.map((_,i)=>k.sum(triple.map(j=>models[j].v[i])));meter.pay('robust_action_export',a.length+8);return {models:masks,a,m:3,regret:value,indices:triple,examined};
}
module.exports={enumerate,pairwise,best};
