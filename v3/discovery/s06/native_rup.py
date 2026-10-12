#!/usr/bin/env python3
"""Persistent IHS plus separately paid RUP proof calls and retained cuts.

DEVELOPMENT. ChatGPT (GPT-6 Astra Pro), 2026-10-12. The persistent method,
its actual native objects and checked witness route are inherited from the
frozen native_repair.py. Only the separately paid proof bridge is replaced.
"""
import time

import native_repair as old
import rup_bridge_v2 as rup
from native_repair import kernel,profile_kernel,S05,sha,structural_id,weighted_instance

VERSION='s06-native-ihs-rup-v1'


def capabilities():
    result=old.capabilities()
    result.update(adapter_version=VERSION,wrapper_sha256=sha(__file__),
                  inherited_adapter_sha256=sha(old.__file__),rup_bridge_sha256=sha(rup.__file__),
                  negative_bridge='Fresh bounded Glucose3 full-CNF export; independent strict RUP check; paid Boolean objective-cut antichain projection',
                  proof_persistence='Checked source-bound objective cuts survive weight changes. Fresh Glucose proof calls do not retain solver state.',
                  projection_limit='At most16 soft features by default; projection has a separately enforced operation cap. Failure retains checked scalar cuts but returns unresolved reusable support.',
                  excluded_claims=result['excluded_claims']+['No formal verification of the Python encoding/RUP/projection kernel',
                                                          'No claim that native IHS cores or raw optimum status become independent proofs'])
    return result


class PersistentIHS(old.PersistentIHS):
    def __init__(self,instance):
        super().__init__(instance)
        self.checked_cuts=[]
        self.cut_projections=[]

    def state(self):
        result=super().state()
        result['retained_rup_cuts']=len(getattr(self,'checked_cuts',[]))
        result['retained_cut_projections']=len(getattr(self,'cut_projections',[]))
        return result

    def purchase(self,weights,budget,limits=None,exact=False,proof_limits=None):
        if self.sat is None:
            raise RuntimeError('Native runtime closed')
        if type(budget) is not int:
            raise ValueError('Integer bounded decision budget required')
        caps=dict(old.DEFAULT_LIMITS)
        if set(limits or {})-set(caps):
            raise ValueError('Unknown native resource cap')
        caps.update(limits or {})
        for key,value in caps.items():
            if value<0 or (key!='mip_seconds_per_call' and type(value) is not int):
                raise ValueError('Nonnegative native caps required')
        pcaps=dict(rup.LIMITS)
        pcaps.update(proof_limits or {})
        # Existing per-purchase proof_units is an encoding/checking tariff
        # allocation, never a conversion of native search into those units.
        pcaps['encoding_units']=min(pcaps['encoding_units'],caps['proof_units'])
        pcaps['checking_units']=min(pcaps['checking_units'],caps['proof_units'])
        weighted=weighted_instance(self.instance,list(weights))
        meter=kernel.Meter(caps['adapter_units'])
        projection_meter=kernel.Meter(pcaps['projection_units'])
        before=self.state()
        events=[]
        got=native=None
        cpu,wall=time.process_time_ns(),time.perf_counter_ns()
        answer=dict(status='UNRESOLVED',model=None,proof=None,witness=None,checked_lower=None,checked_lower_receipt=None)
        try:
            meter.pay('admission','weight_source_budget_words',len(weights)+10)
            native=self._native(weighted,budget,exact,caps,meter,events)
            if native.get('witness') is not None:
                answer.update(witness=native['witness'],model=native['witness']['model'])
            if native['status']=='SAT' and not exact:
                answer['status']='SAT'
            elif native['status'] in ('LOWER_HINT','SAT'):
                proof_budget=native['witness']['original_cost']-1 if exact else budget
                got=rup.purchase(self.instance,list(weights),proof_budget,pcaps)
                self.calls['proof_provider_calls']+=1
                self.calls['glucose_proof_calls']+=got['native_calls']
                proof_event=dict(kind='separate_rup_proof_provider',purchase=got)
                events.append(proof_event)
                if got.get('checked_lower_receipt') is not None:
                    cut=got['checked_lower_receipt']
                    # `cut` was freshly constructed from just-checked raw
                    # export, not admitted from a serialized checked flag.
                    if not any(c['receipt_id']==cut['receipt_id'] for c in self.checked_cuts):
                        self.checked_cuts.append(cut)
                        meter.pay('proof_storage','source_bound_cut_reference',len(weights)+12)
                    answer['checked_lower']=cut['checked_lower']
                    # Project all own paid cuts. This is a source-independent
                    # objective relaxation; no logical model enumeration.
                    projected=rup.compile_cut_supports(self.instance,self.checked_cuts,projection_meter,
                                                       pcaps['max_projected_features'])
                    self.cut_projections.append(projected)
                    receipt=dict(checked=True,kind='rup_cut_projection',structural_source_id=self.structural_id,
                                 source_identity=weighted['identity'],weights=list(weights),budget=proof_budget,
                                 receipt_id=projected['receipt_id'],leaf_masks=projected['leaf_masks'],
                                 dependency=dict(cut_receipts=[c['receipt_id'] for c in self.checked_cuts]),
                                 projection=projected)
                    answer.update(status='SAT' if exact else 'UNSAT',proof=got['raw_proof'],checked_lower_receipt=receipt)
                elif got['status']=='SAT':
                    witness=got['witness']
                    answer.update(status='SAT',witness=witness,model=witness['model'])
                    if exact:
                        answer['native_optimum_disconfirmed']=True
                else:
                    answer['reason']='rup_bridge_'+got.get('reason','unresolved')
            else:
                answer['reason']=native.get('reason','native_incomplete')
        except kernel.CapReached:
            answer.update(status='UNRESOLVED',reason='adapter_or_projection_operation_cap')
        except ValueError as exc:
            answer.update(status='UNRESOLVED',reason=str(exc))
        self.purchases+=1
        proof_invoice=None if got is None else dict(total=got['invoice']['declared_units_excluding_native_search'],
            by_category=dict(encoding=got['invoice']['encoding']['total'],checking=got['invoice']['checking']['total']),
            bridge=got['invoice'],native_search_units=None)
        adapter_invoice=meter.record()
        adapter_invoice['total']+=projection_meter.total
        adapter_invoice['projection']=projection_meter.record()
        answer.update(version=VERSION,source_identity=weighted['identity'],structural_source_id=self.structural_id,
                      weight_id=kernel.digest(list(weights)),weights=list(weights),requested_budget=budget,exact_requested=exact,
                      caps=caps,proof_caps=pcaps,state_before=before,state_after=self.state(),native_result=native,events=events,
                      adapter_invoice=adapter_invoice,proof_provider_invoice=proof_invoice,native_search_units=None,
                      proof_native_timing=None if got is None else got.get('native_timing'),
                      retained_scalar_cuts=[dict(receipt_id=c['receipt_id'],weights=c['weights'],budget=c['budget']) for c in self.checked_cuts],
                      timing=dict(process_ns=time.process_time_ns()-cpu,wall_ns=time.perf_counter_ns()-wall))
        return answer
