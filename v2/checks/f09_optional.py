"""Bounded F09 geometry/grid/robustness/profile audits.

Research contributor: Codex (GPT-6), 2026-09-30. Finite reference calculations
supplement the written proofs. Only the explicitly returned native traces are
certificates; finite samples are never passed off as universal proof checking.
"""
from __future__ import annotations

from dataclasses import replace
from fractions import Fraction as F
from itertools import combinations, product
import random
import unittest

from v2.checks import f06_inference_rules as K
from v2.checks import f06_source_transport as T
from v2.checks import f07_soundness as H
from v2.checks import f08_unit_characterization as U
from v2.checks import f09_fragments as B
from v2.checks import f09_scaling as S


def lattice_value(formula, point):
    op,*args = formula
    if op == 'atom': return H.exact(point[args[0]])
    if op == 'const': return H.exact(args[0])
    if op == 'not': return 1-lattice_value(args[0],point)
    if op in ('min','max'):
        a,b = (lattice_value(x,point) for x in args)
        return min(a,b) if op == 'min' else max(a,b)
    raise H.AuditError('This exact-grid fragment excludes residual/addition/scaling.')


def lattice_data(formula):
    op,*args = formula
    if op == 'atom' and len(args) == 1: return {args[0]},set()
    if op == 'const' and len(args) == 1:
        q = H.exact(args[0])
        if not 0 <= q <= 1: raise H.AuditError('Grid constants must be in [0,1].')
        return set(),{q}
    if (op == 'not' and len(args) == 1) or (op in ('min','max') and len(args) == 2):
        pairs = [lattice_data(x) for x in args]
        return set().union(*(p[0] for p in pairs)),set().union(*(p[1] for p in pairs))
    raise H.AuditError('Unsupported exact-grid syntax.')


def grid_optimum(left,right):
    """B9's restricted cube calculation, no arbitrary Context input accepted."""
    ln,lc = lattice_data(left); rn,rc = lattice_data(right)
    names = tuple(sorted(ln|rn))
    if len(names) > 4: raise H.AuditError('This development audit is bounded to four atoms.')
    constants = lc|rc|{F(0),F(1,2),F(1)}
    grid = tuple(sorted(constants|{1-q for q in constants}))
    candidates = ((lattice_value(left,dict(zip(names,p)))-lattice_value(right,dict(zip(names,p))),p)
                  for p in product(grid,repeat=len(names)))
    value,point = max(candidates)
    return value,dict(zip(names,point)),grid


def boolean_defect(term):
    return K.minimum(K.absolute(term),K.absolute(K.sub(term,K.num(1))))


def two_rays_boolean_certificate():
    x,z = K.src('x'),K.num(0)
    sig = K.Signature('F09-two-ray-Boolean-v1',('U',),(('x','U'),))
    ctx = K.Context(sig,'fixed-visible-observation','r1',(
        K.Case('left',(K.Row(x,K.num(-1)),),(('x',F(-1)),)),
        K.Case('right',(K.Row(K.num(1),x),),(('x',F(1)),))))
    raw = K.scale(F(1,2),K.add(x,K.num(1)))
    hinge = K.maximum(raw,z)
    term = K.minimum(K.num(1),hinge)
    defect = boolean_defect(term)
    outer,roots = K.Builder(ctx),[]
    for case,bit in (('left',F(0)),('right',F(1))):
        builder = K.Builder(ctx,case)
        if bit == 0:
            raw_upper = U.affine_certificate(ctx,case,raw,z,F(0),(F(1,2),))
            hinge_upper = builder.congruence('max',T._copy_into(builder,raw_upper),builder.constant(z,z))
            hinge_upper = builder.rewrite(hinge_upper,hinge,z)
            upper = builder.trans(builder.lattice('min_right',K.num(1),hinge),hinge_upper)
            lower = builder.min_common(builder.constant(z,K.num(1)),builder.lattice('max_right',raw,z))
        else:
            raw_lower = U.affine_certificate(ctx,case,K.num(1),raw,F(0),(F(1,2),))
            hinge_lower = builder.trans(T._copy_into(builder,raw_lower),builder.lattice('max_left',raw,z))
            lower = builder.min_common(builder.constant(K.num(1),K.num(1)),hinge_lower)
            upper = builder.lattice('min_left',K.num(1),hinge)
        upper = builder.rewrite(upper,term,K.num(bit))
        lower = builder.rewrite(lower,K.num(bit),term)
        _,root,_ = B._point_equality(builder,defect,(),{}, {term:(bit,upper,lower)})
        local = T.prune(ctx,builder.proof(root))
        roots.append(T._copy_into(outer,local))
    root = outer.all_cases(roots)
    proof = outer.proof(root)
    expected = H.request(ctx,None,defect,z,F(0))
    H.receive(ctx,proof,expected)
    return ctx,proof,expected


