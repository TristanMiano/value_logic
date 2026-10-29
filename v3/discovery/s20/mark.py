"""Validated administrative clock client; never changes the resident clock code."""
from pathlib import Path
import json
import socket
import sys

HERE=Path(__file__).resolve().parent
mode,lane,purpose,*words=sys.argv[1:]
assert mode in ('D','L','E','O','wait','idle','unmeasured')
assert (lane in ('R','X')) if mode in ('D','L','E') else (lane=='-')
assert purpose in ('generation','screening','synthesis','administration','context','wait')
c=json.loads((HERE/'control.tmp').read_text())
request=dict(command='mark',mode=mode,lane=lane,purpose=purpose,note=' '.join(words))
with socket.create_connection(('127.0.0.1',c['port']),timeout=5) as client:
    client.sendall((json.dumps(request)+'\n').encode())
    r=json.loads(client.makefile('r').readline())
print(json.dumps(dict(observed=r['observed'],research_ns=r['research_ns'],
                     research_minutes=r['research_minutes'],open_segment=r['open_segment'])))
