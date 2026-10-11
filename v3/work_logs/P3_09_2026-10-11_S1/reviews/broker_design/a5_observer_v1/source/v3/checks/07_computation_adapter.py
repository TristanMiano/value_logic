"""P3-07 paid finite modular computation adapter; DEVELOPMENT ONLY.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-09 UTC.
Agent implementation time is unmeasured; zero principal Research90 credit.

This is a new adapter, not a change to P3-03/P3-05/P3-06 evidence.  A
right-to-left binary producer is checked by an independently implemented
left-to-right binary computation.  No answer is returned until paid checking
and acquisition complete.  Exact shortcuts and semantic residue reuse are
public operations available to every controller.

The accounting model counts declared bounded primitive operations, 64-bit
storage words, and explicit input/identity work.  It is not elapsed CPU time or
a claim that Python overhead is free on real machines.  Audit serialization,
Meter snapshots, and the experiment harness's private scoring are outside the
decision model; a controller must not obtain information through those paths.
All numeric inputs and retained policy data are capped.  A failed charge takes
effect before the operation it would fund.  A paid preflight can be followed by
a denied arithmetic bundle: its already spent units remain charged.

There is no dependency compiler or candidate repair search in this arithmetic
adapter.  Their categories remain zero/not applicable here; the exact cache
uses full mathematical input and source-version equality, not a claimed
transport theorem.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass
import hashlib
import json


VERSION = "p307-modular-computation-adapter-v1.1"
SEMANTICS_VERSION = "modular-power-equality-v1"
PRODUCER_VERSION = "right-to-left-binary-v1"
CHECKER_VERSION = "left-to-right-binary-v1"
SHORTCUT_VERSION = "elementary-modular-identities-v1"
MAX_A, MAX_N, MAX_M = 8191, 192, 97
MAX_CACHE, MAX_JOBS, MAX_TRANSACTIONS = 32, 4, 256
MAX_TOTAL_UNITS, MAX_EVENTS = 10_000_000, 100_000
MAX_LABEL = 128
MAX_FULL_TRANSACTIONS = 19
# Loose proved caps for the public common-prefix response below.  The cold cap
# assumes an initially empty cache.  A bounded warm cache adds at most 32 key
# scans, covered by the warm cap.  Neither includes controller/profile work.
MAX_COLD_COMPLETION_UNITS = 1024
MAX_WARM_COMPLETION_UNITS = 2048
CATEGORIES = (
    "admission", "solve", "check", "acquisition", "storage", "cache",
    "forecast", "assessment", "profile", "dependency_compile", "repair_search",
)


class ProtocolError(ValueError):
    pass


class BudgetExhausted(RuntimeError):
    def __init__(self, reason, needed, remaining):
        super().__init__(f"{reason}: need {needed}, remaining {remaining}")
        self.reason, self.needed, self.remaining = reason, needed, remaining


def _nat(value, maximum, name):
    if type(value) is not int or not 0 <= value <= maximum:
        raise ProtocolError(f"{name} must be an exact bounded nonnegative integer.")
    return value


def _label(value, name):
    if (type(value) is not str or not 1 <= len(value) <= MAX_LABEL
            or not value.isascii()):
        raise ProtocolError(f"{name} must be a nonempty capped ASCII string.")
    return value


def _words(length):
    return max(1, (length + 7) // 8)


def _audit_digest(value):
    """Harness-only serialization; not an information-gathering policy API."""
    return hashlib.sha256(json.dumps(value, sort_keys=True,
                                     separators=(",", ":")).encode()).hexdigest()


class Meter:
    """Hard cap on one response/episode, with a shared explicit operation model.

    Every counted operation costs one abstract unit.  Storage uses one unit per
    64-bit word read or written.  Work paid by forecast/assessment/profile code
    must be supplied through this same meter; these names are not free hooks.
    The event log is bounded harness instrumentation, unavailable as an oracle.
    """
    def __init__(self, limit_total, category_limits=None):
        self.limit_total = _nat(limit_total, MAX_TOTAL_UNITS, "total limit")
        limits = {} if category_limits is None else category_limits
        if type(limits) is not dict or set(limits) - set(CATEGORIES):
            raise ProtocolError("Unknown category limit.")
        self.category_limits = {k: _nat(limits.get(k, limit_total),
                                       MAX_TOTAL_UNITS, "category limit")
                                for k in CATEGORIES}
        self.total = 0
        self.by_category = Counter({k: 0 for k in CATEGORIES})
        self.operations = Counter()
        self.events = []
        self.denials = 0
        self.last_denial = None
        self.max_operand_bits = Counter()

    @property
    def remaining(self):
        return self.limit_total - self.total

    def pay(self, category, operation, units=1):
        self.pay_many(((category, operation, units),))

    def pay_many(self, charges):
        """Check the whole bounded bundle before mutating charge counters."""
        if type(charges) is not tuple or not 1 <= len(charges) <= 32:
            raise ProtocolError("A capped immutable nonempty charge bundle is required.")
        delta = Counter()
        for item in charges:
            if type(item) is not tuple or len(item) != 3:
                raise ProtocolError("Malformed charge item.")
            category, operation, units = item
            if category not in CATEGORIES:
                raise ProtocolError("Unknown charged category.")
            _label(operation, "operation")
            _nat(units, MAX_TOTAL_UNITS, "charge units")
            delta[category] += units
        needed = sum(delta.values())
        reason, available = None, None
        if len(self.events) >= MAX_EVENTS:
            reason, needed, available = "event capacity", 1, 0
        elif needed > self.remaining:
            reason, available = "total budget", self.remaining
        else:
            for category, amount in delta.items():
                remaining = self.category_limits[category] - self.by_category[category]
                if amount > remaining:
                    reason, needed, available = category + " budget", amount, remaining
                    break
        if reason is not None:
            self.denials += 1
            self.last_denial = dict(reason=reason, needed=needed, remaining=available)
            raise BudgetExhausted(reason, needed, available)
        self.total += needed
        self.by_category.update(delta)
        for category, operation, units in charges:
            self.operations[category + "." + operation] += units
        self.events.append(dict(index=len(self.events), charges=charges, total=self.total))

    def observe_bits(self, category, *operands):
        """Bounded audit observation after a paid operation, not policy evidence."""
        self.max_operand_bits[category] = max(self.max_operand_bits[category],
            *(max(1, abs(x).bit_length()) for x in operands))

    def snapshot(self):
        return dict(version=VERSION, limit_total=self.limit_total, total=self.total,
                    remaining=self.remaining, by_category=dict(self.by_category),
                    category_limits=dict(self.category_limits),
                    operations=dict(sorted(self.operations.items())),
                    max_operand_bits=dict(self.max_operand_bits), events=len(self.events),
                    denials=self.denials, last_denial=self.last_denial)


@dataclass(frozen=True)
class Query:
    query_id: str
    a: int
    n: int
    m: int
    r: int
    source_version: str = "modexp-input-v1"
    semantics_version: str = SEMANTICS_VERSION

    def __post_init__(self):
        _label(self.query_id, "query identity")
        _label(self.source_version, "source version")
        if type(self.semantics_version) is not str or self.semantics_version != SEMANTICS_VERSION:
            raise ProtocolError("Unsupported modular semantics version.")
        _nat(self.a, MAX_A, "base")
        _nat(self.n, MAX_N, "exponent")
        _nat(self.m, MAX_M, "modulus")
        if self.m < 2:
            raise ProtocolError("Modulus must be at least two.")
        _nat(self.r, self.m - 1, "target residue")

    @property
    def residue_key(self):
        return self.semantics_version, self.source_version, self.a, self.n, self.m

    @property
    def claim_key(self):
        return self.residue_key + (self.r,)

    @property
    def key_words(self):
        return _words(len(self.semantics_version) + len(self.source_version)) + 4


@dataclass(frozen=True)
class Answer:
    query_id: str
    claim_key: tuple
    residue: int
    answer: int
    provenance: str
    producer_version: str
    checker_version: str

    def record(self):
        return asdict(self)


@dataclass(frozen=True)
class JobHandle:
    job_id: int
    claim_key: tuple


@dataclass(frozen=True)
class Progress:
    phase: str
    transactions: int
    spent_units: int
    budget_exhausted: bool

    @property
    def checked_ready(self):
        return self.phase == "ready"


@dataclass(frozen=True)
class _Certificate:
    residue_key: tuple
    residue: int
    producer_version: str
    checker_version: str
    kind: str


class Adapter:
    """Trusted local state machine; underscore state is private to the harness.

    Controllers use lookup/shortcut/start/advance/acquire/cancel only.  Cold
    episodes are new Adapter(Meter(...)) instances.  Source changes alter the
    semantic cache key.  Objective changes (stakes or target r) do not retract
    an established residue, so the same checked residue can answer a new r.
    """
    def __init__(self, meter, cache_cap=MAX_CACHE):
        if type(meter) is not Meter:
            raise ProtocolError("This adapter requires its own metered resource model.")
        self.meter = meter
        self.cache_cap = _nat(cache_cap, MAX_CACHE, "cache capacity")
        self._cache = []
        self._jobs = {}
        self._next_job = 0
        self.peak_jobs = 0
        self.peak_cache = 0

    def _admit(self, query):
        if type(query) is not Query:
            raise ProtocolError("Use the exact immutable Query type.")
        self.meter.pay_many((("admission", "scalar_field_check", 8),
                             ("admission", "identity_word_read", query.key_words)))
        query.__post_init__()

    def _answer(self, query, certificate, provenance):
        self.meter.pay_many((("acquisition", "target_comparison", 1),
                             ("storage", "answer_word_write", 8)))
        return Answer(query.query_id, query.claim_key, certificate.residue,
                      int(certificate.residue == query.r), provenance,
                      certificate.producer_version, certificate.checker_version)

    def lookup(self, query):
        self._admit(query)
        self.meter.pay("cache", "lookup", 1)
        for certificate in self._cache:
            self.meter.pay("cache", "semantic_key_word_compare", query.key_words)
            if certificate.residue_key == query.residue_key:
                return self._answer(query, certificate, "exact_semantic_cache")
        return None

    def _store(self, query, residue, producer, checker, kind, *, release_job=False):
        words = query.key_words + _words(len(producer) + len(checker)) + 4
        charges = [("acquisition", "checked_record_admission", query.key_words),
                   ("storage", "certificate_word_read", words)]
        if self.cache_cap:
            charges.append(("storage", "certificate_word_write", words))
            if len(self._cache) >= self.cache_cap:
                charges.append(("storage", "oldest_certificate_release", 1))
        # Include the returned answer in this same bundle.  No cache entry is
        # published if acquisition/answer construction cannot be paid in full.
        charges += [("acquisition", "target_comparison", 1),
                    ("storage", "answer_word_write", 8)]
        if release_job:
            charges.append(("storage", "completed_job_release", 1))
        self.meter.pay_many(tuple(charges))
        certificate = _Certificate(query.residue_key, residue, producer, checker, kind)
        if self.cache_cap:
            if len(self._cache) >= self.cache_cap:
                del self._cache[0]
            self._cache.append(certificate)
            self.peak_cache = max(self.peak_cache, len(self._cache))
        return Answer(query.query_id, query.claim_key, residue, int(residue == query.r),
                      kind, producer, checker)

    def shortcut(self, query):
        """Try actual elementary identities; an unrecognized case still pays."""
        self._admit(query)
        self.meter.pay_many((("solve", "modular_reduce", 1),
                             ("solve", "shortcut_branch_test", 4),
                             ("solve", "parity_test", 1)))
        base = query.a % query.m
        # Eagerly execute all four declared tests and the parity operation;
        # these counts describe this public implementation, not a lower bound
        # on the cheapest possible implementation of the identities.
        zero_exp, zero_base = query.n == 0, base == 0
        unit_base, minus_unit_base = base == 1, base == query.m - 1
        parity = query.n % 2
        if zero_exp:
            residue, reason = 1, "zero_exponent"
        elif zero_base:
            residue, reason = 0, "zero_residue_base"
        elif unit_base:
            residue, reason = 1, "unit_residue_base"
        elif minus_unit_base:
            residue, reason = (base if parity else 1), "minus_unit_residue_base"
        else:
            return None
        self.meter.pay_many((("check", "modular_reduce", 1),
                             ("check", "shortcut_witness_test", 5),
                             ("check", "parity_test", 1)))
        # An independently specified certificate checker for the four admitted
        # identities; it does not trust an arbitrary producer answer.
        check_base, check_parity = query.a % query.m, query.n & 1
        guards = {
            "zero_exponent": query.n == 0,
            "zero_residue_base": query.n > 0 and check_base == 0,
            "unit_residue_base": query.n > 0 and check_base == 1,
            "minus_unit_residue_base": query.n > 0 and check_base + 1 == query.m,
        }
        expected = {"zero_exponent": 1, "zero_residue_base": 0,
                    "unit_residue_base": 1,
                    "minus_unit_residue_base": query.m - 1 if check_parity else 1}
        verified = guards[reason] and residue == expected[reason]
        if not verified:
            raise AssertionError("Internal shortcut certificate was rejected.")
        self.meter.observe_bits("solve", query.a, query.m, base, residue)
        return self._store(query, residue, SHORTCUT_VERSION, SHORTCUT_VERSION,
                           "checked_shortcut:" + reason)

    def start(self, query, algorithm="binary"):
        if type(algorithm) is not str or algorithm != "binary":
            raise ProtocolError("Only the public efficient binary producer is admitted.")
        if len(self._jobs) >= MAX_JOBS:
            raise ProtocolError("Active job capacity reached.")
        self._admit(query)
        self.meter.pay_many((("solve", "modular_reduce", 2),
                             ("storage", "initial_job_word_write", query.key_words + 8)))
        job_id = self._next_job
        self._next_job += 1
        self._jobs[job_id] = dict(query=query, phase="produce", result=1 % query.m,
                                  base=query.a % query.m, exponent=query.n)
        self.peak_jobs = max(self.peak_jobs, len(self._jobs))
        return JobHandle(job_id, query.claim_key)

    def _job(self, handle):
        if type(handle) is not JobHandle:
            raise ProtocolError("Use the exact immutable JobHandle type.")
        # Validate bounded scalar identity before hashing a caller-owned int.
        # The complete valid handle has one ID, six claim fields and a tuple
        # descriptor.  Its input and comparison work is not a free control path.
        self.meter.pay("admission", "handle_scalar_field_check", 8)
        _nat(handle.job_id, MAX_TOTAL_UNITS, "job identity")
        if type(handle.claim_key) is not tuple or len(handle.claim_key) != 6:
            raise ProtocolError("Malformed immutable claim key.")
        for value in handle.claim_key[:2]:
            _label(value, "handle version identity")
        for value, maximum in zip(handle.claim_key[2:], (MAX_A, MAX_N, MAX_M, MAX_M - 1)):
            _nat(value, maximum, "handle claim scalar")
        if handle.job_id not in self._jobs:
            raise ProtocolError("Unknown or completed job handle.")
        job = self._jobs[handle.job_id]
        self.meter.pay("admission", "handle_identity_word_compare", job["query"].key_words)
        if handle.claim_key != job["query"].claim_key:
            raise ProtocolError("Job handle claim binding changed.")
        return job

    def _step(self, job):
        meter, query = self.meter, job["query"]
        if job["phase"] == "produce":
            meter.pay("solve", "loop_guard", 1)
            if job["exponent"] == 0:
                meter.pay("storage", "phase_word_write", 1)
                job["phase"] = "check_setup"
                return
            meter.pay_many((("solve", "bit_test", 1), ("solve", "exponent_shift", 1),
                            ("solve", "last_iteration_test", 1)))
            odd = job["exponent"] & 1
            exponent = job["exponent"] >> 1
            products = odd + int(exponent != 0)
            meter.pay_many((("solve", "modular_multiply", products),
                            ("solve", "modular_reduce", products),
                            ("storage", "producer_state_word_write", 3)))
            result, base = job["result"], job["base"]
            if odd:
                product = result * base
                meter.observe_bits("solve", product, result, base)
                result = product % query.m
            if exponent:
                product = base * base
                meter.observe_bits("solve", product, base)
                base = product % query.m
            job.update(result=result, base=base, exponent=exponent)
        elif job["phase"] == "check_setup":
            meter.pay_many((("check", "modular_reduce", 2), ("check", "bit_length", 1),
                            ("storage", "checker_initial_word_write", 4)))
            job.update(phase="check", checked=1 % query.m, check_base=query.a % query.m,
                       cursor=query.n.bit_length() - 1)
        elif job["phase"] == "check":
            meter.pay("check", "loop_guard", 1)
            if job["cursor"] < 0:
                meter.pay_many((("check", "producer_checker_comparison", 1),
                                ("storage", "phase_word_write", 1)))
                if job["checked"] != job["result"]:
                    job["phase"] = "rejected"
                    raise AssertionError("Independent binary algorithms disagree.")
                job["phase"] = "ready"
                return
            meter.pay_many((("check", "exponent_shift", 1), ("check", "bit_test", 1)))
            bit = (query.n >> job["cursor"]) & 1
            products = 1 + bit
            meter.pay_many((("check", "modular_multiply", products),
                            ("check", "modular_reduce", products),
                            ("check", "cursor_decrement", 1),
                            ("storage", "checker_state_word_write", 2)))
            product = job["checked"] * job["checked"]
            meter.observe_bits("check", product, job["checked"])
            checked = product % query.m
            if bit:
                product = checked * job["check_base"]
                meter.observe_bits("check", product, checked, job["check_base"])
                checked = product % query.m
            job.update(checked=checked, cursor=job["cursor"] - 1)
        else:
            raise ProtocolError("Job has no executable producer/checker work.")

    def advance(self, handle, transaction_cap):
        _nat(transaction_cap, MAX_TRANSACTIONS, "transaction allowance")
        before = self.meter.total
        job = self._job(handle)
        used, exhausted = 0, False
        for _ in range(transaction_cap):
            if job["phase"] == "ready":
                break
            try:
                self._step(job)
            except BudgetExhausted:
                exhausted = True
                break
            used += 1
        return Progress(job["phase"], used, self.meter.total - before, exhausted)

    def acquire(self, handle):
        job = self._job(handle)
        if job["phase"] != "ready":
            raise ProtocolError("A fully checked job is required for acquisition.")
        answer = self._store(job["query"], job["result"], PRODUCER_VERSION,
                             CHECKER_VERSION, "checked_binary_computation", release_job=True)
        del self._jobs[handle.job_id]
        return answer

    def cancel(self, handle):
        self._job(handle)
        self.meter.pay("storage", "cancelled_job_release", 1)
        del self._jobs[handle.job_id]

    def public_state(self):
        """Harness-only state-cap audit; does not expose mathematical outputs."""
        return dict(version=VERSION, cache_cap=self.cache_cap,
                    active_jobs=len(self._jobs), cached_residues=len(self._cache),
                    peak_jobs=self.peak_jobs, peak_cache=self.peak_cache,
                    dependency_compile="not_applicable", repair_search="not_applicable")


def complete(query, limit_total=5000, transaction_cap=MAX_TRANSACTIONS, *,
             use_shortcut=True, cache_cap=MAX_CACHE):
    """Convenience development episode, with timeout returning no answer.

    The main experiment should retain and charge its own forecast/fallback and
    profile operations through Adapter/Meter directly.  This helper is only a
    producer/checker smoke interface; it is not a complete decision policy.
    """
    meter = Meter(limit_total)
    adapter = Adapter(meter, cache_cap=cache_cap)
    answer, progress = None, None
    try:
        answer = adapter.lookup(query)
        if answer is None and use_shortcut:
            answer = adapter.shortcut(query)
        if answer is None:
            handle = adapter.start(query)
            progress = adapter.advance(handle, transaction_cap)
            if progress.checked_ready:
                answer = adapter.acquire(handle)
    except BudgetExhausted:
        pass
    return dict(answer=answer.record() if answer else None,
                progress=asdict(progress) if progress else None,
                meter=meter.snapshot(), state=adapter.public_state())
