'use strict';
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict'),k=require('./retained.cjs'),tree=require('./tree.cjs');
const root=path.join(__dirname,'tc01'),design=JSON.parse(fs.readFileSync(path.join(root,'design.json'),'utf8')),rows=[];
for(const input of design.inputs){const source=input.source,receipt=JSON.parse(fs.readFileSync(path.join(__dirname,input.receipt),'utf8')),controls=[];
 function reject(label,fn){assert.throws(fn);controls.push(label);}
 let altered=structuredClone(source);altered.name+='changed';delete altered.id;altered=k.seal(altered);reject('source',()=>tree.compile(altered,receipt));
 altered=structuredClone(source);altered.features.reverse();delete altered.id;altered=k.seal(altered);reject('feature_map',()=>tree.compile(altered,receipt));
 function mutate(node,kind){if(node[0]===kind){if(kind==='clause')node[1]=source.hard.length;else node[1]=source.variables;return true;}if(node[0]==='split')return mutate(node[2],kind)||mutate(node[3],kind);return false;}
 for(const kind of ['clause','split']){let bad=structuredClone(receipt);if(mutate(bad.proof,kind)){delete bad.id;bad=k.seal(bad);reject(kind,()=>tree.compile(source,bad));}}
 rows.push({name:input.name,controls});
}k.save(path.join(root,'controls.json'),{status:'pass',count:k.sum(rows.map(r=>r.controls.length)),rows});console.log('controls',k.sum(rows.map(r=>r.controls.length)));
