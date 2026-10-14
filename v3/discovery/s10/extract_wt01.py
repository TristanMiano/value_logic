"""Read only prospectively selected members; never extract arbitrary paths."""
import hashlib, json, pathlib, tarfile
root=pathlib.Path(__file__).resolve().parent
out=root/'wt01'
out.mkdir()
archive=root/'uf01'/'uf20.tgz'
selection=[f'uf20-{i:02d}.cnf' for i in range(9,25)]
manifest={'contributor':'Codex (GPT-6)','archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'selection':selection,'files':{}}
with tarfile.open(archive,'r:gz') as tf:
    members={pathlib.PurePosixPath(m.name).name:m for m in tf.getmembers() if m.isfile()}
    for name in selection:
        data=tf.extractfile(members[name]).read()
        (out/name).write_bytes(data)
        manifest['files'][name]=hashlib.sha256(data).hexdigest()
(out/'extraction.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print(json.dumps(manifest,indent=2))
