'use strict';
// rc03 matched paid service. Codex (GPT-6), DEVELOPMENT.
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const k=require('./retained.cjs'),p=require('./prefix.cjs'),complete=require('./complete.cjs');
const ARMS=['prefix','ordinary_prefix','greedy','threshold','audit_first','direct'];
const FILES=['service.cjs','retained.cjs','prefix.cjs','complete.cjs','rc03.md'];
function portfolio(source,models,meter,direct=false){
 k.admit(source,meter);const m=models.length,menus=[models,...models.map(mask=>Array(m).fill(mask))];
 const receipt=direct?null:k.extract(source,meter);const cuts=direct?[]:k.checkExtraction(source,receipt,meter);
 const actions=menus.map(masks=>{
  const a=k.counts(source,masks,meter),lambda=direct?[]:k.packing(cuts,a.map(x=>4*x),meter),b=a.map(()=>0);let K=0;
  lambda.forEach((v,i)=>{k.integer(v);K+=v;for(const f of cuts[i].features)b[f]+=v;meter.pay('cached_dual_combination',2*cuts[i].features.length+2);});
  const cert=k.seal({source_id:source.id,extraction_id:receipt?receipt.id:null,lambda,b,K});meter.pay('portfolio_retention_words',b.length+lambda.length+masks.length+8);
  const bound=k.bounds(cert,a,m,a.map(()=>0),a.map(()=>4),meter);return {models:masks,m,a,cert,initial:bound.upper,raw_initial:bound.raw};
 });return {receipt,actions};
}
function prepare(root){
 fs.mkdirSync(root);const names=['path4','path8','hyper8','split4','mixed6','mixed8','zero4'],cases=[],preparation=new k.Meter();
 for(const [si,name] of names.entries()){
  const source=JSON.parse(fs.readFileSync(path.join(__dirname,'rc01',name,'source.json'),'utf8')),old=JSON.parse(fs.readFileSync(path.join(__dirname,'rc01',name,'result.json'),'utf8')),models=old.actions.at(-1).models;
  const prepared=portfolio(source,models,preparation),initial=Math.min(...prepared.actions.map(a=>a.initial)),fees=source.features.map((_,i)=>1+i%3),C=Math.ceil(.75*k.sum(fees));
  const historical_model_units=Object.entries(old.diagnostic.categories).filter(([key])=>key.startsWith('enumeration_')).reduce((s,[,v])=>s+v,0);
  for(const quota of [2,6])cases.push({name:name+'_q'+quota,source,models,initial,quota,tolerance:Math.max(0,initial-quota),fees,C,seed:8142300+100*si+quota,requests:128,historical_model_units,historical_source_sha256:k.sha(path.join(__dirname,'rc01',name,'result.json'))});
 }
 const hashes=Object.fromEntries(FILES.map(f=>[f,k.sha(path.join(__dirname,f))]));
 k.save(path.join(root,'design.json'),{created_utc:new Date().toISOString(),contributor:'Codex (GPT-6)',stage:'DEVELOPMENT',cases,arms:ARMS,hashes,design_preparation:preparation.record(),scope:'Model and request construction outside service tariff; historical model proposal allocation is inside each arm. Complete economic cost unknown.'});
 for(const f of FILES)fs.copyFileSync(path.join(__dirname,f),path.join(root,f));
}
function policy(c,actions,arm,meter){
 if(arm==='audit_first'||arm==='direct')return {};
 const allScores=actions.map(a=>a.a.map((_,i)=>[0,2,4].map(t=>k.auditScore(a.cert,a.a,a.m,a.a.map(()=>0),a.a.map(()=>4),i,t,meter))));
 if(arm==='prefix'||arm==='ordinary_prefix'){
  let best=null,selected=0;const candidates=[];
  actions.forEach((a,i)=>{const plan=p.compile(allScores[i],c.fees,Math.max(0,a.raw_initial-c.tolerance),c.C,c.C,meter);candidates.push(p.serial(plan));if(best===null||plan.expected.num*best.expected.den<best.expected.num*plan.expected.den){best=plan;selected=i;}});
  meter.pay('compiled_sequence_retention',best.sequence.length+8);return {selected,sequence:best.sequence,expected:p.record(best.expected),candidates,allScores};
 }
 if(arm==='threshold'){
  const selected=actions.reduce((best,a,i)=>a.initial<actions[best].initial?i:best,0),order=p.orders(allScores[selected],c.fees,meter)[0],sequence=[];let spend=0;
  for(const i of order){if(spend+c.fees[i]>c.C)break;sequence.push(i);spend+=c.fees[i];}
  meter.pay('threshold_retention',sequence.length+8);return {selected,sequence,allScores};
 }
 return {allScores};
}
function run(root,c,arm){
 const out=path.join(root,c.name,arm);fs.mkdirSync(out,{recursive:false});const setup=new k.Meter();setup.pay('historical_model_proposal_allocation',c.historical_model_units);
 const bank=portfolio(c.source,c.models,setup,arm==='direct'),compiled=policy(c,bank.actions,arm,setup);
 k.save(path.join(out,'setup.json'),{bank,compiled,invoice:setup.record(),created_utc:new Date().toISOString()});
 const rand=k.rng(c.seed),rows=[],start=process.hrtime.bigint(),cpuStart=process.cpuUsage();let totalFee=0,totalNamed=setup.total(),totalCalls=0,completeCalls=0;
 for(let request=0;request<c.requests;request++){
  const hidden=c.source.features.map(()=>[0,2,4][Math.floor(rand()*3)]),requestId=c.name+':'+request+':'+arm,file=path.join(out,'r'+String(request).padStart(3,'0')+'.json');
  const meter=new k.Meter(),provider=new k.Meter(),known=c.source.features.map(()=>null),receipts=[];let fee=0,logical=null,result=null,preSpend=0,index=0;
  const persist=status=>k.save(file,{status,request_id:requestId,source_id:c.source.id,request,receipts,physical_fee:fee,known,logical,result,invoice:meter.record(),provider_invoice:provider.record()});
  function buy(query){
   let indices,price;if(query==='all'){indices=hidden.map((_,i)=>i);price=c.C;}else{k.integer(query);assert(known[query]===null);indices=[query];price=c.fees[query];}
   const receipt=k.seal({request_id:requestId,source_id:c.source.id,sequence:receipts.length,query,fee:price,observations:indices.map(i=>[i,hidden[i]])});provider.pay('physical_receipt_export',8+4*indices.length);receipts.push(receipt);fee+=price;persist('purchase_saved_before_consumer');
   k.checkSeal(receipt);assert.equal(receipt.request_id,requestId);assert.equal(receipt.source_id,c.source.id);assert.equal(receipt.fee,price);for(const [i,t] of receipt.observations){assert([0,2,4].includes(t));if(known[i]!==null)assert.equal(known[i],t);known[i]=t;}meter.pay('physical_receipt_check',12+5*indices.length);return receipt;
  }
  function boundAll(){
   const lo=known.map(t=>t===null?0:t),hi=known.map(t=>t===null?4:t),values=[];
   for(let i=0;i<bank.actions.length;i++){const a=bank.actions[i],bound=k.bounds(a.cert,a.a,a.m,lo,hi,meter);values.push(bound);if(bound.upper<=c.tolerance)return {index:i,bound,values,lo,hi};}
   return {index:null,values,lo,hi};
  }
  let terminal=boundAll();
  while(terminal.index===null){
   let next=null;
   if(arm==='prefix'||arm==='ordinary_prefix'||arm==='threshold')next=index<compiled.sequence.length?compiled.sequence[index++]:null;
   else if(arm==='greedy'){
    const best=terminal.values.reduce((a,b,i)=>b.upper<terminal.values[a].upper?i:a,0),action=bank.actions[best],quota=Math.max(0,terminal.values[best].raw-c.tolerance);let value=quota/c.C;
    for(let i=0;i<known.length;i++)if(known[i]===null&&preSpend+c.fees[i]<=c.C){const scores=[0,2,4].map(t=>Math.min(quota,k.auditScore(action.cert,action.a,action.m,terminal.lo,terminal.hi,i,t,meter))),gain=k.sum(scores)/scores.length/c.fees[i];meter.pay('greedy_gain_comparison',scores.length+4);if(gain>value){value=gain;next=i;}}
   }
   if(next===null||preSpend+c.fees[next]>c.C)break;
   buy(next);preSpend+=c.fees[next];terminal=boundAll();
  }
  if(terminal.index===null){
   const remaining=known.map((t,i)=>t===null?i:null).filter(i=>i!==null),individual=k.sum(remaining.map(i=>c.fees[i]));meter.pay('fallback_purchase_choice',known.length+2);
   if(individual<c.C){for(const i of remaining)buy(i);}else buy('all');
   terminal=boundAll();
  }
  if(terminal.index!==null){const action=bank.actions[terminal.index];result={kind:'retained',action:terminal.index,models:action.models,regret_upper:terminal.bound.upper};}
  else{
   assert(known.every(t=>t!==null));const providerProof=new k.Meter();logical=complete.acquire(c.source,known,c.models[0],requestId,providerProof);persist('logical_proof_acquired');const checked=complete.check(c.source,known,logical,requestId,meter);result={kind:'complete',models:Array(c.models.length).fill(checked.model),regret_upper:0};meter.pay('complete_provider_invoice',providerProof.total());completeCalls++;
  }
  for(const mask of result.models)k.modelFeatures(c.source,mask,meter);meter.pay('final_action_export',result.models.length+8);
  assert(fee<=2*c.C);persist('complete');const named=meter.total()+provider.total();totalFee+=fee;totalNamed+=named;totalCalls+=receipts.length;
  rows.push({request,physical_fee:fee,named_units:named,audit_calls:receipts.length,coordinates_observed:known.filter(t=>t!==null).length,output_kind:result.kind,regret_upper:result.regret_upper});
 }
 const summary={status:'complete',source:c.name,arm,outputs:rows.length,physical_fee:totalFee,audit_calls:totalCalls,actual_complete_calls:completeCalls,named_units:totalNamed,setup_units:setup.total(),rows,wall_ns:(process.hrtime.bigint()-start).toString(),process_cpu_microseconds:process.cpuUsage(cpuStart),unknown_costs:['source generation','external prices','storage byte-time','unmetered host/library work']};k.save(path.join(out,'summary.json'),summary);console.log(c.name,arm,totalFee,totalNamed,completeCalls);return summary;
}
function main(){const root=path.join(__dirname,'rc03');if(process.argv[2]==='prepare')return prepare(root);const design=JSON.parse(fs.readFileSync(path.join(root,'design.json'),'utf8'));for(const [f,h] of Object.entries(design.hashes))assert.equal(k.sha(path.join(__dirname,f)),h);const c=design.cases.find(c=>c.name===process.argv[2]),arm=process.argv[3];assert(c&&ARMS.includes(arm));fs.mkdirSync(path.join(root,c.name),{recursive:true});run(root,c,arm);}
if(require.main===module)main();module.exports={portfolio,policy,run};
