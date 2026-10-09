"""Bounded mathematical services for R-P3-B-A; DEVELOPMENT ONLY.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-09 UTC.
Separate same-model implementation assignment; zero principal clock credit.

Public queries are the existing 248 Euler modular-equality claims. This file
contains no evaluator-label table and no learner. ``expert_predictions`` reads
only the public query. ``checked_purchase`` executes the old, source-bound
P3-07 adapter cold. Direct exact, semantic-cache and quadratic-residue-table
controls compute their answers from the same public mathematical inputs.

All tariffs count declared bounded operations and 64-bit storage words, not
CPU time or Python allocations. Every arithmetic operand in these services
fits one word. Table bitsets use separate 64-bit words. Audit snapshots,
ResourceRecord construction and JSON serialization are harness operations;
they never supply an answer to an unbought learner query. A deployment must
call ``registry_setup`` once for its actual source closure; the answer methods
do not repeatedly charge code procurement. Setup and per-answer costs are
separate. Denied answer calls return their spent resources and no answer.

API:
  make_query(p, a, query_id) -> immutable A.Query (public input construction)
  expert_predictions(query, meter) -> tuple of four binary predictions
  checked_purchase(query, limit_total=CHECKED_PURCHASE_CAP) -> ServiceResult
  direct_exact(query, limit_total=DIRECT_CAP) -> ServiceResult
  ExactCache(capacity=248, limit_total=...) -> .answer(query), .setup_resources
  QuadraticResidueTable(limit_total=...) -> .answer(query), .setup_resources
  registry_setup(source_paths=None, limit_total=...) -> RegistryResult

The expert meter needs pay(category, operation, units) and pay_many(tuple).
Local service/control meters are the old A.Meter. The caller reserves the
declared cap, then absorbs returned actual resources into its whole-policy
bill. A source registry or object constructor that cannot finish raises
ServiceSetupError with the exact spent ResourceRecord. No cost is refunded
merely because an operation fails. These objects are trusted local programs,
not security sandboxes or cryptographically authenticated external services.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import importlib.util
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
ADAPTER_PATH = HERE / "07_computation_adapter.py"
_spec = importlib.util.spec_from_file_location("_r_p3ba_service_adapter", ADAPTER_PATH)
assert _spec is not None and _spec.loader is not None
A = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = A
_spec.loader.exec_module(A)

VERSION = "r-p3ba-euler-services-v1.1"
FAMILY = "euler-248-public-modular-equality-v1"
SOURCE_VERSION = "modexp-input-v1"
PRIMES = (17, 31, 47, 61, 97)
OFFSETS = (0, 16, 46, 92, 152)
POPULATION_SIZE = 248
EXPERT_NAMES = ("constant_zero", "constant_one", "odd_base", "lower_half_base")
FAMILY_ADMISSION_CAP = 64
CHECKED_CORE_CAP = A.MAX_COLD_COMPLETION_UNITS
CHECKED_PURCHASE_CAP = FAMILY_ADMISSION_CAP + CHECKED_CORE_CAP
DIRECT_CAP = 512
MAX_CACHE_CAPACITY = POPULATION_SIZE
MAX_SOURCE_FILES = 32
MAX_SOURCE_BYTES = 1_048_576
MAX_SOURCE_PATH_BYTES = 4096
MAX_SETUP_UNITS = A.MAX_TOTAL_UNITS


@dataclass(frozen=True)
class ResourceRecord:
    """Immutable actual debits; record() is harness-only serialization."""
    total: int
    by_category: tuple[tuple[str, int], ...]
    operations: tuple[tuple[str, str, int], ...]

    def record(self):
        return {
            "total": self.total,
            "by_category": dict(self.by_category),
            "operations": [
                {"category": c, "operation": op, "units": units}
                for c, op, units in self.operations
            ],
        }


@dataclass(frozen=True)
class ServiceResult:
    query_id: str
    claim_key: tuple
    answer: int | None
    residue: int | None
    status: str
    provider: str
    provider_version: str
    checked: bool
    resources: ResourceRecord
    detail: str = ""

    @property
    def successful(self):
        return self.status == "success"

    def record(self):
        return {
            "query_id": self.query_id,
            "claim_key": list(self.claim_key),
            "answer": self.answer,
            "residue": self.residue,
            "status": self.status,
            "provider": self.provider,
            "provider_version": self.provider_version,
            "checked": self.checked,
            "resources": self.resources.record(),
            "detail": self.detail,
        }


@dataclass(frozen=True)
class RegistryResult:
    files: tuple[tuple[str, int, str], ...]
    resources: ResourceRecord

    def record(self):
        return {
            "version": VERSION,
            "files": [{"path": p, "bytes": n, "sha256": h} for p, n, h in self.files],
            "resources": self.resources.record(),
        }


class ServiceSetupError(RuntimeError):
    def __init__(self, message, resources):
        super().__init__(message)
        self.resources = resources


def _words(nbytes):
    return max(1, (nbytes + 7) // 8)


def _snapshot(meter):
    """Bounded audit counters, never a query-information API."""
    return meter.total, dict(meter.by_category), dict(meter.operations)


def _resources(meter, before=None):
    old_total, old_categories, old_operations = before or (0, {}, {})
    categories = tuple((c, meter.by_category[c] - old_categories.get(c, 0))
                       for c in A.CATEGORIES)
    operations = []
    for name, value in sorted(meter.operations.items()):
        delta = value - old_operations.get(name, 0)
        if delta:
            category, operation = name.split(".", 1)
            operations.append((category, operation, delta))
    result = ResourceRecord(meter.total - old_total, categories, tuple(operations))
    if result.total != sum(v for _, v in categories):
        raise AssertionError("Resource categories do not sum to total.")
    if result.total != sum(v for _, _, v in operations):
        raise AssertionError("Named operations do not sum to total.")
    return result


def _combine(*records):
    categories = {c: 0 for c in A.CATEGORIES}
    operations = {}
    for record in records:
        for c, v in record.by_category:
            categories[c] += v
        for c, op, v in record.operations:
            operations[(c, op)] = operations.get((c, op), 0) + v
    return ResourceRecord(sum(r.total for r in records), tuple(categories.items()),
                          tuple((c, op, v) for (c, op), v in sorted(operations.items())))


def _admit_euler(query, meter):
    """Pay the actual fixed-word family checks; return the prime index."""
    meter.pay("admission", "euler_query_type_check", 1)
    if type(query) is not A.Query:
        raise A.ProtocolError("Use this module's exact immutable A.Query type.")
    # The old adapter's bounded scalar/string-validation tariff is retained.
    meter.pay_many((("admission", "euler_scalar_field_check", 8),
                    ("admission", "euler_identity_word_read", query.key_words)))
    query.__post_init__()
    prime_index = None
    for index, p in enumerate(PRIMES):
        meter.pay("admission", "euler_prime_membership_compare", 1)
        if query.m == p:
            prime_index = index
            break
    meter.pay_many((("admission", "euler_exponent_subtract_shift", 2),
                    ("admission", "euler_family_scalar_compare", 4),
                    ("admission", "euler_source_word_compare", _words(len(SOURCE_VERSION)))))
    expected_n = (query.m - 1) // 2
    if (prime_index is None or not 1 <= query.a < query.m or query.n != expected_n
            or query.r != 1 or query.source_version != SOURCE_VERSION):
        raise A.ProtocolError("Query is outside the source-bound 248 Euler claims.")
    return prime_index


def make_query(p, a, query_id):
    """Construct public input; deployed admission is paid by each service.

    Population generation and this dataclass allocation belong to the caller's
    public-input supplier. This function performs no answer computation.
    """
    if type(p) is not int or p not in PRIMES or type(a) is not int or not 1 <= a < p:
        raise A.ProtocolError("Public Euler query requires a listed prime and nonzero residue.")
    return A.Query(query_id, a, (p - 1) // 2, p, 1,
                   source_version=SOURCE_VERSION, semantics_version=A.SEMANTICS_VERSION)


def expert_predictions(query, meter):
    """Four fixed, stateless, public-input binary experts; no paid labels read."""
    _admit_euler(query, meter)
    meter.pay_many((("forecast", "fixed_binary_constant_read", 2),
                    ("forecast", "odd_base_bit_test", 1),
                    ("forecast", "lower_half_double_and_compare", 2),
                    ("storage", "expert_prediction_word_write", len(EXPERT_NAMES))))
    return (0, 1, query.a & 1, int(2 * query.a < query.m))


def _identity(query):
    if type(query) is A.Query:
        return query.query_id, query.claim_key
    return "rejected-input", ()


def _result(query, answer, residue, status, provider, checked, resources, detail=""):
    query_id, claim_key = _identity(query)
    return ServiceResult(query_id, claim_key, answer, residue, status, provider,
                         VERSION + ";adapter=" + A.VERSION, checked, resources, detail)


def _failure(query, exc, provider, resources):
    status = "budget_exhausted" if isinstance(exc, A.BudgetExhausted) else "rejected"
    return _result(query, None, None, status, provider, False, resources, str(exc))


def checked_purchase(query, limit_total=CHECKED_PURCHASE_CAP):
    """Cold checked receipt, with admitted family overhead plus old 1024 cap.

    The family admission and old core have separate meters so the old core's
    accepted resource boundary is unchanged. A successful result is bound to
    the full claim key and request identity. No pending job/cache survives a
    cold call. Budget failure releases no uncompleted answer.
    """
    A._nat(limit_total, A.MAX_TOTAL_UNITS, "checked purchase total limit")
    front = A.Meter(min(limit_total, FAMILY_ADMISSION_CAP))
    core = None
    provider = "cold_checked_modular_adapter"
    try:
        _admit_euler(query, front)
        core = A.Meter(min(CHECKED_CORE_CAP, limit_total - front.total))
        adapter = A.Adapter(core, cache_cap=0)
        answer = adapter.lookup(query)
        if answer is None:
            answer = adapter.shortcut(query)
        if answer is None:
            handle = adapter.start(query)
            progress = adapter.advance(handle, A.MAX_FULL_TRANSACTIONS)
            if not progress.checked_ready:
                # The cold object's already paid temporary state is discarded;
                # its Python cleanup is harness scope, not future policy work.
                return _result(query, None, None, "budget_exhausted", provider, False,
                               _combine(_resources(front), _resources(core)),
                               "Admitted binary completion did not reach checked-ready.")
            answer = adapter.acquire(handle)
        if answer.query_id != query.query_id or answer.claim_key != query.claim_key:
            raise AssertionError("Old adapter returned an unbound receipt.")
        return _result(query, answer.answer, answer.residue, "success", provider, True,
                       _combine(_resources(front), _resources(core)), answer.provenance)
    except (A.BudgetExhausted, A.ProtocolError) as exc:
        records = [_resources(front)]
        if core is not None:
            records.append(_resources(core))
        return _failure(query, exc, provider, _combine(*records))


def _binary_residue(query, meter):
    """Ordinary efficient right-to-left binary modular exponentiation."""
    meter.pay_many((("solve", "direct_initial_modular_reduce", 2),
                    ("storage", "direct_initial_state_word_write", 3)))
    result, base, exponent = 1 % query.m, query.a % query.m, query.n
    while True:
        meter.pay("solve", "direct_exponent_loop_guard", 1)
        if not exponent:
            break
        meter.pay("solve", "direct_exponent_bit_test", 1)
        odd = exponent & 1
        if odd:
            meter.pay_many((("solve", "direct_modular_multiply", 1),
                            ("solve", "direct_modular_reduce", 1),
                            ("storage", "direct_result_word_write", 1)))
            result = (result * base) % query.m
        meter.pay_many((("solve", "direct_exponent_shift", 1),
                        ("storage", "direct_exponent_word_write", 1),
                        ("solve", "direct_final_iteration_test", 1)))
        exponent >>= 1
        if exponent:
            meter.pay_many((("solve", "direct_modular_square", 1),
                            ("solve", "direct_modular_reduce", 1),
                            ("storage", "direct_base_word_write", 1)))
            base = (base * base) % query.m
    return result


def _emit(query, residue, meter):
    meter.pay_many((("solve", "direct_target_comparison", 1),
                    ("forecast", "emit_binary_terminal_action", 1),
                    ("storage", "terminal_action_word_write", 1)))
    return int(residue == query.r)


def direct_exact(query, limit_total=DIRECT_CAP):
    """Exact local action, without a mandatory second computation/checker."""
    meter = A.Meter(limit_total)
    provider = "ordinary_direct_binary"
    try:
        _admit_euler(query, meter)
        residue = _binary_residue(query, meter)
        answer = _emit(query, residue, meter)
        return _result(query, answer, residue, "success", provider, False, _resources(meter))
    except (A.BudgetExhausted, A.ProtocolError) as exc:
        return _failure(query, exc, provider, _resources(meter))


class ExactCache:
    """Ordinary direct-address semantic residue cache for this finite family.

    The source-fixed prime, exponent and target restrictions make (p,a) an
    exact semantic key. Slots cover all 248 possible keys; retained residues
    are capped by ``capacity`` using paid FIFO replacement. Fresh request IDs
    reuse the same key. A miss runs the direct solver, not the checked service.
    Setup includes empty slots and the bounded FIFO ring. The cache has no
    precomputed answers and its hit/miss provenance is explicit.
    """
    def __init__(self, capacity=MAX_CACHE_CAPACITY, limit_total=MAX_SETUP_UNITS):
        self.meter = A.Meter(limit_total)
        self.capacity = capacity
        try:
            self.meter.pay("admission", "cache_capacity_check", 1)
            A._nat(capacity, MAX_CACHE_CAPACITY, "cache capacity")
            self.meter.pay_many((("storage", "semantic_cache_empty_slot_write", POPULATION_SIZE),
                                 ("storage", "semantic_cache_fifo_empty_word_write", capacity),
                                 ("storage", "semantic_cache_header_word_write", 6)))
            self._slots = [None] * POPULATION_SIZE
            self._fifo = [None] * capacity
            self._size = 0
            self._cursor = 0
            self.setup_resources = _resources(self.meter)
        except (A.BudgetExhausted, A.ProtocolError) as exc:
            raise ServiceSetupError(str(exc), _resources(self.meter)) from exc

    def answer(self, query):
        before = _snapshot(self.meter)
        provider = "ordinary_exact_semantic_cache"
        try:
            p_index = _admit_euler(query, self.meter)
            self.meter.pay_many((("cache", "semantic_cache_offset_read", 1),
                                 ("cache", "semantic_cache_address_arithmetic", 2),
                                 ("storage", "semantic_cache_slot_read", 1),
                                 ("cache", "semantic_cache_empty_test", 1)))
            index = OFFSETS[p_index] + query.a - 1
            residue = self._slots[index]
            if residue is not None:
                answer = _emit(query, residue, self.meter)
                return _result(query, answer, residue, "success", provider, False,
                               _resources(self.meter, before), "semantic_cache_hit")
            residue = _binary_residue(query, self.meter)
            self.meter.pay("cache", "semantic_cache_capacity_branch", 1)
            charges = [("solve", "direct_target_comparison", 1),
                       ("forecast", "emit_binary_terminal_action", 1),
                       ("storage", "terminal_action_word_write", 1)]
            if self.capacity:
                # Read the ring position and reserve every mutation and output
                # before publishing any new knowledge in the cache.
                charges += [("cache", "semantic_cache_full_test", 1),
                            ("storage", "semantic_cache_fifo_read", 1),
                            ("storage", "semantic_cache_residue_write", 1),
                            ("storage", "semantic_cache_fifo_write", 1),
                            ("cache", "semantic_cache_cursor_add_reduce", 2),
                            ("storage", "semantic_cache_cursor_write", 1)]
                if self._size == self.capacity:
                    charges.append(("storage", "semantic_cache_evicted_slot_clear", 1))
                else:
                    charges += [("cache", "semantic_cache_size_increment", 1),
                                ("storage", "semantic_cache_size_write", 1)]
            self.meter.pay_many(tuple(charges))
            answer = int(residue == query.r)
            if self.capacity:
                if self._size == self.capacity:
                    old_index = self._fifo[self._cursor]
                    self._slots[old_index] = None
                else:
                    self._size += 1
                self._slots[index] = residue
                self._fifo[self._cursor] = index
                self._cursor = (self._cursor + 1) % self.capacity
            return _result(query, answer, residue, "success", provider, False,
                           _resources(self.meter, before), "semantic_cache_miss_direct_compute")
        except (A.BudgetExhausted, A.ProtocolError) as exc:
            return _failure(query, exc, provider, _resources(self.meter, before))


def _paid_prime_check(p, meter):
    meter.pay("check", "prime_lower_bound_test", 1)
    if p < 2:
        return False
    meter.pay("storage", "prime_trial_divisor_initial_write", 1)
    divisor = 2
    while True:
        meter.pay_many((("check", "prime_trial_square", 1),
                        ("check", "prime_trial_bound_compare", 1)))
        if divisor * divisor > p:
            return True
        meter.pay_many((("check", "prime_trial_remainder", 1),
                        ("check", "prime_trial_zero_compare", 1)))
        if p % divisor == 0:
            return False
        meter.pay_many((("check", "prime_trial_increment", 1),
                        ("storage", "prime_trial_divisor_write", 1)))
        divisor += 1


class QuadraticResidueTable:
    """Paid exact square-membership table, with six 64-bit bitset words.

    For an admitted odd prime p, the nonzero squares are exactly the roots of
    z^((p-1)/2)=1. The elementary proof is in the service-design review. Paid
    trial division verifies the five primes. Construction enumerates only
    j=1,...,(p-1)/2: 124 real square/reduce evaluations, with no private labels.
    This ordinary exact action is not an independent per-query checked receipt.
    """
    def __init__(self, limit_total=MAX_SETUP_UNITS):
        self.meter = A.Meter(limit_total)
        try:
            self.meter.pay_many((("admission", "square_table_family_source_read", 8),
                                 ("storage", "square_table_header_word_write", 6)))
            tables = []
            for p in PRIMES:
                self.meter.pay("admission", "square_table_public_prime_read", 1)
                if not _paid_prime_check(p, self.meter):
                    raise A.ProtocolError("Table construction requires the admitted primes.")
                self.meter.pay_many((("solve", "square_table_word_count_add_divide", 2),
                                     ("solve", "square_table_half_range_subtract_divide", 2)))
                nwords = (p + 63) // 64
                half = (p - 1) // 2
                self.meter.pay_many((("storage", "square_table_zero_word_write", nwords),
                                     ("storage", "square_table_loop_initial_write", 1)))
                words = [0] * nwords
                j = 1
                while True:
                    self.meter.pay("solve", "square_table_loop_bound_compare", 1)
                    if j > half:
                        break
                    self.meter.pay_many((("solve", "square_table_modular_square", 1),
                                         ("solve", "square_table_modular_reduce", 1),
                                         ("solve", "square_table_word_divide_remainder", 2),
                                         ("solve", "square_table_mask_shift", 1),
                                         ("storage", "square_table_word_read", 1),
                                         ("solve", "square_table_bit_or", 1),
                                         ("storage", "square_table_word_write", 1),
                                         ("solve", "square_table_loop_increment", 1),
                                         ("storage", "square_table_loop_index_write", 1)))
                    residue = (j * j) % p
                    word_index, bit_index = divmod(residue, 64)
                    words[word_index] |= 1 << bit_index
                    j += 1
                self.meter.pay_many((("storage", "square_table_final_word_copy", nwords),
                                     ("storage", "square_table_prime_table_reference_write", 1)))
                tables.append(tuple(words))
            self.meter.pay("storage", "square_table_final_reference_copy", len(PRIMES))
            self._tables = tuple(tables)
            self.setup_resources = _resources(self.meter)
        except (A.BudgetExhausted, A.ProtocolError) as exc:
            raise ServiceSetupError(str(exc), _resources(self.meter)) from exc

    def answer(self, query):
        before = _snapshot(self.meter)
        provider = "ordinary_quadratic_residue_table"
        try:
            p_index = _admit_euler(query, self.meter)
            self.meter.pay_many((("cache", "square_table_prime_table_read", 1),
                                 ("cache", "square_table_word_divide_remainder", 2),
                                 ("storage", "square_table_lookup_word_read", 1),
                                 ("solve", "square_table_lookup_shift_and_mask", 2),
                                 ("solve", "square_table_negative_residue_subtract", 1),
                                 ("solve", "square_table_implied_residue_select", 1),
                                 ("forecast", "emit_binary_terminal_action", 1),
                                 ("storage", "terminal_action_word_write", 1)))
            word_index, bit_index = divmod(query.a, 64)
            answer = (self._tables[p_index][word_index] >> bit_index) & 1
            negative_residue = query.m - 1
            residue = 1 if answer else negative_residue
            return _result(query, answer, residue, "success", provider, False,
                           _resources(self.meter, before), "exact_public_square_membership")
        except (A.BudgetExhausted, A.ProtocolError) as exc:
            return _failure(query, exc, provider, _resources(self.meter, before))


def registry_setup(source_paths=None, *, limit_total=MAX_SETUP_UNITS):
    """Pay a caller-selected standalone source closure exactly once.

    Each file is charged for path admission, stat, actual 64-bit-word read and
    SHA-256 processing, and retained path/hash/size. Source binding is explicit;
    this bounded tariff is not a machine-code loading or human-proof cost.
    Path and source-byte caps are checked. A concurrent source change rejects
    the registry after preserving already spent costs.
    """
    meter = A.Meter(limit_total)
    try:
        meter.pay("admission", "source_registry_file_count_check", 1)
        if source_paths is not None and type(source_paths) not in (tuple, list):
            raise A.ProtocolError("Source closure must be an explicit bounded list or tuple.")
        paths = (HERE / "07_selective_feedback_service.py", ADAPTER_PATH) if source_paths is None else source_paths
        if not 1 <= len(paths) <= MAX_SOURCE_FILES:
            raise A.ProtocolError("Source registry file count is outside its cap.")
        records = []
        seen = set()
        for raw_path in paths:
            path = Path(raw_path).resolve()
            label = str(path)
            encoded = label.encode("utf-8")
            meter.pay("admission", "source_registry_path_length_check", 1)
            if len(encoded) > MAX_SOURCE_PATH_BYTES:
                raise A.ProtocolError("Source registry path exceeds its byte cap.")
            meter.pay_many((("admission", "source_registry_path_word_read", _words(len(encoded))),
                            ("admission", "source_registry_duplicate_lookup", 1),
                            ("profile", "source_registry_file_stat", 1)))
            if label in seen:
                raise A.ProtocolError("A standalone source closure must not charge duplicate paths.")
            seen.add(label)
            size = path.stat().st_size
            meter.pay("admission", "source_registry_file_size_check", 1)
            if not 0 <= size <= MAX_SOURCE_BYTES:
                raise A.ProtocolError("Source registry file exceeds its byte cap.")
            words = _words(size)
            meter.pay_many((("profile", "source_registry_source_word_read", words),
                            ("profile", "source_registry_sha256_word", words)))
            data = path.read_bytes()
            if len(data) != size:
                raise A.ProtocolError("Source changed length during registry acquisition.")
            digest = hashlib.sha256(data).hexdigest()
            meter.pay_many((("storage", "source_registry_hash_word_write", 4),
                            ("storage", "source_registry_path_word_write", _words(len(encoded))),
                            ("storage", "source_registry_size_word_write", 1)))
            records.append((label, size, digest))
        return RegistryResult(tuple(records), _resources(meter))
    except (A.BudgetExhausted, A.ProtocolError, OSError) as exc:
        raise ServiceSetupError(str(exc), _resources(meter)) from exc
