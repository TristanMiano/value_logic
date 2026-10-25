# Unknown proof times: an early scheduling screen

Codex (GPT-6), s18 DEVELOPMENT. This is an ordinary portfolio/dovetail
construction, not a new generic metareasoning theorem.

The fixed-price membership oracle in total_search.md is a substantive
interface assumption. A proof search may have unknown runtime and may never
return a negative answer. Replace it by finitely many preemptible proof
procedures i. Procedure i, if it succeeds after tau_i units of its own
processing, returns a sound feasible action with warranted loss at most h_i.
The h_i are known nonnegative bounds; tau_i may be infinite. State retention,
preemption and proof verification must have the stated costs. No assumed
distribution over unresolved mathematical propositions is needed.

An idealized offset dovetail raises a virtual level b and gives each
procedure cumulative work x_i(b)=max(0,b-h_i). The first completion occurs
at b*=min_i(tau_i+h_i), if this minimum is finite. Total processing is
S(b*)=sum_i max(0,b*-h_i). If the completing procedure is j, the total
processing plus its returned loss is at most

    S(b*)+h_j <= (n-1)*b* + tau_j+h_j = n*b*.

Continuous equal sharing among currently active procedures implements the
allocation mathematically. A discrete machine needs a separately charged
quantum/rounding and switching analysis; the displayed factor does not
include an unpriced physical parallel computer. Arbitrary nonnegative loss
offsets do not invalidate the bound. When all h_i=0 this is ordinary fair
proof search, and the n factor cannot improve uniformly for deterministic
schedulers against a hidden sole fast procedure.

For anytime solvers, combine a checked primal upper bound from one run with
a checked dual lower bound from another. Their gap is usable even if neither
solver alone completed its task. If a pair needs processing s and t to
certify the requested gap, fair n-way sharing supplies both by at most
n*max(s,t) processing, no more than n*(s+t). This is a capability guarantee,
not a favorable complete-cost result. Practical solvers already share primal
and dual information; shared proof states may improve the bill further.

Disposition: retain the explicit asynchronous interface as a warning against
silently pricing arbitrary mathematical truth queries. The generic dovetail
and solver-sharing principles are elementary strong ordinary controls.
No implementation, novelty forecast or performance headline is warranted
without a more specific scheduling or receipt-reuse delta.
