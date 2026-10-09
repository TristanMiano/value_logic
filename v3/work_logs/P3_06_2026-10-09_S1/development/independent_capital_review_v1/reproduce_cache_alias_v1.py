"""Preserved pre-repair cache type aliasing; development, zero principal time."""
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
SOURCE = HERE / 'source_snapshot/06_capital_forecasting.py'
SPEC = importlib.util.spec_from_file_location('independent_old_capital', SOURCE)
CORE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = CORE
SPEC.loader.exec_module(CORE)


def main():
    rows = []
    for x, bits, alias, alias_bits in (
        (F(2), 16, 2.0, 16), (F(1), 16, True, 16), (F(2), 16, F(2), 16.0)
    ):
        CORE.log_upper.cache_clear()
        baseline = CORE.log_upper(x, bits)
        returned = CORE.log_upper(alias, alias_bits)
        assert returned == baseline
        assert CORE.log_upper.cache_info().hits == 1
        rows.append({'invalid_x': repr(alias), 'invalid_bits': repr(alias_bits),
                     'wrongly_accepted_cache_hit': True})
    result = {'status': 'REPRODUCED_PRE_REPAIR_VALIDATION_DEFECT',
              'source_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
              'principal_research90_seconds': 0, 'cases': rows}
    path = HERE / 'cache_alias_reproduction.json'
    with path.open('x') as handle:
        json.dump(result, handle, indent=2)
        handle.write('\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
