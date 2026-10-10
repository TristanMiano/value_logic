"""Matched ordinary controllers for the P3-08 CNF arm. DEVELOPMENT ONLY.

Contributor: ChatGPT (GPT-6 Astra Pro), delegated ordinary-control implementer.
Only full public queries, paid own receipts and previously retained answers
enter these policies. Private truth evaluation belongs to the external runner.
The ordinary probability/combination policies choose greedy marginal decisions,
so the recurrence's randomized-action bound is NOT claimed for them.
"""
from __future__ import annotations

from fractions import Fraction as F
import re

import p308_cnf as S
from p308_broker import Contract, NumericProd
from p308_common import C, RationalMeter, fraction_record


VERSION = "p308-ordinary-controllers-v1"
METHODS = ("proof_only", "probability_cost", "exact_dpll",
           "exact_cache", "ordinary_combo")


def _price(value, name):
    if type(value) not in (int, F, str):
        raise C.Rejected(name + " must be a finite exact rational.")
    if type(value) is str and re.fullmatch(
            r"[+-]?[0-9]{1,20}(?:/[1-9][0-9]{0,19})?", value) is None:
        raise C.Rejected(name + " needs a bounded integer or integer/positive-integer string.")
    if type(value) is int and abs(value).bit_length() > 64:
        raise C.Rejected(name + " integer exceeds its admitted width.")
    try:
        answer = F(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise C.Rejected(name + " is not a finite rational.") from exc
    if answer < 0 or max(abs(answer.numerator).bit_length(),
                         answer.denominator.bit_length()) > 64:
        raise C.Rejected(name + " must be nonnegative with 64-bit numerator/denominator.")
    return answer


def _greedy(q, fp, fn, rational):
    """Point decision from its explicitly fallible marginal; ties choose zero."""
    loss_zero = rational.mul(fn, q)
    loss_one = rational.mul(fp, rational.sub(1, q))
    if rational.compare(loss_one, loss_zero) < 0:
        return 1, loss_one
    return 0, loss_zero


def _prepay_row(query, meter):
    # Same output/retention word service as the generic broker, paid before the
    # terminal work to preserve the current fallback record on child failure.
    meter.pay_many((("output", "immutable_base_and_live_forecast",
                     24 + len(S.EXPERT_NAMES)),
                    ("storage", "retained_issue_words",
                     24 + len(S.EXPERT_NAMES) + query.key_words),
                    ("output", "terminal_and_knowledge_record", 24),
                    ("storage", "base_statistics_retention", 24)))


class _Policy:
    def __init__(self, tape, method, meter, *, seed, fp, fn, unit_price,
                 block_size, action_bits, state_bits, proof_cap,
                 provider_limit, fallback_action, cache_capacity,
                 prior_cost_multiplier):
        self.tape, self.method, self.meter = tape, method, meter
        self.fp, self.fn, self.unit_price = fp, fn, unit_price
        self.block_size = block_size
        self.action_bits = action_bits
        self.denominator = 1 << action_bits
        self.proof_cap, self.provider_limit = proof_cap, provider_limit
        self.fallback_action = fallback_action
        self.prior_cost_multiplier = prior_cost_multiplier
        self.rational = RationalMeter(meter)
        self.numeric = self.bits = self.contract = None
        self.learning = method in ("probability_cost", "ordinary_combo")
        self.cache = S.ExactCache(cache_capacity) if method in (
            "exact_cache", "ordinary_combo") else None
        self.trace, self.invoices, self.blocks = [], [], []
        self.pending = None
        self.purchases = self.cache_hits = self.provider_failures = 0
        self.successful_purchases = 0
        self.feedback_count = self.known_rounds = 0
        self.cost_history = {}
        self.failed_full_calls = 0
        self.status, self.failure_detail = "partial", None
        # Local initialization is separate from the common installed source bill.
        meter.pay_many((("setup", "ordinary_local_method_configuration", 32),
                        ("storage", "ordinary_local_controller_state", 32),
                        ("admission", "ordinary_exact_price_inputs", 24)))
        if self.learning:
            self.contract = Contract(len(tape), block_size, len(S.EXPERT_NAMES),
                                     action_bits, state_bits, "uniform", 0)
            self.numeric = NumericProd(self.contract, meter)
            selector_bit_count = self.contract.quota * self.contract.selector_bits
            self.bits = C.BitTape.seeded(selector_bit_count, seed, meter)
        self.seed = seed

    def _shape(self, query):
        self.meter.pay("profile", "ordinary_shape_class", 8 + len(query.clauses))
        # Public coarse groups permit honest, fallible reuse across formulas.
        return (query.variables, len(query.clauses) // max(1, query.variables),
                min(4, max((len(c) for c in query.clauses), default=0)))

    def _estimate(self, query):
        key = self._shape(query)
        self.meter.pay_many((("profile", "ordinary_past_cost_lookup", 8),
                            ("storage", "ordinary_cost_profile_record_read", 4)))
        if key in self.cost_history:
            total, count = self.cost_history[key]
            estimate = self.rational.div(total, count)
            return estimate, "own_prior_successful_full_mean", key
        proxy = S.cost_proxy(query, self.meter)
        estimate = self.rational.mul(self.prior_cost_multiplier, proxy)
        return estimate, "public_shape_proxy", key

    def _remember_cost(self, query, receipt):
        key = self._shape(query)
        self.meter.pay_many((("profile", "ordinary_observed_full_cost_update", 8),
                            ("storage", "ordinary_cost_profile_record_write", 4)))
        total, count = self.cost_history.get(key, (0, 0))
        total += receipt.resources.total
        count += 1
        if total.bit_length() > 64 or count.bit_length() > 64:
            raise C.Rejected("Ordinary cost history exceeded its public finite width.")
        self.cost_history[key] = (total, count)

    def _purchase(self, query, solver, requested, purpose):
        cap = S.service_cap(query, solver)
        requested = min(cap, requested)
        if self.provider_limit is not None:
            requested = min(requested, self.provider_limit)
        self.meter.pay("controller", "ordinary_provider_cap_and_choice", 12)
        reservation = "ordinary_provider"
        self.meter.reserve(reservation, requested)
        receipt = S.checked_purchase(query, limit_total=requested, solver=solver)
        # Child failure debits are absorbed before interpreting its status.
        self.meter.absorb(receipt.resources, "ordinary_provider",
                          reservation=reservation, release=requested)
        self.purchases += 1
        self.invoices.append({"index": len(self.trace), "purpose": purpose,
                              "requested_cap": requested, "solver": solver,
                              **receipt.record()})
        self.meter.pay("check", "owned_receipt_identity_status_version", 24 + query.key_words)
        if (type(receipt) is not S.Receipt or receipt.query_id != query.query_id
                or receipt.claim_key != query.claim_key
                or receipt.provider != S.PROVIDER or receipt.provider_version != S.VERSION):
            raise C.Rejected("Owned ordinary provider returned a misbound receipt.")
        if not receipt.successful:
            self.provider_failures += 1
            if purpose == "optional_full" or purpose == "selected_full":
                self.failed_full_calls += 1
            if receipt.answer is not None or receipt.checked is not False:
                raise C.Rejected("A failed ordinary call exposed a purported hard answer.")
            return None, receipt
        if receipt.checked is not True or type(receipt.answer) is not int or receipt.answer not in (0, 1):
            raise C.Rejected("Ordinary provider success is not an exact checked binary answer.")
        self.successful_purchases += 1
        return receipt.answer, receipt

    def _cache_lookup(self, query):
        if self.cache is None:
            return None
        hit = self.cache.lookup(query, self.meter)
        if hit is not None:
            self.cache_hits += 1
        return hit

    def _cache_remember(self, query, receipt):
        if self.cache is not None and receipt is not None and receipt.successful:
            self.cache.remember(query, receipt, self.meter)

    def _row(self, index, query, advice, numerator, selected, propensity):
        cache_hit = self._cache_lookup(query)
        known_before = None if cache_hit is None else cache_hit.answer
        emitted_numerator = numerator if known_before is None else known_before * self.denominator
        _prepay_row(query, self.meter)
        if self.learning:
            self.meter.pay("controller", "ordinary_probability_rational_decode", 32)
            base_q = F(numerator, self.denominator)
            base_action, estimated_error = _greedy(base_q, self.fp, self.fn, self.rational)
        else:
            # A supplied proof/exact fallback needs no fallible-model decision
            # calculation. Do not handicap exact methods with unused VOI work.
            base_action, estimated_error = self.fallback_action, None
        action = base_action
        if known_before is not None:
            action, estimated_error = known_before, F(0)
        record = {
            "index": index, "block": index // self.block_size,
            "query_id": query.query_id, "claim_key": query.claim_key,
            "scope": [query.semantics_version, query.source_version],
            "advice": list(advice), "base_q": [numerator, self.denominator],
            "emitted_q": [emitted_numerator, self.denominator],
            "base_action": base_action, "prospective_action": action,
            "base_terminal": base_action, "terminal_action": action,
            "selected": selected, "propensity": propensity,
            "purchased": False, "purchased_label": None,
            "cached": cache_hit is not None,
            "hard_before": "checked" if known_before is not None else "unresolved",
            "hard_after": {"status": "checked" if known_before is not None else "unresolved",
                           "answer": known_before,
                           "interval": [known_before, known_before] if known_before is not None else [0, 1]},
            "estimated_error_cost": None if estimated_error is None else fraction_record(estimated_error),
            "cost_estimate": None, "cost_estimate_source": None,
            "attempts": [], "forecast_immutable": True
        }
        self.pending = record
        answer, receipt = known_before, cache_hit
        if answer is None:
            if self.method == "proof_only":
                answer, receipt = self._purchase(query, "enumeration", self.proof_cap, "bounded_proof")
            elif self.method in ("exact_dpll", "exact_cache"):
                answer, receipt = self._purchase(query, "dpll", S.service_cap(query, "dpll"), "exact_full")
            elif selected:
                answer, receipt = self._purchase(query, "dpll", S.service_cap(query, "dpll"), "selected_full")
                if receipt.successful and self.method == "ordinary_combo":
                    self._remember_cost(query, receipt)
            elif self.method == "ordinary_combo":
                estimate, estimate_source, _ = self._estimate(query)
                record["cost_estimate"] = fraction_record(estimate)
                record["cost_estimate_source"] = estimate_source
                # Public maximum fee for a bounded DPLL prefix. That prefix
                # admits the provider's exact empty/opposing-unit shortcuts.
                self.meter.pay("controller", "ordinary_quick_probe_cap", 8)
                quick_cap = min(S.service_cap(query, "dpll"), 2048 + 24 * query.key_words)
                quick_fee = self.rational.mul(self.unit_price, quick_cap)
                if self.rational.compare(quick_fee, estimated_error) <= 0:
                    answer, receipt = self._purchase(query, "dpll", quick_cap, "optional_capped_probe")
                    record["attempts"].append({"kind": "capped_probe", "status": receipt.status})
                if answer is None:
                    prospective_fee = self.rational.mul(self.unit_price, estimate)
                    if self.rational.compare(prospective_fee, estimated_error) <= 0:
                        answer, receipt = self._purchase(
                            query, "dpll", S.service_cap(query, "dpll"), "optional_full")
                        record["attempts"].append({"kind": "full", "status": receipt.status})
                        if receipt.successful:
                            self._remember_cost(query, receipt)
        if receipt is not None and cache_hit is None:
            record["purchased"] = True
            record["purchased_label"] = answer
            record["provider_status"] = receipt.status
            if not record["attempts"]:
                record["attempts"].append({"kind": "selected" if selected else self.method,
                                           "status": receipt.status})
        if answer is not None:
            record["terminal_action"] = record["base_terminal"] = answer
            record["hard_after"] = {"status": "checked", "answer": answer,
                                    "interval": [answer, answer]}
            self.known_rounds += 1
            if cache_hit is None:
                self._cache_remember(query, receipt)
        else:
            record["provider_status"] = record.get("provider_status", "not_requested")
        self.trace.append(record)
        self.pending = None
        return answer

    def run(self):
        if self.learning:
            b = self.block_size
            for start in range(0, len(self.tape), b):
                block = self.tape[start:start + b]
                self.meter.pay("admission", "public_block_validation", 8 + b)
                for query in block:
                    self.meter.pay("storage", "public_block_input_retention", query.key_words)
                advice = tuple(S.expert_predictions(query, self.meter) for query in block)
                numerators = tuple(self.numeric.numerator(row) for row in advice)
                self.meter.pay("storage", "public_advice_and_forecast_buffer",
                               b * (len(S.EXPERT_NAMES) + 4))
                selected = self.bits.take(self.contract.selector_bits)
                self.meter.pay("output", "selection_record_words", 12 + 2 * b)
                block_record = {"block": start // b, "selected": selected,
                                "propensities": [[1, b] for _ in block],
                                "weights_before": list(self.numeric.weights)}
                self.blocks.append(block_record)
                updates = []
                for offset, query in enumerate(block):
                    answer = self._row(start + offset, query, advice[offset], numerators[offset],
                                       offset == selected, [1, b])
                    if answer is not None and (self.method == "ordinary_combo" or offset == selected):
                        updates.append((advice[offset], answer))
                # All forecasts in the block precede these label-driven updates.
                for prediction, answer in updates:
                    self.numeric.update(prediction, answer)
                    self.feedback_count += 1
                block_record["weights_after"] = list(self.numeric.weights)
                block_record["paid_or_retained_feedback_updates"] = len(updates)
        else:
            for index, query in enumerate(self.tape):
                self._row(index, query, (), self.denominator // 2, False, None)
        self.status = "success"

    def record(self):
        return {
            "stage": "DEVELOPMENT", "version": VERSION, "method": self.method,
            "status": self.status, "failure_detail": self.failure_detail,
            "rounds_closed": len(self.trace), "remaining_requests": len(self.tape) - len(self.trace),
            "rounds_issued": len(self.trace) + int(self.pending is not None),
            "pending": self.pending, "trace": self.trace,
            "issued_trace": self.trace + ([] if self.pending is None else [self.pending]),
            "blocks": self.blocks, "invoices": self.invoices,
            "purchases": self.purchases, "cache_hits": self.cache_hits,
            "purchase_count_meaning": "Physical provider attempts, including failures; exact cache uses are separate.",
            "successful_purchases": self.successful_purchases,
            "known_terminal_rounds": self.known_rounds,
            "provider_failures": self.provider_failures,
            "failed_full_calls_censored": self.failed_full_calls,
            "feedback_updates": self.feedback_count,
            "weights": None if self.numeric is None else list(self.numeric.weights),
            "cache_retained_words": 0 if self.cache is None else self.cache.retained_words,
            "randomness": None if self.bits is None else self.bits.provenance,
            "random_bits_consumed": 0 if self.bits is None else self.bits.position,
            "price_record": {"false_positive": fraction_record(self.fp),
                             "false_negative": fraction_record(self.fn),
                             "unit": fraction_record(self.unit_price)},
            "cost_history": [{"shape": list(key), "successful_full_total": total,
                              "successful_full_count": count}
                             for key, (total, count) in sorted(self.cost_history.items())],
            "expectation_theorem_eligible": False,
            "successful_quota_contract": False,
            "theorem_disposition": "Greedy marginal actions and optional/cached acquisition have no inherited randomized-action/one-cold-purchase guarantee.",
            "forecast_service": "Immutable forecast emitted before the current provider computation; current paid cache may supply an exact point.",
            "cost_estimate_meaning": "Public cold shape proxy or own prior successful full-call mean; fallible, with failures censored rather than treated as cheap completion.",
            "setup_scope": "Local controller initialization included. Installed shared source registry is billed separately and equally by the experiment runner."
        }


def run_method(tape, method, *, seed=3081001, error_price=1, unit_price=0,
               false_positive_price=None, false_negative_price=None,
               block_size=4, action_bits=16, state_bits=16,
               unit_limit=C.MAX_UNITS, provider_limit=None, proof_cap=2048,
               fallback_action=0, cache_capacity=64, prior_cost_multiplier=1):
    """One fully recorded DEVELOPMENT execution without any private truth API."""
    meter = C.CostMeter(unit_limit)
    policy = None
    try:
        meter.pay_many((("admission", "ordinary_episode_method_and_tape", 16),
                        ("output", "reserved_final_status_words", 64),
                        ("storage", "reserved_failure_state_words", 32)))
        if type(method) is not str or method not in METHODS:
            raise C.Rejected("Unknown ordinary method.")
        if type(tape) is not tuple or not 1 <= len(tape) <= 8192 or any(type(q) is not S.Query for q in tape):
            raise C.Rejected("Supply a bounded immutable public Query tape.")
        meter.pay("admission", "ordinary_whole_tape_shape_validation", 16 * len(tape))
        # Full content admission is charged by advice/provider/cache operations.
        # This whole-tape stage inspects only exact immutable types and shape.
        C.nat(block_size, 1024, "block size", minimum=1)
        C.nat(action_bits, 32, "action bits", minimum=1)
        C.nat(proof_cap, C.MAX_UNITS, "proof cap")
        if provider_limit is not None:
            C.nat(provider_limit, C.MAX_UNITS, "provider cap")
        if type(fallback_action) is not int or fallback_action not in (0, 1):
            raise C.Rejected("Fallback is a named binary action.")
        C.nat(cache_capacity, S.MAX_CACHE, "cache capacity")
        ep, up = _price(error_price, "error price"), _price(unit_price, "unit price")
        fp = ep if false_positive_price is None else _price(false_positive_price, "false-positive price")
        fn = ep if false_negative_price is None else _price(false_negative_price, "false-negative price")
        multiplier = _price(prior_cost_multiplier, "prior cost multiplier")
        policy = _Policy(tape, method, meter, seed=seed, fp=fp, fn=fn, unit_price=up,
                         block_size=block_size, action_bits=action_bits, state_bits=state_bits,
                         proof_cap=proof_cap, provider_limit=provider_limit,
                         fallback_action=fallback_action, cache_capacity=cache_capacity,
                         prior_cost_multiplier=multiplier)
        policy.run()
        result = policy.record()
    except (C.BudgetExceeded, C.Rejected, S.Rejected) as exc:
        if policy is not None:
            policy.status, policy.failure_detail = "failed", type(exc).__name__ + ": " + str(exc)
            result = policy.record()
        else:
            result = {"stage": "DEVELOPMENT", "version": VERSION, "method": method,
                      "status": "failed", "failure_detail": type(exc).__name__ + ": " + str(exc),
                      "rounds_closed": 0, "trace": [], "blocks": [], "invoices": [],
                      "purchases": 0, "expectation_theorem_eligible": False,
                      "successful_quota_contract": False}
    result["meter"] = meter.snapshot()
    result["local_setup_units"] = meter.by_category["setup"]
    result["common_source_setup_included"] = False
    return result
