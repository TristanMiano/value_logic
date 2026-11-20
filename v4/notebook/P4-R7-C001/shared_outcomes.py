"""Check literal sharing of realized bandit payoffs in W7.3's archived rooms."""
import csv
from collections import Counter, defaultdict
from decimal import Decimal
from fractions import Fraction as F
from hashlib import sha256
from itertools import permutations
from math import comb, perm, sqrt
from pathlib import Path
import sys

from bandit_data import EXPECTED, select_room


def pairs(values):
    return sum(comb(n, 2) for n in Counter(values).values())


def permutation_moments(groups):
    """Each row is a same-round group. Permute rewards over the observed slots."""
    counts = Counter(v for g in groups for v in g)
    n = sum(counts.values())
    edges = sum(comb(len(g), 2) for g in groups)
    if not edges:
        return 0, 0
    p2 = F(sum(perm(c, 2) for c in counts.values()), perm(n, 2))
    mean = edges * p2
    var = edges * p2 * (1-p2)
    overlap = 3 * sum(comb(len(g), 3) for g in groups)
    if overlap:
        p3 = F(sum(perm(c, 3) for c in counts.values()), perm(n, 3))
        var += 2 * overlap * (p3-p2*p2)
    disjoint = comb(edges, 2)-overlap
    if disjoint:
        ways = [perm(c, 2) for c in counts.values()]
        both = sum(perm(c, 4) for c in counts.values()) + sum(ways)**2-sum(v*v for v in ways)
        p22 = F(both, perm(n, 4))
        var += 2 * disjoint * (p22-p2*p2)
    assert var >= 0
    return mean, var


def small_check():
    g = [[0, 0, 1], [0, 1], [2]]
    ex, var = permutation_moments(g)
    vals = [pairs(v[:3])+pairs(v[3:5]) for v in permutations(sum(g, []))]
    assert ex == F(sum(vals),len(vals))
    assert var == sum((v-ex)**2 for v in vals)/len(vals)


def main(path):
    assert sha256(path.read_bytes()).hexdigest() == EXPECTED
    rooms = defaultdict(lambda: defaultdict(list))
    seen = set()
    with path.open(encoding="utf8", newline="") as f:
        for row in csv.DictReader(f):
            room, t = row["room"], int(row["round"])
            key = room, t, row["ID"]
            assert key not in seen
            seen.add(key)
            rooms[room][t].append((int(row["machine"]), Decimal(row["result"])))
    strata = defaultdict(lambda: defaultdict(list))
    eligible = [s for s in rooms.values() if select_room(s)]
    for room, series in enumerate(eligible):
        for t, choices in series.items():
            for arm, value in choices:
                strata[room, t>40, arm][t].append(value)
    within = equal = eligible_groups = equal_groups = 0
    expected = variance = cross_expected = F(0)
    cross_pairs_with_reference = 0
    for by_round in strata.values():
        groups = list(by_round.values())
        size = sum(map(len,groups))
        w = sum(comb(len(g), 2) for g in groups)
        eq = sum(pairs(g) for g in groups)
        within += w
        equal += eq
        eligible_groups += sum(len(g)>=2 for g in groups)
        equal_groups += sum(len(g)>=2 and len(set(g))==1 for g in groups)
        cross = comb(size,2)-w
        if cross:
            cross_expected += w * F(pairs([v for g in groups for v in g])-eq,cross)
            cross_pairs_with_reference += w
        ex, var = permutation_moments(groups)
        expected += ex
        variance += var
    print("Rooms", len(eligible), "same-arm same-round pairs/exact matches", within, equal,
          "with cross-round reference", cross_pairs_with_reference,
          "expected using cross-round rate", float(cross_expected))
    print("Multi-person same-arm groups/all identical", eligible_groups, equal_groups,
          "stratified random allocation mean and SD of pair matches", float(expected), sqrt(variance))


if __name__ == "__main__":
    small_check()
    main(Path(sys.argv[1]))
