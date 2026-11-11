#!/usr/bin/env python3
"""Build the W1 cycle summary PDF (v4/reports/W1_cycle_summary.pdf).

Prepared by Claude (Fable 5.2), 2026-11-11, at the author's request. Needs
reportlab and the DejaVu fonts at the Linux path below.
Usage: python build_w1_summary.py OUTPUT.pdf
"""
import sys
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle)

D = "/usr/share/fonts/truetype/dejavu/"
for name, f in [("Serif", "DejaVuSerif.ttf"), ("Serif-B", "DejaVuSerif-Bold.ttf"), ("Serif-I", "DejaVuSerif-Italic.ttf"),
                ("Serif-BI", "DejaVuSerif-BoldItalic.ttf"), ("Sans", "DejaVuSans.ttf"), ("Sans-B", "DejaVuSans-Bold.ttf")]:
    pdfmetrics.registerFont(TTFont(name, D + f))
pdfmetrics.registerFontFamily("Serif", normal="Serif", bold="Serif-B", italic="Serif-I", boldItalic="Serif-BI")
pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="Sans-B", italic="Sans", boldItalic="Sans-B")

INK, ACCENT, RULE, SHADE = colors.HexColor("#1b1f24"), colors.HexColor("#1f4e79"), colors.HexColor("#b8c2cc"), colors.HexColor("#eef2f6")
body = ParagraphStyle("body", fontName="Serif", fontSize=9.6, leading=13.6, textColor=INK, spaceAfter=6, alignment=TA_LEFT)
small = ParagraphStyle("small", parent=body, fontSize=8.4, leading=11.4, spaceAfter=3)
cell = ParagraphStyle("cell", parent=body, fontSize=8.6, leading=11.6, spaceAfter=0)
cellb = ParagraphStyle("cellb", parent=cell, fontName="Sans-B", fontSize=8.2, textColor=colors.white)
h1 = ParagraphStyle("h1", fontName="Sans-B", fontSize=14, leading=18, textColor=ACCENT, spaceBefore=14, spaceAfter=6)
h2 = ParagraphStyle("h2", fontName="Sans-B", fontSize=10.8, leading=14, textColor=INK, spaceBefore=10, spaceAfter=4)
title = ParagraphStyle("title", fontName="Sans-B", fontSize=22, leading=27, textColor=ACCENT, spaceAfter=6)
sub = ParagraphStyle("sub", fontName="Sans", fontSize=11, leading=15, textColor=INK, spaceAfter=10)
bul = ParagraphStyle("bul", parent=body, leftIndent=14, bulletIndent=3, spaceAfter=3)
box = ParagraphStyle("box", parent=body, fontSize=9.2, leading=13, spaceAfter=0)
thm = ParagraphStyle("thm", parent=body, leftIndent=10, rightIndent=6, spaceAfter=6)

S = []
P = lambda t, st=body: S.append(Paragraph(t, st))
H1 = lambda t: S.append(Paragraph(t, h1))
H2 = lambda t: S.append(Paragraph(t, h2))
def B(items):
    for t in items:
        S.append(Paragraph(t, bul, bulletText="•"))
    S.append(Spacer(1, 3))
def T(rows, widths, header=True):
    data = [[Paragraph(c, cellb if (header and i == 0) else cell) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=[w * inch for w in widths], repeatRows=1 if header else 0)
    st = [("VALIGN", (0, 0), (-1, -1), "TOP"), ("LINEBELOW", (0, 0), (-1, -1), .4, RULE),
          ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
          ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]
    if header:
        st.append(("BACKGROUND", (0, 0), (-1, 0), ACCENT))
    t.setStyle(TableStyle(st))
    S.append(t); S.append(Spacer(1, 8))
def BOX(text):
    t = Table([[Paragraph(text, box)]], colWidths=[6.5 * inch])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), SHADE), ("BOX", (0, 0), (-1, -1), .5, RULE),
                           ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                           ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    S.append(t); S.append(Spacer(1, 8))

# ------------------------------------------------------------------ title
P("Judging the Judges", title)
P("What recursive judgment recovers about the world: a summary of the first phase-four research cycle of the "
  "Value Logic project", sub)
P("Prepared for Tristan Miano by <b>Claude (Fable 5.2)</b>, November 11, 2026. The results summarised here were "
  "produced by Claude (Fable 5.2) (results R1.1 to R1.7) and by Codex (GPT-6) (a review of those results, and "
  "results R1.8 to R1.15) between November 9 and 11, 2026.", small)
