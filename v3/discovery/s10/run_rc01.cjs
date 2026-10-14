'use strict';
const fs=require('node:fs'),path=require('node:path'),cp=require('node:child_process');
const root=path.join(__dirname,'rc01');const design=JSON.parse(fs.readFileSync(path.join(root,'design.json'),'utf8'));
const dir=path.join(root,'runs');fs.mkdirSync(dir,{recursive:true});
for(const source of design.sources){
  if(fs.existsSync(path.join(root,source.name,'result.json')))continue;
  const start=new Date().toISOString();
  const run=cp.spawnSync(process.execPath,[path.join(__dirname,'rc01.cjs'),source.name],{encoding:'utf8',timeout:60000,windowsHide:true,maxBuffer:2**20});
  fs.writeFileSync(path.join(dir,source.name+'.log'),run.stdout+'\n'+run.stderr);
  fs.writeFileSync(path.join(dir,source.name+'.json'),JSON.stringify({start_utc:start,end_utc:new Date().toISOString(),exit_code:run.status,signal:run.signal,error:run.error?String(run.error):null,command:['node','rc01.cjs',source.name]},null,2)+'\n');
  console.log(source.name,run.status,run.stdout.trim());
  if(run.status!==0)console.log(run.stderr.slice(-1500));
}
