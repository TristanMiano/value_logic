// Codex (GPT-6). DEVELOPMENT. Exact rational affine profiles on [0,1].
import assert from 'node:assert/strict';
import {F,add,sub,mul,div,cmp} from './rationals.mjs';
const zero=()=>F(0),one=()=>F(1),same=(a,b)=>cmp(a,b)===0;
export function piece(p,x){let l=0,h=p.length;while(l+1<h){const m=(l+h)>>1;if(cmp(p[m].lo,x)<=0)l=m;else h=m;}return p[l];}
export function value(p,x){const t=piece(p,x);return add(mul(t.a,x),t.d);}
function unique(a){a.sort(cmp);return a.filter((x,i)=>!i||!same(x,a[i-1]));}
function push(p,v){if(!p.length||!same(p.at(-1).a,v.a)||!same(p.at(-1).d,v.d))p.push(v);}
function edgeProfile(p,b,c){
 let knots=[zero(),one(),...p.map(t=>t.lo)];if(cmp(b,zero())>0)for(const t of p){const k=div(t.lo,b);if(cmp(k,one())<0)knots.push(k);}
 knots=unique(knots);const crossing=[];
 for(let i=0;i+1<knots.length;i++){
  const lo=knots[i],hi=knots[i+1],x=div(add(lo,hi),F(2)),yes=piece(p,x),no=piece(p,mul(b,x)),a=sub(yes.a,mul(b,no.a)),d=sub(sub(yes.d,c),no.d);
  if(cmp(a,zero())!==0){const k=div(mul(F(-1),d),a);if(cmp(k,lo)>0&&cmp(k,hi)<0)crossing.push(k);}
 }
 knots=unique([...knots,...crossing]);const result=[];
 for(let i=0;i+1<knots.length;i++){
  const lo=knots[i],x=div(add(lo,knots[i+1]),F(2)),yes=piece(p,x),no=piece(p,mul(b,x));
  const y={lo,a:yes.a,d:sub(yes.d,c)},n={lo,a:mul(b,no.a),d:no.d};
  push(result,cmp(add(mul(y.a,x),y.d),add(mul(n.a,x),n.d))>=0?y:n);
 }
 assert(result.length<=p.length+1);return result;
}
function sumProfiles(profiles,r){
 let a=r,d=zero();const deltas=[];for(const p of profiles){a=add(a,p[0].a);d=add(d,p[0].d);for(let i=1;i<p.length;i++)deltas.push({lo:p[i].lo,a:sub(p[i].a,p[i-1].a),d:sub(p[i].d,p[i-1].d)});}
 deltas.sort((a,b)=>cmp(a.lo,b.lo));const result=[{lo:zero(),a,d}];
 for(let i=0;i<deltas.length;){const lo=deltas[i].lo;do{a=add(a,deltas[i].a);d=add(d,deltas[i].d);i++;}while(i<deltas.length&&same(lo,deltas[i].lo));push(result,{lo,a,d});}return result;
}
export function compile(input){
 const {parent,b,c,r}=input,n=parent.length,children=Array.from({length:n},()=>[]),size=Array(n).fill(1),profiles=Array(n);
 for(let v=1;v<n;v++){assert(parent[v]>=0&&parent[v]<v);assert(cmp(b[v],zero())>=0&&cmp(b[v],one())<=0&&cmp(c[v],zero())>=0);children[parent[v]].push(v);}for(const x of r)assert(cmp(x,zero())>=0);
 for(let v=n-1;v>=0;v--){const terms=[];for(const u of children[v]){terms.push(edgeProfile(profiles[u],b[u],c[u]));size[v]+=size[u];}profiles[v]=sumProfiles(terms,r[v]);assert(profiles[v].length<=size[v]);}
 return {profiles,children,size};
}
export function recover(input,compiled,x){
 const selected=[],todo=[[0,x]];while(todo.length){const [v,mag]=todo.pop();for(const u of compiled.children[v]){
  const p=compiled.profiles[u],yes=sub(value(p,mag),input.c[u]),no=value(p,mul(mag,input.b[u]));
  if(cmp(yes,no)>=0){selected.push(u);todo.push([u,mag]);}else todo.push([u,mul(mag,input.b[u])]);
 }}return selected.sort((a,b)=>a-b);
}
export function planValue(input,selected,x){
 const q=new Set(selected),mag=[x];let score=zero();for(let v=0;v<input.parent.length;v++){
  if(v)mag[v]=mul(mag[input.parent[v]],q.has(v)?one():input.b[v]);score=add(score,mul(input.r[v],mag[v]));if(q.has(v))score=sub(score,input.c[v]);
 }return score;
}