BOX("<b>Status of everything in this document.</b> All results are model-generated. None has been reviewed by an "
    "independent expert. One model (Codex) re-derived the three central theorems written by the other (Claude); "
    "the remaining results were each written and checked by a single model. Much of the mathematics is classical "
    "and is used here to make the project's founding ideas precise. Statements are given at the scope their source "
    "files claim, and section 6 lists what is not established.")

H1("1. The question")
P("The Value Logic project starts from the author's claim that, for an agent with limited knowledge, <i>value comes "
  "before truth</i>: an agent can tell that one thing works better than another long before it can say that "
  "anything is finally true. The strongest form of the claim is that value applied to itself produces fact. This "
  "cycle tested that claim in its most concrete form, which concerns judgment.")
P("Three terms from the author's essays are used throughout.")
B(["<b>Judgment (written J).</b> A rating of something that was done or seen. In the author's words (November 10, "
   "2026), a judgment is “something like a prediction that a certain task will be done again (or rather, that a "
   "positive rating means it will be seen again, negative that it will not).” A judgment is therefore a "
   "<i>forecast of reappearance</i>, and it can be right or wrong.",
   "<b>Task delineation (written T).</b> The way an agent divides what it observes into kinds of task or kinds of "
   "thing. This document also calls it a <i>conceptualisation</i>.",
   "<b>T = J².</b> The author's shorthand for the claim that delineating tasks and judging judgments are one "
   "operation. “J²” means judgment applied to judgment: evaluating how good a judge is."])
P("The project's charter lists seven theses, labelled C1 to C7. This cycle bears on four of them:")
T([["Label", "Thesis", "What would count as success (from the charter)"],
   ["C1", "Judging judges forces the recovery of factual distinctions.",
    "A theorem showing that recursive judgment recovers hidden task structure that first-order judgment cannot."],
   ["C2", "Task delineation and judging judgments are two faces of one operation (T = J²).",
    "A precise fixed-point statement in which the task partition and the weighting of judges determine each other."],
   ["C3", "Truth is the limit of value under successful use.",
    "A construction of truth as a limit, with consistency conditions."],
   ["C5", "Self-trust is possible but constrained; values can be assigned to values without chaos.",
    "A limit on self-endorsement, and convergence conditions for recursive value updates."]],
  [0.5, 2.6, 3.4])
P("The other three theses (C4, on local replacement of theories; C6, on neural networks; C7, on the duality of "
  "policy and value) were not addressed in this cycle. The work belongs to the plan's first module, called W1 "
  "(“recursive judgment and task recovery”). A <i>cycle</i> is one block of work on a module with at "
  "least 240 minutes of observed research time; this one is identified in the repository as P4-R1-C001.")

H1("2. The setting, in plain terms")
P("All results use variations of one simple picture.")
T([["Term", "Meaning"],
   ["Performer", "Whoever or whatever produces what is judged. A performer has persistent traits (for example skill) "
                 "that are not directly observed."],
   ["Persistent state", "The general version of a performer's traits: whatever stays the same across the things that "
                        "are seen, such as who is acting or what regime holds."],
   ["Task instance, task type", "A particular piece of work, and the kind of work it is. Types are hidden; the judge "
                                "must work out which instances belong together."],
   ["Result", "How a performance turned out, for example success or failure."],
   ["Delineation, conceptualisation, kinds", "A grouping of instances (or of anything observable) into cells. Finer "
                                              "means more cells. One grouping <i>refines</i> another if it only splits the other's cells."],
   ["Forecast and score", "A judge states probabilities for what will be seen next and is scored by how much "
                          "probability it gave to what happened (a “proper” score, which rewards honest forecasts)."],
   ["Twins", "Two task types that no performer's traits can tell apart: every performer has the same chances on both."],
   ["Transfer partition", "The grouping that merges exactly the twins. It records how skill transfers between tasks."],
   ["Difficulty partition", "The coarser grouping that merges types with the same average success rate."],
   ["Vindication", "A judgment is vindicated when later judgments of the same performer's new performances bear it out."],
   ["Convention", "A standard that judges share which is not a fact about performances, such as task-specific "
                  "leniency, fashion or reputation."]],
  [1.9, 4.6])

