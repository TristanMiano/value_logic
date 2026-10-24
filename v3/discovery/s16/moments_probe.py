"""Exact-rational DEVELOPMENT witnesses; no numerical optimizer or overwrite."""
from fractions import Fraction as F
from pathlib import Path
from time import perf_counter_ns
import hashlib
import json
import platform

HERE = Path(__file__).resolve().parent
OUT = HERE / 'moments_probe.json'
assert not OUT.exists(), 'Replay in an isolated directory; preserve original evidence.'
started = perf_counter_ns()


def response(matrix):
    """Solve (I+M M^T)w=(1,0) by its exact two-dimensional inverse."""
    a = 1 + sum(x*x for x in matrix[0])
    b = sum(x*y for x, y in zip(matrix[0], matrix[1]))
    d = 1 + sum(y*y for y in matrix[1])
    det = a*d-b*b
    assert det > 0
    return (d/det, -b/det)


def columns(first, second=None):
    return [[first[i]] + ([] if second is None else [second[i]]) for i in range(2)]


sources = []
for s, radius in [(F(1,5), F(2,5)), (F(1,2), F(1,2)), (F(4,5), F(2,5))]:
    assert radius**2 == s-s*s
    for sine, cosine in [(F(0),F(1)), (F(3,5),F(4,5)), (F(4,5),F(3,5))]:
        b = radius*sine
        rootq = radius*cosine
        m = s*s+b*b
        q = s-m
        assert rootq*rootq == q and q > 0
        w = (s,b)
        d = (1-s,-b)
        first = tuple(x/rootq for x in d)
        assert response(columns(first)) == w
        sources.append((s,m,q,rootq,w,d,first))

lower_rows = []
upper_rows = []
for s,m,q,rootq,w,d,first in sources:
    for rho in (F(0),F(1,10),F(1,2)):
        # ||rho*w||^2=rho^2*m; sqrt(q) is rational for these sources.
        bound = s*s/(m+(rootq+rho*m)**2)
        previous = None
        gaps = []
        for scale in (1,10,100,1000):
            second = (-scale*w[1], scale*w[0])
            old = columns(first, second)
            assert response(old) == w
            edited = columns(tuple(first[i]+rho*w[i] for i in range(2)), second)
            actual = response(edited)[0]
            assert actual >= bound
            if previous is not None:
                assert actual <= previous
            previous = actual
            gaps.append(str(actual-bound))
        lower_rows.append(dict(s=str(s),m=str(m),edit_norm_squared=str(rho*rho*m),
                               lower=str(bound),scales=[1,10,100,1000],gaps=gaps))
    for e in (F(0),F(1,10),F(1,2)):
        for cosine,sine in ((F(1),F(0)),(F(4,5),F(3,5)),(F(3,5),F(4,5)),(F(0),F(1))):
            h = (-e*rootq*cosine, -e*rootq*sine)
            assert sum(x*x for x in h) == e*e*q
            edited = columns(tuple((d[i]+h[i])/rootq for i in range(2)))
            actual = response(edited)[0]
            x = 1-s-e*rootq*cosine
            y = w[1]+e*rootq*sine
            predicted = (q+y*y)/(x*x+q+y*y)
            assert actual == predicted
            upper_rows.append(dict(s=str(s),m=str(m),e=str(e),
                                   cosine=str(cosine),sine=str(sine),value=str(actual)))

# Strict outward arithmetic for the new partial-moment certificate.
t = F(31,32)
C = 1-t+t*t/2
assert F(9,100) < C/(2*t*t)
root_upper = F(206401,1000)
assert root_upper*root_upper > 42601
upper = F(1025,2048)+F(93,512000)*root_upper+F(8649,10240000)
assert upper < F(539,1000)
# The previous fixed-primal expression exceeds the new decision threshold.
assert F(5009,10000)+F(192,10)/500 > F(539,1000)
assert F(192,10)**2 < 369
# A finite exact witness nearly reaches the new upper decision boundary.
example = F(66181,122825)
assert F(5388,10000) < example < upper

# The joint-proof numerical example uses exact integer comparisons.
joint = F(11,10)**90*F(3,5)**10
assert joint > 20
assert F(3,5)**100 < 1

result = dict(
    status='PASS', contributor='Codex (GPT-6)', classification='DEVELOPMENT',
    python=platform.python_version(),
    source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    source_count=len(sources), lower_families=lower_rows,
    upper_witnesses=upper_rows, strengthened_upper=str(upper),
    upper_threshold='539/1000', near_upper_witness=str(example),
    joint_proof_wealth=str(joint), elapsed_ns=perf_counter_ns()-started,
    limits='Finite exact witness checks; not independent review, general proof, or runtime comparison.')
OUT.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:result[k] for k in ('status','source_sha256','source_count','strengthened_upper','elapsed_ns')}))
