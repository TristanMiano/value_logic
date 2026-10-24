"""Exact strong-control width comparison; DEVELOPMENT, Codex (GPT-6)."""
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
from time import perf_counter_ns
import hashlib
import json
import platform

HERE=Path(__file__).resolve().parent
OUT=HERE/'width_result.json'
if OUT.exists():
    raise SystemExit('Refusing to overwrite an observed result.')
start=perf_counter_ns()
def sqrt_interval(q,digits=12):
    scale=10**digits
    n=isqrt(q.numerator*scale**2//q.denominator)
    lo,hi=F(n,scale),F(n+1,scale)
    assert lo*lo<=q<hi*hi
    return lo,hi

rlo,rhi=sqrt_interval(F(41))
lower_lo=F(2500)/(5041+60*rhi)
lower_hi=F(2500)/(5041+60*rlo)
zlo,zhi=sqrt_interval(F(415769,1000000))
j=lambda z:F(50129681,100000000)+F(291,5000)*z
dj=lambda z:-F(14127,500000)+F(3,50)*z-F(297693,50000000)/z
derivative_abs=max(abs(dj(zlo)),abs(dj(zhi)))
mu=F(9,50)
upper_lo=j(zlo)-derivative_abs**2/(2*mu)
upper_hi=j(zhi)
assert upper_lo>F(1077,2000)
width_lo=upper_lo-lower_hi
width_hi=upper_hi-lower_lo
block_lower=F(618573873750,1340748094907)
block_upper=F(867127945275459,1611861132384100)
certificate_width=block_upper-block_lower
gain_lo=1-certificate_width/width_lo
gain_hi=1-certificate_width/width_hi
assert 0<gain_lo<=gain_hi<1
record=dict(status='PASS',lower_endpoint_interval=list(map(str,(lower_lo,lower_hi))),
            upper_endpoint_interval=list(map(str,(upper_lo,upper_hi))),
            width_interval=list(map(str,(width_lo,width_hi))),
            block_certificate_width=str(certificate_width),
            certificate_width_reduction_interval=list(map(str,(gain_lo,gain_hi))),
            decimal_summary=dict(two_scalar_lower=[float(lower_lo),float(lower_hi)],
                                 two_scalar_upper=[float(upper_lo),float(upper_hi)],
                                 two_scalar_width=[float(width_lo),float(width_hi)],
                                 block_certificate_width=float(certificate_width),
                                 fractional_reduction=[float(gain_lo),float(gain_hi)]),
            elapsed_ns=perf_counter_ns()-start,python=platform.python_version(),
            source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            scope='Exact enclosure using s14 sharp two-scalar formulas and strong convexity; chosen block certificate need not be exactly optimal.')
OUT.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(dict(status='PASS',**record['decimal_summary'],elapsed_ns=record['elapsed_ns'])))