H1("3. Main findings")
H2("3.1 A judgment needs a concept of “it”, and the best concepts are fixed by the world")
P("To say that something “will be seen again” one must say what counts as the same thing. So a delineation "
  "is not a step that comes before judging; it is what gives a judgment its content. The first central result says "
  "which delineations good judging requires.")
BOX("<b>Theorem A</b> (R1.6, Theorem 13; Claude, re-derived by Codex). Suppose the things seen are independent "
    "draws given a persistent state. Measure a conceptualisation by how much the kind of thing seen now tells you "
    "about the kind seen next. Then (i) a finer conceptualisation never captures less; (ii) it captures strictly "
    "more until it separates every two things that are <i>differently diagnostic</i> of the state, meaning that "
    "seeing one or the other changes what should be expected next; (iii) beyond that point further splitting adds "
    "nothing. A single split is worth drawing exactly when its two sides recur differently.")
P("This is the author's statement that judging well requires recognising sub-types well enough to make ever more "
  "granular predictions. In a constructed four-level hierarchy of types and sub-types the gains from successive "
  "splits were 0.179, 0.0105 and 0.0002 nats (a unit of information), and exactly zero for a fourth level that the "
  "constructed world did not contain. In 200 random test worlds the best conceptualisations among all 203 possible "
  "ones were exactly those the theorem predicts.")

H2("3.2 What the reappearance of a performer adds")
BOX("<b>Theorem B</b> (R1.1, Theorem 1; Claude, re-derived by Codex). Score a judge on how well it forecasts a "
    "performer's next result from that performer's past results, labelled by the judge's delineation. Assume tasks "
    "are met independently of skill. If the performer has been seen at least once before, the delineations that "
    "allow the best score are exactly the refinements of the transfer partition. If the performer has never been "
    "seen before, they are the refinements of the difficulty partition only.")
P("So what judging the judge adds to judging the performance is exactly the facts about transfer: tasks that are "
  "equally hard but draw on different skills. One reappearance is enough. If performers are never seen twice, no "
  "method of any kind can recover more than difficulty (R1.1, Proposition 4).")
P("<b>Example.</b> Two task types and two equally common kinds of performer, each succeeding 90% of the time on "
  "one type and 10% on the other. Every success rate averages one half, as with coin flips. A judge who tells the "
  "types apart forecasts well; a judge who cannot stays exactly at chance however much history it sees, although "
  "it uses everything it distinguishes. This matches the essay's remark that a judge who cannot judge looks random.")
P("<b>Physics illustration.</b> Performers are four model builds that include or neglect a drag correction and a "
  "relativistic correction; tasks fall in three regimes. Which regimes count as one task depends on the tolerance "
  "of judgment:")
T([["Tolerance", "Recovered without reappearance", "Recovered with reappearance"],
   ["Loose", "one task", "one task"],
   ["Intermediate", "{slow vacuum, fast vacuum} and {drag}", "the same"],
   ["Strict", "{slow vacuum} and {drag, fast vacuum}", "three separate tasks"]], [1.3, 2.6, 2.6])

H2("3.3 Better judges must draw finer distinctions")
B(["<b>A price for confusing two kinds.</b> A judge whose score is within a given margin of the best possible "
   "cannot be merging two task types that are both common and sufficiently different. Explicit bounds exist for "
   "one past performance (R1.1, Theorem 2; Claude) and for any number, together with a bound in the general "
   "setting of Theorem A (R1.8; Codex, with exact-arithmetic checks that I re-ran successfully).",
   "<b>Resolution grows with experience.</b> For a judge who must learn from limited history, coarse concepts win "
   "at first and finer ones later. In the constructed hierarchy the best level was the first up to 8 observations, "
   "the second from 16 to 128 and the third from 256; the level the world lacks was never best (R1.6, simulation). "
   "For one kind of bounded judge the true transfer partition is the unique best delineation once history is long "
   "enough (R1.2, Theorem 6)."])

H2("3.4 Judging without an outside referee")
P("Theorem B assumes someone can see how performances turn out. The next results remove that assumption: the only "
  "data are judges' approvals.")
