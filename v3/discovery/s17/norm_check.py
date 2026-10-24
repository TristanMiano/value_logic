"""Exact source-norm correction on one saved case; DEVELOPMENT, Codex (GPT-6)."""
from fractions import Fraction as F
from pathlib import Path
from time import perf_counter_ns
import hashlib
import json
import platform
from checker_audit import adj_inverse, mm, transpose, plus, encode

HERE=Path(__file__).resolve().parent
OUT=HERE/'norm_result.json'
if OUT.exists():
    raise SystemExit('Refusing to overwrite an observed result.')
start=perf_counter_ns()
source=HERE/'second_result.json'
data=json.loads(source.read_text())
decode=lambda x:[[F(v) for v in row] for row in x]
dot=lambda a,b:mm(transpose(a),b)[0][0]
scale=lambda a,s:[[s*v for v in row] for row in a]
C,Q=decode(data['C']),decode(data['Q'])
c=decode(data['unnormalized_c'])
normalization=F(data['target_norm_squared'])
alpha=mm(adj_inverse(plus(scale(C,2),Q)),mm(C,c))
offset=plus(c,scale(alpha,2),-1)
H=(dot(offset,offset)-2*dot(offset,mm(C,alpha))+
   dot(alpha,mm(Q,alpha)))/normalization
Cinv=adj_inverse(C)
H_alt=dot(alpha,mm(plus(mm(mm(mm(Q,Cinv),Cinv),Q),Q,-1),alpha))/normalization
assert H==H_alt>0
case=next(r for r in data['cases'] if r['L']==4)
gram=decode(case['source_gram'])
K2=sum(gram[i][i] for i in range(len(gram)))
correction=H/(3+2*K2)
lower=F(data['lower_infimum'])
improved=lower+correction
actual=F(case['value'])
assert lower<F(1,10)<improved<actual
record=dict(status='PASS',L=4,K_squared_warrant=str(K2),H=str(H),
            lower=str(lower),correction=str(correction),improved=str(improved),
            threshold='1/10',actual=str(actual),elapsed_ns=perf_counter_ns()-start,
            python=platform.python_version(),
            source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            input_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
            helper_sha256=hashlib.sha256((HERE/'checker_audit.py').read_bytes()).hexdigest(),
            scope='One exact noncommuting example; the trace supplies a truthful conservative squared operator-norm warrant.')
OUT.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(dict(status=record['status'],lower=str(lower),
                     improved=str(improved),improved_decimal=float(improved),
                     elapsed_ns=record['elapsed_ns'])))
