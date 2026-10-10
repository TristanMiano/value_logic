"""Paid, propensity-corrected allocation within one fixed public query block.

ChatGPT (GPT-6 Astra Pro), 2026-10-09 UTC. DEVELOPMENT, R-P3-B-A.

This separately versioned extension grants B-request public lookahead. It
uses fixed-mass weights, one ticket per position plus B extra tickets for a
disagreement/cost-proxy favorite, and exactly one checked purchase per block.
The favored position depends on previous settled learning, not current labels.
The proxy is a selection heuristic; actual provider invoices are paid in full.

The inherited finite issue/close/normalization implementation is explicitly
source-bound. This class initializes its own allocation contract rather than
claiming that the uniform broker's bit and arithmetic bounds still apply.
"""
from __future__ import annotations

from dataclasses import dataclass
import importlib.util
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location(
    "_selective_allocation_core", HERE / "07_selective_feedback.py")
C = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = C
spec.loader.exec_module(C)
S = C.S
VERSION = "r-p3-b-a-propensity-allocation-v1"
PROXY_CHEAP = 128
PROXY_GENERAL = 304


@dataclass(frozen=True)
class Contract:
    horizon: int
    block_size: int
    expert_count: int = 4
    action_bits: int = 16
    state_bits: int = 16

    def __post_init__(self):
        C.Contract(self.horizon, self.block_size, self.expert_count,
                   self.action_bits, self.state_bits)
        if self.block_size < 2 or self.state_bits is None:
            raise C.Rejected("Allocation requires B>=2 and declared fixed state.")

    @property
    def quota(self):
        return self.horizon // self.block_size

    @property
    def h_bound(self):
        return 2 * self.block_size - 1

    @property
    def k(self):
        return self.h_bound

    @property
    def selector_bits(self):
        return C.ceil_log2(2 * self.block_size)

    @property
    def random_bits(self):
        return self.quota * self.selector_bits + self.horizon * self.action_bits

    @property
    def mass(self):
        return self.expert_count << self.state_bits

    @property
    def maximum_update_denominator(self):
        return (self.block_size + 1) * self.h_bound * self.k

    @property
    def individual_weight_bits(self):
        return self.state_bits + C.ceil_log2(self.expert_count) + 1

    @property
    def prediction_working_bits(self):
        # Normalization numerator <=M^2*D. Disagreement/quote comparison
        # numerator <=M^2*304. Forecast numerator <=M*2^h.
        extra = max(self.maximum_update_denominator.bit_length(), PROXY_GENERAL.bit_length())
        return max(2 * self.individual_weight_bits + extra + 2,
                   self.individual_weight_bits + self.action_bits + 2)

    @property
    def maximum_operand_bits(self):
        return max(95, self.prediction_working_bits)

    @property
    def working_words(self):
        return (self.prediction_working_bits + 63) // 64

    @property
    def buffer_word_cap(self):
        return self.block_size * (128 + self.expert_count + 4 * self.working_words)

    def controller_cap(self):
        n, z, h = self.expert_count, self.working_words, self.action_bits
        initial = 2048 + 4 * n * z + 2 * ((self.random_bits + 63) // 64)
        issue_close = 512 + S.EXPERT_EVALUATION_CAP + 16 * n * z + 8 * z * z + 8 * h
        allocation = 512 + 64 * n * z + 32 * z * z
        block = (1024 + 32 * n * z + 8 * self.selector_bits
                 + n * (16 * z * z + 32 * z + 32))
        return initial + self.horizon * (issue_close + allocation) + self.quota * block

    def record(self):
        return {
            "version": VERSION, "horizon": self.horizon,
            "block_size": self.block_size, "expert_count": self.expert_count,
            "action_bits": self.action_bits, "state_bits": self.state_bits,
            "quota": self.quota, "H": self.h_bound, "K": self.k,
            "tickets_per_block": 2 * self.block_size,
            "minimum_propensity": [1, 2 * self.block_size],
            "random_bits": self.random_bits,
            "individual_weight_bits": self.individual_weight_bits,
            "prediction_working_bits": self.prediction_working_bits,
            "sampler_working_bits": 95, "maximum_operand_bits": self.maximum_operand_bits,
            "buffer_word_cap": self.buffer_word_cap,
            "lookahead": "Current block's public requests only; no unpurchased answers.",
            "cost_proxy": {"elementary_identity": PROXY_CHEAP, "other": PROXY_GENERAL},
        }


class AllocatedProd(C.FrozenProd):
    """Share source-bound issue/close/rounding; replace contract and update."""
    def __init__(self, contract, meter, bits):
        if type(contract) is not Contract or type(meter) is not C.CostMeter or type(bits) is not C.BitTape:
            raise C.Rejected("Use the declared allocation contract and paid interfaces.")
        if bits.meter is not meter or bits.bit_count != contract.random_bits:
            raise C.Rejected("Allocation and its complete bit tape require one funded meter.")
        self.contract, self.meter, self.bits = contract, meter, bits
        meter.pay_many((("admission", "allocation_contract_validation", 24),
                        ("storage", "initial_weight_word_write", contract.expert_count),
                        ("storage", "allocation_scalar_state_write", 24)))
        initial = 1 << contract.state_bits
        self.weights = tuple(initial for _ in range(contract.expert_count))
        self.index = 0
        self.pending = self.feedback = self.block_mass = None
        self.propensity_tickets = None
        self.purchase_count = 0
        self.peak_weight_bits = initial.bit_length()
        self.peak_prediction_working_bits = initial.bit_length()
        self.completed = False
        self.peak_buffer_words = 0

    def prepare_block(self, queries):
        """Inspect public requests, charge their advice, and sample one ticket.

        Scores use no receipts. The full block is an explicit stronger input
        contract; the returned cached advice is immutable throughout it.
        """
        b, n = self.contract.block_size, self.contract.expert_count
        self.meter.pay("admission", "public_block_and_state_check", 12)
        if (self.completed or self.pending is not None or self.feedback is not None
                or self.index % b or type(queries) is not tuple or len(queries) != b):
            raise C.Rejected("Prepare exactly the next complete public block.")
        mass = self.contract.mass
        cached, scores, proxies = [], [], []
        favorite, best_score, best_proxy, retained = 0, -1, 1, 0
        for offset, query in enumerate(queries):
            predictions = S.expert_predictions(query, self.meter)
            self.meter.pay_many((("storage", "lookahead_query_word_retention", query.key_words),
                                 ("storage", "lookahead_advice_word_retention", n),
                                 ("controller", "public_cost_proxy_branches", 3)))
            proxy = PROXY_CHEAP if query.a in (1, query.m - 1) else PROXY_GENERAL
            positive = 0
            for weight, action in zip(self.weights, predictions):
                self.meter.pay_many((("storage", "allocation_weight_word_read", C.words(weight)),
                                     ("controller", "allocation_advice_branch", 1)))
                if action:
                    positive = self._add(positive, weight)
            self.meter.pay("controller", "allocation_mass_subtract_word_tariff",
                           2 * C.words(mass) + 1)
            negative = mass - positive
            self.meter.pay("controller", "allocation_disagreement_multiply_word_tariff",
                           2 * C.words(positive) * C.words(negative)
                           + C.words(positive) + C.words(negative))
            score = positive * negative
            self.meter.pay("controller", "allocation_score_comparison_word_tariff",
                           8 * C.words(score) + 8)
            left, right = score * best_proxy, best_score * proxy
            self.peak_prediction_working_bits = max(
                self.peak_prediction_working_bits, score.bit_length(),
                abs(left).bit_length(), abs(right).bit_length())
            if left > right:
                favorite, best_score, best_proxy = offset, score, proxy
            self.meter.pay_many((("storage", "allocation_score_and_proxy_word_retention", C.words(score) + 1),
                                 ("storage", "allocation_index_state_write", 4)))
            cached.append((query, predictions))
            scores.append(score)
            proxies.append(proxy)
            retained += query.key_words + n + C.words(score) + 5
        if retained > self.contract.buffer_word_cap:
            raise AssertionError("The charged public lookahead buffer exceeds its capacity.")
        self.peak_buffer_words = max(self.peak_buffer_words, retained)
        draw = self.bits.take(self.contract.selector_bits)
        self.meter.pay_many((("controller", "ticket_map_and_propensity_construction", 5),
                             ("output", "public_allocation_record_words", 16 + 3 * b + n)))
        selected = draw if draw < b else favorite
        tickets = b + 1 if selected == favorite else 1
        record = {"block": self.index // b, "favorite": favorite,
                  "selected": selected, "selected_tickets": tickets,
                  "ticket_total": 2 * b, "scores": scores, "cost_proxies": proxies,
                  "frozen_weights": list(self.weights), "buffer_words": retained}
        return tuple(cached), selected, tickets, record

    def close(self, issue, receipt=None, *, tickets=None):
        if receipt is not None:
            self.meter.pay("admission", "selected_propensity_ticket_check", 2)
            if type(tickets) is not int or tickets not in (1, self.contract.block_size + 1):
                raise C.Rejected("The selected receipt needs its actual ticket multiplicity.")
            self.propensity_tickets = tickets
        elif tickets is not None:
            raise C.Rejected("No purchase propensity is admitted without a receipt.")
        return super().close(issue, receipt)

    def _end_block(self):
        if self.feedback is None or self.propensity_tickets is None:
            raise C.Rejected("The complete block needs a checked label and its propensity.")
        self.meter.pay("controller", "propensity_update_integer_factor_construction", 8)
        if self.propensity_tickets == 1:
            numerator, denominator = 1, self.contract.h_bound
        else:
            numerator = self.contract.block_size - 1
            denominator = self.contract.maximum_update_denominator
        actions, label = self.feedback
        products = []
        for weight, action in zip(self.weights, actions):
            self.meter.pay_many((("assessment", "propensity_loss_and_integer_factor", 4),
                                 ("controller", "integer_small_multiply_word_tariff", 3 * C.words(weight) + 1)))
            value = weight * (denominator - numerator * int(action != label))
            self.meter.pay("storage", "unnormalized_product_word_write", C.words(value))
            self.peak_prediction_working_bits = max(self.peak_prediction_working_bits, value.bit_length())
            products.append(value)
        updated = self._round_to_fixed_mass(products)
        for value in updated:
            if value.bit_length() > self.contract.individual_weight_bits:
                raise AssertionError("The fixed-mass weight capacity was exceeded.")
            self.peak_weight_bits = max(self.peak_weight_bits, value.bit_length())
        self.meter.pay("storage", "selected_feedback_and_propensity_release", 2)
        self.weights = tuple(updated)
        self.feedback = self.block_mass = self.propensity_tickets = None

    def record(self):
        result = super().record()
        result.update(version=VERSION, dependency_version=C.VERSION,
                      contract=self.contract.record(), peak_buffer_words=self.peak_buffer_words)
        return result


def execute(tape, contract, *, seed, setup_resources=None, unit_limit=None):
    """Execute the stronger public-lookahead contract with prepaid purchases."""
    if type(contract) is not Contract or type(tape) is not tuple or len(tape) != contract.horizon:
        raise C.Rejected("Supply the allocation contract and its fixed public tape.")
    C.nat(seed, (1 << 64) - 1, "development seed")
    if setup_resources is not None and type(setup_resources) is not S.ResourceRecord:
        raise C.Rejected("Setup requires the source-bound immutable invoice.")
    if contract.expert_count != len(S.EXPERT_NAMES):
        raise C.Rejected("The finite public library has exactly four experts.")
    setup_total = 0 if setup_resources is None else setup_resources.total
    rng_cap = 1248 + (contract.random_bits + 63) // 64
    cap = (setup_total + contract.controller_cap()
           + contract.quota * S.CHECKED_PURCHASE_CAP + rng_cap)
    meter = C.CostMeter(cap if unit_limit is None else unit_limit)
    learner = None
    try:
        meter.pay("admission", "whole_service_funding_check", 1)
        if meter.limit_total < cap:
            raise C.BudgetExceeded("The declared allocation, controller and purchase quota are not funded.")
        if setup_resources is not None:
            meter.absorb(setup_resources, "standalone_setup")
        meter.reserve("checked_query_quota", contract.quota * S.CHECKED_PURCHASE_CAP)
        bits = C.BitTape.seeded(contract.random_bits, seed, meter)
        learner = AllocatedProd(contract, meter, bits)
        transcript, invoices, allocations = [], [], []
        for start in range(0, contract.horizon, contract.block_size):
            cached, selected, tickets, allocation = learner.prepare_block(
                tape[start:start + contract.block_size])
            allocations.append(allocation)
            for offset, (query, predictions) in enumerate(cached):
                issue = learner.issue(query, predictions)
                receipt = None
                if offset == selected:
                    receipt = S.checked_purchase(query)
                    meter.absorb(receipt.resources, "checked_purchase",
                                 reservation="checked_query_quota", release=S.CHECKED_PURCHASE_CAP)
                    invoices.append(receipt)
                transcript.append(learner.close(issue, receipt,
                                               tickets=tickets if receipt is not None else None))
            meter.pay("storage", "public_block_buffer_release", allocation["buffer_words"])
        if meter.reserved or bits.position != contract.random_bits:
            raise AssertionError("A completed allocation left a reservation or bit mismatch.")
    except Exception as error:
        error.meter = meter.snapshot()
        error.rounds_closed = 0 if learner is None else learner.index
        error.purchases = 0 if learner is None else learner.purchase_count
        raise
    return {"learner": learner.record(), "meter": meter.snapshot(), "funded_cap": cap,
            "transcript": tuple(transcript), "invoices": tuple(invoices),
            "allocations": tuple(allocations)}
