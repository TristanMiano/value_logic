'use strict';
const assert=require('node:assert/strict'),k=require('./retained.cjs');
const VALUES=[-4,-2,0,2,4],MULT=[1,2,3,2,1],W=9n;
function problem(models,action,fees,C,tolerance,meter=new k.Meter()){
 const active=[];for(let j=0;j<models.length;j++){const d=action.a.map((x,i)=>x-action.m*models[j].v[i]),r=4*k.sum(d.map(Math.abs))-tolerance;meter.pay('residual_initial_competitor',4*d.length+2);if(r>0)active.push({model:j,d,r});}
 const relevant=action.a.map((_,i)=>new Set(models.map(x=>x.v[i])).size===2?i:null).filter(x=>x!==null);meter.pay('residual_relevance',models.length*action.a.length);
 const deltas=action.a.map((_,i)=>VALUES.map(t=>active.map(c=>{meter.pay('residual_delta_compile',4);return 4*Math.abs(c.d[i])-c.d[i]*t;})));
 meter.pay('residual_table_retention',active.length+action.a.length*5*active.length+fees.length+8);return {initial:active.map(c=>c.r),active:active.map(c=>c.model),deltas,fees,C,relevant,variables:action.a.length};
}
function update(p,residual,i,valueIndex,meter=new k.Meter()) {return residual.map((r,j)=>{meter.pay('residual_update',3);return Math.max(0,r-p.deltas[i][valueIndex][j]);});}
function closed(residual){return residual.every(x=>x===0);}
function fallback(p,mask,meter=new k.Meter()){let remaining=0;for(const i of p.relevant){if(!(mask&(1<<i)))remaining+=p.fees[i];meter.pay('residual_fallback_quote',2);}return Math.min(p.C,remaining);}
function orders(p,meter=new k.Meter()){
 const gain=p.relevant.map(i=>({i,gain:k.sum(VALUES.map((_,t)=>MULT[t]*k.sum(p.initial.map((r,j)=>Math.min(r,p.deltas[i][t][j])))))}));meter.pay('residual_order_score',p.relevant.length*5*p.initial.length*3);
 const candidate=[gain.slice().sort((a,b)=>b.gain*p.fees[a.i]-a.gain*p.fees[b.i]||a.i-b.i).map(x=>x.i),p.relevant.slice().sort((i,j)=>p.fees[i]-p.fees[j]||i-j),p.relevant.slice()];return [...new Map(candidate.map(x=>[x.join(','),x])).values()];
}
function prefix(p,order,meter=new k.Meter(),cap=20000){
 let states=new Map([[p.initial.join(','),{r:p.initial,mass:1n}]]),den=1n,charge=0n,mask=0,spent=0,generated=1;let best={num:BigInt(closed(p.initial)?0:p.C),den:1n,length:0,order:[],open_num:closed(p.initial)?0n:1n},levels=[{depth:0,num:String(best.num),den:'1',states:closed(p.initial)?0:1}],stopped=null;
 if(closed(p.initial))return {...best,levels,generated,stopped};
 for(let depth=0;depth<order.length;depth++){
  const i=order[depth];assert(p.relevant.includes(i));assert(!(mask&(1<<i)));if(spent+p.fees[i]>p.C){stopped='prequery_budget';break;}const next=new Map();let capHit=false,oldMass=0n;for(const state of states.values())oldMass+=state.mass;
  outer:for(const state of states.values())for(let t=0;t<VALUES.length;t++){
   const r=update(p,state.r,i,t,meter);meter.pay('prefix_probability_transition',5);if(closed(r))continue;const key=r.join(','),existing=next.get(key);if(existing)existing.mass+=state.mass*BigInt(MULT[t]);else{if(++generated>cap){capHit=true;break outer;}next.set(key,{r,mass:state.mass*BigInt(MULT[t])});meter.pay('prefix_state_emit',r.length+3);}
  }
  if(capHit){stopped='state_cap_partial_depth_discarded';break;}charge=charge*W+BigInt(p.fees[i])*oldMass*W;den*=W;mask|=1<<i;spent+=p.fees[i];let open=0n;for(const state of next.values())open+=state.mass;const num=charge+BigInt(fallback(p,mask,meter))*open;levels.push({depth:depth+1,num:String(num),den:String(den),states:next.size,open_num:String(open)});
  meter.pay('prefix_value_compare',5);if(num*best.den<best.num*den)best={num,den,length:depth+1,order:order.slice(0,depth+1),open_num:open};states=next;if(!states.size)break;
 }
 meter.pay('prefix_plan_retention',best.order.length+levels.length*5+8);return {...best,levels,generated,stopped};
}
function bestPrefix(p,provided,meter=new k.Meter(),cap=20000){const plans=provided.map(order=>prefix(p,order,meter,cap));return {best:plans.reduce((best,p)=>p.num*best.den<best.num*p.den?p:best),plans};}
function adaptive(p,meter=new k.Meter(),options={depth:3,cap:100000}){
 const cache=new Map(),powers=Array.from({length:p.relevant.length+1},(_,i)=>W**BigInt(i));let generated=0,capped=false;
 function visit(mask,residual,spent,depth){const unknown=p.relevant.filter(i=>!(mask&(1<<i))),den=powers[unknown.length],key=mask+':'+depth+':'+residual.join(',');meter.pay('adaptive_state_key',residual.length+4);if(cache.has(key)){meter.pay('adaptive_memo_hit');return cache.get(key);}if(closed(residual))return {num:0n,den,query:'stop'};
  let best={num:BigInt(fallback(p,mask,meter))*den,den,query:'fallback'};if(depth===0)return best;if(generated>=options.cap){capped=true;return {...best,capped:true};}generated++;
  for(const i of unknown)if(spent+p.fees[i]<=p.C){let num=BigInt(p.fees[i])*den;for(let t=0;t<VALUES.length;t++){const r=update(p,residual,i,t,meter),child=visit(mask|(1<<i),r,spent+p.fees[i],depth-1);assert.equal(child.den*W,den);num+=BigInt(MULT[t])*child.num;meter.pay('adaptive_probability_sum',4);}meter.pay('adaptive_query_compare',3);if(num<best.num)best={num,den,query:i};}
  cache.set(key,best);meter.pay('adaptive_policy_retention',residual.length+8);return best;
 }
 const root=visit(0,p.initial,0,options.depth);return {root,cache,generated,capped,depth:options.depth,powers};
}
function serial(x){return JSON.parse(JSON.stringify(x,(_,v)=>typeof v==='bigint'?v.toString():v instanceof Map?[...v]:v));}
module.exports={VALUES,MULT,problem,update,closed,fallback,orders,prefix,bestPrefix,adaptive,serial};
