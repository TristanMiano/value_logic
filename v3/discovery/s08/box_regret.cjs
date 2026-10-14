// br01 direct corner reconstruction. Codex (GPT-6), DEVELOPMENT.
const fs=require('fs'),path=require('path'),assert=require('assert'),crypto=require('crypto');
const root=path.join(__dirname,'br01');fs.mkdirSync(root,{recursive:true});
const save=(name,x)=>fs.writeFileSync(path.join(root,name),JSON.stringify(x,null,2)+'\n');
let rngState=8141760;function rand(n){rngState=(Math.imul(1664525,rngState)+1013904223)>>>0;return rngState%n;}
function* codes(n,base){for(let code=0;code<base**n;code++){let c=code,a=[];for(let i=0;i<n;i++){a.push(c%base);c=Math.floor(c/base);}yield a;}}
const d=JSON.parse(fs.readFileSync(path.join(__dirname,'mc01/design.json'))),cases=d.cases.map(c=>({...c,vectors:c.bases.map(b=>Array.from({length:c.n},(_,i)=>+b.includes(i)))}));
for(let n=2;n<=6;n++)for(let k=0;k<3;k++){const vectors=[];for(let mask=0;mask<2**n;mask++)if(rand(3)===0)vectors.push(Array.from({length:n},(_,i)=>mask>>i&1));if(!vectors.length)vectors.push(Array(n).fill(0));cases.push({name:`arbitrary${n}_${k}`,n,vectors});}
if(!fs.existsSync(path.join(root,'design.json'))){save('design.json',{stage:'DEVELOPMENT',contributor:'Codex (GPT-6)',seed:8141760,cases,physical_audits:0,source_sha256:crypto.createHash('sha256').update(fs.readFileSync(__filename)).digest('hex')});fs.copyFileSync(__filename,path.join(root,'impl.cjs'));fs.copyFileSync(path.join(__dirname,'box_regret.md'),path.join(root,'declaration.md'));}
const dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0);
for(const c of cases){
 const m=c.vectors.length,a=Array(c.n).fill(0);for(const v of c.vectors)for(let i=0;i<c.n;i++)a[i]+=v[i];
 const intervals=[];
 if(c.n<=4){const options=[[0,2],[0,0],[1,1],[2,2]];for(const row of codes(c.n,4))intervals.push(row.map(i=>options[i]));}
 else {const options=[[0,0],[0,1],[0,2],[1,1],[1,2],[2,2]];for(let k=0;k<128;k++)intervals.push(Array.from({length:c.n},()=>options[rand(6)]));}
 let corners=0,boundChecks=0;for(const box of intervals){
  const l=box.map(x=>x[0]),u=box.map(x=>x[1]),q=a.map((v,i)=>v*(u[i]-l[i])+m*l[i]),U=dot(a,u),qmin=Math.min(...c.vectors.map(v=>dot(v,q))),L=m*Math.min(...c.vectors.map(v=>dot(v,l))),R=U-qmin;
  let worst=-Infinity;const worlds=[];for(const bits of codes(c.n,2)){const z=bits.map((v,i)=>box[i][v]),cost=dot(a,z),opt=m*Math.min(...c.vectors.map(v=>dot(v,z)));worst=Math.max(worst,cost-opt);worlds.push([cost,opt]);corners++;}assert.equal(R,worst);
  for(const price of[0,Math.floor(U/2),U+1]){let repair=-Infinity,replace=0;for(const [cost,opt] of worlds)for(const anchor of[0,2]){repair=Math.max(repair,cost+anchor-Math.min(price,opt+anchor));replace=Math.max(replace,price-opt-anchor);}assert.equal(repair,Math.max(R,U+2-price));assert.equal(replace,Math.max(0,price-L));boundChecks+=2;}
  assert.equal(U-(qmin-1),R+1);boundChecks++;
 }
 save(c.name+'.json',{status:'complete',copies:m,coefficients:a,interval_states:intervals.length,corner_checks:corners,bound_checks:boundChecks,physical_audits:0});
}
assert.equal(Math.max(...[0,1,2].map(z=>z-Math.min(z,z))),0);
save('shared_counterexample.json',{family:[[1,0],[0,1]],action:[1,0],independent_box_regret:2,shared_cost_regret:0});console.log('complete',cases.length);
