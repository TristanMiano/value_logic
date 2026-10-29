"""Bounded report/package verification, not a scientific confirmation campaign."""
from pathlib import Path
import hashlib,json,re,subprocess
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def hashes(base,mapping):
    for name,digest in mapping.items():assert sha(base/name)==digest,name
def main():
    manifest=read(HERE/'consistency.json')
    assert sha(HERE/'content.md')==manifest['canonical_sha256']
    assert sha(HERE/'references.json')==manifest['bibliography_sha256']
    assert sha(HERE/'tables/data.json')==manifest['table_data_sha256']
    hashes(ROOT,manifest['generated'])
    hashes(HERE,read(HERE/'upstream.json')['sha256'])
    seals={}
    for name in ['freeze.json','exit_manifest.json']:
        d=read(ROOT/'v3/confirmation/v19a'/name);hashes(ROOT,d['sha256']);seals[name]=len(d['sha256'])
    hashes(ROOT,read(HERE/'tables/data.json')['source_sha256'])
    hashes(ROOT,read(HERE/'episode_result.json')['source_sha256'])
    files=[ROOT/'paper_v3.md',HERE/'claims.md',HERE/'portfolio.md',HERE/'README.md']
    links=0
    for p in files:
        s=p.read_text(encoding='utf-8')
        for url in re.findall(r'\]\(([^)]+)\)',s):
            if re.match('https?://',url):continue
            path,_,anchor=url.partition('#');q=p.parent/path if path else p
            assert q.exists(),(p,url)
            if anchor and q.suffix=='.md':
                target=q.read_text(encoding='utf-8')
                explicit=re.findall(r'<a id="([^"]+)"',target)
                headings=[re.sub(r'[^\w\- ]','',line.strip().lower()).replace(' ','-') for line in re.findall(r'^#+ (.+)$',target,re.M)]
                assert anchor in explicit+headings,(p,url)
            links+=1
    md=(ROOT/'paper_v3.md').read_text(encoding='utf-8')
    assert not re.search(r'\\(?:cite\w*|eqref|ref|label)\b',md)
    # GitHub must receive the exact display payload, including escaped braces,
    # double backslashes in aligned rows, and double-bar norm delimiters.
    # A balanced $$ count alone did not catch the reported rendering failure.
    assert '$$' not in md
    displays=re.findall(r'^```math\n(.*?)^```\s*$',md,re.M|re.S)
    source=(HERE/'content.md').read_text(encoding='utf-8')
    expected=re.findall(r'^```math\n(.*?)^```\s*$',source,re.M|re.S)
    expected=[re.sub(r'\\label\{([\w-]+)\}',lambda m:r'\tag{'+str(manifest['labels'][m[1]][1])+'}',s).strip() for s in expected]
    def math_tokens(parts):
        parts=[re.sub(r'^\{\n(.*)\n\}\n(\\tag\{\d+\})\s*$',r'\1\n\2',s.strip(),flags=re.S) for s in parts]
        s='\n'.join(parts)
        s=s.replace(r'\lt ', '<').replace(r'\gt ', '>').replace(r'\\[0pt]',r'\\')
        return re.sub(r'\s+','',s)
    assert math_tokens(displays)==math_tokens(expected), 'GitHub mathematical payload differs from canonical TeX'
    assert re.findall(r'\\tag\{\d+\}', '\n'.join(displays))==re.findall(r'\\tag\{\d+\}', '\n'.join(expected))
    assert not re.search(r'^:::|\{\{[\w:-]+\}\}',md,re.M)
    # Closing the commitment may change metadata, never the recurrence rows.
    old=json.loads(subprocess.check_output(['git','show','2b9de3ada09521c02eac9094587b2e1d98962f0b:v3/discovery/recurrences.json']))
    new=read(ROOT/'v3/discovery/recurrences.json')
    assert old['rows']==new['rows'] and new['status']=='CLOSED'
    result={'status':'PASS','local_links':links,'preserved_seals':seals,'preserved_recurrence_rows':len(new['rows']),'result_and_equation_labels':len(manifest['labels']),'references':len(manifest['citation_order']),'protected_display_payloads':len(displays),'pdf_sha256':sha(ROOT/'paper_v3.pdf'),'scope':'Package, preserved evidence and format checks; not independent scientific review.'}
    (HERE/'verification.json').write_bytes((json.dumps(result,indent=2)+'\n').encode())
    print(json.dumps(result))
if __name__=='__main__':main()
