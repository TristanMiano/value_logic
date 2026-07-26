#!/usr/bin/env python3
"""Finalize Task 33's project-control records after validating the merged article."""

from __future__ import annotations

import os
import re
import unicodedata
from pathlib import Path


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected one match, found {count}")
    return text.replace(old, new, 1)


def update_todo(run_url: str) -> None:
    path = Path("TODO.md")
    text = path.read_text(encoding="utf-8")
    text = replace_once(
        text,
        "**Next task: Task 33 — Produce the Substack adaptation.**",
        "**Next task: Task 34 — Cross-check and finalize both artifacts.**",
        "TODO next-task pointer",
    )
    text = replace_once(
        text,
        "- [ ] **Task 33 — Produce the Substack adaptation.**",
        "- [x] **Task 33 — Produce the Substack adaptation.**",
        "Task 33 checkbox",
    )

    task34_marker = "\n- [ ] **Task 34 — Cross-check and finalize both artifacts.**"
    completion = f"""
  Completed 2026-07-25. Created
  [`substack_post.txt`](substack_post.txt), a 4,878-word plain-text adaptation
  of the audited paper. It preserves the required succession-to-value-to-
  fallback-to-license-to-ReLU-to-results narrative, carries the canonical
  adequacy/improvement/latency example through strict surplus, supported
  equality, open, refuted, and missing-evidence cases, and keeps full licensing
  separate from post-license ranking. The article includes every surviving
  claim-ledger `X1` impact at its narrowed scope, including the finite
  policy/value existence result and the conditional proper-score information
  result, without adding a theorem, empirical claim, or evidence grade.

  The public empirical account retains target non-Granted prevalence `.65`,
  target-weighted fallback `.9962/.9139`, and unweighted design-distribution
  conditional-Granted accuracy `.0124/.1811` with their exact labels. It says
  issued-`Granted` mass is not recall, target-weighted conditional accuracy is
  unavailable, and the complete-pipeline difference is not an identified
  wrapper effect. ReLU remains one finite reference witness rather than a
  unique or presumptively optimal architecture.

  Artifact lint found UTF-8 NFC, LF-only text, no Markdown syntax, and exactly
  one standalone formal line. Public GitHub Actions run
  [`30187216977`](https://github.com/TristanMiano/value_logic/actions/runs/30187216977)
  passed the repository semantic and link checks at artifact commit
  `64234227135ffbf19fd29facca4254d32a887183`. The completion-record preparation
  run [is recorded here]({run_url}) and executes the 177-check suite, repaired
  experiment preflight, local-link checker, plain-text assertions, and
  `git diff --check` before committing. The handoff is propagated through the
  [`README`](README.md) and
  [`project specification`](notes/project_spec.md). No experiment was rerun or
  regraded; Task 34 owns the final claim-by-claim crosswalk and proofreading.
"""
    text = replace_once(
        text,
        task34_marker,
        completion + task34_marker,
        "Task 33 completion insertion",
    )

    decision_marker = "## Decision log\n\n"
    decision = (
        "- **2026-07-25 — The Substack adaptation preserves scope while "
        "changing register.** `substack_post.txt` is a plain-text public essay "
        "rather than a second formal paper: it keeps the running succession "
        "example, fallback-derived tolerance, four-way assessment, activation-"
        "to-license correction, complete frozen result asymmetry, and every "
        "surviving `X1` impact. The article retains the finite policy/value "
        "encoder-image existence result while assigning standard-return and "
        "rollout failures to semantics, identification, and practicality; "
        "properly baselined log-loss gain supports only partial outcome/task-"
        "quotient information. No theorem, claim grade, experiment, architecture-"
        "uniqueness claim, or target-weighting interpretation changes.\n"
    )
    text = replace_once(
        text,
        decision_marker,
        decision_marker + decision,
        "Task 33 decision-log insertion",
    )
    path.write_text(text, encoding="utf-8", newline="\n")


def update_readme() -> None:
    path = Path("README.md")
    text = path.read_text(encoding="utf-8")
    text = replace_once(
        text,
        "All scheduled work through Task 32",
        "All scheduled work through Task 33",
        "README completed-through status",
    )
    old = "result, grade, or policy/value boundary changed. **Task 33 is next.**"
    new = """result, grade, or policy/value boundary changed.

[`Task 33`](substack_post.txt) completes the plain-text Substack adaptation. Its
4,878 words preserve the paper's argumentative order and running example while
translating the calculus, ReLU interface, composition and update boundaries,
and optional policy/value motivation into public prose. The frozen empirical
section keeps changed-tolerance transfer, the refuted boundary and in-regime
claims, marginal proposal coverage, target-weighted fallback `.9962/.9139`, and
unweighted conditional-Granted accuracy `.0124/.1811` at their exact scopes.
Issued grants are not called recall, complete-pipeline differences are not
causally allocated, and ReLU remains one reference witness. Plain-text lint and
public semantic/link CI pass without a new experiment or claim change.
**Task 34 is next.**"""
    text = replace_once(text, old, new, "README Task 33 handoff")
    path.write_text(text, encoding="utf-8", newline="\n")


