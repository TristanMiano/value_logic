#!/usr/bin/env python3
"""Objective transfer margins preserving finite within-row dependence.

DEVELOPMENT. ChatGPT (GPT-6 Astra Pro), 2026-10-12. Public row scans only;
no hull, latent row-product or Boolean objective-mask enumeration in the quote.
"""
from fractions import Fraction as F


def margins(modes, possible, q, meter, references=None):
    """Return safe alpha/delta for every compatible w and Boolean z.

    (w-q) dot z <= alpha and (q-w) dot z <= delta. If references is supplied,
    its signed rational rows must sum exactly to q. Otherwise compare an
    integer row-midpoint decomposition (residual assigned to the last
    unresolved row, or the last row if all are known) and the uniform q/N
    decomposition. Independently minimize each margin with the box quotation.
    """
    n, m = len(possible), len(q)
    if not n or not m or any(type(x) is not int or x < 0 for x in q):
        raise ValueError("Nonempty cohort and nonnegative integral query vector required")
    modes = [list(map(F, v)) for v in modes]
    if not modes or any(len(v) != m or any(x < 0 for x in v) for v in modes):
        raise ValueError("Matching nonnegative public cost vectors required")
    if any(not row or any(type(h) is not int or not 0 <= h < len(modes) for h in row)
           for row in possible):
        raise ValueError("Each cohort row needs a nonempty admitted mode set")
    row_lo = [[min(modes[h][j] for h in row) for j in range(m)] for row in possible]
    row_hi = [[max(modes[h][j] for h in row) for j in range(m)] for row in possible]
    lo = [sum((r[j] for r in row_lo), F(0)) for j in range(m)]
    hi = [sum((r[j] for r in row_hi), F(0)) for j in range(m)]
    box_alpha = sum((max(F(0), h - v) for h, v in zip(hi, q)), F(0))
    box_delta = sum((max(F(0), v - l) for v, l in zip(q, lo)), F(0))
    meter.pay("row_margin_quote", "validation_coordinate_enclosures_and_box_margins",
              4 * m * sum(map(len, possible)) + 4 * n * m + 6 * m + len(modes) * m + 8)
    if references is None:
        midpoint = [[(l + h) // 2 for l, h in zip(left, right)]
                    for left, right in zip(row_lo, row_hi)]
        residual = [q[j] - sum(r[j] for r in midpoint) for j in range(m)]
        unresolved = [i for i, row in enumerate(possible) if len(row) > 1]
        residual_row = unresolved[-1] if unresolved else n - 1
        midpoint[residual_row] = [x + e for x, e in zip(midpoint[residual_row], residual)]
        uniform = [[F(v, n) for v in q] for _ in range(n)]
        decompositions = [("row_integer_midpoints_with_one_residual", midpoint),
                          ("uniform_query_share", uniform)]
        meter.pay("row_margin_quote", "two_public_reference_decompositions", 5 * n * m + 3 * m + n)
    else:
        if len(references) != n or any(len(row) != m for row in references):
            raise ValueError("One reference vector per cohort row required")
        references = [list(map(F, row)) for row in references]
        residual_row = None
        decompositions = [("supplied_exact_decomposition", references)]
    candidates = []
    for name, refs in decompositions:
        if any(sum((row[j] for row in refs), F(0)) != q[j] for j in range(m)):
            raise ValueError("Reference rows do not sum to the query objective")
        per_row = []
        for ids, ref in zip(possible, refs):
            positive = [sum((max(F(0), modes[h][j] - ref[j]) for j in range(m)), F(0))
                        for h in ids]
            negative = [sum((max(F(0), ref[j] - modes[h][j]) for j in range(m)), F(0))
                        for h in ids]
            per_row.append(dict(alpha=max(positive), delta=max(negative)))
        alpha = sum((r["alpha"] for r in per_row), F(0))
        delta = sum((r["delta"] for r in per_row), F(0))
        meter.pay("row_margin_quote", "positive_negative_parts_and_row_extrema",
                  8 * m * sum(map(len, possible)) + 4 * n + n * m + 6)
        candidates.append(dict(method=name, references=refs, rows=per_row, alpha=alpha, delta=delta))
    row_alpha = min(c["alpha"] for c in candidates)
    row_delta = min(c["delta"] for c in candidates)
    alpha, delta = min(box_alpha, row_alpha), min(box_delta, row_delta)
    meter.pay("row_margin_quote", "independent_safe_margin_minima", 2 * len(candidates) + 4)
    return dict(alpha=alpha, delta=delta, box_alpha=box_alpha, box_delta=box_delta,
                row_alpha=row_alpha, row_delta=row_delta,
                strict_improvement=alpha < box_alpha or delta < box_delta,
                decompositions=candidates, residual_row=residual_row,
                references=candidates[0]["references"],
                objective_masks_enumerated=0, row_product_enumerated=0,
                premise="Every compatible cohort sum, and its rowwise convex relaxation, with fixed ordered Boolean objective features")
