'use strict';
// Finite mathematical screen, no physical acquisition. Codex (GPT-6).
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const k=require('./retained.cjs');
function cases(){
  const result=[];
  for(const n of [3,4,6,8]){
    result.push(k.source('path'+n,n,Array.from({length:n-1},(_,i)=>[i+1,i+2])));
    result.push(k.source('hyper'+n,n,Array.from({length:n},(_,i)=>[i+1,(i+1)%n+1,(i+2)%n+1])));
    const rand=k.rng(8142000+n),hard=[],plants=[2**n-1,Array.from({length:n},(_,i)=>i%2?0:2**i).reduce((a,b)=>a+b,0)];
    while(hard.length<2*n){const chosen=new Set();while(chosen.size<Math.min(n,3))chosen.add(1+Math.floor(rand()*n));const c=k.source('unused',n,[[1]]).hard&&[...chosen].map(v=>rand()<.45?-v:v);if(plants.every(mask=>c.some(v=>Boolean(mask&(2**(Math.abs(v)-1)))===(v>0))))hard.push(c);}
    result.push(k.source('mixed'+n,n,hard));
  }
  result.push(k.source('clique4',4,[[1,2],[1,3],[1,4],[2,3],[2,4],[3,4]]));
  result.push(k.source('split4',8,[[1,2,5],[1,2,-5],[2,3,6],[2,3,-6],[3,4,7],[3,4,-7],[1,4,8],[1,4,-8]],[1,2,3,4]));
  result.push(k.source('zero4',4,[[-1,-2],[-2,-3],[-3,-4]]));
  return result;
}
function check(root,source){
  const setup=new k.Meter(),diag=new k.Meter(),out=path.join(root,source.name);fs.mkdirSync(out);
  k.save(path.join(out,'source.json'),source);
  const receipt=k.extract(source,setup),all=k.enumerate(source,diag),n=source.features.length;
  const unique=[...new Map(all.map(x=>[x.v.join(''),x])).values()];
  unique.sort((a,b)=>k.sum(a.v)-k.sum(b.v)||a.mask-b.mask);
  const models=[unique[0]];if(unique.length>1)models.push([...unique].sort((a,b)=>k.sum(b.v.map((x,i)=>Number(x!==models[0].v[i])))-k.sum(a.v.map((x,i)=>Number(x!==models[0].v[i])))||a.mask-b.mask)[0]);
  if(unique.length>2)models.push([...unique].reverse().find(x=>!models.some(y=>y.mask===x.mask)));
  const results=[],controls=[];let states=0,corners=0,audits=0,convolutions=0,strict=0;
  function reject(label,fn){assert.throws(fn,undefined,label);controls.push(label);}
  const changed=k.seal({...source,id:undefined,name:source.name+'changed'});delete changed.id;changed.id=k.hash(Object.fromEntries(Object.entries(changed).filter(([key])=>key!=='id')));
  reject('changed_source',()=>k.checkExtraction(changed,receipt));
  let bad=structuredClone(receipt);bad.feature_map=bad.feature_map.slice().reverse();delete bad.id;bad=k.seal(bad);reject('feature_map',()=>k.checkExtraction(source,bad));
  if(receipt.steps.length){let bad=structuredClone(receipt);bad.steps[0].pivot=source.variables+1;delete bad.id;bad=k.seal(bad);reject('pivot',()=>k.checkExtraction(source,bad));}
  if(receipt.cuts.length){let bad=structuredClone(receipt);bad.cuts[0].features=[];delete bad.id;bad=k.seal(bad);reject('cut',()=>k.checkExtraction(source,bad));}
  for(const action of [[models[0]],models]){
    const masks=action.map(x=>x.mask),m=masks.length,a=k.counts(source,masks,setup),q0=a.map(x=>4*x),lambda=k.packing(receipt.cuts,q0,setup),cert=k.dual(source,receipt,lambda,setup);
    if(lambda.length){const bad=[...lambda];bad[0]=-1;reject('negative_multiplier_m'+m,()=>k.dual(source,receipt,bad));}
    reject('receipt_outside_box_m'+m,()=>k.auditScore(cert,a,m,a.map(()=>0),a.map(()=>4),0,5));
    const statesBefore=states,strictBefore=strict,boxes=[];
    if(n<=4)k.product(Array.from({length:n},()=>[[0,0],[0,2],[0,4],[2,2],[2,4],[4,4]]),box=>boxes.push(box));
    else {const rand=k.rng(8142100+n+m);for(let j=0;j<128;j++)boxes.push(Array.from({length:n},()=>{const x=Math.floor(rand()*3)*2,y=Math.floor(rand()*3)*2;return [Math.min(x,y),Math.max(x,y)];}));}
    for(const box of boxes){
      const lo=box.map(x=>x[0]),hi=box.map(x=>x[1]),bound=k.bounds(cert,a,m,lo,hi,diag);
      const optimum=Math.min(...unique.map(x=>k.sum(x.v.map((v,i)=>v*bound.q[i]))));diag.pay('exact_objective',unique.length*(2*n+1));
      const exact=k.sum(a.map((v,i)=>v*hi[i]))-optimum;assert(bound.raw>=exact&&bound.upper>=exact);states++;
      if(n<=4){let worst=0;k.product(box.map(([l,u])=>[...new Set([l,u])]),world=>{const best=Math.min(...unique.map(x=>k.sum(x.v.map((v,i)=>v*world[i]))));worst=Math.max(worst,k.sum(a.map((v,i)=>v*world[i]))-m*best);corners++;diag.pay('corner_objective',unique.length*(2*n+1)+2*n);});assert.equal(worst,exact);}
      const scores=[];
      for(let i=0;i<n;i++){
        const t=(lo[i]+hi[i])/2,delta=k.auditScore(cert,a,m,lo,hi,i,t,diag),l2=[...lo],u2=[...hi];l2[i]=t;u2[i]=t;
        assert.equal(bound.raw-k.bounds(cert,a,m,l2,u2,diag).raw,delta);
        const scalarOnly=Math.min(a[i]*(hi[i]-t),(m-a[i])*(t-lo[i]));assert(delta>=scalarOnly);if(delta>scalarOnly)strict++;
        scores.push(delta);audits++;
      }
      const mid=lo.map((x,i)=>(x+hi[i])/2);assert.equal(bound.raw-k.bounds(cert,a,m,mid,mid,diag).raw,k.sum(scores));
    }
    const lo=a.map(()=>0),hi=a.map(()=>4),base=k.bounds(cert,a,m,lo,hi,diag),block=Array.from({length:Math.min(n,4)},(_,i)=>i),support=block.map(()=>[0,2,4]);
    const scores=block.map(i=>[0,2,4].map(t=>k.auditScore(cert,a,m,lo,hi,i,t,diag)));
    for(let quota=0;quota<=Math.min(base.raw+1,16);quota++){
      const d=k.convolve(support,scores,quota,diag);let numerator=0n,den=0n;k.product(scores,values=>{den++;if(k.sum(values)>=quota)numerator++;diag.pay('enumerated_probability',values.length+1);});assert.equal(d.num,numerator);assert.equal(d.den,den);convolutions++;
    }
    results.push({m,models:masks,a,certificate:cert,initial_bound:base.raw,states:states-statesBefore,strict_contractions_over_scalar_only:strict-strictBefore});
  }
  const result={source:source.name,status:'pass',feature_count:n,variables:source.variables,models:all.length,feature_vectors:unique.length,extraction:receipt,actions:results,states,corners,audits,convolutions,strict,negative_controls:controls,setup:setup.record(),diagnostic:diag.record(),physical_audits:0,complete_calls:0};
  k.save(path.join(out,'result.json'),result);console.log(source.name,states,corners,receipt.steps.length,receipt.cuts.length,setup.total());return result;
}
function main(){const root=path.join(__dirname,'rc01');if(process.argv[2]==='prepare'){fs.mkdirSync(root);k.save(path.join(root,'design.json'),{stage:'DEVELOPMENT',contributor:'Codex (GPT-6)',created_utc:new Date().toISOString(),sources:cases(),source_hash:k.sha(__filename),kernel_hash:k.sha(path.join(__dirname,'retained.cjs')),declaration_hash:k.sha(path.join(__dirname,'rc01.md'))});for(const f of ['rc01.cjs','retained.cjs','rc01.md'])fs.copyFileSync(path.join(__dirname,f),path.join(root,f));return;}
 const design=JSON.parse(fs.readFileSync(path.join(root,'design.json'),'utf8'));assert.equal(k.sha(__filename),design.source_hash);assert.equal(k.sha(path.join(__dirname,'retained.cjs')),design.kernel_hash);for(const source of design.sources)if(source.name===process.argv[2])return check(root,source);throw new Error('Choose prepared source');}
if(require.main===module)main();module.exports={cases,check};
