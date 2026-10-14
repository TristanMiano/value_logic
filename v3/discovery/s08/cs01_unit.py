"""One isolated unchanged cs01 arm; wrapper only, no policy modification."""
from pathlib import Path
import importlib.util
import json
import sys
import traceback

HERE=Path(__file__).resolve().parent
ROOT=HERE/'cs01'
spec=importlib.util.spec_from_file_location('frozen_continuum_service',ROOT/'impl.py')
service=importlib.util.module_from_spec(spec);spec.loader.exec_module(service)
design=json.loads((ROOT/'design.json').read_text())
case=next(c for c in design['cases'] if c['name']==sys.argv[1]);arm=sys.argv[2]
assert arm in design['arms']
for name,digest in design['dependencies'].items():assert service.g01.sha(HERE/name)==digest
assert service.g01.sha(ROOT/'impl.py')==design['source_sha256']
assert not(ROOT/f"{case['name']}_{arm}.jsonl").exists()
try:
    data=service.source(case['costs']);rows=service.ms.draw(data['n'],case['r'],design['requests'],case['seed'])
    result=service.run_arm(ROOT,case,data,rows,arm)
    service.g01.save(ROOT/f"{case['name']}_{arm}_result.json",result)
except BaseException:
    (ROOT/f"{case['name']}_{arm}_failure.txt").write_text(traceback.format_exc())
    raise
