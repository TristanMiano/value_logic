# A priced prefix policy for a retained certificate

**DEVELOPMENT derivation; Codex (GPT-6), October 14, 2026.**

The first screen supports a simpler controller than repeated online block
lookahead. Fix a retained certificate/action, independent finite audit-score
laws, positive query fees c_i and an executable fallback of physical fee C.
Choose an order i_1,...,i_n before the request outcomes. Stop when accumulated
nonnegative score reaches quota Q. For a chosen cutoff k, query only its first
k coordinates; if still unresolved, execute fallback. Queries after success
are not bought. This is an ordinary sequential threshold/prefix policy, not
an optimal adaptive decision tree or a new decision-theoretic principle.

Let S_j be the score of the first j coordinates in that order, S_0=0. Its exact
expected physical fee is

```math
F_k=\sum_{j=1}^{k}c_{i_j}\Pr(S_{j-1}<Q)
       +C\Pr(S_k<Q).
```

Every query is bought precisely when the previous prefix has not completed;
fallback is bought precisely when the chosen prefix has not completed. Sum
the indicator invoices. Truncated score convolution gives all prefix tail
probabilities in O(n Q s) transitions for integer quota and support size at most
s, with exact integer probability counts. Different denominators are retained.

The difference between successive prefix values is

```math
F_k-F_{k-1}=c_{i_k}\Pr(S_{k-1}<Q)
 -C\Pr(S_{k-1}<Q\le S_k).
```

Some early differences may be positive before a later prefix repays them. Thus
minimizing all F_k can exploit complementary observations that the one-query
completion test rejects. Taking k=0 as a candidate proves min_k F_k<=C. If only
prefixes whose total listed fee is at most B are admitted, every realized fee
is at most B+C. These are physical-fee statements under the correct score law;
they do not price computation, acquisition of the logical certificate or an
incorrect probability model.

Choose among a few prospectively specified orders and their admissible cutoffs,
charging every evaluated order and transition. A fixed compiled sequence needs
only the next query index and score during execution. It does not require the
exponential observed-cost vector state of a general policy DAG. The price of
this simplicity is restriction to the selected static orders and one retained
certificate; no approximation to unrestricted optimum is claimed.

## Cost and comparison contract

Give every ordinary controller the same source, cuts, action and fallback.
Include an ordinary implementation of this exact prefix rule (a tie is expected),
a fixed-order threshold controller without cutoff optimization, and audit-first
with certificate checking before complete solve. A direct exact solver may be
cheaper than certificate compilation on short horizons; retain that possibility.
Count actual setup once per arm at the declared reuse horizon, never amortize it
over unexecuted future work. Report source admission, extraction, compiler,
receipts, final action checks, fallback proof acquisition and checking separately.

A full-information fallback can check a retained bound at the actual costs and
avoid a complete solve when that suffices; it must not be forced to solve just
to exaggerate the partial-information saving. If a new action is proposed, its
source model and its own certificate must be checked. The original supplied
action's regret bound does not transfer to an arbitrary improved action.

The first rc01 diagnostic passed 15 sources and 30 action choices, with 18,384
box states, 83,106 direct corners, 76,848 coordinate audits and 381 convolution
comparisons. There were 13,545 coordinate states where retained dual structure
contracted more than scalar-only transport. These are finite mathematical
counts, not physical purchases. Extraction is expensive on two mixed formulas:
their full setup is 122,905 and 77,741 named units, versus 157--1,170 on the other
sources. This cost must be included before claiming cheap general admission.
