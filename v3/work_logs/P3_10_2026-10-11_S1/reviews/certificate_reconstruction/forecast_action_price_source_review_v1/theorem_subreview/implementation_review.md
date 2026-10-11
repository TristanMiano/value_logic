# Additive source review: exact price observer

Reviewer: **ChatGPT (GPT-6 Astra Pro), /root/certificate_reconstruction/decision_rank_information**, 2026-10-11.
Scope: source-only inspection; no summary data read and no scientific code executed.

**Disposition: PASS at the stated source and mathematical scope.** The implemented Fourier–Motzkin witness also resolves the strict-feasibility qualification raised in `derivation_review.md`; it does not rely on strict improvement occurring at a weak-region vertex. No numerical result or successful run is asserted by this review.

## Reviewed revisions

The initial derivation review remains bound to draft `c4055022904b258beccd3b1e71259d807bd72604cbaea464431ddd8ccb4fa266`. The initial observer was read at `a860b74090906e900f24c29364cf65c407dc99b83ea0f49483f5a7fbb06d4920`. During snapshot creation, later revisions were observed and separately read:

- Derivation: `81ecaf5d091d53786389a31a3c8455d6748186bf080f8e95aa5b43d355899678`.
- Observer: `8de009e469acd692c66b0e2ee3c26268d11609b97c7d711298488d0c89a0d72c`.

The two later revisions are preserved in `source_snapshot/`. Their additions explain the interior witness and turn empty-region multipliers into a convex certificate. The original signed derivation review is not rewritten.

## 1. Elimination signs and exact contradiction multipliers

For `a*lambda+b*mu<=d`, the observer correctly treats positive `b` as an upper bound and negative `b` as a lower bound. It combines a lower row with multiplier `-1/b_lower>0` and an upper row with multiplier `1/b_upper>0`, making the mu coefficient zero. Its assertions reconstruct both remaining coefficients and the right side from the original constraints.

Rows with `b=0` are retained directly. A projected row with zero lambda coefficient and negative right side is an immediate contradiction. Otherwise, positive lambda coefficients give upper bounds and negative coefficients lower bounds. When `L>U`, normalizing the active lower coefficient to -1 and upper coefficient to +1 gives `0<=U-L<0`; the recorded multipliers stay nonnegative. All multiplier overlaps are accumulated correctly.

Both quadrant rows are supplied by the caller. Hence the projected lower bound exists and is nonnegative, and the mu lower-bound list is nonempty. Unbounded upper endpoints are represented by `None`; adding 1 to a finite lower bound supplies a rational interior point without asserting a practical price threshold. Finite singleton intervals, constant constraints, and equality boundaries are retained.

The Cramer-rule formulas in `vertices` have the correct signs. Zero determinants skip parallel, coincident, and zero-normal pairs, while every original inequality remains in feasibility checking. Vertices are deduplicated by exact coordinate pairs, with all tight constraints retained. The independent agreement check between vertex existence and elimination feasibility is valid under the finite quadrant-constrained contract.

## 2. The returned witness lies in relative interior

The initial generic warning about inspecting only weak vertices remains correct, but it does not describe this observer's witness construction.

The chosen lambda is in the relative interior of its projected feasible interval: its midpoint when bounded, its singleton value when collapsed, or `L+1` when unbounded above. The chosen mu is similarly in the relative interior of its vertical feasible interval.

For completeness, consider any defining ordinary row tied at this point. If its mu coefficient is zero, the row is a projected inequality. A nonconstant projected affine inequality cannot be tight in the interior of a non-singleton feasible interval; if the projection is a singleton, equality holds throughout the full feasible set. A zero row tied at zero is also universally tight.

If the row has a nonzero mu coefficient, it cannot be tight when the vertical interval has positive length, because the constructed mu is strictly between its finite endpoints or strictly above its lower endpoint. If that interval collapses, an active lower and upper row yield a tight eliminated inequality. At an interior lambda in a non-singleton projection this eliminated affine inequality must vanish identically, forcing the same coincident lower and upper boundary throughout the feasible projection. Any row tied to it at the interior point must likewise be tight throughout the feasible set. When the projection itself is a singleton, a collapsed fiber is a single point. These cases establish the same conclusion.

Therefore every ordinary row tied at the returned point is universally tight on the weak region. Conversely, if strict improvement against all ordinary rows is feasible, each ordinary row has positive slack at this relative-interior witness. The observer's strict-slack test is thus complete for the finite exact system, with axes correctly excluded from the strict requirement. Zero prices remain admissible. Stating this lemma supports a claim stronger than merely “a strict witness was found.”

## 3. New convex certificate for empty regions

Let alpha_i be the nonnegative ordinary multipliers and let t_C,t_B be the nonnegative axis multipliers. Zero variable coefficients give

`sum alpha_i*(C_c-C_i)=t_C>=0` and `sum alpha_i*(B_c-B_i)=t_B>=0`.

The negative right side is `sum alpha_i*(W_i-W_c)<0`, so the ordinary mass `S=sum alpha_i` is strictly positive. Normalizing `pi_i=alpha_i/S` gives a convex combination with W strictly below the candidate and C and B no greater. The revised implementation computes exactly these quantities and checks the conclusions.

For every fixed nonnegative pair of score weights, that combination has strictly lower K, and at least one positively weighted ordinary component has K no greater than the combination. The valid quantifier is “for every price pair, some named component beats the candidate”; the selected component can depend on the prices. This is a mathematical certificate over saved records, not an executed mixture, an uncharged randomization service, or one fixed ordinary winner for all prices.

## 4. Catalogue and denominator checks visible in source

The source checks 76 total rows, excludes four rows with asymmetric stakes, and requires 24 symmetric rows in each of three families: 19 ordinary configurations, four candidate configurations, and one mirror. These counts exhaust the 72 symmetric rows. Its twelve candidate cells each use all 19 ordinary rows; the three mirrors are recorded as identities and excluded from that comparison catalogue. Named witness gaps must be positive in all three coordinates as defined, or the run fails.

Every candidate/ordinary vector extraction requires the complete-denominator flag, zero unknown-cost episodes, equal complete/planned/scored episode counts, and no incomplete-unit IDs. It reads exact rational pairs and takes action loss, cold units per scheduled request, and issued Brier from the named fields. The full population/seed aggregation and empirical truth of those flags remain inherited from the independently reconstructed, pinned summary; this source review does not inspect that data or recalculate those denominators.

**Optional source hardening:** the label “19 distinct ordinary configurations” relies on the pinned roster's identity contract. The observer asserts row counts but does not separately assert uniqueness of configuration IDs or absence of a reserved `axis:` prefix. Those identities are used as dictionary keys in certificates and slacks. A per-family unique-ID assertion and rejection of reserved-prefix collisions would make the local premise explicit. No actual duplicate or collision is asserted here.

## 5. Preserved scope

The expected summary hash is checked before JSON values are used. The global economic restriction is asserted false and propagated as false; optional report fees remain excluded, and no independent-policy-sample claim is made. The observer never calls a paid controller, generator, truth evaluator, scorer, or frozen analyzer. This review has not run the observer. New descriptive weights cannot repair an adverse frozen endpoint, establish equal-service reporting economics, or defeat an identical ordinary kernel.

Principal Research90 credit: **0 seconds**. No P3-11 or novelty assessment.
