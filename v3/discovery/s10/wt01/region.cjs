'use strict';
const assert=require('node:assert/strict'),k=require('./retained.cjs');
function component(x,y,l,u){if(x===0&&y===0)return 2*Math.min(0,u);if(x===1&&y===1)return -2*Math.max(0,l);return Math.min(u,-l);}
function bank(models,lo,hi,meter=new k.Meter()){
 const pairs=[];for(let j=0;j<models.length;j++)for(let z=j+1;z<models.length;z++){let value=0;for(let i=0;i<lo.length;i++){value+=3*component(models[j].v[i],models[z].v[i],lo[i],hi[i]);meter.pay('pair_floor_initial',6);}pairs.push({j,z,value});}meter.pay('pair_floor_retention',pairs.length*3+2*lo.length);return {pairs,lo:lo.slice(),hi:hi.slice()};
}
function update(bank,models,lo,hi,meter=new k.Meter()){
 for(let i=0;i<lo.length;i++)if(lo[i]!==bank.lo[i]||hi[i]!==bank.hi[i]){for(const pair of bank.pairs){pair.value+=3*(component(models[pair.j].v[i],models[pair.z].v[i],lo[i],hi[i])-component(models[pair.j].v[i],models[pair.z].v[i],bank.lo[i],bank.hi[i]));meter.pay('pair_floor_update',13);}bank.lo[i]=lo[i];bank.hi[i]=hi[i];}
 let best=null;for(const p of bank.pairs){if(!best||p.value>best.value)best=p;meter.pay('pair_floor_max',2);}return best;
}
function positive(models,action,lo,hi,query,tolerance,meter=new k.Meter()){
 let lower=0,upper=6*query.max;const i=query.coordinate;
 for(const v of models){let base=0;for(let j=0;j<lo.length;j++)if(j!==i){const d=action.a[j]-3*v.v[j];base+=d*(d>=0?hi[j]:lo[j]);meter.pay('positive_region_other',4);}const d=action.a[i]-3*v.v[i],slope=d*(d>=0?query.hi1:query.lo1);base+=d*(d>=0?query.hi0:query.lo0);meter.pay('positive_region_halfspace',7);if(slope===0){if(base>tolerance)return null;}else{const endpoint=6*(tolerance-base)/slope;assert(Number.isInteger(endpoint));if(slope>0)upper=Math.min(upper,endpoint);else lower=Math.max(lower,endpoint);if(lower>upper)return null;}}
 return {kind:'positive',lower,upper,action};
}
function negative(models,pair,lo,hi,query,tolerance,meter=new k.Meter()){
 const v=models[pair.j].v,w=models[pair.z].v,i=query.coordinate;let other=0;for(let j=0;j<lo.length;j++)if(j!==i){other+=3*component(v[j],w[j],lo[j],hi[j]);meter.pay('negative_region_other',6);}
 let terms;if(v[i]===0&&w[i]===0)terms=[[0,0],[2*query.hi0,2*query.hi1]];else if(v[i]===1&&w[i]===1)terms=[[0,0],[-2*query.lo0,-2*query.lo1]];else terms=[[query.hi0,query.hi1],[-query.lo0,-query.lo1]];
 const inequalities=terms.map(([base,slope])=>({left_coefficient:3*slope,right:2*tolerance-other-3*base}));meter.pay('negative_region_halfspaces',12);return {kind:'negative',pair:[models[pair.j].mask,models[pair.z].mask],indices:[pair.j,pair.z],inequalities,query,other};
}
function contains(region,t){if(region.kind==='positive')return region.lower<=6*t&&6*t<=region.upper;return region.inequalities.every(x=>x.left_coefficient*t>x.right);}
function queryMap(known,query,max){const i=query.coordinate,other=known[2*i+(query.kind==='true'?1:0)];if(query.kind==='true')return {coordinate:i,max,lo0:other===null?-max:-other,lo1:1,hi0:other===null?0:-other,hi1:1};return {coordinate:i,max,lo0:other===null?0:other,lo1:-1,hi0:other===null?max:other,hi1:-1};}
module.exports={component,bank,update,positive,negative,contains,queryMap};
