"""Optional F11 adapter for the two-bit program from N01 recurrence C16/C22."""
from dataclasses import dataclass
from fractions import Fraction as Q

from .model import InputError, exact


@dataclass(frozen=True)
class ProgramEvidence:
    error_cap: Q = Q(1, 20)
    second_cap: Q = Q(3, 10)
    revision: str = 'program-initial'
    foreign_zero: bool = False

    def validate(self):
        if not 0 <= exact(self.error_cap) <= Q(1, 20):
            raise InputError('Error evidence must lie in [0,1/20].')
        if not Q(1, 5) <= exact(self.second_cap) <= Q(3, 10):
            raise InputError('Second-input mass cap must lie in [1/5,3/10].')
        if not isinstance(self.revision, str) or not self.revision or len(self.revision) > 128:
            raise InputError('A bounded nonempty revision is required.')
        if type(self.foreign_zero) is not bool:
            raise InputError('Foreign-unit control must be Boolean.')
        return self


@dataclass(frozen=True)
class ProgramQuery:
    kind: str = 'mean_edit'
    alpha: Q = Q(0)
    budget: Q = Q(0)

    def validate(self):
        if self.kind not in ('mean_edit', 'risk_vs_full'):
            raise InputError('Unknown finite-program consumer.')
        if not 0 <= exact(self.alpha) < 1:
            raise InputError('Tail confidence must lie in [0,1).')
        if self.kind == 'mean_edit' and self.alpha != 0:
            raise InputError('Mean edit does not take a tail-confidence parameter.')
        exact(self.budget)
        return self
