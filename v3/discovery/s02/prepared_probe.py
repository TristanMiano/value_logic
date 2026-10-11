"""DEVELOPMENT: reusable ordinary threshold SAT versus identical guarded kernel.

Codex (GPT-6), 2026-10-11. Fixed action/tolerance/loss version, single-clause
counterfactual deletion from a shared admitted parent. Warm lifecycle timings.
"""
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction as F
from math import lcm
import hashlib
import json
from pathlib import Path
import sys
import time
import traceback

from tolerance_v2 import affine, threshold, Minisat22
from decision_probe import compatible, row


class Prepared:
    def __init__(self,n,clauses,actions,p,epsilon,old_upper,guarded):
        assert old_upper <= epsilon
        self.n,self.clauses,self.actions,self.p = n,tuple(tuple(c) for c in clauses),actions,p
        self.epsilon,self.guarded = epsilon,guarded
        self.contrasts = [affine(actions,p,a) for a in range(len(actions))]
        self.cube = [c+sum(max(F(0),w) for w in weights) for c,weights in self.contrasts]
        self.prepared = {}
        self.counts = Counter()

    def build(self,a):
        constant,coeff = self.contrasts[a]
        denominator = lcm(*(v.denominator for v in [constant,self.epsilon]+coeff))
        ints = [int(v*denominator) for v in coeff]
        weighted = [(i+1 if value>0 else -(i+1),abs(value)) for i,value in enumerate(ints) if value]
        target = int((self.epsilon-constant)*denominator)+sum(-v for v in ints if v<0)+1
        assert target <= sum(w for _,w in weighted)
        extras,aux = ([],0) if target<=0 else threshold(self.n,weighted,target)
        offset = self.n+aux+1
        hard = extras+[[-(offset+i),*c] for i,c in enumerate(self.clauses)]
        solver = Minisat22(bootstrap_with=hard)
        self.counts['solver_builds'] += 1
        self.counts['encoded_clauses'] += len(extras)
        self.counts['installed_clauses'] += len(hard)
        self.counts['auxiliary_variables'] += aux
        self.prepared[a] = solver,offset
        return solver,offset

    def query(self,index):
        self.counts['requests'] += 1
        removed = self.clauses[index]
        fixed = {}
        if self.guarded:
            # Include this linear source scan; no free duplicate index assumed.
            self.counts['duplicate_clause_comparisons'] += len(self.clauses)-1
            if any(c==removed for i,c in enumerate(self.clauses) if i!=index) or any(-lit in removed for lit in removed):
                self.counts['same_source'] += 1
                return True
            fixed = {abs(lit)-1:int(lit<0) for lit in removed}
            delta_box = max(u+sum(weights[i]*bit-max(F(0),weights[i]) for i,bit in fixed.items())
                            for u,(_,weights) in zip(self.cube,self.contrasts))
            self.counts['guard_coefficient_visits'] += len(fixed)*len(self.actions)
            if delta_box <= self.epsilon:
                self.counts['box_guard'] += 1
                return True
        for a,cube in enumerate(self.cube):
            if cube <= self.epsilon:
                continue
            solver,offset = self.prepared.get(a) or self.build(a)
            assumptions = [-(offset+i) if i==index else offset+i for i in range(len(self.clauses))]
            assumptions += [i+1 if bit else -(i+1) for i,bit in fixed.items()]
            self.counts['assumption_literals'] += len(assumptions)
            self.counts['sat_calls'] += 1
            if solver.solve(assumptions=assumptions):
                model = set(solver.get_model() or [])
                x = tuple(int(i+1 in model) for i in range(self.n))
                rest = self.clauses[:index]+self.clauses[index+1:]
                assert compatible(x,rest)
                assert sum(q*v for q,v in zip(self.p,row(x,self.actions))) > self.epsilon
                return False
        return True

    def close(self):
        for solver,_ in self.prepared.values():
            solver.delete()


def run(case,indices,guarded):
    n,clauses,actions=case['n'],case['request']['clauses'],case['request']['actions']
    p=tuple(F(v) for v in case['action'])
    bound=F(case['old_upper'])
    start=time.perf_counter_ns()
    engine=Prepared(n,clauses,actions,p,bound,bound,guarded)
    try:
        answers=[engine.query(index) for index in indices]
        counts=dict(engine.counts)
    finally:
        engine.close()
    return dict(guarded=guarded,answers=answers,counts=counts,elapsed_ns=time.perf_counter_ns()-start)


def main(output):
    assert not output.exists()
    started=time.monotonic_ns()
    source=Path(__file__).with_name('delta01.json')
    result=dict(status='running',evidence='DEVELOPMENT',contributor='Codex (GPT-6)',
                start_utc=datetime.now(timezone.utc).isoformat(),command=sys.argv,
                sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                         (Path(__file__),Path(__file__).with_name('tolerance_v2.py'),Path(__file__).with_name('decision_probe.py'))},
                input_record=dict(path=source.name,sha256=hashlib.sha256(source.read_bytes()).hexdigest()),
                scope='warm whole-service construction, retained solver state, all queries/checks and cleanup; old certified bound shared input; native UNSAT trust')
    try:
        originals=json.loads(source.read_text())['cases'][::2]
        rows=[]
        for case_no,case in enumerate(originals):
            indices=list(range(len(case['request']['clauses'])))
            for repetition in range(2):
                ordered=indices if repetition==0 else list(reversed(indices))
                first=run(case,ordered,bool(repetition))
                second=run(case,ordered,not bool(repetition))
                assert first['answers']==second['answers']
                for answer in (first,second):
                    answer.update(case=case_no,n=case['n'],indices=ordered,repetition=repetition)
                    rows.append(answer)
        result.update(status='complete',rows=rows,answer_comparisons=sum(len(r['answers']) for r in rows))
    except Exception:
        result.update(status='failed',failure=traceback.format_exc())
        raise
    finally:
        result['elapsed_ns']=time.monotonic_ns()-started
        result['end_utc']=datetime.now(timezone.utc).isoformat()
        output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
        print(json.dumps({k:v for k,v in result.items() if k!='rows'}))


if __name__=='__main__':
    main(Path(sys.argv[1]))
