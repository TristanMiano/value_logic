'use strict';
// Original-source objective normalization and signed cube transport.
const assert=require('node:assert/strict'),k=require('./retained.cjs'),complete=require('./complete.cjs');
function normalize(source,q,meter=new k.Meter()){
 k.admit(source,meter);assert.equal(q.length,source.features.length);assert(source.features.length<=26);const flipVars=new Set();let flipMask=0,constant=0;
 q.forEach((w,i)=>{assert(Number.isSafeInteger(w));if(w<0){flipVars.add(source.features[i]);flipMask+=2**(source.features[i]-1);constant+=w;}meter.pay('signed_objective_normalization',4);});
 const hard=source.hard.map(c=>c.map(lit=>flipVars.has(Math.abs(lit))?-lit:lit));meter.pay('signed_clause_substitution',k.sum(hard.map(c=>c.length)));
 return {source:k.source(source.name+':flip'+flipMask,source.variables,hard,source.features),weights:q.map(Math.abs),constant,flipMask};
}
function acquire(source,q,incumbent,requestId,meter=new k.Meter()){
 const normalized=normalize(source,q,meter),provider=new k.Meter(),receipt=complete.acquire(normalized.source,normalized.weights,incumbent^normalized.flipMask,requestId,provider);meter.pay('signed_provider_invoice',provider.total());
 return k.seal({version:'s10-signed-v1',original_source_id:source.id,objective:q,normalization:normalized,receipt,invoice:meter.record()});
}
function check(source,q,bound,requestId,meter=new k.Meter()){
 k.checkSeal(bound);assert.equal(bound.original_source_id,source.id);assert.deepEqual(bound.objective,q);const normalized=normalize(source,q,meter);assert.deepEqual(bound.normalization,normalized);
 const checked=complete.check(normalized.source,normalized.weights,bound.receipt,requestId,meter),model=checked.model^normalized.flipMask,v=k.modelFeatures(source,model,meter),value=k.sum(v.map((x,i)=>x*q[i]));assert.equal(value,checked.optimum+normalized.constant);
 return {model,lower:value};
}
function cubes(source,bound,meter=new k.Meter()){
 k.checkSeal(bound);assert.equal(bound.original_source_id,source.id);const norm=normalize(source,bound.objective,meter);assert.deepEqual(norm,bound.normalization);k.checkSeal(bound.receipt);assert.equal(bound.receipt.source_id,norm.source.id);
 const assignment=Array(source.variables).fill(-1),leaves=[];let nodes=0;
 function walk(node){nodes++;meter.pay('cube_node',2);
  if(node[0]==='clause'){const c=norm.source.hard[node[1]];assert(c);for(const lit of c){const v=assignment[Math.abs(lit)-1];assert(v!==-1&&Boolean(v)!==(lit>0));meter.pay('cube_conflict_literal');}return;}
  if(node[0]==='bound'){let yes=0,no=0;source.features.forEach((variable,i)=>{const y=assignment[variable-1];if(y!==-1){const x=y^Number(Boolean(norm.flipMask&(2**(variable-1))));if(x)yes+=2**i;else no+=2**i;}meter.pay('cube_feature_projection',3);});leaves.push({yes,no});return;}
  assert.equal(node[0],'split');assert.equal(node.length,4);const v=node[1];k.integer(v);assert(v<source.variables&&assignment[v]===-1);assignment[v]=0;walk(node[2]);assignment[v]=1;walk(node[3]);assignment[v]=-1;
 }walk(bound.receipt.proof);assert.equal(nodes,bound.receipt.proof_nodes);assert(leaves.length>0);
 const unique=[...new Map(leaves.map(c=>[c.yes+':'+c.no,c])).values()],minimal=[];
 for(const c of unique){let subset=false;for(const d of unique){meter.pay('cube_subsumption_probe',3);if(c!==d&&(d.yes&c.yes)===d.yes&&(d.no&c.no)===d.no){subset=true;break;}}if(!subset)minimal.push(c);}
 meter.pay('cube_retention_words',2*minimal.length+source.features.length+8);
 return k.seal({version:'s10-signed-cubes-v1',source_id:source.id,features:source.features,proof_id:bound.id,raw_leaves:leaves.length,cubes:minimal});
}
function lower(cert,q,meter=new k.Meter()){
 let best=Infinity;for(const c of cert.cubes){let value=0;for(let i=0;i<q.length;i++){const bit=2**i;value+=(c.yes&bit)?q[i]:(c.no&bit)?0:Math.min(0,q[i]);meter.pay('signed_cube_lower',4);}best=Math.min(best,value);}return best;
}
function leafBounds(cert,a,m,lo,hi,meter=new k.Meter()){
 const values=[];for(const c of cert.cubes){let value=0;for(let i=0;i<a.length;i++){const bit=2**i;value+=(c.yes&bit)?-(m-a[i])*lo[i]:(c.no&bit)?a[i]*hi[i]:Math.max(a[i]*hi[i],-(m-a[i])*lo[i]);meter.pay('signed_cube_bound',5);}values.push(value);}return values;
}
function completion(cert,a,m,lo,hi,tau,i,meter=new k.Meter()){
 const values=leafBounds(cert,a,m,lo,hi,meter);let yes=0,no=0,free=0;
 cert.cubes.forEach((c,j)=>{const r=Math.max(0,values[j]-tau),bit=2**i;if(c.yes&bit)yes=Math.max(yes,r);else if(c.no&bit)no=Math.max(no,r);else free=Math.max(free,r);meter.pay('signed_completion_max',4);});
 return {yes,no,free,h:Math.max(a[i]*hi[i],-(m-a[i])*lo[i])};
}
function closes(r,a,m,lo,hi,i,t){return a[i]*(hi[i]-t)>=r.no&&(m-a[i])*(t-lo[i])>=r.yes&&Math.max(a[i]*t,-(m-a[i])*t)<=r.h-r.free;}
module.exports={normalize,acquire,check,cubes,lower,leafBounds,completion,closes};
