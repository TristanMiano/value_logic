#!/usr/bin/env python3
"""Build the W6 cycle summary PDF (v4/reports/W6_cycle_summary.pdf).

Prepared by Claude (Fable 5.2), 2026-11-12, at the author's request. Reuses the
page styles of build_w1_summary.py, which must sit beside this file. Needs
reportlab and the DejaVu fonts. Usage: python build_w6_summary.py OUTPUT.pdf
"""
import pathlib, sys
_src = (pathlib.Path(__file__).parent / "build_w1_summary.py").read_text(encoding="utf-8")
exec(_src.split("# ------------------------------------------------------------------ title")[0])

P("Shared Purposes, Shared Facts", title)
P("What agents with different goals come to value in common, and when a useful priority persists: a summary of "
  "the second phase-four research cycle of the Value Logic project", sub)
P("Prepared for Tristan Miano by <b>Claude (Fable 5.2)</b>, November 12, 2026. The results summarised here "
  "(R6.1 to R6.16 and two supplements) were produced by <b>Codex (GPT-6)</b> on November 12, 2026, in the cycle "
  "identified in the repository as P4-R6-C001.", small)
BOX("<b>Status of everything in this document.</b> All results are model-generated, by a single model, and none "
    "has been independently reviewed. For this summary I re-ran the cycle's report verifier and six of its checking "
    "programs, which reproduced their saved outputs, and independently recomputed the reference values of the "
    "central example (Appendix A.1). I did not re-derive the other proofs. Much of the mathematics is established "
    "and is used to make the project's questions precise; section 6 lists what is not shown.")

H1("1. The question")
P("The previous cycle (module W1) found that judging judges recovers facts about the world only if something "
  "outside the judges has a say in what succeeds. This cycle, on the plan's module W6, asks what that outside "
  "pressure looks like when many agents with <i>different</i> goals live in one world.")
P("<b>Instrumental convergence</b> is the observation that agents with different final goals often benefit from "
  "the same intermediate things: the same capabilities, the same information, the same preserved options. The "
  "module asks three things about it: when it happens, whether what agents converge on is <i>fact</i> or merely "
  "agreement, and what it implies for how goals persist or change.")
P("The cycle's record says it answers four questions posed by the author. I report them as the record describes "
  "them, not in the author's original wording:")
B(["Can an agent acquire direction when no final goal is represented in it at the start?",
   "Can a useful intermediate priority become persistent, or “terminal-like”, and in what degrees?",
   "If final goals are held fixed, what is still free to adapt?",
   "How does instrumental convergence connect to judging judgments (written J² in the author's essays, "
   "meaning the evaluation of how good a judge is)?"])
P("The project's charter lists seven theses, labelled C1 to C7. This cycle bears on five:")
T([["Label", "Thesis"],
   ["C1", "Judging judges forces the recovery of factual distinctions."],
   ["C2", "Task delineation and judging judgments are two faces of one operation."],
   ["C3", "Truth is the limit of value under successful use."],
   ["C5", "Self-trust is possible but constrained; values can be assigned to values without chaos."],
   ["C7", "Policy and value are dual: what an agent does and what it values can each be reconstructed from the other."]],
  [0.6, 5.9])

H1("2. Vocabulary")
T([["Term", "Meaning in this document"],
   ["Final (terminal) goal", "What an agent ultimately pursues, valued for itself."],
   ["Instrumental value, priority, subgoal", "Something valued because it helps reach other goals: a capability, a "
                                              "piece of information, an option kept open."],
   ["Convergence", "Different agents, with different final goals, coming to value the same thing. Distinct from "
                   "<i>persistence</i>, which is one agent keeping a value over time."],
   ["Representation", "The distinctions an agent keeps about its situation; the same notion as a delineation or "
                      "conceptualisation in the W1 summary. Keeping more distinctions costs more."],
   ["Forecast, purchased feedback", "An agent states how likely an opportunity is to pay off, decides whether to "
                                    "buy it at the offered price, and learns the outcome only if it buys."],
   ["Policy", "A rule saying what to do in each situation."],
   ["Value (of a state)", "How well an agent expects to do from that state onward under a given policy."],
   ["Planning depth", "How many steps ahead a limited planner looks."],
   ["Revision", "A change in an agent's priorities over time."],
   ["Selection, retention", "An outside process that keeps some behaviours and discards others, for example by survival."]],
  [2.0, 4.5])

