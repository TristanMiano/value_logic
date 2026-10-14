'use strict';
const assert=require('node:assert/strict'),k=require('./retained52.cjs');
function target(source,variable,value){k.integer(variable,1);assert(variable<=source.variables);assert(value===0||value===1);const {id,...body}=source;return k.seal({...body,name:source.name+'_x'+variable+'_'+value,hard:[...source.hard,[value?variable:-variable]]});}
function apply(source,parent,variable,value,meter=new k.Meter()){
 const next=target(source,variable,value);assert.equal(parent.source_id,source.id);const depth=parent.order.indexOf(variable),nodes=[{terminal:false},{terminal:true}],mapping=[0,1],unique=new Map();
 for(let i=2;i<parent.nodes.length;i++){const old=parent.nodes[i];let low=mapping[old.low],high=mapping[old.high];if(old.depth===depth){if(value)low=0;else high=0;}meter.pay('patch_node',8);if(low===0&&high===0){mapping[i]=0;continue;}const key=old.depth+':'+low+':'+high;if(unique.has(key))mapping[i]=unique.get(key);else{mapping[i]=nodes.length;nodes.push({depth:old.depth,low,high});unique.set(key,mapping[i]);meter.pay('patch_emit',4);}}
 meter.pay('patch_binding_words',source.hard.reduce((s,c)=>s+c.length+1,0)+source.features.length+4*parent.nodes.length+20);
 meter.pay('patch_retention',mapping.length+4*nodes.length+parent.order.length+12);
 return k.seal({version:'s10-source-unit-patch-v1',parent_id:k.hash(parent),source_id:source.id,target:next,variable,value,order:parent.order,features:parent.features,variables:parent.variables,nodes,mapping,root:mapping[parent.root]});
}
function check(source,parent,proof,meter=new k.Meter()){
 k.admit(source,meter);k.checkSeal(proof);assert.equal(proof.version,'s10-source-unit-patch-v1');assert.equal(proof.parent_id,k.hash(parent));assert.equal(proof.source_id,source.id);assert.equal(parent.source_id,source.id);assert.deepEqual(proof.target,target(source,proof.variable,proof.value));k.admit(proof.target,meter);assert.equal(proof.variables,source.variables);assert.deepEqual(proof.features,source.features);assert.deepEqual(proof.order,parent.order);assert.deepEqual(parent.features,source.features);assert.equal(parent.variables,source.variables);
 const {mapping,nodes}=proof,depth=parent.order.indexOf(proof.variable);assert(depth>=0);assert.equal(mapping.length,parent.nodes.length);assert.equal(mapping[0],0);assert.equal(mapping[1],1);assert.deepEqual(nodes[0],{terminal:false});assert.deepEqual(nodes[1],{terminal:true});const used=new Set([0,1]);
 for(let i=2;i<parent.nodes.length;i++){const old=parent.nodes[i],id=mapping[i];let low=mapping[old.low],high=mapping[old.high];if(old.depth===depth){if(proof.value===0)high=0;else low=0;}k.integer(id);assert(id<nodes.length);if(id===0)assert(low===0&&high===0);else{assert(id>1);assert.deepEqual(nodes[id],{depth:old.depth,low,high});assert(low<id&&high<id);used.add(id);}meter.pay('patch_check_node',12);}
 assert.equal(used.size,nodes.length);assert.equal(proof.root,mapping[parent.root]);meter.pay('patch_check_binding',4*parent.nodes.length+mapping.length+parent.order.length+16);
 return {version:proof.version,source_id:proof.target.id,features:proof.features,variables:proof.variables,order:proof.order,nodes,root:proof.root,receipt_id:proof.id,parent_receipt_id:parent.receipt_id};
}
module.exports={target,apply,check};
