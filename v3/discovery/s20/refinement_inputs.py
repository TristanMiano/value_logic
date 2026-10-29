"""Build prospective finite loss panels without evaluating any method."""
import json
from pathlib import Path
import random

if __name__ == '__main__':
    rng = random.Random(51029)
    matrices = [
        dict(name='joint_maxima',values=[[9,0],[0,10],[12,13],[9,0],[0,10]]),
        dict(name='optimal_not_safe',values=[[0,10],[10,0],[0,10],[10,0],[0,10]]),
    ]
    for j in range(3):
        matrices.append(dict(name='seeded_'+str(j),values=[[rng.randrange(14) for _ in range(3)] for _ in range(5)]))
    matrices.append(dict(name='one_action',values=[[j] for j in range(5)]))
    for row in matrices:
        row['values'] = [[str(v) for v in r] for r in row['values']]
    Path(__file__).with_name('refinement_inputs.json').write_text(json.dumps(matrices,indent=2)+'\n',encoding='utf-8')
