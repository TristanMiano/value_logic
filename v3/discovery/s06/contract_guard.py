#!/usr/bin/env python3
"""Admission guard for the specific source bytes underlying the s06 quotation.

DEVELOPMENT. ChatGPT (GPT-6 Astra Pro), 2026-10-12. Byte binding does not prove
semantics; the derivation in contract_findings.md applies to these bound bytes.
Independent witness and negative-proof checks still occur on every new call.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
import time

import contract_quote as quote


EXPECTED = {
    "contract_quote.py": "37ba5bcca266df999407e5819648e1d8fce6b79d055442daa3a8d80ca2867482",
    "maxsat_repair.py": "9ffa16975dea8d892a9379d3fa119ae63c1eaf70e30f171965457aa469835086",
    "maxsat_reprice.py": "cff64423b29dc9cb230c87d9126b17684f60e7bded43052117fc7362955c9f99",
}


def admit():
    """Check the quotation/procedure version before relying on its cap bound."""
    cpu, wall = time.process_time_ns(), time.perf_counter_ns()
    rows = []
    for filename in [quote.__file__, quote.source.__file__, quote.compilation.__file__]:
        path = Path(filename)
        payload = path.read_bytes()
        actual = hashlib.sha256(payload).hexdigest()
        if actual != EXPECTED[path.name]:
            raise ValueError("The finite tariff derivation is not admitted for changed source: " + path.name)
        rows.append(dict(file=path.name, sha256=actual, bytes=len(payload),
                         read_words=(len(payload)+7)//8,
                         sha256_blocks=(len(payload)+72)//64,
                         binding_compare_units=1))
    return dict(binding_rows=rows,
                declared_admission_units=sum(r["read_words"]+r["sha256_blocks"]+1 for r in rows),
                timing=dict(process_ns=time.process_time_ns()-cpu,wall_ns=time.perf_counter_ns()-wall),
                source_semantics="Manual finite-procedure derivation in contract_findings.md; no checksum-only proof admission.")


def finite_call_quote(instance):
    admission = admit()
    result = quote.finite_call_quote(instance)
    result["code_admission"] = admission
    return result


def execute_complete(instance, budget):
    admission = admit()
    result = quote.execute_complete(instance, budget)
    # Keep the underlying independently checked receipt identity and expose a
    # separate outer binding receipt/invoice, rather than changing its body.
    return dict(code_admission=admission, checked_call=result,
                total_operation_units=admission["declared_admission_units"]+result["total_operation_units"])
