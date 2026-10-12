// Codex (GPT-6). DEVELOPMENT portability amendment. All numerical values exact.
import fs from 'node:fs';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
const integer=x=>{assert(Number.isSafeInteger(x));return x;};
export function solve(prizes,anchors,edges){
  const n=prizes.length;assert(n>0&&anchors.length===n&&edges.length===n-1);
  prizes.forEach(x=>assert(integer(x)>=0));anchors.forEach(x=>assert(x===null||integer(x)>=0));
  const adj=Array.from({length:n},()=>[]);
  edges.forEach(([u,v,c],j)=>{assert(u>=0&&u<n&&v>=0&&v<n&&u!==v&&integer(c)>=0);adj[u].push([v,j,c]);adj[v].push([u,j,c]);});
  const parent=Array(n).fill(null),order=[0];parent[0]=-1;
  for(const v of order)for(const [u] of adj[v])if(u!==parent[v]){assert(parent[u]===null);parent[u]=v;order.push(u);}
  assert(order.length===n);
  const rec=[[null,null,null]],states=Array(n);
  const node=(val,left=0,right=0,action=null)=>{rec.push([left,right,action]);return [integer(val),rec.length-1];};
  const pick=(...opts)=>opts.filter(x=>x!==null).reduce((a,b)=>a===null||b[0]>a[0]?b:a,null);
  const join=(a,b,j=null,c=0)=>a===null||b===null?null:node(a[0]+b[0]-c,a[1],b[1],j===null?null:['edge',j]);
  for(const v of order.toReversed()){
    let N=[0,0],U=node(prizes[v]),A=anchors[v]===null?null:node(prizes[v]-anchors[v],0,0,['anchor',v]);
    for(const [u,j,c] of adj[v])if(parent[u]===v){
      const [nc,uc,ac]=states[u],closed=pick(nc,ac);
      [N,U,A]=[join(N,closed),pick(join(U,closed),join(U,uc,j,c)),pick(join(A,closed),join(A,uc,j,c),join(A,ac,j,c),join(U,ac,j,c))];
    }
    states[v]=[N,U,A];
  }
  const [value,ref]=pick(states[0][0],states[0][2]),es=[],as=[],stack=[ref];
  while(stack.length){const k=stack.pop();if(k===0)continue;const [l,r,a]=rec[k];stack.push(l,r);if(a)(a[0]==='edge'?es:as).push(a[1]);}
  return {value,edges:es.sort((a,b)=>a-b),anchors:as.sort((a,b)=>a-b),states:states.map(s=>s.map(x=>x===null?null:x[0])),records:rec.length};
}
export function check(prizes,anchors,edges,plan){
  const parent=prizes.map((_,i)=>i);const root=v=>{while(parent[v]!==v){parent[v]=parent[parent[v]];v=parent[v];}return v;};
  assert(new Set(plan.edges).size===plan.edges.length&&new Set(plan.anchors).size===plan.anchors.length);
  let cost=0;for(const j of plan.edges){assert(j>=0&&j<edges.length);const [u,v,c]=edges[j];parent[root(u)]=root(v);cost+=c;}
  const known=new Set();for(const v of plan.anchors){assert(anchors[v]!==null);known.add(root(v));cost+=anchors[v];}
  const covered=prizes.map((_,i)=>i).filter(v=>known.has(root(v)));const reward=covered.reduce((a,v)=>a+prizes[v],0),value=integer(reward-cost);
  if('value' in plan)assert(value===plan.value);return {value,reward,cost:integer(cost),covered};
}
export function predict(n,edges,plan,el,al,flip){
  assert(flip===0||flip===1);const adj=Array.from({length:n},()=>[]),rel=Array(n).fill(null),guess=Array(n);
  for(const j of plan.edges){const [u,v]=edges[j],y=el[j];assert(y===0||y===1);adj[u].push([v,y]);adj[v].push([u,y]);}
  for(let v=0;v<n;v++)if(rel[v]===null){
    rel[v]=0;const component=[v];for(const u of component)for(const [z,y] of adj[u])if(rel[z]===null){rel[z]=rel[u]^y;component.push(z);}else assert(rel[z]===(rel[u]^y));
    const offsets=new Set(component.filter(u=>Object.hasOwn(al,u)).map(u=>rel[u]^al[u]));assert(offsets.size<=1);const offset=offsets.size?[...offsets][0]:flip;
    for(const u of component)guess[u]=rel[u]^offset;
  }return guess;
}
function bellman(weights,anchors,edges){
  const n=weights.length,queries=anchors.flatMap((c,v)=>c===null?[]:[[1<<v,c]]).concat(edges.map(([u,v,c])=>[(1<<u)|(1<<v),c]));
  const parity=x=>{let y=0;while(x){y^=1;x&=x-1;}return y;};const memo=new Map();
  function best(worlds){
    const key=worlds.join(',');if(memo.has(key))return memo.get(key);let value=0;
    for(let v=0;v<n;v++){let ones=0;for(const x of worlds)ones+=(x>>v)&1;value+=weights[v]*Math.max(ones,worlds.length-ones)/worlds.length;}
    integer(value);
    for(const [mask,c] of queries){const zero=worlds.filter(x=>!parity(x&mask)),one=worlds.filter(x=>parity(x&mask));if(!zero.length||!one.length)continue;
      const trial=integer(-c+(zero.length*best(zero)+one.length*best(one))/worlds.length);value=Math.max(value,trial);
    }memo.set(key,value);return value;
  }return {value:best(Array.from({length:1<<n},(_,i)=>i)),states:memo.size};
}
if(process.argv[1]&&new URL(import.meta.url).pathname.replace(/^\//,'').toLowerCase()===process.argv[1].replaceAll('\\','/').toLowerCase()){
  const [inputPath,outPath]=process.argv.slice(2);assert(!fs.existsSync(outPath));const start=process.hrtime.bigint(),input=JSON.parse(fs.readFileSync(inputPath,'utf8'));
  const hash=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
  assert(hash(new URL('graph_node.mjs',import.meta.url))===input.sources['graph_node.mjs']);
  const results=[];let subsetChecks=0,worldChecks=0;
  for(const c of input.cases){
    const {n,prizes,anchors,edges}=c,weights=prizes.map(x=>2*x),base=prizes.reduce((a,b)=>a+b,0),plan=solve(prizes,anchors,edges),checked=check(prizes,anchors,edges,plan);
    const available=anchors.flatMap((x,v)=>x===null?[]:[v]);let optimum=0;
    for(let bits=0;bits<(1<<(edges.length+available.length));bits++){
      const p={edges:edges.flatMap((_,j)=>(bits>>j)&1?[j]:[]),anchors:available.filter((_,j)=>(bits>>(j+edges.length))&1)};
      optimum=Math.max(optimum,check(prizes,anchors,edges,p).value);subsetChecks++;
    }assert(optimum===plan.value);const adaptive=c.index<12?bellman(weights,anchors,edges):null;if(adaptive)assert(adaptive.value===base+optimum);
    for(let x=0;x<(1<<n);x++){
      const el=Object.fromEntries(plan.edges.map(j=>[j,((x>>edges[j][0])^(x>>edges[j][1]))&1])),al=Object.fromEntries(plan.anchors.map(v=>[v,(x>>v)&1]));let twice=0;
      for(const flip of [0,1]){const g=predict(n,edges,plan,el,al,flip);for(let v=0;v<n;v++)if(g[v]===((x>>v)&1))twice+=weights[v];}
      assert(twice/2-checked.cost===base+optimum);worldChecks++;
    }results.push({index:c.index,scale:c.scale,plan,checked,adaptive});
  }
  const large=[];for(const c of input.large){let t=process.hrtime.bigint();const plan=solve(c.prizes,c.anchors,c.edges),solve_ns=Number(process.hrtime.bigint()-t);t=process.hrtime.bigint();const checked=check(c.prizes,c.anchors,c.edges,plan),check_ns=Number(process.hrtime.bigint()-t);large.push({shape:c.shape,scale:c.scale,source_ns:c.source_ns,plan,checked,solve_ns,check_ns});}
  const result={status:'complete',evidence:'DEVELOPMENT; explicit implementation amendment after exhausted Python retry',contributor:'Codex (GPT-6)',node:process.version,sources:input.sources,input_sha256:hash(inputPath),seed:input.seed,results,subsetChecks,worldChecks,large,elapsed_ns:Number(process.hrtime.bigint()-start),limits:'Identical ordinary tree DP. Supplied synthetic exact query prices, no real acquisition or model authentication billed. Original two failures retained.'};
  fs.writeFileSync(outPath,JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify({status:result.status,cases:results.length,subsetChecks,worldChecks,beliefStates:results.reduce((a,c)=>a+(c.adaptive?.states??0),0),large:large.map(c=>({shape:c.shape,gain:c.plan.value/c.scale,covered:c.checked.covered.length,anchors:c.plan.anchors.length,edges:c.plan.edges.length,source_ns:c.source_ns,solve_ns:c.solve_ns,check_ns:c.check_ns})),elapsed_ns:result.elapsed_ns}));
}
