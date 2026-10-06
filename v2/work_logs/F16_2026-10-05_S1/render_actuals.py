"""Render the closed accounting into current control documents; no research."""
from decimal import Decimal, localcontext
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[2]
a=json.loads((ROOT/'actuals.json').read_text())
def rounded(value):
    with localcontext() as c:
        c.prec=80
        return f'{Decimal(value):.6f}'
def minutes(ns):
    with localcontext() as c:
        c.prec=80
        return str(Decimal(ns)/Decimal(60_000_000_000))
replacement={
 'F16_OVERHEAD_TOTAL':rounded(a['minutes_decimal']['O']),
 'F16_ENGAGED_TOTAL':rounded(a['engaged_minutes_decimal']),
 'F16_TOOL_WAIT_TOTAL':rounded(a['minutes_decimal']['tool_wait']),
 'F16_RECOVERY_TOTAL':rounded(minutes(a['mode_and_exclusion_ns']['recovery_unobserved']+a['mode_and_exclusion_ns']['paused_recovery'])),
 'F16_POST_B_TOTAL':rounded(a['post_b_1']['close_minutes_decimal']),
 'F16_POST_B_REMAINING':rounded(a['post_b_1']['remaining_minutes_decimal']),
 'F16_LEDGER_ROWS_ADDED':str(a['ledger_rows_added']),
 'F16_LEDGER_ROWS_FINAL':str(a['ledger_final_rows']),
 'F16_ACCOUNTING_CUTOFF':a['accounting_cutoff_utc'],
}
for rel in ['TODO_v2.md','v2/work_logs/F16_2026-10-05_S1.md']:
 p=REPO/rel;s=p.read_text()
 for old,new in replacement.items():s=s.replace(old,new)
 p.write_text(s)
print(json.dumps(replacement,indent=2))
