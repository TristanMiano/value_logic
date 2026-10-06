"""Gate D editorial source comparison and local math-only TeX rendering.

Contributor: ChatGPT (GPT-6 Astra Pro), delegated editorial reviewer.
No experiment is run. Binary renderer products stay in a new /tmp directory.
This checks local TeX, not the live GitHub renderer.
"""

from collections import Counter
from datetime import datetime, timezone
from difflib import SequenceMatcher
from hashlib import sha256
import json
from pathlib import Path
import re
import resource
import shutil
import subprocess
import tempfile
import time
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent
BASE = "f7aa0bef07cb21da9336429426244f6e944644a4"
PAPER_SHA = "38d6330a07ebb86615b11b00c507c03f609d401c3c2478086edd669770b6beef"
README_SHA = "29aa47baadbcbec9fc1b1909808eb07a70c41d459529d345af88692d0f265570"


def digest(data):
    return sha256(data).hexdigest()


def extract_math(text):
    """Dollar extraction for this document, with its sole code fence removed."""
    masked = re.sub(r"(?ms)^```[^\n]*\n.*?^```[^\n]*$",
                    lambda m: "".join("\n" if c == "\n" else " " for c in m[0]), text)
    assert not re.search(r"`[^`\n]*\$[^`\n]*`", masked), "Unexpected code-span dollar"
    pattern = re.compile(r"\$\$([\s\S]*?)\$\$|\$([^$\n]+)\$")
    entries = []
    for m in pattern.finditer(masked):
        entries.append({
            "index": len(entries)+1,
            "line": text.count("\n", 0, m.start())+1,
            "display": m[1] is not None,
            "tex": (m[1] if m[1] is not None else m[2]).strip(),
        })
    assert "$" not in pattern.sub("", masked), "Unmatched or unhandled dollar"
    return entries


def normalize_operator(tex):
    value = re.sub(r"\\operatorname\{([^{}]+)\}", r"\\mathrm{\1}", tex)
    return value.replace(r"\mathrm{rank}T", r"\mathrm{rank}\,T").replace(
        r"\mathrm{rank}Q", r"\mathrm{rank}\,Q")


def anchors(path):
    text = path.read_text()
    found = set(re.findall(r'<a\s+id="([^"]+)"', text))
    counts = Counter()
    for heading in re.findall(r"(?m)^#{1,6}\s+(.+?)\s*#*$", text):
        heading = re.sub(r"\[([^]]+)\]\([^)]*\)", r"\1", heading)
        heading = heading.replace("`", "").replace("*", "").lower()
        slug = "".join(c for c in heading if c.isalnum() or c in " _-").replace(" ", "-")
        suffix = counts[slug]
        counts[slug] += 1
        found.add(slug if not suffix else f"{slug}-{suffix}")
    return found


paper_bytes = (ROOT/"paper_v2.md").read_bytes()
readme_bytes = (ROOT/"README.md").read_bytes()
assert digest(paper_bytes) == PAPER_SHA, "Paper differs from assigned snapshot"
assert digest(readme_bytes) == README_SHA, "README differs from assigned snapshot"
paper = paper_bytes.decode()
readme = readme_bytes.decode()
baseline = subprocess.check_output(["git", "show", f"{BASE}:paper_v2.md"], cwd=ROOT).decode()
old_math = extract_math(baseline)
new_math = extract_math(paper)
old_normalized = [normalize_operator(x["tex"]) for x in old_math]
new_values = [x["tex"] for x in new_math]
differences = []
for op, a, b, c, d in SequenceMatcher(a=old_normalized, b=new_values, autojunk=False).get_opcodes():
    if op != "equal":
        differences.append({"operation": op, "baseline": old_math[a:b], "current": new_math[c:d]})
assert len(differences) == 1 and differences[0]["operation"] == "insert"
assert [x["tex"] for x in differences[0]["current"]] == ["c", "d"], differences
assert r"\operatorname" not in paper
assert r"\hline" not in paper and r"\left\{" not in paper
old_operators = Counter(re.findall(r"\\operatorname\{([^{}]+)\}", baseline))
new_operators = Counter(re.findall(r"\\mathrm\{([^{}]+)\}", paper))
assert dict(old_operators) == {"res": 5, "convert": 1, "rank": 2, "logit": 1}
assert dict(new_operators) == dict(old_operators)

byline = "Tristan Miano · ChatGPT (GPT-6 Astra Pro) · Codex (GPT-6) · GPT-5.6 Sol"
assert paper.splitlines()[2] == byline
readme_links = []
for label, target in re.findall(r"\[([^]\n]+)\]\(([^)\n]+)\)", readme):
    parts = urlsplit(target)
    assert not parts.scheme, "README external links require separate network review"
    path = ROOT / unquote(parts.path) if parts.path else ROOT / "README.md"
    item = {"label": label, "target": target, "exists": path.exists()}
    if parts.fragment:
        item["anchor_exists"] = unquote(parts.fragment) in anchors(path)
    assert item["exists"] and item.get("anchor_exists", True), item
    item["tracked_at_base"] = subprocess.run(
        ["git", "ls-tree", "--name-only", BASE, "--", str(path.relative_to(ROOT))],
        cwd=ROOT, capture_output=True, text=True).stdout.strip() != ""
    readme_links.append(item)
