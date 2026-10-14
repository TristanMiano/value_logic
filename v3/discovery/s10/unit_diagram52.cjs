'use strict';
const assert=require('node:assert/strict'),k=require('./retained52.cjs'),dg=require('./diagram52.cjs');
function propagate(source,depth,active,position,meter){
 const assigned=Array(source.variables+1).fill(null),steps=[];let changed=true;
 while(changed){changed=false;for(const ci of active){let satisfied=false;const open=[];for(const lit of source.hard[ci]){meter.pay('unit_propagation_literal');const v=Math.abs(lit);if(position[v]<depth)continue;if(assigned[v]===null)open.push(lit);else if(assigned[v]===Number(lit>0)){satisfied=true;break;}}
  if(satisfied)continue;if(!open.length)return {assigned,steps,conflict:ci};if(open.length===1){const literal=open[0];assigned[Math.abs(literal)]=Number(literal>0);steps.push({clause:ci,literal});meter.pay('unit_propagation_step',3);changed=true;break;}
 }}return {assigned,steps,conflict:null};
}
function compile(source,meter=new k.Meter(),cap=100000){
 k.admit(source,meter);const order=dg.variableOrder(source,meter),position=Array(source.variables+1);order.forEach((v,i)=>position[v]=i);const trace=[],nodes=[{terminal:false},{terminal:true}],memo=new Map(),unique=new Map();let probes=0;
 function build(depth,active){const key=depth+':'+active.join(',');meter.pay('unit_state_key',active.length+2);if(memo.has(key)){meter.pay('unit_memo_hit');return memo.get(key);}assert(++probes<=cap,'Unit diagram state cap');const propagation=propagate(source,depth,active,position,meter);let entry;
  if(propagation.conflict!==null)entry={depth,active,steps:propagation.steps,kind:'conflict',clause:propagation.conflict,node:0};
  else if(depth===order.length){assert.equal(active.length,0);entry={depth,active,steps:propagation.steps,kind:'true',node:1};}
  else {const variable=order[depth],forced=propagation.assigned[variable],children=[null,null],ids=[0,0];for(const value of [0,1]){if(forced!==null&&forced!==value)continue;const next=[];for(const ci of active){let satisfied=false;for(const lit of source.hard[ci]){meter.pay('unit_child_literal');if(lit===(value?variable:-variable))satisfied=true;}if(!satisfied)next.push(ci);}children[value]=build(depth+1,next);ids[value]=trace[children[value]].node;}
   const nodeKey=depth+':'+ids.join(',');let node=unique.get(nodeKey);meter.pay('unit_unique_probe',4);if(node===undefined){node=nodes.length;nodes.push({depth,low:ids[0],high:ids[1]});unique.set(nodeKey,node);meter.pay('unit_node_emit',4);}entry={depth,active,steps:propagation.steps,kind:'split',children,node};
  }
  const index=trace.length;trace.push(entry);memo.set(key,index);meter.pay('unit_trace_emit',active.length+8+3*entry.steps.length);return index;
 }
 const rootTrace=build(0,source.hard.map((_,i)=>i)),root=trace[rootTrace].node;meter.pay('unit_export_words',4*nodes.length+trace.reduce((s,r)=>s+r.active.length+8+3*r.steps.length,0));return k.seal({version:'s10-unit-diagram-v1',source_id:source.id,features:source.features,variables:source.variables,order,trace,nodes,rootTrace,root,invoice:meter.record()});
}
function check(source,receipt,meter=new k.Meter()){
 k.admit(source,meter);k.checkSeal(receipt);assert.equal(receipt.version,'s10-unit-diagram-v1');assert.equal(receipt.source_id,source.id);assert.deepEqual(receipt.features,source.features);assert.equal(receipt.variables,source.variables);const {order,trace,nodes}=receipt,n=source.variables;assert.deepEqual([...order].sort((a,b)=>a-b),Array.from({length:n},(_,i)=>i+1));assert.deepEqual(nodes[0],{terminal:false});assert.deepEqual(nodes[1],{terminal:true});const position=Array(n+1),states=new Set();order.forEach((v,i)=>position[v]=i);
 for(let index=0;index<trace.length;index++){
  const r=trace[index],assigned=Array(n+1).fill(null);k.integer(r.depth);assert(r.depth<=n);assert.deepEqual(r.active,[...new Set(r.active)].sort((a,b)=>a-b));for(const ci of r.active){k.integer(ci);assert(ci<source.hard.length);}const key=r.depth+':'+r.active.join(',');assert(!states.has(key));states.add(key);k.integer(r.node);assert(r.node<nodes.length);meter.pay('unit_check_state',r.active.length+6);
  function residual(ci){assert(r.active.includes(ci));const remaining=[];let trueLiteral=false;for(const lit of source.hard[ci]){meter.pay('unit_check_reason_literal');const v=Math.abs(lit);if(position[v]<r.depth)continue;if(assigned[v]===null)remaining.push(lit);else if(assigned[v]===Number(lit>0))trueLiteral=true;}assert(!trueLiteral);return remaining;}
  for(const step of r.steps){k.integer(step.clause);assert.equal(residual(step.clause).length,1);assert.deepEqual(residual(step.clause),[step.literal]);const v=Math.abs(step.literal);assert(v>=1&&v<=n&&position[v]>=r.depth);assert.equal(assigned[v],null);assigned[v]=Number(step.literal>0);meter.pay('unit_check_step',4);}
  if(r.kind==='conflict'){assert.equal(residual(r.clause).length,0);assert.equal(r.node,0);}
  else if(r.kind==='true'){assert.equal(r.depth,n);assert.equal(r.active.length,0);assert.equal(r.node,1);}
  else{assert.equal(r.kind,'split');assert(r.depth<n);assert.equal(r.children.length,2);assert(r.node>1);const node=nodes[r.node],variable=order[r.depth];assert.equal(node.depth,r.depth);for(const value of [0,1]){const child=r.children[value],nodeChild=value?node.high:node.low;if(assigned[variable]!==null&&assigned[variable]!==value){assert.equal(child,null);assert.equal(nodeChild,0);continue;}k.integer(child);assert(child<index);const expected=[];for(const ci of r.active){let satisfied=false;for(const lit of source.hard[ci]){meter.pay('unit_check_child_literal');if(lit===(value?variable:-variable))satisfied=true;}if(!satisfied)expected.push(ci);}assert.equal(trace[child].depth,r.depth+1);assert.deepEqual(trace[child].active,expected);assert.equal(nodeChild,trace[child].node);}}
 }
 k.integer(receipt.rootTrace);assert(receipt.rootTrace<trace.length);const reached=new Set();function visit(i){if(reached.has(i))return;reached.add(i);const r=trace[i];if(r.kind==='split')for(const child of r.children)if(child!==null)visit(child);}visit(receipt.rootTrace);assert.equal(reached.size,trace.length);const top=trace[receipt.rootTrace];assert.equal(top.depth,0);assert.deepEqual(top.active,source.hard.map((_,i)=>i));assert.equal(top.node,receipt.root);const used=new Set([0,1]);for(const r of trace)used.add(r.node);assert.equal(used.size,nodes.length);
 for(let i=2;i<nodes.length;i++){const node=nodes[i];k.integer(node.depth);assert(node.depth<n);for(const child of [node.low,node.high]){k.integer(child);assert(child<i);if(child===1)assert.equal(node.depth,n-1);else if(child>1)assert.equal(nodes[child].depth,node.depth+1);}meter.pay('unit_check_node',7);}
 meter.pay('unit_retained_words',nodes.length*4+n+12);return {version:receipt.version,source_id:source.id,features:source.features,variables:n,order,nodes,root:receipt.root,receipt_id:receipt.id};
}
module.exports={compile,check};