H1("3. Main findings")
H2("3.1 Different goals can select the same fact, and the selection can be learned")
P("The central example is a world of eight situations that conceal three independent yes-or-no facts: one that "
  "matters to both agents (the common fact) and one private to each. An agent sees a situation, a goal label and "
  "a price, decides whether to buy, and sees the outcome only if it buys. It is told neither what the situations "
  "mean nor the odds. Keeping an extra distinction has a stated cost.")
B(["<b>Overlap decides what is kept.</b> When the goal that depends on the common fact arises more than half the "
   "time, the common fact is the best single distinction to keep; below half, each agent's private fact is. I "
   "recomputed this boundary and the reference values independently (Appendix A.1).",
   "<b>The learner finds it from its own purchases.</b> Comparing all 4,140 possible groupings of the eight "
   "situations, learners trained on purchased feedback chose the predicted representation in 64 of 64 runs at "
   "both settings tested (R6.16, with a consistency proof under stated assumptions)."])
T([["How often the common goal arises", "Representation chosen", "Learner's net return", "Return with no distinctions", "Best possible with the odds known"],
   ["80%", "the common fact, 64 of 64 agents", "0.1365", "0.1250", "0.1410"],
   ["40%", "own private fact, 64 of 64 agents", "0.1272", "0.1250", "0.1320"]], [1.5, 1.7, 1.0, 1.15, 1.15])
B(["<b>Agreement is not the same as fact.</b> In the low-overlap world both agents can agree on a coarse forecast "
   "near one half while discarding a real 20%-versus-80% distinction. Their agreement is useful at that cost and "
   "has less factual content. What makes the common distinction a fact is the environment and the payoff "
   "arrangement, not the number of agents who hold it (R6.1).",
   "<b>The pressure is weak near indifference.</b> With the common goal at 51%, 41 of 64 agents chose the common "
   "fact at the original budget and 52 of 64 with more evidence; at exactly 50% mixed choices persist.",
   "<b>Durability and change.</b> If a distinction is paid for once and reused, keeping both the common and the "
   "private fact eventually pays for any positive frequency of both goals. If goal frequencies change while the "
   "facts stay the same, old evidence can be re-weighted: the newly useful distinction was selected in 31 of 32 "
   "runs before any new purchase.",
   "<b>Useful information still has to be paid for.</b> When a reusable observation is worth more to the agents "
   "together than it costs, an agreed sequence of cost shares can fund it, but simultaneous voluntary "
   "contributions also admit an outcome in which nobody pays (R6.3)."])

H2("3.2 What “persistent” means: four different measurements")
P("The essays suggest that the line between instrumental and final values blurs: a value that keeps being useful "
  "becomes entrenched. The cycle's answer is that this is true in degrees, and that the degrees are different "
  "quantities which should not be merged into one notion of “terminal” (R6.4):")
T([["Measurement", "Question it answers"],
   ["Breadth", "How many goals benefit from the priority, with what weights and costs?"],
   ["Robustness", "Does the priority survive changes in goals and circumstances?"],
   ["Resistance to revision", "How readily can the priority itself change?"],
   ["Persistence after its benefit is removed", "Does the priority remain when the practical support that produced it is taken away?"]],
  [2.4, 4.1])
B(["<b>A guarantee of persistence.</b> If a priority gives an advantage in every goal context and the routes by "
   "which goals change overlap enough, its long-run frequency has an explicit positive lower bound. Sorting by "
   "goal can defeat the guarantee; restoring overlap repairs it.",
   "<b>Entrenchment is conditional.</b> When the benefit is removed, continued revision eventually erases the "
   "acquired priority. It is preserved only if revision dies away quickly enough, or if coordination with others "
   "sustains it as a convention. A stronger original advantage raises the acquired level but not how long it "
   "lasts after removal.",
   "<b>Agreeing on average is not converging together</b> (R6.11). Agents who share one history are drawn "
   "together by revision; agents with separate histories can remain different even when their long-run "
   "statistics agree."])

