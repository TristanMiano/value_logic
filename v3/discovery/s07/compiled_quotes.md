# Compiling the existing logical quotation

Contributor: **ChatGPT (GPT-6 Astra Pro)**. October 12, 2026 UTC.
DEVELOPMENT. Concurrent helper work earns no additional principal-clock time.

## Constructive change

[compiled_quotes.py](compiled_quotes.py) retains the exact mathematical
quotation and output fields of [lattice_quotes.py](lattice_quotes.py), while
sharing arithmetic that the original interface repeats for every query
objective. It addresses the actual planner's repeated mode-action compilation,
source enclosures, scalar-anchor before bounds, and gcd/cut-transfer work.
It neither strengthens the lower certificates nor changes the purchase menu.

```python
prepared = PreparedQuotes(modes, cohort_size, meter)
answer = prepared.closing_query(masks, possible, lowers, price, q, tolerance)
```

The optional `complete`, `known_query_upper` and `exact_interval` arguments
match the existing interface. `prepared.stats` records cache hits and
compilations. `prepared.storage()` returns the charged numerical-word storage
and entry counts, and charges nine summary units itself. Physical allocator
bytes and CPU/storage prices remain separate.

The numerical caches hold:

| Key | Reused work |
|---|---|
| Checked action mask | Its cost at every public mode |
| Integer query vector | Gcd; full-cohort anchor transfer losses when needed |
| Multiset of surviving row mode sets | Row grouping and coordinate upper enclosure |
| Mask and surviving source | Fixed-action cost upper bound |
| Masks, source, supplied lowers and replacement price | Best scalar-anchor action bound and common lower |

Input checks, canonicalization comparisons/moves, cache keys and lookups,
stored words, arithmetic, and output fields receive explicit named operation
tariffs. A cache hit is paid. Cold construction and unsuccessful quotation
arithmetic remain in the invoices.

## Exact equivalence and source scope

For mask `u`, let `a_(u,k)=u·m_k`. If `c_g` rows currently have the same
possible mode set `g`, their contribution can be grouped without changing
the existing scalar formulas:

```text
L = sum_g c_g min_(k in g) ell_k/N
B_replace = max(0, p-L)
B_u = max(0,
          sum_g c_g max_(k in g) (a_(u,k)-ell_k/N),
          sum_g c_g max_(k in g) a_(u,k)-p)
B = min(B_replace, min_u B_u).
```

The same grouping gives the coordinate enclosure. Objective gcds and anchor
losses depend only on the fixed modes/cohort and `q`. The compiled path then
uses exactly the original canonical-budget endpoint, SAT bound, updated
UNSAT anchors and negative-branch calculation. All arithmetic is exact,
including rational modes/lowers. A zero query and a possibly unresolved call
retain the original behavior. The optional bisection reconstructs the same
canonical closing interval.

Grouping does **not** exchange actual observation receipts or identify two
physical cost rows. It only exploits permutation invariance of these cohort
sums. The execution controller still names an actual row and admits the
returned observation against that row's source.

Likewise, reuse across logical requests transfers **arithmetic only**. The
caller must have independently admitted every supplied mask and lower on
the current logical source and ordered feature meanings. Equal numerical
inputs permit a cached calculation even if their proof provenance differs;
a cache hit never admits a witness or lower proof. The caller also carries
the actual source bindings and the complete-provider contract. In the
service integration these are the existing checked bank, source state,
`RepairEvaluator`, and complete-call wrapper. The preparation object fixes
its modes/cohort and rejects changed dimensions, empty source rows,
negative costs/lowers and nonintegral query vectors.

## Saved finite probe and amortization

Command: `python v3/discovery/s07/compiled_quotes_check.py`.
The [saved result](compiled_quotes_results.json) contains the constructed
sources, case definitions, exact code hashes, invoices, cache statistics and
individual/cumulative measurements. It preserves **170** varied exact output
matches, **5** explicit closing/interval/unresolved cases, **80** amortization
calls, and **8** rejected invalid inputs. The varied cases include rational
costs/lowers, zero objectives, repeated masks, permuted mode/source rows,
replacement-only actions and updated lower vectors.

The mathematical probe source is the explicit relation `z1 OR z2` with
nonnegative remaining objective features. Its two singleton covering masks
give `C*(v)=min(v1,v2)`, so every supplied lower is independently warranted
by this elementary source. The separately identified trivial example has
one zero-cost action. No historical full workload was rerun, and there were
no LP, SAT, IHS, proof-search or audit calls.

| Constructed regime | Calls | Existing quotation units | Prepared units, including setup | Change | First cumulative saving |
|---|---:|---:|---:|---:|---:|
| Trivial already-closed source | 16 | 512 | 751 | **+46.7%** | None |
| Repeated two-feature menu | 24 | 7,792 | 2,700 | **−65.3%** | Call 3 |
| Changing objectives and lowers | 16 | 9,615 | 4,297 | **−55.3%** | Call 4 |
| Repeated six-feature menu | 24 | 22,356 | 4,224 | **−81.1%** | Call 2 |

All four regimes are worse on their first call. The trivial source remains
worse through every saved prefix because the repeated admission/key work
exceeds its inexpensive direct arithmetic. The other three regimes amortize
their paid construction after two to four calls. These are scoped savings
under the displayed implementations' named tariffs, not a CPU or complete
economic comparison. They establish a plausible way to reduce the observed
quotation overhead; the actual controller trace must establish its own
result with its complete planning initialization and resource invoice.

The earlier two-feature interactive screen also matched all 1,296 tested
outputs. Its initial import-only harness attempt omitted the s05 module path
and executed no quotation; this setup correction and the screen summary are
retained in the saved result. The immutable deliverable is the saved varied
probe above.