def typed_refinement_fixture():
    x = K.src('x')
    sig = K.Signature('F09-typed-refinement-v1',('U','V'),(('x','U'),),
                      (K.Conversion('out','U','V',F(1)),))
    rows = (K.Row(x,K.num(10)),K.Row(K.convert('out',x),K.num(-1,'V')))
    old = K.Context(sig,'fixed-visible-observation','r1',(K.Case('h',rows,(('x',F(-1)),)),))
    new = replace(old,revision='sign-refined',cases=(replace(old.cases[0],rows=rows+(K.Row(x,K.num(0)),)),))
    builder = K.Builder(new,'h'); builder.rewrite(builder.row(2),x,K.num(0))
    proof = builder.proof()
    expected = H.request(new,'h',x,K.num(0),F(0))
    H.receive(new,proof,expected)
    return old,new,proof,expected


def convex_conflict_certificate():
    x,y,z = K.src('x'),K.src('y'),K.num(0)
    ctx = K.context(('x','y'),(),{'x':F(-1,3),'y':F(-1,3)},scope='F09-convex-conflict-v1')
    a,b,c = K.scale(-1,x),K.scale(-1,y),K.add(K.add(x,y),K.num(1))
    pair = K.maximum(a,b); joint = K.maximum(pair,c)
    builder = K.Builder(ctx,'h')
    left = builder.lattice('max_left',pair,c)
    roots = (builder.trans(builder.lattice('max_left',a,b),left),
             builder.trans(builder.lattice('max_right',a,b),left),
             builder.lattice('max_right',pair,c))
    average = builder.add(builder.add(builder.scale(F(1,3),roots[0]),builder.scale(F(1,3),roots[1])),
                          builder.scale(F(1,3),roots[2]))
    average = builder.rewrite(average,K.num(F(1,3)),joint)
    root = builder.trans(builder.constant(z,K.num(F(1,3))),average)
    proof = builder.proof(root)
    expected = H.request(ctx,'h',z,joint,F(-1,3))
    H.receive(ctx,proof,expected)
    return ctx,proof,expected


def subsets(indices):
    indices = tuple(indices)
    return (frozenset(c) for n in range(len(indices)+1) for c in combinations(indices,n))


def profile_summary(points):
    """Exact finite-domain observation summary, not a general feasibility solver."""
    points = tuple(tuple(H.exact(v) for v in p) for p in points)
    if not points or not points[0] or any(len(p)!=len(points[0]) for p in points):
        raise H.AuditError('A nonempty rectangular table of finite source values is required.')
    indices = tuple(range(len(points[0])))
    supported = frozenset(i for i in indices if all(p[i] <= 0 for p in points))
    conflicts = []
    for required in subsets(indices):
        if required and not any(all(p[i] <= 0 for i in required) for p in points):
            if not any(previous <= required for previous in conflicts): conflicts.append(required)
    return supported,frozenset(conflicts)


def realization(n,supported,conflicts):
    indices = frozenset(range(n)); supported = frozenset(supported)
    conflicts = frozenset(frozenset(c) for c in conflicts)
    if (not supported <= indices or any(not c or not c <= indices or c & supported for c in conflicts)
            or any(a < b for a in conflicts for b in conflicts)):
        raise H.AuditError('Invalid supported set or conflict antichain.')
    points = []
    for possible in subsets(indices-supported):
        if not any(c <= possible for c in conflicts):
            accepted = supported|possible
            points.append(tuple(F(0) if i in accepted else F(1) for i in range(n)))
    return tuple(points)


