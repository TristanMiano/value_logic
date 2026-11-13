"""Cross-check reported summaries from saved per-run evidence. Codex (GPT-6)."""
import json
import math
from pathlib import Path
import statistics

ROOT=Path(__file__).parent


def close(a,b):
    assert math.isclose(a,b,rel_tol=1e-11,abs_tol=1e-13),(a,b)


def mean_se(values):
    return statistics.mean(values),statistics.stdev(values)/math.sqrt(len(values))


def check_finite(obj):
    if isinstance(obj,float):
        assert math.isfinite(obj)
    elif isinstance(obj,dict):
        for v in obj.values():check_finite(v)
    elif isinstance(obj,list):
        for v in obj:check_finite(v)


def main():
    json_files=0
    for p in ROOT.glob('*.json'):
        if p.stem=='verify_report':continue
        obj=json.loads(p.read_text(encoding='utf-8',newline='\n'))
        check_finite(obj)
        json_files+=1
    boundary=json.loads((ROOT/'boundary_concepts.json').read_text())
    checks=0
    for row in boundary['summary']:
        group=[r for r in boundary['runs'] if r['common_goal_probability']==row['common_goal_probability'] and r['horizon']==row['horizon']]
        assert len(group)==64
        assert row['optimal_partition_count']==sum(r['optimal_partition'] for r in group)
        for category,n in row['category_counts'].items():
            assert n==sum(r['category']==category for r in group)
        for key in ('deployment_regret','whole_run_net','realized_net','purchased_outcomes'):
            values=[statistics.mean(r[key] for r in group if r['replica']==i) for i in range(32)]
            m,se=mean_se(values)
            close(m,row[key]['mean']);close(se,row[key]['standard_error']);checks+=2
    selective=json.loads((ROOT/'selective_concepts.json').read_text())
    forced=json.loads((ROOT/'learned_concepts.json').read_text())
    old={(r['common_goal_probability'],r['replica'],r['agent']):r for r in forced['final_runs']}
    final=max(r['horizon'] for r in selective['summary'])
    for row in selective['summary']:
        if row['horizon']!=final:continue
        group=[r for r in selective['final_runs'] if r['common_goal_probability']==row['common_goal_probability'] and r['method']==row['method']]
        assert len(group)==64
        for r in group:
            baseline=old[(r['common_goal_probability'],r['replica'],r['agent'])]
            close(r['paired_gain_over_forced'],r['whole_run_population_net']-(r['oracle_net']-baseline['mean_population_regret']))
            checks+=1
        for key in ('whole_run_population_net','realized_net_per_opportunity','paired_gain_over_forced'):
            values=[statistics.mean(r[key] for r in group if r['replica']==i) for i in range(32)]
            m,se=mean_se(values)
            close(m,row[key]['mean']);close(se,row[key]['standard_error']);checks+=2
    # A second exact algebra implementation checks the new inverse-value
    # witness, including its stated determinant order.
    import sympy as sp
    queries=json.loads((ROOT/'value_queries.json').read_text())
    exact=0
    for name in ('witness','four_state_witness'):
        w=queries[name];gamma=sp.Rational(w['gamma'])
        kernels=[sp.Matrix([[sp.Rational(x) for x in row] for row in k]) for k in w['action_kernels']]
        reward=sp.Matrix([sp.Rational(x) for x in w['reward']]);n=len(reward)
        values=[sp.Matrix([sp.Rational(x) for x in row]) for row in w['values']]
        for choices,v in zip(w['policies'],values):
            transition=sp.Matrix([list(kernels[choices[i]].row(i)) for i in range(n)])
            assert (sp.eye(n)-gamma*transition)*v==reward
            exact+=1
        for i in range(n):
            rows=[[int(a==b) for a in range(2) for j in range(n)] for b in range(2)]
            rhs=[sp.Integer(1),sp.Integer(1)]
            for choices,v in zip(w['policies'],values):
                rows.append([int(choices[i]==a)*v[j] for a in range(2) for j in range(n)])
                rhs.append((v[i]-reward[i])/gamma)
            matrix=sp.Matrix(rows)
            assert matrix.det()==sp.Rational(w['exact_determinants'][i])
            recovered=matrix.inv()*sp.Matrix(rhs)
            assert recovered==sp.Matrix([kernels[a][i,j] for a in range(2) for j in range(n)])
            exact+=2
    out={'status':'passed','finite_json_files':json_files,'independent_summary_comparisons':checks,
         'independent_sympy_equalities':exact}
    (ROOT/'verify_report.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(out))


if __name__=='__main__':main()
