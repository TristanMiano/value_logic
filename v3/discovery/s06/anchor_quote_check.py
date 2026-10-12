#!/usr/bin/env python3
"""Reconstruct the new anchor quotation on existing actual tiny receipts."""
from datetime import datetime,timezone
from fractions import Fraction as F
import json
from pathlib import Path
import sys
import time

import anchor_quotes as aq
import contract_quote as cq
import native_repair as native
from vertex_probe import jsonable

HERE=Path(__file__).resolve().parent


def run(output):
    if output.exists():
        raise FileExistsError('Preserve quotation evidence')
    wall,cpu=time.perf_counter_ns(),time.process_time_ns()
    meter=native.kernel.Meter()
    old=json.loads((HERE/'contract_results.json').read_text())
    tiny=old['tiny_source']; modes=old['tiny_cost_contract']['possible_cost_modes']
    if tiny['identity']!=native.kernel.digest({k:v for k,v in tiny.items() if k!='identity'}):
        raise ValueError('Changed tiny source')
    receipt=old['tiny']['initial_paid_lower_receipt']
    native.kernel.check_negative(tiny,receipt['budget'],receipt['provider_response']['proof'],meter)
    leaves=native.profile_kernel.compile_tree(receipt['provider_response']['proof'],meter)
    # The actual checked tree supplies independently admitted scalar values at
    # each declared anchor. No new provider or diagnostic optimum is run.
    lowers=[min(sum(w for j,w in enumerate(v) if z&(1<<j)) for z in leaves) for v in modes]
    witness=native.profile_kernel.compile_witness(tiny,3,meter)
    masks=[witness['violation_mask']]; possible=[[0,1]]
    audits=[aq.audit_quote(masks,modes,possible,lowers,8,0,j,meter) for j in range(2)]
    complete=aq.logical_quote(masks,modes,possible,lowers,8,[3,3],4,meter,complete=True)
    interrupted=aq.logical_quote(masks,modes,possible,lowers,8,[3,3],4,meter,complete=False)
    quote=cq.finite_call_quote(tiny)
    assert lowers==[3,3]
    assert all(q['guaranteed_gain']==0 for q in audits)
    assert complete['worst_bound']==2 and complete['guaranteed_gain']==2
    assert interrupted['worst_bound']==4 and interrupted['guaranteed_gain']==0
    paid=old['tiny']['paid_query']
    got=native.profile_kernel.compile_witness(tiny,paid['provider_response']['model'],meter)
    assert got['original_cost']<=4
    realized=aq.best(masks+[got['violation_mask']],modes,possible,lowers,8,meter)
    assert realized['bound']==0
    files=['anchor_quotes.py','anchor_quote_check.py','source_anchor.py','contract_results.json','contract_quote.py']
    for name in files:
        size=(HERE/name).stat().st_size
        meter.pay('input_admission','eight_byte_words',(size+7)//8)
        meter.pay('input_admission','hash_blocks',(size+72)//64)
    result=dict(status='passed',evidence='DEVELOPMENT same-model correspondence check',contributor='ChatGPT (GPT-6 Astra Pro)',
                created_utc=datetime.now(timezone.utc).isoformat(),hashes={name:native.sha(HERE/name) for name in files},
                source_id=tiny['identity'],admitted_anchor_lowers=lowers,audit_quotes=audits,
                logical_complete_quote=complete,logical_with_cap_quote=interrupted,finite_provider_quote=quote,
                realized_existing_witness=got,realized_certificate=realized,
                new_native_provider_or_audit_calls=0,
                scope='The already executed contract tiny example is reconstructed through a new scalar-anchor quotation; its historical two paid calls are not new execution or new validation.',
                invoice=meter.record(),timing=dict(wall_ns=time.perf_counter_ns()-wall,process_ns=time.process_time_ns()-cpu),
                accounting='Prospective finite-provider quote is separate from actual replay arithmetic. External audit price, native/host timing laws and full economic conversion remain unspecified.')
    output.write_text(json.dumps(jsonable(result),indent=2)+'\n')
    print(json.dumps(jsonable(dict(status=result['status'],audit_gains=[q['guaranteed_gain'] for q in audits],
                   complete_gain=complete['guaranteed_gain'],with_unresolved_gain=interrupted['guaranteed_gain'],invoice=meter.total))))


if __name__=='__main__':
    run(Path(sys.argv[1]))
