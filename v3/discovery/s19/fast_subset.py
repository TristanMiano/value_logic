"""Tagged exact min-max subset convolution, using the established chunk method."""
import math


def boolean_convolution(f, g, k):
    size = 1 << k
    fr = [[0] * size for _ in range(k + 1)]
    gr = [[0] * size for _ in range(k + 1)]
    for mask in range(size):
        rank = mask.bit_count()
        fr[rank][mask] = f[mask]
        gr[rank][mask] = g[mask]
    for rows in (fr, gr):
        for row in rows:
            for bit in range(k):
                b = 1 << bit
                for mask in range(size):
                    if mask & b:
                        row[mask] += row[mask ^ b]
    hr = [[0] * size for _ in range(k + 1)]
    for rank in range(k + 1):
        for left_rank in range(rank + 1):
            a, b, row = fr[left_rank], gr[rank-left_rank], hr[rank]
            for mask in range(size):
                row[mask] += a[mask] * b[mask]
        row = hr[rank]
        for bit in range(k):
            b = 1 << bit
            for mask in range(size):
                if mask & b:
                    row[mask] -= row[mask ^ b]
    return [hr[mask.bit_count()][mask] for mask in range(size)]


def minmax(f, g, k, counts=None):
    size = 1 << k
    entries = sorted((v, side, mask) for side, row in enumerate((f, g))
                     for mask, v in enumerate(row))
    width = math.isqrt(size)
    if width * width < size:
        width += 1
    active = [[0] * size, [0] * size]
    answer, split = [None] * size, [None] * size
    for start in range(0, len(entries), width):
        chunk = entries[start:start+width]
        for _, side, mask in chunk:
            active[side][mask] = 1
        possible = boolean_convolution(*active, k)
        if counts is not None:
            counts['boolean_calls'] = counts.get('boolean_calls', 0) + 1
        for mask in range(size):
            if split[mask] is not None or not possible[mask]:
                continue
            for _, side, sub in chunk:
                if counts is not None:
                    counts['tag_scans'] = counts.get('tag_scans', 0) + 1
                if sub & mask != sub:
                    continue
                left = sub if side == 0 else mask ^ sub
                val = max(f[left], g[mask ^ left])
                if split[mask] is None or val < answer[mask]:
                    answer[mask], split[mask] = val, left
            if split[mask] is None:
                raise AssertionError('first-positive chunk has no witness')
    if any(x is None for x in split):
        raise AssertionError('incomplete convolution')
    return answer, split


def maxmin(f, g, k, counts=None):
    vals, splits = minmax([-x for x in f], [-x for x in g], k, counts)
    return [-x for x in vals], splits
