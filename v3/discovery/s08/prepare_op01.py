"""Freeze op01 before acquisition. Codex (GPT-6), DEVELOPMENT."""
from pathlib import Path
import random
import observation_policy as op

root=op.HERE/'op01';root.mkdir(exist_ok=False);rng=random.Random(8141660);cases=[]
for j,weights in enumerate(([1,1],[5,2],[1,2,3],[2,3,5,1])):
    H=5;W=sum(weights);A=10*H*W;fees=[rng.randrange(1,8) for _ in range(len(weights)+1)]+[9]
    cases.append(dict(name=f'c{j}',weights=weights,H=H,A=A,alphabet=[0,2,3,5],fees=fees,seed=8141670+j,
        duties=sorted(set((p,t) for p in(A,A+H*W,A+2*H*W) for t in(H*W//2,H*W)))))
dependencies={name:op.g01.sha(op.HERE/name) for name in('partial_star.py','frontier_service.py','replacement_frontier.py','action_audits.py','g01.py','joint_guard.py')}
design=dict(stage='DEVELOPMENT',contributor='Codex (GPT-6)',cases=cases,arms=['minimax','ordinary_minimax','cheapest','narrow'],source_sha256=op.g01.sha(op.__file__),dependencies=dependencies,
    physical_requests_per_duty_arm=64,logical_acquisition='one original mandatory-feature resolution per case, shared with all arms',complete_sat_calls=0)
op.g01.save(root/'design.json',design)
(root/'observation_policy.py').write_bytes(Path(op.__file__).read_bytes());(root/'declaration.md').write_bytes((op.HERE/'observation_policy.md').read_bytes())
for name in dependencies:(root/name).write_bytes((op.HERE/name).read_bytes())
for case in cases:
    geometry=op.fs.acquire_geometry(op.source(case));op.g01.save(root/f"{case['name']}_geometry.json",geometry)
print('frozen',len(cases),'cases',sum(len(c['duties']) for c in cases),'duties')
