"""P3-08 bounded CNF decision-program services. DEVELOPMENT ONLY.

Contributor: ChatGPT (GPT-6 Astra Pro), delegated ordinary-control implementer.
The finite SAT answer is deterministic. Public input generation never calls a
truth solver. Both ordinary and candidate controllers may use every operation
here. A successful receipt is bound to full immutable content and versions.

The provider uses a common bounded 64-bit-word operation tariff. It prepays
final output/cleanup before computing truth. SAT witnesses are checked by a
separate clause evaluator. UNSAT uses a checked empty/opposing-unit certificate
or independent complete assignment enumeration. No incomplete search emits a false label.
Receipt objects are trusted local-provider records, not authenticated external
proofs. Audit JSON is an evaluator-only export, not a policy information API.
"""
from __future__ import annotations

from dataclasses import dataclass
import itertools
import random

from p308_common import C, ResourceRecord, resources


VERSION = "p308-bounded-cnf-services-v1.1"
SEMANTICS_VERSION = "bounded-cnf-sat-v1"
SOURCE_VERSION = "cnf-input-v1"
PROVIDER = "bounded_cnf_checked"
MAX_VARIABLES = 12
MAX_CLAUSES = 64
MAX_WIDTH = 4
MAX_LABEL = 128
MAX_CACHE = 64
SERVICE_CAP = 1_000_000_000
EXPERT_NAMES = ("constant_unsat", "constant_sat", "sparse_sat",
                "unit_consistency_sat", "pure_coverage_sat", "literal_balance_sat")
EXPERT_CAP = 8192


class Rejected(ValueError):
    """An input or receipt is outside this declared finite local contract."""


def _label(value):
    if (type(value) is not str or not 1 <= len(value) <= MAX_LABEL
            or not value.isascii()):
        raise Rejected("Identity/version must be capped nonempty ASCII.")


