'use strict';
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
let s=fs.readFileSync(path.join(__dirname,'region_service.cjs'),'utf8');
function replace(a,b){assert(s.includes(a),a);s=s.replace(a,b);}
s=s.replaceAll('rr01','br01').replaceAll('region_service.cjs','budget_service.cjs');
replace("['regions','ordinary_regions','positive_cache','early_local','threshold','relevant_audit']","['budget100k','ordinary_budget100k','budget0','regions','threshold','relevant_audit']");
replace('seed:c.seed+600','seed:c.seed+800');
replace("const useRegions=arm==='regions'||arm==='ordinary_regions',useCache=useRegions||arm==='positive_cache',useLocal=useCache||arm==='early_local';",String.raw`
 const useRegions=['budget100k','ordinary_budget100k','budget0','regions'].includes(arm),useCache=useRegions,useLocal=useRegions;
 const budget=arm==='budget0'?0:arm.includes('budget100k')?100000:null,BUDGET=Symbol('budget');let optionalSpent=0,largestChunk=0,exhausted=budget===0,aborts=0,optionalActive=false;const optionalCategories={};
 class BudgetMeter extends k.Meter {pay(name,n=1){super.pay(name,n);if(optionalActive){optionalSpent+=n;largestChunk=Math.max(largestChunk,n);optionalCategories[name]=(optionalCategories[name]||0)+n;if(budget!==null&&optionalSpent>budget){exhausted=true;aborts++;throw BUDGET;}}}}
 function optional(f){assert(!exhausted);optionalActive=true;try{return f();}finally{optionalActive=false;}}
`);
replace("if(useLocal)baseTable=la.initialTable(models,setup);if(useRegions)floorTemplate=rg.bank(models,Array(n).fill(-MAX),Array(n).fill(MAX),setup);",'');
replace('meter=new k.Meter(),provider=new k.Meter()','meter=new BudgetMeter(),provider=new k.Meter()');
replace('function local(){localCalls++;','function local(){localCalls++;if(!baseTable)baseTable=la.initialTable(models,meter);');
replace("if(exact(action)<=c.tolerance*SCALE)return {kind:'existing_action',entry:useCache?positive():null,closes:true};",String.raw`
   if(exact(action)<=c.tolerance*SCALE){let entry=null;if(useCache&&!exhausted){try{entry=optional(positive);}catch(e){if(e!==BUDGET)throw e;}}return {kind:'existing_action',entry,closes:true};}
   if(exhausted)return {kind:'budget_exhausted',closes:false};
   try{return optional(()=>{
`);
replace('if(useRegions){if(!floorBank){','if(useRegions){if(!floorTemplate)floorTemplate=rg.bank(models,Array(n).fill(-MAX),Array(n).fill(MAX),meter);if(!floorBank){');
replace('return resolution;\n  }',String.raw`return resolution;
   });}catch(e){if(e!==BUDGET)throw e;table=null;tableLo=null;tableHi=null;floorBank=null;return {kind:'budget_abort',closes:exact(action)<=c.tolerance*SCALE};}
  }`);
replace("status:'complete',source:c.name,arm,outputs:","status:'complete',source:c.name,arm,budget,optional_spent:optionalSpent,largest_optional_chunk:largestChunk,budget_exhausted:exhausted,budget_aborts:aborts,optional_categories:optionalCategories,outputs:");
fs.writeFileSync(path.join(__dirname,'budget_service.cjs'),s);
let d=fs.readFileSync(path.join(__dirname,'run_rr01.cjs'),'utf8').replaceAll('rr01','br01').replaceAll('region_service.cjs','budget_service.cjs');fs.writeFileSync(path.join(__dirname,'run_br01.cjs'),d);
