"""Checked value queries from a rational CDF band; DEVELOPMENT.

ChatGPT (GPT-6 Astra Pro), 2026-10-12. SciPy proposes LP duals; rational
arithmetic checks their warranted values. No new source labels are acquired.
This prices bounded payoffs on H, not actual CNF costs omitted from H.
"""
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path
import platform
import sys
import time

import numpy as np
import scipy
from scipy.optimize import linprog


class CDFValues:
    def __init__(self, lower, upper):
        self.lower, self.upper = tuple(map(F, lower)), tuple(map(F, upper))
        if not self.lower or len(self.lower) != len(self.upper):
            raise ValueError('Mismatched nonempty CDF bounds')
        for l, u in zip(self.lower, self.upper):
            if not 0 <= l <= u <= 1:
                raise ValueError('Invalid CDF bound')
        if any(a > b for values in (self.lower, self.upper)
               for a, b in zip(values, values[1:])):
            raise ValueError('CDF bounds must be nondecreasing')
        self.size = len(self.lower) + 1
        self.A, self.b = [], []
        for j, (l, u) in enumerate(zip(self.lower, self.upper)):
            prefix = tuple(int(h <= j) for h in range(self.size))
            self.A.extend((prefix, tuple(-v for v in prefix)))
            self.b.extend((u, -l))
        # Choosing the lower CDF and putting its residual mass at the last
        # support point witnesses feasibility of these monotone bands.
        cdf = (F(0), *self.lower, F(1))
        self.feasible_witness = tuple(b-a for a, b in zip(cdf, cdf[1:]))
        assert self.feasible(self.feasible_witness)
        self.common_denominator = math.lcm(*(x.denominator for x in self.b))

    def feasible(self, p):
        return (len(p) == self.size and all(x >= 0 for x in p) and sum(p) == 1
                and all(sum(a*x for a, x in zip(row, p)) <= rhs
                        for row, rhs in zip(self.A, self.b)))

    def minimum(self, payoff):
        g = tuple(map(F, payoff))
        if len(g) != self.size:
            raise ValueError('One payoff is required for each threshold')
        start = time.perf_counter_ns()
        result = linprog(np.array(g, dtype=float), A_ub=np.array(self.A, dtype=float),
                         b_ub=np.array(self.b, dtype=float),
                         A_eq=np.ones((1, self.size)), b_eq=[1],
                         bounds=(0, None), method='highs')
        if not result.success:
            raise RuntimeError(result.message)
        proposal_ns = time.perf_counter_ns() - start
        check_start = time.perf_counter_ns()
        # Any nonpositive rational y gives a feasible exact dual after this
        # choice of nu. The guarantee does not trust floating-point residuals.
        y = tuple(min(F(0), F(float(v)).limit_denominator(1_000_000))
                  for v in result.ineqlin.marginals)
        nu = min(g[h] - sum(row[h]*yi for row, yi in zip(self.A, y))
                 for h in range(self.size))
        lower = sum(b*yi for b, yi in zip(self.b, y)) + nu
        assert all(yi <= 0 for yi in y)
        assert all(sum(row[h]*yi for row, yi in zip(self.A, y)) + nu <= g[h]
                   for h in range(self.size))
        # With rational CDF endpoints, a proposed vertex often reconstructs
        # on their common denominator. Only accept after exact feasibility.
        den = self.common_denominator
        primal = self.feasible_witness
        if den <= 10**9:
            empirical = [F(0)] + [F(round(den*sum(result.x[:j+1])), den)
                                   for j in range(self.size-1)] + [F(1)]
            candidate = tuple(b-a for a, b in zip(empirical, empirical[1:]))
            if self.feasible(candidate):
                primal = candidate
        primal_value = sum(gv*p for gv, p in zip(g, primal))
        assert lower <= primal_value
        exact_gap = primal_value - lower
        return dict(lower=str(lower), primal_value=str(primal_value),
                    exact_optimality=exact_gap == 0, exact_gap=str(exact_gap),
                    dual_y=list(map(str, y)), dual_nu=str(nu),
                    primal=list(map(str, primal)),
                    proposal_ns=proposal_ns, check_ns=time.perf_counter_ns()-check_start,
                    checked_dual_constraints=self.size, checked_primal_constraints=len(self.A))

    def interval(self, payoff):
        payoff = tuple(map(F, payoff))
        low = self.minimum(payoff)
        negative = self.minimum(tuple(-g for g in payoff))
        return dict(lower=low['lower'], upper=str(-F(negative['lower'])),
                    minimum_certificate=low, negative_minimum_certificate=negative)