B(["<b>Approvals can be their own outcomes.</b> If approvals depend on a task only through how the performance "
   "turned out, and are better than chance, then predicting later approvals recovers the transfer partition. One "
   "such judge checked against its own later approvals suffices (R1.2, Theorem 4).",
   "<b>Agreement is not vindication.</b> Two judges who follow a shared fashion agree perfectly on each performance "
   "and earn no credit across performances, because a judgment is tested on a performance that did not exist when "
   "it was made (R1.2, Proposition 6)."])
BOX("<b>Theorem C</b> (R1.2, Theorem 5; Claude, re-derived by Codex). Consider two maps: “which judges are "
    "vindicated under this delineation” and “what the vindicated judges jointly tell apart”. Both are "
    "monotone, so the states in which they agree (the <i>fixed points</i>) form an ordered family with a largest "
    "member. The largest member contains exactly the judges whose approvals track some persistent trait of "
    "performers. Random judges, followers of fashion, and judges applying a pure convention about tasks belong to "
    "no fixed point.")
P("This is the cycle's most direct reading of T = J²: neither the delineation nor the crediting of judges "
  "comes first; the stable states are those in which each determines the other. Not all stable states are good "
  "ones. Three kinds of <i>self-confirming</i> state were constructed:")
T([["Self-confirming state", "Why it sustains itself", "What moves a society out of it"],
   ["Ignorance: nobody is credited and there is one task", "Without the right distinctions even accurate judges look random.",
    "A general factor of skill, or any proposed distinction that weakly matches the truth."],
   ["Partial grounding: right about one domain, blind to another", "The blind domain's judges are never vindicated under the current concepts.",
    "A proposed distinction inside the blind domain."],
   ["Reputation: only a judge of reputation is credited", "Reputation is persistent, so judging by it is vindicated.",
    "Judging blind to identity, or a test against consequences."]], [2.0, 2.4, 2.1])
P("Codex extended this (R1.14): judging small <i>groups</i> of judges can reveal distinctions invisible to every "
  "individual judge, and in a recorded example four hidden task classes were recovered from approvals in which "
  "each single judge was uninformative.")

H2("3.5 What judges' conventions cannot distort")
P("Suppose judges respond to how performances turn out but are as lenient or harsh as they like on each kind of "
  "task. Then the <i>transfer correlation</i> between two task types (how strongly success on one goes with success "
  "on the other, across performers) can be recovered from approvals of two performances by the same performer, and "
  "it comes out the same whatever the leniencies (R1.4, Theorem 9). Three simulated communities with different "
  "leniencies recovered the same matrix to fourteen decimal places.")
P("What conventions <i>can</i> hide is the scale: two tasks that draw on the same skill and differ in how hard they "
  "are, or in how sharply they depend on skill, can be made indistinguishable by a suitable pattern of leniency. "
  "(The second clause is a correction by Codex to the original statement.) So “which skill does this task draw "
  "on, and how are skills related” is a fact that survives convention, while “this task is harder” cannot "
  "be separated from “the judges are stricter here” using approvals alone. The identity involved is a "
  "classical one (the correction for attenuation in test theory).")

H2("3.6 Who determines what is seen again")
P("The author's framing (November 10, 2026): something has to determine success, and it can be “the same agent, "
  "another agent, or something in the environment that requires it.”")
T([["What determines reappearance", "What vindication certifies"],
   ["The same agent", "Nothing beyond the agent's own policy: the forecast produces what it forecasts."],
   ["Other agents", "Membership in the prevailing consensus. Every consensus is equally vindicated."],
   ["The environment, to any degree", "Alignment with the environment: always, if judges can revise their ratings; "
                                      "conditionally, if only their influence changes."]], [2.4, 4.1])
B(["<b>Self-revising judges end up tracking the world</b> however small the environment's share, because the "
   "self-fulfilling part of vindication rewards all ratings equally and so cannot choose between them. With fixed "
   "judges whose influence shifts, conventions can lock in, including one opposed to the environment (R1.7, "
   "Theorem 15, a first linear model).",
   "<b>Recursive weighting converges.</b> If judges gain weight by being borne out by weighted judges, the weights "
   "settle. Every competent judge keeps weight when the traits that judges track are connected in the population; "
   "otherwise weight can concentrate on the most mutually predictable family, which need not be the most accurate "
   "(R1.5, Theorem 12).",
   "<b>Coupled concepts and influence (Codex, R1.9 and R1.11 to R1.13).</b> Judges with different "
   "conceptualisations forecast, partly cause what recurs, and gain or lose influence by predictive success. Under "
   "a positive environmental share, continued learning by the alternatives, and a supplied set of candidate "
   "concepts rich enough to express the truth, forecasts converge to the environment's recurrence law and the "
   "adequate concepts are selected. A counterexample shows an initially wrong but useful model can be starved of "
   "influence. Deliberate probes can repair slow discovery: at a 5% environmental share, a probing learner reached "
   "an error of 0.0089 against 0.324 for the passive one."])

