"""Paid public-only live-performance reporting. P3-08 DEVELOPMENT.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-10.
Implements derivations/08_live_hard_performance.md. Input is a completed
record of the trusted local broker, not an externally authenticated receipt.
The reporter never calls a truth evaluator or reads an unpurchased answer.
Exact rational outputs are deliberately unreduced integer pairs: no hidden
Fraction normalization is required by this declared word-record service.
"""
from __future__ import annotations

import math

from p308_common import C
from p308_broker import Contract, VERSION as BROKER_VERSION

VERSION = "p308-live-performance-v1"
MAX_BITS = 256
# A conservative universal completion budget for the bounded input contract.
# At most 8192 rows, 4096 checked keys, 1024 words/key: all linear key scans
# cost <2^38, and all remaining bounded arithmetic/output costs <2^38.
# The extra factor >512 covers fixed validation and report serialization.
REPORT_FUNDING_CAP = 1 << 48


class IntegerMeter:
    """Precharged bounded signed-integer word operations."""
    def __init__(self, meter):
        self.meter = meter
        self.peak_bits = 1

    def _bits(self, value):
        if type(value) is not int:
            raise C.Rejected("Reporting arithmetic requires exact integers.")
        bits = max(1, abs(value).bit_length())
        if bits > MAX_BITS:
            raise C.Rejected("Reporting integer exceeds the finite width.")
        self.peak_bits = max(self.peak_bits, bits)
        return bits

    def op(self, name, a, b):
        aa, bb = self._bits(a), self._bits(b)
        za, zb = (aa + 63) // 64, (bb + 63) // 64
        if name in ("add", "sub"):
            bound, price = max(aa, bb) + 1, max(za, zb) + 2
        elif name == "mul":
            bound, price = aa + bb, 2 * za * zb + za + zb + 2
        elif name == "div":
            if b <= 0:
                raise C.Rejected("Reporting divisor must be positive.")
            bound, price = aa, 2 * (za + 1) * (zb + 1) + 2
        else:
            raise C.Rejected("Unknown reporting operation.")
        if bound > MAX_BITS:
            raise C.Rejected("Reporting pre-operation width exceeds its cap.")
        self.meter.pay("assessment", "report_integer_" + name, price)
        self.peak_bits = max(self.peak_bits, bound)
        value = a + b if name == "add" else a - b if name == "sub" else a * b if name == "mul" else a // b
        self._bits(value)
        return value

    def add(self, a, b): return self.op("add", a, b)
    def sub(self, a, b): return self.op("sub", a, b)
    def mul(self, a, b): return self.op("mul", a, b)
    def div(self, a, b): return self.op("div", a, b)

    def compare(self, a, b):
        z = (max(self._bits(a), self._bits(b)) + 63) // 64
        self.meter.pay("assessment", "report_integer_compare", 2 * z + 2)
        return (a > b) - (a < b)

    def minimum(self, a, b): return a if self.compare(a, b) <= 0 else b
    def maximum(self, a, b): return a if self.compare(a, b) >= 0 else b

    def ceil_sqrt(self, n):
        bits = self._bits(n)
        if n < 0:
            raise C.Rejected("Square-root input must be nonnegative.")
        self.meter.pay("assessment", "report_integer_sqrt_envelope", 8 * (bits + 1)**2)
        x = math.isqrt(n)
        return x + int(x * x < n)

    def pair(self, numerator, denominator):
        bn, bd = self._bits(numerator), self._bits(denominator)
        if denominator <= 0:
            raise C.Rejected("Output rational denominator must be positive.")
        # Typed integer words plus conservative binary-to-decimal output work.
        self.meter.pay("output", "report_exact_rational_words", 4 + (bn + 63)//64 + (bd + 63)//64 + 2 * (bn + bd))
        return [numerator, denominator]


def _same_key(a, b, words, meter):
    meter.pay("check", "report_complete_key_comparison", 2 * words + 4)
    return a == b


def _key_words(key, meter):
    if type(key) not in (tuple, list) or len(key) != 4:
        raise C.Rejected("Malformed public semantic key.")
    semantics, source, variables, clauses = key
    if (type(semantics) is not str or type(source) is not str
            or len(semantics) > 64 or len(source) > 64
            or type(variables) is not int or not 1 <= variables <= 12
            or type(clauses) not in (tuple, list) or len(clauses) > 64):
        raise C.Rejected("Public semantic key outside the bounded source contract.")
    meter.pay("admission", "report_clause_shape_reads", 4 * len(clauses) + 16)
    if any(type(c) not in (tuple, list) or len(c) > 4 for c in clauses):
        raise C.Rejected("Clause outside the bounded source contract.")
    literals = sum(len(c) for c in clauses)
    meter.pay("admission", "report_literal_validation", 4 * literals)
    if any(type(x) is not int or x == 0 or abs(x) > variables for c in clauses for x in c):
        raise C.Rejected("Literal outside the bounded source contract.")
    words = 4 + (len(semantics) + 7)//8 + (len(source) + 7)//8 + len(clauses) + literals
    if words > 1024:
        raise C.Rejected("Reporting key word bound exceeded.")
    return words


def report_owned_episode(service, episode, *, unit_limit=C.MAX_UNITS):
    """Compute one declared two-sided report from the owned broker's record.

    Low reporting budgets retain a failed record and actual spent resources.
    A successful finite-budget calculation is not labeled confidence-eligible
    without both the broker's all-path premise and this reporter's completion
    envelope. Exact identities can still be independently audited on it.
    """
    meter = C.CostMeter(unit_limit)
    integer = IntegerMeter(meter)
    output = {"stage": "DEVELOPMENT", "version": VERSION,
              "status": "failed", "confidence_eligible": False,
              "public_only": True, "authority": "trusted_local_broker",
              "coverage": "per-declared-episode fixed-end; no simultaneous multi-arm or conditional-on-success claim",
              "funded_reporting_cap": REPORT_FUNDING_CAP}
    try:
        meter.pay_many((("output", "report_reserved_final_status", 128),
                        ("admission", "report_contract_and_authority", 128)))
        if (type(episode) is not dict or episode.get("version") != BROKER_VERSION
                or episode.get("status") != "success"
                or episode.get("successful_quota_contract") is not True):
            raise C.Rejected("Only the completed owned broker schema is admitted.")
        raw = episode["contract"]
        contract = Contract(raw["horizon"], raw["block_size"], raw["expert_count"],
                            raw["action_bits"], raw["state_bits"], raw["selector"],
                            raw["hard_capacity"])
        t, b, m = contract.horizon, contract.block_size, contract.quota
        d = 1 << contract.action_bits
        p = b if contract.selector == "uniform" else 2 * b
        multiple = 1 if contract.selector == "uniform" else b + 1
        rows, blocks, invoices = episode["trace"], episode["blocks"], episode["invoices"]
        if len(rows) != t or len(blocks) != m or len(invoices) != m:
            raise C.Rejected("The completed transcript does not fulfill its quota.")
        scope = episode["scope"]
        meter.pay("storage", "report_fixed_accumulators", 128)
        known = []
        u_num = integer.div(integer.mul(integer.mul(t - m, d), multiple), 2)
        d2 = integer.mul(d, d)
        a_num = integer.div(integer.mul(integer.mul(t, d2), multiple), 2)
        q_num = delta_f = delta_v = delta_z = 0
        v_low = v_high = f_low = f_high = n_live = 0
        for k, block in enumerate(blocks):
            meter.pay("admission", "report_owned_selector_record", 48 + 4 * b)
            selected = block["selected"]
            ticket, favorite = block["ticket"], block["favorite"]
            if (type(selected) is not int or not 0 <= selected < b
                    or type(ticket) is not int or not 0 <= ticket < p
                    or type(favorite) is not int or not 0 <= favorite < b
                    or block["block"] != k):
                raise C.Rejected("Malformed actual selection record.")
            implied_selected = ticket if contract.selector == "uniform" or ticket < b else favorite
            if selected != implied_selected:
                raise C.Rejected("Ticket and selected position disagree.")
            selected_mult = 1 if contract.selector == "uniform" or selected != favorite else b + 1
            if block["multiplicity"] != selected_mult:
                raise C.Rejected("Actual selected multiplicity disagrees.")
            width = 0
            for offset in range(b):
                row = rows[k * b + offset]
                # Charge the record header, then actual bounded clause/key
                # reads. Do not debit a full 1024-word key for a short query.
                meter.pay("admission", "report_public_row_header", 128)
                key = row["claim_key"]
                words = _key_words(key, meter)
                meter.pay("admission", "report_public_row_key_read", 8 * words)
                if (row["index"] != k * b + offset or row["block"] != k
                        or row["scope"] != scope or list(key[:2]) != list(scope[:2])
                        or type(row["selected"]) is not bool
                        or row["selected"] != (offset == selected)):
                    raise C.Rejected("Public row chronology or scope mismatch.")
                multiplicity = 1 if contract.selector == "uniform" or offset != favorite else b + 1
                if row["propensity"] != [multiplicity, p] or block["propensities"][offset] != [multiplicity, p]:
                    raise C.Rejected("Reported probability is not the owned selector's actual law.")
                num, den = row["base_q"]
                out, out_den = row["emitted_q"]
                if any(type(x) is not int for x in (num, den, out, out_den)) or den != d or out_den != d or not 0 <= num <= d or not 0 <= out <= d:
                    raise C.Rejected("Forecast is not a valid immutable contract dyadic.")
                if any(type(row[z]) is not int or row[z] not in (0, 1) for z in ("base_action", "prospective_action", "base_terminal", "terminal_action")):
                    raise C.Rejected("Terminal/action record is not binary.")
                prior = None
                for old_key, answer, old_words in reversed(known):
                    if _same_key(old_key, key, old_words + words, meter):
                        prior = answer
                        break
                hard = row["hard_before"] == "checked"
                if row["hard_before"] not in ("checked", "unresolved"):
                    raise C.Rejected("A completed epoch cannot report stale/conflicted issuance.")
                if hard and (prior is None or out != prior * d or row["prospective_action"] != prior):
                    raise C.Rejected("A hard override lacks an earlier current owned receipt.")
                if not hard and (out != num or row["prospective_action"] != row["base_action"]):
                    raise C.Rejected("An unresolved output must retain the base forecast and action.")
                meter.pay("check", "report_forecast_chronology_and_action_binding", 64 + 2 * words)
                known_label = prior if hard else None
                if offset == selected:
                    receipt = invoices[k]
                    meter.pay("check", "report_purchased_receipt_binding", 64 + 4 * words)
                    if (receipt["provider"] != service.PROVIDER or receipt["provider_version"] != service.VERSION
                            or receipt["status"] != "success" or receipt["checked"] is not True
                            or receipt["query_id"] != row["query_id"]
                            or not _same_key(receipt["claim_key"], key, words, meter)
                            or type(receipt["answer"]) is not int or receipt["answer"] not in (0, 1)
                            or row["purchased_label"] != receipt["answer"]):
                        raise C.Rejected("Purchased row lacks its owned current checked receipt.")
                    label = receipt["answer"]
                    if prior is not None and prior != label:
                        raise C.Rejected("Contradictory receipts cannot support this report.")
                    if row["base_terminal"] != label or row["terminal_action"] != label:
                        raise C.Rejected("A selected terminal action was not corrected.")
                    r_num = integer.mul(integer.sub(num, d // 2), 1 - 2 * label)
                    factor = integer.div(multiple, multiplicity)
                    u_num = integer.add(u_num, integer.mul(integer.mul(p - multiplicity, r_num), factor))
                    a_num = integer.add(a_num, integer.mul(integer.mul(integer.mul(p, r_num), d), factor))
                    known_label = label
                    if prior is None:
                        meter.pay("storage", "report_checked_key_retention", 8 + words)
                        known.append((key, label, words))
                elif row["purchased_label"] is not None or row["base_terminal"] != row["base_action"] or row["terminal_action"] != row["prospective_action"]:
                    raise C.Rejected("An unselected row changes its owned terminal path.")
                if hard:
                    diff = integer.sub(num, integer.mul(d, prior))
                    delta_f = integer.add(delta_f, integer.mul(diff, diff))
                    if offset != selected:
                        loss_num = integer.add(num, integer.mul(integer.sub(d, integer.mul(2, num)), prior))
                        delta_v = integer.add(delta_v, loss_num)
                        delta_z = integer.add(delta_z, int(row["base_action"] != prior))
                elif offset != selected:
                    n_live = integer.add(n_live, 1)
                    v_low = integer.add(v_low, integer.minimum(num, integer.sub(d, num)))
                    v_high = integer.add(v_high, integer.maximum(num, integer.sub(d, num)))
                if known_label is not None:
                    live_diff = integer.sub(out, integer.mul(d, known_label))
                    exact = integer.mul(live_diff, live_diff)
                    f_low, f_high = integer.add(f_low, exact), integer.add(f_high, exact)
                else:
                    left = integer.mul(out, out)
                    right = integer.mul(integer.sub(d, out), integer.sub(d, out))
                    f_low = integer.add(f_low, integer.minimum(left, right))
                    f_high = integer.add(f_high, integer.maximum(left, right))
                variance = integer.mul(num, integer.sub(d, num))
                a_num = integer.sub(a_num, integer.mul(variance, multiple))
                magnitude = abs(integer.sub(d, integer.mul(2, num)))
                candidate_width = integer.mul(integer.mul(magnitude, p), integer.div(multiple, multiplicity))
                width = integer.maximum(width, candidate_width)
                meter.pay("storage", "report_accumulator_update", 32)
            q_num = integer.add(q_num, integer.mul(width, width))
        r = integer.mul(p, integer.ceil_sqrt(integer.mul(2, m)))
        q_den = integer.mul(d2, integer.mul(multiple, multiple))
        common = integer.mul(integer.mul(8, r), q_den)
        rho = integer.add(integer.mul(8, q_num), integer.mul(integer.mul(5, integer.mul(r, r)), q_den))
        u_scaled = integer.mul(u_num, integer.div(common, integer.mul(d, multiple)))
        a_scaled = integer.mul(a_num, integer.div(common, integer.mul(d2, multiple)))
        live_u = integer.sub(u_scaled, integer.mul(delta_v, integer.div(common, d)))
        live_a = integer.sub(a_scaled, integer.mul(delta_f, integer.div(common, d2)))
        action_radius = integer.ceil_sqrt(integer.div(integer.add(integer.mul(5, n_live), 1), 2))
        z_radius = integer.add(rho, integer.mul(action_radius, common))
        v_min = integer.mul(v_low, integer.div(common, d))
        v_max = integer.mul(v_high, integer.div(common, d))
        f_min = integer.mul(f_low, integer.div(common, d2))
        f_max = integer.mul(f_high, integer.div(common, d2))

        def interval(center, radius, lower, upper):
            low = integer.maximum(integer.sub(center, radius), lower)
            high = integer.minimum(integer.add(center, radius), upper)
            return {"lower": integer.pair(low, common), "upper": integer.pair(high, common),
                    "confidence_conflict": integer.compare(low, high) > 0}

        if n_live == 0:
            # An exact observable statement is stronger here and needs no
            # sampling coverage assertion. Preserve the generic centers too.
            v_interval = interval(0, 0, 0, 0)
            z_interval = interval(0, 0, 0, 0)
            f_interval = interval(f_min, 0, f_min, f_max)
        else:
            v_interval = interval(live_u, rho, v_min, v_max)
            f_interval = interval(live_a, rho, f_min, f_max)
            z_interval = interval(live_u, z_radius, 0, integer.mul(n_live, common))
        output.update(status="success", confidence_eligible=bool(episode.get("all_path_funded")) and unit_limit >= REPORT_FUNDING_CAP,
                      confidence_level=[19, 20], all_path_reporting_funded=unit_limit >= REPORT_FUNDING_CAP,
                      n_live=n_live, exact_all_remaining_known=n_live == 0,
                      base_centers={"V": integer.pair(u_scaled, common), "F": integer.pair(a_scaled, common)},
                      live_centers={"V": integer.pair(live_u, common), "F": integer.pair(live_a, common)},
                      corrections={"F": integer.pair(delta_f, d2), "V": integer.pair(delta_v, d), "Z": delta_z},
                      Q=integer.pair(q_num, q_den), R=r, sampling_radius=integer.pair(rho, common), action_radius=action_radius,
                      intervals={"V": v_interval, "F": f_interval, "Z": z_interval},
                      deterministic_envelopes={"V": [integer.pair(v_min, common), integer.pair(v_max, common)],
                                               "F": [integer.pair(f_min, common), integer.pair(f_max, common)],
                                               "Z": [[0, 1], [n_live, 1]]},
                      rows_read=t, purchased_labels_read=m, retained_checked_keys=len(known),
                      peak_integer_bits=integer.peak_bits)
        meter.pay_many((("output", "report_metadata_words", 512),
                        ("storage", "report_terminal_retention", 512)))
    except (C.BudgetExceeded, C.Rejected, KeyError, TypeError, ValueError, IndexError) as error:
        output = {"stage": "DEVELOPMENT", "version": VERSION, "status": "failed",
                  "confidence_eligible": False, "failure_detail": type(error).__name__ + ": " + str(error),
                  "public_only": True, "peak_integer_bits": integer.peak_bits}
    output["meter"] = meter.snapshot()
    return output
