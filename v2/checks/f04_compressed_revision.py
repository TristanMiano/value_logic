"""Exact finite checks for F04 S3; not a general solver or empirical certificate.

All public numeric inputs here are integers or Fractions. Source/context validity
is an explicit premise: this fixture checks algebra, not empirical calibration.
Run with --json PATH to save the deterministic worked-example report.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
import sys
import unittest

from .f04_nonlinear_reflection import JointSelfModel


def exact(x: int | F) -> F:
    if isinstance(x, bool) or not isinstance(x, (int, F)):
        raise TypeError('Use finite exact integers/Fractions, not floats or booleans.')
    return F(x)


def probability(x: int | F) -> F:
    x = exact(x)
    if not 0 <= x <= 1:
        raise ValueError('Expected a probability in [0,1].')
    return x


def vector(xs) -> tuple[F, ...]:
    return tuple(exact(x) for x in xs)


def dot(xs, ys) -> F:
    xs, ys = vector(xs), vector(ys)
    if len(xs) != len(ys):
        raise ValueError('Vector dimensions differ.')
    return sum((a*b for a, b in zip(xs, ys)), F(0))


def positive(x: F) -> F:
    return max(exact(x), F(0))


def vertices(ps) -> tuple[tuple[F, F], ...]:
    rows = tuple(tuple(probability(x) for x in p) for p in ps)
    if not rows or any(len(p) != 2 for p in rows):
        raise ValueError('A nonempty finite family of probability pairs is required.')
    return rows


@dataclass(frozen=True)
class RateSummary:
    """Exact query summary for one supplied model family and cost convention."""
    floor: F
    least: F
    greatest: F
    scope: str

    def __post_init__(self):
        object.__setattr__(self, 'floor', probability(self.floor))
        object.__setattr__(self, 'least', exact(self.least))
        object.__setattr__(self, 'greatest', exact(self.greatest))
        if self.least > self.greatest or not self.scope:
            raise ValueError('Invalid slope order or empty scope.')

    @classmethod
    def from_vertices(cls, ps, k: int | F = 0, scope: str = 'example-v1'):
        ps, k = vertices(ps), exact(k)
        if k < 0:
            raise ValueError('Negative branch resource cost is outside this fixture.')
        floor = max([F(0), *[b/(1-a+b) for a, b in ps if 1-a+b > 0]])
        slopes = [a-b+k for a, b in ps]
        return cls(floor, min(slopes), max(slopes), scope)

    @property
    def signature(self) -> tuple[F, F, F]:
        return self.floor, positive(self.greatest), positive(-self.least)

    def check_scope(self, scope: str) -> None:
        if scope != self.scope:
            raise ValueError('Source/controller/cost context does not match.')

    def signed_change(self, old, new, *, scope: str) -> F:
        self.check_scope(scope)
        t = probability(new)-probability(old)
        return self.greatest*t if t >= 0 else self.least*t

    def deterioration(self, old, new, *, scope: str) -> F:
        return positive(self.signed_change(old, new, scope=scope))


def conservative_interval(floor_upper, c_plus, c_minus, old, budget,
                          *, accepted_baseline: bool) -> tuple[F, F]:
    """Uses an explicitly accepted same-context old-report validity premise.

    It does not itself prove that premise or the three upper-bound inputs.
    Tests check them separately against the original supplied models.
    """
    floor_upper, old = probability(floor_upper), probability(old)
    c_plus, c_minus, budget = map(exact, (c_plus, c_minus, budget))
    if not accepted_baseline or min(c_plus, c_minus, budget) < 0:
        raise ValueError('An accepted baseline and nonnegative rates/budget are required.')
    lower = min(floor_upper, old)
    upper = F(1)
    if c_minus:
        lower = max(lower, old-budget/c_minus)
    if c_plus:
        upper = min(upper, old+budget/c_plus)
    return lower, upper


def clip_segment(ps, normal, bound) -> tuple[tuple[F, F], ...]:
    """Exact halfspace intersection of a two-endpoint convex segment."""
    ps = vertices(ps)
    if len(ps) != 2:
        raise ValueError('This routine supports exactly two endpoints.')
    normal, bound = vector(normal), exact(bound)
    p, q = ps
    fp, fq = dot(normal, p)-bound, dot(normal, q)-bound
    if fp <= 0 and fq <= 0:
        return ps
    if fp > 0 and fq > 0:
        raise ValueError('The source intersection is empty.')
    t = fp/(fp-fq)
    cut = tuple(a+t*(b-a) for a, b in zip(p, q))
    return (p, cut) if fp <= 0 else (cut, q)


def support(points, direction) -> F:
    points, direction = tuple(vector(p) for p in points), vector(direction)
    if not points:
        raise ValueError('Support of an empty set is not admitted here.')
    return max(dot(p, direction) for p in points)


@dataclass(frozen=True)
class LinearFacts:
    """Outer possible-source inequalities, with a finite feasibility witness."""
    rows: tuple[tuple[F, ...], ...]
    upper: tuple[F, ...]
    feasible: tuple[F, ...]
    scope: str = 'linear-example-v1'

    def __post_init__(self):
        rows = tuple(vector(r) for r in self.rows)
        upper, feasible = vector(self.upper), vector(self.feasible)
        if (not rows or not feasible or len(rows) != len(upper)
                or any(len(r) != len(feasible) for r in rows) or not self.scope):
            raise ValueError('Invalid finite template dimensions or scope.')
        if any(dot(r, feasible) > b for r, b in zip(rows, upper)):
            raise ValueError('Supplied nonemptiness witness does not satisfy all facts.')
        object.__setattr__(self, 'rows', rows)
        object.__setattr__(self, 'upper', upper)
        object.__setattr__(self, 'feasible', feasible)

    def check(self, direction, ceiling, multipliers, *, scope: str) -> dict:
        if scope != self.scope:
            raise ValueError('Certificate scope mismatch.')
        v, lam, ceiling = vector(direction), vector(multipliers), exact(ceiling)
        if len(lam) != len(self.rows) or len(v) != len(self.feasible):
            raise ValueError('Certificate dimensions do not match the facts.')
        if any(x < 0 for x in lam):
            raise ValueError('Negative multipliers are not a valid inequality rule.')
        derived = tuple(sum((w*r[j] for w, r in zip(lam, self.rows)), F(0))
                        for j in range(len(v)))
        if derived != v:
            raise ValueError('Weighted premise directions do not equal the query.')
        bound = dot(lam, self.upper)
        if bound > ceiling:
            raise ValueError('The certificate bound exceeds the requested ceiling.')
        return {'direction': v, 'multipliers': lam, 'bound': bound,
                'ceiling': ceiling, 'margin': ceiling-bound, 'scope': scope}


KA = ((F(1,4), F(3,4)), (F(1,2), F(0)))
KB = ((F(1,4), F(3,4)), (F(3,4), F(1,4)))


def example_report() -> dict:
    a, b = RateSummary.from_vertices(KA), RateSummary.from_vertices(KB)
    a_cut = clip_segment(KA, (0, -1), -F(1,8))
    facts = LinearFacts(((1,1),(-1,0),(0,-1)), (F(9,10),0,0), (0,0))
    requests = [('old_self_report', (F(3,5),F(2,5)), F(3,5), (F(3,5),0,F(1,5))),
                ('new_self_report', (F(1,2),F(1,2)), F(1,2), (F(1,2),0,0)),
                ('paired_revision', (-F(1,10),F(1,10)), F(9,100), (F(1,10),F(1,5),0))]
    return {
        'scope': 'Finite supplied models and rational certificates; no trained model or full proof search.',
        'same_summary_different_optimizer': {
            'summary_A': a.signature, 'summary_B': b.signature,
            'optimum_A': JointSelfModel(KA).optimize(0),
            'optimum_B': JointSelfModel(KB).optimize(0)},
        'evidence_b_at_least_one_eighth': {
            'A_cut_vertices': a_cut,
            'A_paired_bound': RateSummary.from_vertices(a_cut).deterioration(F(1,2),F(3,4),scope='example-v1'),
            'B_paired_bound': b.deterioration(F(1,2),F(3,4),scope='example-v1'),
            'separating_allowance': F(1,10)},
        'approximate_guard': {
            'exact_interval': conservative_interval(F(2,5),F(3,5),F(2,5),F(3,5),F(3,50),accepted_baseline=True),
            'coarse_interval': conservative_interval(F(2,5),F(4,5),F(1,2),F(3,5),F(3,50),accepted_baseline=True)},
        'reflection_certificates': {name: facts.check(v,c,lam,scope=facts.scope)
                                    for name,v,c,lam in requests},
        'proxy_target_change': (-F(1,8), -F(3,40)),
        'exhaustive_boundaries': {'summary_models': 81, 'resource_weights': 3,
                                 'report_pairs_per_model_weight': 25,
                                 'total_paired_checks': 6075},
        'unrestricted_results': 'The cone, continuous-domain and derivative claims rely on the written proofs, not these finite samples.'}


def json_ready(obj):
    if isinstance(obj, F):
        return str(obj)
    if isinstance(obj, dict):
        return {str(k): json_ready(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [json_ready(v) for v in obj]
    return obj


class F04CompressedRevisionTests(unittest.TestCase):
    def test_exact_summary_on_6075_paired_queries(self):
        points = tuple(product((F(0),F(1,2),F(1)), repeat=2))
        reports = tuple(F(i,4) for i in range(5))
        count = 0
        for p,q in product(points, repeat=2):
            for k in (F(0),F(3,10),F(1)):
                s=RateSummary.from_vertices((p,q),k)
                for old,new in product(reports,repeat=2):
                    direct=max((a-b+k)*(new-old) for a,b in (p,q))
                    self.assertEqual(s.signed_change(old,new,scope=s.scope),direct)
                    self.assertEqual(s.deterioration(old,new,scope=s.scope),positive(direct))
                    self.assertEqual(new>=s.floor,all(a*new+b*(1-new)<=new for a,b in (p,q)))
                    count+=1
        self.assertEqual(count,6075)

    def test_directed_triangle(self):
        s=RateSummary.from_vertices(KA,F(3,10))
        for x,y,z in product((F(i,4) for i in range(5)),repeat=3):
            self.assertLessEqual(s.deterioration(x,z,scope=s.scope),
                s.deterioration(x,y,scope=s.scope)+s.deterioration(y,z,scope=s.scope))
        self.assertNotEqual(s.deterioration(0,1,scope=s.scope),s.deterioration(1,0,scope=s.scope))

    def test_summary_is_not_an_absolute_optimizer(self):
        self.assertEqual(RateSummary.from_vertices(KA).signature,RateSummary.from_vertices(KB).signature)
        self.assertEqual(JointSelfModel(KA).optimize(0),(F(3,4),F(3,8)))
        self.assertEqual(JointSelfModel(KB).optimize(0),(F(1,2),F(1,2)))

    def test_degenerate_probability_endpoints(self):
        self.assertEqual(RateSummary.from_vertices(((1,0),)).floor,0)
        a=RateSummary.from_vertices(((1,1),)); b=RateSummary.from_vertices(((1,F(1,2)),))
        self.assertEqual((a.floor,b.floor),(1,1))
        self.assertNotEqual(a.signature,b.signature)
        self.assertEqual(a.deterioration(1,1,scope=a.scope),b.deterioration(1,1,scope=b.scope))

    def test_summary_scope_and_exact_input_validation(self):
        s=RateSummary.from_vertices(KA)
        with self.assertRaises(ValueError):s.deterioration(0,1,scope='changed-cost')
        for invalid in (0.5,True,float('inf')):
            with self.assertRaises(TypeError):RateSummary.from_vertices(((invalid,0),))
        with self.assertRaises(ValueError):RateSummary.from_vertices(())
        with self.assertRaises(ValueError):RateSummary.from_vertices(((2,0),))
        with self.assertRaises(ValueError):RateSummary.from_vertices(KA,-1)

    def test_guard_keeps_a_certified_old_report(self):
        self.assertEqual(conservative_interval(F(9,10),F(1,2),F(1,2),F(1,2),0,
                                              accepted_baseline=True),(F(1,2),F(1,2)))
        self.assertGreater(F(9,10),F(1,2))  # Naive floor intersection would be empty.
        with self.assertRaises(ValueError):conservative_interval(1,1,1,F(1,2),0,accepted_baseline=False)

    def test_exact_and_coarse_intervals(self):
        ps=((F(4,25),F(14,25)),(F(7,10),F(1,10)))
        s=RateSummary.from_vertices(ps)
        self.assertEqual(s.floor,F(2,5))
        self.assertEqual(conservative_interval(s.floor,positive(s.greatest),positive(-s.least),F(3,5),F(3,50),
            accepted_baseline=True),(F(9,20),F(7,10)))
        coarse=conservative_interval(s.floor,F(4,5),F(1,2),F(3,5),F(3,50),accepted_baseline=True)
        self.assertEqual(coarse,(F(12,25),F(27,40)))
        for r in (coarse[0],F(3,5),coarse[1]):
            self.assertGreaterEqual(r,s.floor)
            self.assertLessEqual(s.deterioration(F(3,5),r,scope=s.scope),F(3,50))

    def test_zero_rate_directions_and_guard_negative_inputs(self):
        self.assertEqual(conservative_interval(0,0,0,F(1,2),0,accepted_baseline=True),(0,1))
        self.assertEqual(conservative_interval(0,0,1,F(1,2),0,accepted_baseline=True),(F(1,2),1))
        with self.assertRaises(ValueError):conservative_interval(0,-1,0,0,0,accepted_baseline=True)
        with self.assertRaises(ValueError):conservative_interval(0,1,1,0,-1,accepted_baseline=True)

    def test_convex_intersection_creates_a_new_endpoint(self):
        cut=clip_segment(KA,(0,-1),-F(1,8))
        self.assertEqual(cut,(KA[0],(F(11,24),F(1,8))))
        self.assertNotIn(cut[1],KA)
        self.assertEqual(clip_segment(KB,(0,-1),-F(1,8)),KB)
        with self.assertRaises(ValueError):clip_segment(KA,(0,-1),-1)

    def test_equal_summaries_cannot_update_exactly_for_general_evidence(self):
        a=RateSummary.from_vertices(clip_segment(KA,(0,-1),-F(1,8)))
        b=RateSummary.from_vertices(KB)
        self.assertEqual((a.floor,b.floor),(F(1,2),F(1,2)))
        da=a.deterioration(F(1,2),F(3,4),scope=a.scope)
        db=b.deterioration(F(1,2),F(3,4),scope=b.scope)
        self.assertEqual((da,db),(F(1,12),F(1,8)))
        self.assertLessEqual(da,F(1,10)); self.assertGreater(db,F(1,10))

    def test_slope_restriction_updates_rates_but_not_report_floor(self):
        a=RateSummary.from_vertices(clip_segment(KA,(-1,1),0))
        b=RateSummary.from_vertices(clip_segment(KB,(-1,1),0))
        self.assertEqual((a.least,a.greatest),(0,F(1,2)))
        self.assertEqual((a.least,a.greatest),(b.least,b.greatest))
        self.assertEqual((a.floor,b.floor),(F(3,8),F(1,2)))

    def test_source_restriction_preserves_old_upper_certificates(self):
        for ps in (KA,KB):
            original=RateSummary.from_vertices(ps)
            for bound in (F(1,8),F(1,4),F(1,2)):
                new=RateSummary.from_vertices(clip_segment(ps,(0,-1),-bound))
                self.assertTrue(all(n<=o for n,o in zip(new.signature,original.signature)))
        self.assertGreater(RateSummary.from_vertices((*KA,(1,1))).floor,RateSummary.from_vertices(KA).floor)

    def test_changed_resource_weight_requires_signed_information(self):
        kc=(KA[0],(F(1,10),F(1,2))); kd=(KA[0],(F(1,10),F(1,5)))
        self.assertEqual(RateSummary.from_vertices(kc).signature,RateSummary.from_vertices(kd).signature)
        a,b=(RateSummary.from_vertices(ps,F(3,10)) for ps in (kc,kd))
        self.assertEqual(a.signed_change(F(1,2),F(3,4),scope=a.scope),-F(1,40))
        self.assertEqual(b.signed_change(F(1,2),F(3,4),scope=b.scope),F(1,20))

    def test_end_to_end_reflective_certificates(self):
        certs=example_report()['reflection_certificates']
        self.assertEqual([certs[k]['bound'] for k in ('old_self_report','new_self_report','paired_revision')],
                         [F(27,50),F(9,20),F(9,100)])
        self.assertEqual(F(9,10)*(1-F(1,2))-F(9,10)*(1-F(3,5)),F(9,100))

    def test_template_enclosure_and_one_relational_repair(self):
        square=LinearFacts(((1,0),(-1,0),(0,1),(0,-1)),(1,1,1,1),(0,0))
        self.assertEqual(square.check((1,1),2,(1,0,1,0),scope=square.scope)['bound'],2)
        self.assertTrue(all(dot(r,(1,1))<=b for r,b in zip(square.rows,square.upper)))
        with self.assertRaises(ValueError):square.check((1,1),0,(1,0,1,0),scope=square.scope)
        repaired=LinearFacts((*square.rows,(1,1)),(*square.upper,0),(0,0))
        self.assertEqual(repaired.check((1,1),0,(0,0,0,0,1),scope=repaired.scope)['bound'],0)
        self.assertEqual(support(((1,-1),(-1,1)),(1,1)),0)

    def test_rejects_bad_certificate_rules_and_scope(self):
        f=LinearFacts(((1,0),(0,1)),(1,1),(0,0))
        for v,c,lam in [((1,1),0,(1,1)),((1,1),2,(1,-1)),((1,1),3,(1,)),((1,0),2,(1,1))]:
            with self.assertRaises(ValueError):f.check(v,c,lam,scope=f.scope)
        with self.assertRaises(ValueError):f.check((1,1),2,(1,1),scope='wrong')
        with self.assertRaises(TypeError):f.check((1,1),2,(1.0,1),scope=f.scope)

    def test_nonempty_enclosure_is_checked(self):
        with self.assertRaises(ValueError):LinearFacts(((1,),(-1,)),(0,-1),(0,))
        with self.assertRaises(ValueError):LinearFacts(((1,0),),(1,),(0,))
        f=LinearFacts(((1,),),(1,),(0,))
        with self.assertRaises(ValueError):f.check((0,),-1,(0,),scope=f.scope)

    def test_weighted_rule_sound_on_finite_feasible_points(self):
        f=LinearFacts(((1,0),(-1,0),(0,1),(0,-1)),(1,1,1,1),(0,0))
        pts=list(product((-1,0,1),repeat=2))
        for lam in product((0,1,2),repeat=4):
            v=tuple(sum(F(w)*row[j] for w,row in zip(lam,f.rows)) for j in range(2))
            bound=dot(lam,f.upper); f.check(v,bound,lam,scope=f.scope)
            for point in pts:self.assertLessEqual(dot(v,point),bound)

    def test_precision_error_uses_multipliers(self):
        certified=LinearFacts(((1,),),(F(99,100)+F(1,100),),(0,))
        self.assertEqual(certified.check((10,),10,(10,),scope=certified.scope)['bound'],10)
        with self.assertRaises(ValueError):certified.check((10,),F(99,10),(10,),scope=certified.scope)

    def test_quantitative_premise_change_can_preserve_certificate(self):
        f=LinearFacts(((1,1),),(F(1,20),),(0,0))
        c=f.check((1,1),F(1,10),(1,),scope=f.scope)
        self.assertEqual(c['margin'],F(1,20))
        with self.assertRaises(ValueError):LinearFacts(((1,1),),(F(1,5),),(0,0)).check((1,1),F(1,10),(1,),scope=f.scope)

    def test_retraction_can_be_repaired_by_an_alternate_certificate(self):
        f=LinearFacts(((1,0),(0,1)),(0,0),(0,0))
        self.assertEqual(f.check((1,1),0,(1,1),scope=f.scope)['bound'],0)

    def test_direction_drift_is_not_rounding_of_the_bound(self):
        eps=F(1,100); f=LinearFacts(((1,eps),),(0,),(0,0))
        self.assertEqual(dot((1,eps),(1,-100)),0)
        with self.assertRaises(ValueError):f.check((1,0),0,(1,),scope=f.scope)
        repaired=LinearFacts(((1,eps),(0,-1)),(0,3),(0,0))
        self.assertEqual(repaired.check((1,0),F(3,100),(1,eps),scope=f.scope)['bound'],F(3,100))

    def test_tube_split_improves_a_global_gradient_bound(self):
        value=lambda r:positive(exact(r)-F(1,2))
        change=value(F(3,4))-value(F(1,4))
        self.assertEqual(change,F(1,4))
        self.assertGreater(change,0)  # Current-region derivative alone misses it.
        self.assertLessEqual(change,support(((0,),(1,)),(F(1,2),)))
        self.assertEqual(change,0*F(1,4)+1*F(1,4))

    def test_template_pairing_survives_positive_rescaling_and_permutation(self):
        G=((F(1),F(-1)),(F(-1),F(1))); scales=(F(2),F(3)); perm=(1,0)
        Gp=tuple(tuple(g[perm[i]]/scales[i] for i in range(2)) for g in G)
        for v in product((-2,0,3),repeat=2):
            vp=tuple(scales[i]*v[perm[i]] for i in range(2))
            self.assertEqual(support(G,v),support(Gp,vp))

    def test_proxy_error_changes_need_no_absolute_bound(self):
        differences=[]
        for z,t in product((0,1,10**50),(-F(1,10),0,F(1,10))):
            L=lambda r:1+z-F(2,5)*r
            J=lambda r:L(r)+z+t*r
            old,new=F(1,2),F(3,4); difference=J(new)-J(old)
            self.assertGreaterEqual(J(1),0)
            self.assertLessEqual(difference,-F(3,40));self.assertGreaterEqual(difference,-F(1,8))
            differences.append(difference)
        self.assertEqual((min(differences),max(differences)),(-F(1,8),-F(3,40)))

    def test_changing_context_requires_a_drift_term(self):
        ps=[F(1,2),F(3,4),F(2,3)]
        lines=[(F(0),F(1)),(F(2),F(-1)),(F(3),F(2))]
        j=lambda t,p:lines[t][0]+lines[t][1]*p
        policy=sum((j(t,ps[t])-j(t,ps[t-1]) for t in (1,2)),F(0))
        drift=sum((j(t,ps[t-1])-j(t-1,ps[t-1]) for t in (1,2)),F(0))
        self.assertEqual(j(2,ps[2])-j(0,ps[0]),policy+drift)
        self.assertNotEqual(policy,policy+drift)

    def test_report_is_deterministic_and_explicitly_scoped(self):
        self.assertEqual(json_ready(example_report()),json_ready(example_report()))
        self.assertEqual(example_report()['exhaustive_boundaries']['total_paired_checks'],6075)


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json',type=Path)
    args=parser.parse_args()
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(F04CompressedRevisionTests))
    if not result.wasSuccessful():return 1
    if args.json:
        args.json.parent.mkdir(parents=True,exist_ok=True)
        args.json.write_text(json.dumps(json_ready(example_report()),indent=2,sort_keys=True)+'\n',encoding='utf-8')
    return 0


if __name__=='__main__':
    sys.exit(main())
