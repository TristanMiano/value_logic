"""Explicit separately identified retry of a failed paid gc02 control."""
from pathlib import Path
import copy
import json
import graph_cover_service as service
root=service.HERE/'gc02';design=json.loads((root/'design.json').read_text());case=copy.deepcopy(next(c for c in design['cases'] if c['name']=='n32_clique'))
if service.g01.sha(service.__file__)!=design['source_sha256']:raise ValueError('Changed frozen implementation')
for name,digest in design['dependencies'].items():
    if service.g01.sha(service.HERE/name)!=digest:raise ValueError('Changed dependency '+name)
case['name']='n32_clique_retry2';directory=root/'n32_clique_scan_retry2'
# The source itself is identical. Copy the immutable evidence bytes under the
# attempt alias so the original frozen runner binds its distinct request IDs.
(root/'n32_clique_retry2_evidence.json').write_bytes((root/'n32_clique_evidence.json').read_bytes())
service.run(root,case,'scan',directory)
