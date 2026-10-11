"""DEVELOPMENT: exercise the previously untested activation-log reset.

Codex (GPT-6), 2026-10-11. Targeted constructive check, not confirmation.
"""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
import time

from library_probe import LazyEngine, alternations
from revision_probe import run


def main(output):
    assert not output.exists()
    started = time.monotonic_ns()
    rows = []
    for n in (4,8,12):
        stream = alternations(n)
        expected = run(stream,'fresh')['answers']
        for capacity in (1,2,4):
            engine = LazyEngine(n,capacity,max_active=2*n)
            try:
                for cid,c in stream['initial']:
                    engine.edit(engine.version,'add',cid,c)
                answers = [engine.answer()]
                for op,cid,c in stream['patches']:
                    engine.edit(engine.version,op,cid,c)
                    answers.append(engine.answer())
                    assert len(engine.activations) < 4*n
                    assert len(engine.active) <= 2*n
                assert answers == expected and engine.counts['rebases'] > 0
                rows.append(dict(n=n,capacity=capacity,counts=dict(engine.counts),answers=''.join(map(str,answers))))
            finally:
                engine.close()
    result=dict(status='complete',evidence='DEVELOPMENT',contributor='Codex (GPT-6)',
                end_utc=datetime.now(timezone.utc).isoformat(),elapsed_ns=time.monotonic_ns()-started,
                command=sys.argv,rows=rows,
                sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                         (Path(__file__),Path(__file__).with_name('library_probe.py'),Path(__file__).with_name('revision_probe.py'))})
    output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='rows'}))


if __name__ == '__main__':
    main(Path(sys.argv[1]))