H2("3.7 Kinds of excellence")
P("The essay's “best tree” argument says that many judges with different values pick from a small set of "
  "exemplars. For judges who weigh criteria linearly, the set of objects that are ever picked is the same for "
  "every sufficiently diverse population of judges; only the frequencies depend on who is judging (R1.3, Theorem "
  "7). With normally distributed underlying causes the set is small and grows very slowly with the number of "
  "objects. Codex's review corrected an overstatement: few shared causes do not by themselves guarantee few "
  "exemplars; that needs a condition on how objects are distributed.")

H2("3.8 Harder settings (Codex)")
B(["<b>Performers who choose their tasks</b> (R1.10). Transfer structure can still be recovered, using three past "
   "performances, and an example shows that fewer can fail. This settles a question left open in R1.1.",
   "<b>Ordered recurrence</b> (R1.15). When seeing one thing makes another likely next but not the reverse, "
   "adequate concepts still exist, but a useful concept may need several distinctions adopted together; a rule that "
   "accepts only individually profitable splits can stall.",
   "<b>From prediction to decision.</b> A distinction that changes forecasts changes the best action in some "
   "simple decision, and a broad family of decisions values exactly the predictive distinctions. This classical "
   "fact is the bridge to the next module, which asks when different goals reward the same distinctions."])

H1("4. Progress against the theses")
T([["Thesis", "What this cycle supports", "What is still missing"],
   ["C1. Judging judges recovers fact",
    "Scoring forecasts of reappearance selects delineations fixed by the world (Theorems A and B), with quantitative "
    "versions, without an outside referee under stated conditions, and under skill-dependent choice of tasks.",
    "A test of validity that does not assume honest reporting or an environmental share. Finite-data guarantees for "
    "an adaptive learner. Difficulty cannot be recovered from approvals alone."],
   ["C2. T = J²",
    "A precise sense in which delineation and the crediting of judges determine each other (Theorem C), and a "
    "coupled selection process for concepts and influence.",
    "Concepts are selected from candidates that are supplied; generating new concepts is not yet part of the theory."],
   ["C3. Truth as a limit",
    "A conditional mechanism: specified learners converge to the environment's law when the environment has any share "
    "in what recurs and learning continues.",
    "No theory of truth: no notion of consequence, no treatment of changing languages or theories."],
   ["C5. Values over values",
    "Convergence of recursive weighting and of rating updates, with the condition separating pluralism from "
    "concentration. Evaluating judges is the same kind of problem as evaluating performers.",
    "Self-trust in the logical sense (a limit on self-endorsement) is untouched."]], [1.35, 2.75, 2.4])

H1("5. Faithfulness to the founding ideas")
B(["<b>Close to the essays.</b> The general reading of J as a forecast of reappearance is the author's own, and "
   "the central theorems are statements about judgment, delineation and vindication, not about a neighbouring "
   "technical problem. The examples (the random-looking judge, the best tree, Newtonian and relativistic regimes) "
   "come from the founding material.",
   "<b>A shift during the cycle.</b> The first three sessions read J more narrowly, as a forecast of a performer's "
   "result. The author's November 10 statement replaced that with the general reading, and the earlier results are "
   "now special cases of it. Codex's review notes that the two objectives are related but not identical.",
   "<b>Where the work leans on convenience.</b> Later results concentrate on learners with designed features "
   "(calibration, exploration, a supplied vocabulary). They show such learners succeed; they do not yet explain why "
   "agents would come to have those features. That question belongs to the next two modules."])

