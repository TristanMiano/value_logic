"""Reproduce the retained v1 post-assessment arithmetic-bound observation.

Uses frozen review sources and existing run_v1 profile only. Development;
agent time unmeasured, zero principal Research90 credit. Refuses overwrite.
"""
from fractions import Fraction as F
import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("extra_review_v1", HERE / "implementation_probes_v1.py")
M = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = M
SPEC.loader.exec_module(M)


def run():
    profile = M.profile_from_json(M.RUN / "profile_1024.json")
    setup = F(1, (1 << M.C.MAX_ARITHMETIC_BITS) - 159)
    result = M.C.select(profile, profile.scope, M.D.PRICES["high"], 1, setup_to_recover=setup)
    fields = {}
    for name in ("lower_gain_per_query", "conditional_batch_lower_gain", "assessment_cost",
                 "setup_to_recover", "all_in_lower_gain"):
        value = F(result[name])
        fields[name] = dict(numerator_bits=abs(value.numerator).bit_length(),
                            denominator_bits=value.denominator.bit_length())
    return dict(accepted_setup_components_within_cap=max(setup.numerator.bit_length(),
        setup.denominator.bit_length()) <= M.C.MAX_ARITHMETIC_BITS,
        declared_arithmetic_component_cap=M.C.MAX_ARITHMETIC_BITS, output_component_bits=fields,
        reported_assessment_units=result["meter"]["total"], source="source_snapshot_v1/07_paid_reasoning.py",
        scope="Focused valid-input arithmetic-bound observation; no broad rerun",
        principal_research90_credit_seconds=0)


if __name__ == "__main__":
    result = run()
    with (HERE / "post_assessment_arithmetic_probe_v1.json").open("x") as stream:
        stream.write(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps(result, sort_keys=True, indent=2))
