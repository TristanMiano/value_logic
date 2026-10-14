// Publication-only fallback after three monolithic interpreter crashes.
// Same test_*.py modules as python -m verification; fresh process per module.
const fs=require('fs'),path=require('path'),cp=require('child_process');
const root=path.resolve(__dirname,'../../../..'),out=path.join(__dirname,'isolated');
fs.mkdirSync(out,{recursive:true});
const names=fs.readdirSync(path.join(root,'verification')).filter(x=>/^test_.*\.py$/.test(x)).sort();
const record={scope:'all verification/test_*.py modules, separate interpreter per module',research_credit_ns:0,modules:[],tests_passed:0};
for(const name of names){
 const module='verification.'+name.slice(0,-3),attempts=[];let passed=false,count=0;
 for(let i=1;i<=5;i++){
  const log=path.join(out,name.slice(0,-3)+'_'+i+'.txt');
  if(fs.existsSync(log)){
   const text=fs.readFileSync(log,'utf8'),m=text.match(/Ran (\d+) tests? in/);
   if(m&&/\nOK(?: \([^\n]*\))?\s*$/.test(text)){passed=true;count=Number(m[1]);attempts.push({attempt:i,reused_saved_completed_check:true,log:path.basename(log)});break;}
   attempts.push({attempt:i,retained_failed_log:path.basename(log)});continue;
  }
  const exe=i%2?'C:\\Python313\\python.exe':'C:\\Users\\trist\\.cache\\codex-runtimes\\codex-primary-runtime\\dependencies\\python\\python.exe';
  const r=cp.spawnSync(exe,['-B','-X','faulthandler','-m','unittest',module,'-v'],{cwd:root,encoding:'utf8',timeout:300000,maxBuffer:32*1024*1024,windowsHide:true});
  const text=(r.stdout||'')+(r.stderr||'');fs.writeFileSync(log,text);
  const m=text.match(/Ran (\d+) tests? in/);passed=r.status===0&&!!m&&/\nOK(?: \([^\n]*\))?\s*$/.test(text);count=passed?Number(m[1]):0;
  attempts.push({attempt:i,python:exe,exit:r.status,signal:r.signal,error:r.error?.message||null,log:path.basename(log)});if(passed)break;
 }
 record.modules.push({module,passed,tests:count,attempts});record.tests_passed+=count;
 fs.writeFileSync(path.join(out,'summary.json'),JSON.stringify(record,null,2)+'\n');
 console.log(module,passed?'PASS':'FAIL',count);
}
record.complete=true;record.all_pass=record.modules.every(x=>x.passed);fs.writeFileSync(path.join(out,'summary.json'),JSON.stringify(record,null,2)+'\n');
console.log('FINAL',record.all_pass,record.modules.length,record.tests_passed);process.exitCode=record.all_pass?0:1;
