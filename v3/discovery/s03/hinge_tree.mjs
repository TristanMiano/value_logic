// Codex (GPT-6). DEVELOPMENT. Convex profiles for marginal-error lower values.
import assert from 'node:assert/strict';
import {F,add,sub,mul,div,cmp} from './rationals.mjs';
import {piece} from './biased_tree.mjs';
const eq=(a,b)=>cmp(a,b)===0,zero=()=>F(0),one=()=>F(1);
const line=(p,z)=>cmp(z,one())>=0?{a:zero(),d:zero()}:piece(p,z);
export function value(p,z){const t=line(p,z);return add(mul(t.a,z),t.d);}
const unique=a=>{a.sort(cmp);return a.filter((x,i)=>!i||!eq(x,a[i-1]));};
function push(p,t){if(!p.length||!eq(p.at(-1).a,t.a)||!eq(p.at(-1).d,t.d))p.push(t);}
function transform(p,error,c){
 let knots=[zero(),one(),...p.map(t=>t.lo)];for(const k of [...p.map(t=>t.lo),one()]){const z=sub(k,error);if(cmp(z,zero())>0&&cmp(z,one())<0)knots.push(z);}knots=unique(knots);
 const candidates=[];for(let i=0;i+1<knots.length;i++){
  const lo=knots[i],hi=knots[i+1],z=div(add(lo,hi),F(2)),y=line(p,z),t=line(p,add(z,error)),a=sub(y.a,t.a),d=sub(sub(y.d,c),add(t.d,mul(t.a,error)));
  if(cmp(a,zero())!==0){const crossing=div(mul(F(-1),d),a);if(cmp(crossing,lo)>0&&cmp(crossing,hi)<0)candidates.push(crossing);}
 }
 knots=unique([...knots,...candidates]);const result=[];
 for(let i=0;i+1<knots.length;i++){
  const lo=knots[i],z=div(add(lo,knots[i+1]),F(2)),y=line(p,z),t=line(p,add(z,error)),yes={lo,a:y.a,d:sub(y.d,c)},no={lo,a:t.a,d:add(t.d,mul(t.a,error))};
  push(result,cmp(add(mul(yes.a,z),yes.d),add(mul(no.a,z),no.d))>=0?yes:no);
 }assert(result.length<=p.length+2);return result;
}
function sumProfiles(ps,r){
 let a=mul(F(-1),r),d=r;const changes=[];for(const p of ps){a=add(a,p[0].a);d=add(d,p[0].d);for(let i=1;i<p.length;i++)changes.push({lo:p[i].lo,a:sub(p[i].a,p[i-1].a),d:sub(p[i].d,p[i-1].d)});}
 changes.sort((a,b)=>cmp(a.lo,b.lo));const result=[{lo:zero(),a,d}];for(let i=0;i<changes.length;){const lo=changes[i].lo;do{a=add(a,changes[i].a);d=add(d,changes[i].d);i++;}while(i<changes.length&&eq(changes[i].lo,lo));push(result,{lo,a,d});}return result;
}
export function compile(input){
 const n=input.parent.length,children=Array.from({length:n},()=>[]),profiles=Array(n),size=Array(n).fill(1);
 for(let v=1;v<n;v++){assert(input.parent[v]>=0&&input.parent[v]<v);assert(cmp(input.error[v],zero())>=0&&cmp(input.error[v],one())<=0&&cmp(input.c[v],zero())>=0);children[input.parent[v]].push(v);}
 for(const r of input.r)assert(cmp(r,zero())>=0);
 for(let v=n-1;v>=0;v--){profiles[v]=sumProfiles(children[v].map(u=>transform(profiles[u],input.error[u],input.c[u])),input.r[v]);for(const u of children[v])size[v]+=size[u];assert(profiles[v].length<=2*size[v]-1);}
 return {profiles,children,size};
}
export function recover(input,compiled,z){
 const selected=[],todo=[[0,z]];while(todo.length){const [v,current]=todo.pop();for(const u of compiled.children[v]){
  const yes=sub(value(compiled.profiles[u],current),input.c[u]),no=value(compiled.profiles[u],add(current,input.error[u]));
  if(cmp(yes,no)>=0){selected.push(u);todo.push([u,current]);}else todo.push([u,add(current,input.error[u])]);
 }}return selected.sort((a,b)=>a-b);
}
export function planValue(input,selected,z){
 const q=new Set(selected),load=[z];let score=zero();for(let v=0;v<input.parent.length;v++){
  if(v)load[v]=add(load[input.parent[v]],q.has(v)?zero():input.error[v]);const mag=sub(one(),load[v]);if(cmp(mag,zero())>0)score=add(score,mul(input.r[v],mag));if(q.has(v))score=sub(score,input.c[v]);
 }return score;
}
