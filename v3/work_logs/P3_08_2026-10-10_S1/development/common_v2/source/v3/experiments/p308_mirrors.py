"""Executable ordinary representation controls. P3-08 DEVELOPMENT.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-10.
For binary unit loss, a marginal q gives task-cost coordinates (q,1-q).
An ordinary controller may use exactly the same randomized policy, finite
update and hard-answer implementation. This wrapper performs that identical
program. It is not an independent algorithm or an extra statistical trial.
The cost-coordinate interpretation requires no additional emitted service.
"""
from p308_broker import execute

VERSION = "p308-ordinary-mirror-v1"


def run_ordinary_mixture(service, tape, contract, **kwargs):
    """Same paid kernel, with the elementary ordinary marginal-cost meaning."""
    return execute(service, tape, contract, **kwargs)
