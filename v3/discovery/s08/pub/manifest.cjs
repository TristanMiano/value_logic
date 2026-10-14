// Snapshot only staged s08 scientific/closing files; publication logs are separate.
const fs=require('fs'),path=require('path'),crypto=require('crypto'),cp=require('child_process');
const root=path.resolve(__dirname,'../../../..'),prefix='v3/discovery/s08/',target=prefix+'manifest.json';
const records=cp.execFileSync('git',['ls-files','--stage','-z','--',prefix],{cwd:root,encoding:'utf8',maxBuffer:16*1024*1024}).split('\0').filter(Boolean),files=[];
for(const record of records){
 const [meta,name]=record.split('\t');if(name.includes('/pub/')||name===target)continue;
 const raw=fs.readFileSync(path.join(root,name));const git=crypto.createHash('sha1').update(Buffer.from('blob '+raw.length+'\0')).update(raw).digest('hex');
 if(git!==meta.split(' ')[1])throw Error('Working bytes differ from staged source: '+name);
 files.push({path:name.slice(prefix.length),bytes:raw.length,sha256:crypto.createHash('sha256').update(raw).digest('hex'),git_blob:git});
}
const doc={schema:'s08-scientific-handoff-manifest-v1',contributor:'Codex (GPT-6)',prepared_date_utc:'2026-10-14',research_credit_ns:0,scope:'Staged s08 files excluding this manifest and pub/; raw failures included; actual/development scope remains in each executed design and findings. Hashes preserve bytes, not scientific confirmation.',file_count:files.length,total_bytes:files.reduce((a,x)=>a+x.bytes,0),files};
fs.writeFileSync(path.join(root,target),JSON.stringify(doc,null,2)+'\n');console.log(doc.file_count,doc.total_bytes);
