"""Reproduce the post-outcome mathematical illustration, not a model score.

Contributor: ChatGPT (GPT-6 Astra Pro), October 5, 2026.
The first calculation was made inline before this reproducibility wrapper
was saved. --check preserves its original JSON bytes and SHA sidecar.
"""
import hashlib
import json
import math
from fractions import Fraction as F
from pathlib import Path
import sys

p = Path(__file__).resolve().parent
x = F(4, 25)
single_bound = (1 / (1 - x)) / (1 + 1 / (1 - x)) - F(1, 2)
joint_bound = (1 + 2 * x) / (2 + 2 * x) - F(1, 2)
assert single_bound == F(1, 23) < F(1, 20) < F(2, 29) == joint_bound
value = {
    "schema": "ND01-interpretive-toy-tolerance-v1",
    "development_only": True,
    "not_a_saved_F15_network": True,
    "saved_model_forwards": 0,
    "new_populations": 0,
    "new_fits": 0,
    "case": "h(t)=(t,t,2t),v=(1,1,-1),t in[0,4/25],targetlogit0;two disjoint coordinate edits",
    "single_uniform_probability_error_upper_bound_exact": str(single_bound),
    "joint_witness_probability_error_lower_bound_exact": str(joint_bound),
    "illustrative_point_tolerance_exact": "1/20",
    "single_extremal_error_float": 1 / (1 + math.exp(-float(x))) - .5,
    "joint_witness_error_float": 1 / (1 + math.exp(-float(2 * x))) - .5,
    "derivation_sha256": hashlib.sha256((p / "joint_semantic_error.md").read_bytes()).hexdigest(),
    "not_frozen_endpoint_amendment": True,
}
q = p / "joint_semantic_error_example.json"
encoded = (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()
if sys.argv[1:] == ["--check"]:
    assert q.read_bytes() == encoded
    assert Path(str(q) + ".sha256").read_text().strip() == hashlib.sha256(encoded).hexdigest()
    print("Interpretive tolerance example reproduced byte for byte; no saved model evaluation.")
else:
    assert not sys.argv[1:]
    with q.open("xb") as handle:
        handle.write(encoded)
    with Path(str(q) + ".sha256").open("x") as handle:
        handle.write(hashlib.sha256(encoded).hexdigest() + "\n")