def update_project_spec() -> None:
    path = Path("notes/project_spec.md")
    text = path.read_text(encoding="utf-8")
    text = replace_once(
        text,
        "Status: living specification, version 3.9 after Task 32 publication formatting",
        "Status: living specification, version 4.0 after Task 33 Substack adaptation",
        "project-spec version",
    )
    text = replace_once(
        text,
        "Task 32 Gist-compatibility and publication formatting: 2026-07-25\n",
        "Task 32 Gist-compatibility and publication formatting: 2026-07-25\n"
        "Task 33 Substack adaptation: 2026-07-25\n",
        "project-spec task history",
    )
    gate_marker = "\n## 18. Specification gates after Checkpoint E"
    decision = """
154. Task 33 creates `substack_post.txt` as a 4,878-word, non-Markdown public
adaptation with one standalone formal line. It preserves the required narrative
order, the canonical adequacy/improvement/latency fixture, all four public
outcomes, the activation-to-prediction-to-certificate-to-license ladder, and
the hybrid authorization boundary. Every surviving `X1` impact appears at its
narrowed scope. The frozen empirical section retains target non-Granted
prevalence `.65`, target-weighted fallback `.9962/.9139`, and unweighted
design-distribution conditional-Granted accuracy `.0124/.1811`; issued grants
are not recall, target-weighted conditional accuracy remains unavailable, and
complete-pipeline differences receive no causal wrapper allocation. The finite
policy/value encoder-image isomorphism survives; standard-return and rollout
limitations concern semantics, identification, and practicality, while the
proper-score result establishes only partial outcome/task-quotient information
under its baseline and mediation assumptions. Public run `30187216977` passes
at artifact commit `64234227135ffbf19fd29facca4254d32a887183`. No theorem,
claim grade, experiment, architecture-uniqueness claim, or policy/value
existence boundary changes. Task 34 remains the final cross-artifact audit.
"""
    text = replace_once(
        text,
        gate_marker,
        "\n" + decision + gate_marker,
        "project-spec Task 33 decision",
    )
    path.write_text(text, encoding="utf-8", newline="\n")


def validate_article() -> None:
    article = Path("substack_post.txt").read_text(encoding="utf-8")
    if not unicodedata.is_normalized("NFC", article):
        raise SystemExit("substack_post.txt is not NFC")
    if "\r" in article or "\t" in article or "\0" in article:
        raise SystemExit("substack_post.txt contains forbidden control characters")

    forbidden = {
        "Markdown heading": r"(?m)^#{1,6}\s",
        "Markdown bullet": r"(?m)^\s*[-*+]\s+",
        "numbered list": r"(?m)^\s*\d+[.)]\s+",
        "fence": r"```",
        "inline-code delimiter": r"`",
        "Markdown link": r"\[[^\]\n]+\]\([^\)\n]+\)",
        "HTML tag": r"<[A-Za-z][^>]*>",
        "asterisk": r"\*",
        "underscore": r"_",
    }
    for label, pattern in forbidden.items():
        if re.search(pattern, article):
            raise SystemExit(f"substack_post.txt contains {label}")

    formal_lines = [
        line
        for line in article.splitlines()
        if line.strip()
        and any(op in line for op in (" = ", "≤", "≥", "→"))
        and len(line.split()) <= 12
    ]
    if formal_lines != ["εB(D) = J(B,D) − Δ"]:
        raise SystemExit(f"unexpected standalone formal lines: {formal_lines!r}")

    words = re.findall(r"\b[\w’'-]+\b", article, re.UNICODE)
    if len(words) != 4878:
        raise SystemExit(f"unexpected article word count: {len(words)}")

    required = [
        ".65",
        ".9962",
        ".9139",
        ".0124",
        ".1811",
        "Remembering the number helped when the rule changed",
        "issued-Granted mass may contain false grants and is not recall",
        "not an identified causal decomposition",
        "finite isomorphism or lossless correspondence",
        "one explicit reference witness",
    ]
    missing = [item for item in required if item.lower() not in article.lower()]
    if missing:
        raise SystemExit(f"missing required article content: {missing}")


def main() -> None:
    run_url = os.environ.get(
        "FINALIZE_RUN_URL",
        "https://github.com/TristanMiano/value_logic/actions",
    )
    validate_article()
    update_todo(run_url)
    update_readme()
    update_project_spec()


if __name__ == "__main__":
    main()
