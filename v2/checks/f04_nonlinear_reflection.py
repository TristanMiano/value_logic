"""Exact finite F04 fixtures: nonlinear source bounds and common-policy reflection.

These tests are development evidence, not a full RLL verifier or trained model.
General statements are proved in 01a_nonlinear_and_reflective_reconstruction.md.
Run: python -m v2.checks.f04_nonlinear_reflection --json path/to/report.json
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product, combinations_with_replacement
import json
from pathlib import Path
import unittest
from typing import Iterable, Optional

from v2.checks.f04_countermodels import q, vec, dot, probability


def relu(x: F) -> F:
    return max(x, F(0))


@dataclass(frozen=True)
class Layer:
    weights: tuple[tuple[F, ...], ...]
    biases: tuple[F, ...]

    def __post_init__(self) -> None:
        rows = tuple(vec(row) for row in self.weights)
        biases = vec(self.biases)
        if not rows or not rows[0] or len(rows) != len(biases):
            raise ValueError('A layer needs a nonempty matrix and one bias per row.')
        if any(len(row) != len(rows[0]) for row in rows):
            raise ValueError('Ragged layer matrix.')
        object.__setattr__(self, 'weights', rows)
        object.__setattr__(self, 'biases', biases)


@dataclass(frozen=True)
class ReLUNetwork:
    input_dim: int
    layers: tuple[Layer, ...]
    output: tuple[F, ...]
    offset: F = F(0)

    def __post_init__(self) -> None:
        if isinstance(self.input_dim, bool) or not isinstance(self.input_dim, int) or self.input_dim < 1:
            raise ValueError('input_dim must be a positive integer.')
        layers = tuple(self.layers)
        width = self.input_dim
        for layer in layers:
            if not isinstance(layer, Layer) or len(layer.weights[0]) != width:
                raise ValueError('Incompatible consecutive layer dimensions.')
            width = len(layer.biases)
        out = vec(self.output)
        if len(out) != width:
            raise ValueError('Output dimension does not match the last layer.')
        object.__setattr__(self, 'layers', layers)
        object.__setattr__(self, 'output', out)
        object.__setattr__(self, 'offset', q(self.offset))

    def evaluate(self, x: Iterable[int | F], *, zero_bias: bool = False) -> F:
        values = vec(x)
        if len(values) != self.input_dim:
            raise ValueError('Wrong network input dimension.')
        for layer in self.layers:
            values = tuple(relu(dot(row, values) + (F(0) if zero_bias else b))
                           for row, b in zip(layer.weights, layer.biases))
        return dot(self.output, values) + (F(0) if zero_bias else self.offset)

    def envelopes(self) -> tuple[F, tuple[F, ...]]:
        """Return global beta and coordinatewise input sensitivity p (not tight)."""
        errors = (F(0),) * self.input_dim
        matrix = tuple(tuple(F(i == j) for j in range(self.input_dim))
                       for i in range(self.input_dim))
        for layer in self.layers:
            absolute = tuple(tuple(abs(v) for v in row) for row in layer.weights)
            errors = tuple(dot(row, errors) + abs(b)
                           for row, b in zip(absolute, layer.biases))
            matrix = tuple(tuple(sum((row[k] * matrix[k][j]
                                      for k in range(len(row))), F(0))
                                 for j in range(self.input_dim)) for row in absolute)
        absolute_out = tuple(abs(v) for v in self.output)
        beta = dot(absolute_out, errors) + abs(self.offset)
        p = tuple(sum((absolute_out[k] * matrix[k][j]
                       for k in range(len(absolute_out))), F(0))
                  for j in range(self.input_dim))
        return beta, p

    def source_remainder(self, centre: Iterable[int | F],
                         bounded: Iterable[Iterable[int | F]]) -> F:
        """C for x=centre+Bz+A eps. Does NOT certify the separate h0(Bz) premise."""
        centre = vec(centre)
        bounded = tuple(vec(row) for row in bounded)
        if len(centre) != self.input_dim or len(bounded) != self.input_dim:
            raise ValueError('Wrong source dimensions.')
        if len({len(row) for row in bounded}) != 1:
            raise ValueError('Ragged bounded-source matrix.')
        beta, p = self.envelopes()
        radius = tuple(abs(c) + sum(map(abs, row), F(0))
                       for c, row in zip(centre, bounded))
        return beta + dot(p, radius)


@dataclass(frozen=True)
class LineReLU:
    """q*z+c+sum(v*rho(k*z+b)); finite rational coefficients, all real z."""
    terms: tuple[tuple[F, F, F], ...]  # (v,k,b)
    linear: F = F(0)
    offset: F = F(0)

    def __post_init__(self) -> None:
        terms = tuple(vec(term) for term in self.terms)
        if any(len(term) != 3 for term in terms):
            raise ValueError('Each term must have (v,k,b).')
        object.__setattr__(self, 'terms', terms)
        object.__setattr__(self, 'linear', q(self.linear))
        object.__setattr__(self, 'offset', q(self.offset))

    def evaluate(self, z: int | F) -> F:
        z = q(z)
        return self.linear*z + self.offset + sum((v*relu(k*z+b) for v,k,b in self.terms), F(0))

    def slopes(self) -> tuple[F, F]:
        left = self.linear + sum((v*k for v,k,_ in self.terms if k < 0), F(0))
        right = self.linear + sum((v*k for v,k,_ in self.terms if k > 0), F(0))
        return left, right

    def candidates(self) -> tuple[F, ...]:
        return tuple(sorted({F(0)} | {-b/k for _,k,b in self.terms if k != 0}))

    def bounds(self) -> tuple[Optional[F], Optional[F]]:
        """None denotes -infinity at left, +infinity at right; never emptiness."""
        left, right = self.slopes()
        values = [self.evaluate(z) for z in self.candidates()]
        low = None if left > 0 or right < 0 else min(values)
        high = None if left < 0 or right > 0 else max(values)
        return low, high


SELF_VERSION = 'F04_SELF_TWO_BRANCH_v1'


@dataclass(frozen=True)
class JointSelfModel:
    vertices: tuple[tuple[F, F], ...]
    version: str = SELF_VERSION

    def __post_init__(self) -> None:
        vertices = tuple(vec(pair) for pair in self.vertices)
        if not vertices or any(len(pair) != 2 for pair in vertices):
            raise ValueError('Need a nonempty collection of (a,b) pairs.')
        for pair in vertices:
            for value in pair:
                probability(value)
        if self.version != SELF_VERSION:
            raise ValueError('Unsupported controller version; do not reuse its semantics.')
        object.__setattr__(self, 'vertices', vertices)

    @staticmethod
    def failure(pair: tuple[F, F], r: int | F) -> F:
        if len(pair) != 2:
            raise ValueError('Need (a,b).')
        a, b = (probability(v) for v in pair)
        r = probability(r)
        return a*r+b*(1-r)

    def floor(self) -> F:
        ratios = [b/(1-a+b) for a,b in self.vertices if 1-a+b > 0]
        return max([F(0), *ratios])

    def valid(self, r: int | F) -> bool:
        r = probability(r)
        return all(self.failure(pair, r) <= r for pair in self.vertices)

    def risk_interval(self, r: int | F) -> tuple[F, F]:
        r = probability(r)
        values = [self.failure(pair, r) for pair in self.vertices]
        return min(values), max(values)

    def robust_cost(self, r: int | F, k: int | F) -> F:
        r, k = probability(r), q(k)
        if k < 0:
            raise ValueError('Cautious-branch cost must be nonnegative in this fragment.')
        return self.risk_interval(r)[1]+k*r

    def optimizer_candidates(self, k: int | F, *,
                             bounds: Optional[tuple[F, F]] = None) -> tuple[F, ...]:
        k = q(k)
        if k < 0:
            raise ValueError('Negative cost is outside the declared fragment.')
        floor = self.floor()
        lower, upper = (floor, F(1)) if bounds is None else vec(bounds)
        if not floor <= lower <= upper <= 1:
            raise ValueError('Optimizer interval must lie within the report-valid interval.')
        lines = [(b, a-b+k) for a,b in self.vertices]
        choices = {lower, upper}
        for i, (b_i,s_i) in enumerate(lines):
            for b_j,s_j in lines[i+1:]:
                if s_i != s_j:
                    r = (b_j-b_i)/(s_i-s_j)
                    if lower <= r <= upper:
                        choices.add(r)
        return tuple(sorted(choices))

    def optimize(self, k: int | F) -> tuple[F, F]:
        k = q(k)
        choices = self.optimizer_candidates(k)
        # Canonical tie break: smallest report among equally good candidates.
        r = min(choices, key=lambda r: (self.robust_cost(r,k), r))
        return r, self.robust_cost(r,k)

    def paired_interval(self, old_r: int | F, k: int | F,
                        budget: int | F) -> tuple[F, F]:
        old_r, k, budget = probability(old_r), q(k), q(budget)
        if k < 0 or budget < 0:
            raise ValueError('Cost and deterioration budget must be nonnegative.')
        if not self.valid(old_r):
            raise ValueError('The old report must be valid under the current model.')
        slopes = [a-b+k for a,b in self.vertices]
        lower = max([self.floor(), *[old_r+budget/s for s in slopes if s < 0]])
        upper = min([F(1), *[old_r+budget/s for s in slopes if s > 0]])
        return lower, upper

    def optimize_guarded(self, old_r: int | F, k: int | F,
                         budget: int | F) -> tuple[F, F]:
        bounds = self.paired_interval(old_r, k, budget)
        candidates = self.optimizer_candidates(k, bounds=bounds)
        r = min(candidates, key=lambda r: (self.robust_cost(r,k), r))
        return r, self.robust_cost(r,k)

    def paired_change(self, old_r: int | F, new_r: int | F, k: int | F) -> F:
        """Worst signed change for the same hidden model; not difference of worst cases."""
        old_r, new_r, k = probability(old_r), probability(new_r), q(k)
        if k < 0:
            raise ValueError('Negative cost outside this fragment.')
        return max((a-b+k)*(new_r-old_r) for a,b in self.vertices)


def cost_probability(j0: int | F, j1: int | F) -> F:
    j0,j1 = q(j0),q(j1)
    if j0 <= 0 or j1 <= 0:
        raise ValueError('Both action costs must be strictly positive.')
    return j0/(j0+j1)


def swapped_cost_probability(donor_j0: int | F, base_j1: int | F,
                             donor_scale: int | F = 1, base_scale: int | F = 1) -> F:
    donor_scale, base_scale = q(donor_scale), q(base_scale)
    if donor_scale <= 0 or base_scale <= 0:
        raise ValueError('Scales must be strictly positive.')
    return cost_probability(q(donor_j0)*donor_scale, q(base_j1)*base_scale)


class NonlinearBoundsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.net = ReLUNetwork(2, (Layer(((2,-1),(-1,2)),(1,-2)),
                                  Layer(((1,-1),(-2,1)),(-1,3))), (1,-2), F(1,3))
        self.gap = LineReLU(((1,1,1),(-1,1,0)), offset=-2)

    def test_bias_envelope_on_signed_large_inputs(self):
        beta, _ = self.net.envelopes()
        for x in product([-10**20,-3,0,2,10**20], repeat=2):
            self.assertLessEqual(abs(self.net.evaluate(x)-self.net.evaluate(x,zero_bias=True)), beta)

    def test_zero_bias_positive_homogeneity(self):
        for x in product([-2,0,3], repeat=2):
            for scale in (0,F(1,7),2,10**10):
                self.assertEqual(self.net.evaluate([scale*v for v in x],zero_bias=True),
                                 scale*self.net.evaluate(x,zero_bias=True))

    def test_coordinatewise_sensitivity(self):
        _,p = self.net.envelopes()
        points = list(product([-2,0,3], repeat=2))
        for x,y in product(points,repeat=2):
            self.assertLessEqual(abs(self.net.evaluate(x,zero_bias=True)-self.net.evaluate(y,zero_bias=True)),
                                 dot(p, tuple(F(abs(a-b)) for a,b in zip(x,y))))

    def test_strip_remainder_uses_global_bound(self):
        centre=(F(1),F(-2)); A=((F(1,4),),(F(-1,2),))
        C=self.net.source_remainder(centre,A)
        for z,e in product([-10**20,-2,0,3,10**20],[-1,0,1]):
            x=(centre[0]+z+A[0][0]*e, centre[1]+z+A[1][0]*e)
            self.assertLessEqual(abs(self.net.evaluate(x)-self.net.evaluate((z,z),zero_bias=True)),C)

    def test_affine_network_with_no_hidden_layer(self):
        n=ReLUNetwork(2,(),(2,-1),3)
        self.assertEqual(n.envelopes(),(F(3),(F(2),F(1))))
        self.assertEqual(n.evaluate((4,5)),6)

    def test_sharp_nonnegative_loss_comparison(self):
        self.assertEqual(self.gap.bounds(),(F(-2),F(-1)))
        self.assertEqual(self.gap.evaluate(-1),-2)
        self.assertEqual(self.gap.evaluate(0),-1)
        n=ReLUNetwork(1,(Layer(((1,),(1,)),(1,0)),),(1,-1),-2)
        self.assertEqual(n.envelopes()[0],3)
        for z in (-10**20,-1,F(-1,2),0,10**20):
            self.assertEqual(n.evaluate((z,)),self.gap.evaluate(z))
            self.assertEqual(n.evaluate((z,),zero_bias=True),0)

    def test_bounded_does_not_imply_invariant(self):
        f=LineReLU(((1,1,1),(-1,1,0)))
        self.assertEqual(f.bounds(),(0,1))
        self.assertNotEqual(f.evaluate(-2),f.evaluate(2))

    def test_only_upper_bound_is_needed_for_no_deterioration(self):
        f=LineReLU(((-1,1,0),(-1,-1,0)))
        self.assertEqual(f.bounds(),(None,F(0)))
        self.assertEqual(f.evaluate(10**20),-10**20)

    def test_opposite_tail_failures(self):
        self.assertEqual(LineReLU(((1,1,0),)).bounds(),(F(0),None))
        self.assertEqual(LineReLU(((1,-1,0),)).bounds(),(F(0),None))
        self.assertEqual(LineReLU((),linear=1).bounds(),(None,None))

    def test_one_observed_cell_does_not_control_other_cells(self):
        f=LineReLU(((1,1,-2),))
        self.assertEqual([f.evaluate(x) for x in (-1,0,1)],[0,0,0])
        self.assertIsNone(f.bounds()[1])
        self.assertEqual(f.evaluate(100),98)

    def test_constant_units_and_empty_sum(self):
        self.assertEqual(LineReLU(((3,0,2),(-1,0,-9)),offset=-1).bounds(),(5,5))
        self.assertEqual(LineReLU((),offset=7).bounds(),(7,7))

    def test_breakpoint_enclosures_on_972_small_networks(self):
        cases=0
        for k1,k2 in product((-1,1), repeat=2):
            for v1,v2,b1,b2,lin in product((-1,0,1),repeat=5):
                f=LineReLU(((v1,k1,b1),(v2,k2,b2)),linear=lin)
                lo,hi=f.bounds(); points=(*f.candidates(),F(-100),F(100),F(1,3))
                for z in points:
                    value=f.evaluate(z)
                    if lo is not None:self.assertLessEqual(lo,value)
                    if hi is not None:self.assertGreaterEqual(hi,value)
                if lo is not None:self.assertIn(lo,[f.evaluate(z) for z in f.candidates()])
                if hi is not None:self.assertIn(hi,[f.evaluate(z) for z in f.candidates()])
                cases+=1
        self.assertEqual(cases,972)

    def test_invariant_output_without_invariant_hidden_preactivations(self):
        n=ReLUNetwork(2,(Layer(((1,0),(-1,0),(0,1),(0,-1)),(0,0,0,0)),),(1,-1,-1,1))
        for x,y,t in product((-2,0,3),repeat=3):
            self.assertEqual(n.evaluate((x+t,y+t)),F(x-y))
        self.assertTrue(all(sum(row)!=0 for row in n.layers[0].weights))

    def test_squared_transform_breaks_fixed_difference_bound(self):
        for z in (0,1,10,10**20):
            self.assertEqual((z+1)**2-z**2,2*z+1)
        self.assertGreater((10+1)**2-10**2,1)

    def test_invalid_networks_and_inexact_inputs_rejected(self):
        with self.assertRaises(ValueError):Layer(((1,),(1,2)),(0,0))
        with self.assertRaises(ValueError):ReLUNetwork(2,(Layer(((1,),),(0,)),),(1,))
        with self.assertRaises(ValueError):self.net.evaluate((1,))
        with self.assertRaises(TypeError):self.net.evaluate((1.0,0))
        with self.assertRaises(ValueError):self.net.source_remainder((0,0),((1,),()))
        with self.assertRaises(ValueError):LineReLU(((1,2),))


class JointReflectionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.joint=JointSelfModel(((F(9,10),0),(0,F(9,10))))

    def test_exact_joint_floor(self):
        self.assertEqual(self.joint.floor(),F(9,19))
        self.assertTrue(self.joint.valid(F(9,19)))
        self.assertFalse(self.joint.valid(F(9,19)-F(1,10000)))
        self.assertTrue(self.joint.valid(F(1,2)))

    def test_preserves_convex_hull_constraints(self):
        R=self.joint.floor()
        for weight in (F(i,20) for i in range(21)):
            pair=(F(9,10)*weight,F(9,10)*(1-weight))
            for r in (R,(1+R)/2,F(1)):
                self.assertLessEqual(self.joint.failure(pair,r),r)

    def test_rectangular_relaxation_discards_a_useful_report(self):
        box=JointSelfModel(((0,0),(0,F(9,10)),(F(9,10),0),(F(9,10),F(9,10))))
        self.assertEqual(box.floor(),F(9,10))
        self.assertFalse(box.valid(F(1,2)))
        self.assertTrue(self.joint.valid(F(1,2)))

    def test_best_policy_is_not_the_least_report(self):
        r,value=self.joint.optimize(0)
        self.assertEqual((r,value),(F(1,2),F(9,20)))
        self.assertGreater(self.joint.robust_cost(self.joint.floor(),0),value)

    def test_degenerate_identity_branch_pair_does_not_divide_by_zero(self):
        m=JointSelfModel(((1,0),))
        self.assertEqual(m.floor(),0)
        for r in (0,F(1,7),1):self.assertTrue(m.valid(r))
        self.assertEqual(m.optimize(0),(F(0),F(0)))

    def test_always_failing_model_has_only_report_one(self):
        m=JointSelfModel(((1,1),))
        self.assertEqual(m.floor(),1)
        self.assertFalse(m.valid(F(99,100)))
        self.assertEqual(m.risk_interval(1),(F(1),F(1)))

    def test_pointwise_optimizers_are_not_one_unknown_parameter_policy(self):
        per_model=[JointSelfModel((p,)).optimize(0)[1] for p in self.joint.vertices]
        self.assertEqual(per_model,[0,0])
        self.assertEqual(self.joint.optimize(0)[1],F(9,20))

    def test_refinement_can_improve_robust_optimum_but_worsen_actual_cost(self):
        T=(F(0),F(1,5)); B=(F(0),F(4,5)); C=(F(9,10),F(9,10));k=F(3,10)
        old,new=JointSelfModel((T,B,C)),JointSelfModel((T,B))
        ro,vo=old.optimize(k);rn,vn=new.optimize(k)
        self.assertEqual((ro,vo),(F(9,10),F(117,100)))
        self.assertEqual((rn,vn),(F(1),F(3,10)))
        self.assertLess(vn,vo)
        old_actual=old.failure(T,ro)+k*ro; new_actual=new.failure(T,rn)+k*rn
        self.assertEqual((old_actual,new_actual),(F(29,100),F(3,10)))
        self.assertGreater(new_actual,old_actual)

    def test_paired_policy_comparison_catches_the_refinement_counterexample(self):
        m=JointSelfModel(((0,F(1,5)),(0,F(4,5))))
        self.assertEqual(m.paired_change(F(9,10),1,F(3,10)),F(1,100))
        self.assertLess(m.paired_change(F(9,10),1,0),0)

    def test_finite_optimizer_against_rational_grid_135_cases(self):
        points=list(product((F(0),F(1,2),F(1)),repeat=2));cases=0
        for pair in combinations_with_replacement(points,2):
            for k in (0,F(1,2),1):
                m=JointSelfModel(pair);r,v=m.optimize(k)
                self.assertTrue(m.valid(r))
                for candidate in (F(i,20) for i in range(21)):
                    if m.valid(candidate):self.assertLessEqual(v,m.robust_cost(candidate,k))
                cases+=1
        self.assertEqual(cases,135)

    def test_duplicate_vertices_and_flat_objective_ties(self):
        m=JointSelfModel(((0,F(1,2)),(0,F(1,2))))
        self.assertEqual(m.optimize(F(1,2)),(F(1,3),F(1,2)))

    def test_guarded_interval_attains_an_exact_deterioration_budget(self):
        m=JointSelfModel(((0,F(1,5)),(0,F(4,5))))
        self.assertEqual(m.paired_interval(F(9,10),F(3,10),F(1,200)),
                         (F(89,100),F(19,20)))
        r,v=m.optimize_guarded(F(9,10),F(3,10),F(1,200))
        self.assertEqual((r,v),(F(19,20),F(13,40)))
        self.assertEqual(m.paired_change(F(9,10),r,F(3,10)),F(1,200))

    def test_zero_budget_freezes_oppositely_ordered_policies(self):
        m=JointSelfModel(((0,F(1,5)),(0,F(4,5))))
        self.assertEqual(m.paired_interval(F(9,10),F(3,10),0),(F(9,10),F(9,10)))
        self.assertEqual(m.optimize_guarded(F(9,10),F(3,10),0),(F(9,10),F(7,20)))

    def test_zero_budget_can_still_permit_strict_improvement(self):
        m=JointSelfModel(((0,F(4,5)),(0,F(3,5))))
        r,v=m.optimize_guarded(F(1,2),F(1,5),0)
        self.assertEqual((r,v),(F(1),F(1,5)))
        self.assertLess(v,m.robust_cost(F(1,2),F(1,5)))
        self.assertLess(m.paired_change(F(1,2),r,F(1,5)),0)

    def test_paired_budget_telescopes_over_two_revisions(self):
        m=JointSelfModel(((0,F(1,5)),(0,F(4,5))))
        r0=F(9,10);k=F(3,10);d=F(1,400)
        r1,_=m.optimize_guarded(r0,k,d);r2,_=m.optimize_guarded(r1,k,d)
        self.assertEqual((r1,r2),(F(37,40),F(19,20)))
        self.assertEqual(m.paired_change(r0,r2,k),2*d)

    def test_guarded_optimizer_in_270_finite_cases(self):
        points=list(product((F(0),F(1,2),F(1)),repeat=2));cases=0
        for pair in combinations_with_replacement(points,2):
            m=JointSelfModel(pair);old=(1+m.floor())/2
            for k,d in product((F(0),F(1,2),F(1)),(F(0),F(1,10))):
                r,v=m.optimize_guarded(old,k,d)
                self.assertTrue(m.valid(r))
                self.assertLessEqual(m.paired_change(old,r,k),d)
                self.assertLessEqual(v,m.robust_cost(old,k))
                cases+=1
        self.assertEqual(cases,270)

    def test_negative_deterioration_allowance_rejected(self):
        with self.assertRaises(ValueError):self.joint.optimize_guarded(1,0,-1)

    def test_invalid_old_report_is_not_assumed_available(self):
        with self.assertRaises(ValueError):self.joint.optimize_guarded(0,0,1)

    def test_input_and_version_guards(self):
        with self.assertRaises(ValueError):JointSelfModel(())
        with self.assertRaises(ValueError):JointSelfModel(((0,2),))
        with self.assertRaises(ValueError):JointSelfModel(((0,0),),version='new-unchecked-version')
        with self.assertRaises(TypeError):JointSelfModel(((0.0,1),))
        with self.assertRaises(ValueError):self.joint.optimize(-1)
        with self.assertRaises(ValueError):self.joint.valid(2)


class CostIdentifiabilityTests(unittest.TestCase):
    def test_observational_equivalence_under_positive_common_scaling(self):
        for a,b,g in product((F(1,4),F(1),F(3)),repeat=3):
            self.assertEqual(cost_probability(a,b),cost_probability(g*a,g*b))

    def test_input_dependent_scaling_changes_interchange_prediction(self):
        self.assertEqual(swapped_cost_probability(F(3,4),F(1,2)),F(3,5))
        self.assertEqual(swapped_cost_probability(F(3,4),F(1,2),2,1),F(3,4))

    def test_equal_positive_scales_exactly_characterize_same_swap(self):
        for a,b,gd,gb in product((F(1,3),F(1),F(2)),repeat=4):
            self.assertEqual(swapped_cost_probability(a,b,gd,gb)==swapped_cost_probability(a,b),gd==gb)

    def test_nonpositive_costs_or_scales_rejected(self):
        with self.assertRaises(ValueError):cost_probability(0,1)
        with self.assertRaises(ValueError):swapped_cost_probability(1,1,-1,1)
        with self.assertRaises(TypeError):cost_probability(True,1)


def report() -> dict:
    gap=LineReLU(((1,1,1),(-1,1,0)),offset=-2)
    joint=JointSelfModel(((F(9,10),0),(0,F(9,10))))
    old=JointSelfModel(((0,F(1,5)),(0,F(4,5)),(F(9,10),F(9,10))))
    new=JointSelfModel(((0,F(1,5)),(0,F(4,5))))
    return {
        'task':'F04','session':'2026-09-26-S2',
        'evidence_scope':'Exact rational development fixtures; no trained model, generic ReLU verifier, RLL proof engine or held-out evaluation.',
        'nonlinear_gap':{'range':list(map(str,gap.bounds())),
                         'tail_slopes':list(map(str,gap.slopes())),
                         'breakpoints':list(map(str,gap.candidates())),
                         'global_bias_envelope':'3',
                         'useful_improvement':'1'},
        'one_sided_negative_absolute':{'lower':'-infinity','upper':'0'},
        'joint_reflection':{'report_floor':str(joint.floor()),
                            'optimal_report_and_cost':list(map(str,joint.optimize(0))),
                            'rectangular_report_floor':'9/10'},
        'refinement':{'old_optimum':list(map(str,old.optimize(F(3,10)))),
                      'new_optimum':list(map(str,new.optimize(F(3,10)))),
                      'actual_cost_old':'29/100','actual_cost_new':'3/10',
                      'paired_worst_deterioration':str(new.paired_change(F(9,10),1,F(3,10)))},
        'guarded_revision':{'budget':'1/200','feasible_interval':['89/100','19/20'],
                            'optimum':list(map(str,new.optimize_guarded(F(9,10),F(3,10),F(1,200)))),
                            'paired_change':str(new.paired_change(F(9,10),F(19,20),F(3,10)))},
        'cost_scale_intervention':{'original':'3/5','recoded':'3/4'},
        'enumeration':{'two_unit_line_networks':972,'reflection_grid_comparisons':135, 'guarded_revision_cases':270,
                       'notice':'Finite tests exercise analytic algorithms; they do not prove unrestricted network or reflection theorems.'}
    }


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json',type=Path)
    args=parser.parse_args()
    suite=unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromTestCase(cls)
                             for cls in (NonlinearBoundsTests,JointReflectionTests,CostIdentifiabilityTests))
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():return 1
    if args.json:
        args.json.parent.mkdir(parents=True,exist_ok=True)
        args.json.write_text(json.dumps(report(),indent=2,sort_keys=True)+'\n',encoding='utf-8')
    return 0


if __name__=='__main__':
    raise SystemExit(main())
