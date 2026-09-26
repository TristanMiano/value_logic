"""Finite F04 S4 checks; not a general prover or empirical evidence procedure.

Linear algebra uses exact rational values. Decimal log/exp calculations are
separately labelled numerical illustrations and are not proof certificates.
"""
from __future__ import annotations

import argparse
from decimal import Decimal, localcontext
from fractions import Fraction as F
from itertools import combinations, product
import json
from math import comb, isqrt
from pathlib import Path
import sys
import unittest

from .f04_compressed_revision import LinearFacts, dot, exact, vector, json_ready


def unique_solution(columns, target):
    """Solve an independent-column system exactly; None means dependent/inconsistent."""
    cols, target = tuple(vector(c) for c in columns), vector(target)
    d, k = len(target), len(cols)
    if not k:
        return () if all(x == 0 for x in target) else None
    if k > d or any(len(c) != d for c in cols):
        return None
    aug = [[cols[j][i] for j in range(k)] + [target[i]] for i in range(d)]
    for j in range(k):
        pivot = next((i for i in range(j, d) if aug[i][j]), None)
        if pivot is None:
            return None
        aug[j], aug[pivot] = aug[pivot], aug[j]
        scale = aug[j][j]
        aug[j] = [x / scale for x in aug[j]]
        for i in range(d):
            if i != j:
                factor = aug[i][j]
                aug[i] = [a - factor*b for a, b in zip(aug[i], aug[j])]
    if any(all(x == 0 for x in row[:k]) and row[k] != 0 for row in aug):
        return None
    return tuple(aug[i][k] for i in range(k))


def basic_certificates(rows, query, max_subsets=20000):
    """Small-fixture enumeration of independent supports, not a preferred LP solver."""
    rows, query = tuple(vector(r) for r in rows), vector(query)
    if not rows or not query or any(len(r) != len(query) for r in rows):
        raise ValueError('Nonempty consistent dimensions are required.')
    if type(max_subsets) is not int or max_subsets <= 0:
        raise ValueError('Invalid enumeration limit.')
    if sum(comb(len(rows), k) for k in range(min(len(rows), len(query))+1)) > max_subsets:
        raise ValueError('Fixture enumeration budget exceeded.')
    found = set()
    for k in range(min(len(rows), len(query))+1):
        for inds in combinations(range(len(rows)), k):
            sol = unique_solution([rows[i] for i in inds], query)
            if sol is None or any(x < 0 for x in sol):
                continue
            lam = [F(0)]*len(rows)
            for i, x in zip(inds, sol):
                lam[i] = x
            found.add(tuple(lam))
    return tuple(sorted(found))


def portfolio_bound(facts: LinearFacts, query, certificates, *, scope):
    certs = tuple(vector(c) for c in certificates)
    if not certs:
        raise ValueError('No certificate provided; empty minimum is not zero evidence.')
    checks = [facts.check(query, dot(c, facts.upper), c, scope=scope) for c in certs]
    i = min(range(len(checks)), key=lambda j: (checks[j]['bound'], j))
    return checks[i]['bound'], certs[i]


def case_certificate(modes, certificates, query, ceiling, *, scope):
    if not modes or set(modes) != set(certificates):
        raise ValueError('Every declared possible mode must be covered exactly.')
    out = {}
    for name in sorted(modes):
        out[name] = modes[name].check(query, ceiling, certificates[name], scope=scope)
    return out


def common_bound(modes, certificate, query, *, scope):
    if not modes:
        raise ValueError('Empty mode family.')
    values = []
    rows = next(iter(modes.values())).rows
    for facts in modes.values():
        if facts.rows != rows:
            raise ValueError('A common coefficient vector needs common template rows.')
        value = dot(certificate, facts.upper)
        facts.check(query, value, certificate, scope=scope)
        values.append(value)
    return max(values)


def duplicate_rows(d):
    if type(d) is not int or not 1 <= d <= 12:
        raise ValueError('Small positive fixture dimension required.')
    return tuple(tuple(F(int(i == j)) for j in range(d)) for i in range(d) for _ in range(2))


