"""Clarify current reporting without rewriting any historical recurrence row."""
from pathlib import Path
import json

p=Path(__file__).resolve().parents[2]/'recurrences.json'
raw=p.read_text(encoding='utf-8'); before=json.loads(raw)
replacements={
    'Historical N/A cells are preserved. From s07 onward, reassess the declared event numerically every recurrence, permitting broad uncertainty.':
    'Historical N/A cells and dated assessments are preserved. Reassess a specified event only when warranted; otherwise carry its dated assessment explicitly. New targets remain unassessed until evidence supports their own forecast.',
    'The author requires useful quantitative columns and a numerical promotion forecast at each recurrence; this overrides the older prospective N/A instruction, preserving history.':
    'The author requires relevant progress metrics and a visible promotion forecast with candidate/event scope. The October 14 clarification distinguishes the broad program from F01; dated carries and new unassessed targets are explicit.',
    'Numerically reassess the same declared event every recurrence, with central estimate, subjective range, rationale, risks, same-event percentage-point changes and gaps to 80/90. A different event starts a new series. Never reconstruct older probabilities.':
    'For a new assessment retain the exact event and report estimate, range, rationale, risks and comparable changes. Otherwise carry its original date, event and assessment without claiming a new measurement. A different claim starts a separate series and may remain UNASSESSED. Never reconstruct old probabilities.'
}
for old,new in replacements.items():
    assert old in raw
    raw=raw.replace(old,new,1)
after=json.loads(raw)
assert after['rows']==before['rows']
p.write_bytes(raw.encode('utf-8'))
print('Current reporting policy clarified; all 21 recurrence objects unchanged.')
