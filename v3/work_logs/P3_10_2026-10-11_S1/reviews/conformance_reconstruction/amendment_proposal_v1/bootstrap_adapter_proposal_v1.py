"""Proposed external P3-10 conformance bootstrap amendment; NOT EXECUTED.

Contributor: ChatGPT (GPT-6 Astra Pro), /root/conformance_reconstruction.
The caller must use a new, explicitly bound amendment lineage and unchanged
sealed inputs. This helper never changes a frozen file or monkey-patches a
module. Its initialization placement matches the old run_development wrapper.
This is external orchestration, outside the unchanged STRUCTURAL-VM worker.
"""

def run_with_explicit_bootstrap(original_adapter, unit, public_input, config):
    if unit["engine"] == "legacy_structural":
        legacy = original_adapter._load("v3/experiments/p308_structural.py")
        legacy._load_legacy()
        if legacy.M is None or legacy.K is None:
            raise RuntimeError("Structural dependency bootstrap did not complete.")
    return original_adapter.run(unit, public_input, config)
