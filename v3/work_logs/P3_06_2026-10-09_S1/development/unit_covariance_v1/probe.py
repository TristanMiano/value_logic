"""Exact episode unit-covariance probe. ChatGPT (GPT-6 Astra Pro), 2026-10-09.

Reads fixed public issue/admission prefixes; no private pending label input.
This is a new finite property check, not a new forecast method or tuning run.
"""
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
SESSION = HERE.parents[1]


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    sys.modules[name] = value
    spec.loader.exec_module(value)
    return value


def main():
    target = HERE / 'result.json'
    if target.exists():
        raise SystemExit('Preserve the existing result.')
    start, utc = time.perf_counter_ns(), datetime.now(timezone.utc).isoformat()
    plan = json.loads((HERE / 'plan.json').read_text())
    replay = module('p306_unit_replay', ROOT / 'v3/checks/06_price_replay.py')
    capital = module('p306_unit_capital', ROOT / 'v3/checks/06_capital_forecasting.py')
    core = replay.CORE
    checks, results, inputs = Counter(), [], {}

    def check(value, name):
        checks[name] += 1
        if not value:
            raise AssertionError(name)

    for case_name in plan['cases']:
        path = SESSION / 'development/mathematical_queries_v1' / (case_name + '.json')
        case = json.loads(path.read_text())
        inputs[str(path.relative_to(ROOT))] = hashlib.sha256(path.read_bytes()).hexdigest()
        tape = [e for e in replay.public_projection(case) if e['tick'] <= plan['prefix_issue_ticks']]
        scope = tape[0]['query']['scope']
        wmax = F(8 if case_name == 'delayed_pending_tail' else 1)
        for profile in plan['profiles']:
            u, v = F(profile['u']), F(profile['v'])
            old_pools = {d: core.DelayedPool(replay.EXPERTS, scope=scope, decision_features=d) for d in (False, True)}
            new_pools = {d: core.DelayedPool(replay.EXPERTS, scope=scope, decision_features=d, gamma=1/v) for d in (False, True)}
            old_caps, new_caps, cap_pending = [], [], {}
            moduli, residues, issues = Counter(), Counter(), {}
            issued, admitted, cap_records = 0, 0, []
            for event in tape:
                if event['kind'] == 'issue':
                    query, tick = event['query'], event['tick']
                    identity, w = query['query_id'], F(event['weight'])
                    qs = replay.expert_values(query, moduli, residues)
                    rows = tuple(tuple(F(x) for x in row) for row in event['actions']['rows'])
                    eta = F(event['actions']['eta'])
                    g = (F(1000 + tick), F(-2000 + 2*tick)) if profile['offset'] else (F(0), F(0))
                    new_rows = tuple(tuple(v*row[y] + g[y] for y in (0,1)) for row in rows)
                    old_table, new_table = core.ActionTable(rows, eta), core.ActionTable(new_rows, v*eta)
                    for decision in (False, True):
                        old = old_pools[decision].issue(identity, qs, w, F(1,4096), actions=old_table if decision else None)
                        new = new_pools[decision].issue(identity, qs, u*w, u*u*F(1,4096), actions=new_table if decision else None)
                        check(old.probability == new.probability, 'polynomial report covariance')
                        check(new.features == tuple(u*x for x in old.features), 'feature covariance')
                        check(new.score == u*u*old.score and new.allowance == u*u*old.allowance, 'score and allowance covariance')
                        check(new.lipschitz_bound == u*u*old.lipschitz_bound, 'score Lipschitz covariance')
                        check((new.bisections,new.score_evaluations,new.sufficient_bisections,new.tolerance_met)==
                              (old.bisections,old.score_evaluations,old.sufficient_bisections,old.tolerance_met), 'search control covariance')
                        check(new.action_one_probability == old.action_one_probability, 'polynomial action covariance')
                    free = next((i for i,c in enumerate(old_caps) if c.pending is None),None)
                    if free is None:
                        free = len(old_caps)
                        old_caps.append(capital.CapitalForecaster(replay.EXPERTS,16,wmax,6,scope=scope))
                        new_caps.append(capital.CapitalForecaster(replay.EXPERTS,16,u*wmax,v*6,scope=scope))
                    old = old_caps[free].issue(identity,qs,w,rows=rows,eta=eta)
                    new = new_caps[free].issue(identity,qs,u*w,rows=new_rows,eta=v*eta)
                    check(old.probability == new.probability and old.action_one_probability == new.action_one_probability,
                          'capital scalar and action invariance')
                    check(old.logs_by_outcome == new.logs_by_outcome, 'capital log increments invariant for both outcomes')
                    check((old.capital_before_interval,old.capital_after_intervals,old.capital_allowance)==
                          (new.capital_before_interval,new.capital_after_intervals,new.capital_allowance), 'capital enclosure and allowance invariance')
                    check((old.bisections,old.capital_evaluations,old.max_enclosure_bits,old.allowance_met)==
                          (new.bisections,new.capital_evaluations,new.max_enclosure_bits,new.allowance_met), 'capital search control invariance')
                    cap_pending[identity] = free
                    issues[identity] = query
                    cap_records.append({'query':identity,'p':str(old.probability),'copy':free})
                    issued += 1
                else:
                    identity, y = event['query_id'], event['answer']
                    for decision in (False,True):
                        old_pools[decision].reveal(identity,y,scope=scope)
                        new_pools[decision].reveal(identity,y,scope=scope)
                        check(old_pools[decision].pending == new_pools[decision].pending,'pending copy mapping invariant')
                        for a,b in zip(old_pools[decision].copies,new_pools[decision].copies):
                            a,b=a.accumulator,b.accumulator
                            check(b.residual==tuple(u*x for x in a.residual),'residual state covariance')
                            check(b.variance==u*u*a.variance and b.allowance==u*u*a.allowance,'raw per-copy budget covariance')
                            check(b.own_loss==u*a.own_loss and b.weight==u*a.weight,'Brier and weight covariance')
                            if decision:
                                check(b.smoothing_slack==u*v*a.smoothing_slack,'weighted smoothing covariance')
                                check(all(b.mixed_action_loss-b.action_losses[i]==u*v*(a.mixed_action_loss-a.action_losses[i]) for i in (0,1)),
                                      'common offset cancels from action regret')
                    free = cap_pending.pop(identity)
                    old_caps[free].reveal(identity,y,scope=scope)
                    new_caps[free].reveal(identity,y,scope=scope)
                    a,b = old_caps[free].audit(),new_caps[free].audit()
                    check(a['state']['logs']==b['state']['logs'] and a['capital_bound']==b['capital_bound'],'settled capital invariant')
                    check(b['expert_regret_upper']==u*a['expert_regret_upper'],'capital expert certificate covariance')
                    check(b['calibration_absolute_upper']==tuple(u*x for x in a['calibration_absolute_upper']),'capital calibration certificate covariance')
                    check(b['mixed_action_regret_upper']==tuple(u*v*x for x in a['mixed_action_regret_upper']),'capital action certificate covariance')
                    q=issues[identity]
                    moduli[q['m']] += 1
                    residues[q['m'],event['residue']] += 1
                    admitted += 1
            results.append({'case':case_name,'profile':profile,'issued':issued,'admitted':admitted,
                'pending':len(cap_pending),'capital_reports':cap_records})
    source_paths=[HERE/'plan.json',Path(__file__),ROOT/'v3/checks/06_price_replay.py',
                  ROOT/'v3/checks/06_defensive_forecasting.py',ROOT/'v3/checks/06_capital_forecasting.py']
    result={'status':'PASS','stage':plan['stage'],'started_utc':utc,'elapsed_wall_ns':time.perf_counter_ns()-start,
        'checks':dict(checks),'assertions':sum(checks.values()),'cases':results,'inputs_sha256':inputs,
        'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in source_paths}}
    target.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status','assertions','elapsed_wall_ns')}))


if __name__=='__main__':
    main()
