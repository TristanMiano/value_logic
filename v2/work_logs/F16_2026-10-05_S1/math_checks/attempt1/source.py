"""Bounded exact F16 mathematical checks, independent of experiment modules.

Contributor: ChatGPT (GPT-6 Astra Pro). See prospective design.json.
This creates no scientific preparation/evaluation population or neural model.
"""

from __future__ import annotations

import datetime as dt
from fractions import Fraction as Q
import hashlib
import importlib.metadata
import itertools as it
import json
from math import comb
import os
from pathlib import Path
import platform
import resource
import sys
import time
import traceback


HERE = Path(__file__).resolve().parent
SESSION = HERE.parent
REPO = HERE.parents[3]
DESIGN = HERE / "design.json"
SAVED = SESSION / "reviews/price/coherent_center_search/attempt1/records.jsonl"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strings(value):
    if isinstance(value, Q):
        return str(value)
    if isinstance(value, dict):
        return {str(k): strings(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [strings(v) for v in value]
    return value


def dot(a, b):
    return sum((x * y for x, y in zip(a, b, strict=True)), Q(0))


def level_costs(k, penalty):
    return tuple(Q(k + 1, k + 1 - h) for h in range(k)) + (Q(k) + penalty,)


def reach_values(k, r):
    return tuple(Q(comb(h, r), comb(k, r)) if h >= r else Q(0)
                 for h in range(k + 1))


def level_vertices(k, penalty, mean):
    costs = level_costs(k, penalty)
    out = set()
    for i, value in enumerate(costs):
        if value == mean:
            q = [Q(0)] * (k + 1)
            q[i] = Q(1)
            out.add(tuple(q))
    for i, j in it.combinations(range(k + 1), 2):
        if costs[i] <= mean <= costs[j]:
            q = [Q(0)] * (k + 1)
            q[j] = (mean - costs[i]) / (costs[j] - costs[i])
            q[i] = 1 - q[j]
            out.add(tuple(q))
    assert out, (k, penalty, mean)
    return sorted(out)


def canonical_center(k, penalty, mean):
    costs = level_costs(k, penalty)
    end = [Q(0)] * (k + 1)
    end[k] = (mean - 1) / (costs[k] - 1)
    end[0] = 1 - end[k]
    adj = [Q(0)] * (k + 1)
    for i in range(k):
        if costs[i] <= mean <= costs[i + 1]:
            adj[i + 1] = (mean - costs[i]) / (costs[i + 1] - costs[i])
            adj[i] = 1 - adj[i + 1]
            break
    else:
        raise AssertionError((k, penalty, mean))
    return tuple((x + y) / 2 for x, y in zip(end, adj, strict=True))


def compositions(n, length):
    if length == 1:
        yield (n,)
        return
    for first in range(n + 1):
        for tail in compositions(n - first, length - 1):
            yield (first,) + tail


def moment(law, subset):
    return sum((p for w, p in enumerate(law) if w & subset == subset), Q(0))


def costs_by_world(order, prices, penalty):
    """Direct stopped execution, independent of the moment-cost expansion."""
    values = []
    for w in range(1 << len(prices)):
        total = Q(0)
        for procedure in order:
            total += prices[procedure]
            if not (w & (1 << procedure)):
                break
        else:
            total += penalty
        values.append(total)
    return tuple(values)


def k3_fiber(law, penalty):
    coeff = (
        (-3 + 1 / penalty, 3 + 1 / penalty),
        (1 - 1 / penalty, -2 - 1 / penalty),
        (1 / penalty, 1 + 1 / penalty),
        (-1 / penalty, -1 / penalty),
    )
    rows = [(p, *coeff[w.bit_count()]) for w, p in enumerate(law)]
    vertices = set()
    for (p, a, b), (q, c, d) in it.combinations(rows, 2):
        det = a * d - b * c
        if det:
            u, v = (-p * d + b * q) / det, (-a * q + p * c) / det
            if all(x + y * u + z * v >= 0 for x, y, z in rows):
                vertices.add((u, v))
    assert vertices
    vertices = sorted(vertices)
    u_mid = (min(u for u, _ in vertices) + max(u for u, _ in vertices)) / 2
    v_mid = (min(v for _, v in vertices) + max(v for _, v in vertices)) / 2

    def decode(u, v):
        return tuple(p + a * u + b * v for p, a, b in rows)

    midpoint_law = decode(u_mid, v_mid)
    vertex_laws = [decode(u, v) for u, v in vertices]
    dimension = 0
    if len(vertices) > 1:
        dimension = 1
        u0, v0 = vertices[0]
        if any((u - u0) * (b - v0) != (a - u0) * (v - v0)
               for (u, v), (a, b) in it.combinations(vertices[1:], 2)):
            dimension = 2
    return vertices, vertex_laws, midpoint_law, dimension


def canonical_from_law(law, k, penalty):
    # Within-level contrasts determine these residues without retaining a law.
    minima = [min(p for w, p in enumerate(law) if w.bit_count() == h)
              for h in range(k + 1)]
    residues = tuple(p - minima[w.bit_count()] for w, p in enumerate(law))
    residual_mass = 1 - sum(residues)
    assert residual_mass >= 0
    if residual_mass == 0:
        return residues, Q(0), None
    costs = level_costs(k, penalty)
    old_average = sum((p * costs[w.bit_count()] for w, p in enumerate(law)), Q(0))
    fixed_average = sum((p * costs[w.bit_count()] for w, p in enumerate(residues)), Q(0))
    mean = (old_average - fixed_average) / residual_mass
    q = canonical_center(k, penalty, mean)
    candidate = tuple(p + residual_mass * q[w.bit_count()] / comb(k, w.bit_count())
                      for w, p in enumerate(residues))
    return candidate, residual_mass, mean


def check_k3(emit):
    count = 0
    dimensions = {0: 0, 1: 0, 2: 0}
    nonexchangeable = 0
    prices = (Q(1),) * 3
    for penalty in map(Q, ("1/10", "1", "4", "16")):
        orders = list(it.permutations(range(3)))
        old_costs = [costs_by_world(order, prices, penalty) for order in orders]
        edits = [(edited, epsilon, order,
                  costs_by_world(order, tuple(1 + epsilon if j == edited else Q(1)
                                              for j in range(3)), penalty))
                 for edited in range(3) for epsilon in (Q(-1, 10), Q(1, 10))
                 for order in orders]
        for denominator in (1, 2, 3):
            for weights in compositions(denominator, 8):
                law = tuple(Q(w, denominator) for w in weights)
                vertices, laws, middle, dim = k3_fiber(law, penalty)
                assert sum(middle) == 1 and min(middle) >= 0
                assert all(sum(p) == 1 and min(p) >= 0 for p in laws)
                old = [dot(law, c) for c in old_costs]
                assert [dot(middle, c) for c in old_costs] == old
                assert all([dot(p, c) for c in old_costs] == old for p in laws)
                intervals = {}
                for subset in range(1, 7):
                    values = [moment(p, subset) for p in laws]
                    lo, hi = min(values), max(values)
                    intervals[subset] = (lo, hi)
                    assert moment(middle, subset) == (lo + hi) / 2
                    assert hi - lo <= (2 * penalty + 1) / (3 * (penalty + 2))
                candidate, residual_mass, mean = canonical_from_law(law, 3, penalty)
                assert sum(candidate) == 1 and min(candidate) >= 0
                assert [dot(candidate, c) for c in old_costs] == old
                radius = max(hi - lo for lo, hi in intervals.values()) / 2
                singleton_radius = (intervals[1][1] - intervals[1][0]) / 2
                assert radius == singleton_radius
                candidate_radius = max(max(moment(candidate, subset) - lo,
                                           hi - moment(candidate, subset))
                                       for subset, (lo, hi) in intervals.items())
                assert candidate_radius == radius
                for edited, epsilon, order, costs in edits:
                    values = [dot(p, costs) for p in laws]
                    assert dot(middle, costs) == (min(values) + max(values)) / 2
                    assert max(abs(dot(candidate, costs) - v) for v in values) <= abs(epsilon) * radius
                unequal = any(len({law[w] for w in range(8) if w.bit_count() == h}) > 1
                              for h in range(4))
                nonexchangeable += int(unequal)
                dimensions[dim] += 1
                emit({"family": "k3_nonexchangeable_fibers", "M": penalty,
                      "denominator": denominator, "weights": weights,
                      "fiber_dimension": dim, "nonexchangeable": unequal,
                      "vertices_uv": vertices, "proper_midpoint_law": middle,
                      "proper_intervals": intervals, "canonical_law": candidate,
                      "residual_mass": residual_mass, "residual_mean": mean,
                      "common_radius": radius, "edited_query_checks": len(edits),
                      "status": "pass"})
                count += 1
    assert count == 656
    return {"records": count, "dimensions": dimensions,
            "nonexchangeable_records": nonexchangeable,
            "direct_edited_order_checks": count * 36}


def check_saved(emit):
    count = 0
    for line in SAVED.read_text().splitlines():
        saved = json.loads(line)
        k, penalty, mean = saved["k"], Q(saved["M"]), Q(saved["mu"])
        candidate = tuple(map(Q, saved["candidate"]))
        assert len(candidate) == k + 1 and min(candidate) >= 0 and sum(candidate) == 1
        assert dot(candidate, level_costs(k, penalty)) == mean
        assert candidate == canonical_center(k, penalty, mean)
        vertices = level_vertices(k, penalty, mean)
        intervals, values = [], []
        for r in range(1, k):
            function = reach_values(k, r)
            vertex_values = [dot(v, function) for v in vertices]
            intervals.append((min(vertex_values), max(vertex_values)))
            values.append(dot(candidate, function))
        assert strings(intervals) == saved["intervals"]
        assert strings(values) == saved["candidate_values"]
        radius = max(hi - lo for lo, hi in intervals) / 2
        singleton_radius = (intervals[0][1] - intervals[0][0]) / 2
        actual_radius = max(max(value - lo, hi - value)
                            for value, (lo, hi) in zip(values, intervals, strict=True))
        assert radius == singleton_radius == actual_radius
        assert radius == Q(saved["free_radius"]) == Q(saved["singleton_half_width"])
        assert actual_radius == Q(saved["candidate_radius"])
        assert len(vertices) == saved["vertex_count"]
        emit({"family": "saved_candidate_certificates", "source_record": count,
              "k": k, "M": penalty, "mean": mean,
              "vertices_checked": len(vertices), "common_radius": radius,
              "status": "pass"})
        count += 1
    assert count == 735
    return {"records": count, "saved_input_sha256": digest(SAVED)}


def check_global(emit):
    count = 0
    for k in range(2, 11):
        for penalty in map(Q, ("0", "1/10", "1", "4", "16")):
            costs = level_costs(k, penalty)
            diameters = []
            for r in range(1, k):
                function = reach_values(k, r)
                gaps = []
                for i, j, ell in it.combinations(range(k + 1), 3):
                    chord = ((costs[ell] - costs[j]) * function[i]
                             + (costs[j] - costs[i]) * function[ell]) / (costs[ell] - costs[i])
                    gaps.append(abs(function[j] - chord))
                diameters.append(max(gaps))
            c = k + penalty - 1
            singleton = [Q(j, k) - Q(j) / ((k - j + 1) * c) for j in range(1, k)]
            maximum = max(singleton)
            assert diameters[0] == max(diameters) == maximum
            selected_s = next((s for s in range(2, k + 1) if c * s * (s + 1) >= k * (k + 1)), k)
            selected_j = k + 1 - selected_s
            assert singleton[selected_j - 1] == maximum
            emit({"family": "global_radius_formula", "k": k, "M": penalty,
                  "prefix_diameters": diameters, "singleton_formula": maximum,
                  "selected_j": selected_j, "status": "pass"})
            count += 1
    assert count == 45
    return {"records": count}


def check_boundaries(emit):
    level = tuple(Q(x, 816) for x in (275, 135, 333, 73))
    proper = [dot(level, reach_values(3, r)) for r in (1, 2)]
    assert sum(level) == 1 and min(level) >= 0
    assert dot(level, level_costs(3, Q(4))) == 2
    assert proper == [Q(5, 12), Q(23, 102)]
    top_values = [q[3] for q in level_vertices(3, Q(4), Q(2))]
    top_midpoint = (min(top_values) + max(top_values)) / 2
    assert top_midpoint == Q(1, 12) != level[3]
    emit({"family": "exact_boundary_witnesses", "id": "k3_terminal",
          "level_law": level, "proper_moments": proper,
          "terminal_value": level[3], "terminal_midpoint": top_midpoint,
          "status": "pass"})

    k, penalty, mean = 4, Q(1, 10), Q(9, 8)
    prefix_midpoints = [Q(41, 496), Q(1, 48), Q(5, 248)]
    terminal = (mean - 1 - sum(prefix_midpoints)) / penalty
    assert terminal == Q(5, 372)
    # Inclusion-exclusion for one specified exact two-failure world.
    bad_mass = prefix_midpoints[1] - 2 * prefix_midpoints[2] + terminal
    assert bad_mass == Q(-3, 496)
    emit({"family": "exact_boundary_witnesses", "id": "k4_midpoint_negative_mass",
          "proper_midpoints": prefix_midpoints, "terminal_forced": terminal,
          "two_failure_world_mass": bad_mass, "status": "pass"})

    center = canonical_center(k, penalty, mean)
    assert center == (Q(181, 248), Q(1, 4), Q(0), Q(0), Q(5, 248))
    values = [dot(center, reach_values(k, r)) for r in range(1, k)]
    assert values == [Q(41, 496), Q(5, 248), Q(5, 248)]
    intervals = []
    for r in range(1, k):
        vals = [dot(v, reach_values(k, r)) for v in level_vertices(k, penalty, mean)]
        intervals.append((min(vals), max(vals)))
    radius = max(max(value - lo, hi - value)
                 for value, (lo, hi) in zip(values, intervals, strict=True))
    assert radius == Q(21, 496)
    assert values[1] - prefix_midpoints[1] == Q(-1, 1488)
    emit({"family": "exact_boundary_witnesses", "id": "k4_coherent_common_radius",
          "level_law": center, "proper_moments": values,
          "common_radius": radius, "status": "pass"})
    return {"records": 3}


def main():
    out = HERE / "attempt1"
    out.mkdir(exist_ok=False)
    start = dt.datetime.now(dt.timezone.utc).isoformat()
    clock = time.monotonic_ns()
    initial_usage = resource.getrusage(resource.RUSAGE_SELF)
    env = {key: os.environ.get(key) for key in
           ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS")}
    manifest = {"id": "F16-MATH-01-attempt1", "start_utc": start,
                "scope": "bounded exact mathematical verification, not frozen experiment execution",
                "python": sys.version, "implementation": platform.python_implementation(),
                "platform": platform.platform(), "numpy": importlib.metadata.version("numpy"),
                "single_thread_environment": env, "argv": sys.argv,
                "source_sha256": digest(Path(__file__)), "design_sha256": digest(DESIGN),
                "saved_input_sha256": digest(SAVED)}
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (out / "source.py").write_bytes(Path(__file__).read_bytes())
    summary = {"status": "running", "families": {}, "completed_records": 0}

    def emit(record):
        with (out / "records.jsonl").open("a") as handle:
            handle.write(json.dumps(strings(record), sort_keys=True) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        summary["completed_records"] += 1

    try:
        assert platform.python_implementation() == "CPython" and sys.version_info[:2] == (3, 12)
        assert manifest["numpy"] == "2.3.5"
        assert all(value == "1" for value in env.values())
        for name, function in (("k3_nonexchangeable_fibers", check_k3),
                               ("saved_candidate_certificates", check_saved),
                               ("global_radius_formula", check_global),
                               ("exact_boundary_witnesses", check_boundaries)):
            summary["active_family"] = name
            summary["families"][name] = function(emit)
        summary.pop("active_family")
        assert summary["completed_records"] == 1439
        summary["status"] = "pass"
    except BaseException as error:
        summary["status"] = "failure"
        summary["failure"] = {"type": type(error).__name__, "message": str(error),
                              "traceback": traceback.format_exc()}
        raise
    finally:
        usage = resource.getrusage(resource.RUSAGE_SELF)
        summary.update({"end_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
                        "wall_seconds": (time.monotonic_ns() - clock) / 1e9,
                        "user_cpu_seconds": usage.ru_utime - initial_usage.ru_utime,
                        "system_cpu_seconds": usage.ru_stime - initial_usage.ru_stime,
                        "peak_rss_kib": usage.ru_maxrss,
                        "records_sha256": digest(out / "records.jsonl") if (out / "records.jsonl").exists() else None})
        encoded = json.dumps(strings(summary), indent=2) + "\n"
        (out / "summary.json").write_text(encoded)
        print(encoded)


if __name__ == "__main__":
    main()
