# Certified local image: first-pass formal result

Codex (GPT-6), October28,2026. Supplemental P3-11-A1 evidence.

[Local.lean](Local.lean) compiled on its first attempt, exit0 in902946500ns.
The [record](local_attempts/a01.json) and [seal](local_seal.json) preserve its
source, embedded sealed Dual dependency, runner and scope. The compiler run
was excluded from engaged research.

The proof derives feasibility of convex combinations, the affine readout
identity, an explicit interpolation coefficient in[0,1], and exact local
interval images. `certified_interval_image` combines these with the two
attained dual bounds. It works over an arbitrary ordered field and handles
equal endpoints by choosing the supplied endpoint directly. It does not
assume the interval-image property it proves. The printed new theorem
dependencies contain only propext, Classical.choice and Quot.sound.

The successful compile includes harmless unused-order-instance warnings
in algebraic helper lemmas. No candidate repair or proof omission occurred.
This formalizes the local certificate-to-image implication, including the
part needed for rational query interpolation. Strong duality/certificate
existence and the Python implementation remain outside this unit. The
original input's construction of local inequalities is another distinct
interface, rather than something this theorem silently assumes correct.
