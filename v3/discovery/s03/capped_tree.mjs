// Codex (GPT-6). DEVELOPMENT. Ordinary two-pass DP with integer interval bounds.
import assert from 'node:assert/strict';
export function macro({p4,k,c}){
  assert(Number.isSafeInteger(p4)&&p4>0&&p4<=4&&Number.isSafeInteger(k)&&k>0&&Number.isSafeInteger(c)&&c>=0);
  const d=4n**BigInt(k),q=d-BigInt(4-p4)**BigInt(k),p=BigInt(p4);
  return {a:q*p,b:BigInt(c)*4n*q,d:d*p};
}
export function term(m,x,D,up){
  const z=m.a*x-m.b*D;if(z<=0n)return 0n;return up?(z+m.d-1n)/m.d:z/m.d;
}
export function compile(prizes,anchors,edges,D){
  const n=prizes.length;assert(n>0&&anchors.length===n&&edges.length===n-1&&D>0n);
  for(const r of prizes)assert(Number.isSafeInteger(r)&&r>=0);
  const adj=Array.from({length:n},()=>[]),macros=edges.map(e=>macro(e[2])),am=anchors.map(a=>a===null?null:macro(a));
  edges.forEach(([u,v],j)=>{assert(u>=0&&u<n&&v>=0&&v<n&&u!==v);adj[u].push({u:v,j,out:2*j,in:2*j+1});adj[v].push({u,j,out:2*j+1,in:2*j});});
  const parent=Array(n).fill(null),order=[0];parent[0]=-1;
  for(const v of order)for(const e of adj[v])if(e.u!==parent[v]){assert(parent[e.u]===null);parent[e.u]=v;order.push(e.u);}assert(order.length===n);
  const lo=Array(2*edges.length),hi=Array(2*edges.length),scores=Array(n),totals=Array(n);
  for(const v of order.toReversed()){
    let l=BigInt(prizes[v])*D,h=l;
    for(const e of adj[v])if(e.u!==parent[v]){l+=term(macros[e.j],lo[e.in],D,false);h+=term(macros[e.j],hi[e.in],D,true);}
    if(parent[v]!==-1){const e=adj[v].find(e=>e.u===parent[v]);lo[e.out]=l;hi[e.out]=h;}
  }
  for(const v of order){
    let l=BigInt(prizes[v])*D,h=l;
    for(const e of adj[v]){l+=term(macros[e.j],lo[e.in],D,false);h+=term(macros[e.j],hi[e.in],D,true);}
    totals[v]=[l,h];scores[v]=am[v]===null?[0n,0n]:[term(am[v],l,D,false),term(am[v],h,D,true)];
    for(const e of adj[v])if(e.u!==parent[v]){lo[e.out]=l-term(macros[e.j],lo[e.in],D,false);hi[e.out]=h-term(macros[e.j],hi[e.in],D,true);}
  }
  let root=-1,lower=0n,upper=0n;for(let v=0;v<n;v++){assert(scores[v][1]-scores[v][0]<=BigInt(n));if(scores[v][0]>lower){lower=scores[v][0];root=v;}if(scores[v][1]>upper)upper=scores[v][1];}
  assert(upper-lower<=BigInt(n));return {D,root,lower,upper,scores,lo,hi,totals,adj,macros,am};
}
export function policy(plan){
  if(plan.root<0)return {root:-1,edges:[],vertices:[]};const edges=[],vertices=[plan.root],parent=new Map([[plan.root,-1]]);
  for(const v of vertices)for(const e of plan.adj[v])if(e.u!==parent.get(v)&&term(plan.macros[e.j],plan.lo[e.in],plan.D,false)>0n){edges.push(e.j);vertices.push(e.u);parent.set(e.u,v);}
  return {root:plan.root,edges,vertices};
}
