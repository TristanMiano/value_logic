# A lower certificate can reject an edited solve before performing it

Codex (GPT-6), October24,2026 UTC. DEVELOPMENT; an additional operational
interpretation of the selected N16 inequalities, not an economic benchmark.

Let C=diag(1/10,9/10), c=(1,1)/sqrt(2), e=1/10, E=1/100.
At the feasible parameter t=1/4, a=5/4 and d=1/5, the lower bound is

    L=(1/2)*[(1/10)/(5/4-1/50)+(9/10)/(5/4-9/50)]
      =6070/13161 >23/50=0.46.

Suppose a known alternative incurs loss23/50. Taking the edited option
requires finding and using an optimizer, then incurs optimized loss F_N
plus a nonnegative computation cost. The certificate rejects that option
for every edit within the warranted budget. This decision does not need
the new optimizer: even its best possible objective is already too large.
The certificate itself and prior acquisition still have costs.

The conclusion tolerates C_minus=C-I/10000. The derivative of
L_t(z)=z/(a-dz) is a/(a-dz)^2<=500/441 on[0,1]. Therefore the rounded
lower value is at least6070/13161-1/8820, still strictly above23/50.
Truthful C_plus=C+I/10000 completes the existing checker interface.

Keeping only the old target value s=1/2 cannot justify this rejection:
M=I_2 and N=(11/10)I_2 have that same old value and edit radius1/10,
but F_N=100/221<23/50. This compares different information budgets.
The stronger old-solution-vector control already considered elsewhere
can also reject at this threshold; there is no superiority claim over it.
An ordinary calculation using the same retained block ties exactly.

The original upper-certificate example instead evaluates what a new
optimized objective can achieve. An upper value bound alone does not
deliver the optimizer or eliminate the cost of producing a deployed
solution. Lower rejection cleanly illustrates one way an information
certificate can avoid an unnecessary solve. No number of saved CPU
seconds, audit fees or end-to-end utility gain has been measured here.

The [unchanged-checker run](rejection_result.json) returns the exact rounded
lower value1517237495/3290365001 and verdict above. The
[script](rejection_check.py) also checks the analytic rounding margin and
the old-value-only counterexample, using246,200ns after imports on
Python3.12.14. The later serialization repair does not alter this result.
