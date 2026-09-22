"""Exact, finite F02 candidate checks, not the later phase-two reasoner.

All cases are constructed development fixtures. Fractions avoid hidden floating
point error. Types guard dimensions/units, not unobservable semantic assumptions
such as whether a chooser may inspect a hidden state or two policies can compose.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import product
import json
from pathlib import Path
from typing import Callable, Iterable, Sequence
import unittest

Number = int | Q
Vector = tuple[Q, ...]


def vec(xs: Iterable[Number]) -> Vector:
    out = []
    for x in xs:
        if isinstance(x, bool) or not isinstance(x, (int, Q)):
            raise TypeError("Use integers or Fractions for exact fixtures.")
        out.append(Q(x))
    return tuple(out)


def dot(x: Sequence[Q], y: Sequence[Q]) -> Q:
    if len(x) != len(y):
        raise ValueError("Vector dimensions must agree.")
    return sum((a * b for a, b in zip(x, y)), Q(0))


def weighted(x: Sequence[Number], p: Sequence[Number]) -> Q:
    x, p = vec(x), vec(p)
    if not x or len(x) != len(p) or any(a < 0 for a in p) or sum(p) != 1:
        raise ValueError("Weights must be a matching nonempty probability vector.")
    return dot(x, p)


def infnorm(x: Sequence[Q]) -> Q:
    if not x:
        raise ValueError("A value vector must be nonempty.")
    return max(abs(a) for a in x)


def osc(x: Sequence[Q]) -> Q:
    if not x:
        raise ValueError("A value vector must be nonempty.")
    return max(x) - min(x)


def squash(x: Number) -> Q:
    x = vec((x,))[0]
    return x / (1 + abs(x))


def unsquash(x: Number) -> Q:
    x = vec((x,))[0]
    if abs(x) >= 1:
        raise ValueError("The exact bounded code lies strictly between -1 and 1.")
    return x / (1 - abs(x))


@dataclass(frozen=True)
class Scalar:
    value: Q
    task: str = "fixed-task"
    unit: str = "payoff"

    def __post_init__(self) -> None:
        object.__setattr__(self, "value", vec((self.value,))[0])

    def add(self, other: Scalar) -> Scalar:
        if (self.task, self.unit) != (other.task, other.unit):
            raise ValueError("Additive values need the same task and unit.")
        return Scalar(self.value + other.value, self.task, self.unit)


@dataclass(frozen=True)
class Profile:
    labels: tuple[str, ...]
    values: Vector
    unit: str = "payoff"

    def __post_init__(self) -> None:
        object.__setattr__(self, "values", vec(self.values))
        if not self.labels or len(self.labels) != len(self.values):
            raise ValueError("Labels and values must be nonempty and matched.")
        if len(set(self.labels)) != len(self.labels):
            raise ValueError("Scenario labels must be unique.")

    def combine(self, other: Profile, op: Callable[[Q, Q], Q]) -> Profile:
        if self.labels != other.labels or self.unit != other.unit:
            raise ValueError("Joint profiles require explicit common alignment and units.")
        return Profile(self.labels, tuple(op(x, y) for x, y in zip(self.values, other.values)), self.unit)

    def value(self, weights: Sequence[Number]) -> Q:
        return weighted(self.values, weights)


@dataclass(frozen=True)
class Step:
    inputs: tuple[str, ...]
    outputs: tuple[str, ...]
    rewards: Vector
    kernel: tuple[Vector, ...]
    unit: str = "payoff"

    def __post_init__(self) -> None:
        object.__setattr__(self, "rewards", vec(self.rewards))
        object.__setattr__(self, "kernel", tuple(vec(row) for row in self.kernel))
        if not self.inputs or not self.outputs:
            raise ValueError("Interfaces must be nonempty.")
        if len(set(self.inputs)) != len(self.inputs) or len(set(self.outputs)) != len(self.outputs):
            raise ValueError("Interface labels must be unique.")
        if len(self.rewards) != len(self.inputs) or len(self.kernel) != len(self.inputs):
            raise ValueError("There must be one reward and kernel row per input.")
        for row in self.kernel:
            if len(row) != len(self.outputs) or any(x < 0 for x in row) or sum(row) != 1:
                raise ValueError("Every kernel row must be a matching probability vector.")

    def __call__(self, continuation: Sequence[Number]) -> Vector:
        h = vec(continuation)
        if len(h) != len(self.outputs):
            raise ValueError("Continuation does not match the output interface.")
        return tuple(r + dot(p, h) for r, p in zip(self.rewards, self.kernel))

    def then(self, other: Step) -> Step:
        if self.outputs != other.inputs or self.unit != other.unit:
            raise ValueError("Sequential interfaces and payoff units must match.")
        rewards = self(other.rewards)
        kernel = tuple(tuple(sum((p[b] * other.kernel[b][c] for b in range(len(p))), Q(0))
                             for c in range(len(other.outputs))) for p in self.kernel)
        return Step(self.inputs, other.outputs, rewards, kernel, self.unit)


def branch(steps: Sequence[Step], h: Sequence[Number], operation: str) -> Vector:
    if not steps or operation not in {"min", "max"}:
        raise ValueError("A branch needs nonempty children and min/max semantics.")
    first = steps[0]
    if any((s.inputs, s.outputs, s.unit) != (first.inputs, first.outputs, first.unit) for s in steps):
        raise ValueError("Branch interfaces and units must match.")
    values = [s(h) for s in steps]
    fn = min if operation == "min" else max
    return tuple(fn(v[a] for v in values) for a in range(len(first.inputs)))


def probabilities(dimension: int, denominator: int) -> tuple[Vector, ...]:
    if dimension <= 0 or denominator <= 0:
        raise ValueError("Positive dimension and denominator are required.")
    return tuple(tuple(Q(n, denominator) for n in ns)
                 for ns in product(range(denominator + 1), repeat=dimension)
                 if sum(ns) == denominator)


def total_variation(p: Sequence[Number], q: Sequence[Number]) -> Q:
    p, q = vec(p), vec(q)
    weighted(p, q)  # Validate q's dimensions and probability properties.
    weighted(q, p)
    return sum((abs(a - b) for a, b in zip(p, q)), Q(0)) / 2


def leq(x: Sequence[Q], y: Sequence[Q]) -> bool:
    if len(x) != len(y):
        raise ValueError("Cost dimensions must agree.")
    return all(a <= b for a, b in zip(x, y))


def minimal(points: Iterable[Sequence[Number]], dimension: int) -> tuple[Vector, ...]:
    if dimension <= 0:
        raise ValueError("A cost vector must have positive dimension.")
    unique = sorted(set(vec(x) for x in points))
    if any(len(x) != dimension for x in unique):
        raise ValueError("Cost dimensions must agree.")
    return tuple(x for x in unique if not any(y != x and leq(y, x) for y in unique))


@dataclass(frozen=True)
class Front:
    units: tuple[str, ...]
    points: tuple[Vector, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "points", minimal(self.points, len(self.units)))

    def compatible(self, other: Front) -> None:
        if self.units != other.units:
            raise ValueError("Resource components and units must match.")

    def feasible(self, budget: Sequence[Number]) -> bool:
        b = vec(budget)
        if len(b) != len(self.units):
            raise ValueError("Budget dimensions must match the resource interface.")
        return any(leq(a, b) for a in self.points)

    def choice(self, other: Front) -> Front:
        self.compatible(other)
        return Front(self.units, self.points + other.points)

    def independent_add(self, other: Front) -> Front:
        """Valid only when every pair of local controlled choices may compose."""
        self.compatible(other)
        return Front(self.units, tuple(tuple(x + y for x, y in zip(a, b))
                                      for a in self.points for b in other.points))

    def separate_budget_intersection(self, other: Front) -> Front:
        self.compatible(other)
        return Front(self.units, tuple(tuple(max(x, y) for x, y in zip(a, b))
                                      for a in self.points for b in other.points))


@dataclass(frozen=True)
class Edge:
    source: str
    target: str
    cost: Vector

    def __post_init__(self) -> None:
        object.__setattr__(self, "cost", vec(self.cost))


@dataclass(frozen=True)
class ResourceRelation:
    inputs: tuple[str, ...]
    outputs: tuple[str, ...]
    units: tuple[str, ...]
    edges: tuple[Edge, ...]

    def __post_init__(self) -> None:
        if not self.inputs or not self.outputs or not self.units:
            raise ValueError("Relation interfaces and resource dimensions must be nonempty.")
        groups: dict[tuple[str, str], list[Vector]] = {}
        for e in self.edges:
            if e.source not in self.inputs or e.target not in self.outputs or len(e.cost) != len(self.units):
                raise ValueError("An edge violates the declared interface.")
            groups.setdefault((e.source, e.target), []).append(e.cost)
        reduced = [Edge(a, b, c) for (a, b), cs in sorted(groups.items())
                   for c in minimal(cs, len(self.units))]
        object.__setattr__(self, "edges", tuple(reduced))

    def then(self, other: ResourceRelation) -> ResourceRelation:
        if self.outputs != other.inputs or self.units != other.units:
            raise ValueError("Sequential resource interfaces must match.")
        edges = tuple(Edge(e.source, f.target, tuple(x + y for x, y in zip(e.cost, f.cost)))
                      for e in self.edges for f in other.edges if e.target == f.source)
        return ResourceRelation(self.inputs, other.outputs, self.units, edges)


class F02CandidateTests(unittest.TestCase):
    def test_exact_number_guard(self):
        with self.assertRaises(TypeError):
            vec((0.1,))

    def test_scalar_context_guard(self):
        with self.assertRaises(ValueError):
            Scalar(Q(1), "task-a").add(Scalar(Q(1), "task-b"))

    def test_scalar_unit_guard(self):
        with self.assertRaises(ValueError):
            Scalar(Q(1), unit="metres").add(Scalar(Q(1), unit="seconds"))

    def test_scalar_cost_preference_and_feasibility_collision(self):
        self.assertGreater(-Q(1, 1000) - Q(1, 1000), -8 * Q(1, 1000))
        self.assertLess(-Q(1, 1000) - Q(1, 10000), -8 * Q(1, 10000))
        self.assertEqual(Q(1, 8) + Q(1, 56), 8 * Q(1, 56))
        self.assertGreater(Q(1, 8), Q(1, 100))

    def test_task_weight_reversal_and_boundary(self):
        self.assertGreater(-4 * (1 - Q(9, 10)), -1)
        self.assertLess(-4 * (1 - Q(1, 10)), -1)
        self.assertEqual(-4 * (1 - Q(3, 4)), -1)

    def test_profile_alignment_and_units_guard(self):
        a = Profile(("a", "b"), (Q(3), Q(-1)))
        for b in [Profile(("b", "a"), a.values), Profile(a.labels, a.values, "seconds")]:
            with self.assertRaises(ValueError):
                a.combine(b, min)

    def test_profile_joint_counterexample(self):
        a = Profile(("a", "b"), (Q(3), Q(-1)))
        b = Profile(a.labels, (Q(-1), Q(3)))
        p = (Q(1, 2), Q(1, 2))
        self.assertEqual((a.value(p), b.value(p)), (1, 1))
        self.assertEqual(a.combine(b, min).value(p), -1)
        self.assertEqual(a.combine(a, min).value(p), 1)
        self.assertEqual(a.combine(b, lambda x, y: x + y).value(p), 2)

    def test_expectation_additive_without_independence(self):
        for x, y in product(product((-2, 0, 3), repeat=2), repeat=2):
            for t in (Q(0), Q(1, 4), Q(1, 2), Q(3, 4), Q(1)):
                p = (t, 1-t)
                self.assertEqual(weighted(tuple(a+b for a,b in zip(x,y)),p), weighted(x,p)+weighted(y,p))

    def test_minimum_gap_and_exact_equality_boundary(self):
        p = (Q(1, 3), Q(2, 3))
        for x, y in product(product(range(-2, 3), repeat=2), repeat=2):
            ex, ey = weighted(x, p), weighted(y, p)
            emin = weighted(tuple(min(a, b) for a, b in zip(x, y)), p)
            gap = (weighted(tuple(abs(a-b) for a,b in zip(x,y)),p)-abs(ex-ey))/2
            self.assertEqual(min(ex, ey)-emin, gap)
            self.assertEqual(emin == min(ex, ey), leq(x,y) or leq(y,x))

    def test_minimum_equality_ignores_zero_weight_coordinates(self):
        x, y, p = (0,10), (1,-10), (1,0)
        self.assertFalse(leq(x,y) or leq(y,x))
        self.assertEqual(weighted(tuple(min(a,b) for a,b in zip(x,y)),p), min(weighted(x,p),weighted(y,p)))

    def test_unbounded_fixed_mean_family(self):
        for n in range(21):
            x, y = (1+n,1-n), (1-n,1+n)
            self.assertEqual(weighted(x,(Q(1,2),Q(1,2))),1)
            self.assertEqual(weighted(y,(Q(1,2),Q(1,2))),1)
            self.assertEqual(weighted(tuple(min(a,b) for a,b in zip(x,y)),(Q(1,2),Q(1,2))),1-n)

    def test_profile_model_envelope_is_not_modelwise_expectation(self):
        xs = [(3,-1),(-1,3)]
        self.assertEqual(min(weighted(x,(Q(1,2),Q(1,2))) for x in xs),1)
        envelope = tuple(min(x[i] for x in xs) for i in range(2))
        self.assertEqual(weighted(envelope,(Q(1,2),Q(1,2))),-1)

    def test_interval_dependency_loss(self):
        self.assertEqual((0-1,1-0),(-1,1))
        self.assertEqual({x-x for x in (Q(0),Q(1,2),Q(1))},{0})

    def test_interval_tolerance_without_exact_recovery(self):
        self.assertGreaterEqual(-Q(1,2),-Q(3,5))
        self.assertNotEqual(-Q(1,2),-Q(1,3))

    def test_reachable_scope_scalar_propagation(self):
        self.assertEqual(Q(1,50)+100*Q(1,100),Q(51,50))
        self.assertNotEqual(Q(1,50)+Q(1,100),Q(51,50))

    def test_bottleneck_mean_errors_can_add(self):
        x,y,xh,yh=(1,1),(1,1),(0,1),(1,0)
        p=(Q(1,2),Q(1,2))
        ex=weighted(tuple(abs(a-b) for a,b in zip(x,xh)),p)
        ey=weighted(tuple(abs(a-b) for a,b in zip(y,yh)),p)
        combined=weighted(tuple(abs(min(a,b)-min(c,d)) for a,b,c,d in zip(x,y,xh,yh)),p)
        self.assertEqual((ex,ey,combined),(Q(1,2),Q(1,2),1))
        self.assertGreater(combined,max(ex,ey))

    def test_bottleneck_uniform_error_bound(self):
        profiles=list(product((-1,0,1),repeat=2))
        for x,y,xh,yh in product(profiles,repeat=4):
            error=max(abs(min(a,b)-min(c,d)) for a,b,c,d in zip(x,y,xh,yh))
            bound=max(max(abs(a-b) for a,b in zip(x,xh)),max(abs(a-b) for a,b in zip(y,yh)))
            self.assertLessEqual(error,bound)

    def test_bounded_code_requires_transported_operations(self):
        for a,b in product(range(-3,4),repeat=2):
            self.assertEqual(unsquash(squash(a)),a)
            encoded_sum = squash(unsquash(squash(a)) + unsquash(squash(b)))
            self.assertEqual(unsquash(encoded_sum), a+b)
        self.assertNotEqual((squash(1)+squash(3))/2,squash(Q(2)))
        with self.assertRaises(ValueError):
            unsquash(1)

    def test_step_probability_guard(self):
        for p in [(-1,2),(0,0),(Q(1,2),)]:
            with self.assertRaises(ValueError):
                Step(("s",),("L","R"),(Q(0),),(p,))

    def test_step_interface_guard(self):
        a=Step(("s",),("L","R"),(Q(0),),((Q(1),Q(0)),))
        with self.assertRaises(ValueError):
            a((1,))
        b=Step(("wrong",),("t",),(Q(0),),((Q(1),),))
        with self.assertRaises(ValueError):
            a.then(b)

    def test_equal_zero_values_different_continuations(self):
        l=Step(("s",),("L","R"),(Q(0),),((Q(1),Q(0)),))
        r=Step(("s",),l.outputs,(Q(0),),((Q(0),Q(1)),))
        self.assertEqual(l((0,0)),r((0,0)))
        self.assertEqual((l((10,0)),r((10,0))),((10,),(0,)))
        self.assertEqual((l((0,10)),r((0,10))),((0,),(10,)))

    def test_affine_composition_matches_direct_propagation(self):
        e=Step(("s",),("low","high"),(Q(-1),),((Q(1,4),Q(3,4)),))
        f=Step(e.outputs,("fail","pass"),(Q(-2),Q(-2)),((Q(1),Q(0)),(Q(0),Q(1))))
        ef=e.then(f)
        self.assertEqual(ef.rewards,(-3,))
        self.assertEqual(ef((0,10)),(Q(9,2),))
        for h in product((-3,0,10),repeat=2):
            self.assertEqual(ef(h),e(f(h)))

    def test_choice_is_not_lower_envelope_concave(self):
        l=Step(("s",),("L","R"),(Q(0),),((Q(1),Q(0)),))
        r=Step(l.inputs,l.outputs,(Q(0),),((Q(0),Q(1)),))
        middle=branch((l,r),(Q(1,2),Q(1,2)),"max")[0]
        ends=(branch((l,r),(1,0),"max")[0]+branch((l,r),(0,1),"max")[0])/2
        self.assertEqual((middle,ends),(Q(1,2),1))
        self.assertLess(middle,ends)

    def test_empty_and_mismatched_choices_rejected(self):
        with self.assertRaises(ValueError):
            branch((),(0,),"min")
        a=Step(("a",),("b",),(Q(0),),((Q(1),),))
        b=Step(("x",),("b",),(Q(0),),((Q(1),),))
        with self.assertRaises(ValueError):
            branch((a,b),(0,),"max")

    def test_transformer_shift_monotonicity_and_uniform_bound(self):
        a=Step(("s","t"),("L","R"),(Q(2),Q(-1)),((Q(1,4),Q(3,4)),(Q(1),Q(0))))
        b=Step(a.inputs,a.outputs,(Q(-2),Q(3)),((Q(0),Q(1)),(Q(1,2),Q(1,2))))
        hs=list(product((-1,0,2),repeat=2))
        for kind in ("min","max"):
            for h,k in product(hs,repeat=2):
                th,tk=branch((a,b),h,kind),branch((a,b),k,kind)
                if leq(h,k): self.assertTrue(leq(th,tk))
                self.assertLessEqual(infnorm(tuple(x-y for x,y in zip(th,tk))),infnorm(tuple(Q(x-y) for x,y in zip(h,k))))
            for h in hs:
                shifted=branch((a,b),tuple(Q(x+7) for x in h),kind)
                self.assertEqual(shifted,tuple(x+7 for x in branch((a,b),h,kind)))
                self.assertLessEqual(osc(branch((a,b),h,kind)),osc(branch((a,b),(0,0),kind))+osc(h))

    def test_fixed_parameter_must_survive_composition(self):
        true=min(t+(1-t) for t in (0,1))
        separately=min((0,1))+min((1,0))
        self.assertEqual((true,separately),(1,0))

    def test_hidden_model_control_and_randomization(self):
        table=((Q(1),Q(0)),(Q(0),Q(1)))
        robust=max(min(a) for a in table)
        revealed=min(max(table[a][t] for a in range(2)) for t in range(2))
        mixed=min(Q(1,2)*table[0][t]+Q(1,2)*table[1][t] for t in range(2))
        self.assertEqual((robust,revealed,mixed),(0,1,Q(1,2)))
        self.assertNotEqual((min(table[0])+min(table[1]))/2,mixed)

    def test_product_uncertainty_identity(self):
        p=(Q(1,4),Q(3,4)); z=((Q(2),Q(-1)),(Q(-2),Q(4)))
        local=sum((p[b]*min(z[b]) for b in range(2)),Q(0))
        independent=min(sum((p[b]*z[b][j[b]] for b in range(2)),Q(0)) for j in product(range(2),repeat=2))
        shared=min(sum((p[b]*z[b][j] for b in range(2)),Q(0)) for j in range(2))
        self.assertEqual(local,independent)
        self.assertLess(local,shared)

    def test_signal_value_from_independent_policy_enumeration(self):
        for p,kappa in product((Q(1,2),Q(3,4),Q(1)),(Q(0),Q(1,4),Q(2))):
            returns=[]
            for policy in product((0,1),repeat=2):
                payoff=Q(0)
                for w,s in product((0,1),repeat=2):
                    joint=Q(1,2)*(p if w==s else 1-p)
                    payoff+=joint*(3 if policy[s]==w else -1)
                returns.append(payoff-kappa)
            self.assertEqual(max([Q(1)]+returns),max(Q(1),4*p-1-kappa))
        self.assertEqual(max(Q(1),4*Q(3,4)-1-Q(1,4)),Q(7,4))

    def test_span_bound_is_exact_on_all_finite_vertices(self):
        ps=probabilities(3,4)
        self.assertEqual(len(ps),15)
        for p,q,m,offset in product(ps,ps,(Q(0),Q(1),Q(3)),(Q(-1),Q(0),Q(2))):
            differences=[offset+dot(tuple(a-b for a,b in zip(p,q)),h) for h in product((Q(0),m),repeat=3)]
            self.assertEqual(min(differences),offset-m*total_variation(p,q))
            self.assertEqual(max(abs(x) for x in differences),abs(offset)+m*total_variation(p,q))

    def test_span_comparison_is_shift_invariant_and_unbounded_in_origin(self):
        p,q=(Q(1,4),Q(3,4)),(Q(3,4),Q(1,4))
        d=tuple(a-b for a,b in zip(p,q))
        for h,c in product(product((Q(0),Q(2)),repeat=2),(Q(-1000),Q(0),Q(1000))):
            self.assertEqual(dot(d,h),dot(d,tuple(x+c for x in h)))

    def test_unrestricted_continuation_counterexample(self):
        p,q=(Q(1,4),Q(3,4)),(Q(3,4),Q(1,4))
        d=tuple(a-b for a,b in zip(p,q)); h=tuple(-32*x for x in d)
        self.assertLess(10+dot(p,h),dot(q,h)-5)

    def test_resource_benefit_can_dominate_bounded_relative_stakes(self):
        for h in product((0,1),repeat=2):
            self.assertGreaterEqual(-1+h[0],-2+h[1])
        self.assertLess(-1+0,-2+2)

    def test_missing_continuation_closure_breaks_chaining(self):
        l=Step(("s",),("L","R"),(Q(0),),((Q(1),Q(0)),))
        r=Step(l.inputs,l.outputs,l.rewards,((Q(0),Q(1)),))
        suffix=Step(l.outputs,("t",),(Q(0),Q(10)),((Q(1),),(Q(1),)))
        for h in product((0,1),repeat=2): self.assertGreaterEqual(l(h)[0],r(h)[0]-1)
        self.assertEqual((l.then(suffix)((0,)),r.then(suffix)((0,))),((0,),(10,)))
        self.assertGreater(osc(suffix((0,))),1)

    def test_error_chaining_with_valid_interfaces(self):
        p=((Q(1,3),Q(2,3)),)
        u1=Step(("s",),("L","R"),(Q(0),),p)
        t1=Step(u1.inputs,u1.outputs,(Q(-1,4),),p)
        u2=Step(u1.outputs,("a","b"),(Q(0),Q(1)),((Q(1),Q(0)),(Q(0),Q(1))))
        t2=Step(u2.inputs,u2.outputs,(Q(-1,3),Q(2,3)),u2.kernel)
        for h in product((-2,0,2),repeat=2):
            self.assertEqual(t1.then(t2)(h)[0],u1.then(u2)(h)[0]-Q(1,4)-Q(1,3))

    def test_profile_embedding_does_not_preserve_function_addition(self):
        x,y,c=(Q(2),Q(5)),(Q(1),Q(-1)),Q(3)
        ordinary=tuple((a+c)+(b+c) for a,b in zip(x,y))
        intended=tuple(a+b+c for a,b in zip(x,y))
        self.assertNotEqual(ordinary,intended)
        self.assertEqual(tuple(a-b for a,b in zip(ordinary,intended)),(c,c))

    def test_front_pruning_preserves_all_tested_budgets(self):
        raw=((Q(0),Q(2)),(Q(2),Q(0)),(Q(3),Q(3)),(Q(0),Q(2)))
        a=Front(("error","work"),raw)
        self.assertEqual(len(a.points),2)
        for b in product(range(-1,5),repeat=2):
            self.assertEqual(a.feasible(b),any(leq(x,b) for x in raw))

    def test_front_cost_error_examples(self):
        a=Front(("error","work"),((Q(1,1000),Q(1)),(Q(0),Q(8))))
        self.assertTrue(a.feasible((Q(1,100),8)))
        b=Front(a.units,((Q(1,8),Q(1)),(Q(0),Q(8))))
        self.assertTrue(b.feasible((Q(1,100),8)))
        self.assertFalse(b.feasible((Q(1,100),2)))

    def test_nonconvex_budget_distinction_survives_equal_weighted_optima(self):
        a=Front(("e1","e2"),((Q(0),Q(2)),(Q(2),Q(0))))
        b=Front(a.units,a.points+((Q(3,2),Q(3,2)),))
        self.assertEqual(len(b.points),3)
        for i in range(101):
            w=(Q(i,100),1-Q(i,100))
            self.assertEqual(min(dot(w,x) for x in a.points),min(dot(w,x) for x in b.points))
        self.assertFalse(a.feasible((Q(3,2),Q(3,2))))
        self.assertTrue(b.feasible((Q(3,2),Q(3,2))))

    def test_mean_mixture_changes_per_use_budget_contract(self):
        a=Front(("e1","e2"),((Q(0),Q(2)),(Q(2),Q(0))))
        mean=tuple((x+y)/2 for x,y in zip(*a.points))
        self.assertTrue(leq(mean,(Q(3,2),Q(3,2))))
        self.assertFalse(a.feasible((Q(3,2),Q(3,2))))

    def test_front_intersection_means_separate_feasibility(self):
        a=Front(("x","y"),((Q(0),Q(2)),(Q(2),Q(0))))
        b=Front(a.units,((Q(1),Q(1)),))
        intersection=a.separate_budget_intersection(b)
        for budget in product(range(4),repeat=2):
            self.assertEqual(intersection.feasible(budget),a.feasible(budget) and b.feasible(budget))

    def test_front_algebra_including_empty_and_signed_costs(self):
        units=("x","y")
        fronts=[Front(units,()),Front(units,((Q(0),Q(0)),)),
                Front(units,((Q(0),Q(1)),(Q(1),Q(0)))),
                Front(units,((Q(-1),Q(2)),)),Front(units,((Q(2),Q(-1)),))]
        empty,zero=fronts[:2]
        for a in fronts:
            self.assertEqual(a.choice(a),a)
            self.assertEqual(a.choice(empty),a)
            self.assertEqual(a.independent_add(zero),a)
            self.assertEqual(a.independent_add(empty),empty)
        for a,b,c in product(fronts,repeat=3):
            self.assertEqual(a.independent_add(b).independent_add(c),a.independent_add(b.independent_add(c)))
            self.assertEqual(a.choice(b).independent_add(c),a.independent_add(c).choice(b.independent_add(c)))

    def test_signed_cost_identity_need_not_be_greatest(self):
        zero=Front(("cost",),((Q(0),),))
        rebate=Front(zero.units,((Q(-1),),))
        self.assertNotEqual(zero.choice(rebate),zero)

    def test_front_unit_guard(self):
        a=Front(("seconds",),((Q(1),),)); b=Front(("metres",),((Q(1),),))
        with self.assertRaises(ValueError): a.independent_add(b)
        with self.assertRaises(ValueError): a.feasible((1,2))

    def test_shared_control_breaks_independent_front_addition(self):
        marginal=Front(("cost",),((Q(0),),(Q(1),)))
        naive=marginal.independent_add(marginal)
        compatible=Front(marginal.units,tuple((Q(i+1-i),) for i in (0,1)))
        self.assertEqual(naive.points,((0,),))
        self.assertEqual(compatible.points,((1,),))

    def test_relation_preserves_endpoint_needed_by_suffix(self):
        first=ResourceRelation(("s",),("L","R"),("cost",),(Edge("s","L",(Q(0),)),Edge("s","R",(Q(1),))))
        last=ResourceRelation(first.outputs,("t",),first.units,(Edge("L","t",(Q(100),)),Edge("R","t",(Q(0),))))
        composed=first.then(last)
        self.assertEqual(composed.edges,(Edge("s","t",(Q(1),)),))
        prematurely_pruned=ResourceRelation(first.inputs,first.outputs,first.units,(first.edges[0],))
        self.assertEqual(prematurely_pruned.then(last).edges[0].cost,(100,))

    def test_relation_associativity_and_endpoint_guard(self):
        a=ResourceRelation(("s",),("L","R"),("cost",),(Edge("s","L",(Q(0),)),Edge("s","R",(Q(2),))))
        b=ResourceRelation(a.outputs,("t",),a.units,(Edge("L","t",(Q(3),)),Edge("R","t",(Q(0),))))
        c=ResourceRelation(b.outputs,("u",),a.units,(Edge("t","u",(Q(1),)),))
        self.assertEqual(a.then(b).then(c),a.then(b.then(c)))
        with self.assertRaises(ValueError): a.then(c)

    def test_positive_unit_scaling_preserves_budget_membership(self):
        a=Front(("x","y"),((Q(0),Q(2)),(Q(2),Q(0)),(Q(3,2),Q(3,2))))
        scales=(Q(100),Q(1,10))
        b=Front(("new-x","new-y"),tuple(tuple(x*s for x,s in zip(v,scales)) for v in a.points))
        for v in product(range(4),repeat=2):
            self.assertEqual(a.feasible(v),b.feasible(tuple(x*s for x,s in zip(v,scales))))


    def test_one_optimized_map_can_hide_different_mean_constraint_menus(self):
        for h in product(range(-3, 4), repeat=2):
            self.assertEqual(max(h), max(h[0], h[1], Q(h[0]+h[1], 2)))
        pure=Front(("mean-e1","mean-e2"),((Q(0),Q(2)),(Q(2),Q(0))))
        lottery=Front(pure.units,pure.points+((Q(1),Q(1)),))
        self.assertFalse(pure.feasible((1,1)))
        self.assertTrue(lottery.feasible((1,1)))

    def test_capability_per_task_is_not_one_universal_policy(self):
        tests=((Q(1),Q(0)),(Q(0),Q(1)))
        self.assertTrue(all(any(h[a]==max(h) for a in range(2)) for h in tests))
        self.assertFalse(any(all(h[a]==max(h) for h in tests) for a in range(2)))

    def test_robust_coordinate_front_is_exact_for_universal_caps(self):
        models=(((Q(0),Q(1)),(Q(1),Q(0))),
                ((Q(2),Q(0)),(Q(0),Q(2))))
        robust=Front(("c1","c2"),tuple(tuple(max(row[j] for row in action) for j in range(2)) for action in models))
        for budget in product(range(4),repeat=2):
            direct=any(all(leq(row,budget) for row in action) for action in models)
            self.assertEqual(robust.feasible(budget),direct)
        self.assertEqual(sum(max(row[j] for row in models[0]) for j in range(2)),2)
        self.assertEqual(max(sum(row) for row in models[0]),1)

    def test_robust_front_before_and_after_observation_differ(self):
        costs=((Q(0),Q(1)),(Q(1),Q(0)))
        before=min(max(a) for a in costs)
        after=max(min(costs[a][theta] for a in range(2)) for theta in range(2))
        self.assertEqual((before,after),(1,0))

    def test_subprobability_step_is_not_in_shift_preserving_candidate(self):
        with self.assertRaises(ValueError):
            Step(("s",),("t",),(Q(0),),((Q(1,2),),))
        self.assertNotEqual(Q(1,2)*(0+1), Q(1,2)*0+1)


def report(test_count: int) -> dict:
    return {
        "task": "F02", "status": "constructed finite candidate fixtures; no final calculus or held-out experiment",
        "test_count": test_count,
        "arithmetic": "exact fractions; no random seeds or floating-point tolerance",
        "cases": {
            "S_fixed_task_values": [str(-Q(2,1000)),str(-Q(8,1000))],
            "P_crossed_bottleneck": "-1", "P_aligned_bottleneck": "1", "additive_value_both": "2",
            "T_composed_value": "9/2", "T_signal_optional_value": "7/4",
            "T_shared_model_total": "1", "T_stagewise_lower_total": "0",
            "T_hidden_model_deterministic": "0", "T_revealed_model": "1", "T_fixed_model_half_mixture": "1/2",
            "G_AB_budget_feasible": False, "G_ABC_budget_feasible": True,
            "G_compatible_sequence_cost": "1", "G_premature_cost_pruning": "100",
            "equal_T_maps_pure_mean_budget_feasible": False, "equal_T_maps_lottery_mean_budget_feasible": True,
            "G_robust_before_observation_cost": "1", "G_robust_after_observation_cost": "0",
        },
        "enumeration_bounds": {
            "expectation_additivity": "81 profile pairs by 5 two-point weight vectors",
            "minimum_identity_and_equality": "625 profile pairs on {-2,-1,0,1,2}^2 with weights (1/3,2/3)",
            "uniform_bottleneck_bound": "6561 quadruples of two-coordinate profiles over {-1,0,1}",
            "span_bound": "15 three-point distributions with denominator 4; all 225 pairs; M in {0,1,3}; reward offsets in {-1,0,2}; all 8 box vertices",
            "weighted_fronts": "101 normalized nonnegative weight pairs, plus the analytic all-weight proof in the note",
            "front_algebra": "125 triples from 5 fronts including empty, zero, signed costs, and an incomparable front",
        },
        "limits": ["Finite checks do not prove unrestricted theorems.",
                   "Semantic assumptions about observations and compatibility are not automatically checked by these data types.",
                   "No F11 reasoner, F03 literature audit, or gate is completed by this suite."]
    }


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json",type=Path,help="Write deterministic result metadata only after all checks pass.")
    args=parser.parse_args()
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(F02CandidateTests))
    if not result.wasSuccessful(): return 1
    if args.json:
        args.json.parent.mkdir(parents=True,exist_ok=True)
        args.json.write_text(json.dumps(report(result.testsRun),indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return 0


if __name__=="__main__":
    raise SystemExit(main())