H1("6. What is not established")
B(["<b>No independent review.</b> Codex re-derived Theorems A, B and C and made corrections to five of "
   "Claude's results. Results R1.8 to R1.15 were written and checked by Codex alone. For this summary I re-ran "
   "five of Codex's checking programs; four matched their saved outputs and the fifth ran without "
   "error. I did not re-derive those proofs.",
   "<b>Classical mathematics.</b> The core results rest on sufficiency, proper scoring, the Perron-Frobenius "
   "theorem, test theory and evolutionary dynamics. The contribution is the identification of these structures "
   "with the project's ideas and the boundary statements, not new mathematics. Several sources were cited from memory.",
   "<b>Small worlds.</b> Numerical checks use small constructed examples chosen by the models that proved the "
   "statements.",
   "<b>Predictability is not validity.</b> Without an environmental share or honest reporting, vindication "
   "certifies consistency, including that of reputation."])

H1("7. Recommended next steps")
B(["Close this cycle and begin the module on instrumental convergence (W6), then the module on evolution and "
   "selection (W7). Both are needed before the first milestone can be assessed.",
   "Before that milestone, have results R1.8 to R1.15 re-derived by a model that did not write them, as was done "
   "for R1.1 to R1.7.",
   "Return to W1 for concept generation: a learner that proposes new distinctions and pays for the search."])

S.append(PageBreak())
H1("Appendix A. Formal statements and proofs of the three central theorems")
P("Notation: θ is the persistent state with law P; H(·) is entropy and I(·;·) mutual information, in "
  "nats; E is expectation over θ.", small)
H2("A.1 Theorem A (reappearance; R1.6, Theorem 13)")
P("<b>Setting.</b> Given θ, the things seen W<sub>1</sub>, W<sub>2</sub>, … are independent with law "
  "L(· | θ) on a finite set. A conceptualisation c maps things to kinds, and I(c) = I(c(W<sub>1</sub>); "
  "c(W<sub>2</sub>)). Two things w, w' are <i>equally diagnostic</i> if L(w | θ)/L(w) = L(w' | θ)/L(w') "
  "for almost every θ; c* merges exactly the equally diagnostic things.", thm)
P("<b>Statement.</b> (a) If c' refines c then I(c') ≥ I(c). (b) I(c) ≤ I(c*) = I(W<sub>1</sub>; W<sub>2</sub>), "
  "with equality exactly when c refines c*. (c) If c' splits one kind κ of c into two parts, then I(c') &gt; I(c) "
  "exactly when the parts' aggregate likelihoods g<sub>i</sub>(θ) = Σ<sub>w in part i</sub> L(w | θ) are "
  "not proportional.", thm)
P("<b>Proof.</b> (a) is the data-processing inequality. For I(c*) = I(W<sub>1</sub>; W<sub>2</sub>): the posterior of "
  "θ given W<sub>1</sub> depends on W<sub>1</sub> only through its class, hence so does the law of W<sub>2</sub> "
  "given W<sub>1</sub>; the same holds with the roles exchanged. For strictness, let c' refine c with I(c') = I(c). "
  "Writing c<sub>1</sub>, c<sub>2</sub> for the kinds of the two sightings, I(c<sub>1</sub>; c<sub>2</sub>) ≤ "
  "I(c'<sub>1</sub>; c<sub>2</sub>) ≤ I(c'<sub>1</sub>; c'<sub>2</sub>) are then equalities, so c'<sub>2</sub> is "
  "independent of c'<sub>1</sub> given c<sub>2</sub>. Within a kind κ of c with parts κ<sub>a</sub>, the "
  "chance that the next thing lies in κ<sub>b</sub> after one in κ<sub>a</sub> is proportional to "
  "Γ<sub>ab</sub> = E[g<sub>a</sub> g<sub>b</sub>] and must not depend on a. A symmetric matrix of this form "
  "with proportional rows has rank one, so the g<sub>a</sub> are proportional. This proves (c). Applying it to the "
  "common refinement of c and c* proves (b), because the parts of a kind that mixes two classes of c* are not "
  "proportional. □", thm)

H2("A.2 Theorem B (recurrent recovery; R1.1, Theorem 1)")
P("<b>Setting.</b> Task instances are drawn independently of θ (assumption A1), each type with positive "
  "probability. Given θ and the instances, results of distinct performances are independent, a performance of "
  "type z having result law f(· | θ, z) on a finite set (A2). Types z, z' are <i>twins</i> if f(· | θ, z) "
  "= f(· | θ, z') for almost every θ; τ denotes the map from a type to its twin class (the transfer partition) and "
  "f<sub>A</sub> the law of class A. A judge with delineation c sees n past (cell, result) pairs of one performer, "
  "H<sub>n</sub><super>c</super>, and the target's cell c<sub>0</sub>, and forecasts the target result Y<sub>0</sub>. "
  "The best expected log score is V<sub>n</sub>(c) = −H(Y<sub>0</sub> | H<sub>n</sub><super>c</super>, c<sub>0</sub>), "
  "attained by the Bayes forecast M<sub>n</sub><super>c</super>.", thm)
