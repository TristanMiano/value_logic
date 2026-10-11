"""Finite, paid, exact-quota selective feedback. DEVELOPMENT.

ChatGPT (GPT-6 Astra Pro), 2026-10-09 UTC.

Ordinary blocked product weights, with a checked current-answer service. The
probability theorem assumes a fixed exogenous query tape and independent fair
bits. Seeded bit tapes are reproducible development realizations, not proof of
that randomness premise. Only a purchased receipt may enter the update API.

The resource ledger is an explicit 64-bit-word tariff, not measured CPU cycles
or Python heap use. Integer arithmetic is charged by operand word sizes;
service invoices retain the existing adapter's actual abstract operations.
Trusted local Python/provider execution is the trust boundary. Dataclass and
source-version checks do not authenticate arbitrary hostile external receipts.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import importlib.util
from pathlib import Path
import random
import sys

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location(
    "_selective_feedback_service", HERE / "07_selective_feedback_service.py")
S = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = S
spec.loader.exec_module(S)

VERSION = "r-p3-b-a-blocked-prod-v1.2"
WORD_BITS = 64
MAX_HORIZON = 8192
MAX_BLOCK = 1024
MAX_EXPERTS = 32
MAX_ACTION_BITS = 32
MAX_UNITS = (1 << 62) - 1
CATEGORIES = tuple(S.A.CATEGORIES) + ("controller", "randomness", "output", "setup")


class Rejected(ValueError):
    """Outside the admitted finite contract; no performance claim is emitted."""


class BudgetExceeded(RuntimeError):
    """An atomic tariff charge was denied; earlier spending is retained."""


def nat(value, upper, name, *, minimum=0):
    if type(value) is not int or not minimum <= value <= upper:
        raise Rejected(f"{name} outside [{minimum}, {upper}].")
    return value


def ceil_log2(n):
    return (n - 1).bit_length()


def words(n):
    return max(1, (n.bit_length() + WORD_BITS - 1) // WORD_BITS)


@dataclass(frozen=True)
class Contract:
    horizon: int
    block_size: int
    expert_count: int
    action_bits: int = 16
    state_bits: int | None = None

    def __post_init__(self):
        nat(self.horizon, MAX_HORIZON, "horizon", minimum=1)
        nat(self.block_size, MAX_BLOCK, "block size", minimum=1)
        nat(self.expert_count, MAX_EXPERTS, "expert count", minimum=1)
        nat(self.action_bits, MAX_ACTION_BITS, "action bits", minimum=1)
        if self.state_bits is not None:
            nat(self.state_bits, 32, "fixed-state precision bits", minimum=1)
        if self.block_size & (self.block_size - 1):
            raise Rejected("Exact bounded-bit selectors require a power-of-two block.")
        if self.horizon % self.block_size:
            raise Rejected("The first executable contract requires equal complete blocks.")

    @property
    def quota(self):
        return self.horizon // self.block_size

    @property
    def k(self):
        return max(2, self.block_size - 1)

    @property
    def selector_bits(self):
        return ceil_log2(self.block_size)

    @property
    def random_bits(self):
        return self.quota * self.selector_bits + self.horizon * self.action_bits

    @property
    def individual_weight_bits(self):
        if self.state_bits is not None:
            return self.state_bits + ceil_log2(self.expert_count) + 1
        return 1 + self.quota * ceil_log2(self.k)

    @property
    def prediction_working_bits(self):
        if self.state_bits is not None:
            # M=N*2^s; normalization multiplies (M-N)*v_i <= M^2*K.
            return max(2 * self.individual_weight_bits + ceil_log2(self.k) + 2,
                       self.individual_weight_bits + self.action_bits + 2)
        return self.individual_weight_bits + ceil_log2(self.expert_count) + self.action_bits + 2

    @property
    def maximum_operand_bits(self):
        # A 32-bit extraction crossing a 64-bit word can create 95 bits.
        # Counters and bounded monetary-resource indices fit one 64-bit word.
        return max(95, self.prediction_working_bits)

    @property
    def working_words(self):
        return (self.prediction_working_bits + WORD_BITS - 1) // WORD_BITS

    def controller_cap(self, feature_cap):
        """Conservative tariff envelope; proof and enumeration audit it.

        Includes all supplied bit storage, every issued output, one receipt
        slot, public feature evaluation and weight updates. Source-registry
        setup and the cold checked-service reservation are separate terms.
        """
        nat(feature_cap, 4096, "per-query feature cap")
        n, z, h = self.expert_count, self.working_words, self.action_bits
        initial = 1024 + 4 * n * z + 2 * ((self.random_bits + 63) // 64)
        per_round = 512 + feature_cap + 16 * n * z + 8 * z * z + 8 * h
        per_block = 512 + 32 * n * z + 8 * self.selector_bits
        if self.state_bits is not None:
            per_block += n * (16 * z * z + 32 * z + 32)
        return initial + self.horizon * per_round + self.quota * per_block

    def record(self):
        return {
            "version": VERSION, "horizon": self.horizon,
            "block_size": self.block_size, "expert_count": self.expert_count,
            "action_bits": self.action_bits, "quota": self.quota,
            "state_bits": self.state_bits,
            "k": self.k, "random_bits": self.random_bits,
            "individual_weight_bits": self.individual_weight_bits,
            "prediction_working_bits": self.prediction_working_bits,
            "sampler_working_bits": 95,
            "maximum_operand_bits": self.maximum_operand_bits,
        }


class CostMeter:
    """Actual debits under the declared tariff, with separate reservations."""
    def __init__(self, limit_total=MAX_UNITS):
        self.limit_total = nat(limit_total, MAX_UNITS, "resource limit")
        self.total = 0
        self.by_category = Counter({name: 0 for name in CATEGORIES})
        self.operations = Counter()
        self.reservations = {}
        self.denials = 0

    @property
    def reserved(self):
        return sum(self.reservations.values())

    def pay(self, category, operation, units=1):
        self.pay_many(((category, operation, units),))

    def pay_many(self, charges):
        charges = tuple(charges)
        for category, operation, units in charges:
            if category not in CATEGORIES or type(operation) is not str or not operation:
                raise Rejected("Unknown resource category or empty operation name.")
            nat(units, MAX_UNITS, "charge")
        amount = sum(units for _, _, units in charges)
        if self.total + self.reserved + amount > self.limit_total:
            self.denials += 1
            raise BudgetExceeded("Tariff bundle denied before the described operation.")
        self.total += amount
        for category, operation, units in charges:
            self.by_category[category] += units
            self.operations[category, operation] += units

    def reserve(self, name, amount):
        nat(amount, MAX_UNITS, "reservation")
        if name in self.reservations:
            raise Rejected("Duplicate reservation.")
        if self.total + self.reserved + amount > self.limit_total:
            self.denials += 1
            raise BudgetExceeded("Insufficient resources to fund the admitted service.")
        self.reservations[name] = amount

    def absorb(self, record, component="service", *, reservation=None, release=0):
        """Debit a trusted completed child invoice, including a failed call.

        A caller invoking a child first reserves its entire advertised cap.
        Redemption releases exactly one cap, then debits actual work. It never
        creates fresh query positions from a refund.
        """
        rec = record.record() if hasattr(record, "record") else record
        charges = tuple((row["category"], component + ":" + row["operation"], row["units"])
                        for row in rec["operations"])
        if rec["total"] != sum(row[2] for row in charges):
            raise Rejected("Child invoice total does not equal its named debits.")
        expected = Counter()
        for category, _, amount in charges:
            expected[category] += amount
        if any(expected[c] != rec["by_category"].get(c, 0)
               for c in set(expected) | set(rec["by_category"])):
            raise Rejected("Child invoice categories disagree with named debits.")
        if reservation is not None:
            if reservation not in self.reservations or not 0 <= rec["total"] <= release <= self.reservations[reservation]:
                raise Rejected("Invoice exceeds its funded completion reservation.")
            self.reservations[reservation] -= release
            if not self.reservations[reservation]:
                del self.reservations[reservation]
        elif release:
            raise Rejected("Cannot release an unnamed reservation.")
        self.pay_many(charges)

    def snapshot(self):
        return {
            "limit_total": self.limit_total, "total": self.total,
            "by_category": dict(self.by_category),
            "operations": [{"category": c, "operation": op, "units": units}
                           for (c, op), units in sorted(self.operations.items())],
            "reservations": dict(self.reservations), "denials": self.denials,
        }


class BitTape:
    """A finite prepaid bit input, read in bounded <=32-bit chunks.

    Independent uniform supplied words instantiate the randomized contract.
    `seeded` is a deterministic development source with the same finite API.
    The bit string carries no mathematical-query answers.
    """
    def __init__(self, supplied_words, bit_count, meter, *, provenance):
        nat(bit_count, MAX_HORIZON * (MAX_ACTION_BITS + 10), "bit count")
        expected = (bit_count + 63) // 64
        if type(supplied_words) is not tuple or len(supplied_words) != expected:
            raise Rejected("Bit tape has the wrong finite word length.")
        meter.pay_many((("admission", "bit_tape_word_validation", expected),
                        ("storage", "bit_tape_word_retention", expected)))
        for value in supplied_words:
            nat(value, (1 << 64) - 1, "bit word")
        self._words = supplied_words
        self.bit_count, self.position, self.meter = bit_count, 0, meter
        self.provenance = provenance

    @classmethod
    def seeded(cls, bit_count, seed, meter):
        nat(seed, (1 << 64) - 1, "development seed")
        # The generation mechanism is outside the probability theorem. Charge
        # its fixed MT state/setup and generated words in development invoices.
        count = (bit_count + 63) // 64
        meter.pay_many((("randomness", "development_mt_state_initialization", 624),
                        ("storage", "development_mt_state_words", 624),
                        ("randomness", "development_mt_generated_words", count)))
        rng = random.Random(seed)
        return cls(tuple(rng.getrandbits(64) for _ in range(count)), bit_count,
                   meter, provenance=f"deterministic-development-mt-seed:{seed}")

    def take(self, count):
        nat(count, MAX_ACTION_BITS, "requested random bits")
        if self.position + count > self.bit_count:
            raise Rejected("Finite random-bit input exhausted.")
        self.meter.pay_many((("randomness", "supplied_bit_consumption", count),
                             ("controller", "bit_tape_extract_and_advance", 8)))
        if count == 0:
            return 0
        word, offset = divmod(self.position, 64)
        value = self._words[word] >> offset
        if offset + count > 64:
            value |= self._words[word + 1] << (64 - offset)
        self.position += count
        return value & ((1 << count) - 1)


@dataclass(frozen=True)
class Issued:
    index: int
    block: int
    query: object
    expert_actions: tuple[int, ...]
    numerator: int
    denominator: int
    prospective_action: int


@dataclass(frozen=True)
class Closed:
    issue: Issued
    purchased: bool
    terminal_action: int
    purchased_label: int | None


class FrozenProd:
    """Only fixed public expert predictions and selected receipts enter here."""
    def __init__(self, contract, meter, bits):
        if type(contract) is not Contract or type(meter) is not CostMeter or type(bits) is not BitTape:
            raise Rejected("Use the declared finite contract, meter and bit API.")
        if bits.bit_count != contract.random_bits:
            raise Rejected("Random-bit capacity must match the entire contract.")
        if bits.meter is not meter:
            raise Rejected("The learner and its paid bit input require the same meter.")
        self.contract, self.meter, self.bits = contract, meter, bits
        meter.pay_many((("admission", "learner_contract_validation", 16),
                        ("storage", "initial_weight_word_write", contract.expert_count),
                        ("storage", "learner_scalar_state_write", 16)))
        initial_weight = 1 if contract.state_bits is None else (1 << contract.state_bits)
        self.weights = tuple(initial_weight for _ in range(contract.expert_count))
        self.index = 0
        self.pending = None
        self.feedback = None
        self.block_mass = None
        self.purchase_count = 0
        self.peak_weight_bits = initial_weight.bit_length()
        self.peak_prediction_working_bits = initial_weight.bit_length()
        self.completed = False

    def _add(self, left, right):
        self.meter.pay("controller", "integer_add_word_tariff", 2 * max(words(left), words(right)) + 1)
        result = left + right
        self.peak_prediction_working_bits = max(self.peak_prediction_working_bits, result.bit_length())
        return result

    def issue(self, query, expert_actions):
        if self.completed or self.pending is not None or self.index >= self.contract.horizon:
            raise Rejected("Issue requires the next open round and no pending action.")
        self.meter.pay("admission", "public_issue_type_check", 1)
        if type(query) is not S.A.Query:
            raise Rejected("The declared immutable mathematical query is required.")
        self.meter.pay_many((("admission", "public_issue_and_prediction_checks", 16 + self.contract.expert_count),
                             ("storage", "public_query_word_read", query.key_words)))
        if (type(expert_actions) is not tuple or len(expert_actions) != self.contract.expert_count
                or any(type(x) is not int or x not in (0, 1) for x in expert_actions)):
            raise Rejected("The fixed expert library must emit exactly N binary actions.")
        if self.index % self.contract.block_size == 0:
            if self.feedback is not None:
                raise Rejected("Prior block feedback was not consumed.")
            total = 0
            for weight in self.weights:
                self.meter.pay("storage", "block_weight_word_read", words(weight))
                total = self._add(total, weight)
            self.block_mass = total
            self.meter.pay("storage", "block_total_mass_word_write", words(total))
        mass = 0
        for weight, action in zip(self.weights, expert_actions):
            self.meter.pay_many((("storage", "prediction_weight_word_read", words(weight)),
                                 ("forecast", "expert_action_branch", 1)))
            if action:
                mass = self._add(mass, weight)
        self.meter.pay("controller", "integer_shift_word_tariff", 2 * words(mass) + 2)
        shifted = mass << self.contract.action_bits
        self.meter.pay("controller", "integer_divide_word_tariff",
                       2 * (words(shifted) + 1) * (words(self.block_mass) + 1))
        numerator = shifted // self.block_mass
        denominator = 1 << self.contract.action_bits
        self.peak_prediction_working_bits = max(self.peak_prediction_working_bits, shifted.bit_length(), self.block_mass.bit_length())
        draw = self.bits.take(self.contract.action_bits)
        self.meter.pay_many((("forecast", "binary_action_comparison", 1),
                             ("output", "immutable_forecast_and_action_words", 12 + len(expert_actions)),
                             ("storage", "pending_issue_word_retention", 16 + len(expert_actions) + query.key_words)))
        self.pending = Issued(self.index, self.index // self.contract.block_size,
                              query, expert_actions, numerator, denominator,
                              int(draw < numerator))
        return self.pending

    def close(self, issue, receipt=None):
        if self.pending is None or type(issue) is not Issued or issue is not self.pending:
            raise Rejected("Close only the exact locally issued pending record.")
        self.meter.pay("admission", "close_round_identity_and_state_checks", 12)
        purchased = receipt is not None
        terminal = issue.prospective_action
        label = None
        if purchased:
            self.meter.pay_many((("check", "purchased_receipt_binding_checks", 24 + issue.query.key_words),
                                 ("storage", "selected_feedback_word_retention", 16 + self.contract.expert_count)))
            if self.feedback is not None:
                raise Rejected("The contract admits one purchase per block.")
            if (type(receipt) is not S.ServiceResult
                    or receipt.query_id != issue.query.query_id or receipt.claim_key != issue.query.claim_key
                    or receipt.checked is not True or type(receipt.answer) is not int
                    or receipt.answer not in (0, 1) or receipt.status != "success"
                    or receipt.provider != "cold_checked_modular_adapter"
                    or receipt.provider_version != S.VERSION + ";adapter=" + S.A.VERSION):
                raise Rejected("The purchased checked answer does not bind this issued request.")
            terminal = label = receipt.answer
            self.feedback = (issue.expert_actions, label)
            self.purchase_count += 1
        self.meter.pay_many((("output", "terminal_action_word_emission", 8),
                             ("storage", "pending_issue_release_and_state_write", 8)))
        closed = Closed(issue, purchased, terminal, label)
        self.index += 1
        self.pending = None
        if self.index % self.contract.block_size == 0:
            self._end_block()
        if self.index == self.contract.horizon:
            if self.purchase_count != self.contract.quota:
                raise Rejected("Successful completion requires the exact quota of checked labels.")
            self.completed = True
        return closed

    def _end_block(self):
        if self.feedback is None:
            raise Rejected("A complete block requires one checked selected label.")
        actions, label = self.feedback
        updated = []
        for weight, action in zip(self.weights, actions):
            self.meter.pay_many((("assessment", "selected_expert_loss_and_factor", 3),
                                 ("controller", "integer_small_multiply_word_tariff", 3 * words(weight) + 1)))
            value = weight * (self.contract.k - int(action != label))
            self.meter.pay("storage", "unnormalized_product_word_write", words(value))
            self.peak_prediction_working_bits = max(self.peak_prediction_working_bits, value.bit_length())
            updated.append(value)
        if self.contract.state_bits is not None:
            updated = self._round_to_fixed_mass(updated)
        for value in updated:
            if value.bit_length() > self.contract.individual_weight_bits:
                raise AssertionError("The proved integer-weight capacity was exceeded.")
            self.peak_weight_bits = max(self.peak_weight_bits, value.bit_length())
        self.meter.pay("storage", "selected_feedback_release", 1)
        self.weights = tuple(updated)
        self.feedback = None
        self.block_mass = None

    def _round_to_fixed_mass(self, products):
        n = self.contract.expert_count
        self.meter.pay("controller", "fixed_mass_and_slack_construction", 4)
        mass = n << self.contract.state_bits
        slack = mass - n
        total = 0
        for value in products:
            self.meter.pay("storage", "normalization_product_word_read", words(value))
            total = self._add(total, value)
        rounded, subtotal = [], 0
        for value in products:
            self.meter.pay("controller", "integer_multiply_word_tariff",
                           2 * words(slack) * words(value) + words(slack) + words(value))
            numerator = slack * value
            self.peak_prediction_working_bits = max(self.peak_prediction_working_bits, numerator.bit_length())
            self.meter.pay("controller", "integer_divide_word_tariff",
                           2 * (words(numerator) + 1) * (words(total) + 1))
            floor = numerator // total
            weight = self._add(1, floor)
            self.meter.pay("storage", "normalized_weight_word_write", words(weight))
            rounded.append(weight)
            subtotal = self._add(subtotal, weight)
        self.meter.pay("controller", "integer_subtract_word_tariff", 2 * max(words(mass), words(subtotal)) + 1)
        residual = mass - subtotal
        if not 0 <= residual < n:
            raise AssertionError("The floor-plus-one residual bound failed.")
        for index in range(n):
            self.meter.pay("controller", "fixed_order_residual_compare", 1)
            if index < residual:
                rounded[index] = self._add(rounded[index], 1)
                self.meter.pay("storage", "residual_weight_word_rewrite", words(rounded[index]))
        return rounded

    def record(self):
        return {"version": VERSION, "contract": self.contract.record(),
                "rounds_closed": self.index, "purchases": self.purchase_count,
                "completed": self.completed, "peak_weight_bits": self.peak_weight_bits,
                "peak_prediction_working_bits": self.peak_prediction_working_bits,
                "random_bits_consumed": self.bits.position,
                "randomness_provenance": self.bits.provenance,
                "final_weights": list(self.weights)}


def execute(tape, contract, *, seed, setup_resources=None, unit_limit=None):
    """Run one immutable DEVELOPMENT tape without an evaluator in the policy.

    `tape` carries mathematical inputs only. The purchase broker samples a
    position before each block, but does not pass its flag to `issue`. Receipt
    feedback changes weights only after the last action of that block closes.
    A declared-cap failure raises with its meter attached; it does not claim
    the successful-learning theorem or erase work already spent.
    """
    if type(tape) is not tuple or len(tape) != contract.horizon:
        raise Rejected("Supply the complete fixed tuple of public requests.")
    nat(seed, (1 << 64) - 1, "development seed")
    if setup_resources is not None and type(setup_resources) is not S.ResourceRecord:
        raise Rejected("Standalone setup must be a trusted immutable resource invoice.")
    if contract.expert_count != len(S.EXPERT_NAMES):
        raise Rejected("Contract N disagrees with the source-bound fixed library.")
    setup_total = 0 if setup_resources is None else setup_resources.total
    # Include a deterministic-development generator debit beyond the ideal
    # supplied-fair-bit controller bound. No waiting/physical time is priced.
    development_rng_cap = 1248 + (contract.random_bits + 63) // 64
    cap = (setup_total + contract.controller_cap(S.EXPERT_EVALUATION_CAP)
           + contract.quota * S.CHECKED_PURCHASE_CAP + development_rng_cap)
    meter = CostMeter(cap if unit_limit is None else unit_limit)
    try:
        meter.pay("admission", "whole_service_funding_check", 1)
    except BudgetExceeded as error:
        error.meter = meter.snapshot()
        raise
    if meter.limit_total < cap:
        error = BudgetExceeded("The complete declared controller and query quota are not funded.")
        error.meter = meter.snapshot()
        raise error
    if setup_resources is not None:
        meter.absorb(setup_resources, "standalone_setup")
    meter.reserve("checked_query_quota", contract.quota * S.CHECKED_PURCHASE_CAP)
    bits = BitTape.seeded(contract.random_bits, seed, meter)
    learner = FrozenProd(contract, meter, bits)
    transcript = []
    invoices = []
    try:
        for block_start in range(0, contract.horizon, contract.block_size):
            selected = bits.take(contract.selector_bits)
            for offset in range(contract.block_size):
                query = tape[block_start + offset]
                predictions = S.expert_predictions(query, meter)
                issued = learner.issue(query, predictions)
                receipt = None
                if offset == selected:
                    receipt = S.checked_purchase(query)
                    meter.absorb(receipt.resources, "checked_purchase",
                                 reservation="checked_query_quota", release=S.CHECKED_PURCHASE_CAP)
                    invoices.append(receipt)
                transcript.append(learner.close(issued, receipt))
    except Exception as error:
        error.meter = meter.snapshot()
        error.rounds_closed = learner.index
        error.purchases = learner.purchase_count
        raise
    if meter.reserved or bits.position != contract.random_bits:
        raise AssertionError("Finished service left a reservation or bit-count mismatch.")
    return {"learner": learner.record(), "meter": meter.snapshot(),
            "funded_cap": cap, "transcript": tuple(transcript),
            "invoices": tuple(invoices)}