H2("3.3 Fixed final goals, adaptable means")
B(["<b>Shared internal values help limited planners</b> (R6.6). Three agents with different fixed goals all "
   "benefit from the same “preparation” value when they can plan only one step ahead: their expected "
   "returns rise from 0.4 to 0.6, 0.7 and 0.8. In an environment where preparation rarely succeeds, the same "
   "value is harmful, and feedback rejects it.",
   "<b>How a value is used matters</b> (R6.15). Paid as a recurring bonus, a value for an intermediate state can "
   "make an agent linger to collect it instead of finishing the task. Paid as a difference between successive "
   "states, it guides without changing what is ultimately best (Appendix A.2). This separates making a means "
   "salient from adding it as an end.",
   "<b>Commitment</b> (R6.10). In strategic settings an agent can gain, by its earlier standard, from visibly "
   "binding itself to a different preference. Regions where such commitments spread, vanish or coexist are mapped "
   "for a two-type model."])

H2("3.4 Direction without a represented final goal")
P("Start from behaviour with no goal at all, and let an outside process retain the histories that survive. Long "
  "retained histories then behave as if guided by a value, although no ultimate objective is written inside the "
  "agent; the environment and the retention rule supply the direction (R6.12, an interpretation of established "
  "mathematics).")
B(["<b>Copy actions, not luck.</b> Imitating the <i>states</i> that survivors passed through credits them with "
   "control over chance events. Imitating their <i>actions</i> and then living with the real consequences does "
   "not. With correctly timed copying, survival improves, and under stated conditions repeated copying converges "
   "to the best achievable survival rate (R6.13).",
   "<b>It works, slowly and imperfectly.</b> In one world the copied controller's survival over 32 steps was "
   "0.0176 against 0.0012 initially, while an informed controller achieves certainty. In another, copying from "
   "one-step success made long-run survival <i>worse</i> (0.365 against 0.515) and a longer horizon was needed "
   "(0.791). Rare successes make learning from finite samples unreliable, and ordinary planning with a model was "
   "faster wherever both were run."])
P("Why such a retention process and its rules should exist and remain stable is the question for the next module.")

H2("3.5 The link to judging judgments")
P("Instrumental convergence asks which intermediate capabilities serve many purposes. Judging judges asks which "
  "judges and distinctions support successful judgments. When both are scored by the same real consequences of "
  "decisions, they can select the same factual representation; the central example is an implemented case.")
B(["<b>Judgments of policies can identify the world</b> (R6.8). If one is told how well certain policies do, "
   "the environment's dynamics can be recovered when those judgments are varied enough; in a small class of "
   "environments four specified policies suffice and fewer do not. The judgments are supplied, not discovered.",
   "<b>Success alone underdetermines fact</b> (R6.7). Knowing the best achievable outcome for every goal fixes "
   "what is attainable, but an action that is never best can change without any best outcome changing. Judging "
   "that action's consequences directly is what tells the two worlds apart."])

H1("4. Progress against the theses")
T([["Thesis", "What this cycle supports", "What is still missing"],
   ["C1. Judging judges recovers fact", "Real decision losses identify which distinctions are worth keeping, and "
    "a learner selects them from paid feedback.", "The candidate distinctions and the evaluator are supplied. No "
    "advantage over an ordinary learner with the same information is claimed."],
   ["C2. Delineation and judging judges are one operation", "Representations are chosen by the decisions their "
    "forecasts support, with a worked boundary between shared and private choices.", "This mechanism and the "
    "previous cycle's fixed points of judges and delineations have not been joined."],
   ["C3. Truth as a limit", "Conditions that separate grounded agreement from a useful coarse consensus, in "
    "finite examples.", "No construction of truth as a limit."],
   ["C5. Values over values", "Explicit regimes of stability, flexibility and diversity for revisable "
    "priorities.", "Where the revision rule comes from; self-endorsement in the logical sense."],
   ["C7. Policy and value", "Behaviour reconstructed from values; an environment identified from judgments of "
    "policies.", "Size, cost and learned representations."]], [1.35, 2.65, 2.5])

