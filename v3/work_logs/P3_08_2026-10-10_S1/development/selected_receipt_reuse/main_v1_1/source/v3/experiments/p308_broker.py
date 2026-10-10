"""Versioned finite program/forecast broker. DEVELOPMENT, P3-08.

Research-by: ChatGPT (GPT-6 Astra Pro), 2026-10-10.
The generic query/receipt layer is NEW. Fixed-mass rounding and paid integer
addition are inherited unchanged from C.FrozenProd. Actual selectors are owned
here. Live hard corrections transfer base upper bounds, not base lower bounds
or a freshly recomputed within-block concentration identity.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from fractions import Fraction
import math

from p308_common import C, RationalMeter, fraction_record, resources
from p308_hashcache import paid_key_bucket

VERSION = "p308-program-broker-v1.2"
HARD_BUCKET_COUNT = 128


def _paid_scope(scope, meter):
    """Validate a bounded scope, paying before shape and content reads."""
    meter.pay("admission", "scope_shape_preflight", 4)
    if type(scope) not in (tuple, list) or len(scope) != 3:
        raise C.Rejected("A scope has exactly three version/epoch labels.")
    meter.pay("admission", "scope_scalar_type_length_check", 6)
    if any(type(value) is not str or not 1 <= len(value) <= 128 for value in scope):
        raise C.Rejected("Scope labels must be capped nonempty ASCII strings.")
    meter.pay("admission", "scope_label_validation_words",
              6 + sum((len(value) + 7) // 8 for value in scope))
    if any(not value.isascii() for value in scope):
        raise C.Rejected("Scope labels must be capped nonempty ASCII strings.")
    return tuple(scope)


@dataclass(frozen=True)
class Contract:
    horizon: int
    block_size: int = 4
    expert_count: int = 6
    action_bits: int = 16
    state_bits: int = 16
    selector: str = "uniform"
    hard_capacity: int = 128
    hard_index: str = "linear"

    def __post_init__(self):
        C.nat(self.state_bits, 32, "fixed-state precision bits", minimum=1)
        C.Contract(self.horizon, self.block_size, self.expert_count,
                   self.action_bits, self.state_bits)
        if self.block_size < 2 or self.selector not in ("uniform", "tickets"):
            raise C.Rejected("Use B>=2 and the uniform or positive-ticket selector.")
        C.nat(self.hard_capacity, 8192, "hard-answer capacity")
        if type(self.hard_index) is not str or self.hard_index not in ("linear", "hashed"):
            raise C.Rejected("Hard-answer index must be linear or hashed.")

    @property
    def quota(self):
        return self.horizon // self.block_size

    @property
    def k(self):
        return max(2, self.block_size - 1) if self.selector == "uniform" else 2 * self.block_size - 1

    @property
    def selector_bits(self):
        return C.ceil_log2(self.block_size) + int(self.selector == "tickets")

    @property
    def random_bits(self):
        return self.quota * self.selector_bits + self.horizon * self.action_bits

    @property
    def individual_weight_bits(self):
        return self.state_bits + C.ceil_log2(self.expert_count) + 1

    @property
    def maximum_operand_bits(self):
        d = (self.block_size + 1) * self.k**2 if self.selector == "tickets" else self.k
        return max(95, 2 * self.individual_weight_bits + d.bit_length() + 2,
                   self.individual_weight_bits + self.action_bits + 2)

    def record(self):
        return dict(version=VERSION, horizon=self.horizon, block_size=self.block_size,
                    expert_count=self.expert_count, action_bits=self.action_bits,
                    state_bits=self.state_bits, selector=self.selector,
                    hard_capacity=self.hard_capacity, hard_index=self.hard_index,
                    quota=self.quota,
                    random_bits=self.random_bits, maximum_operand_bits=self.maximum_operand_bits)


class NumericProd:
    """Ported numerical kernel: binary stateless advice and selected labels only."""
    _add = C.FrozenProd._add
    _round_to_fixed_mass = C.FrozenProd._round_to_fixed_mass

    def __init__(self, contract, meter):
        self.contract, self.meter = contract, meter
        self.weights = tuple(1 << contract.state_bits for _ in range(contract.expert_count))
        self.peak_prediction_working_bits = contract.state_bits + 1
        self.peak_weight_bits = contract.state_bits + 1
        self.updates = 0
        meter.pay_many((("admission", "generic_numeric_contract", 16),
                        ("storage", "initial_weight_words", contract.expert_count)))

    def numerator(self, advice):
        n = self.contract.expert_count
        self.meter.pay("admission", "binary_advice_validation", n + 2)
        if type(advice) is not tuple or len(advice) != n or any(type(a) is not int or a not in (0, 1) for a in advice):
            raise C.Rejected("Expected the declared fixed binary expert library.")
        mass = positive = 0
        for weight, action in zip(self.weights, advice):
            self.meter.pay_many((("storage", "forecast_weight_read", C.words(weight)),
                                 ("forecast", "expert_action_branch", 1)))
            mass = self._add(mass, weight)
            if action:
                positive = self._add(positive, weight)
        self.meter.pay("controller", "forecast_shift_word_tariff", 2 * C.words(positive) + 2)
        shifted = positive << self.contract.action_bits
        self.meter.pay("controller", "forecast_divide_word_tariff",
                       2 * (C.words(shifted) + 1) * (C.words(mass) + 1))
        self.peak_prediction_working_bits = max(self.peak_prediction_working_bits,
                                               shifted.bit_length(), mass.bit_length())
        return shifted // mass

    def update(self, advice, label, multiplicity=1):
        if type(label) is not int or label not in (0, 1):
            raise C.Rejected("No update without one checked binary answer.")
        b, k = self.contract.block_size, self.contract.k
        if self.contract.selector == "uniform":
            denominator, loss_scale = k, 1
            if multiplicity != 1:
                raise C.Rejected("Uniform receipt has a nonuniform propensity.")
        else:
            if multiplicity not in (1, b + 1):
                raise C.Rejected("Selected ticket multiplicity is outside the contract.")
            # 1 - [(1/pi)-1] * loss / (H*K), with H=K=2B-1.
            denominator, loss_scale = multiplicity * k * k, 2 * b - multiplicity
        products = []
        for weight, action in zip(self.weights, advice):
            self.meter.pay_many((("assessment", "selected_loss_and_factor", 5),
                                 ("controller", "selected_product_word_tariff",
                                  2 * C.words(weight) * C.words(denominator) + C.words(weight) + C.words(denominator))))
            value = weight * (denominator - loss_scale * int(action != label))
            self.meter.pay("storage", "selected_product_word", C.words(value))
            self.peak_prediction_working_bits = max(self.peak_prediction_working_bits, value.bit_length())
            products.append(value)
        self.weights = tuple(self._round_to_fixed_mass(products))
        self.peak_weight_bits = max(self.peak_weight_bits, *(w.bit_length() for w in self.weights))
        if self.peak_weight_bits > self.contract.individual_weight_bits or self.peak_prediction_working_bits > self.contract.maximum_operand_bits:
            raise AssertionError("Generic numerical port exceeded its proved finite width.")
        self.updates += 1


@dataclass(frozen=True)
class HardEntry:
    scope: tuple
    generation: int
    key: tuple
    key_words: int
    answer: int
    receipt_request_id: str
    provider_version: str


class HardState:
    """A bounded finite conjunction of versioned hard Boolean coordinates.

    Unknown coordinates retain [0,1]; admitted answers supply a singleton.
    No unreceived cross-query Boolean relation or truth probability is implied.
    The default linear search retains the earlier behavior. Optional paid
    key hashing narrows candidates to a fixed bucket; every candidate still
    receives a complete key, scope and generation check. Old scoped entries
    remain historically stored. No bucket match authorizes an answer.
    """
    def __init__(self, meter, capacity, scope, *, index_kind="linear"):
        self.meter, self.capacity, self.scope = meter, capacity, tuple(scope)
        self.index_kind = index_kind
        self.entries = []
        self.conflicts = set()
        self.withdrawals = 0
        self.generation = 0
        meter.pay_many((("admission", "hard_store_initialization", 8),
                        ("storage", "hard_store_state_words", 8)))
        if type(index_kind) is not str or index_kind not in ("linear", "hashed"):
            raise C.Rejected("Hard-answer index must be linear or hashed.")
        self._buckets = None
        if index_kind == "hashed":
            meter.pay_many((("admission", "hard_hash_fixed_bucket_configuration", 4),
                            ("storage", "hard_hash_bucket_head_words", HARD_BUCKET_COUNT),
                            ("storage", "hard_hash_bucket_count_word", 1)))
            # Each head names a newest-first chain of immutable (entry slot,
            # previous head) nodes. A prepend writes two words and one head;
            # it never copies or resizes a growing bucket list.
            self._buckets = [None] * HARD_BUCKET_COUNT

    def _bucket_candidates(self, bucket):
        self.meter.pay("storage", "hard_hash_bucket_head_read", 1)
        node = self._buckets[bucket]
        while node is not None:
            self.meter.pay_many((("cache", "hard_hash_bucket_chain_step", 2),
                                ("storage", "hard_hash_node_and_entry_slot_read", 3)))
            slot, node = node
            yield slot, self.entries[slot]

    def _locate(self, query):
        """Return a state plus the owned slot/bucket, without exposing either."""
        self.meter.pay("admission", "hard_scope_read", 4)
        key = query.claim_key
        bucket = None
        if self.index_kind == "hashed":
            # Epoch/generation are deliberately outside the digest so a
            # stale same-key warrant remains visible in this bucket.
            bucket = paid_key_bucket(query, self.meter, HARD_BUCKET_COUNT)
            candidates = self._bucket_candidates(bucket)
        else:
            candidates = ((slot, self.entries[slot])
                          for slot in range(len(self.entries) - 1, -1, -1))
        stale = False
        for slot, entry in candidates:
            self.meter.pay("cache", "hard_scope_comparison", 4)
            self.meter.pay("cache", "complete_semantic_key_comparison", query.key_words + entry.key_words)
            if entry.key == key:
                if entry.scope != self.scope or entry.generation != self.generation:
                    stale = True
                    continue
                if self.index_kind == "hashed":
                    self.meter.pay("cache", "hard_hash_conflict_slot_read", 1)
                    conflict = slot in self.conflicts
                else:
                    conflict = (self.generation, self.scope, key) in self.conflicts
                if conflict:
                    return {"status": "conflict", "answer": None, "interval": None}, bucket, slot
                self.meter.pay("storage", "hard_answer_read", 4)
                return ({"status": "checked", "answer": entry.answer,
                         "interval": [entry.answer, entry.answer]}, bucket, slot)
            if self.index_kind == "hashed":
                self.meter.pay("cache", "hard_hash_bucket_collision_step", 1)
        return ({"status": "stale" if stale else "unresolved",
                 "answer": None, "interval": [0, 1]}, bucket, None)

    def lookup(self, query):
        return self._locate(query)[0]

    def admit(self, query, receipt):
        """Broker calls this only after binding and accepting its own receipt."""
        current, bucket, slot = self._locate(query)
        if current["status"] == "conflict":
            raise C.Rejected("Conflicted hard coordinate has no active warrant.")
        if current["answer"] is not None:
            self.meter.pay("check", "duplicate_hard_answer_comparison", 1)
            if current["answer"] != receipt.answer:
                self.meter.pay("storage", "hard_conflict_state_write", 8 + query.key_words)
                # Hashed entries use a bounded integer slot as their conflict
                # token, avoiding another unpriced semantic-key hash. Slots
                # are never reused, including after generation withdrawal.
                token = slot if self.index_kind == "hashed" else (self.generation, self.scope, query.claim_key)
                self.conflicts.add(token)
                raise C.Rejected("Contradictory checked receipts invalidate the coordinate.")
            return
        if len(self.entries) >= self.capacity:
            raise C.BudgetExceeded("Hard-answer capacity exhausted; new receipt is not admitted.")
        commit = [("storage", "hard_answer_and_full_key_write", 16 + query.key_words)]
        if self.index_kind == "hashed":
            commit += [("storage", "hard_hash_node_and_bucket_head_write", 3),
                       ("storage", "hard_hash_entry_slot_retention", 1),
                       ("controller", "hard_hash_chain_prepend", 2)]
        # Charge the full key retention and every index mutation atomically.
        # A denial cannot append an entry without its searchable bucket node.
        self.meter.pay_many(tuple(commit))
        slot = len(self.entries)
        self.entries.append(HardEntry(self.scope, self.generation, query.claim_key, query.key_words,
                                      receipt.answer, receipt.query_id, receipt.provider_version))
        if self.index_kind == "hashed":
            self._buckets[bucket] = (slot, self._buckets[bucket])

    def invalidate(self, new_scope):
        new_scope = _paid_scope(new_scope, self.meter)
        self.meter.pay_many((("check", "scope_epoch_change", 8),
                            ("storage", "scope_epoch_state_write", 8)))
        self.scope = new_scope
        self.withdrawals += 1
        self.generation += 1

    def record(self):
        return {"scope": list(self.scope), "entries_retained": len(self.entries),
                "index_kind": self.index_kind,
                "bucket_count": HARD_BUCKET_COUNT if self.index_kind == "hashed" else 0,
                "active_entries": sum(e.scope == self.scope and e.generation == self.generation for e in self.entries),
                "conflicts": len(self.conflicts), "withdrawals": self.withdrawals,
                "generation": self.generation}


@dataclass(frozen=True)
class Issued:
    index: int
    block: int
    query: object
    advice: tuple[int, ...]
    base_numerator: int
    output_numerator: int
    denominator: int
    base_action: int
    prospective_action: int
    hard_status: str


class Broker:
    """Trusted local owner of one epoch, with no external receipt admission API."""
    def __init__(self, service, contract, meter, bits, scope, *, hard=True,
                 purchase_solver="enumeration", provider_limit=None):
        if type(contract) is not Contract or type(meter) is not C.CostMeter or type(bits) is not C.BitTape:
            raise C.Rejected("Use the declared broker contract, meter and paid bits.")
        if bits.meter is not meter or bits.bit_count != contract.random_bits:
            raise C.Rejected("Broker and bit tape must share the complete funded contract.")
        if contract.expert_count != len(service.EXPERT_NAMES):
            raise C.Rejected("The actual fixed advice library disagrees with N.")
        self.service, self.contract, self.meter, self.bits = service, contract, meter, bits
        self.scope, self.hard_enabled = _paid_scope(scope, meter), bool(hard)
        # This terminal status slot is paid even for a direct Broker caller.
        # It permits one fail-closed epoch withdrawal after budget exhaustion.
        meter.pay_many((("storage", "broker_prepaid_failure_state_words", 8),
                        ("output", "broker_prepaid_failure_status_words", 8),
                        ("output", "hard_index_configuration_words", 8)))
        self.purchase_solver, self.provider_limit = purchase_solver, provider_limit
        self.numeric = NumericProd(contract, meter)
        self.hard = HardState(meter, contract.hard_capacity, self.scope,
                              index_kind=contract.hard_index)
        self.pending = None
        self.received = None
        self.selected = None
        self.multiplicity = None
        self.advice_block = None
        self.numerators = None
        self.index = self.purchases = 0
        self.trace, self.invoices, self.blocks = [], [], []
        self.failed = False
        self.failure_detail = None

    def begin_block(self, queries):
        b = self.contract.block_size
        if (self.failed or self.pending is not None or self.received is not None
                or self.advice_block is not None or self.index % b
                or self.index >= self.contract.horizon):
            raise C.Rejected("A block can start only at the next clean boundary.")
        if type(queries) is not tuple or len(queries) != b:
            raise C.Rejected("A complete public block is required.")
        self.meter.pay("admission", "public_block_validation", 8 + b)
        for query in queries:
            if type(query) is not self.service.Query or (query.semantics_version, query.source_version) != self.scope[:2]:
                raise C.Rejected("Public query or source version does not match this epoch.")
            self.meter.pay("storage", "public_block_input_retention", query.key_words)
        self.advice_block = tuple(self.service.expert_predictions(q, self.meter) for q in queries)
        self.numerators = tuple(self.numeric.numerator(a) for a in self.advice_block)
        self.meter.pay("storage", "public_advice_and_forecast_buffer", b * (self.contract.expert_count + 4))
        favorite = 0
        if self.contract.selector == "tickets":
            den = 1 << self.contract.action_bits
            best_num, best_proxy = -1, 1
            for offset, (query, num) in enumerate(zip(queries, self.numerators)):
                proxy = self.service.cost_proxy(query, self.meter)
                if type(proxy) is not int or proxy <= 0 or proxy.bit_length() > 32:
                    raise C.Rejected("Require a positive public 32-bit cost proxy.")
                self.meter.pay("controller", "disagreement_proxy_cross_products", 24)
                score = num * (den - num)
                if score * best_proxy > best_num * proxy:
                    favorite, best_num, best_proxy = offset, score, proxy
        ticket = self.bits.take(self.contract.selector_bits)
        if self.contract.selector == "uniform":
            self.selected, self.multiplicity = ticket, 1
            propensities = [[1, b] for _ in queries]
        else:
            self.selected = ticket if ticket < b else favorite
            self.multiplicity = b + 1 if self.selected == favorite else 1
            propensities = [[b + 1 if t == favorite else 1, 2 * b] for t in range(b)]
        self.block_queries = queries
        self.blocks.append({"block": self.index // b, "selected": self.selected,
                            "ticket": ticket, "favorite": favorite,
                            "multiplicity": self.multiplicity,
                            "propensities": propensities, "weights_before": list(self.numeric.weights)})
        self.meter.pay("output", "selection_record_words", 12 + 2 * b)

    def issue(self):
        if (self.failed or self.pending is not None or self.advice_block is None
                or self.index >= self.contract.horizon):
            raise C.Rejected("Issue only the next owned request in an open block.")
        offset = self.index % self.contract.block_size
        query = self.block_queries[offset]
        current = self.hard.lookup(query) if self.hard_enabled else {"status": "unresolved", "answer": None}
        if current["status"] == "conflict":
            raise C.Rejected("No action warrant from a conflicted coordinate.")
        numerator, denominator = self.numerators[offset], 1 << self.contract.action_bits
        out = numerator if current["answer"] is None else denominator * current["answer"]
        draw = self.bits.take(self.contract.action_bits)
        self.meter.pay_many((("forecast", "base_and_live_action_comparison", 2),
                            ("output", "immutable_base_and_live_forecast", 24 + self.contract.expert_count),
                            ("storage", "retained_issue_words", 24 + self.contract.expert_count + query.key_words)))
        self.pending = Issued(self.index, self.index // self.contract.block_size, query,
                              self.advice_block[offset], numerator, out, denominator,
                              int(draw < numerator), int(draw < out), current["status"])
        return self.pending

    def _bind_receipt(self, issued, receipt):
        """Validation alone is not external authentication; provider is owned."""
        self.meter.pay("check", "owned_receipt_identity_status_version", 24 + issued.query.key_words)
        if (type(receipt) is not self.service.Receipt or receipt.query_id != issued.query.query_id
                or receipt.claim_key != issued.query.claim_key or receipt.status != "success"
                or receipt.checked is not True or type(receipt.answer) is not int
                or receipt.answer not in (0, 1)
                or receipt.provider_version != self.service.VERSION
                or receipt.provider != self.service.PROVIDER):
            raise C.Rejected("The owned provider did not return a current checked receipt.")

    def close(self, issued):
        if self.failed or self.pending is None or issued is not self.pending:
            raise C.Rejected("Close only the exact locally issued record.")
        self.meter.pay("check", "pending_issue_identity", 8)
        offset = self.index % self.contract.block_size
        selected = offset == self.selected
        receipt = None
        base_terminal, terminal = issued.base_action, issued.prospective_action
        if selected:
            if self.received is not None:
                raise C.Rejected("Duplicate purchase in a block.")
            cap = self.service.service_cap(issued.query, self.purchase_solver)
            requested = cap if self.provider_limit is None else min(cap, self.provider_limit)
            self.meter.reserve("selected_provider", requested)
            receipt = self.service.checked_purchase(issued.query, limit_total=requested,
                                                     solver=self.purchase_solver)
            self.meter.absorb(receipt.resources, "selected_provider", reservation="selected_provider", release=requested)
            self.invoices.append(receipt.record())
            self._bind_receipt(issued, receipt)
            self.received = receipt
            self.purchases += 1
            base_terminal = terminal = receipt.answer
            if self.hard_enabled:
                self.hard.admit(issued.query, receipt)
        self.meter.pay_many((("output", "terminal_and_knowledge_record", 24),
                            ("storage", "base_statistics_retention", 24)))
        current = self.hard.lookup(issued.query) if self.hard_enabled else {"status": "unresolved", "answer": None, "interval": [0, 1]}
        row = {"index": issued.index, "block": issued.block,
               "query_id": issued.query.query_id, "claim_key": issued.query.claim_key,
               "advice": list(issued.advice), "base_q": [issued.base_numerator, issued.denominator],
               "emitted_q": [issued.output_numerator, issued.denominator],
               "base_action": issued.base_action, "prospective_action": issued.prospective_action,
               "base_terminal": base_terminal, "terminal_action": terminal,
               "selected": selected, "propensity": self.blocks[-1]["propensities"][offset],
               "purchased_label": None if receipt is None else receipt.answer,
               "hard_before": issued.hard_status, "hard_after": current,
               "scope": list(self.scope)}
        self.trace.append(row)
        self.pending = None
        self.index += 1
        if self.index % self.contract.block_size == 0:
            if self.received is None:
                raise C.Rejected("Missing selected receipt at block close.")
            self.numeric.update(self.advice_block[self.selected], self.received.answer,
                                self.multiplicity)
            self.blocks[-1]["weights_after"] = list(self.numeric.weights)
            self.received = self.advice_block = self.numerators = None
        # A detached audit copy prevents a caller's historical record from
        # mutating retained statistics. Deployed output words were paid above.
        return deepcopy(row)

    def withdraw(self, new_scope):
        """End this statistical epoch; an incomplete block has no success theorem."""
        if self.failed:
            raise C.Rejected("This statistical epoch has already ended.")
        # The failure-status slot was prepaid at construction. Stop first:
        # even a rejected or unfunded invalidation cannot retain an active
        # successful-episode warrant or permit another issue/close operation.
        self.failed = True
        self.failure_detail = "scope_withdrawal_requires_a_new_epoch"
        try:
            self.hard.invalidate(new_scope)
        except (C.BudgetExceeded, C.Rejected) as error:
            self.failure_detail = "scope_withdrawal_stopped: " + type(error).__name__ + ": " + str(error)
            raise

    def record(self):
        """Detached audit export; the deployed word records were already paid."""
        complete = (not self.failed and self.index == self.contract.horizon
                    and self.purchases == self.contract.quota
                    and self.numeric.updates == self.contract.quota
                    and self.pending is None and self.received is None
                    and self.advice_block is None
                    and self.bits.position == self.contract.random_bits)
        return deepcopy({"stage": "DEVELOPMENT", "version": VERSION, "contract": self.contract.record(),
                "status": "success" if complete else "failed" if self.failed else "partial",
                "successful_quota_contract": complete,
                "rounds_closed": self.index, "purchases": self.purchases,
                "remaining_requests": self.contract.horizon - self.index,
                "failure_detail": self.failure_detail, "scope": list(self.scope),
                "hard_enabled": self.hard_enabled, "index_kind": self.hard.index_kind,
                "hard_state": self.hard.record(), "weights": list(self.numeric.weights),
                "peak_weight_bits": self.numeric.peak_weight_bits,
                "peak_numeric_bits": self.numeric.peak_prediction_working_bits,
                "random_bits_consumed": self.bits.position,
                "randomness": self.bits.provenance,
                "pending_query_id": None if self.pending is None else self.pending.query.query_id,
                "trace": self.trace, "blocks": self.blocks, "invoices": self.invoices})


def funded_cap(service, tape, contract, *, hard=True, solver="enumeration"):
    """Conservative finite all-path envelope for this fixed public tape.

    It reserves a maximum cold answer in every block, regardless of sampled
    position. The remaining envelope covers paid advice, complete semantic-key
    comparisons, fixed-state arithmetic, bit generation and all trace words.
    Source procurement and optional separate reporting are billed separately.
    No inaccessible true answer or hindsight invoice enters this calculation.
    """
    t, b, n = contract.horizon, contract.block_size, contract.expert_count
    z = (contract.maximum_operand_bits + 63) // 64
    key_max = max(q.key_words for q in tape)
    service_total = sum(max(service.service_cap(q, solver) for q in tape[start:start + b])
                        for start in range(0, t, b))
    # Each round makes <=3 hard lookups (before issue, admission, after close),
    # each scanning <=quota entries; use capacity or quota, whichever is less.
    keys = min(contract.hard_capacity, contract.quota) if hard else 0
    controller = (4096 + 8 + contract.random_bits * 10
                  + t * (service.EXPERT_CAP + 8192 + 64 * n * (z + 1)**2
                         + 12 * (keys + 1) * (key_max + 32)))
    if contract.hard_index == "hashed":
        # Fixed128 bucket allocation also occurs when hard overrides are off.
        # An active position makes <=3 paid key hashes; allow4 conservatively.
        # Each costs <=4*key_max+16 under the shared bounded helper tariff.
        # Linked-node reads/collision steps remain covered by the unchanged
        # worst-case full-key scan term, including total bucket collisions.
        controller += 256
        if hard:
            controller += t * (16 * key_max + 256)
    return service_total + controller


def execute(service, tape, contract, *, seed, hard=True, unit_limit=C.MAX_UNITS,
            purchase_solver="enumeration", provider_limit=None, scope_epoch="epoch-1"):
    """One new DEVELOPMENT episode; private truth scoring is a separate caller."""
    meter = C.CostMeter(unit_limit)
    broker = None
    service_rejection = getattr(service, "Rejected", C.Rejected)
    try:
        meter.pay("admission", "episode_input_contract", 8)
        if type(contract) is not Contract:
            raise C.Rejected("Use the exact finite broker contract.")
        if type(tape) is not tuple or len(tape) != contract.horizon:
            raise C.Rejected("Tape length must equal the declared complete horizon.")
        # The complete tape is public input but all methods pay actual reads.
        for query in tape:
            if type(query) is not service.Query:
                raise C.Rejected("Funding admission requires exact immutable public query records.")
            meter.pay("admission", "full_key_read_and_public_shape_cap", 32 + 8 * query.key_words)
        scope = _paid_scope((tape[0].semantics_version,
                             tape[0].source_version, scope_epoch), meter)
        cap = funded_cap(service, tape, contract, hard=hard, solver=purchase_solver)
        uniformly_funded = unit_limit >= cap and provider_limit is None
        if hard and contract.hard_capacity < contract.quota:
            uniformly_funded = False
        meter.pay_many((("output", "reserved_final_status_words", 64),
                        ("storage", "reserved_failure_state_words", 32)))
        bits = C.BitTape.seeded(contract.random_bits, seed, meter)
        broker = Broker(service, contract, meter, bits, scope, hard=hard,
                        purchase_solver=purchase_solver, provider_limit=provider_limit)
        for start in range(0, contract.horizon, contract.block_size):
            broker.begin_block(tape[start:start + contract.block_size])
            for _ in range(contract.block_size):
                broker.close(broker.issue())
        if bits.position != contract.random_bits:
            raise AssertionError("Successful broker did not consume the full fixed bit schedule.")
        result = broker.record()
        result["all_path_funded"] = uniformly_funded
        result["funded_cap"] = cap
        result["expectation_theorem_eligible"] = result["successful_quota_contract"] and uniformly_funded
    except (C.BudgetExceeded, C.Rejected, service_rejection) as error:
        if broker is not None:
            broker.failed, broker.failure_detail = True, type(error).__name__ + ": " + str(error)
            result = broker.record()
        else:
            result = {"stage": "DEVELOPMENT", "version": VERSION, "status": "failed",
                      "successful_quota_contract": False, "trace": [], "invoices": [],
                      "rounds_closed": 0, "purchases": 0,
                      "failure_detail": type(error).__name__ + ": " + str(error)}
    result.setdefault("all_path_funded", False)
    result.setdefault("expectation_theorem_eligible", False)
    result["meter"] = meter.snapshot()
    return result