def variance_budget(payoff):
    """Discrete total variation, not stochastic variance."""
    g = tuple(map(F, payoff))
    return sum(abs(a-b) for a, b in zip(g, g[1:]))


def main(destination):
    if destination.exists():
        raise FileExistsError('Preserve the recorded development result; choose a new path')
    here = Path(__file__).resolve().parent
    evidence = here/'threshold_cnf_results.json'
    raw = json.loads(evidence.read_text())
    assert raw['status'] == 'complete'
    query_definitions = {
        'original_pair_3_4': [int(3 < h <= 4) for h in range(9)],
        'later_pair_0_7': [int(0 < h <= 7) for h in range(9)],
        'two_interval_union': [int(0 < h <= 2 or 5 < h <= 7) for h in range(9)],
        'all_pair_disagreements': [h*(8-h) for h in range(9)],
        'lower_first_query_count': [2-int(h <= 3) for h in range(9)],
        'upper_first_query_count': [1+int(h <= 4) for h in range(9)],
        'paired_order_count_difference': [1-int(h <= 3)-int(h <= 4) for h in range(9)],
    }
    rows = []
    for arm in raw['arms']:
        for stage in arm['stages']:
            band = stage['cdf_band']['endpoints']
            lower = [band[str(k)]['lower'] for k in range(8)]
            upper = [band[str(k)]['upper'] for k in range(8)]
            source = CDFValues(lower, upper)
            outputs = {}
            for name, g in query_definitions.items():
                answer = source.interval(g)
                # The exact finite-source expansion is independently checked
                # at every possible H, not only at the observed samples.
                for h in range(9):
                    rebuilt = g[-1] + sum((g[j]-g[j+1])*int(h <= j) for j in range(8))
                    assert rebuilt == g[h]
                eps = F(stage['cdf_band']['radius'])
                partial = stage['draw_intervals']
                variation = variance_budget(g)
                tv_lower = max(F(min(g)), sum(F(min(g[l:u+1])) for l, u in partial)/len(partial)-eps*variation)
                tv_upper = min(F(max(g)), sum(F(max(g[l:u+1])) for l, u in partial)/len(partial)+eps*variation)
                # These are two separately valid consequences of the same
                # DKW event; intersect them without a new statistical charge.
                answer['partial_variation_interval'] = list(map(str, (tv_lower, tv_upper)))
                answer['intersection'] = [str(max(F(answer['lower']), tv_lower)),
                                          str(min(F(answer['upper']), tv_upper))]
                assert F(answer['intersection'][0]) <= F(answer['intersection'][1])
                outputs[name] = answer
            rows.append(dict(mode=arm['mode'], stage=stage['stage'],
                             source_acquisition_units=stage['invoice']['total_units'],
                             lower_cdf=lower, upper_cdf=upper, outputs=outputs))
    certificates = [a[k] for row in rows for a in row['outputs'].values()
                    for k in ('minimum_certificate','negative_minimum_certificate')]
    result = dict(status='DEVELOPMENT', contributor='ChatGPT (GPT-6 Astra Pro)',
                  generated_utc=datetime.now(timezone.utc).isoformat(), command=sys.argv,
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                           for p in [Path(__file__), evidence]},
                  environment=dict(python=platform.python_version(), scipy=scipy.__version__),
                  query_definitions=query_definitions, new_source_evaluations=0,
                  source_warrant='Inherited fixed-n rational outward DKW bands; selected-query coverage is conditional on the stated sampling law',
                  scope='Post-exposure query interface; exact LP dual/primal certificates. Query-count prices are illustrative complete unit tariffs, not actual solver bills. Acquisition invoices are inherited, not repaid or credited as zero cost.',
                  exact_certificates=len(certificates),
                  exact_optima=sum(c['exact_optimality'] for c in certificates),
                  lp_proposal_ns=sum(c['proposal_ns'] for c in certificates),
                  exact_check_ns=sum(c['check_ns'] for c in certificates), rows=rows)
    destination.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['exact_certificates','exact_optima',
                                           'new_source_evaluations','lp_proposal_ns','exact_check_ns']}))
    print(json.dumps([dict(mode=row['mode'], stage=row['stage'],
                     values={name:out['intersection'] for name,out in row['outputs'].items()})
                     for row in rows]))


if __name__ == '__main__':
    main(Path(sys.argv[1]))
