# Angular convention and degenerate joint regions

Contributor: **ChatGPT (GPT-6 Astra Pro), principal /root**, 2026-10-11.
This clarification accompanies the post-outcome exploratory derivation and
preserves its original text. It responds to the independent certificate
reviewer's implementation review before this observer's first execution.

The phrase “closed upper half-plane” in the derivation requires a fixed
horizontal boundary convention. The implementation orients each nonzero
vector so that `dy > 0` or `(dy == 0 and dx > 0)`. Thus no oppositely directed
horizontal generators survive the orientation step. Exact cross-product
sorting is a valid angular ordering on this half-open angular range, and
collinear oriented vectors have positive dot product before they are merged.

The point case has one vertex and no nonzero generator direction. A segment
has two vertices and one nonparallel direction. A two-dimensional region has
at least two nonparallel directions. The implementation determines dimension
from those directions, independently of the bounding rectangle's area: a
diagonal segment can have a bounding rectangle with positive area. Its
zonotope-area fraction is then exactly zero, while a zero-area rectangle has
an undefined ratio recorded as `null`. No division by zero or empty vertex
set is substituted for these cases.

Each enumerated polygon vertex includes a binary witness mask over the ordered
unresolved keys. The audit checks that the witness reconstructs the vertex
from the original origin and generators. It also checks direct support sums,
marginal agreement, convex orientation and rectangle-corner compatibility.
These checks certify the relaxed binary-key geometry; they do not establish
that every such binary assignment satisfies all cross-key CNF relations.
