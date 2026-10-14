"""Preserve archives and selected numeric instances without arbitrary extraction."""
import hashlib,json,pathlib,tarfile,urllib.request,datetime
root=pathlib.Path(__file__).resolve().parent
out=root/'up50'
out.mkdir()
manifest={'contributor':'Codex (GPT-6)','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'selection':list(range(1,5)),'archives':{},'sources':[]}
for family in ['uf50','uuf50']:
    url=f'https://www.cs.ubc.ca/~hoos/SATLIB/Benchmarks/SAT/RND3SAT/{family}-218.tar.gz'
    target=out/(family+'.tgz')
    data=urllib.request.urlopen(url,timeout=30).read()
    target.write_bytes(data)
    manifest['archives'][family]={'url':url,'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)}
    with tarfile.open(target,'r:gz') as tf:
        members={int(pathlib.PurePosixPath(m.name).stem.split('-')[1]):m for m in tf.getmembers() if m.isfile() and pathlib.PurePosixPath(m.name).suffix=='.cnf'}
        for number in manifest['selection']:
            member=members[number]
            body=tf.extractfile(member).read()
            filename=f'{family}-{number:02d}.cnf'
            (out/filename).write_bytes(body)
            manifest['sources'].append({'file':filename,'archive':family,'member':member.name,'sha256':hashlib.sha256(body).hexdigest(),'expected_sat':family=='uf50'})
(out/'extraction.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print(json.dumps(manifest,indent=2))
