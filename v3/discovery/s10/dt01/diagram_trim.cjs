'use strict';
// Checked ordinary dead-state elimination; keep live variable layers.
const assert=require('node:assert/strict'),k=require('./retained.cjs');
function trim(diagram,meter=new k.Meter()){
 const nodes=[{terminal:false},{terminal:true}],mapping=[0,1],unique=new Map();
 for(let i=2;i<diagram.nodes.length;i++){const old=diagram.nodes[i],low=mapping[old.low],high=mapping[old.high];meter.pay('diagram_trim_node',6);if(low===0&&high===0){mapping[i]=0;continue;}const key=old.depth+':'+low+':'+high;if(unique.has(key))mapping[i]=unique.get(key);else{mapping[i]=nodes.length;nodes.push({depth:old.depth,low,high});unique.set(key,mapping[i]);meter.pay('diagram_trim_emit',4);}}
 const result={...diagram,nodes,root:mapping[diagram.root],parent_receipt_id:diagram.receipt_id};meter.pay('diagram_trim_retention',mapping.length+4*nodes.length+8);return {diagram:result,mapping};
}
function check(original,transformed,meter=new k.Meter()){
 const {diagram,mapping}=transformed;assert.deepEqual(diagram.features,original.features);assert.equal(diagram.source_id,original.source_id);assert.deepEqual(diagram.order,original.order);assert.equal(diagram.variables,original.variables);assert.equal(diagram.parent_receipt_id,original.receipt_id);assert.equal(mapping.length,original.nodes.length);assert.equal(mapping[0],0);assert.equal(mapping[1],1);assert.deepEqual(diagram.nodes[0],{terminal:false});assert.deepEqual(diagram.nodes[1],{terminal:true});const used=new Set([0,1]);
 for(let i=2;i<original.nodes.length;i++){const old=original.nodes[i],low=mapping[old.low],high=mapping[old.high],id=mapping[i];k.integer(id);assert(id<diagram.nodes.length);if(id===0)assert(low===0&&high===0);else{assert(id>1);assert.deepEqual(diagram.nodes[id],{depth:old.depth,low,high});assert(low<id&&high<id);used.add(id);}meter.pay('diagram_trim_check',10);}
 assert.equal(used.size,diagram.nodes.length);assert.equal(diagram.root,mapping[original.root]);return diagram;
}
module.exports={trim,check};
