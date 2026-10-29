"""Build both editions from content.md and a single bibliography; no scientific reruns."""
from pathlib import Path
import argparse, hashlib, json, re, shutil, subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pandoc', default='pandoc')
    ap.add_argument('--tectonic', default='tectonic')
    ap.add_argument('--pdf', action='store_true')
    args = ap.parse_args()
    subprocess.run(['python', '-X', 'utf8', str(HERE/'tables.py')], check=True)
    raw = (HERE/'content.md').read_text(encoding='utf-8')
    # Canonical Markdown follows the repository's GitHub math-fence convention.
    # Normalize only internally so Pandoc and numbered-equation handling agree.
    raw = re.sub(r'^```math\n(.*?)^```\s*$', lambda m: '$$\n'+m[1].rstrip()+'\n$$', raw, flags=re.M|re.S)
    for p in (HERE/'tables').glob('*.md'):
        raw = raw.replace('{{table:'+p.stem+'}}', p.read_text(encoding='utf-8').strip())
    refs = json.loads((HERE/'references.json').read_text(encoding='utf-8'))
    by_id = {r['id']:r for r in refs}
    order = list(dict.fromkeys(re.findall(r'\[@([\w-]+)\]',raw)))
    assert all(k in by_id for k in order)
    assert set(order)==set(by_id), 'Uncited bibliography entry'
    labels, n, e = {}, 0, 0
    for m in re.finditer(r'^::: (definition|theorem|lemma|proposition) ([\w-]+) \| (.+)$|\\label\{([\w-]+)\}',raw,re.M):
        if m[4]:
            e += 1; labels[m[4]]= ('equation',e)
        else:
            n += 1; labels[m[2]]=(m[1],n)
    def xref(m,tex):
        k=m[1];kind,num=labels[k]
        if tex: return ('Equation ' if kind=='equation' else kind.title()+' ')+'\\ref{'+k+'}'
        return f'[{"Equation" if kind=="equation" else kind.title()} {num}](#{k})'
    def edition(tex):
        s=raw.replace('](../', '](v3/')
        def block(m):
            kind,key,title,body=m.groups();num=labels[key][1]
            if tex: return '\n```{=latex}\n\\begin{'+kind+'}['+title+']\\label{'+key+'}\n```\n'+body+'\n```{=latex}\n\\end{'+kind+'}\n```\n'
            return f'\n<a id="{key}"></a>\n\n**{kind.title()} {num} ({title}).**\n'+body+'\n'
        s=re.sub(r'^::: (definition|theorem|lemma|proposition) ([\w-]+) \| ([^\n]+)\n(.*?)^:::\s*$',block,s,flags=re.M|re.S)
        def proof(m):
            body=m[1]
            return ('\n```{=latex}\n\\begin{proof}\n```\n'+body+'\n```{=latex}\n\\end{proof}\n```\n') if tex else '\n**Proof.** '+body.strip()+' $\\square$\n'
        s=re.sub(r'^::: proof\n(.*?)^:::\s*$',proof,s,flags=re.M|re.S)
        def eq(m):
            body=m[1];lab=re.search(r'\\label\{([\w-]+)\}',body)
            if not lab: return m[0] if tex else '```math\n'+body+'\n```'
            key=lab[1]
            if tex: return '\n```{=latex}\n\\begin{equation}\n'+body.strip()+'\n\\end{equation}\n```\n'
            # Protect TeX backslashes from GitHub's Markdown escape processing.
            body=body.replace(lab[0],r'\tag{'+str(labels[key][1])+r'}').strip()
            # GitHub's live renderer rejected the aligned environment even
            # after escapes were preserved. Stack its unchanged rows as separate
            # displays, with the shared number on the final row.
            aligned=re.fullmatch(r'\\begin\{aligned\}(.*?)\\end\{aligned\}\s*(\\tag\{\d+\})',body,re.S)
            if aligned:
                rows=[s.replace('&','').strip() for s in re.split(r'\\\\',aligned[1])]
                rows[-1]+='\n'+aligned[2]
            else: rows=[body]
            return f'\n<a id="{key}"></a>\n\n'+'\n\n'.join('```math\n'+s+'\n```' for s in rows)+'\n'
        s=re.sub(r'\$\$\n(.*?)\n\$\$',eq,s,flags=re.S)
        s=re.sub(r'\{\{([\w-]+)\}\}',lambda m:xref(m,tex),s)
        s=re.sub(r'\[@([\w-]+)\]',lambda m:('\\citep{'+m[1]+'}') if tex else f'[{order.index(m[1])+1}](#ref-{m[1]})',s)
        if tex:
            s=re.sub(r'\$`(.*?)`\$', r'$\1$', s, flags=re.S)
            s=re.sub(r'\]\((v3/[^)]+)\)',r'](https://github.com/TristanMiano/value_logic/blob/main/\1)',s)
        else:
            s=re.sub(r'^(#+) (.+) \{#([\w-]+)\}$',lambda m:'<a id="'+m[3]+'"></a>\n\n'+m[1]+'# '+m[2],s,flags=re.M)
        return s
    md=edition(False)
    bibmd=[];bib=[]
    for i,k in enumerate(order,1):
        r=by_id[k]
        bibmd.append(f'<a id="ref-{k}"></a>\n\n{i}. {r["display_author"]}. *[{r["title"]}]({r["url"]})*. {r["venue"]}, {r["year"]}.')
        # Metadata uses literal TeX-compatible author names; protect title capitalization.
        bib.append('@misc{'+k+',\n  author = {'+r['bib_author']+'},\n  title = {{'+r['title']+'}},\n  year = {'+str(r['year'])+'},\n  howpublished = {'+r['venue']+'},\n  url = {'+r['url']+'}\n}')
    title='# Useful Decisions under Unresolved Mathematics\n\n## A phase-three synthesis of Value Logic\n\nTristan Miano, project author. Research contributions: ChatGPT (GPT-6 Astra Pro) and Codex (GPT-6); synthesis: Codex (GPT-6). October 2026.\n\n'
    (ROOT/'paper_v3.md').write_text(title+md+'\n## References\n\n'+'\n\n'.join(bibmd)+'\n',encoding='utf-8',newline='\n')
    (HERE/'tex/references.bib').write_text('\n\n'.join(bib)+'\n',encoding='utf-8',newline='\n')
    build=HERE/'build';build.mkdir(exist_ok=True)
    (build/'paper.md').write_text(edition(True),encoding='utf-8',newline='\n')
    command=[args.pandoc,str(build/'paper.md'),'-f','markdown+raw_tex+fenced_divs','-t','latex','--standalone','--template',str(HERE/'template.tex'),'-o',str(HERE/'tex/main.tex')]
    subprocess.run(command,check=True)
    # Explicit edition checks: every numbered result/equation and citation is accounted for.
    tex=(HERE/'tex/main.tex').read_text(encoding='utf-8').replace('\n\n\\end{proof}', '\n\\end{proof}')
    (HERE/'tex/main.tex').write_text(tex,encoding='utf-8',newline='\n')
    for key in labels: assert '\\label{'+key+'}' in tex and f'id="{key}"' in md,key
    assert not re.search(r'\\(?:cite|ref|eqref|label)\b',md)
    assert not re.search(r'\{\{[^}]+\}\}|^:::',md,re.M)
    manifest={'canonical_sha256':sha(HERE/'content.md'),'bibliography_sha256':sha(HERE/'references.json'),'table_data_sha256':sha(HERE/'tables/data.json'),'labels':labels,'citation_order':order,'generated':{str(p.relative_to(ROOT)).replace('\\','/'):sha(p) for p in [ROOT/'paper_v3.md',HERE/'tex/main.tex',HERE/'tex/references.bib']},'method':'Both editions generated from identical expanded content; only math, reference, and link syntax differ.'}
    if args.pdf:
        subprocess.run([args.tectonic,'--keep-logs','--keep-intermediates','main.tex'],cwd=HERE/'tex',check=True)
        shutil.copyfile(HERE/'tex/main.pdf',ROOT/'paper_v3.pdf')
        manifest['generated']['paper_v3.pdf']=sha(ROOT/'paper_v3.pdf')
    (HERE/'consistency.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'results_and_equations':len(labels),'references':len(order),'pdf':args.pdf}))

if __name__=='__main__':main()