P("<b>Statement.</b> (a) V<sub>n</sub>(c) ≤ V<sub>n</sub>(τ) for all c and n, with equality when c refines "
  "τ. (b) For every n ≥ 1, if c does not refine τ then V<sub>n</sub>(c) &lt; V<sub>n</sub>(τ). (c) For "
  "n = 0 the optimal delineations are exactly the refinements of the difficulty partition.", thm)
P("<b>Proof.</b> (a) Let d be the common refinement of c and τ. By A1 and A2, given the twin classes of the n + 1 "
  "instances, (θ, results) is independent of the instances, so V<sub>n</sub>(d) = V<sub>n</sub>(τ); and "
  "V<sub>n</sub>(c) ≤ V<sub>n</sub>(d) because the judge with d can discard information. (b) Suppose a cell κ of "
  "c meets distinct classes A and B with positive probability and V<sub>n</sub>(c) = V<sub>n</sub>(d). Since "
  "M<super>c</super> is the conditional mean of M<super>d</super>, the gap V<sub>n</sub>(d) − V<sub>n</sub>(c) is the "
  "expected divergence between them, so M<super>d</super> = M<super>c</super> almost surely. Fix the d-labels and results "
  "ρ of history positions 2 to n, and let P<sub>ρ</sub> be the posterior of θ given ρ. For a, b in "
  "{A, B} put N<sub>ab</sub>(y', y) = ∫ f<sub>a</sub>(y' | θ) f<sub>b</sub>(y | θ) dP<sub>ρ</sub> and "
  "D<sub>a</sub>(y') = ∫ f<sub>a</sub>(y' | θ) dP<sub>ρ</sub>. When position 1 has label (κ, a) and "
  "result y' and the target has label (κ, b), M<super>d</super>(y) = N<sub>ab</sub>(y', y)/D<sub>a</sub>(y'). On all "
  "four such events the judge with c sees the same thing, so M<super>c</super>(y) is one number m(y). Hence "
  "N<sub>ab</sub> = m D<sub>a</sub> for all a, b, which gives N<sub>AA</sub> = N<sub>AB</sub> and N<sub>BA</sub> = "
  "N<sub>BB</sub>, and therefore ∫ (f<sub>A</sub>(y') − f<sub>B</sub>(y'))(f<sub>A</sub>(y) − "
  "f<sub>B</sub>(y)) dP<sub>ρ</sub> = 0. Taking y' = y shows f<sub>A</sub> = f<sub>B</sub> almost everywhere "
  "under P<sub>ρ</sub>, for every ρ, hence under P. So A and B are twins, a contradiction. (c) With no "
  "history V<sub>0</sub>(c) = −H(Y<sub>0</sub> | c<sub>0</sub>), which is maximal exactly when the once-met "
  "result law is constant on each cell, by strict concavity of entropy. □", thm)

H2("A.3 Theorem C (credited judges and delineation; R1.2, Theorem 5)")
P("<b>Setting.</b> A panel J of judges approves performances; the panel's approval vector on one performance has "
  "law k<sub>J</sub>(· | θ, x) for instance x, with k<sub>S</sub> its marginal on a subset S. Instances are "
  "drawn independently of θ, and approval vectors of distinct performances are independent given θ and the "
  "instances. π(S) is the twin partition of instances under k<sub>S</sub> (π of the empty set has one "
  "cell). Judge j is <i>vindicated under</i> c, written j ∈ Σ(c), if its approval of one performance and the "
  "panel's approvals of another performance of the same performer are dependent given the two cell labels. "
  "Φ(S) = Σ(π(S)).", thm)
P("<b>Statement.</b> (a) π, Σ and Φ are monotone, so the fixed points of Φ form a complete lattice. "
  "(b) Its largest element is the set J<sub>tr</sub> of judges whose approval law depends on θ on a set of "
  "instances of positive probability. (c) Iterating Φ from the empty set increases to the least fixed point; "
  "iterating from Σ(c<sub>0</sub>) for any delineation c<sub>0</sub> increases to the least fixed point "
  "containing Σ(c<sub>0</sub>).", thm)
