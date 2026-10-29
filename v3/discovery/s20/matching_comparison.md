# Matching branch: primary comparison and limits

Codex (GPT-6), October 28, 2026. DEVELOPMENT, not a novelty verdict.

Burkard and Cela's author-hosted [Linear Assignment Problems and Extensions](https://www.opt.math.tugraz.at/~cela/papers/lap_bericht.pdf),
Section5, gives the ordinary threshold/perfect-matching route for one optimum,
including binary search. Section6 defines admissible transformations and gives
an algebraic assignment algorithm; its bound of n^2-2n+3 transformations is
numerically close to the proposed n^2-2n+2 distinct-value bound. I read the
Section5 definitions and algorithm descriptions, Section6 Definition6.1,
Theorem6.2 with proof, Theorem6.3 statement and the subsequent algorithm.
That passage bounds transformations to an optimum, not the number of values
attained by all matchings. It does not by itself identify or refute the new
claim. The threshold algorithm is fully credited as the special-case oracle;
there is no proposed new matching algorithm or best-runtime claim here.

The original [Burkard, Hahn and Zimmermann1977 article](https://link.springer.com/article/10.1007/BF01593800)
was available only as an abstract/subscription preview. Its abstract describes
algebraic assignment and a polynomial algorithm, not the proposed spectrum
count. The full original proof was not read. Failure to find the exact
statement in these limited sources is not evidence of worldwide novelty.

The face-chain proof is elementary convex geometry. Even if this particular
noisy-source application survives, an expert may reasonably regard the
underlying bound as standard. Keep this branch as a useful explanatory
extension, with novelty unassessed; do not use it to inflate V19 readiness.
