"""Paid selected-receipt reuse. P3-08 DEVELOPMENT only.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-10.
One fresh instance per owned episode. Selection, propensities, expert updates
and actions remain the broker's responsibility. This provider changes the
paid implementation of a selected checked receipt, not its truth value.
See derivations/08_selected_receipt_reuse.md for the coupling and funding scope.
"""
import p308_cnf as S
import p308_hashcache as H
from p308_common import C, resources

VERSION = "p308-selected-receipt-cache-v1.1"
PROVIDER = "owned_cached_cnf_receipt"
CACHE_CONTROL_CAP = 131072
MIN_ACCOUNT = 576


class CachedService:
    """Trusted local provider facade; audit data is never policy input."""
    Query = S.Query
    Receipt = S.Receipt
    Rejected = S.Rejected
    VERSION = VERSION
    PROVIDER = PROVIDER
    EXPERT_NAMES = S.EXPERT_NAMES
    EXPERT_CAP = S.EXPERT_CAP
    expert_predictions = staticmethod(S.expert_predictions)
    cost_proxy = staticmethod(S.cost_proxy)

    def __init__(self, *, cache_kind="linear", capacity=64):
        if cache_kind not in ("linear", "hashed"):
            raise S.Rejected("Use a named paid cache index.")
        self.cache_kind = cache_kind
        self.cache = (S.ExactCache if cache_kind == "linear" else H.ExactHashCache)(capacity)
        self.logical_calls = self.cold_calls = self.hits = 0
        self.audit = []

    def service_cap(self, query, solver="dpll"):
        return S.service_cap(query, solver) + CACHE_CONTROL_CAP

    def checked_purchase(self, query, limit_total=S.SERVICE_CAP+CACHE_CONTROL_CAP,
                         solver="dpll"):
        meter = C.CostMeter(limit_total)
        if meter.limit_total < MIN_ACCOUNT:
            # External admission rejection: no paid work or deployed response.
            raise S.Rejected("Selected receipt account must fund the 576-word response.")
        answer = witness = None
        status, detail, checked = "rejected", "", False
        key, query_id = (), "rejected-input"
        child = None
        cache_hit = False
        try:
            # First paid operation: every later admitted failure has a response.
            # Q<=343 and request ID<=16 words; 576 includes bounded metadata.
            meter.pay("output", "selected_cache_final_receipt_prepaid", MIN_ACCOUNT)
            meter.pay_many((("admission", "selected_cache_provider_contract", 16),
                            ("storage", "selected_cache_provider_call_state", 32)))
            if type(query) is not S.Query or solver not in ("enumeration", "dpll"):
                raise S.Rejected("Use the exact bounded query and named cold solver.")
            query_id, key = query.query_id, query.claim_key
            meter.pay_many((("storage", "selected_cache_provider_record_words", 32+query.key_words),
                            ("controller", "selected_cache_provider_call_counter", 8)))
            hit = self.cache.lookup(query, meter)
            if hit is None:
                cap = S.service_cap(query, solver)
                meter.pay("controller", "selected_cache_cold_cap_and_reservation", 8)
                meter.reserve("cold_provider", cap)
                child = S.checked_purchase(query, limit_total=cap, solver=solver)
                meter.absorb(child.resources, "selected_cache_cold_provider",
                             reservation="cold_provider", release=cap)
                self.cold_calls += 1
                meter.pay("check", "selected_cache_cold_receipt_binding", 32+query.key_words)
                if (type(child) is not S.Receipt or child.query_id != query.query_id
                        or child.claim_key != query.claim_key or child.provider != S.PROVIDER
                        or child.provider_version != S.VERSION):
                    raise S.Rejected("Cold child returned a misbound receipt.")
                if not child.successful:
                    if child.answer is not None or child.checked:
                        raise S.Rejected("Failed child exposed a purported hard answer.")
                    raise S.Rejected("Cold child did not complete a checked answer.")
                if child.checked is not True or type(child.answer) is not int or child.answer not in (0,1):
                    raise S.Rejected("Cold child success was not checked binary evidence.")
                self.cache.remember(query, child, meter)
                received = child
            else:
                meter.pay("check", "selected_cache_hit_receipt_binding", 32+query.key_words)
                if (type(hit) is not S.Receipt or hit.query_id != query.query_id
                        or hit.claim_key != query.claim_key or hit.provider_version != S.VERSION
                        or hit.provider not in ("bounded_cnf_exact_cache", H.PROVIDER)
                        or not hit.successful or hit.checked is not True
                        or type(hit.answer) is not int or hit.answer not in (0,1)):
                    raise S.Rejected("Cache hit lacks a current complete-key checked receipt.")
                # Its lookup invoice is already paid into this parent meter.
                # Do not absorb the delta receipt a second time.
                received, cache_hit = hit, True
                self.hits += 1
            meter.pay("acquisition", "selected_cache_checked_answer_release", 8)
            answer, witness, checked, status = received.answer, received.witness, True, "success"
            detail = ("Paid current checked cache receipt" if cache_hit else
                      "Paid cold checked receipt; retention follows cache capacity")
        except (C.BudgetExceeded, C.Rejected, S.Rejected) as exc:
            status = "budget_exhausted" if isinstance(exc,C.BudgetExceeded) else "rejected"
            detail = type(exc).__name__+": "+str(exc)
        self.logical_calls += 1
        receipt = S.Receipt(query_id,key,answer,checked,status,PROVIDER,VERSION,
                            resources(meter),witness,detail[:192])
        # This audit is external instrumentation, never consulted by the
        # provider or passed into any learning/advice/selection operation.
        self.audit.append({"query_id":query_id,"status":status,"cache_hit":cache_hit,
                           "cold_receipt":None if child is None else child.record(),
                           "adapter_receipt":receipt.record()})
        return receipt

    def audit_record(self):
        return {"stage":"DEVELOPMENT","version":VERSION,"cache_kind":self.cache_kind,
                "capacity":self.cache.capacity,"logical_selected_calls":self.logical_calls,
                "physical_cold_calls":self.cold_calls,"checked_cache_hits":self.hits,
                "retained_words":self.cache.retained_words,"requests":self.audit,
                "fresh_instance_for_each_episode_required":True,
                "audit_is_policy_input":False}
