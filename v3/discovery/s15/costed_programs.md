# Partial proofs can support a least-cost program mixture

Codex (GPT-6), October 23, 2026. DEVELOPMENT; pass 30.
This is a finite operational specialization of established PAC-Bayes and
convex duality, not a new universal induction theorem.

## A total policy universe with an explicit computation bill

Fix a bounded interpreter and a safe fallback action. A description h=(p,b)
runs finite binary program p for at most b charged machine steps, including
its required validation, and otherwise falls back. Malformed programs also
fall back. A separately specified constant fallback cost is included in the
policy's known per-case upper cost c_h. Learned parameters are part of the
description; sample-dependent global state is not silently free.

This yields a countable universe of total policies without deciding arbitrary
program termination. One explicit rational prior, for all strings p and
integers b>=0, is

    pi_(p,b)=2^(-2*len(p)-1)/((b+1)*(b+2)).

The two sums each equal one. The universal universe and prior precede the
iid case stream, although a bounded reasoner may discover descriptions much
later and retain only a finite list A. No complete enumeration is required.
Let Y_hi in [0,1] be each policy's task loss, and let sound partial receipts
U_hi>=Y_hi initially equal one. Use the common anytime event already derived
in anytime_programs.md, with fixed eta>0, a=1-exp(-eta), confidence delta.

## A convex risk-budget problem

For a selected sample prefix of size N, let s_h=sum_(i<=N) U_hi and define

    J(q)=KL(q||pi)+eta*sum_h q_h*s_h,
    K=-N*log(1-a*epsilon)-log(1/delta).

The same common event certifies expected future Gibbs-policy loss at most
epsilon whenever J(q)<=K. Here a fresh program is drawn from q on each
future iid case. Minimize the paid upper cost C(q)=sum q_h*c_h over finite
posteriors supported on A subject to this constraint. This is convex.
Do not renormalize pi over A: the missing prior mass is part of the bill.

The least-J posterior is q_0 proportional to pi_h*exp(-eta*s_h).
If J(q_0)>K, the current receipts do not certify any mixture on A. Otherwise,
the cost frontier has the family

    q_beta(h)=pi_h*exp(-eta*s_h-beta*c_h)/Z_beta, beta>=0.

For this family,

    C'(beta)=-Var_(q_beta)(c),
    J(q_beta)=-log Z_beta-beta*C(q_beta),
    dJ(q_beta)/dbeta=beta*Var_(q_beta)(c)>=0.

Thus one scalar search increases cost pressure until the risk constraint
binds. If a cheapest-policy-supported posterior is already feasible, use
that face; among its ties the same restricted Gibbs formula minimizes J.
The Lagrange multiplier proof is standard: minimizing C+lambda*J gives
beta=1/lambda, and convexity supplies global optimality on the finite list.

The exponential Catoni bound plus an additive cost objective should NOT
be casually minimized by this Gibbs formula: that different nonlinear
objective is not the convex risk-budget problem above. The distinction is
part of the specification, not an implementation detail.

## Proof acquisition and honest guarantees

Any truthful refinement lowering some U_hi can only expand the feasible
set, so the minimum certified cost cannot increase. Adding a new program
with its original prior weight likewise preserves all old choices. These
claims are pointwise on the common confidence event and allow adaptive
refinement, program enumeration, prefix choice and posterior selection.
The runtime cost upper bounds and prior descriptions must themselves be
truthful; neither is inferred from a good empirical loss.

Where the constraint is active and differentiability holds, the envelope
derivative of minimum cost with respect to s_h is lambda*eta*q_h. This can
guide a fallible acquisition model toward potentially useful loss proofs.
It is not a guarantee that a requested proof will succeed or repay its
price, and complementary proofs can defeat singleton-greedy stopping.

The certified quantity is average future loss under the stated iid law.
It is not a guarantee of each answer, a persistent one-time draw of a
program, or an arbitrary changed environment. Known c_h are worst-case
per-case computation bounds; the service has not learned uncapped mean
runtime by treating unfinished runs as failures. Interpreter, forecasting,
proof checking, scalar search and program storage must be charged when
comparing complete costs.

This interface directly connects unresolved mathematical outputs, fallible
program proposals and reasoning prices. Its ingredients are conventional;
usefulness and a moderately novel operational delta need a concrete task
and comparison with ordinary constrained PAC-Bayes/program-selection methods.

## A finite proof-investment illustration

For a separately fixed TWO-policy universe with prior (1/2,1/2), let their
declared exact per-case costs be (100,1). Take N=1000, eta=1, delta=.05,
epsilon=.06. Suppose their current summed loss upper receipts are (10,40).
A posterior putting probability .153184 on the expensive program has
mean cost 16.165216 and computed loss bound below .06. The cheap program
alone has bound about .06763, so the current receipts do not certify it.

Five additional zero-loss receipts for the cheap program reduce its sum
from 40 to 35. The expensive probability can then fall to .000713 and
mean cost to 1.070587. Ten such receipts, reducing the sum to 30, permit
the cheap program alone, with bound about .05241. This describes changes
to certified cost GIVEN the old paid evidence and the stated new proofs;
it does not supply those proofs, establish their price, or measure actual
workload savings. The two-policy prior is distinct from the universal
program prior above and cannot be retrofitted after seeing the cases.

`program_probe.py` checked 16 such cost/risk states and the monotone Gibbs
frontier with 90-digit decimal arithmetic. The millionth-rounded posterior
probabilities have numerical slack, but this is not a formal outward-rounded
interval certificate. Source SHA-256:
`283a5b3b2090db40f73659f2c8505a73e394dc49620cbd8fe8a3778a1a38d02b`.
Measured probe runtime: 556,473,100 ns. Ordinary constrained selection on
the identical receipts yields the same result.
