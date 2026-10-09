"""Two targeted development witnesses for nonvacuity conditions.

Questions fixed before execution: can a zero bisection allowance alone guarantee
scalar calibration; can unbounded delayed-copy allocation preserve a useful
normalized rate? These are deterministic witnesses, not final evaluations.
Contributor: ChatGPT (GPT-6 Astra Pro), independent implementation reviewer.
"""
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import sys
import time

sys.dont_write_bytecode = True
here = Path(__file__).resolve().parent
source = here.parent / 'preserved_rerun_v1/defensive_forecasting.py'
target = here / 'boundary_witnesses_result.json'
if target.exists():
    raise SystemExit('Refusing to overwrite an existing boundary result.')
spec = importlib.util.spec_from_file_location('boundary_defensive_forecasting', source)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
start = time.monotonic_ns()
start_utc = datetime.now(timezone.utc).isoformat()
horizon = 64

# With a fixed half expert and only middle-bin occupancy, endpoint scores keep
# their valid bracket. Zero bisections always returns half despite all-zero labels.
f = module.Forecaster(('half',), bins=2)
trajectory = []
for t in range(horizon):
    pred = f.issue('budget-zero-' + str(t), {'half': F(1, 2)}, max_bisections=0)
    trajectory.append({'p': str(pred.probability), 'score': str(pred.score),
                       'allowance': str(pred.allowance), 'tolerance_met': pred.tolerance_met})
    f.reveal(pred.query, 0)
budget = {'rounds': horizon, 'weight_total': horizon, 'trajectory': trajectory,
          'middle_bin_residual': str(f.residual[2]),
          'variance': str(f.variance), 'allowance': str(f.allowance),
          'bound_squared': str(f.variance + f.allowance),
          'own_loss': str(f.own_loss),
          'normalized_middle_bin_absolute_residual': str(abs(f.residual[2]) / horizon)}
assert all(row['p'] == '1/2' for row in trajectory)
assert f.variance == F(horizon, 4)
assert f.allowance == F(horizon * (horizon - 1), 4)
assert f.residual[2] == -F(horizon, 2)

# All forecasts are issued first, and all labels are disclosed afterward.
# A zero settled bound before disclosure says nothing about the pending population.
pool = module.DelayedPool(('zero', 'one'), bins=2)
delayed_predictions = []
for t in range(horizon):
    delayed_predictions.append(pool.issue('late-' + str(t), {'zero': 0, 'one': 1}))
before = pool.audit()
for pred in delayed_predictions:
    pool.reveal(pred.query, 0)
after = pool.audit()
own = sum((copy.own_loss for copy in pool.copies), F(0))
expert_zero = sum((copy.expert_losses[0] for copy in pool.copies), F(0))
delayed = {'rounds': horizon, 'weight_total': horizon,
           'all_forecasts_are_half': all(pred.probability == F(1, 2) for pred in delayed_predictions),
           'before_any_label': before, 'after_all_labels': after,
           'own_loss': own, 'zero_expert_loss': expert_zero,
           'normalized_expert_regret': (own - expert_zero) / horizon,
           'normalized_middle_bin_absolute_residual': abs(after['residual'][3]) / horizon}
assert before['settled'] == 0 and before['pending'] == horizon and before['bound_squared'] == 0
assert after['settled'] == horizon and after['pending'] == 0 and after['copies'] == horizon
assert own == F(horizon, 4) and expert_zero == 0
assert after['bound_squared'] == F(3 * horizon * horizon, 8)

result = {'schema': 'value_logic.p306.independent_boundary_witnesses.v1', 'status': 'PASS',
          'start_utc': start_utc, 'end_utc': datetime.now(timezone.utc).isoformat(),
          'execution_ns': time.monotonic_ns() - start, 'python': platform.python_version(),
          'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
          'audit_source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
          'zero_root_budget': budget, 'unbounded_copy_count': delayed,
          'interpretation': ['A fixed root work cap does not itself make the cumulative allowance negligible.',
              'Without a copy-count/feedback condition, complete eventual labels still allow linear regret.',
              'An intermediate zero certificate for the empty settled set gives no pending-population conclusion.'],
          'contributor': 'ChatGPT (GPT-6 Astra Pro), independent implementation reviewer',
          'research_time_credit_ns': 0, 'scope': 'Deterministic development witnesses, no historical clock credit.'}
target.write_text(json.dumps(result, indent=2, default=str) + '\n')
print(json.dumps({'status': result['status'], 'result': str(target), 'execution_ns': result['execution_ns']}))