P("<b>Proof.</b> (a) Twins for a larger set of judges are twins for every smaller set, so π is monotone. "
  "Vindication is the existence of a nonzero covariance, over θ, between a cell-averaged approval probability "
  "of j and one of the panel; cell averages of a coarser delineation are mixtures of those of a finer one and "
  "covariance is bilinear, so a nonzero covariance for coarse cells forces one for some pair of fine cells. "
  "Monotone maps on a finite lattice have a lattice of fixed points (Knaster and Tarski). (b) If k<sub>j</sub> does "
  "not depend on θ all its covariances vanish, so Σ(c) is contained in J<sub>tr</sub> for every c. "
  "Conversely, if j belongs to S and to J<sub>tr</sub>, then π(S) refines π({j}), so on some cell of "
  "positive probability j's approval probability has positive variance in θ; that variance is a sum of "
  "covariances with the panel's probabilities, so one of them is nonzero and j ∈ Φ(S). Hence Φ(J) = "
  "J<sub>tr</sub> = Φ(J<sub>tr</sub>). (c) Φ(S) contains S whenever S is contained in J<sub>tr</sub>, so "
  "the chains increase, and by monotonicity their limits lie below every fixed point above the start. □", thm)

H1("Appendix B. Index of the cycle's results")
P("Files are in the repository folder v4/results. “Claude” is Claude (Fable 5.2); “Codex” is Codex (GPT-6).", small)
T([["No.", "Subject", "By", "Theses"],
   ["R1.1", "Recurrent judgment recovers the transfer structure of tasks (Theorem B)", "Claude", "C1, C2"],
   ["R1.2", "Judges vindicated by later judgments; fixed points; bounded judges (Theorem C)", "Claude", "C1, C2"],
   ["R1.3", "Excellence exemplars: what choices of “the best” reveal", "Claude", "C1"],
   ["R1.4", "What survives the judges' conventions: transfer geometry", "Claude", "C1"],
   ["R1.5", "Reinforcing judges by weighted vindication: convergence and concentration", "Claude", "C5, C2"],
   ["R1.6", "Judgment as a forecast of reappearance (Theorem A)", "Claude", "C1, C2"],
   ["R1.7", "Who determines what is seen again: ratings that cause recurrence", "Claude", "C1, C3, C5"],
   ["R1.8", "How much predictive value is lost by merging kinds", "Codex", "C1, C2"],
   ["R1.9", "Coupled judgment and conceptual kinds under self-influenced recurrence", "Codex", "C1, C2, C3, C5"],
   ["R1.10", "Transfer recovery when performers choose their tasks", "Codex", "C1, C2"],
   ["R1.11", "Finite evidence under self-influenced recurrence; probes and costs", "Codex", "C1, C2, C3"],
   ["R1.12", "Grounded judgments under weakening environmental influence", "Codex", "C1, C2, C3"],
   ["R1.13", "Coupled judgment from observed outcomes: an implemented learner", "Codex", "C1, C2, C3"],
   ["R1.14", "Small coalitions can recover joint judgment structure", "Codex", "C1, C2"],
   ["R1.15", "Directed reappearance: concepts that require a joint refinement", "Codex", "C1, C2, C3"]],
  [0.55, 4.25, 0.7, 1.0])

def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Sans", 7.5); canvas.setFillColor(colors.HexColor("#5b6670"))
    canvas.drawString(inch, .55 * inch, "Judging the Judges: summary of Value Logic cycle P4-R1-C001. Prepared by Claude (Fable 5.2), November 11, 2026.")
    canvas.drawRightString(letter[0] - inch, .55 * inch, f"{doc.page}")
    canvas.restoreState()

out = sys.argv[1]
doc = SimpleDocTemplate(out, pagesize=letter, leftMargin=inch, rightMargin=inch, topMargin=.9 * inch, bottomMargin=.9 * inch,
                        title="Judging the Judges: what recursive judgment recovers", author="Claude (Fable 5.2), for Tristan Miano",
                        subject="Summary of Value Logic phase-four cycle P4-R1-C001 (module W1)")
doc.build(S, onFirstPage=footer, onLaterPages=footer)
print("built", out)
