// Codex (GPT-6). DEVELOPMENT: checked receipt attempts, not truth-valued failures.
import fs from 'node:fs';import crypto from 'node:crypto';import assert from 'node:assert/strict';
const out=process.argv[2];assert(out&&!fs.existsSync(out));const start=process.hrtime.bigint();
const seed=81497;let state=seed;const rand=n=>{state=(Math.imul(state,1664525)+1013904223)>>>0;return state%n;};
const exact=x=>{assert(Number.isSafeInteger(x));return x;};
const pop=x=>{let n=0;while(x){x&=x-1;n++;}return n;};
function planners(prizes,queries,explicit){
  const n=prizes.length,m=queries.length,Q=8**m,base=prizes.reduce((a,b)=>a+b,0)*Q,all=(1<<m)-1,rewards=new Map();
  function reward(K){
    if(rewards.has(K))return rewards.get(K);const parent=Array.from({length:n+1},(_,i)=>i);
    const root=v=>{while(parent[v]!==v){parent[v]=parent[parent[v]];v=parent[v];}return v;};
    queries.forEach((q,j)=>{if((K>>j)&1)parent[root(q.u)]=root(q.v);});
    let value=0;for(let v=0;v<n;v++)if(root(v)===root(n))value+=prizes[v]*Q;rewards.set(K,value);return value;
  }
  const memo=new Map(),policy=new Map();const key=(K,R)=>K+','+R;
  function best(K,R){
    const k=key(K,R);if(memo.has(k))return memo.get(k);let value=reward(K),action=-1;
    for(let j=0;j<m;j++)if((R>>j)&1){const q=queries[j],next=R^(1<<j),s=best(K|(1<<j),next),f=best(K,next);assert(s>=f);
      const trial=exact(-q.c*Q+(q.lo*s+(4-q.lo)*f)/4);if(trial>value){value=trial;action=j;}
    }memo.set(k,value);policy.set(k,action);return value;
  }
  const value=best(0,all),adversarial=new Map();
  function evaluate(K,R){
    const k=key(K,R);if(adversarial.has(k))return adversarial.get(k);const action=policy.get(k);let value;
    if(action===-1)value=reward(K);else{const q=queries[action],next=R^(1<<action),s=evaluate(K|(1<<action),next),f=evaluate(K,next);
      const ev=p=>exact(-q.c*Q+(p*s+(4-p)*f)/4);value=Math.min(ev(q.lo),ev(q.hi));
    }adversarial.set(k,value);return value;
  }
  const robust=evaluate(0,all);assert(robust===value);
  let fixed=0,fixedSet=0,batchOutcomes=0;
  for(let B=0;B<=all;B++){
    let cost=0;queries.forEach((q,j)=>{if((B>>j)&1)cost+=q.c*Q;});let expected=0;
    for(let S=B;;S=(S-1)&B){let probability=1;queries.forEach((q,j)=>{if((B>>j)&1)probability*=((S>>j)&1)?q.lo:4-q.lo;});expected+=exact(probability*reward(S)/4**pop(B));batchOutcomes++;if(S===0)break;}
    const trial=expected-cost;if(trial>fixed){fixed=trial;fixedSet=B;}
  }assert(value>=fixed);
  let worldValue=null,worldStates=0;
  if(explicit){
    const wm=new Map();const parity=x=>pop(x)&1;
    function wb(worlds,R){
      const k=worlds.join(',')+'|'+R;if(wm.has(k))return wm.get(k);let value=0;
      for(let v=0;v<n;v++){let ones=0;for(const x of worlds)ones+=(x>>v)&1;value+=2*prizes[v]*Q*Math.max(ones,worlds.length-ones)/worlds.length;}exact(value);
      for(let j=0;j<m;j++)if((R>>j)&1){const q=queries[j],next=R^(1<<j),mask=(1<<q.u)^(q.v===n?0:1<<q.v),zero=worlds.filter(x=>!parity(x&mask)),one=worlds.filter(x=>parity(x&mask));
        let success=0;if(zero.length)success+=zero.length*wb(zero,next)/worlds.length;if(one.length)success+=one.length*wb(one,next)/worlds.length;
        const trial=exact(-q.c*Q+(q.lo*success+(4-q.lo)*wb(worlds,next))/4);value=Math.max(value,trial);
      }wm.set(k,value);return value;
    }worldValue=wb(Array.from({length:1<<n},(_,i)=>i),all);worldStates=wm.size;assert(worldValue===base+value);
  }
  return {scale:Q,gain:value,fixedGain:fixed,fixedSet,rootAction:policy.get(key(0,all)),robustGain:robust,states:memo.size,batchOutcomes,worldValue,worldStates};
}
const cases=[];
for(let k=0;k<24;k++){
  const n=2+rand(3),prizes=Array.from({length:n},()=>1+rand(12)),queries=[];
  for(let v=0;v<n;v++)if(rand(5)!==0){const lo=1+rand(4);queries.push({u:v,v:n,c:rand(16),lo,hi:Math.min(4,lo+1)});}
  for(let v=1;v<n;v++){const u=rand(v),lo=1+rand(4);queries.push({u,v,c:rand(10),lo,hi:Math.min(4,lo+1)});}
  cases.push({index:k,prizes,queries,result:planners(prizes,queries,k<12)});
}
const separation={prizes:[100,100],queries:[{u:0,v:2,c:150,lo:4,hi:4},{u:0,v:1,c:4,lo:2,hi:4}]};
separation.result=planners(separation.prizes,separation.queries,true);assert(separation.result.gain===21*separation.result.scale&&separation.result.fixedGain===0);
function permutations(a){if(a.length===0)return [[]];return a.flatMap((x,i)=>permutations(a.filter((_,j)=>j!==i)).map(p=>[x,...p]));}
const bundles=[];
for(let k=0;k<12;k++){
  const n=2+rand(5),tests=Array.from({length:n},()=>({c:rand(10),p:1+rand(4)})),V=1+rand(200),Q=4**n;
  function invoice(order){let prefix=1,denom=1,cost=0;for(const j of order){cost+=exact(tests[j].c*Q*prefix/denom);prefix*=tests[j].p;denom*=4;}return {cost,gain:exact(V*Q*prefix/denom-cost)};}
  const order=tests.map((_,i)=>i).sort((i,j)=>tests[i].c*(4-tests[j].p)-tests[j].c*(4-tests[i].p)),chosen=invoice(order),ps=permutations(tests.map((_,i)=>i));
  assert(chosen.cost===Math.min(...ps.map(p=>invoice(p).cost)));
  const memo=new Map();function optional(R){if(R===0)return V*Q;if(memo.has(R))return memo.get(R);let v=0;for(let j=0;j<n;j++)if((R>>j)&1)v=Math.max(v,exact(-tests[j].c*Q+tests[j].p*optional(R^(1<<j))/4));memo.set(R,v);return v;}
  const optimal=optional((1<<n)-1);assert(optimal===Math.max(0,chosen.gain));bundles.push({tests,V,scale:Q,order,chosen,optimal,permutations:ps.length});
}
const source=crypto.createHash('sha256').update(fs.readFileSync(new URL(import.meta.url))).digest('hex');
const result={status:'complete',evidence:'DEVELOPMENT',contributor:'Codex (GPT-6)',node:process.version,seed,sources:{'failure_probe.mjs':source},cases,separation,bundles,elapsed_ns:Number(process.hrtime.bigint()-start),limits:'Exact supplied success/cost models; rectangular endpoint adversary checked. Learned probability validity, real workloads and economic superiority not established.'};
fs.writeFileSync(out,JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify({status:result.status,cases:cases.length,positive:cases.filter(c=>c.result.gain>0).length,strictAdaptive:cases.filter(c=>c.result.gain>c.result.fixedGain).length,states:cases.reduce((a,c)=>a+c.result.states,0),worldStates:cases.reduce((a,c)=>a+c.result.worldStates,0),batchOutcomes:cases.reduce((a,c)=>a+c.result.batchOutcomes,0),separationGain:separation.result.gain/separation.result.scale/400,bundles:bundles.length,permutations:bundles.reduce((a,c)=>a+c.permutations,0),elapsed_ns:result.elapsed_ns}));