def _text_words(value):
    return max(1, (len(value) + 7) // 8)


@dataclass(frozen=True)
class Query:
    query_id: str
    variables: int
    clauses: tuple[tuple[int, ...], ...]
    source_version: str = SOURCE_VERSION
    semantics_version: str = SEMANTICS_VERSION

    def __post_init__(self):
        _label(self.query_id)
        _label(self.source_version)
        _label(self.semantics_version)
        if self.semantics_version != SEMANTICS_VERSION:
            raise Rejected("Unknown CNF interpretation.")
        if type(self.variables) is not int or not 1 <= self.variables <= MAX_VARIABLES:
            raise Rejected("Variable count outside [1,12].")
        if type(self.clauses) is not tuple or len(self.clauses) > MAX_CLAUSES:
            raise Rejected("Use at most 64 immutable clauses.")
        if any(type(clause) is not tuple or len(clause) > MAX_WIDTH
               for clause in self.clauses):
            raise Rejected("Use immutable clauses of width at most four.")
        for clause in self.clauses:
            if any(type(lit) is not int or lit == 0
                   or abs(lit) > self.variables for lit in clause):
                raise Rejected("Literals must be signed variable indices.")
            if any(a > b for a, b in zip(clause, clause[1:])):
                raise Rejected("Literals must be supplied in canonical sorted order.")
        if any(a > b for a, b in zip(self.clauses, self.clauses[1:])):
            raise Rejected("Clauses must be supplied in canonical sorted order.")

    @property
    def claim_key(self):
        return (self.semantics_version, self.source_version,
                self.variables, self.clauses)

    @property
    def literal_count(self):
        return sum(len(clause) for clause in self.clauses)

    @property
    def key_words(self):
        # Each scalar/literal and each tuple length fits a single 64-bit word.
        return (4 + _text_words(self.semantics_version)
                + _text_words(self.source_version)
                + len(self.clauses) + self.literal_count)

    def record(self):
        return {"query_id": self.query_id, "variables": self.variables,
                "clauses": [list(c) for c in self.clauses],
                "source_version": self.source_version,
                "semantics_version": self.semantics_version}


def make_query(query_id, variables, clauses, source_version=SOURCE_VERSION):
    """Public supplier conversion; deployed admission is charged separately.

    Sorting defines the admitted public encoding; duplicates and tautologies
    are retained. It performs no truth computation. Noncanonical raw inputs are
    not accepted by Query or implicitly normalized for free by a controller.
    """
    if type(clauses) not in (tuple, list):
        raise Rejected("Clause supplier must provide a finite sequence.")
    if len(clauses) > MAX_CLAUSES:
        raise Rejected("Too many supplier clauses.")
    if any(type(c) not in (tuple, list) or len(c) > MAX_WIDTH for c in clauses):
        raise Rejected("Clause supplier width/type.")
    canonical = tuple(sorted(tuple(sorted(c)) for c in clauses))
    return Query(query_id, variables, canonical, source_version)


def _snapshot(meter):
    return meter.snapshot()


@dataclass(frozen=True)
class Receipt:
    query_id: str
    claim_key: tuple
    answer: int | None
    checked: bool
    status: str
    provider: str
    provider_version: str
    resources: ResourceRecord
    witness: int | None = None
    detail: str = ""

    @property
    def successful(self):
        return self.status == "success"

    def record(self):
        return {"query_id": self.query_id, "claim_key": self.claim_key,
                "answer": self.answer, "checked": self.checked,
                "status": self.status, "provider": self.provider,
                "provider_version": self.provider_version,
                "resources": self.resources.record(),
                "witness": self.witness, "detail": self.detail}


def _admit(query, meter):
    # Type/shape rejection is bounded before traversing caller content.
    meter.pay("admission", "cnf_exact_query_type", 1)
    if type(query) is not Query:
        raise Rejected("Use this exact immutable Query class.")
    meter.pay_many((("admission", "cnf_scalar_and_version_validation", 16),
                    ("admission", "cnf_input_identity_words", query.key_words
                     + _text_words(query.query_id)),
                    ("admission", "cnf_canonical_order_comparisons",
                     query.literal_count + MAX_WIDTH * len(query.clauses)),
                    ("admission", "cnf_literal_validation",
                     3 * query.literal_count + len(query.clauses))))
    query.__post_init__()


def _prepay_finish(query, meter):
    # This is a reserved, fully charged service envelope, not a later refund.
    # Max output includes the full key, answer/status, bounded witness and detail.
    meter.pay_many((("output", "cnf_final_response_prepaid", 64 + query.key_words
                     + _text_words(query.query_id)),
                    ("storage", "cnf_final_cleanup_prepaid",
                     64 + 4 * query.variables + query.key_words)))


def _enumeration(query, meter, category="solve"):
    """Producer enumeration, early SAT stopping, complete UNSAT otherwise."""
    meter.pay(category, "enumeration_horizon_shift", 2)
    horizon = 1 << query.variables
    for assignment in range(horizon):
        meter.pay(category, "enumeration_assignment_loop", 2)
        satisfied = True
        for clause in query.clauses:
            meter.pay(category, "enumeration_clause_read", 2)
            clause_true = False
            for literal in clause:
                meter.pay(category, "enumeration_literal_evaluate", 6)
                value = bool(assignment & (1 << (abs(literal) - 1)))
                if value == (literal > 0):
                    clause_true = True
                    break
            meter.pay(category, "enumeration_clause_branch", 1)
            if not clause_true:
                satisfied = False
                break
        meter.pay(category, "enumeration_assignment_branch", 1)
        if satisfied:
            return 1, assignment
    return 0, None


def _verify_witness(query, witness, meter):
    """Independent signed-bit checker; no producer helper is reused."""
    meter.pay_many((("check", "witness_scalar_range", 4),
                    ("storage", "witness_word_read", 1)))
    if type(witness) is not int or not 0 <= witness < 1 << query.variables:
        return False
    for clause in query.clauses:
        meter.pay("check", "witness_clause_begin", 2)
        ok = False
        for lit in clause:
            meter.pay("check", "witness_literal_shift_sign_compare", 6)
            index = lit - 1 if lit > 0 else -lit - 1
            bit = (witness >> index) & 1
            if (bit == 1 and lit > 0) or (bit == 0 and lit < 0):
                ok = True
        meter.pay("check", "witness_clause_conjunction", 1)
        if not ok:
            return False
    return True


def _verify_unsat(query, meter):
    """Separate complete Boolean-tuple checker, paid before every operation."""
    meter.pay_many((("check", "unsat_product_initialization", 4),
                    ("storage", "unsat_bit_tuple_capacity", query.variables)))
    # itertools enumerates the same finite Cartesian product in another order;
    # each new tuple's n bits/control are explicitly charged.
    iterator = itertools.product((0, 1), repeat=query.variables)
    for _ in range(1 << query.variables):
        meter.pay_many((("check", "unsat_assignment_tuple_generate",
                         2 + query.variables),
                        ("storage", "unsat_assignment_tuple_write", query.variables)))
        bits = next(iterator)
        all_true = True
        for clause in query.clauses:
            meter.pay("check", "unsat_clause_begin", 2)
            truth = False
            for lit in clause:
                meter.pay("check", "unsat_signed_literal_index_compare", 6)
                if lit > 0:
                    lit_true = bits[lit - 1] == 1
                else:
                    lit_true = bits[-lit - 1] == 0
                truth = truth or lit_true
            meter.pay("check", "unsat_clause_conjunction", 1)
            if not truth:
                all_true = False
                break
        meter.pay("check", "unsat_assignment_existence_test", 1)
        if all_true:
            return False
    return True


def _simple_unsat_witness(query, meter):
    """Cheap ordinary empty-clause/opposing-singleton shortcut with evidence."""
    meter.pay_many((("solve", "simple_contradiction_array_initialization", 4),
                    ("storage", "simple_contradiction_clause_indices",
                     2 * (query.variables + 1))))
    positive = [None] * (query.variables + 1)
    negative = [None] * (query.variables + 1)
    for index, clause in enumerate(query.clauses):
        meter.pay("solve", "simple_contradiction_clause_shape", 3)
        if not clause:
            return ("empty", index)
        if len(clause) == 1:
            meter.pay_many((("solve", "simple_contradiction_unit_lookup", 6),
                            ("storage", "simple_contradiction_unit_index_write", 1)))
            lit = clause[0]
            variable = abs(lit)
            same, opposite = (positive, negative) if lit > 0 else (negative, positive)
            if opposite[variable] is not None:
                return ("opposing_units", index, opposite[variable])
            same[variable] = index
    return None


def _verify_simple_unsat(query, proof, meter):
    """Independent clause-index check for the ordinary cheap contradiction."""
    meter.pay("check", "simple_contradiction_proof_shape", 6)
    if type(proof) is not tuple or not proof:
        return False
    if proof[0] == "empty" and len(proof) == 2:
        index = proof[1]
        meter.pay("check", "empty_clause_index_and_content", 5)
        return (type(index) is int and 0 <= index < len(query.clauses)
                and query.clauses[index] == ())
    if proof[0] == "opposing_units" and len(proof) == 3:
        a, b = proof[1:]
        meter.pay("check", "opposing_unit_indices_and_literals", 12)
        if any(type(i) is not int or not 0 <= i < len(query.clauses) for i in (a, b)):
            return False
        left, right = query.clauses[a], query.clauses[b]
        return len(left) == len(right) == 1 and left[0] == -right[0]
    return False


def _dpll(query, meter):
    """Complete DPLL, unit and pure-literal propagation, public first-variable rule.

    Assignment masks are <=12 bits. Every propagation pass either assigns a
    variable, detects a terminal case or branches; recursion depth <= n.
    No generator property, learned label or evaluator state is read.
    """
    def search(true_mask, false_mask):
        meter.pay_many((("solve", "dpll_node_enter", 4),
                        ("storage", "dpll_frame_words", 4)))
        while True:
            meter.pay("solve", "dpll_propagation_pass_begin", 4)
            unresolved = []
            units = []
            positive = negative = 0
            for clause in query.clauses:
                meter.pay("solve", "dpll_clause_read", 2)
                unknown = []
                satisfied = False
                for literal in clause:
                    meter.pay("solve", "dpll_literal_read_assignment", 8)
                    bit = 1 << (abs(literal) - 1)
                    if (literal > 0 and true_mask & bit) or (
                            literal < 0 and false_mask & bit):
                        satisfied = True
                        break
                    if not ((true_mask | false_mask) & bit):
                        # Duplicate identical literals must count once for unit
                        # detection. Width<=4 bounds paid membership work.
                        meter.pay("solve", "dpll_unknown_literal_membership",
                                  1 + len(unknown))
                        if literal not in unknown:
                            meter.pay("storage", "dpll_unknown_literal_write", 1)
                            unknown.append(literal)
                meter.pay("solve", "dpll_clause_status_branch", 3)
                if satisfied:
                    continue
                if not unknown:
                    return None
                meter.pay("storage", "dpll_unresolved_clause_write",
                          1 + len(unknown))
                unresolved.append(tuple(unknown))
                if len(unknown) == 1:
                    meter.pay("storage", "dpll_unit_write", 1)
                    units.append(unknown[0])
                for lit in unknown:
                    meter.pay("solve", "dpll_polarity_collect", 4)
                    bit = 1 << (abs(lit) - 1)
                    if lit > 0:
                        positive |= bit
                    else:
                        negative |= bit
            meter.pay("solve", "dpll_formula_status_branch", 1)
            if not unresolved:
                return true_mask  # Unassigned variables are completed with zero.
            if units:
                for lit in units:
                    meter.pay("solve", "dpll_unit_assignment_check", 8)
                    bit = 1 << (abs(lit) - 1)
                    if lit > 0:
                        if false_mask & bit:
                            return None
                        true_mask |= bit
                    else:
                        if true_mask & bit:
                            return None
                        false_mask |= bit
                continue
            meter.pay("solve", "dpll_pure_literal_masks", 6)
            pure_positive = positive & ~negative
            pure_negative = negative & ~positive
            if pure_positive or pure_negative:
                meter.pay("solve", "dpll_pure_literal_assignment", 4)
                true_mask |= pure_positive
                false_mask |= pure_negative
                continue
            meter.pay("solve", "dpll_first_unassigned_selection", 6)
            choices = positive | negative
            bit = choices & -choices
            if not bit:
                raise AssertionError("Unresolved clause without an unassigned variable.")
            witness = search(true_mask | bit, false_mask)
            meter.pay("solve", "dpll_branch_result_read", 1)
            if witness is not None:
                return witness
            return search(true_mask, false_mask | bit)
    witness = search(0, 0)
    return (0, None) if witness is None else (1, witness)


def service_cap(query, solver="dpll"):
    """Public conservative source bound, excluding controller/registry work.

    Node count <=2^(n+1)-1, propagation passes <=n+1 per node; full
    independent UNSAT verification visits <=2^n assignments. This deliberately
    loose cap covers all literal, frame, admission and prepaid output charges.
    No truth evaluation is needed to compute it.
    """
    if type(query) is not Query or solver not in ("enumeration", "dpll"):
        raise Rejected("Unknown query/solver for public cap.")
    n, m, length = query.variables, len(query.clauses), query.literal_count
    admission_finish = 4096 + 16 * query.key_words
    enumeration = (1 << n) * (16 * length + 8 * m + 8 * n + 64)
    if solver == "enumeration":
        result = admission_finish + 2 * enumeration
    else:
        result = (admission_finish + enumeration
                  + ((1 << (n + 1)) - 1) * (n + 1)
                  * (24 * length + 24 * m + 128))
    if result > SERVICE_CAP:
        raise AssertionError("Static service cap is below admitted source envelope.")
    return result


def checked_purchase(query, limit_total=SERVICE_CAP, solver="dpll"):
    """Return a source-bound checked answer or a spent-cost failure receipt."""
    meter = C.CostMeter(limit_total)
    query_id, key = ("rejected-input", ())
    if type(query) is Query:
        query_id, key = query.query_id, query.claim_key
    answer = witness = None
    status, detail = "rejected", ""
    checked = False
    try:
        meter.pay("admission", "cnf_solver_name_check", 1)
        if solver not in ("enumeration", "dpll"):
            raise Rejected("Unknown public exact solver.")
        _admit(query, meter)
        _prepay_finish(query, meter)
        simple_proof = _simple_unsat_witness(query, meter) if solver == "dpll" else None
        if simple_proof is not None:
            candidate, candidate_witness = 0, None
        else:
            candidate, candidate_witness = (
                _enumeration(query, meter) if solver == "enumeration"
                else _dpll(query, meter))
        meter.pay("check", "cnf_candidate_type_check", 4)
        if (type(candidate) is not int or candidate not in (0, 1)
                or (candidate == 0 and candidate_witness is not None)):
            raise Rejected("Producer did not return an exact binary candidate.")
        if simple_proof is not None:
            valid = _verify_simple_unsat(query, simple_proof, meter)
        elif candidate == 1:
            valid = _verify_witness(query, candidate_witness, meter)
        else:
            valid = _verify_unsat(query, meter)
        meter.pay("check", "cnf_candidate_checker_agreement", 2)
        if not valid:
            raise Rejected("Independent checker rejected proposed answer.")
        meter.pay_many((("acquisition", "cnf_checked_answer_release", 8),
                        ("storage", "cnf_checked_receipt_words", 16 + query.key_words)))
        answer, witness, checked, status = candidate, candidate_witness, True, "success"
        detail = ("SAT witness checked" if answer else
                  "UNSAT cheap contradiction checked" if simple_proof is not None else
                  "UNSAT independently checked by all assignments")
    except C.BudgetExceeded as exc:
        status, detail = "budget_exhausted", str(exc)[:192]
    except Rejected as exc:
        status, detail = "rejected", str(exc)[:192]
    return Receipt(query_id, key, answer, checked, status, PROVIDER,
                   VERSION, resources(meter), witness, detail)


def expert_predictions(query, meter):
    """Six public syntactic binary predictors; no paid/evaluator labels."""
    _admit(query, meter)
    meter.pay_many((("forecast", "cnf_expert_constants_and_dimensions", 8),
                    ("storage", "cnf_expert_feature_state_initialization", 8)))
    unit_positive = unit_negative = positive = negative = 0
    positive_count = negative_count = 0
    for clause in query.clauses:
        meter.pay("forecast", "cnf_expert_clause_length", 2)
        if len(clause) == 1:
            meter.pay("forecast", "cnf_expert_unit_bit", 4)
            literal = clause[0]
            if literal > 0:
                unit_positive |= 1 << (literal - 1)
            else:
                unit_negative |= 1 << (-literal - 1)
        for literal in clause:
            meter.pay("forecast", "cnf_expert_sign_feature", 6)
            if literal > 0:
                positive |= 1 << (literal - 1)
                positive_count += 1
            else:
                negative |= 1 << (-literal - 1)
                negative_count += 1
    meter.pay("forecast", "cnf_expert_pure_masks", 4)
    pure_positive, pure_negative = positive & ~negative, negative & ~positive
    covered = True
    for clause in query.clauses:
        meter.pay("forecast", "cnf_expert_pure_clause_begin", 2)
        clause_covered = False
        for literal in clause:
            meter.pay("forecast", "cnf_expert_pure_literal_test", 5)
            bit = 1 << (abs(literal) - 1)
            clause_covered = clause_covered or bool(
                (pure_positive if literal > 0 else pure_negative) & bit)
        covered = covered and clause_covered
    meter.pay_many((("forecast", "cnf_expert_final_binary_comparisons", 10),
                    ("output", "cnf_expert_prediction_words", len(EXPERT_NAMES))))
    return (0, 1, int(len(query.clauses) <= 3 * query.variables),
            int(not (unit_positive & unit_negative)),
            int(covered), int(positive_count >= negative_count))


def cost_proxy(query, meter):
    """Public shape-only estimate; no claim of optimal value of computation."""
    _admit(query, meter)
    meter.pay("forecast", "cnf_shape_cost_proxy_arithmetic", 8)
    return 128 + query.key_words + (1 << query.variables) * max(1, query.literal_count)


class ExactCache:
    """Shared ordinary/candidate FIFO exact cache, no free prepopulation.

    The key is full admitted content plus source and semantics versions.
    A new request identifier may reuse the same mathematical result. Returned
    records bind the new request and cite a cache provider. Entry acquisition
    was paid at remember(); lookup does not repay full solving costs.
    """
    def __init__(self, capacity=MAX_CACHE):
        if type(capacity) is not int or not 0 <= capacity <= MAX_CACHE:
            raise Rejected("Cache capacity outside [0,64].")
        self.capacity = capacity
        self._entries = []
        self._initialized = False

    def _setup(self, meter):
        if not self._initialized:
            meter.pay_many((("admission", "cnf_cache_capacity_validation", 2),
                            ("storage", "cnf_cache_header_words", 4)))
            self._initialized = True

    def lookup(self, query, meter):
        before = _snapshot(meter)
        self._setup(meter)
        _admit(query, meter)
        for key, answer, witness, key_words in self._entries:
            meter.pay_many((("cache", "cnf_cache_key_full_compare",
                             1 + max(query.key_words, key_words)),
                            ("storage", "cnf_cache_entry_pointer_read", 1)))
            if key == query.claim_key:
                meter.pay_many((("check", "cnf_cache_current_key_answer_binding",
                                 8 + query.key_words),
                                ("output", "cnf_cache_rebound_receipt_words",
                                 32 + query.key_words)))
                return Receipt(query.query_id, query.claim_key, answer, True,
                               "success", "bounded_cnf_exact_cache", VERSION,
                               resources(meter, before), witness,
                               "Reused paid same-content same-version answer")
        return None

    def remember(self, query, receipt, meter):
        self._setup(meter)
        _admit(query, meter)
        meter.pay("check", "cnf_cache_receipt_binding", 16 + query.key_words)
        if (type(receipt) is not Receipt or receipt.status != "success"
                or receipt.checked is not True or type(receipt.answer) is not int
                or receipt.answer not in (0, 1)
                or receipt.query_id != query.query_id or receipt.claim_key != query.claim_key
                or receipt.provider not in (PROVIDER, "bounded_cnf_exact_cache")
                or receipt.provider_version != VERSION):
            raise Rejected("Cache insertion requires this provider's bound checked result.")
        if not self.capacity:
            return False
        for key, answer, witness, key_words in self._entries:
            meter.pay("cache", "cnf_cache_insert_full_key_compare",
                      1 + max(query.key_words, key_words))
            if key == query.claim_key:
                if answer != receipt.answer:
                    raise Rejected("Conflicting exact same-key answers.")
                return False
        meter.pay("storage", "cnf_cache_retained_entry_write", 8 + query.key_words)
        if len(self._entries) >= self.capacity:
            meter.pay("cache", "cnf_cache_fifo_eviction_shift", 2 + len(self._entries))
            self._entries.pop(0)
        self._entries.append((query.claim_key, receipt.answer, receipt.witness, query.key_words))
        return True

    @property
    def retained_words(self):
        return 4 + sum(8 + entry[3] for entry in self._entries)

    @property
    def entries(self):
        return len(self._entries)


def make_development_queries(seed=3081001, count=32, prefix="cnf-development"):
    """Public, label-independent cohort generation; all outputs DEVELOPMENT.

    Width/density/component cohorts are determined before any truth calculation.
    Every eighth item repeats a previous full formula under a new request ID.
    A source-version change can be applied by callers as an explicit new input.
    """
    if type(seed) is not int or type(count) is not int or not 1 <= count <= 8192:
        raise Rejected("Bounded development seed/count required.")
    _label(prefix)
    rng = random.Random(seed)
    queries = []
    variables = (4, 6, 8, 10, 12)
    for i in range(count):
        identity = f"{prefix}-{i:05d}"
        if i and i % 8 == 7:
            previous = queries[i - 7]
            queries.append(Query(identity, previous.variables, previous.clauses,
                                 previous.source_version))
            continue
        n = variables[i % len(variables)]
        cohort = i % 4
        m = min(MAX_CLAUSES, (2 + (i // 4) % 4) * n)
        clauses = []
        for j in range(m):
            if cohort == 0:
                width = rng.choice((1, 2))
                pool = list(range(1, n + 1))
            elif cohort == 1:
                width = 3
                pool = list(range(1, n + 1))
            elif cohort == 2:
                width = min(3, n // 2)
                half = j & 1
                pool = list(range(1 + half * (n // 2), 1 + (half + 1) * (n // 2)))
            else:
                width = rng.choice((2, 3, 4))
                pool = list(range(1, n + 1))
            chosen = rng.sample(pool, width)
            clauses.append(tuple(v if rng.randrange(2) else -v for v in chosen))
        queries.append(make_query(identity, n, clauses))
    return tuple(queries)
