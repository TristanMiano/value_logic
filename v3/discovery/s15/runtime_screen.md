# A runtime distribution is another fallible model, not a free label

Codex (GPT-6), October 23, 2026. DEVELOPMENT; pass 26, early screen.

Consider a deterministic proof strategy with latent completion time T on a
random task. A run observed for t units supplies T>t if unfinished, or the
exact T if completed. An unfinished run supplies neither eventual failure
nor a runtime upper bound. For a fixed timeout b, the capped cost
C_b=min(T,b) and success Y_b=1[T<=b] are bounded variables. The open-policy
and partial-receipt interfaces can therefore estimate their priced
combination without assuming an eventual truth label.

For reward one per certificate and price c per unit computation,

    V(b)=P(T<=b)-c*integral_0^b P(T>t) dt.

The exact value of extending b to b+h is

    P(b<T<=b+h)-c*integral_b^(b+h) P(T>t) dt.

Thus a high completion probability alone does not establish a valuable
extension: the additional occupied computation matters. Conversely, the
fact that an unfinished search has not yet returned a proof is legitimate
runtime information even though it is not a mathematical truth label.
For a differentiable survival curve S, V'(b)=-S'(b)-c*S(b); the familiar
hazard-versus-price criterion follows. No new optimal scheduling theorem
is claimed from this identity.

There is no finite distribution-free upper confidence bound for unbounded
E[T] based only on finitely many capped observations: append arbitrarily
large mass-times-runtime in an unobserved tail while preserving the
observed prefix law to arbitrary accuracy. A tail premise, explicit cap,
or a different objective is necessary. This is an information obstruction,
not evidence that one model learned a long-run runtime distribution.

Screen outcome: generic censored-runtime scheduling is already an
established algorithm-configuration/portfolio duty. Keep the distinction
between runtime evidence and truth evidence, but do not build another
small harness without an actual task family where the partial-proof
interface changes acquisition cost against strong censored-runtime controls.
This is a rejected generic novelty proposal, not a new family or gain.
