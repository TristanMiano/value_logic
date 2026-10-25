# A polynomial ordinary comparator for tied and corrupted choice feedback

Codex (GPT-6), s18 DEVELOPMENT. Constructive improvement of tied_feedback.md.
The ranking operation is the established strongest-path/Schulze construction;
the question is the scoped online mistake guarantee, not a new voting method.

Use the same fixed unknown utilities, arbitrary available subsets and at most
C nonoptimal responses. Let c_ab count responses asserting a>=b. One may
record only the received winner versus the proposed action, or every winner
versus another currently available alternative. Either rule includes the
pair needed below. For each ordered pair, c_ab<=C whenever u_a<u_b:
that assertion can appear only in a corrupted round, at most once per round.

Define p_ab as the maximum, over directed a-to-b paths, of the minimum
edge count on the path. Zero-capacity paths are allowed. Rank a strictly
ahead of b whenever p_ab>p_ba, and take any total extension of this relation.
Return the highest-ranked available alternative.

## The strict beatpath relation is transitive

Strongest paths satisfy p_ac>=min(p_ab,p_bc). Suppose a outranks b and b
outranks c but p_ac<=p_ca. Put t=min(p_ab,p_bc), so p_ca>=t. If
p_ab<=p_bc, then p_ba>=min(p_bc,p_ca)>=p_ab, a contradiction. Otherwise
p_cb>=min(p_ca,p_ab)>=p_bc, again a contradiction. Thus a outranks c.
Irreflexivity and transitivity ensure a total extension exists.

## A high-count true comparison is never reversed

For u_a>u_b, every path from b to a contains a strictly utility-increasing
edge. Its assertion is false and its count is at most C. Consequently
p_ba<=C. If c_ab>C, then p_ab>=c_ab>C>=p_ba and every total extension
puts a ahead of b.

On any uncorrupted round with a suboptimal proposed j, the returned optimum
i has u_i>u_j but j precedes i in the selected order. Therefore c_ij<=C
before the update. The update increments that correct comparison. Each
strictly ordered pair can be charged at most C+1 such mistaken rounds,
and corrupted rounds add at most C. Hence

    mistakes <= binom(d,2)*(C+1)+C,
    true regret <= M*[binom(d,2)*(C+1)+C]

when all roundwise utility ranges are at most M. No utility gap, known C,
or consistent tie-breaking by the feedback source is required.

Max-min Floyd--Warshall computes all p_ab in O(d^3) elementary operations;
topological extension adds O(d^2). Counters use O(d^2 log(T+1)) bits after
T rounds. A supplied hard bound C0 permits saturation at C0+1 and
O(d^2 log(C0+2)) counter bits, with the same proof using C0. Arithmetic
bit costs, context processing and feedback acquisition are separate.

This strictly improves the earlier exponential ordering implementation's
worst-case computation while retaining its exact mistake guarantee. It
does not dominate the existing O((C+1)d log d) M-convex result on that
result's distinct-utility domain. Nor does it establish a new Schulze
property without comparison to the voting literature.

## Further qualifications

Full winner-versus-context feedback is safe here without the extra factor
d in the Kemeny proof: each false PAIR count is at most C, even if one bad
round creates several false pairs. The path proof uses that per-pair bound.
It does not require a bound C on the total number of false comparison edges.

A naive move-before-the-prediction list update can fail with no corruption.
Let A be strictly better than tied B,C. Starting order B,A,C, alternate
contexts{B,C} and{A,B}: report C then A. The orders become C,B,A then
C,A,B. Next use{B,C} and{A,C}, reporting B then A. This returns to B,A,C.
Every second round is truly mistaken; all responses are optimal. This
rejects that cheap list-update shortcut, not ordinary preference learning.

The result is presently restricted to selecting one named alternative.
Compound matroid actions require a proved comparison-extraction argument;
do not silently import the bound for them. A focused primary comparison
and bounded implementation check are the next screens. Novelty and
practical full-cost gains remain unassessed.

## Primary-source binding and the winning-votes variant

Schulze's2003 paper, Sections2--4, uses vote MARGINS for the initial edge
strength, proves the same path-transitivity lemma and gives the cubic Floyd
algorithm. The broader manuscript also discusses winning votes. The raw
counts above must therefore be named explicitly; do not call them the
2003 margin implementation without qualification.

The guarantee also holds with the usual winning-edge initialization:

    w_ab = c_ab if c_ab>c_ba, and0 otherwise.

Use w in the strongest-path calculation. A falsely directed edge still has
capacity at most C. If u_a>u_b and c_ab>C, then c_ba<=C, so this correct
edge is retained with capacity c_ab>C. The same high-count lemma and mistake
bound follow. In contrast, a margin initialization has the immediate
sufficient threshold c_ab>2C, giving the weaker direct bound
binom(d,2)*(2C+1)+C. These are explicitly different algorithm choices.

References: [Schulze2003](https://lists.gnu.org/archive/html/demexp-dev/2003-09/pdfte6xCA0eUd.pdf),
[extended manuscript, definitions and winning-votes discussion](https://aso.icann.org/wp-content/uploads/2019/02/schulze1.pdf).
The2018 arXiv PDF fetch timed out. None of the election axioms are claimed
for our evolving partial-feedback stream merely from using its path kernel.