def factored_pair_bound(upper):
    upper = vector(upper)
    if not upper or len(upper) % 2:
        raise ValueError('Expected a nonempty list of bound pairs.')
    lam = [F(0)]*len(upper)
    for i in range(0, len(upper), 2):
        j = i if upper[i] <= upper[i+1] else i+1
        lam[j] = F(1)
    return dot(lam, upper), tuple(lam)


def relu_affine_piece(weights, biases, output, offset, x, *, zero_rule="lexicographic"):
    """Exact one-sided affine fingerprint; optional inactive mask is a negative control."""
    if zero_rule not in ("lexicographic", "inactive"):
        raise ValueError("Unknown zero-mask convention.")
    x, biases, output, offset = vector(x), vector(biases), vector(output), exact(offset)
    weights = tuple(vector(w) for w in weights)
    if (not x or not weights or len(weights) != len(biases) or len(weights) != len(output)
            or any(len(w) != len(x) for w in weights)):
        raise ValueError('Network dimensions do not match.')
    lam, intercept, value = [F(0)]*len(x), offset, offset
    for w, b, a in zip(weights, biases, output):
        z = dot(w, x)+b
        value += a*max(z, F(0))
        leading = next((t for t in w if t), F(0))
        active = z > 0 or (z == 0 and zero_rule == "lexicographic" and leading > 0)
        if active:
            intercept += a*b
            lam = [u+a*t for u, t in zip(lam, w)]
    assert value == dot(lam, x)+intercept
    return value, tuple(lam), intercept


def checked_neural_piece(facts, query, network, *, scope):
    value, lam, intercept = relu_affine_piece(*network, facts.upper)
    if intercept < 0:
        raise ValueError('Negative intercept: not certified by this sufficient method.')
    record = facts.check(query, value, lam, scope=scope)
    record['intercept'] = intercept
    return record


def min_pair_network(d, offset=0):
    weights, outputs = [], []
    for i in range(d):
        x, nx, diff = [0]*(2*d), [0]*(2*d), [0]*(2*d)
        x[2*i], nx[2*i] = 1, -1
        diff[2*i], diff[2*i+1] = 1, -1
        weights.extend([x, nx, diff]); outputs.extend([1, -1, -1])
    return weights, [0]*len(weights), outputs, offset


def cover_modes(universe, sets):
    universe, sets = frozenset(universe), tuple(frozenset(s) for s in sets)
    if not universe or not sets or any(not s <= universe for s in sets):
        raise ValueError('Invalid finite cover data.')
    if frozenset().union(*sets) != universe:
        raise ValueError('Possible modes lack coverage.')
    return {str(k): LinearFacts(tuple((1,) for _ in sets),
                               tuple(0 if k in s else 1 for s in sets), (0,), 'cover-v1')
            for k in sorted(universe)}


def minimum_cover(universe, sets):
    u, sets = frozenset(universe), tuple(frozenset(s) for s in sets)
    if len(sets) > 16:
        raise ValueError('This exact fixture search is deliberately bounded.')
    cover_modes(u, sets)
    for k in range(len(sets)+1):
        for inds in combinations(range(len(sets)), k):
            if frozenset().union(*(sets[i] for i in inds)) == u:
                return inds
    raise AssertionError('Previously validated coverage was lost.')


def greedy_cover(universe, sets):
    cover_modes(universe, sets)
    remaining, chosen = set(universe), []
    while remaining:
        i = max(range(len(sets)), key=lambda j: (len(remaining & set(sets[j])), -j))
        chosen.append(i); remaining -= set(sets[i])
    return tuple(chosen)


def shortest_path_bound(n, edges, start, target):
    """Finite exact difference-constraint fixture. Raises on any negative cycle."""
    if type(n) is not int or not 1 <= n <= 100:
        raise ValueError('Invalid finite vertex count.')
    if any(type(i) is not int or not 0 <= i < n for i in (start, target)):
        raise ValueError('Invalid query vertices.')
    es = []
    for i, j, w in edges:
        if any(type(k) is not int or not 0 <= k < n for k in (i, j)):
            raise ValueError('Invalid edge vertex.')
        es.append((i,j,exact(w)))
    if len(es) > 2000:
        raise ValueError('Fixture edge limit exceeded.')
    # Super-source distances detect inconsistency anywhere, not only at start.
    pot = [F(0)]*n
    for round_ in range(n):
        changed = False
        for i,j,w in es:
            if pot[j] > pot[i]+w:
                pot[j] = pot[i]+w; changed = True
        if not changed:
            break
        if round_ == n-1:
            raise ValueError('Negative cycle: inconsistent source inequalities.')
    best = [None]*n; best[start] = (F(0), ())
    for _ in range(n-1):
        new = list(best)
        for k,(i,j,w) in enumerate(es):
            if best[i] is not None:
                cand = (best[i][0]+w, best[i][1]+(k,))
                if new[j] is None or (cand[0],len(cand[1]),cand[1]) < (new[j][0],len(new[j][1]),new[j][1]):
                    new[j] = cand
        best = new
    return best[target], tuple(pot)


