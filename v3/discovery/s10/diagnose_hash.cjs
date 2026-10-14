'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),k=require('./retained.cjs'),root=path.join(__dirname,'ds01');
const original=k.checkSeal;let calls=0;
k.checkSeal=function(value){calls++;try{return original(value);}catch(error){const {id,...rest}=value,canonical=k.canonical(rest),bytes=Buffer.from(canonical);fs.writeFileSync(path.join(root,'hash_failure05.canonical.txt'),bytes);k.save(path.join(root,'hash_failure05.object.json'),value);console.error(JSON.stringify({calls,claimed:id,immediate:crypto.createHash('sha256').update(bytes).digest('hex'),second:crypto.createHash('sha256').update(bytes).digest('hex'),length:bytes.length}));throw error;}};
require('./check_ds01.cjs');
