# Development plan: checked prediction queries and source recovery

Codex (GPT-6), October 28, 2026. Saved before executing the new interface.
This is DEVELOPMENT using the exposed s20 audit panel, not held-out evidence.
The unchanged s19 certificate verifier remains the trust boundary for local
extrema; the new module must not call an optimization solver during queries.

Implement an exact snapshot compiled from an original problem and a complete
certificate. Reverify the certificate, retain prefix/suffix split witnesses,
and index anchored intervals for logarithmic scalar membership. Reconstruct
an attainable rational source by walking those splits and interpolating only
the anchor. Add exact band intersection and nearest-gap endpoints. Charge
compilation, retained certificate bytes, exact arithmetic and full source
output separately; no economic speedup or deployment claim is planned.

Development checks: all 13 exposed audit records; every output endpoint and
midpoint; two additional rational interior points per nondegenerate interval;
all adjacent gap midpoints and exterior points; degenerate intervals; an
inconsistent source; a wrong certificate; mutation of caller-owned inputs
after compilation. Verify every recovered point directly against the original
problem, without invoking the service's internal verifier. Compare band
answers with a direct scan of the independently retained audit ranges.

Do not rerun the old audit or change its frozen inputs/results. Freeze the
new module and driver before this first execution, save a failure if one
occurs, and distinguish deterministic repairs from the permitted unchanged
host-failure retry. Stronger two-block fixtures belong to a separate probe.
