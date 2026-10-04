"""Generate F13 exact development evidence; no held-out or novelty claim."""
import argparse
from fractions import Fraction as Q
from itertools import product
import json
from pathlib import Path

from v2.checks import f06_inference_rules as K
from v2.checks import f07_soundness as A
from . import case_science as S, case_cascade as C, case_reference as R
from .program_reference import tail


def report():
    scientific = []
    for index, (u, v, d, price) in enumerate(product(
            (Q(0), Q(1, 8), Q(1)), (Q(0), Q(1, 16), Q(1)),
            (None, Q(0), Q(1, 64), Q(1, 8)), (Q(0), Q(1, 32)))):
        source = S.Source(u, v, d, f'science-{index}')
        ctx, proof = S.prove(source, price)
        bound, point = R.scientific_bound(source, price)
        new, old = S.pair(price)
        root = A.receive(ctx, proof, A.request(ctx, None, new, old, bound))
        if root.budget != bound:
            raise AssertionError('Native bound disagrees with direct polynomial execution.')
        if bound <= 0:
            A.receive(ctx, proof, A.request(ctx, None, new, old, 0))
        try:
            A.receive(ctx, proof, A.request(ctx, None, new, old, bound-Q(1, 128)))
        except A.AuditError:
            pass
        else:
            raise AssertionError('Receiver accepted an insufficient stronger request.')
        scientific.append({'u_cap': str(u), 'v_cap': str(v), 'joint_cap': None if d is None else str(d),
                           'price': str(price), 'bound': str(bound), 'attainer': list(map(str, point)),
                           'zero_budget_result': 'certified' if bound <= 0 else 'refuted_by_reference',
                           'proof_nodes': len(proof.steps)})

    stages = []
    raw_traces = {}
    for query_budget in (Q(0), Q(1)):
        records = C.collect(budget=query_budget, revision=f'current-query-{query_budget}')
        raw_traces[str(query_budget)] = [
            {'source_caps': list(caps), 'observed_failures': list(observed),
             'versions': [a.version for a in attempts], 'statuses': [a.status for a in attempts],
             'proof_nodes': [a.proof_nodes for a in attempts],
             'ordinary_nodes': ordinary.proof_nodes, 'fallback_nodes': fallback.proof_nodes}
            for caps, (observed, attempts, fallback, ordinary) in records.items()]
        for parity, mixing, penalty in product((0, 1), (Q(0), Q(1, 4), Q(1, 2)),
                                               (Q(0), Q(2), Q(5), Q(10), Q(20), Q(40))):
            input_law = {bits: (1-mixing)*C.parity_population(3, parity).get(bits, 0)
                         + mixing*int(bits == (1, 0, 1)) for bits in product((0, 1), repeat=3)}
            behavior_law = {}
            for caps, probability in input_law.items():
                observed = records[caps][0]
                behavior_law[observed] = behavior_law.get(observed, Q(0))+probability
            moments = C.summary(behavior_law)
            for order in R.all_orders(3):
                executed, _ = R.expected(behavior_law, order, (Q(5),)*3, penalty)
                if executed != C.compiled_cost(moments, order, (Q(5),)*3, penalty):
                    raise AssertionError('Prefix compilation differs from path execution.')
            selected = R.choose(behavior_law, (Q(5),)*3, penalty, Q(9))
            # Later stage actually runs the chosen bounded procedures on each current request.
            deployed_cost = deployed_unresolved = Q(0)
            for caps, probability in input_law.items():
                ctx = C.context(caps, f'deployment-query-{query_budget}')
                charge, unresolved, _ = C.deploy(ctx, selected[3], penalty, query_budget)
                deployed_cost += probability*charge
                deployed_unresolved += probability*unresolved
            if (deployed_cost, deployed_unresolved) != selected[:2]:
                raise AssertionError('Selected policy was not realized by actual later executions.')
            ordinary_nodes = sum((probability*records[caps][3].proof_nodes
                                  for caps, probability in input_law.items()), Q(0))
            ordinary_with_stopping = sum((probability*min(penalty, records[caps][3].proof_nodes)
                                         for caps, probability in input_law.items()), Q(0))
            stages.append({'query_budget': str(query_budget), 'parity': parity, 'mixing': str(mixing),
                           'penalty': str(penalty), 'selected_order': selected[3],
                           'selected_cost': str(deployed_cost), 'unresolved': str(deployed_unresolved),
                           'ordinary_complete_emitted_nodes': str(ordinary_nodes),
                           'ordinary_cost_with_permitted_stopping': str(ordinary_with_stopping)})

    meta = []
    for q in (Q(0), Q(1, 100), Q(1, 80), Q(1, 64), Q(1, 4)):
        ctx, proof, new, old = C.meta_proof(q)
        bound = proof.steps[proof.root].budget
        A.receive(ctx, proof, A.request(ctx, None, new, old, bound, 'L'))
        meta.append({'q_cap': str(q), 'bound': str(bound), 'proof_nodes': len(proof.steps),
                     'replacement_licensed': bound <= 0})

    shared = []
    for z in (Q(1, 8), Q(1, 12)):
        ctx, proof, new, old = S.prove_shared_error(S.Source(Q(1), Q(1), Q(1, 64)),
                                                  Q(1, 32), Q(1, 100), Q(1, 200), z)
        A.receive(ctx, proof, A.request(ctx, None, new, old, 0))
        shared.append({'fourth_node': str(z), 'weights': [[str(x), str(w)] for x, w in S.weights(z)],
                       'bound': str(proof.steps[proof.root].budget), 'proof_nodes': len(proof.steps),
                       'common_error': 'unbounded'})

    risk = []
    good = C.parity_population(3, 0)
    losses = [R.execute(bits, (0, 1, 2), (Q(5),)*3, Q(20))[0] for bits in good]
    for alpha in (Q(0), Q(1, 17), Q(1, 16), Q(1, 15), Q(1, 2), Q(3, 4)):
        value = tail(losses, list(good.values()), alpha)
        risk.append({'alpha': str(alpha), 'cvar': str(value), 'versus_fallback': str(value-9)})

    return {'status': 'PASS', 'scope': 'F13 exact development families; task timing is recorded separately',
            'novelty': 'NOT YET SUPPORTED', 'native_kernel_changed': False,
            'scientific_sources': 36, 'scientific_comparisons': len(scientific),
            'scientific': scientific, 'raw_current_traces': raw_traces,
            'staged_scenarios': len(stages), 'policy_comparisons': len(stages)*len(R.all_orders(3)),
            'stages': stages, 'metalevel': meta, 'shared_error': shared, 'risk_revision': risk,
            'stateful_orders': {''.join(order): C.stateful_run(order)[0]
                               for order in (('A',), ('B',), ('A', 'B'), ('B', 'A'))},
            'cost_scope': 'emitted native proof nodes plus declared unresolved penalty; not total runtime',
            'population_scope': 'finite declared law, no deployment calibration claim'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json', type=Path, required=True)
    args = parser.parse_args()
    if args.json.exists():
        parser.error('Choose a fresh evidence filename; existing results are not overwritten.')
    data = report()
    args.json.write_text(json.dumps(data, indent=2, sort_keys=True)+'\n', encoding='utf-8')
    print(json.dumps({key: data[key] for key in ('status', 'scientific_sources', 'scientific_comparisons',
                                              'staged_scenarios', 'policy_comparisons', 'novelty')}, indent=2))


if __name__ == '__main__':
    main()