def norm_ceiling(v, bits=16):
    """Rational outward-rounded Euclidean norm, with no floating-point square root."""
    v = vector(v)
    if not v or type(bits) is not int or not 0 <= bits <= 256:
        raise ValueError('Invalid norm input/precision.')
    q = dot(v, v)
    scaled_num = q.numerator << (2*bits)
    k = isqrt(scaled_num//q.denominator)
    if k*k*q.denominator < scaled_num:
        k += 1
    return F(k, 1 << bits)


def smooth_bound(values, tau=1, prior=None):
    """70-digit numerical illustration only; not a certified log/exp interval."""
    values, tau = vector(values), exact(tau)
    if not values or tau <= 0:
        raise ValueError('Nonempty finite values and positive temperature required.')
    prior = tuple(F(1,len(values)) for _ in values) if prior is None else vector(prior)
    if len(prior) != len(values) or min(prior) <= 0 or sum(prior) != 1:
        raise ValueError('A strictly positive normalized prior is required.')
    with localcontext() as ctx:
        ctx.prec = 70
        cvt = lambda a: Decimal(a.numerator)/Decimal(a.denominator)
        xs, t = [cvt(x) for x in values], cvt(tau)
        lo = min(xs)
        terms = [cvt(p)*(-(x-lo)/t).exp() for p,x in zip(prior,xs)]
        z = sum(terms); w = [a/z for a in terms]
        return lo-t*z.ln(), tuple(w)


def reflective_modes():
    rows = ((1,0),(-1,0),(0,1),(0,-1),(F(3,4),F(1,4)),
            (F(19,20),F(1,20)),(1,-1),(1,-1))
    common = (1,0,1,0,F(3,4),F(19,20))
    return {name: LinearFacts(rows, common+end, (0,F(1,2)), 'self-mix-S4')
            for name,end in [('A',(-F(1,2),F(1,4))), ('B',(F(1,4),-F(1,2)))]}


def example_report():
    modes = reflective_modes()
    branch = {'A': (0,0,0,0,0,0,1,0), 'B':(0,0,0,0,0,0,0,1)}
    common = (0,0,0,0,0,0,F(1,2),F(1,2))
    case_certificate(modes, branch, (1,-1), -F(1,2), scope='self-mix-S4')
    rows = ((1,0),(-1,0),(0,1),(0,-1),(F(3,5),F(4,5)),(F(4,5),F(3,5)))
    disk_poly = LinearFacts(rows,(1,)*6,(0,0),'disk-tangent')
    direction = (F(1,10),F(1,10))
    poly_bound, lam = portfolio_bound(disk_poly,direction,basic_certificates(rows,direction),scope='disk-tangent')
    smooth, _ = smooth_bound((1,1))
    with localcontext() as ctx:
        ctx.prec = 70
        raw = Decimal(1)-Decimal(2).ln()
    return {
        'scope':'F04 S4 finite examples; no trained network, global neural verifier, or full proof search.',
        'sparse_precision':{'epsilon':'1/16','tau':'1/64','multipliers':['8','8'],
                            'sharp_relaxed_bound':'1/4','with_extra_certified_row':'1/8'},
        'adaptive_marginal_failure':{'rows':3,'marginal_error':'1/10','selected_error':1-F(9,10)**3},
        'flat_portfolio_vs_factored':{'dimension':6,'necessary_flat_entries':64,'selected_rows':6,
                                     'explicit_relu_units_signed':18},
        'mode_geometry':{'case_bound':-F(1,2),'common_bound':common_bound(modes,common,(1,-1),scope='self-mix-S4'),
                         'rowwise_bound':F(1,4),'fixed_reports':(F(3,4),F(19,20))},
        'cover_example':{'minimum_indices':minimum_cover(range(1,7),({1,2,3,4},{1,2,5},{3,4,6})),
                         'greedy_indices':greedy_cover(range(1,7),({1,2,3,4},{1,2,5},{3,4,6}))},
        'path_revision':{str(shift):shortest_path_bound(3,((0,1,2+shift),(1,2,-3),(0,2,0)),0,2)[0][0]
                         for shift in (F(0),F(1,2),F(2))},
        'curved_source':{'coordinate_bound':F(1,5),'tangent_bound':poly_bound,
                          'tangent_certificate':lam,'accepted_tolerance':F(3,20),
                          'squared_query_norm':dot(direction,direction),
                          'rational_norm_upper_16_bits':norm_ceiling(direction)},
        'smoothing_numerical_only':{'duplicate_one_normalized':str(smooth),
                                    'duplicate_one_unnormalized':str(raw),
                                    'decimal_precision':70},
        'proof_status':'Unrestricted conclusions rely on the written derivations, not finite enumeration.'}


class F04CertificatePortfolioTests(unittest.TestCase):
    def test_independent_solver(self):
        self.assertEqual(unique_solution(((1,0),(0,1)),(2,3)),(2,3))
        self.assertIsNone(unique_solution(((1,1),(2,2)),(1,1)))
        self.assertIsNone(unique_solution(((1,0),),(1,1)))

    def test_sparse_zero_and_outside_cone(self):
        self.assertEqual(basic_certificates(((1,0),(1,0)),(0,0)),((0,0),))
        self.assertEqual(basic_certificates(((1,0),(1,0)),(0,1)),())

    def test_exact_sparse_library_box_queries(self):
        rows=((1,0),(-1,0),(0,1),(0,-1))
        for a,b,x,y in product(range(1,4),range(1,4),range(-2,3),range(-2,3)):
            facts=LinearFacts(rows,(a,a,b,b),(0,0),'box')
            certs=basic_certificates(rows,(x,y))
            bound,lam=portfolio_bound(facts,(x,y),certs,scope='box')
            self.assertEqual(bound,a*abs(x)+b*abs(y))
            self.assertLessEqual(sum(z>0 for z in lam),2)

    def test_enumeration_budget_and_numeric_guards(self):
        with self.assertRaises(ValueError): basic_certificates(((1,0),)*20,(1,0),max_subsets=2)
        with self.assertRaises(TypeError): basic_certificates(((1.0,),),(1,))
        with self.assertRaises(ValueError): basic_certificates(((1,2),),(1,))

    def test_precision_amplification_is_sharp(self):
        for k in range(1,10):
            eps,tau=F(1,2**k),F(1,64)
            facts=LinearFacts(((1,eps),(-1,eps)),(tau,tau),(0,tau/eps),'precision')
            lam=(1/(2*eps),)*2
            self.assertEqual(facts.check((0,1),tau/eps,lam,scope='precision')['bound'],tau/eps)

    def test_scaled_uncertainty_cost_invariant(self):
        facts=LinearFacts(((2,F(1,8)),(-F(1,4),F(1,64))),
                          (F(1,32),F(1,256)),(0,F(1,4)),'scaled')
        self.assertEqual(facts.check((0,1),F(1,4),(4,32),scope='scaled')['bound'],F(1,4))

    def test_better_alternative_after_precision_change(self):
        rows=((1,F(1,16)),(-1,F(1,16)),(0,1))
        facts=LinearFacts(rows,(F(1,64),F(1,64),F(1,8)),(0,F(1,8)),'extra')
        bound,lam=portfolio_bound(facts,(0,1),basic_certificates(rows,(0,1)),scope='extra')
        self.assertEqual((bound,lam),(F(1,8),(0,0,1)))

    def test_one_row_adaptive_selection_failure_probability(self):
        alpha=F(1,10); total=F(0)
        for bits in product((0,1),repeat=3):
            p=F(1)
            for b in bits: p*=alpha if b else 1-alpha
            if any(bits): total+=p
        self.assertEqual(total,F(271,1000))
        self.assertGreater(total,alpha)

    def test_flat_library_needs_every_binary_setting(self):
        for d in range(1,7):
            unique=set()
            for bits in product((0,1),repeat=d):
                rhs=tuple(F(int(j!=bit)) for bit in bits for j in (0,1))
                val,lam=factored_pair_bound(rhs)
                self.assertEqual(val,0); unique.add(lam)
                self.assertEqual(sum(z>0 for z in lam),d)
            self.assertEqual(len(unique),2**d)

    def test_factored_min_equals_flat_enumeration(self):
        rows=duplicate_rows(3); certs=basic_certificates(rows,(1,1,1))
        self.assertEqual(len(certs),8)
        for rhs in product((-1,0,2),repeat=6):
            pt=tuple(min(rhs[2*i:2*i+2]) for i in range(3))
            facts=LinearFacts(rows,rhs,pt,'dup')
            self.assertEqual(portfolio_bound(facts,(1,1,1),certs,scope='dup')[0],factored_pair_bound(rhs)[0])

    def test_factored_relu_affine_certificate(self):
        rows=duplicate_rows(2)
        for rhs in product((-2,0,3),repeat=4):
            facts=LinearFacts(rows,rhs,(min(rhs[:2]),min(rhs[2:])),'relu')
            record=checked_neural_piece(facts,(1,1),min_pair_network(2),scope='relu')
            self.assertEqual(record['bound'],factored_pair_bound(rhs)[0])
            self.assertEqual(record['intercept'],0)

    def test_inactive_zero_mask_is_not_a_genuine_gradient(self):
        facts=LinearFacts(((1,),(1,)),(0,-2),(-2,),"zero-mask")
        val,lam,c=relu_affine_piece(*min_pair_network(1),facts.upper,zero_rule="inactive")
        self.assertEqual((val,lam,c),(-2,(-1,1),0))
        with self.assertRaises(ValueError): facts.check((1,),val,lam,scope="zero-mask")
        record=checked_neural_piece(facts,(1,),min_pair_network(1),scope="zero-mask")
        self.assertEqual(record["multipliers"],(0,1))
        self.assertEqual(record["bound"],-2)

    def test_wrong_neural_intercept_is_rejected(self):
        facts=LinearFacts(duplicate_rows(1),(1,2),(0,),'bad')
        with self.assertRaises(ValueError): checked_neural_piece(facts,(1,),min_pair_network(1,-1),scope='bad')

    def test_max_network_is_sound_not_minimal(self):
        # x + ReLU(y-x), including signed x carried by two ReLU units.
        network=(((1,0),(-1,0),(-1,1)),(0,0,0),(1,-1,1),0)
        facts=LinearFacts(((1,),(1,)),(1,3),(0,),'max')
        record=checked_neural_piece(facts,(1,),network,scope='max')
        self.assertEqual(record['bound'],3)
        self.assertGreater(record['bound'],min(facts.upper))

    def test_neural_wrong_query_scope_and_negative_weight(self):
        facts=LinearFacts(((1,),(1,)),(1,2),(0,),'scope-A')
        with self.assertRaises(ValueError): checked_neural_piece(facts,(1,),min_pair_network(1),scope='scope-B')
        with self.assertRaises(ValueError): facts.check((1,),5,(-1,2),scope='scope-A')
        with self.assertRaises(ValueError): facts.check((2,),5,(1,0),scope='scope-A')

    def test_empty_portfolio_and_infeasibility_are_not_evidence(self):
        facts=LinearFacts(((1,),),(1,),(0,))
        with self.assertRaises(ValueError): portfolio_bound(facts,(1,),(),scope=facts.scope)
        with self.assertRaises(ValueError): LinearFacts(((1,),(-1,)),(0,-1),(0,))

    def test_mode_proofs_same_query_and_missing_case(self):
        modes=reflective_modes()
        cs={'A':(0,0,0,0,0,0,1,0),'B':(0,0,0,0,0,0,0,1)}
        self.assertEqual(len(case_certificate(modes,cs,(1,-1),-F(1,2),scope='self-mix-S4')),2)
        with self.assertRaises(ValueError): case_certificate(modes,{'A':cs['A']},(1,-1),0,scope='self-mix-S4')
        with self.assertRaises(ValueError): case_certificate(modes,dict.fromkeys(modes,cs['A']),(1,-1),-F(1,2),scope='self-mix-S4')

    def test_reflective_three_level_gap(self):
        modes=reflective_modes(); q=(1,-1)
        lam=(0,0,0,0,0,0,F(1,2),F(1,2))
        self.assertEqual(common_bound(modes,lam,q,scope='self-mix-S4'),-F(1,8))
        rows=modes['A'].rows
        for upper,pt,value in [
            (tuple((a+b)/2 for a,b in zip(modes['A'].upper,modes['B'].upper)),(0,F(1,8)),-F(1,8)),
            (tuple(max(a,b) for a,b in zip(modes['A'].upper,modes['B'].upper)),(F(1,4),0),F(1,4))]:
            facts=LinearFacts(rows,upper,pt,'relaxation')
            self.assertEqual(dot(pt,q),value)
            self.assertEqual(portfolio_bound(facts,q,basic_certificates(rows,q),scope='relaxation')[0],value)

    def test_reflective_policy_cost_identity(self):
        r0,r1=F(3,4),F(19,20)
        for a,b,z in product((F(0),F(1,4),F(1,2)),(F(1,2),F(3,4),F(1)),(0,10**30)):
            if a-b > -F(1,2): continue
            h=lambda r:a*r+b*(1-r)
            self.assertLessEqual(h(r0),r0); self.assertLessEqual(h(r1),r1)
            self.assertEqual((5*h(r1)+z)-(5*h(r0)+z),a-b)

    def test_cover_optimum_and_greedy_gap(self):
        sets=({1,2,3,4},{1,2,5},{3,4,6}); u=range(1,7)
        self.assertEqual(minimum_cover(u,sets),(1,2))
        self.assertEqual(greedy_cover(u,sets),(0,1,2))
        self.assertEqual(common_bound(cover_modes(u,sets),(0,F(1,2),F(1,2)),(1,),scope='cover-v1'),F(1,2))

    def test_cover_mixture_is_intersection(self):
        sets=({1,2,3,4},{1,2,5},{3,4,6}); modes=cover_modes(range(1,7),sets)
        for lam in ((F(1,2),F(1,2),0),(0,F(1,2),F(1,2)),(1,0,0)):
            covered={int(k) for k,facts in modes.items() if dot(lam,facts.upper)==0}
            expected=set(range(1,7))
            for w,s in zip(lam,sets):
                if w: expected &= s
            self.assertEqual(covered,expected)

    def test_cover_guards(self):
        with self.assertRaises(ValueError): cover_modes({1,2},({1},))
        with self.assertRaises(ValueError): cover_modes({1},({1,2},))

    def test_graph_improvement_and_revision(self):
        for delta,expected in ((0,-1),(F(1,2),-F(1,2)),(2,0)):
            edges=((0,1,2+delta),(1,2,-3),(0,2,0))
            best,pot=shortest_path_bound(3,edges,0,2)
            self.assertEqual(best[0],expected)
            self.assertEqual(sum(edges[i][2] for i in best[1]),expected)
            self.assertLessEqual(len(best[1]),2)
            for i,j,w in edges: self.assertLessEqual(pot[j]-pot[i],w)

    def test_graph_unreachable_identity_and_negative_cycles(self):
        self.assertIsNone(shortest_path_bound(3,((0,1,2),),0,2)[0])
        self.assertEqual(shortest_path_bound(2,(),0,0)[0],(0,()))
        with self.assertRaises(ValueError): shortest_path_bound(3,((1,2,-1),(2,1,0)),0,0)
        with self.assertRaises(ValueError): shortest_path_bound(2,((0,2,0),),0,1)

    def test_graph_matches_simple_path_enumeration(self):
        edges_structure=((0,1),(1,2),(0,2),(2,3),(1,3),(0,3))
        paths=((5,),(0,4),(2,3),(0,1,3))
        for ws in product((-1,1,2),repeat=6):
            es=tuple((i,j,w) for (i,j),w in zip(edges_structure,ws))
            best,_=shortest_path_bound(4,es,0,3)
            self.assertEqual(best[0],min(sum(ws[k] for k in path) for path in paths))

    def test_circle_relational_certificate(self):
        rows=((1,0),(-1,0),(0,1),(0,-1),(F(3,5),F(4,5)),(F(4,5),F(3,5)))
        facts=LinearFacts(rows,(1,)*6,(F(5,7),F(5,7)),'disk')
        q=(F(1,10),)*2; lam=(0,0,0,0,F(1,14),F(1,14))
        self.assertEqual(facts.check(q,F(3,20),lam,scope='disk')['bound'],F(1,7))
        self.assertEqual(dot(q,facts.feasible),F(1,7))
        self.assertLessEqual(dot(q,q),F(3,20)**2)

    def test_quadratic_identity_exact(self):
        for a,b,x,y in product(range(-2,3),repeat=4):
            self.assertEqual((a*x+b*y)**2+(a*y-b*x)**2,(a*a+b*b)*(x*x+y*y))

    def test_norm_ceiling_is_outward_and_close(self):
        for a,b,bits in product(range(-5,6),range(-5,6),(0,2,8,20)):
            q=(F(a,7),F(b,7)); upper=norm_ceiling(q,bits)
            self.assertGreaterEqual(upper**2,dot(q,q))
            lower=upper-F(1,1<<bits)
            if lower>=0: self.assertLess(lower**2,dot(q,q))
        with self.assertRaises(ValueError): norm_ceiling((1,1),-1)

    def test_structural_hypotheses_counterexamples(self):
        facts=LinearFacts(((1,),(0,)),(1,1),(1,),'negative')
        self.assertLess(facts.upper[0]-facts.upper[1],facts.feasible[0])
        with self.assertRaises(ValueError): facts.check((1,),0,(1,-1),scope='negative')
        self.assertLess(0,1)  # constant-zero predictor versus feasible target one

    def test_smooth_duplicate_is_not_new_evidence(self):
        val,weights=smooth_bound((1,1))
        self.assertEqual(val,1); self.assertEqual(weights,(Decimal('.5'),)*2)
        with localcontext() as ctx:
            ctx.prec=70; raw=Decimal(1)-Decimal(2).ln()
            self.assertGreater(raw,0); self.assertLess(raw,1)

    def test_normalized_smoothing_bounds_and_temperature(self):
        last=Decimal('-Infinity')
        for tau in (F(1,10),F(1,2),F(1),F(2),F(10)):
            val,w=smooth_bound((0,2),tau)
            self.assertGreaterEqual(val,0); self.assertLessEqual(val,1)
            self.assertGreaterEqual(val,last); last=val
            with localcontext() as ctx:
                ctx.prec=65
                average=2*w[1]
                self.assertLessEqual(average,val+Decimal('1e-60'))
                self.assertAlmostEqual(sum(w),Decimal(1),places=60)

    def test_smooth_prior_split_and_units(self):
        a,_=smooth_bound((0,2),prior=(F(1,3),F(2,3)))
        b,_=smooth_bound((0,0,2),prior=(F(1,6),F(1,6),F(2,3)))
        c,_=smooth_bound((0,6),tau=3,prior=(F(1,3),F(2,3)))
        self.assertAlmostEqual(a,b,places=60)
        with localcontext() as ctx:
            ctx.prec=65; self.assertAlmostEqual(c,3*a,places=60)

    def test_smooth_invalid_inputs(self):
        for kwargs in ({'values':()}, {'values':(0,1),'tau':0},
                       {'values':(0,1),'prior':(1,1)}, {'values':(0,1),'prior':(0,1)}):
            with self.assertRaises(ValueError): smooth_bound(**kwargs)

    def test_report_generates_without_claiming_proof_search(self):
        r=example_report()
        self.assertEqual(r['mode_geometry']['common_bound'],-F(1,8))
        self.assertEqual(r['curved_source']['tangent_bound'],F(1,7))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json',type=Path)
    args=parser.parse_args()
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(F04CertificatePortfolioTests)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful(): return 1
    if args.json:
        args.json.parent.mkdir(parents=True,exist_ok=True)
        args.json.write_text(json.dumps(json_ready(example_report()),indent=2,sort_keys=True)+'\n',encoding='utf-8')
    return 0


if __name__=='__main__':
    sys.exit(main())
