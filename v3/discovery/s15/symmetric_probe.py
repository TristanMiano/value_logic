"""Exact explicit-channel screen, without importing either numerical policy."""
from decimal import Decimal,localcontext
from fractions import Fraction as F
from itertools import combinations
import hashlib,json
from pathlib import Path
from time import perf_counter_ns
HERE=Path(__file__).resolve().parent
OUT=HERE/'symmetric_probe.json'
assert not OUT.exists()
start=perf_counter_ns()
def syndrome(x):
    s=0
    for i in range(7):
        if (x>>i)&1:s^=i+1
    return s
def center(x):
    s=syndrome(x)
    return x if s==0 else x^(1<<(s-1))
code=[x for x in range(128) if center(x)==x]
def numer(x,omitted):
    known=[i for i in range(7) if i not in omitted]
    ones=[i for i in known if (x>>i)&1]
    if len(ones)<=1:return 0
    if len(ones)>=4:return 4
    selected=ones if len(ones)==2 else [i for i in known if i not in ones]
    label=(selected[0]+1)^(selected[1]+1)
    special=label in [i+1 for i in omitted]
    return (3 if special else 4) if len(ones)==2 else (1 if special else 0)
pairs=list(combinations(range(7),2))
prob={x:F(sum(numer(x,p) for p in pairs),84) for x in range(128)}
assert all(prob[x]==F(center(x).bit_count(),7) for x in range(128))
translations=0
for c0 in code:
    for x in range(128):
        assert center(x^c0)==center(x)^c0
        assert prob[x^c0]==F((center(x)^c0).bit_count(),7)
        assert (prob[x^c0]==0)==(center(x)==c0)
        translations+=1
for x in range(128):
    for pair in pairs:
        for coin in range(4):
            accept=coin<numer(x,pair)
            known=[i for i in range(7) if i not in pair]
            queried=known if accept else known+[pair[0]]
            assert len(queried)==len(set(queried))==(5 if accept else 6)

a,b=F(4,7),F(3,7)
union=lambda r:7*a**r+7*b**r
exact_tail=lambda r:1-(1-a**r)**7*(1-b**r)**7
rounds=next(r for r in range(1,100) if union(r)<=F(1,100))
assert rounds==1 or union(rounds-1)>F(1,100)
assert exact_tail(rounds)<=union(rounds)
partial=1+sum(exact_tail(r) for r in range(1,41))
remainder=7*a**41/(1-a)+7*b**41/(1-b)
max_rounds_upper=partial+remainder
wrong_visits=F(7)*(F(7,3)+F(7,4)+F(1,7))
episodes_upper=wrong_visits+max_rounds_upper
queries_upper=6*episodes_upper-15
def dec(z):
    with localcontext() as ctx:
        ctx.prec=30
        return str(Decimal(z.numerator)/Decimal(z.denominator))
result=dict(status='PASS',classification='DEVELOPMENT; exact all-input explicit rule',
  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
  elapsed_ns=perf_counter_ns()-start,inputs=128,pairs_per_input=21,private_coin_outcomes=4,
  translated_channel_checks=translations,acceptance='weight(Q(x))/7',cap=6,
  no_false_elimination=True,as_termination='Theoretical almost-sure result under fresh independent episodes',
  complete_rounds_for_99pct=rounds,max_episodes_at_round_cap=16*rounds,
  completion_failure_union_upper=str(union(rounds)),completion_failure_exact=str(exact_tail(rounds)),
  expected_wrong_visits=str(wrong_visits),expected_max_rounds_upper=str(max_rounds_upper),
  expected_episodes_upper=str(episodes_upper),expected_queries_upper=str(queries_upper),
  expected_episodes_upper_decimal=dec(episodes_upper),expected_queries_upper_decimal=dec(queries_upper),
  max_round_tail_remainder_upper=dec(remainder),
  limits='Expectations bounded analytically; no sampled runtime, no full computation bill, averaged privacy.')
OUT.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k not in
  ('expected_max_rounds_upper','expected_episodes_upper','expected_queries_upper','completion_failure_exact')},indent=2))
