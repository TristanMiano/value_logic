"""Shared finite accounting for P3-08. DEVELOPMENT only.

Research-by: ChatGPT (GPT-6 Astra Pro), 2026-10-10.
The unchanged P3-B recurrence supplies the word meter, finite bit tape and
numeric product update. A separate generic broker versions its query boundary.
JSON construction and evidence hashing are research-harness operations unless
explicitly charged by registry_setup; deployed output is a priced word record.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
_name = "_p308_inherited_selective_core"
if _name not in sys.modules:
    _spec = importlib.util.spec_from_file_location(
        _name, HERE.parent / "checks/07_selective_feedback.py")
    _module = importlib.util.module_from_spec(_spec)
    sys.modules[_name] = _module
    _spec.loader.exec_module(_module)
C = sys.modules[_name]
VERSION = "p308-common-v1"
STAGE = "DEVELOPMENT"


@dataclass(frozen=True)
class ResourceRecord:
    total: int
    by_category: tuple[tuple[str, int], ...]
    operations: tuple[tuple[str, str, int], ...]

    def record(self):
        return {"total": self.total, "by_category": dict(self.by_category),
                "operations": [{"category": c, "operation": op, "units": n}
                               for c, op, n in self.operations]}


def resources(meter, before=None):
    """Immutable delta invoice; the snapshot itself is harness bookkeeping."""
    before = before or {"total": 0, "by_category": {}, "operations": []}
    old = {(r["category"], r["operation"]): r["units"] for r in before["operations"]}
    operations = tuple((c, op, n - old.get((c, op), 0))
                       for (c, op), n in sorted(meter.operations.items())
                       if n != old.get((c, op), 0))
    categories = tuple((c, meter.by_category[c] - before["by_category"].get(c, 0))
                       for c in C.CATEGORIES)
    result = ResourceRecord(meter.total - before["total"], categories, operations)
    if result.total != sum(n for _, n in categories) or result.total != sum(n for _, _, n in operations):
        raise AssertionError("Invoice does not reconcile.")
    return result


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def fraction_record(value):
    value = Fraction(value)
    return [value.numerator, value.denominator]


def fraction_value(value):
    return Fraction(*value) if isinstance(value, (tuple, list)) else Fraction(value)


def registry_setup(paths, meter):
    """One cold source procurement under a declared byte/block tariff.

    Every 64-bit source word costs a read plus retention; each SHA-256 input
    block costs one named hashing primitive. Python import/compile wall time
    is not inferred from this service tariff. All compared methods receive
    the same installed platform and its common cold bill.
    """
    records = []
    for path in sorted(set(Path(p).resolve() for p in paths)):
        if not path.is_relative_to(REPO):
            raise C.Rejected("Source procurement must remain in the declared repository.")
        size = path.stat().st_size
        if size > 2**20:
            raise C.Rejected("Source file outside the finite registry contract.")
        words = max(1, (size + 7) // 8)
        meter.pay_many((("setup", "source_word_read", words),
                        ("setup", "source_sha256_block", (size + 72) // 64),
                        ("storage", "installed_source_word", words)))
        data = path.read_bytes()
        if len(data) != size:
            raise C.Rejected("Source changed during procurement.")
        records.append({"path": str(path.relative_to(REPO)), "bytes": size,
                        "sha256": hashlib.sha256(data).hexdigest()})
    return records


class RationalMeter:
    """Precharged bounded exact reporting arithmetic, separately from scores.

    Charge a conservative word-operation bundle before Fraction arithmetic.
    The 512-bit cap concerns inputs and pre-normalization intermediates, not
    physical heap use. Binary operators below bound the products first.
    """
    MAX_BITS = 512

    def __init__(self, meter):
        self.meter = meter
        self.peak_bits = 1

    def _check(self, *values):
        for value in values:
            value = Fraction(value)
            bits = max(abs(value.numerator).bit_length(), value.denominator.bit_length(), 1)
            if bits > self.MAX_BITS:
                raise C.Rejected("Reporting rational exceeds the admitted width.")
            self.peak_bits = max(self.peak_bits, bits)

    def operation(self, op, left, right):
        left, right = Fraction(left), Fraction(right)
        self._check(left, right)
        a = max(abs(left.numerator).bit_length(), left.denominator.bit_length(), 1)
        b = max(abs(right.numerator).bit_length(), right.denominator.bit_length(), 1)
        bound = a + b + (1 if op in ("add", "sub") else 0)
        if bound > self.MAX_BITS:
            raise C.Rejected("Reporting pre-normalization intermediate exceeds its cap.")
        za, zb = (a + 63) // 64, (b + 63) // 64
        # Four schoolbook products, additions and a conservative Euclidean
        # normalization envelope. This is a declared abstract service price.
        amount = 8 * za * zb + 4 * (za + zb) + 4 * bound * ((bound + 63) // 64)**2
        self.meter.pay("assessment", "rational_" + op + "_word_envelope", amount)
        if op == "add":
            result = left + right
        elif op == "sub":
            result = left - right
        elif op == "mul":
            result = left * right
        elif op == "div":
            if not right:
                raise C.Rejected("Zero reporting divisor.")
            result = left / right
        else:
            raise C.Rejected("Unknown rational operator.")
        self.peak_bits = max(self.peak_bits, bound)
        self._check(result)
        return result

    def add(self, a, b):
        return self.operation("add", a, b)

    def sub(self, a, b):
        return self.operation("sub", a, b)

    def mul(self, a, b):
        return self.operation("mul", a, b)

    def div(self, a, b):
        return self.operation("div", a, b)

    def compare(self, a, b):
        a, b = Fraction(a), Fraction(b)
        self._check(a, b)
        bound = max(abs(a.numerator).bit_length(), a.denominator.bit_length(), 1) + max(abs(b.numerator).bit_length(), b.denominator.bit_length(), 1)
        if bound > self.MAX_BITS:
            raise C.Rejected("Reporting comparison intermediate exceeds its cap.")
        z = (bound + 63) // 64
        self.meter.pay("assessment", "rational_compare_word_envelope", 8 * z * z + 4 * z)
        self.peak_bits = max(self.peak_bits, bound)
        return (a > b) - (a < b)
