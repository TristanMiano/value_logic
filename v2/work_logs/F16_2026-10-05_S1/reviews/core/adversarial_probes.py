"""F16 bounded core witnesses; run from the repository root.

No test discovery, source mutation, neural work, or semantic decision oracle.
These probes supplement the mathematical reconstruction in the two review notes.
"""
from dataclasses import replace
from fractions import Fraction as F
import json

from v2.checks import f06_inference_rules as K
from v2.checks import f07_soundness as A
from v2.checks import f06_derived_cases as D


def rejected(operation):
    try:
        operation()
    except (K.SemanticError, K.ProofError, A.AuditError) as error:
        return {"rejected": True, "exception": type(error).__name__, "reason": str(error)}
    raise AssertionError("The intentionally invalid operation was accepted.")


def run():
    result = {}
    ctx = K.context(("x",), (), {"x": 1})
    b = K.Builder(ctx)
    b.constant(K.num(0), K.num(0))
    proof = b.proof()
    root = K.check(ctx, proof)
    assert root.budget == 0
    good = A.request(ctx, None, K.num(0), K.num(0), 0)
    assert A.receive(ctx, proof, good) == root
    result["independent_current_request"] = {
        "valid_trace_budget": str(root.budget),
        "different_requested_gap_at_x1": "1",
        "wrong_pair": rejected(lambda: A.receive(
            ctx, proof, A.request(ctx, None, K.src("x"), K.num(0), 0))),
        "wrong_unit": rejected(lambda: A.receive(ctx, proof, replace(good, unit="V"))),
        "stale_request": rejected(lambda: A.receive(
            replace(ctx, revision="v2"), proof, good)),
    }

    ctx = K.context(("x",), (K.Row(K.src("x"), K.num(1)),), {"x": 1})
    b = K.Builder(ctx, "h")
    b.rewrite(b.row(0), K.src("x"), K.num(0))
    result["insufficient_strength"] = rejected(lambda: A.receive(
        ctx, b.proof(), A.request(ctx, "h", K.src("x"), K.num(0), 0)))

    sig = K.Signature("unused-foreign-let", ("U", "V"), (("v", "V"),))
    ctx = K.Context(sig, "o", "v1", (K.Case("h", (), (("v", F(41)),)),))
    term = K.let("dead", K.src("v"), K.num(0, "U"))
    assert K.infer(term, sig) == "U"
    assert K.evaluate(term, sig, {"v": 41}) == 0
    b = K.Builder(ctx, "h")
    b.constant(term, K.num(0))
    result["unused_foreign_let"] = {
        "result_unit": "U", "foreign_source_unit": "V", "conversion_edges": [],
        "value_at_v41": "0", "checked_budget": str(K.check(ctx, b.proof()).budget),
        "corrects": "Initial note section 6 syntactic-leaf overstatement only.",
    }

    ctx = K.context((("a", "V"), ("b", "V")), (), {"a": 1, "b": -1},
                    units=("V", "U"), conversions=(K.Conversion("c", "V", "U", F(2)),))
    a, c, k = K.src("a"), K.src("b"), F(2)
    b = K.Builder(ctx, "h")
    i = b.conversion("c", b.lattice("min_left", a, c))
    j = b.conversion("c", b.lattice("min_right", a, c))
    forward = b.min_common(i, j)
    i = b.scale(1/k, b.lattice("min_left", K.scale(k, a), K.scale(k, c)))
    j = b.scale(1/k, b.lattice("min_right", K.scale(k, a), K.scale(k, c)))
    backward = b.scale(1/k, b.conversion("c", b.scale(k, b.min_common(i, j))))
    backward = b.rewrite(backward, K.minimum(K.convert("c", a), K.convert("c", c)),
                         K.convert("c", K.minimum(a, c)))
    assert K.check(ctx, b.proof(forward)).budget == 0
    assert K.check(ctx, b.proof(backward)).budget == 0
    result["forward_conversion_lattice"] = {"factor": "2", "directions": 2,
                                               "budget_each": "0", "nodes": len(b.steps)}

    sig = K.Signature("incoherent-cycle", ("U", "V"), (("x", "U"),),
                      (K.Conversion("up", "U", "V", F(2)),
                       K.Conversion("down", "V", "U", F(3))))
    ctx = K.Context(sig, "o", "v1", (K.Case("h", (), (("x", F(1)),)),))
    term = K.convert("down", K.convert("up", K.src("x")))
    result["conversion_cycle_is_not_identity"] = {
        "value_at_x1": str(K.evaluate(term, sig, {"x": 1})),
        "false_identity": rejected(lambda: K.Builder(ctx, "h").constant(term, K.src("x"))),
    }

    ns = tuple("n1 n2 o1 o2 t1 t2".split())
    n1, n2, o1, o2, t1, t2 = map(K.src, ns)
    rows = (K.Row(K.sub(K.sub(n1, o1), t1), K.num(F(-3, 4))),
            K.Row(K.add(K.sub(n2, o2), t2), K.num(F(1, 4))))
    point = {"n1": F(1, 4), "n2": F(1, 4), "o1": 0, "o2": 0, "t1": 1, "t2": 0}
    ctx = K.context(ns, rows, point)
    b = K.Builder(ctx, "h")
    b.rewrite(b.add(b.row(0), b.row(1)), K.add(n1, n2), K.add(o1, o2))
    result["unshared_component_cancellation"] = {
        "feasible_combined_gap": str(K.evaluate(K.sub(K.add(n1, n2), K.add(o1, o2)),
                                               ctx.signature, point)),
        "bad_rewrite": rejected(lambda: K.check(ctx, b.proof())),
    }

    sig = K.Signature("local-extension", ("U",), (("x", "U"),))
    case0 = K.Case("h0", (K.Row(K.src("x"), K.num(0)),), (("x", F(0)),))
    old = K.Context(sig, "o", "v1", (case0,))
    b = K.Builder(old, "h0")
    b.rewrite(b.row(0), K.src("x"), K.num(0))
    case1 = K.Case("h1", (K.Row(K.src("x"), K.num(1)),), (("x", F(1)),))
    new = K.Context(sig, "o", "v2", (case0, case1))
    extended = K.Proof(tuple(replace(s, context_id=K.fingerprint(new)) for s in b.steps), 1)
    local = A.request(new, "h0", K.src("x"), K.num(0), 0)
    assert A.receive(new, extended, local).budget == 0
    global_request = A.request(new, None, K.src("x"), K.num(0), 0)
    b2 = K.Builder(new, "h0")
    b2.steps = list(extended.steps)
    b2.all_cases([extended.root])
    result["local_extension_and_union"] = {
        "same_case_extension": "accepted as local h0 only",
        "feasible_h1_countermodel_gap": "1",
        "global_request": rejected(lambda: A.receive(new, extended, global_request)),
        "missing_case": rejected(lambda: K.check(new, b2.proof())),
    }

    result["vacuity"] = {
        "empty_case_list": rejected(lambda: K.Context(sig, "o", "v1", ()).validate()),
        "inconsistent_live_case": rejected(lambda: K.context(
            ("x",), (K.Row(K.src("x"), K.num(0)), K.Row(K.num(1), K.src("x"))), {"x": 0})),
    }

    ctx = K.context(("x", "y"), (), {"x": 0, "y": 0})
    b = K.Builder(ctx, "h")
    left, right = K.src("x"), K.maximum(K.src("y"), K.num(0))
    proof = D.finish(b, D.positive_min(b, left, right))
    root = K.check(ctx, proof)
    assert root.budget == 0
    assert all(s.rule != "row" for s in proof.steps)
    result["generic_positive_min_nonlinear_instantiation"] = {
        "budget": str(root.budget), "nodes": len(proof.steps),
        "source_row_reads": 0, "all_tags_native": all(s.rule in A.NATIVE_RULES for s in proof.steps),
        "substituted_second_argument": "max(y,0)",
    }

    return result


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
