"""Disjoint DEVELOPMENT gate-clause checks; no population constructor calls.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-11.
The only imported constructor used is the Boolean gate's local clause encoder.
No _gate_query, mixed generator, final family, policy, or private scorer runs.
"""
from pathlib import Path
import hashlib
import itertools
import json
import sys

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "v3/experiments"))
import p309_broker as B


def main():
    rows = []
    operations = {"and": lambda a, b: a and b, "or": lambda a, b: a or b,
                  "xor": lambda a, b: a != b}
    for name, operation in operations.items():
        for a, b in itertools.product((-2, -1, 1, 2), repeat=2):
            clauses = B._gate_clauses(name, a, b, 3)
            for bits in itertools.product((False, True), repeat=3):
                def literal(x):
                    return bits[abs(x) - 1] if x > 0 else not bits[abs(x) - 1]
                cnf = all(any(literal(x) for x in clause) for clause in clauses)
                reference = bits[2] == operation(literal(a), literal(b))
                rows.append({"operation": name, "a": a, "b": b, "bits": list(map(int, bits)),
                             "cnf": cnf, "reference": reference, "pass": cnf == reference})
    assert len(rows) == 384 and all(row["pass"] for row in rows)
    result = {"stage": "DEVELOPMENT", "status": "PASS", "final_population_generated": False,
        "adapter_sha256": hashlib.sha256(Path(B.__file__).read_bytes()).hexdigest(),
        "checks": len(rows), "rows": rows,
        "scope": "Local AND/OR/XOR clauses with signed, aliased and complementary inputs; fresh output coordinate only.",
        "excluded": "No twelve-variable circuit or final-family instance, seed draw, final generator, paid policy, certificate family or private final scorer."}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
