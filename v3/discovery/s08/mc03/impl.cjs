// Independent grouped-rank finite reconstruction. Codex (GPT-6), DEVELOPMENT.
const fs=require('fs'),path=require('path'),assert=require('assert'),crypto=require('crypto');
const root=path.join(__dirname,'mc03');fs.mkdirSync(root,{recursive:true});
const design=JSON.parse(fs.readFileSync(path.join(__dirname,'mc01/design.json'))),save=(name,x)=>fs.writeFileSync(path.join(root,name),JSON.stringify(x,null,2)+'\n');
function* vectors(n,base){for(let code=0;code<base**n;code++){let c=code,a=[];for(let i=0;i<n;i++){a.push(c%base);c=Math.floor(c/base);}yield a;}}
if(!fs.existsSync(path.join(root,'design.json'))){save('design.json',{stage:'DEVELOPMENT',contributor:'Codex (GPT-6)',parent_sha256:crypto.createHash('sha256').update(fs.readFileSync(path.join(__dirname,'mc01/design.json'))).digest('hex'),source_sha256:crypto.createHash('sha256').update(fs.readFileSync(__filename)).digest('hex'),physical_audits:0});fs.copyFileSync(__filename,path.join(root,'impl.cjs'));fs.copyFileSync(path.join(__dirname,'grouped_rank.md'),path.join(root,'declaration.md'));}
const cases=[...design.cases,{name:'triangle_partition',n:6,bases:[0,1].flatMap(a=>[2,3].flatMap(b=>[4,5].map(c=>[a,b,c]))),groups:[0,1,1,2,0,2]}];
for(const c of cases){
 if(fs.existsSync(path.join(root,c.name+'.json')))continue;
 const groups=c.groups||Array.from({length:c.n},(_,i)=>i%Math.ceil(c.n/2)),k=Math.max(...groups)+1,r=c.bases[0].length,m=c.bases.length,H=2;
 const count=c.bases.map(b=>{let a=Array(k).fill(0);for(const i of b)a[groups[i]]++;return a;}),a=Array(k).fill(0);for(const b of count)for(let j=0;j<k;j++)a[j]+=b[j];
 const R=H*Math.max(...count.map(b=>b.reduce((s,x,j)=>s+Math.max(0,a[j]-m*x),0))),R2=H/2*Math.max(...count.map(b=>b.reduce((s,x,j)=>s+Math.abs(a[j]-m*x),0)));assert.equal(R,R2);
 let worst=0,corners=0;
 for(const bits of vectors(k,2)){const z=bits.map(v=>v*H),opt=m*Math.min(...count.map(b=>b.reduce((s,x,j)=>s+x*z[j],0))),value=a.reduce((s,x,j)=>s+x*z[j],0);worst=Math.max(worst,value-opt);corners++;}assert.equal(R,worst);
 let reductions=0,submodularity=0;
 for(const d of vectors(k,3)){
  const values=[];for(let mask=0;mask<2**k;mask++){
   const gain=Math.max(...count.map(b=>b.reduce((s,x,j)=>s+(mask>>j&1?x*d[j]:0),0))),upper=Math.min(...count.map(b=>b.reduce((s,x,j)=>s+x*(H-(mask>>j&1?d[j]:0)),0)));assert.equal(upper,r*H-gain);values.push(gain);reductions++;
  }
  for(let mask=0;mask<2**k;mask++)for(let i=0;i<k;i++)if(!(mask>>i&1))for(let j=i+1;j<k;j++)if(!(mask>>j&1)){assert(values[mask|1<<i]+values[mask|1<<j]>=values[mask]+values[mask|1<<i|1<<j]);submodularity++;}
 }
 if(c.name==='triangle_partition'){assert.equal(R,m*H);/* balanced m/2 copies times MaxCut2 times H */}
 save(c.name+'.json',{status:'complete',groups,rank:r,copies:m,coefficients:a,regret:R,corner_checks:corners,rank_reductions:reductions,submodularity_checks:submodularity,physical_audits:0});console.log(c.name,R,reductions,submodularity);
}