class F09OptionalTests(unittest.TestCase):
    def test_two_ray_boolean_defect_has_native_certificate(self):
        ctx,proof,expected = two_rays_boolean_certificate()
        self.assertEqual(H.receive(ctx,proof,expected).budget,0)
        for case in ctx.cases:
            self.assertEqual(H.value(expected.new,ctx.signature,dict(case.witness)),0)

    def test_foreign_ray_rows_cannot_certify_boolean_at_target(self):
        ctx,_,expected = two_rays_boolean_certificate()
        sig = replace(ctx.signature,units=('U','V'),conversions=(K.Conversion('out','U','V',F(1)),))
        cases = tuple(replace(h,rows=tuple(K.Row(K.convert('out',r.lhs),K.convert('out',r.rhs)) for r in h.rows)) for h in ctx.cases)
        foreign = replace(ctx,signature=sig,cases=cases)
        point = {'x':F(0)}
        reduct = U.unit_reduct(foreign,'U')
        self.assertFalse(any(H.case_feasible(foreign,h.name,point) for h in foreign.cases))
        self.assertTrue(H.case_feasible(reduct,'left',point))
        self.assertEqual(H.value(expected.new,sig,point),F(1,2))

    def test_separated_rounding_and_error(self):
        for epsilon in (F(0),F(1,10),F(1,3),F(49,100)):
            for bit,k in product((F(0),F(1)),range(-10,11)):
                t = bit+epsilon*F(k,10)
                rounded = min(F(1),max((t-epsilon)/(1-2*epsilon),F(0)))
                self.assertEqual(rounded,bit)
                self.assertLessEqual(abs(t-rounded),epsilon)

    def test_rounding_half_threshold_has_no_constant_solution(self):
        for bit in (F(0),F(1)):
            self.assertGreater(max(abs(x-bit) for x in (F(0),F(1))),F(1,2))

    def test_residual_amplification_exact(self):
        epsilon = F(1,1000)
        for k in range(1,13):
            value = 1-epsilon
            for _ in range(k): value = max(2*value-1,F(0))
            self.assertEqual(1-value,min(2**k*epsilon,F(1)))

    def test_grid_optima_against_distinct_dense_reference(self):
        rng = random.Random(909)
        leaves = (('atom','x'),('atom','y'),('const',F(0)),('const',F(1)),('const',F(1,3)))
        def make(depth):
            if depth == 0 or rng.randrange(3)==0: return rng.choice(leaves)
            op = rng.choice(('not','min','max'))
            return (op,make(depth-1)) if op=='not' else (op,make(depth-1),make(depth-1))
        for _ in range(24):
            left,right = make(4),make(4)
            optimum,point,_ = grid_optimum(left,right)
            dense = max(lattice_value(left,{'x':F(x,12),'y':F(y,12)})-
                        lattice_value(right,{'x':F(x,12),'y':F(y,12)}) for x,y in product(range(13),repeat=2))
            self.assertEqual(optimum,dense)
            self.assertEqual(lattice_value(left,point)-lattice_value(right,point),optimum)

    def test_half_grid_needed_for_complement(self):
        x = ('atom','x'); middle = ('min',x,('not',x))
        self.assertEqual(grid_optimum(middle,('const',F(0)))[0],F(1,2))
        self.assertEqual(max(lattice_value(middle,{'x':F(k)}) for k in (0,1)),0)

    def test_grid_interface_rejects_residual_and_correlated_contexts(self):
        with self.assertRaises(H.AuditError): grid_optimum(('res',('atom','x'),('const',F(1))),('const',F(0)))
        grid = (F(0),F(1,2),F(1))
        self.assertEqual(max(min(x,y) for x,y in product(grid,repeat=2) if x+y<=F(1,2)),0)
        self.assertEqual(min(F(1,4),F(1,4)),F(1,4))

    def test_no_fixed_grid_residual_family_exact_witnesses(self):
        for grid in ((F(0),F(1,2),F(1)),tuple(F(k,17) for k in range(18)),(F(0),)):
            positive = [x for x in grid if x>0]
            n = 2 if not positive else max(2,(1/min(positive)).__ceil__())
            f = lambda x:min(x,max(1-n*x,F(0)))
            self.assertTrue(all(f(x)==0 for x in grid))
            self.assertEqual(f(F(1,n+1)),F(1,n+1))

    def test_joint_profile_summary_and_realization(self):
        examples = ((4,{0},({1,2},{2,3})),(3,set(),({0},{1,2})),(3,{0,1,2},()))
        for n,supported,conflicts in examples:
            points = realization(n,supported,conflicts)
            actual_s,actual_f = profile_summary(points)
            self.assertEqual(actual_s,frozenset(supported))
            self.assertEqual(actual_f,frozenset(map(frozenset,conflicts)))
            for required in subsets(range(n)):
                if not required: continue
                expected = (B.P.AtomValue.SUPPORTED if required <= actual_s else
                            B.P.AtomValue.REFUTED if any(c<=required for c in actual_f) else B.P.AtomValue.OPEN)
                self.assertEqual(B.status(max(p[i] for i in required) for p in points),expected)

    def test_arbitrary_high_order_conflict_in_two_dimensions(self):
        for k in range(2,8):
            margins = tuple(tuple(F(1,2)-(j-i)**2 for i in range(1,k+1)) for j in range(1,k+1))
            supported,conflicts = profile_summary(margins)
            self.assertEqual(supported,frozenset())
            self.assertEqual(conflicts,frozenset((frozenset(range(k)),)))
            self.assertTrue(all(max(p)==F(1,2) for p in margins))
            self.assertTrue(all(B.status(p[i] for p in margins)==B.P.AtomValue.OPEN for i in range(k)))

    def test_convex_dimension_bound_sharp_fixture_native(self):
        ctx,proof,expected = convex_conflict_certificate()
        self.assertEqual(H.receive(ctx,proof,expected).budget,F(-1,3))
        point = {'x':F(-1,3),'y':F(-1,3)}
        self.assertEqual(H.value(expected.new,ctx.signature,point)-H.value(expected.old,ctx.signature,point),F(-1,3))
        for x,y in ((F(-2),F(0)),(F(0),F(-2)),(F(0),F(0))):
            self.assertEqual(sum(v<=0 for v in (-x,-y,x+y+1)),2)

    def test_typed_case_pruning_changes_native_information(self):
        old,new,proof,expected = typed_refinement_fixture()
        self.assertEqual(H.receive(new,proof,expected).budget,0)
        point = {'x':F(1)}
        self.assertTrue(H.case_feasible(U.unit_reduct(old,'U'),'h',point))
        self.assertFalse(H.case_feasible(U.unit_reduct(new,'U'),'h',point))
        for x in (F(-10),F(-1),F(0),F(1),F(10)):
            self.assertEqual(H.case_feasible(old,'h',{'x':x}),H.case_feasible(new,'h',{'x':x}))

    def test_common_offset_blind_trace_map_also_fails(self):
        x = K.src('x'); zero = K.num(0)
        ctx = K.context(('x',),(),{'x':F(0)})
        builder = K.Builder(ctx,'h')
        builder.constant(K.residual(x,zero),K.maximum(K.scale(-1,x),zero))
        proof = builder.proof(); K.check(ctx,proof)
        presentation = S.Presentation(ctx.signature,{'U':F(1)},{'U':F(1)})
        new,candidate = S._relabel_proof(ctx,proof,presentation)
        with self.assertRaises(K.ProofError): K.check(new,candidate)
        root = candidate.steps[candidate.root]
        for x in (F(-2),F(0),F(1),F(3)):
            self.assertEqual(H.value(root.new,new.signature,{'x':x}),H.value(root.old,new.signature,{'x':x}))

    def test_exact_hinge_modulus_both_signs(self):
        h = lambda x:x+min(max(x,F(0)),F(1))
        for budget in (F(-3),F(-1,4),F(0),F(1,4),F(3)):
            candidates = {F(0),F(1),-budget,1-budget,F(-10),F(10)}
            self.assertEqual(max(h(x+budget)-h(x) for x in candidates),
                             budget+min(max(budget,F(0)),F(1)))

    def test_composed_optimal_moduli_can_lose_alignment(self):
        g = lambda x:x+min(max(x,F(0)),F(1))
        h = lambda y:y+min(max(y-10,F(0)),F(1))
        budget = F(1,4)
        candidates = {F(0),F(1),F(9),F(10)}
        candidates |= {x-budget for x in tuple(candidates)}
        self.assertEqual(max(h(g(x+budget))-h(g(x)) for x in candidates),F(1,2))
        self.assertEqual(2*(2*budget),1)


if __name__ == '__main__': unittest.main()
