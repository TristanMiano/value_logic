# Exact source diagrams as an ordinary comparison

**Codex (GPT-6), October 14, 2026. DEVELOPMENT derivation.**

The next representation is a conventional layered ordered binary decision
diagram, with an explicit source-equivalence receipt. It is an ordinary
knowledge-compilation comparator, not a newly invented logical representation.
Retaining all layers (including equal-child nodes) makes weighted min-marginals
simple. Compilation can be exponential and every generated/checking state must
be charged. A small resulting diagram alone does not establish cheap admission.

Fix a variable order. At depth d represent the residual CNF by the original
clause indices not yet satisfied. The surviving literals of each active clause
are precisely those whose variables are at depths at least d. A child removes
clauses satisfied by its chosen literal. A state with an empty surviving clause
is false; an empty active set is true, with free future layers. This recurrence
is a source-equivalence proof by Shannon expansion. Memoize equal residual
states; merge diagram nodes with the same depth and two children. Retain a
separate trace from residual states to nodes. Checking clause removal and node
correspondence independently proves equivalence; a digest alone does not.

For signed weights q let B(v) be the minimum suffix cost at diagram node v,
with B(false)=infinity and B(true)=0. Then

```math
B(v)=\min\{B(v_0),q_i+B(v_1)\}.
```

Let F(v) be the minimum prefix cost reaching v, propagated from F(root)=0.
For each variable i, the minimum total objective subject to x_i=t is

```math
M_{it}=\min_{v\text{ at layer }i}\{F(v)+tq_i+B(v_t)\}.
```

The passes cost O(nodes + variables) arithmetic operations once the layered
diagram is admitted. They handle negative weights directly. An infinite
M_it means the corresponding value is impossible. A variable with only one
possible value contributes the same cost to every feasible action and its
regret cancels. Full-information fallback can omit these proved fixed variables.

For a feasible m-copy action with counts a, box [l,u], and
q_i=a_i u_i+(m-a_i)l_i, put A=sum a_i u_i. Exact regret is A-B(root).
After observing coordinate i at value t, the induced weight becomes m t.
Define b_i0=M_i0 and b_i1=M_i1-q_i. The exact post-query regret is

```math
R_i(t)=\max\{A-a_i u_i+a_i t-b_{i0},\;
                    A-a_i u_i-(m-a_i)t-b_{i1}\}.
```

Ignore a term for an impossible branch. Thus a completion certificate for a
fixed action is an interval of t values satisfying two affine inequalities.
All coordinate completion probabilities under a finite independent cost law
can be evaluated from one forward/backward pass, without a new source solve
per hypothetical response. Across a finite action menu, take the union of
completion intervals before summing response probabilities. Do not sum
overlapping action probabilities or assume the current best action remains best.

If an exact query costs c and a universally executable fallback costs at most C,
then c < C p(close) guarantees an expected fee improvement over immediate
fallback for that one step, when the response law conditional on observations
is correct. It does not include computation prices or prove globally optimal
query selection. A hard pre-query budget C gives pathwise fee at most 2C.
Improving the action menu may avoid more queries than optimizing their order.

For symmetric initial [-H,H], regret is
H max_v sum_i |a_i-m v_i|. A source diagram evaluates this exactly, but finding
the best feasible integer m-copy action is a further optimization problem.
A finite public menu must not silently stand for that global optimization.
