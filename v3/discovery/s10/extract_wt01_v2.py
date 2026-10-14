"""Correct SATLIB's leading-zero member names; retain the first failed prefix."""
import hashlib, json, pathlib, tarfile
root=pathlib.Path(__file__).resolve().parent
out=root/'wt01'
archive=root/'uf01'/'uf20.tgz'
manifest={'contributor':'Codex (GPT-6)','archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'numeric_selection':list(range(9,25)),'files':{},'previous_failure':'extract_wt01.py assumed two-digit archive filenames. uf20-09.cnf was preserved; numeric 10 is actually member uf20-010.cnf. No source outcomes examined.'}
with tarfile.open(archive,'r:gz') as tf:
    members={int(pathlib.PurePosixPath(m.name).stem.split('-')[1]):m for m in tf.getmembers() if m.isfile() and pathlib.PurePosixPath(m.name).suffix=='.cnf'}
    for number in manifest['numeric_selection']:
        member=members[number]
        data=tf.extractfile(member).read()
        name=f'uf20-{number:02d}.cnf'
        target=out/name
        if target.exists():
            assert target.read_bytes()==data
        else:
            target.write_bytes(data)
        manifest['files'][name]={'member':member.name,'sha256':hashlib.sha256(data).hexdigest()}
(out/'extraction.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print('Selected',len(manifest['files']),'numeric instances')
