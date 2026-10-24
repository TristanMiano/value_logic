# Build a rounded block warrant from scalar value receipts

Codex (GPT-6), October24,2026 UTC. DEVELOPMENT; pass63.
This is a concrete acquisition adapter for block_check.py, using ordinary
polarization and a row-sum operator bound. No new matrix norm inequality.

Let W have k orthonormal columns and C=W^T S W. Acquire truthful intervals
for q(e_i)=C_ii and q(e_i+e_j), i<j, where q(z)=z^T C z. There are
k*(k+1)/2 scalar queries. Let their midpoints be m_i,m_ij and their
half-widths be epsilon_i,epsilon_ij. Set

    C_hat_ii=m_i,
    C_hat_ij=(m_ij-m_i-m_j)/2,
    b_ii=epsilon_i,
    b_ij=(epsilon_ij+epsilon_i+epsilon_j)/2,
    delta=max_i sum_j b_ij.

Every entry of C-C_hat is bounded in magnitude by b_ij. Symmetry and the
induced row/column norm bound imply ||C-C_hat||_op<=delta, and therefore

    C_hat-delta*I <= C <= C_hat+delta*I.

The interval values and delta are rational when the original endpoints
are rational. This supplies the matrix-order warrant required by the
checker, conditional on the scalar receipts' source identity and truth.
It does not verify those external facts by arithmetic alone. The k
diagonal and k*(k-1)/2 pair queries, their precision and W must be paid.

For uniform scalar half-width epsilon, delta=(3*k-1)*epsilon/2. In the
two-target worked block this is2.5*epsilon. To obtain an operator bracket
with half-width10^-5, scalar half-width4*10^-6 is sufficient under this
conservative conversion. Correlated or joint error information can improve
the bound, but is additional information and cannot be silently assumed.

block_check.py's present bounded interface requires0<C_minus<=C_plus<I.
If this constructed bracket violates that domain, obtain tighter values,
use another explicitly verified domain treatment, or report unresolved.
Eigenvalue clipping does not generally preserve a matrix-order bracket.
With fixed valid t, the error penalties in operator_receipt.md then give
an explicit precision budget for a strict decision margin. This closes a
small implementation gap between paid scalar acquisition and a usable
rounded counterfactual certificate; it does not establish favorable total
query economics or novelty of polarization/Gershgorin bounds.
