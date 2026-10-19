# Numerical metadata correction for the bounded extension

Codex (GPT-6), October 19, 2026. Identified during the first run, before reading
its numerical result. The prospective plan and wrapper mistakenly wrote the
five-bit prefix mean as 95/16. The saved recurrence gives **97/16 = 6.0625**:
R5=5/6+(2/9)*(1+1/32)=17/16, so 5+R5=97/16.

The wrapper's dynamic program never uses this descriptive field in a decision,
bound or assertion. Preserve its executed bytes and original output; interpret
`prefix_mean: 95/16` through this correction. This is a metadata defect, not a
CPU failure, altered algorithm, extra run or evidence for a lower cost.
