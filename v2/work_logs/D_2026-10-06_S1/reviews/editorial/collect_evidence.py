"""Read-only baseline inventory for Gate D's requested editorial corrections.

Contributor: ChatGPT (GPT-6 Astra Pro), delegated editorial reviewer.
Only this review directory receives new files. No scientific code is imported.
"""

from collections import Counter
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent
BASE = "f7aa0bef07cb21da9336429426244f6e944644a4"


def baseline(path):
    return subprocess.check_output(["git", "show", f"{BASE}:{path}"], cwd=ROOT)


EVIDENCE = {
    "paper_v2.md": [(1, 6), (1754, 1764)],
    "v2/RESEARCH_PROTOCOL.md": [(371, 380)],
    "v2/derivations/03f_soundness_acceptance.md": [(1, 7)],
    "v2/derivations/04_characterization.md": [(1, 6)],
    "v2/derivations/05_fragments_and_comparisons.md": [(1, 8)],
    "v2/derivations/06_n01_decision_retention.md": [(1, 5)],
    "v2/derivations/09_c4_price_revision.md": [(1, 9), (411, 420)],
    "v2/derivations/10_f16_coherent_recovery.md": [(1, 8)],
    "v2/work_logs/F08_2026-09-30_S1.md": [(1, 5), (224, 230)],
    "v2/work_logs/F14_2026-10-04_S1.md": [(298, 318)],
    "v2/work_logs/F15_2026-10-04_S1.md": [(1, 9)],
    "v2/work_logs/F15_ND01_2026-10-05_S1.md": [(1, 8)],
    "v2/work_logs/F17_2026-10-06_S1.md": [(1, 5)],
    "substack_post.txt": [(1, 7)],
    "README_phase1_archive.md": [(208, 217)],
    "TODO.md": [(963, 969)],
    "TODO_v2_contracts_archive.md": [(12, 18)],
    "llm_convos/README.md": [(1, 16)],
    "llm_convos/claude_audit_2026-07-11.md": [(1, 16)],
    "llm_convos/claude_audit_2026-07-12.md": [(1, 9)],
    "llm_convos/claude_audit_2026-07-14.md": [(1, 9)],
    "llm_convos/claude_audit_2026-07-17.md": [(1, 9)],
    "llm_convos/claude_audit_2026-07-21.md": [(1, 9)],
    "llm_convos/claude_audit_2026-07-24.md": [(1, 19)],
    "llm_convos/claude.txt": [(37, 40), (225, 225), (310, 314)],
    "verification/test_paper_markdown.py": [(1, 34)],
}

source_bindings = []
for path, ranges in EVIDENCE.items():
    data = baseline(path)
    lines = data.decode().splitlines()
    source_bindings.append({
        "path": path, "sha256": sha256(data).hexdigest(), "bytes": len(data),
        "read_scope": "Selected attribution or compatibility passages; not a fresh full substantive review.",
        "passages": [{"start_line": a, "end_line": b,
                      "text": "\n".join(lines[a-1:b])} for a, b in ranges],
    })

paper = baseline("paper_v2.md").decode()
macros = Counter(re.findall(r"\\([A-Za-z]+)", paper))
occurrences = []
for line, text in enumerate(paper.splitlines(), 1):
    for m in re.finditer(r"\\operatorname\{([^{}]+)\}", text):
        occurrences.append({"line": line, "name": m[1], "source_line": text})

