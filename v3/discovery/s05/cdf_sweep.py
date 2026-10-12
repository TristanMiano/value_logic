"""Exact finite probability-box expectations by a sliding quantile sweep.

ChatGPT (GPT-6 Astra Pro), 2026-10-12. DEVELOPMENT implementation of the
established p-box/random-set expectation representation. See cdf_sweep.md.
The source has only pointwise CDF constraints; extra moment constraints are
not silently ignored. Arithmetic counts are linear, not constant-bit costs.
"""
from collections import deque
from fractions import Fraction as F
from heapq import merge


class CDFSweep:
    def __init__(self, lower, upper):
        self.lower = tuple(map(F, lower))
        self.upper = tuple(map(F, upper))
        if len(self.lower) != len(self.upper):
            raise ValueError('CDF arrays have different lengths')
        for bound in (self.lower, self.upper):
            if any(not 0 <= value <= 1 for value in bound):
                raise ValueError('CDF values must lie in [0,1]')
            if any(a > b for a, b in zip(bound, bound[1:])):
                raise ValueError('CDF endpoints must be nondecreasing')
        if any(a > b for a, b in zip(self.lower, self.upper)):
            raise ValueError('Lower CDF exceeds upper CDF')
        self.size = len(self.lower) + 1
        # There are two sorted arrays, so this merge has linear comparison
        # count. No sort of an unsorted O(m)-element list is hidden here.
        levels = []
        for value in merge((F(0), *self.lower, F(1)),
                           (F(0), *self.upper, F(1))):
            if not levels or levels[-1] != value:
                levels.append(value)
        lo_cdf, hi_cdf = (*self.lower, F(1)), (*self.upper, F(1))
        a = b = 0
        windows = []
        for left, right in zip(levels, levels[1:]):
            # u is in (left,right); equality boundaries have zero mass.
            while hi_cdf[a] <= left:
                a += 1
            while lo_cdf[b] <= left:
                b += 1
            assert a <= b < self.size
            windows.append((left, right, a, b))
        self.windows = tuple(windows)

    def feasible(self, probability):
        if len(probability) != self.size:
            return False
        p = tuple(map(F, probability))
        if any(x < 0 for x in p) or sum(p) != 1:
            return False
        cumulative = F(0)
        for j, (lower, upper) in enumerate(zip(self.lower, self.upper)):
            cumulative += p[j]
            if not lower <= cumulative <= upper:
                return False
        return True

    def minimum(self, payoff, certificate=True):
        g = tuple(map(F, payoff))
        if len(g) != self.size:
            raise ValueError('One payoff per support point is required')
        candidates = deque()
        next_index = 0
        probability = [F(0)] * self.size
        value, last_choice = F(0), -1
        trace = []
        counters = dict(pushes=0, back_pops=0, front_pops=0,
                        payoff_comparisons=0, windows=len(self.windows))
        for left, right, a, b in self.windows:
            while next_index <= b:
                while candidates:
                    counters['payoff_comparisons'] += 1
                    # Strict inequality retains the leftmost minimizer.
                    if g[candidates[-1]] <= g[next_index]:
                        break
                    candidates.pop()
                    counters['back_pops'] += 1
                candidates.append(next_index)
                counters['pushes'] += 1
                next_index += 1
            while candidates[0] < a:
                candidates.popleft()
                counters['front_pops'] += 1
            chosen = candidates[0]
            assert a <= chosen <= b and chosen >= last_choice
            last_choice = chosen
            mass = right - left
            probability[chosen] += mass
            value += mass*g[chosen]
            if certificate:
                trace.append(dict(left=str(left), right=str(right),
                                  a=a, b=b, chosen=chosen))
        assert self.feasible(probability)
        assert sum(x*y for x, y in zip(probability, g)) == value
        assert counters['pushes'] <= self.size
        assert counters['back_pops'] + counters['front_pops'] <= self.size
        return dict(value=str(value), probability=list(map(str, probability)),
                    trace=trace, operations=counters)

    def interval(self, payoff, certificate=True):
        payoff = tuple(map(F, payoff))
        lower = self.minimum(payoff, certificate)
        negative = self.minimum(tuple(-v for v in payoff), certificate)
        return dict(lower=lower['value'], upper=str(-F(negative['value'])),
                    lower_certificate=lower,
                    negative_upper_certificate=negative)


def verify_minimum(source, payoff, answer):
    """Independent direct range check of an emitted certificate.

    This deliberately simple checker can cost O(m^2); it is separate from
    the linear sweep. A feasible distribution plus pointwise range minima
    proves attainment and the lower bound without trusting a floating LP.
    """
    g = tuple(map(F, payoff))
    if len(g) != source.size or len(answer['trace']) != len(source.windows):
        return False
    probability = [F(0)] * source.size
    checked_value = F(0)
    for expected, row in zip(source.windows, answer['trace']):
        left, right, a, b = expected
        if (F(row['left']), F(row['right']), row['a'], row['b']) != expected:
            return False
        chosen = row['chosen']
        if not a <= chosen <= b or g[chosen] != min(g[a:b+1]):
            return False
        probability[chosen] += right-left
        checked_value += (right-left)*g[chosen]
    return (source.feasible(probability)
            and probability == list(map(F, answer['probability']))
            and checked_value == F(answer['value']))
