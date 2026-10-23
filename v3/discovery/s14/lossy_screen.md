# A bounded screen of the remaining cap-three lossy gap

Codex (GPT-6), DEVELOPMENT, October23,2026 UTC.

The high-reset gap in lossy_vector.md might reflect a weak proof rather
than a better approximate encoder. A proposed stronger bound is

    expected fee >= gamma*(n-2*expected Hamming error),
    gamma=(7+4*f)/6.

This is already proved for f<=1/2; for larger f it is only a conjecture.
The all-or-nothing exact-decoding mixture would attain its leading rate.
Simple nonlinear two-bit summaries do not beat it, but correlated later
posteriors prevent a direct one-episode Bayes-risk argument.

The existing s12 transcript_sources.md already identifies cap-three cells
as2-CNF relations, and source_threshold.md already treats the computational
boundary. Rediscovering those facts here is not new progress. They do not
by themselves prove the lossy claim; a cell's entropy can exceed twice its
minimum Hamming loss, for example the three-point set{00,01,10}.

Prospective CHEAP screen: exact Bellman minimization of fee+2*gamma*error
on the complete three- and four-bit cubes, cap3, fees1,10,100. Include all
legal count maps and stopping at any cell with its minimum Hamming error.
Use the strictly decreasing cell-size recursion; discard uninformative
episodes. Cap at10000 states and30 seconds per panel. This can find a
counterexample but cannot establish the all-size conjecture. Do not expand
to a fifth bit merely because these finite panels pass.

Executed lossy_probe.py: all six panels returned NO_COUNTEREXAMPLE, using
165 nonempty three-bit and4169 nonempty four-bit sources. The exact optimum
of fee+2*gamma*error equals the no-purchase value in each panel. Correlated
substates DO benefit from further purchase, so the lack of a root improvement
does not validate a naive local Bayes-risk argument. No cap was reached.
The general high-reset claim remains open; no larger enumeration is selected.
