'use strict';
const assert=require('node:assert/strict'),k=require('./retained.cjs');
function compile(source,receipt,meter=new k.Meter()){
 k.admit(source,meter);k.checkSeal(receipt);assert.equal(receipt.source_id,source.id);const assignment=Array(source.variables).fill(-1),leaves=[];let nodes=0;
 function walk(node){nodes++;meter.pay('partition_node',2);assert(Array.isArray(node));
  if(node[0]==='clause'){assert.equal(node.length,2);const c=source.hard[node[1]];assert(c);for(const lit of c){const value=assignment[Math.abs(lit)-1];assert(value!==-1&&Boolean(value)!==(lit>0));meter.pay('partition_conflict_literal');}return;}
  if(node[0]==='bound'){assert.equal(node.length,1);let mask=0;source.features.forEach((v,i)=>{if(assignment[v-1]===1)mask+=2**i;meter.pay('partition_feature_projection');});leaves.push(mask);return;}
  assert.equal(node[0],'split');assert.equal(node.length,4);const v=node[1];k.integer(v);assert(v<source.variables&&assignment[v]===-1);assignment[v]=0;walk(node[2]);assignment[v]=1;walk(node[3]);assignment[v]=-1;
 }
 walk(receipt.proof);assert.equal(nodes,receipt.proof_nodes);assert(leaves.length>0);
 function bits(mask){let count=0;for(let i=0;i<source.features.length;i++){count+=Number(Boolean(mask&(2**i)));meter.pay('partition_popcount');}return count;}
 const unique=[...new Set(leaves)].map(mask=>({mask,count:bits(mask)})).sort((a,b)=>a.count-b.count||a.mask-b.mask),minimal=[];
 for(const {mask} of unique){let dominated=false;for(const old of minimal){meter.pay('partition_subset_probe');if((old&mask)===old){dominated=true;break;}}if(!dominated)minimal.push(mask);}
 meter.pay('partition_retention_words',minimal.length+source.features.length+10);
 return k.seal({version:'s10-proof-cover-v1',source_id:source.id,feature_map:source.features,receipt_id:receipt.id,raw_leaves:leaves.length,unique_leaves:unique.length,masks:minimal,nodes});
}
function lower(cert,q,meter=new k.Meter()){
 assert.equal(q.length,cert.feature_map.length);q.forEach(x=>k.integer(x));let value=Infinity;
 for(const mask of cert.masks){let term=0;for(let i=0;i<q.length;i++){if(mask&(2**i))term+=q[i];meter.pay('partition_objective_probe',2);}value=Math.min(value,term);meter.pay('partition_minimum');}return value;
}
function leafBounds(cert,a,m,lo,hi,meter=new k.Meter()){
 assert(a.length===cert.feature_map.length);const values=[];
 for(const mask of cert.masks){let value=0;for(let i=0;i<a.length;i++){assert(lo[i]>=0&&lo[i]<=hi[i]);value+=(mask&(2**i))?-(m-a[i])*lo[i]:a[i]*hi[i];meter.pay('leaf_bound_coordinate',4);}values.push(value);}return values;
}
function completion(cert,a,m,lo,hi,tolerance,i,meter=new k.Meter()){
 k.integer(i);assert(i<a.length);const values=leafBounds(cert,a,m,lo,hi,meter);let inside=0,outside=0;
 for(let j=0;j<values.length;j++){const r=Math.max(0,values[j]-tolerance);if(cert.masks[j]&(2**i))inside=Math.max(inside,r);else outside=Math.max(outside,r);meter.pay('completion_partition_max',3);}
 return {inside,outside,lower:a[i]===m?(inside===0?lo[i]:Infinity):lo[i]+inside/(m-a[i]),upper:a[i]===0?(outside===0?hi[i]:-Infinity):hi[i]-outside/a[i]};
}
function closes(interval,a,m,lo,hi,i,t){return (m-a[i])*(t-lo[i])>=interval.inside&&a[i]*(hi[i]-t)>=interval.outside;}
module.exports={compile,lower,leafBounds,completion,closes};
