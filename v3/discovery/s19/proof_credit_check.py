"""Developmental hidden-work probe; controller never receives completion lengths."""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import hashlib, json, random, time, traceback

SEED=191926

class Oracle:
    def __init__(self, length):
        self._length=length
        self.calls=0
    def step(self):
        self.calls+=1
        return self._length is not None and self.calls==self._length

def satisfied(clauses, bank):
    return all(any(j in bank for j in clause) for clause in clauses)

def run(steppers, requests, order='first'):
    m=len(steppers)
    credit=[Q(0) for _ in range(m)]
    instructions=[0]*m
    bank=set()
    dual=[]
    fallback=Q(0)
    fallback_rounds=0
    for clauses,price in requests:
        used=Q(0)
        row=[Q(0)]*len(clauses)
        while not satisfied(clauses,bank) and used<price:
            unsat=[a for a,c in enumerate(clauses) if not any(j in bank for j in c)]
            a=unsat[0] if order=='first' else unsat[-1]
            clause=clauses[a]
            delta=min([price-used]+[Q(credit[j].numerator//credit[j].denominator+1)-credit[j] for j in clause])
            assert delta>0
            used+=delta
            row[a]+=delta
            for j in clause:
                credit[j]+=delta
            # Finish every instruction due at the same credit crossing.
            for j in clause:
                if credit[j].denominator==1:
                    assert instructions[j]+1==credit[j]
                    instructions[j]+=1
                    if steppers[j]():
                        bank.add(j)
        if not satisfied(clauses,bank):
            fallback+=price
            fallback_rounds+=1
            assert used==price
        dual.append(row)
    return dict(credit=credit,instructions=instructions,bank=sorted(bank),dual=dual,
                fallback=fallback,fallback_rounds=fallback_rounds,
                work=sum(instructions),bill=Q(sum(instructions))+fallback)

def offline(lengths, requests):
    m=len(lengths)
    candidates=[]
    for mask in range(1<<m):
        bank={j for j in range(m) if mask>>j&1}
        if any(lengths[j] is None for j in bank):
            continue
        value=Q(sum(lengths[j] for j in bank))
        value+=sum((price for clauses,price in requests if not satisfied(clauses,bank)),Q(0))
        candidates.append((value,mask))
    return min(candidates)

def check(lengths, requests, order='first'):
    machines=[Oracle(r) for r in lengths]
    r=run([machine.step for machine in machines],requests,order)
    dual=sum((sum(row,Q(0)) for row in r['dual']),Q(0))
    d=max([len(c) for clauses,price in requests for c in clauses]+[0])
    for j,length in enumerate(lengths):
        col=sum((row[a] for (clauses,price),row in zip(requests,r['dual']) for a,c in enumerate(clauses) if j in c),Q(0))
        assert col==r['credit'][j]
        assert r['instructions'][j]==col.numerator//col.denominator
        assert length is None or col<=length
        assert machines[j].calls==r['instructions'][j]
    for (clauses,price),row in zip(requests,r['dual']):
        assert sum(row,Q(0))<=price
    opt,mask=offline(lengths,requests)
    assert dual<=opt
    assert r['bill']<=(d+1)*dual
    r.update(opt=opt,offline_mask=mask,dual_value=dual,width=d,
             ratio=r['bill']/opt if opt else Q(1))
    return r

def serial(value):
    if isinstance(value,Q):return str(value)
    if isinstance(value,dict):return {str(k):serial(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)):return [serial(v) for v in value]
    return value

def main():
    rng=random.Random(SEED)
    cases=[]
    # Exhaustive short one-clause schedules and rational prices.
    for lengths in product((1,2,3,None),repeat=2):
        for prices in product((Q(0),Q(1,3),Q(1),Q(3,2)),repeat=3):
            cases.append((lengths,[([(0,1)],p) for p in prices]))
    # Complementarity, shared primitives, empty conditions and impossible clauses.
    for _ in range(400):
        m=rng.randint(1,6)
        lengths=tuple(rng.choice((1,2,4,9,None)) for j in range(m))
        requests=[]
        for t in range(rng.randint(1,10)):
            clauses=[]
            for a in range(rng.randint(0,4)):
                clause=tuple(sorted(rng.sample(range(m),rng.randint(0,min(3,m)))))
                clauses.append(clause)
            requests.append((clauses,Q(rng.randint(0,9),rng.choice((1,2,3,5)))))
        cases.append((lengths,requests))
    encoded=json.dumps(serial(cases),sort_keys=True,separators=(',',':')).encode()
    worst=Q(0)
    worst_case=None
    total_instructions=0
    checks=0
    for case_id,(lengths,requests) in enumerate(cases):
        for order in ('first','last'):
            result=check(lengths,requests,order)
            checks+=1
            total_instructions+=result['work']
            if result['ratio']>worst:
                worst=result['ratio']
                worst_case=dict(case_id=case_id,lengths=lengths,requests=requests,order=order,result=result)
    worked={}
    worked['two_alternatives']=check((10,None),[([(0,1)],Q(1))]*40)
    worked['two_required_lemmas']=check((10,None,10,None),[([(0,1),(2,3)],Q(1))]*40)
    worked['fractional_credit']=check((1,None),[([(0,1)],Q(1,10))]*10)
    return dict(status='PASS',seed=SEED,input_sha256=hashlib.sha256(encoded).hexdigest(),
                generated_cases=len(cases),policy_checks=checks,total_instructions=total_instructions,
                worst_ratio=worst,worst_case=worst_case,worked=worked,
                scope='Hidden integer completion oracles, exact rational budgets, finite offline subset enumeration; no actual proof search, wall-clock economics, or novelty established.')

if __name__=='__main__':
    start=time.perf_counter_ns()
    try:
        result=main()
    except Exception:
        result=dict(status='FAIL',traceback=traceback.format_exc())
    result['runtime_ns']=time.perf_counter_ns()-start
    result['source_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    target=Path(__file__).with_name('proof_credit_result.json')
    assert not target.exists(), 'Preserve a prior result; use a new version for a new run.'
    target.write_bytes((json.dumps(serial(result),indent=2)+'\n').encode())
    print(json.dumps(serial({k:v for k,v in result.items() if k not in ('worst_case','worked')}),indent=2))
    if result['status']!='PASS':raise SystemExit(1)
