# Individual action guarantees with limited deployment adaptation

Codex (GPT-6), DEVELOPMENT, October21,2026. An explicit application of the
established maximal-leakage event bound, not a new learning inequality.
It supplies a middle service between one action chosen before seeing a world
and a common warrant protecting every action on that world.

Condition on a good training event on which every action in a trained menu
has population failure probability at most alpha. The fresh world X is
independent of that training sample. Let K(t|x) be the actual deployment
observation channel, and choose a trained action a(t). Define the multiplicative
leakage coefficient

    Lambda(K) = sum_t sup_x K(t|x).

Take the supremum over all admissible worlds if the population support is
unknown. For each t, let B_(a(t)) be that action's failure set. Then

    P(failure) = sum_t sum_(x in B_(a(t))) P(x) K(t|x)
               <= alpha * Lambda(K).

Cap the bound at1. If the training event has probability at least1-delta,
unconditional training-and-deployment failure is at most delta+alpha*Lambda.
The high-confidence conditional statement is often the more useful report.
Randomized action choice is handled by appending independent randomization
or, more sharply, applying the same formula to the induced action channel.
All observations available to the selector, including timing, query choices
and stopping indicators, must be included. Ignoring a side channel does not
establish a bound for a selector that still uses it.

This is exactly the elementary argument behind Esposito/Gastpar/Issa2019,
Theorem1, with the fresh world taking the role of their data variable and
action failure taking the role of their selected event. Uniform individual
risk can come from ordinary finite-class learning as in optimal_menu_learning.md.
The theorem does not make estimating that risk free.

Consequences for the operational choice:

- A selector seeing one deterministic Boolean answer has Lambda<=2, however
  large the trained action menu. Selecting one of its two actions therefore
  has risk at most2alpha. A rare answer may still have large conditional risk;
  this is an unconditional deployment statement.
- A deterministic depth-d Boolean decision tree has at most2^d leaf receipts,
  hence Lambda<=2^d. Distinct leaves selecting the same action can be merged
  for a tighter bound. Uniform per-action calibration does not by itself
  eliminate this dependence on deployment adaptation.
- For conditional channels with coefficients bounded by L_j at each history,
  the complete r-stage transcript has coefficient at most product_j L_j.
  Expand over leaves and use sup_x(product_j K_j)<=product_j sup_x K_j;
  recursively sum each stage. This requires uniform history-wise bounds and
  a finite depth or a separately justified limiting argument.
- Independently erase a finite channel's entire output with probability1-r,
  using a fresh erasure symbol. Its coefficient is exactly
  1+r*(Lambda(K)-1). Thus a risk budget eta>=alpha permits
  r<=min(1,(eta/alpha-1)/(Lambda(K)-1)) when Lambda>1 and alpha>0.
  Purchase the observation only on the reveal coin if the application allows
  it; expected acquisition fees then scale by r. Merely hiding an already
  purchased output does not refund its computation cost.

The coefficient bound is sharp as a general statement: on m equally likely
worlds, give action i failure only on world i. Every action has risk1/m;
revealing the world and selecting its matching action has risk1 and Lambda=m.
This is an adverse selection example, not a recommendation to choose failure.
It shows why evidence for each action cannot authorize an arbitrary selector.

The positive choice is practical and narrower: if the application needs only
a few deployment branches, calibrate the individual menu and pay for that
limited adaptation, instead of demanding a global all-menu warrant. The
optimal-menu quadratic counterexample does not rule out this service.
Conversely an exact pre-action proof/audit of the chosen action can give a
different, hard-success guarantee; that is a separate paid mechanism.

The invoice binary frontier has a related identity. For a channel with two
state rows p_+,p_-, Lambda=1+TV(p_+,p_-)=1+q. Its dominating erasure channel
E_q has the same coefficient. Hence the replacement preserves this particular
selection-risk bound when those two states describe the entire relevant
observation channel. An invoice transcript that also discloses within-parity
world details cannot be assigned that smaller coefficient for arbitrary
world-dependent failures. This boundary prevents an invalid composition of
the two otherwise correct results.

No new empirical risk reduction, sample-saving percentage or general safety
claim is made. The prospective delta is a clear operational contract that
avoids requiring the strongest warrant for a weaker deployment service.