H1("5. Faithfulness to the founding ideas")
B(["<b>The module's own question is answered at a restricted scope.</b> The cycle does what the plan asked: it "
   "defines convergence, separates agreement across agents from change within one, and states when shared "
   "usefulness amounts to shared fact.",
   "<b>It qualifies an essay claim instead of confirming it.</b> The essay “Is Utility All You Need?” says "
   "the distinction between terminal and instrumental values is “largely gone.” The cycle's result is "
   "more specific: a useful priority can entrench, but removing its benefit erases it unless revision stops or "
   "others sustain it. That is an informative correction and should be stated as one.",
   "<b>Breadth over depth.</b> Eighteen documents were produced in one four-hour cycle. Most are small finite "
   "constructions, and several restate established results in the project's terms. The central example's sharp "
   "boundary is an elementary calculation; the substantive part is that it is learned from purchased feedback. "
   "The portfolio is useful as a map, and thinner as support for any single thesis than its size suggests."])

H1("6. What is not established")
B(["<b>No independent review</b> of any result in this cycle. Together with the second half of the previous "
   "cycle, about two dozen results now rest on one model's proofs and checks.",
   "<b>Small constructed worlds.</b> The shared fact is built into the central example; the result shows when it "
   "is selected, not that real environments contain such facts.",
   "<b>Supplied ingredients.</b> Candidate distinctions, the evaluator, and the retention rule are given.",
   "<b>No integration</b> with the previous cycle's results on judges, and no account of why the selecting "
   "environment has the form it does."])

H1("7. Recommended next steps")
B(["Proceed to the module on evolution and selection (W7), as the cycle recommends, and build one model in depth "
   "there instead of another broad portfolio.",
   "Before the first milestone is assessed, have the load-bearing results of both cycles re-derived by a model "
   "that did not write them.",
   "Keep W6 open for the integration with W1 and for learners that generate their own distinctions."])

S.append(PageBreak())
H1("Appendix A. Two derivations behind the findings")
P("These are the derivations I checked myself. Proofs of the cycle's other results are in the files listed in "
  "Appendix B and were not re-derived for this summary.", small)
H2("A.1 The value of a distinction, and the shared-or-private boundary")
P("<b>Setting.</b> An opportunity pays 1 with probability q. A price p is drawn uniformly between 0 and 1, and "
  "the agent buys when its forecast f exceeds the price.", thm)
P("<b>Value of a forecast.</b> The expected net return is the integral of (q − p) over prices from 0 to f, "
  "which equals q f − f<super>2</super>/2. It is largest at f = q, where it equals q<super>2</super>/2, and "
  "a forecast f loses (q − f)<super>2</super>/2 relative to that. So an agent that forecasts each group of "
  "situations at the group's true rate earns one half of the average squared rate, and distinguishing two groups "
  "gains one half of the variance between them.", thm)
P("<b>The example.</b> A fact makes the rate 0.8 or 0.2 with equal chance. Knowing it earns (0.64 + 0.04)/4 = "
  "0.17 per use; not knowing it earns 0.25/2 = 0.125. The gain is 0.045 per use.", thm)
P("<b>The boundary.</b> Let the goal that depends on the common fact arise a fraction c of the time and the "
  "private goal the rest, and let an extra distinction cost 0.02. Keeping the common fact returns 0.125 + 0.045 c "
  "− 0.02; keeping the private fact returns 0.125 + 0.045 (1 − c) − 0.02; keeping neither returns "
  "0.125; keeping both costs three extra groups and returns 0.125 + 0.045 − 0.06 = 0.110. Hence the common "
  "fact is the best choice exactly when c exceeds one half and the private fact when c is below it. At c = 0.8 "
  "the best return is 0.141 and at c = 0.4 it is 0.132, the reference values reported in section 3.1. (The "
  "uniform price and the cost per extra group are my reading of the model; they reproduce the reported values.)", thm)
