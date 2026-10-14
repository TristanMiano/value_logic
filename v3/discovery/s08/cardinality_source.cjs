// mc02 original source construction and independent clause checks. Codex (GPT-6).
const fs=require('fs'),path=require('path'),crypto=require('crypto'),assert=require('assert');
const root=path.join(__dirname,'mc02');fs.mkdirSync(root,{recursive:true});
const digest=x=>crypto.createHash('sha256').update(JSON.stringify(x)).digest('hex');
const save=(name,x)=>fs.writeFileSync(path.join(root,name),JSON.stringify(x,null,2)+'\n');
function gate(y,a,x,b){return (!a||y)&&(!x||!b||y)&&(!y||a||x)&&(!y||a||b);}
for(let bits=0;bits<16;bits++){let [y,a,x,b]=[0,1,2,3].map(i=>!!(bits>>i&1));assert.equal(gate(y,a,x,b),y===(a||(x&&b)));}
function build(n,r){
 const m=n,span=n+(n+1)*(r+2),variables=m*span+1,h=variables,hard=[],features=[];
 const y=(copy,i,j)=>copy*span+n+i*(r+2)+j+1;
 for(let copy=0;copy<m;copy++){
  for(let i=0;i<=n;i++)hard.push([y(copy,i,0)]);
  for(let j=1;j<=r+1;j++)hard.push([-y(copy,0,j)]);
  for(let i=1;i<=n;i++)for(let j=1;j<=r+1;j++){
   const out=y(copy,i,j),a=y(copy,i-1,j),x=copy*span+i,b=y(copy,i-1,j-1);
   hard.push([-a,out],[-x,-b,out],[-out,a,x],[-out,a,b]);
  }
  hard.push([y(copy,n,r)],[-y(copy,n,r+1)]);
  for(let i=0;i<n;i++)features.push({clause:[-(copy*span+i+1)],coordinate:i,scale:1});
 }
 hard.push([1,h],[-1,h]);features.push({clause:[-h],coordinate:n,scale:1});
 return {n,r,m,H:2,span,variables,hard,features,anchor:h};
}
function model(source,bases,enforce=true){
 const {n,r,m,span,variables}=source;assert.equal(bases.length,m);let mask=1n<<BigInt(variables-1);
 for(let copy=0;copy<m;copy++){
  const b=new Set(bases[copy]);if(enforce)assert.equal(b.size,r);let count=0;
  for(let i=0;i<=n;i++){
   if(i>0&&b.has(i-1)){count++;mask|=1n<<BigInt(copy*span+i-1);}
   for(let j=0;j<=r+1;j++)if(count>=j)mask|=1n<<BigInt(copy*span+n+i*(r+2)+j);
  }
 }
 return mask;
}
function check(source,mask){
 let literalChecks=0;
 for(const clause of source.hard){let satisfied=false;for(const lit of clause){literalChecks++;if(Boolean((mask>>BigInt(Math.abs(lit)-1))&1n)===(lit>0))satisfied=true;}assert(satisfied);}
 const coefficients=Array(source.n+1).fill(0);
 for(const f of source.features)if(!f.clause.some(l=>Boolean((mask>>BigInt(Math.abs(l)-1))&1n)===(l>0)))coefficients[f.coordinate]+=f.scale;
 return {literalChecks,coefficients};
}
if(!fs.existsSync(path.join(root,'design.json'))){
 save('design.json',{stage:'DEVELOPMENT',contributor:'Codex (GPT-6)',n:[4,8,16,32],physical_audits:0,resolution_steps:0,complete_sat_calls:0,source_sha256:crypto.createHash('sha256').update(fs.readFileSync(__filename)).digest('hex')});
 fs.copyFileSync(__filename,path.join(root,'impl.cjs'));fs.copyFileSync(path.join(__dirname,'cardinality_source.md'),path.join(root,'declaration.md'));
}
for(const n of[4,8,16,32]){
 if(fs.existsSync(path.join(root,`n${n}_result.json`)))continue;
 const r=n/2,s=build(n,r),sourceId=digest(s),cyclic=Array.from({length:n},(_,c)=>Array.from({length:r},(_,j)=>(c+j)%n));
 const fallback=model(s,cyclic),a=check(s,fallback);assert.deepEqual(a.coefficients,[...Array(n).fill(r),1]);
 const upper=Array.from({length:n},(_,i)=>i%3===0?0:i%3===1?1:2),chosen=Array.from({length:n},(_,i)=>i).sort((a,b)=>upper[a]-upper[b]||a-b).slice(0,r),repair=model(s,Array.from({length:n},()=>chosen)),b=check(s,repair);
 assert.deepEqual(b.coefficients,[...Array.from({length:n},(_,i)=>chosen.includes(i)?n:0),1]);
 let projectionChecks=0,auxRejects=0;
 if(n<=8){
  for(let bits=0;bits<(1<<n);bits++){
   const subset=Array.from({length:n},(_,i)=>i).filter(i=>bits>>i&1),candidate=model(s,Array.from({length:n},()=>subset),false);let valid=true;
   try{check(s,candidate);}catch(e){if(e.code!=='ERR_ASSERTION')throw e;valid=false;}
   assert.equal(valid,subset.length===r);projectionChecks++;
  }
  for(let j=n;j<s.span;j++){assert.throws(()=>check(s,fallback^(1n<<BigInt(j))),assert.AssertionError);auxRejects++;}
 }
 assert.throws(()=>model(s,Array.from({length:n},()=>chosen.slice(1))),assert.AssertionError);
 assert.throws(()=>check(s,fallback^1n),assert.AssertionError);assert.notEqual(digest({...s,hard:s.hard.slice(1)}),sourceId);
 save(`n${n}_source.json`,{identity:sourceId,...s});save(`n${n}_actions.json`,{source:sourceId,fallback_hex:fallback.toString(16),upper_hex:repair.toString(16),upper,upper_basis:chosen});
 save(`n${n}_result.json`,{status:'complete',source:sourceId,variables:s.variables,clauses:s.hard.length,features:s.features.length,projectionChecks,auxRejects,gateTruthTable:16,original_clause_checks:2*s.hard.length,literal_checks:a.literalChecks+b.literalChecks,negative_controls:3,physical_audits:0});
 console.log(n,s.variables,s.hard.length,projectionChecks,auxRejects);
}
