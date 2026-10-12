#!/usr/bin/env python3
"""One small native DRUP export capability probe, separate from repair stream.

DEVELOPMENT, ChatGPT (GPT-6 Astra Pro), 2026-10-12. No general PB encoder,
independent proof checker, or retained checked lower bank is claimed here.
"""
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import inspect
from itertools import combinations
import json
from pathlib import Path
import sys
import time

import pysat.solvers
import pysolvers
from pysat.solvers import Glucose3


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main(destination):
    if destination.exists():
        raise FileExistsError('Preserve prior capability evidence')
    # Each original soft clause [-i] charges 2 when x_i is true. The budget
    # 2*sum(x_i)<=3 is exactly at most one true x, encoded by all pairs.
    # This elementary special case needs no external PB library or labels.
    hard = [[1, 2], [3, 4]]
    bound_cnf = [[-a, -b] for a, b in combinations(range(1, 5), 2)]
    cnf = hard + bound_cnf
    started = datetime.now(timezone.utc).isoformat()
    cpu, wall = time.process_time_ns(), time.perf_counter_ns()
    with Glucose3(with_proof=True, use_timer=True) as solver:
        # Activate proof tracing before any original CNF clauses are loaded.
        solver.append_formula(cnf)
        solver.conf_budget(10_000)
        sat = solver.solve_limited(assumptions=[])
        proof = solver.get_proof()
        stats = solver.accum_stats()
        model = solver.get_model() if sat is True else None
    elapsed = dict(process_ns=time.process_time_ns()-cpu,
                   wall_ns=time.perf_counter_ns()-wall)
    result = dict(status='exported' if sat is False and proof else 'capability_unresolved',
                  evidence='DEVELOPMENT', contributor='ChatGPT (GPT-6 Astra Pro)',
                  start_utc=started, end_utc=datetime.now(timezone.utc).isoformat(),
                  implementation_sha256=sha(__file__),
                  solver=dict(python_sat=importlib.metadata.version('python-sat'),
                              wrapper='Glucose3', solver_version='Glucose 3.0',
                              wrapper_sha256=sha(pysat.solvers.__file__),
                              native_binary_sha256=sha(pysolvers.__file__)),
                  source=dict(variables=4, hard=hard,
                              soft=[dict(clause=[-i], weight=2) for i in range(1, 5)],
                              budget=3),
                  encoding=dict(kind='uniform_weight2_budget3_pairwise_atmost1',
                                budget_clauses=bound_cnf, full_cnf=cnf,
                                clauses=len(cnf), literal_occurrences=sum(map(len, cnf)),
                                auxiliaries=0),
                  native_status='SAT' if sat is True else 'UNSAT' if sat is False else 'UNRESOLVED',
                  proof_lines=proof, proof_ascii_bytes=len(('\n'.join(proof or [])+'\n').encode()),
                  model=model, stats=stats, timing=elapsed,
                  new_native_calls=1, new_diagnostic_optimum_calls=0,
                  conflict_cap=10_000, assumptions=[],
                  independent_checker_executed=False, checked_lower_admitted=False,
                  source_read=dict(Glucose3_new=inspect.getsource(Glucose3.new),
                                   Glucose3_get_proof=inspect.getsource(Glucose3.get_proof)))
    destination.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(status=result['status'], proof=proof, stats=stats,
                          timing=elapsed, calls=1)))


if __name__ == '__main__':
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name('proof_cap_results.json'))
