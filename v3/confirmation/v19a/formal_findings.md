# Mechanized projection core: result and exact limits

Codex (GPT-6), October 28, 2026. P3-11-A1 same-model reconstruction.

Lean4.35.0 compiled all four prospectively named lemmas on the first compiler
attempt. The complete source, compiler transcript and environment identity
are sealed. No global axioms, admitted goals or unsafe evaluation were added.
The printed dependencies are Classical.choice for witness assignment;
propext, Classical.choice and Quot.sound for the interval/anchor lemmas;
and no axioms for the attained-largest-threshold lemma. These are Lean's
reported logical dependencies, not a claim that the compiler/hardware trust
base has been independently verified.

The source starts from actual local scalar choices and the definition of
an attained minimum. It proves the branch interval characterization, then
rearranges the branch union by anchor and label. The last lemma discharges
the existential threshold comparison when a largest value is attained.
Reflexivity and transitivity of the supplied order relation are explicit
parameters. The lemmas are general enough that totality and antisymmetry
are not needed at this abstract layer; finite real minima and rational
polytope images are instantiated in the mathematical reconstruction.

The compiler issued only deprecation warnings for accepted `if_pos`/`if_neg`
names. After saving its PASS record, the Python wrapper failed to print
the Unicode warning decorations on the cp1252 console. That deterministic
reporting error is preserved separately. The saved compiler exit code is0;
the wrapper's exit code was1. Only future console-summary printing was
repaired, and the compiler was not rerun. This was not attributed to the
user's possible hardware instability.

The17-second compile was not bracketed at entry by a principal wait mark.
The entire enclosing151-second E interval is therefore excluded from
research credit. The successful proof remains evidence; output does not
manufacture measured time.

These lemmas do not formalize real compactness/convexity, LP duality, subset
DP code, bit complexity, the Python verifier, or the noisy application.
They strengthen one mathematical link and do not complete P3-11 or settle
useful moderate novelty. The exact frozen candidate and event remain unchanged.