result = {
    "schema": "Gate-D-editorial-evidence-v1",
    "contributor": "ChatGPT (GPT-6 Astra Pro), delegated editorial reviewer",
    "created_utc": datetime.now(timezone.utc).isoformat(),
    "base_commit": BASE,
    "principal_concurrent_credit_minutes": 0,
    "scientific_runs": 0,
    "paper": {"path": "paper_v2.md", "sha256": sha256(paper.encode()).hexdigest(),
              "macro_counts": dict(sorted(macros.items())),
              "operatorname_occurrences": occurrences,
              "operatorname_name_counts": dict(Counter(x["name"] for x in occurrences)),
              "literal_render_error_text_present": "macros are not allowed" in paper,
              "other_historical_rejected_fragments_present": {
                  "hline": r"\hline" in paper, "left_brace": r"\left\{" in paper}},
    "observed_rendering": {
        "current_browser_render_performed": False,
        "user_report": "User supplied a browser-style error naming operatorname and said multiple formulas fail.",
        "local_precedent": "Existing phase-one test bans operatorname, hline, and scalable opening event braces; it recommends mathop{text{...}}.",
        "document_scan": "All nine operatorname uses identified; no hline or left-brace occurrence in baseline paper_v2.",
    },
    "recorded_identities": [
        {"label": "Tristan Miano", "role": "Human project originator/director and publisher", "recommendation": "Byline"},
        {"label": "ChatGPT (GPT-6 Astra Pro)", "role": "Explicit v2 F07, F14, F15, ND01, F16, F17 contributions and same-model internal reviews", "recommendation": "Byline"},
        {"label": "Codex (GPT-6)", "role": "Explicit v2 F08-F13, N01/C3/C4 mathematics, implementation and reviews", "recommendation": "Byline; retain recorded label without inferring a more specific GPT-6 version"},
        {"label": "GPT-5.6 Sol", "role": "Phase-one formalism, experiments, audits and writing, explicitly credited in the public adaptation and audit headers", "recommendation": "Byline is supported if inherited phase-one contributions are included; state stage in contribution paragraph"},
        {"label": "Claude Fable 5", "role": "Five signed phase-one external audit records, July 11-21", "recommendation": "Credit explicitly as phase-one auditor; do not imply v2 review. Can be included among model coauthors if the byline expressly includes audit contributions."},
        {"label": "Claude Opus 5", "role": "July 24 phase-one audit's source header; its directory manifest instead says Fable 5", "recommendation": "Credit using exact dated source label and preserve the manifest discrepancy; no unsupported identity merge"},
        {"label": "ChatGPT 5.5 / GPT 5.5", "role": "User-attributed founding conversation ideas mentioned in claude.txt, not a precise assignment of later v2 derivations", "recommendation": "Acknowledge source conversations; insufficient to assign later research or a v2 byline role"},
        {"label": "Earlier Claude/Fable, generation unspecified", "role": "Founding conversation; audit of July 11 says it was an earlier generation", "recommendation": "Acknowledge source conversation without inventing a numbered model"},
    ],
    "model_identity_limit": "These are recorded contributor labels. ChatGPT/Codex are interfaces, and labels do not independently establish distinct weight identities. No model identity is inferred from Git author settings, timestamps, or prose style.",
    "source_bindings": source_bindings,
    "official_renderer_sources": [
        {"url": "https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/writing-mathematical-expressions",
         "retrieval_ref": "turn92view0", "access_date": "2026-10-06", "read_scope": "GitHub Markdown math overview and delimiters",
         "finding": "GitHub documents MathJax-backed mathematics in Markdown. This does not establish its full allowed-macro filter."},
        {"url": "https://docs.mathjax.org/en/latest/input/tex/macros/index.html",
         "retrieval_refs": ["turn92view1", "turn93view0", "turn93view1", "turn93view2"],
         "access_date": "2026-10-06", "read_scope": "Intro and specific macro table rows",
         "finding": "MathJax lists mathop and mathrm as base macros, and operatorname as an ams macro. Host restrictions remain distinct from general MathJax support."},
    ],
    "search_limitations_and_administrative_errors": [
        "Broad attribution regex outputs were clipped; exact relevant headers and passages were reread and are bound here.",
        "A combined read command returned exit 2 because optional guessed F17 presentation/validator globs did not exist; the existing phase-one compatibility test itself was read successfully. No file or experiment was changed by this command.",
    ],
}
target = OUT / "editorial_evidence.json"
with target.open("x", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
    f.write("\n")
print(json.dumps({"status": "saved", "path": str(target.relative_to(ROOT)),
                  "sources": len(source_bindings), "operatorname_occurrences": len(occurrences),
                  "paper_sha256": result["paper"]["sha256"]}))
