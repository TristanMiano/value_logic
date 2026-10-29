# Final assurance boundary

Codex (GPT-6), October29,2026 UTC. Same-model P3-11-A1 review.

The Layer/Mask definitions specify a recursive optimization whose repeated
subproblems need not be memoized by the Lean evaluator. The mathematical
table implementation stores one result for each(layer,receipt subset), of
which there are O(n*2^k). All transitions into a state use only those stored
values and local upper endpoints. Induction on layer proves that memoization
returns the same result as the recursive specification. The formal membership,
coverage and dominance proofs justify that specification; the written count
and inspected Python implementation justify the table realization. The
compiler accepting the recursive theorem does not itself establish its
evaluation time or the Python runtime's asymptotic behavior.

The formal capped proof uses a finite ceiling at least every local upper
endpoint, in place of an extended-real +infinity. Such a ceiling exists for
the finite table; empty entries may use arbitrary fixed defaults. Any
queried anchor value is bounded by its own finite local upper endpoint,
so clipping against that ceiling is harmless. The implementation's infinity
sentinel is a separate representation, audited in implementation.md.
This convention also handles an empty outside family for the one-block case.

The n source blocks can have different domains, dimensions and affine forms.
Their labels encode modeling roles. No exchangeability, probabilistic
independence or guarantee that one individual model is true is assumed.
The minimum aggregate is the quantity being analyzed under a supplied
contract; a maximum aggregate is covered by negating forms and outputs.
Neither operation establishes an epistemic warrant for choosing that aggregate.

The positive consequence is exact conditional inference, with a constructive
source or contradiction relative to retained premises. It can improve use
of uncertain/fallible models even though another conventional construction
with the same information ties. It does not establish that a minimum across
models is the best decision rule, that model plurality increases predictive
accuracy, or that retaining this particular representation always pays.

The reconstructed evidence supports the stated theorem, certificate contract,
resource account and noisy duty. No unaddressed technical defect has emerged.
The outstanding uncertainty for the whole contribution event is chiefly the
moderate-novelty judgment and incomplete access to two close literature items,
as retained in contribution_review.md. These limits should remain visible in
any author recommendation or later research report.
