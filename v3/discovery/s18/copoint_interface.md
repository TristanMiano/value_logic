# A common separator interface for uncertain and fallible witnesses

Codex (GPT-6), s18 DEVELOPMENT. A synthesis of the finite closure constructions,
not a new general separation theorem. Closure systems, copoints and robust
set cover are established mathematical machinery.

Fix a finite action set A and a known closure operator cl with cl(empty)=empty.
The unknown nonempty feasible set F is closed. Reports say F intersects T_i,
where each nonempty T_i is supplied in a specified representation; at most r<m
reports can be false. Reliable retained actions B are in F. For a target z,
a copoint is an inclusion-maximal closed set C excluding z. Finiteness ensures
that every closed set excluding z is contained in such a C.

Then z is guaranteed feasible exactly when every copoint C excluding z obeys

    B is not contained in C,
    OR more than r contacts T_i are disjoint from C.               (P1)

If(P1) holds, a source excluding z lies inside some C and cannot hit more
than m-r contacts while containing B. Conversely, if(P1) fails, declare the
at most r disjoint contacts faulty and use C as the compatible countermodel.
Every other report has a witness in T_i intersect C. If C is empty, r<m and
nonempty contacts prevent that countermodel, as required. This proof does
not assume independence between report errors.

For r=0 the same result follows by intersecting cl(B union{x_i}) over every
selector. The separator form avoids expanding those potentially exponentially
many selections. Its computational usefulness depends on the closure class,
the number/representation of separators and the cost of contact disjointness.

## Three explicit instantiations

- **Meet closure:** for proper z, separators can be taken as the complements
  of D_j(z)={x:x>=z and x_j=0}, one per zero coordinate. These complements
  are meet-closed: a meet entering D_j would require both operands to dominate
  z and one to have zero at j, so that operand was already outside the
  complement. Every generated-set failure has one such coordinate witness.
  Top uses A minus{top}. This recovers the count test and monotone least-action
  algorithm in meet_receipts.md and fallible_contacts.md.
- **Majority closure:** separators forbid a single unary/binary target
  pattern. The familiar binary-projection theorem supplies completeness.
  Compiling(P1) for all targets yields the ordinary2-CNF core.
- **Affine closure:** separators are affine hyperplanes excluding z.
  Their compact representation does not make universal quantification easy:
  the contact version encodes positive one-in-three satisfiability, and the
  full-point fault-budget version encodes a MaxCut threshold.

Some displayed separators need not be inclusion-maximal as written; this
does not affect the tests because they form a complete separating family.
Maximality is used only to state the generic finite interface succinctly.

## What a bounded reasoner can retain or reject

Each contact covers the separators it excludes. A positive certificate for z
is a cover, or an(r+1)-fold cover under the hard error budget, after removing
separators already ruled out by B. A minimum-cost certificate is therefore
an ordinary set-cover/multicover problem in this representation. The short
meet and majority certificates exploit their small target-specific families;
they do not turn general cover optimization into a free operation.

A negative certificate is a closed separator, at most r discarded reports,
and compatible points for the remaining contacts. In the three explicit
classes the separator itself has a short ordinary logical/algebraic form.
Such a certificate proves that the retained information does not authorize
z. It does not prove that z is actually infeasible in the true F. Further
paid evidence can remove the countermodel and change the decision.

The possible contribution is this specified incomplete-evidence interface
and its useful tractability/limitation distinctions. Ordinary methods given
the same information obtain the same conclusions. A full witness returned
by an actual solver, or a known complete source formula, may make this
restricted interface unnecessary; acquisition and deliberate retention must
be justified before an economic comparison. No generic novelty or promotion
is claimed from the duality alone.
