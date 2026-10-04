"""Public rational input contract, independent of native syntax and search."""
from dataclasses import dataclass
from fractions import Fraction
from itertools import product


class InputError(ValueError):
    """Malformed or out-of-scope input, never a semantic refutation."""


def exact(value):
    if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
        raise InputError('Use exact integers or Fraction values.')
    value = Fraction(value)
    if max(abs(value.numerator).bit_length(), value.denominator.bit_length()) > 256:
        raise InputError('Input rationals are limited to 256 bits per component.')
    return value


@dataclass(frozen=True)
class Evidence:
    """Four optional bundles, plus permanent |beta|,|gamma| <= 1.

    None means absent, while zero is a present exact bound. The two joint
    bounds are separate rows; a cap contributes both signs. All states admit
    beta=gamma=0. Version changes remain explicit even if bounds are identical.
    """
    plus: Fraction | None = None
    minus: Fraction | None = None
    beta: Fraction | None = None
    gamma: Fraction | None = None
    revision: str = 'initial'

    def validate(self):
        for value, maximum in zip(self.bounds, (2, 2, 1, 1)):
            if value is not None and not 0 <= exact(value) <= maximum:
                raise InputError('Evidence lies outside the frozen rational box.')
        if not isinstance(self.revision, str) or not self.revision or len(self.revision) > 128:
            raise InputError('A nonempty revision of at most 128 characters is required.')
        return self

    @property
    def bounds(self):
        return self.plus, self.minus, self.beta, self.gamma


@dataclass(frozen=True)
class Query:
    action: str
    budget: Fraction = Fraction(0)

    def validate(self):
        if self.action not in ('T1', 'T2', 'R'):
            raise InputError('Supported actions are T1, T2 and R against F=T4.')
        exact(self.budget)
        return self


def core_states():
    """The fixed first acceptance slice: sixteen zero/absent states."""
    return tuple(Evidence(*values, revision=f'core-{i:02d}')
                 for i, values in enumerate(product((None, Fraction(0)), repeat=4)))
