"""Exact spectral-measure screen of finite-scale acquisition, DEVELOPMENT."""
from fractions import Fraction as F
from pathlib import Path
from time import perf_counter_ns
import hashlib
import json
import platform

HERE=Path(__file__).resolve().parent
OUT=HERE/'scale_probe.json'
assert not OUT.exists(), 'Replay separately; do not overwrite evidence.'
started=perf_counter_ns()


def moments(spectrum,t):
    assert sum(p for x,p in spectrum)==1
    assert all(0<x<=1 and p>=0 for x,p in spectrum)
    return (sum(p*x for x,p in spectrum),
            sum(p*x/(t-(t-1)*x) for x,p in spectrum),
            sum(p*x*x for x,p in spectrum))


def bounds(s,r,t):
    a=t-1
    assert a>0 and 0<s<1 and s/(t-a*s)<=r<s
    lo=s-t*(1-s)*(s-r)/(a*(1-r))
    hi=s-s*(s-r)/(a*r)
    assert s*s<=lo<=hi<=s
    assert hi-lo==(s-r)/a*(r*(t-a*s)-s)/(r*(1-r))
    return lo,hi


spectra=[[(F(1,10),F(1,2)),(F(9,10),F(1,2))],
         [(F(1,5),F(1,4)),(F(1,2),F(1,4)),(F(4,5),F(1,2))],
         [(F(1,3),F(1))]]
scales=[F(1001,1000),F(101,100),F(11,10),F(3,2),F(2),F(5)]
rows=[]
for spectrum_id,spectrum in enumerate(spectra):
    for t in scales:
        s,r,m=moments(spectrum,t)
        lo,hi=bounds(s,r,t)
        assert lo<=m<=hi
        a=t-1;c=t*(s-r)/(a*(1-r))
        low_spectrum=[(c,(1-s)/(1-c)),(F(1),(s-c)/(1-c))]
        assert moments(low_spectrum,t)==(s,r,lo)
        upper_gaps=[]
        if hi>s*s:
            q0=(1+a*r)/t;h=(t*r-s)/a
            previous=None
            for power in range(1,5):
                epsilon=c/(10**power)
                d=(h-epsilon*r)/(r-epsilon*q0)
                p=(s-epsilon)/(d-epsilon)
                upper_spectrum=[(epsilon,1-p),(d,p)]
                ss,rr,mm=moments(upper_spectrum,t)
                assert (ss,rr)==(s,r) and lo<=mm<=hi
                gap=hi-mm
                if previous is not None:
                    assert gap<previous
                previous=gap
                upper_gaps.append(str(gap))
        else:
            assert lo==hi==m==s*s
        rows.append(dict(spectrum=spectrum_id,t=str(t),s=str(s),r=str(r),m=str(m),
                         lower=str(lo),upper=str(hi),upper_witness_gaps=upper_gaps))

known={row['t']:row for row in rows if row['spectrum']==0}
assert (known['2']['r'],known['2']['lower'],known['2']['upper'])==('91/209','91/236','155/364')
assert tuple(F(known['101/100'][key]) for key in ('r','lower','upper'))==(
    F(504100,1010009),F(829109,2023636),F(8273,20164))

# Feed the close-scale acquired interval to the rational threshold duty.
row=known['1001/1000'];s=F(row['s']);l=F(row['lower']);h=F(row['upper'])
u=F(539,1000);mu=F(11);E=F(1,100);ell=F(288,625)
upper_remainders=[]
for m in (l,h):
    q=s-m;B=m-s*s;a=1-s
    remainder=(u*a*a-(1-u)*(q+B)-mu*E*q-u*u*a*a/(mu+u)
               -(1-u)**2*B/(mu-1+u))
    assert remainder>0
    upper_remainders.append(str(remainder))
vertex=(s*s+ell*s)/(ell*(E+4));x=max(l,min(vertex,h))
K=s*s-ell*(s+E*h)
P=(s*s-ell*(s+E*x))**2-4*ell*ell*E*x*(s-x)
assert K>=0 and P>0

result=dict(status='PASS',contributor='Codex (GPT-6)',classification='DEVELOPMENT',
    python=platform.python_version(),source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    cases=rows,integrated_interval=dict(t=row['t'],r=row['r'],moment_lower=str(l),moment_upper=str(h),
       upper_remainders=upper_remainders,lower_K=str(K),lower_squared=str(P),
       certified_value_lower=str(ell),certified_value_upper=str(u)),
    elapsed_ns=perf_counter_ns()-started,
    limits='Finite rational spectral checks, not independent proof or cost comparison; exact nearby values are paid premises.')
OUT.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:result[k] for k in ('status','source_sha256','integrated_interval','elapsed_ns')}))
