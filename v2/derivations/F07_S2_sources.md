# F07 S2 — source orientation and transfer boundary

Checked September 28, 2026 UTC (September 27 America/Los_Angeles).
This is a narrow soundness/producer audit, not a new literature survey. The
existing F03, Gate A and F06 source records remain the detailed background.

## Proof production versus a checking core

John Harrison's official HOL Light overview at
https://www.cl.cam.ac.uk/~jrh13/hol-light/ describes a small logical core with
programmable higher-level proof tools. The HTML introduction was read, not an
entire external implementation or proof of its kernel. Its historical page
revision is not treated as a current release guarantee.

Relationship: it is an established architectural precedent for separating
proof construction from trusted checking. It does not prove this project's
Python checker correct, establish a producer's requested postcondition, or
supply empirical source validity. The new proofs reconstruct those boundaries
for the finite existing code. No theorem is imported from HOL Light.

## Reports that change evaluated behavior

Perdomo, Zrnic, Mendler-Dünner and Hardt, *Performative Prediction*, ICML 2020,
PMLR 119:7599–7609, official abstract:
https://proceedings.mlr.press/v119/perdomo20a.html

The abstract describes predictions that influence their target and separates
a performative-stability objective from ordinary evaluation on past outcomes.
Only the official abstract/interface was rechecked here. The controller audit
uses direct finite probability calculations; no source convergence, calibration
or optimization theorem is imported. In particular, a proof of present paired
improvement is not a proof of historical performance improvement after a source
change. The report itself must retain its probability interpretation.

## What was not claimed

Pre-derivation source orientation and late HTML verification were mixed with
setup/administration and receive no separately measured L credit. No new PDF
figure was analyzed, no source PDF was redistributed, and no unavailable source
or whole-paper proof was represented as checked. Finite counting, monotone-DAG
error propagation and linear source-certificate arguments are baselines, not
new-priority claims. The interesting project question remains their precise
integration with loss-valued, revisable, explicitly scoped reasoning.
