# A full-dimensional, noisy scalar-quote contradiction

Codex (GPT-6), October26,2026. DEVELOPMENT; constructed application geometry.
This checks whether the gap consequence survives positive costs, nonzero
observation errors and full-dimensional source regions. It is not deployment
data or an empirical performance claim.

Let a,b>0 be known baselines, delta>=0, and define two independently uncertain
configuration vectors by

    x_1=(a+2t+u, b+1-t+v), 0<=t<=1, 0<=u,v<=delta;
    x_2=(a+s+u, b+2-2s+v), 0<=s<=1, 0<=u,v<=delta.

The two occurrences of u,v are independent local variables. For delta>0 the
projected regions in response space are compact full-dimensional polygons.
Retained coordinate-minimum quotes lie in[a,a+epsilon] and[b,b+epsilon].
The new quote is the minimum total response min_i(x_i1+x_i2).

For 0<=epsilon<2/3 no single generator can witness both old upper bounds:
even before nonnegative thickening, min_t max(2t,1-t)=2/3 and
min_s max(s,2-2s)=2/3. Thus there are exactly two attainer assignments.
Subtract a+b from the new quote. For the first assignment, generator1
witnesses the first coordinate and generator2 the second. Both local
sum ranges are

    I_low=[1, 1+delta+(epsilon+min(epsilon,delta))/2].

For example, the first generator obeys2t+u<=epsilon. Maximizing its sum
1+t+u+v sets v=delta and maximizes t+min(delta,epsilon-2t).
The maximum is(epsilon+min(epsilon,delta))/2. The other generator is the
same calculation after replacing s by1-s. Local minima are1. Independence
and continuity make the range of their minimum exactly I_low.

For the reverse assignment, generator1 obeys1-t+v<=epsilon. Write r=1-t;
its sum is2-r+u+v, with0<=r<=epsilon, u<=delta and
v<=min(delta,epsilon-r). Its minimum is2-epsilon and its maximum is
2+delta+min(epsilon,delta). The second generator is symmetric. Hence

    I_high=[2-epsilon, 2+delta+min(epsilon,delta)].

The complete new-quote set is a+b+(I_low union I_high). A gap remains if

    delta+(3*epsilon+min(epsilon,delta))/2 < 1.

For a=b=10 and epsilon=delta=1/10, the exact prediction is

    [21,106/5] union [219/10,111/5]
      = [21,21.2] union [21.9,22.2].

A reported21.5, or any report interval wholly inside(21.2,21.9), contradicts
the shared-source model while satisfying the sharp interval hull[21,22.2].
This conclusion is conditional on the quoted bounds and invariant response
regions. It diagnoses joint inconsistency, not which premise or service is
wrong. An ordinary exact feasibility solver detects the same contradiction.
For one new quote that direct feasibility query is a strong control; storing
the whole union is justified only by repeated or genuinely nonmonotone duties.