H2("A.2 Why a value paid as a difference guides without distorting")
P("<b>Setting.</b> A task gives reward r at each step, discounted by a factor γ per step. Let Φ assign "
  "a number to each state. Add to each step's reward the amount γ Φ(next state) − Φ(current "
  "state).", thm)
P("<b>Claim.</b> Every course of action has its total discounted reward changed by the same amount, −Φ "
  "of the starting state (for tasks that end, or with Φ bounded). So the ranking of courses of action, and "
  "therefore the best policy, is unchanged.", thm)
P("<b>Proof.</b> Along any sequence of states s<sub>0</sub>, s<sub>1</sub>, … the added amounts are "
  "γ Φ(s<sub>1</sub>) − Φ(s<sub>0</sub>), then γ times (γ Φ(s<sub>2</sub>) "
  "− Φ(s<sub>1</sub>)), and so on. In the discounted sum each Φ(s<sub>k</sub>) for k ≥ 1 "
  "appears once with coefficient +γ<super>k</super> and once with −γ<super>k</super>, and cancels; "
  "only −Φ(s<sub>0</sub>) remains. □", thm)
P("By contrast a bonus paid for <i>being in</i> a state, at every step, does not cancel: it adds reward for "
  "staying, which is how a means can turn into something the agent lingers to collect. This invariance is a "
  "classical result on reward shaping, quoted here from memory.", thm)

H1("Appendix B. Index of the cycle's results")
P("Files are in the repository folder v4/results. All are by Codex (GPT-6), November 12, 2026.", small)
T([["No.", "Subject", "Evidence stated by its author"],
   ["R6.1", "Practical goal coverage and common factual kinds", "Proof, exact checks"],
   ["R6.2", "Observed shared representation and coverage repair", "Proof, sampled learning"],
   ["R6.3", "Reusable observation value and provision", "Proof, exact checks"],
   ["R6.4", "Persistent revisable priorities and degrees of terminality", "Proof, exact and numerical checks"],
   ["R6.5", "Learning judgments from purchased payoffs", "Proof, sampled learning"],
   ["R6.6", "Shared internal values for bounded planning", "Proof, exact checks"],
   ["R6.7", "Capability geometry and information comparison", "Proof, exact checks"],
   ["R6.8", "Conditional policy/value reconstruction; world identification (supplement)", "Proof, exact witnesses"],
   ["R6.9", "Weighted retargeting and option costs", "Proof, exact checks"],
   ["R6.10", "Strategic preferences and observable commitments", "Proof, exact and numerical checks"],
   ["R6.11", "Shared histories and changing goal distributions", "Proof, numerical and sampled checks"],
   ["R6.12", "Externally retained values and actual action copying", "Proof, sampled runs"],
   ["R6.13", "Exact and finite-trial survival learning (with a sampling supplement)", "Proof, numerical and sampled checks"],
   ["R6.14", "Context-dependent goals and adequate side-information codes", "Proof, exact checks"],
   ["R6.15", "Continuation values, bonus fixation and correction", "Proof, exact and numerical checks"],
   ["R6.16", "Paid shared/private learning, changed relevance, near ties and reuse", "Proof, exact and sampled checks"]],
  [0.6, 3.9, 2.0])

def footer6(canvas, doc):
    canvas.saveState()
    canvas.setFont("Sans", 7.5); canvas.setFillColor(colors.HexColor("#5b6670"))
    canvas.drawString(inch, .55 * inch, "Shared Purposes, Shared Facts: Value Logic cycle P4-R6-C001. Prepared by Claude (Fable 5.2), November 12, 2026.")
    canvas.drawRightString(letter[0] - inch, .55 * inch, f"{doc.page}")
    canvas.restoreState()

out = sys.argv[1]
doc = SimpleDocTemplate(out, pagesize=letter, leftMargin=inch, rightMargin=inch, topMargin=.9 * inch, bottomMargin=.9 * inch,
                        title="Shared Purposes, Shared Facts", author="Claude (Fable 5.2), for Tristan Miano",
                        subject="Summary of Value Logic phase-four cycle P4-R6-C001 (module W6)")
doc.build(S, onFirstPage=footer6, onLaterPages=footer6)
print("built", out)
