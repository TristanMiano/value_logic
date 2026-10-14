'use strict';
// Actual finite complete branch proofs; no native solver status is trusted.
const assert=require('node:assert/strict'),k=require('./retained.cjs');
function validate(source,weights,meter){k.admit(source,meter);assert.equal(weights.length,source.features.length);weights.forEach(x=>k.integer(x));}
function cost(source,weights,assignment,meter){let value=0;for(let i=0;i<weights.length;i++){if(assignment[source.features[i]-1]===1)value+=weights[i];meter.pay('complete_partial_cost');}return value;}
function clauses(source,assignment,meter){let all=true;for(let i=0;i<source.hard.length;i++){let satisfied=false,open=false;for(const lit of source.hard[i]){const x=assignment[Math.abs(lit)-1];if(x===-1)open=true;else if(Boolean(x)===(lit>0))satisfied=true;meter.pay('complete_partial_literal');}if(!satisfied&&!open)return {conflict:i,all:false};if(!satisfied)all=false;}return {conflict:null,all};}
function ordering(source,meter){const degree=Array(source.variables).fill(0);for(const c of source.hard)for(const lit of c){degree[Math.abs(lit)-1]++;meter.pay('complete_order');}return degree.map((_,i)=>i).sort((i,j)=>degree[j]-degree[i]||i-j);}
function maskOf(assignment){return assignment.reduce((s,v,i)=>s+(v===1?2**i:0),0);}
function acquire(source,weights,incumbent,requestId,meter=new k.Meter(),cap=200000){
 validate(source,weights,meter);const first=k.modelFeatures(source,incumbent,meter);let best=k.sum(first.map((x,i)=>x*weights[i])),model=incumbent,nodes=0;
 const assignment=Array(source.variables).fill(-1),order=ordering(source,meter);
 function search(){if(++nodes>cap)throw new Error('Complete search cap');meter.pay('complete_search_node',2);const state=clauses(source,assignment,meter);if(state.conflict!==null)return;const lower=cost(source,weights,assignment,meter);if(lower>=best)return;if(state.all){best=lower;model=maskOf(assignment);return;}const v=order.find(i=>assignment[i]===-1);assert(v!==undefined);for(const t of [0,1]){assignment[v]=t;search();}assignment[v]=-1;}
 search();const budget=best-1;let proofNodes=0;
 function prove(){if(++proofNodes>cap)throw new Error('Complete proof cap');meter.pay('complete_proof_node',2);const state=clauses(source,assignment,meter);if(state.conflict!==null)return ['clause',state.conflict];if(cost(source,weights,assignment,meter)>budget)return ['bound'];const v=order.find(i=>assignment[i]===-1);assert(v!==undefined,'Claimed optimal value admits a cheaper model');assignment[v]=0;const left=prove();assignment[v]=1;const right=prove();assignment[v]=-1;return ['split',v,left,right];}
 const proof=prove();meter.pay('complete_export_words',proofNodes*3+weights.length+8);
 return k.seal({version:'s10-complete-v1',request_id:requestId,source_id:source.id,weights:[...weights],budget,lower:best,model,proof,search_nodes:nodes,proof_nodes:proofNodes,provider_invoice:meter.record()});
}
function check(source,weights,receipt,requestId,meter=new k.Meter()){
 validate(source,weights,meter);k.checkSeal(receipt);assert.equal(receipt.source_id,source.id);assert.equal(receipt.request_id,requestId);assert.deepEqual(receipt.weights,weights);k.integer(receipt.lower);assert.equal(receipt.budget,receipt.lower-1);
 const assignment=Array(source.variables).fill(-1);let nodes=0;
 function verify(node){assert(Array.isArray(node));nodes++;meter.pay('negative_check_node',2);
  if(node[0]==='clause'){assert.equal(node.length,2);k.integer(node[1]);const c=source.hard[node[1]];assert(c);for(const lit of c){const x=assignment[Math.abs(lit)-1];assert(x!==-1&&Boolean(x)!==(lit>0),'Conflict leaf is not falsified');meter.pay('negative_check_literal');}return;}
  if(node[0]==='bound'){assert.equal(node.length,1);let lower=0;for(let i=0;i<weights.length;i++){if(assignment[source.features[i]-1]===1)lower+=weights[i];meter.pay('negative_check_weight');}assert(lower>receipt.budget,'Objective leaf does not exclude budget');return;}
  assert.equal(node[0],'split');assert.equal(node.length,4);const v=node[1];k.integer(v);assert(v<source.variables&&assignment[v]===-1);assignment[v]=0;verify(node[2]);assignment[v]=1;verify(node[3]);assignment[v]=-1;
 }
 verify(receipt.proof);assert.equal(nodes,receipt.proof_nodes);const v=k.modelFeatures(source,receipt.model,meter),value=k.sum(v.map((x,i)=>x*weights[i]));assert.equal(value,receipt.lower);meter.pay('complete_receipt_binding',weights.length+12);return {model:receipt.model,optimum:value,nodes};
}
module.exports={acquire,check};
