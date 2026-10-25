# Prospective rational attainer-DP screen

Codex (GPT-6), s18 DEVELOPMENT. Before execution, implement the face table
and subset recurrence for rational line-segment regions, where every face
optimization is exact one-dimensional interval arithmetic. Generate at most
200 reproducible small cases with n<=5, dimension<=4, k<=4, including values
from rational interior witnesses and deliberately perturbed values.

Compare sharp endpoints and consistency with independent complete enumeration
of each clipped segment's endpoints and old-value equality intersections.
These candidates suffice for the linear endpoint questions: each attainer
branch has independent intervals whose linear extrema occur at their ends.
Return source witnesses for both DP endpoints and check their old values,
segment membership and new values directly.

Include the one-dimensional surrogate-conditioning counterexample and the
SAT-to-segments adapter on a small fixed formula panel. Report exact work
counts and source hash; do not turn a finite comparison or fewer abstract
states into a measured full computation/audit saving. One frozen source/run,
preserving any failure, is enough for this early screen.

The frozen[attainer_check.py](attainer_check.py) passed once;
[attainer_result.json](attainer_result.json), Python3.12.14,253,242,400ns,
SHA25677b814838716372a4d0f4664113adc10e1f042d1de09240d4d82af98515e0f21.
All201 segment cases agree with complete candidate-point enumeration:
181 consistent and20 inconsistent. The24 SAT-adapter instances include
19 satisfiable and five unsatisfiable cases. The implementation made5,040
face-region calculations,12,520 constraint tests and11,867 DP transition
attempts; enumeration visited2,438 configurations,1,600 consistent. These
counts are not comparable unit operations and establish no speedup.
All400 returned endpoint source witnesses passed direct receipt, segment
and new-value checks. The conditioning example has exact new range[-2,0],
including the collapsed source omitted by naive surrogate conditioning.
