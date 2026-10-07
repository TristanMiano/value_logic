# P3-03 — Finite halting certificates and revisable convergence

Contributor: **ChatGPT (GPT-6 Astra Pro)**, `/root/bounded_sources`.
Same-model internal source and proof review. Source inspection completed
**2026-10-07T15:49:04.719933+00:00**.

## 1. Primary source and exact import

A. M. Turing, [On Computable Numbers, with an Application to the
Entscheidungsproblem](https://www.cs.virginia.edu/~robins/Turing_Paper_1936.pdf),
1936 paper, printed pp. 230–265. **Section 8, printed pp. 246–248**, especially
the opening statement and argument on **p. 248**: no machine decides, from
an arbitrary machine's standard description, whether it ever prints a
specified symbol. The page reduces such a proposed decider to the preceding
circle-free contradiction.

The selected section was inspected; p. 248 was also checked visually in the
scan. It is PDF page index 18, counting from zero. Turing's circle-free
condition concerns infinitely many printed figures and is not the modern
halting predicate. We import his symbol-occurrence undecidability result;
the translations and certificate/estimate arguments below are elementary
reconstructions for the project's interface. No full universal-machine
implementation audit or new undecidability result is claimed.

## 2. Obstruction to universally complete sound certificates

Fix a standard effective universal program encoding with its input included
in the description. Write $H(P)=1$ if the program eventually halts and $0$
otherwise, in one fixed operational semantics.

First, a total halting decider would decide Turing's symbol-occurrence problem.
Given a described machine $M$, effectively construct $S_M$ that simulates it
and halts exactly when the simulated machine prints the designated symbol.
If $M$ itself stops without printing that symbol, $S_M$ continues idling
forever. Thus $S_M$ halts exactly when $M$ eventually prints that symbol.
A total halting decider applied to $S_M$ would contradict §8.

Now suppose a uniform computable process, on each $P$, can emit pending states,
fallible guesses and candidate finite certificates. Its acceptance procedure
is effective and binds each accepted sign to this exact program/input and
unbounded query. Assume both:

1. **Sound accepted signs:** every accepted positive certificate means
   $H(P)=1$, and every accepted negative certificate means $H(P)=0$.
2. **Universal finite completion:** for every $P$, some signed certificate is
   accepted after finitely many computation steps.

Run the process on $P$ until its first accepted signed certificate, then return
its bit. Acceptance is observable by effective computation, completion makes
this algorithm halt on every input, and soundness makes its answer $H(P)$.
This contradicts the preceding reduction. Hence the two properties cannot
both hold uniformly for all unbounded programs.

This argument permits arbitrary finite runtime depending on $P$; no claimed
uniform deadline is needed. It also permits any number of earlier unaccepted
or explicitly fallible outputs. Noncomputable external answers or a
theory-conditional proof lacking the soundness bridge do not satisfy its
premises. The statement does not prohibit sound negative certificates for
particular programs or complete decisions on a restricted decidable family.

## 3. A computable revisable estimate can still converge everywhere

For each finite $t$, simulate $P$ for $t$ transitions and define

$$
h_t(P)=
\begin{cases}
1,&\text{if }P\text{ halts within }t\text{ transitions},\\
0,&\text{otherwise}.
\end{cases}
$$

This is a finite computation, with its simulation cost included. For a fixed
program that halts after $T$ transitions, $h_t(P)=1$ for every $t\ge T$.
For a fixed nonhalting program, $h_t(P)=0$ for every $t$. Therefore

$$
\text{for every fixed }P,\qquad \lim_{t\to\infty}h_t(P)=H(P).
$$

The estimate $0$ means only that halting has not yet been observed. It is
not a sound finite certificate of unbounded nonhalting: a later halting
program can have exactly that estimate at the current budget. The positive
estimate has a finite execution witness. A finite negative result about
**halting within the stated horizon** is also sound, but answers a different
query from eventual nonhalting.

Thus pointwise convergence, even eventual exactness for each fixed input,
does not provide an effective signal that a provisional zero has become
permanently correct. If a computable bound $m(P)$ guaranteed correctness for
all $t\ge m(P)$ on every input, evaluating $h_{m(P)}(P)$ would decide halting.

## 4. Growing queries and P3-03 scope

Let $P_n$ perform $n$ dummy increment instructions and then execute a halt
instruction, with each instruction consuming one transition. Then $P_n$
halts after $n+1$ transitions, but

$$
h_n(P_n)=0,\qquad H(P_n)=1
$$

for every $n$. Every fixed program's estimate converges; the estimate at the
initial budget of each new query is always wrong. This is a counterexample
for the stated simulation estimator. A same-access solver that recognizes
the simple program structure may answer earlier, with that analysis charged.
It is not a lower bound against all bounded reasoning methods.

P3-03's executable claims concern specified finite horizons and explicit
resource limits. They can be decided by completing the finite computation.
The obstruction concerns an attempted extension to uniformly complete,
always-sound finite certificates for **unbounded** halting. The revisable
estimate establishes neither calibration, anticipatory learning nor useful
decisions at each new budget. All three arguments are classical elementary
reconstructions; **P3-N01 remains NOT YET SUPPORTED**.

This review changes no previous source record or principal artifact. No
scientific execution, clock entry or additional concurrent time credit was
produced.
