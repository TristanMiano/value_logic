'use strict';
// Ordinary layered OBDD with a source-equivalence trace, signed min-marginals.
const assert=require('node:assert/strict'),k=require('./retained52.cjs');
function variableOrder(source,meter=new k.Meter()){
 const degree=Array(source.variables).fill(0);for(const c of source.hard)for(const lit of c){degree[Math.abs(lit)-1]++;meter.pay('diagram_order_literal');}
 return degree.map((_,i)=>i+1).sort((i,j)=>degree[j-1]-degree[i-1]||i-j);
}
function compile(source,meter=new k.Meter(),cap=100000){
 k.admit(source,meter);const order=variableOrder(source,meter),position=Array(source.variables+1);order.forEach((v,i)=>position[v]=i);
 const trace=[],nodes=[{terminal:false},{terminal:true}],memo=new Map(),unique=new Map();let probes=0;
 function build(depth,active){
  meter.pay('diagram_state_key',active.length+2);const key=depth+':'+active.join(',');if(memo.has(key)){meter.pay('diagram_memo_hit');return memo.get(key);}
  if(++probes>cap)throw new Error('Diagram compilation state cap');let conflict=null;
  for(const ci of active){let open=false;for(const lit of source.hard[ci]){if(position[Math.abs(lit)]>=depth)open=true;meter.pay('diagram_residual_literal');}if(!open){conflict=ci;break;}}
  let entry;if(conflict!==null)entry={depth,active,kind:'conflict',clause:conflict,node:0};
  else if(depth===order.length){assert.equal(active.length,0);entry={depth,active,kind:'true',node:1};}
  else {
   const variable=order[depth],children=[];
   for(const value of [0,1]){const next=[];for(const ci of active){let satisfied=false;for(const lit of source.hard[ci]){if(Math.abs(lit)===variable&&(lit>0)===Boolean(value))satisfied=true;meter.pay('diagram_child_literal');}if(!satisfied)next.push(ci);}children.push(build(depth+1,next));}
   const low=trace[children[0]].node,high=trace[children[1]].node,nodeKey=depth+':'+low+':'+high;let node=unique.get(nodeKey);meter.pay('diagram_unique_probe',4);
   if(node===undefined){node=nodes.length;nodes.push({depth,low,high});unique.set(nodeKey,node);meter.pay('diagram_node_emit',4);}
   entry={depth,active,kind:'split',children,node};
  }
  const id=trace.length;trace.push(entry);memo.set(key,id);meter.pay('diagram_trace_emit',active.length+8);return id;
 }
 const rootTrace=build(0,source.hard.map((_,i)=>i)),root=trace[rootTrace].node;meter.pay('diagram_export_words',nodes.length*4+trace.reduce((s,r)=>s+r.active.length+8,0));
 return k.seal({version:'s10-layered-diagram-v1',source_id:source.id,features:source.features,variables:source.variables,order,trace,nodes,rootTrace,root,invoice:meter.record()});
}
function check(source,receipt,meter=new k.Meter()){
 k.admit(source,meter);k.checkSeal(receipt);assert.equal(receipt.source_id,source.id);assert.deepEqual(receipt.features,source.features);assert.equal(receipt.variables,source.variables);
 const {order,trace,nodes}=receipt,n=source.variables;assert.equal(order.length,n);assert.deepEqual([...order].sort((a,b)=>a-b),Array.from({length:n},(_,i)=>i+1));assert.deepEqual(nodes[0],{terminal:false});assert.deepEqual(nodes[1],{terminal:true});
 const position=Array(n+1);order.forEach((v,i)=>position[v]=i);const seen=new Set();
 for(let index=0;index<trace.length;index++){
  const r=trace[index];k.integer(r.depth);assert(r.depth<=n);assert.deepEqual(r.active,[...new Set(r.active)].sort((a,b)=>a-b));r.active.forEach(ci=>{k.integer(ci);assert(ci<source.hard.length);});k.integer(r.node);assert(r.node<nodes.length);meter.pay('diagram_check_state',r.active.length+6);
  const key=r.depth+':'+r.active.join(',');assert(!seen.has(key));seen.add(key);
  if(r.kind==='conflict'){assert(r.active.includes(r.clause));for(const lit of source.hard[r.clause]){assert(position[Math.abs(lit)]<r.depth);meter.pay('diagram_check_conflict_literal');}assert.equal(r.node,0);}
  else if(r.kind==='true'){assert.equal(r.depth,n);assert.equal(r.active.length,0);assert.equal(r.node,1);}
  else {
   assert.equal(r.kind,'split');assert(r.depth<n);assert.equal(r.children.length,2);const node=nodes[r.node];assert.equal(node.depth,r.depth);
   for(let t=0;t<2;t++){
    const child=r.children[t];k.integer(child);assert(child<index);const expected=r.active.filter(ci=>{let satisfied=false;for(const lit of source.hard[ci]){if(lit===(t?1:-1)*order[r.depth])satisfied=true;meter.pay('diagram_check_child_literal');}return !satisfied;});
    assert.equal(trace[child].depth,r.depth+1);assert.deepEqual(trace[child].active,expected);assert.equal(node[t?'high':'low'],trace[child].node);
   }
  }
 }
 const reached=new Set();function visit(id){if(reached.has(id))return;reached.add(id);const r=trace[id];if(r.kind==='split')r.children.forEach(visit);}k.integer(receipt.rootTrace);assert(receipt.rootTrace<trace.length);visit(receipt.rootTrace);assert.equal(reached.size,trace.length);
 const top=trace[receipt.rootTrace];assert.equal(top.depth,0);assert.deepEqual(top.active,source.hard.map((_,i)=>i));assert.equal(top.node,receipt.root);
 const reachableNodes=new Set([0,1]);for(const r of trace)reachableNodes.add(r.node);assert.equal(reachableNodes.size,nodes.length);
 for(let id=2;id<nodes.length;id++){const v=nodes[id];k.integer(v.depth);assert(v.depth<n);for(const child of [v.low,v.high]){k.integer(child);assert(child<id);if(child===1)assert.equal(v.depth,n-1);else if(child>1)assert.equal(nodes[child].depth,v.depth+1);}meter.pay('diagram_check_node',7);}
 meter.pay('diagram_retained_words',nodes.length*4+n+12);return {version:receipt.version,source_id:source.id,features:source.features,variables:n,order,nodes,root:receipt.root,receipt_id:receipt.id};
}
function evaluate(diagram,q,meter=new k.Meter(),marginals=true){
 assert.equal(q.length,diagram.features.length);q.forEach(x=>assert(Number.isSafeInteger(x)));const weights=Array(diagram.variables+1).fill(0);diagram.features.forEach((v,i)=>weights[v]=q[i]);
 const {nodes,order}=diagram,back=Array(nodes.length).fill(Infinity),choice=Array(nodes.length).fill(0);back[1]=0;
 for(let id=2;id<nodes.length;id++){const v=nodes[id],left=back[v.low],right=weights[order[v.depth]]+back[v.high];choice[id]=Number(right<left);back[id]=Math.min(left,right);meter.pay('diagram_backward',6);}
 assert(Number.isFinite(back[diagram.root]));let model=0,id=diagram.root;
 while(id>1){const v=nodes[id],t=choice[id];if(t)model+=2**(order[v.depth]-1);id=t?v.high:v.low;meter.pay('diagram_witness_step',4);}assert.equal(id,1);
 if(!marginals)return {lower:back[diagram.root],model};
 const forward=Array(nodes.length).fill(Infinity),all=order.map(()=>[Infinity,Infinity]);forward[diagram.root]=0;
 // Every child was emitted before its parents; reverse ID order is topological.
 for(let at=nodes.length-1;at>=2;at--){const v=nodes[at];for(let t=0;t<2;t++){const child=t?v.high:v.low,cost=forward[at]+t*weights[order[v.depth]];forward[child]=Math.min(forward[child],cost);all[v.depth][t]=Math.min(all[v.depth][t],cost+back[child]);meter.pay('diagram_forward_marginal',7);}}
 const position=Array(diagram.variables+1);order.forEach((v,i)=>position[v]=i);const featureMarginals=diagram.features.map(v=>all[position[v]].map(x=>Number.isFinite(x)?x:null));meter.pay('diagram_marginal_export',2*q.length+8);
 return {lower:back[diagram.root],model,marginals:featureMarginals};
}
function bound(diagram,a,m,lo,hi,meter=new k.Meter(),marginals=true){
 const q=a.map((x,i)=>x*hi[i]+(m-x)*lo[i]),A=k.sum(a.map((x,i)=>x*hi[i]));meter.pay('diagram_induced_objective',5*a.length);const result=evaluate(diagram,q,meter,marginals);return {...result,q,A,regret:A-result.lower};
}
function after(bound,a,m,hi,i,t,meter=new k.Meter()){
 const [M0,M1]=bound.marginals[i],base=bound.A-a[i]*hi[i],terms=[];if(M0!==null)terms.push(base+a[i]*t-M0);if(M1!==null)terms.push(base-(m-a[i])*t-(M1-bound.q[i]));meter.pay('diagram_response_regret',10);assert(terms.length);return Math.max(...terms);
}
module.exports={variableOrder,compile,check,evaluate,bound,after};