scaffolding = re.findall(r"F(?:0[1-9]|1[0-7])\b|POST-B-1|engaged minutes|\bGate [A-D]\b|\bD60\b|\bE60\b|\bResearch90\b", readme)
assert not scaffolding, scaffolding

attempt = OUT / "local_tex_attempt1"
attempt.mkdir(exist_ok=False)
tmp = Path(tempfile.mkdtemp(prefix="value_logic_gate_d_math_"))
selected = [x for x in new_math if re.search(r"\\mathrm\{(?:res|convert|rank|logit)\}", x["tex"])]
assert len(selected) == 7
header = r"""\documentclass[11pt]{article}
\usepackage[T1]{fontenc}
\usepackage{amsmath,amssymb}
\usepackage[letterpaper,margin=0.75in]{geometry}
\setlength{\parindent}{0pt}
\setlength{\parskip}{5pt}
\begin{document}
\section*{Gate D: corrected operator expressions}
Local TeX specimen from the assigned report snapshot. This is not a GitHub rendering check.
"""
chunks = [header]
for item in selected:
    chunks.append(f"Source line {item['line']}, segment {item['index']}.\n")
    chunks.append("\\[\n" + item["tex"] + "\n\\]\n")
chunks.append("\\clearpage\n\\section*{All extracted mathematical segments}\n")
for item in new_math:
    chunks.append(f"\\textbf{{Segment {item['index']}}} (source line {item['line']})\\par\n")
    chunks.append(("\\[\n"+item["tex"]+"\n\\]\n") if item["display"]
                  else ("\\( "+item["tex"]+" \\)\\par\n"))
chunks.append("\\end{document}\n")
tex = "".join(chunks)
specimen = tmp / "math_specimen.tex"
specimen.write_text(tex)
(attempt / "math_specimen.tex").write_text(tex)
cmd = ["pdflatex", "-no-shell-escape", "-interaction=nonstopmode", "-halt-on-error",
       f"-output-directory={tmp}", str(specimen)]
version_cmd = ["pdflatex", "--version"]
version = subprocess.run(version_cmd, text=True, capture_output=True, cwd=tmp)
(attempt / "renderer_version.stdout.txt").write_text(version.stdout)
(attempt / "renderer_version.stderr.txt").write_text(version.stderr)
begin_utc = datetime.now(timezone.utc).isoformat()
begin_ns = time.monotonic_ns()
before = resource.getrusage(resource.RUSAGE_CHILDREN)
run = subprocess.run(cmd, cwd=tmp, capture_output=True, text=True)
after = resource.getrusage(resource.RUSAGE_CHILDREN)
end_ns = time.monotonic_ns()
end_utc = datetime.now(timezone.utc).isoformat()
(attempt / "renderer.stdout.txt").write_text(run.stdout)
(attempt / "renderer.stderr.txt").write_text(run.stderr)
log = tmp / "math_specimen.log"
if log.exists():
    shutil.copyfile(log, attempt / "math_specimen.log")
pdf = tmp / "math_specimen.pdf"
record = {
    "schema": "Gate-D-settled-editorial-check-v1",
    "contributor": "ChatGPT (GPT-6 Astra Pro), delegated editorial reviewer",
    "principal_concurrent_credit_minutes": 0,
    "base_commit": BASE,
    "paper_sha256": PAPER_SHA,
    "readme_sha256": README_SHA,
    "baseline_math_segments": len(old_math), "current_math_segments": len(new_math),
    "current_math_counts": dict(Counter("display" if x["display"] else "inline" for x in new_math)),
    "operatorname_replacements": dict(old_operators),
    "math_difference_after_declared_typographic_substitution": differences,
    "math_diff_disposition": "All prior mathematical segments preserved after the nine macro substitutions and rank spacing. Two new inline symbols c and d make the attempt-price-vector hypothesis explicit.",
    "byline": byline,
    "readme_links": readme_links,
    "readme_scaffolding_matches": scaffolding,
    "renderer": {"version_command": version_cmd, "command": cmd, "cwd": str(tmp),
                 "start_utc": begin_utc, "end_utc": end_utc,
                 "wall_seconds": (end_ns-begin_ns)/1e9,
                 "child_user_seconds": after.ru_utime-before.ru_utime,
                 "child_system_seconds": after.ru_stime-before.ru_stime,
                 "returncode": run.returncode,
                 "tex_sha256": digest(tex.encode()),
                 "pdf_path": str(pdf) if pdf.exists() else None,
                 "pdf_sha256": digest(pdf.read_bytes()) if pdf.exists() else None,
                 "not_github_renderer": True},
    "representative_math_segments": selected,
    "visual_inspection": "Pending explicit PDF-page image inspection; not claimed by this script.",
}
(attempt / "check_result.json").write_text(json.dumps(record, ensure_ascii=False, indent=2)+"\n")
print(json.dumps({"returncode": run.returncode, "math_segments": len(new_math),
                  "readme_links": len(readme_links), "record": str(attempt/"check_result.json"),
                  "pdf_path": str(pdf) if pdf.exists() else None}))
raise SystemExit(run.returncode)
