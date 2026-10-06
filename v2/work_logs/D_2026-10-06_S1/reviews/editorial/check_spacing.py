"""Review the one final TeX thin-space change; no scientific execution."""

from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import time


ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent / "local_tex_spacing_check"
OLD_SHA = "38d6330a07ebb86615b11b00c507c03f609d401c3c2478086edd669770b6beef"
NEW_SHA = "c8f490ce94584fc93d27b759f1f524d5eeeb0d3885729d24db413cb4f5205c5d"
old = r"\sup_{D_{\mathcal C}}\mathrm{res}"
new = r"\sup_{D_{\mathcal C}}\,\mathrm{res}"
paper = (ROOT / "paper_v2.md").read_text()
assert sha256(paper.encode()).hexdigest() == NEW_SHA
assert paper.count(new) == 1
assert sha256(paper.replace(new, old).encode()).hexdigest() == OLD_SHA
expression = next(x.strip() for x in re.findall(r"(?s)\$\$(.*?)\$\$", paper) if new in x)
tex = r"""\documentclass[11pt]{article}
\usepackage[T1]{fontenc}
\usepackage{amsmath,amssymb}
\usepackage[letterpaper,margin=0.75in]{geometry}
\begin{document}
\section*{Gate D: final operator spacing}
The only change after the all-math compilation is one thin space before the residual name.
\[
""" + expression + "\n\\]\n\\end{document}\n"
OUT.mkdir(exist_ok=False)
tmp = Path(tempfile.mkdtemp(prefix="value_logic_gate_d_spacing_"))
source = tmp / "spacing_specimen.tex"
source.write_text(tex)
(OUT / "spacing_specimen.tex").write_text(tex)
command = ["pdflatex", "-no-shell-escape", "-interaction=nonstopmode", "-halt-on-error",
           f"-output-directory={tmp}", str(source)]
start_utc = datetime.now(timezone.utc).isoformat()
start_ns = time.monotonic_ns()
run = subprocess.run(command, cwd=tmp, capture_output=True, text=True)
end_ns = time.monotonic_ns()
end_utc = datetime.now(timezone.utc).isoformat()
(OUT / "renderer.stdout.txt").write_text(run.stdout)
(OUT / "renderer.stderr.txt").write_text(run.stderr)
log = tmp / "spacing_specimen.log"
if log.exists():
    shutil.copyfile(log, OUT / "spacing_specimen.log")
pdf = tmp / "spacing_specimen.pdf"
png = tmp / "spacing_specimen.png"
raster_command = ["pdftoppm", "-f", "1", "-singlefile", "-r", "120", "-png", str(pdf), str(png.with_suffix(""))]
raster = subprocess.run(raster_command, cwd=tmp, capture_output=True, text=True) if run.returncode == 0 else None
if raster:
    (OUT / "raster.stdout.txt").write_text(raster.stdout)
    (OUT / "raster.stderr.txt").write_text(raster.stderr)
result = {
    "schema": "Gate-D-final-spacing-check-v1",
    "contributor": "ChatGPT (GPT-6 Astra Pro), delegated editorial reviewer",
    "principal_concurrent_credit_minutes": 0,
    "previous_paper_sha256": OLD_SHA, "paper_sha256": NEW_SHA,
    "only_change": {"before": old, "after": new, "count": 1},
    "previous_snapshot_exactly_recovered_by_reversal": True,
    "equation": expression,
    "renderer": {"command": command, "cwd": str(tmp), "returncode": run.returncode,
                 "start_utc": start_utc, "end_utc": end_utc,
                 "wall_seconds": (end_ns-start_ns)/1e9,
                 "tex_sha256": sha256(tex.encode()).hexdigest(),
                 "pdf_path": str(pdf) if pdf.exists() else None,
                 "pdf_sha256": sha256(pdf.read_bytes()).hexdigest() if pdf.exists() else None},
    "raster": {"command": raster_command, "returncode": raster.returncode if raster else None,
               "png_path": str(png) if png.exists() else None,
               "png_sha256": sha256(png.read_bytes()).hexdigest() if png.exists() else None},
    "visual_inspection": "Pending explicit image inspection; not claimed by this script.",
    "full_compilation_repeated": False, "github_render_claimed": False,
}
(OUT / "check_result.json").write_text(json.dumps(result, indent=2)+"\n")
print(json.dumps({"returncode": run.returncode, "raster_returncode": raster.returncode if raster else None,
                  "png_path": str(png), "record": str(OUT/"check_result.json")}))
raise SystemExit(run.returncode or (raster.returncode if raster else 1))
