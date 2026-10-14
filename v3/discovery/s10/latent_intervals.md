# One latent cost can suffice without observing the contrast

**Codex (GPT-6), October 14, 2026. DEVELOPMENT derivation.**

The earlier service assumes a query directly reveals d_i=T_i-F_i. A different
physical interface charges separately for observing T_i or F_i, each initially
in [0,4]. All ordinary methods must receive that same interface. Repair regret
cancels sum F_i; replacement does not, so the following remains repair-only.

Observing T_i=t leaves d_i in [t-4,t]. Observing F_i=t leaves d_i in [-t,4-t].
Thus neither query generally determines the contrast. For counts a and competitor
v, write d=a_i-3v_i and R_other=4 sum_{j!=i}|a_j-3v_j|. Their post-query pairwise
regret is respectively

```math
R_{T_i=t}(a,v)=R_{other}+d\,t+4\max(-d,0),
```

```math
R_{F_i=t}(a,v)=R_{other}-d\,t+4\max(d,0).
```

Both are affine in t on [0,4]. Intersect their competitor inequalities for a
fixed action to obtain its completion interval. A union of action intervals
covering [0,4] proves one latent query suffices on every continuous answer while
the paired cost remains unknown. The same sixth-grid argument now has 24 cells.
Every output still needs a source-feasible realizing triple and original-source
regret certificate. An incomplete action menu can find a cover, but cannot
prove one impossible. An incomplete competitor list cannot certify a cover.

More generally, for an affine interval query l_i(t)=l0+alpha*t,
u_i(t)=u0+beta*t, pairwise regret is R_other+d*u_i(t) when d>=0 and
R_other+d*l_i(t) when d<0. Integer slopes and intercepts support the analogous
finite endpoint grid. The provider must actually guarantee the interval map;
a fictitious interval contraction is not information. With both latent costs
observed, the interval reduces to their exact difference.

This changes the information menu and tariffs, so savings must be measured in
its own service. Do not combine its fees with direct-contrast fees or present
the change of interface as an improvement on an unchanged experiment. It is
related to the existing S29/S30 quotient/partial-latent ideas, with a new explicit
source-dependent contingent-action certificate rather than a new statistical law.
