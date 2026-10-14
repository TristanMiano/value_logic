'use strict';
const fs=require('node:fs'),path=require('node:path'),cp=require('node:child_process');
const root=path.join(__dirname,'rc03'),design=JSON.parse(fs.readFileSync(path.join(root,'design.json'),'utf8')),dir=path.join(root,'runs');fs.mkdirSync(dir,{recursive:true});
for(const c of design.cases)for(const arm of design.arms){
 const out=path.join(root,c.name,arm);if(fs.existsSync(path.join(out,'summary.json')))continue;
 if(fs.existsSync(out)){console.log('PRESERVE unfinished',c.name,arm);continue;}
 const name=c.name+'_'+arm,start=new Date().toISOString();const run=cp.spawnSync(process.execPath,[path.join(__dirname,'service.cjs'),c.name,arm],{encoding:'utf8',timeout:60000,windowsHide:true,maxBuffer:2**20});
 fs.writeFileSync(path.join(dir,name+'.log'),run.stdout+'\n'+run.stderr);
 fs.writeFileSync(path.join(dir,name+'.json'),JSON.stringify({start_utc:start,end_utc:new Date().toISOString(),exit_code:run.status,signal:run.signal,error:run.error?String(run.error):null,command:['node','service.cjs',c.name,arm]},null,2)+'\n');
 console.log(name,run.status,run.stdout.trim());if(run.status!==0)console.log(run.stderr.slice(-1500));
}
