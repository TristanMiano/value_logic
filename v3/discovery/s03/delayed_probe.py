"""Small exact domination check, not independent statistical confirmation."""
from fractions import Fraction as F
from itertools import product
import hashlib,json
from pathlib import Path
from datetime import datetime,timezone
from delayed_bets import DelayedGroup
from positive_bets import Group


def run():
    checks=0;refinements=0
    for N in range(1,7):
        for s in range(N+1):
            for truth in product((0,1),repeat=s):
                full=Group(N,(F(0),F(1,4),F(1),F(4)))
                for y in truth:full.observe(y)
                for partial in product(*[(0,1) if y else (0,) for y in truth]):
                    got=DelayedGroup(N,full.etas)
                    for j,z in enumerate(partial):got.add(j,z)
                    Ms=range(sum(truth),N-s+sum(truth)+1)
                    for M in Ms:
                        assert got.wealth(M)<=full.wealth(M);checks+=1
                    for i in reversed(range(s)):
                        if truth[i] and not partial[i]:
                            old={M:got.wealth(M) for M in Ms}
                            assert got.accept(i)
                            for M in Ms:
                                assert old[M]<=got.wealth(M)<=full.wealth(M);refinements+=1
                    assert got.trace==full.trace
    g=DelayedGroup(3);g.add(1,0)
    before=(g.trace.copy(),g.identities.copy(),g.positives)
    rejected=0
    for fn in (lambda:g.add(1,1),lambda:g.add(False,0),lambda:g.accept(2)):
        try:fn();raise AssertionError('bad identity accepted')
        except ValueError:
            rejected+=1;assert before==(g.trace,g.identities,g.positives)
    assert g.accept(1) and not g.accept(1)
    return {'domination_checks':checks,'monotone_refinement_checks':refinements,'invalid_identity_checks':rejected}


if __name__=='__main__':
    out=Path(__file__).with_name('delayed01.json');assert not out.exists()
    result={'status':'running','evidence':'DEVELOPMENT','contributor':'Codex (GPT-6)','start_utc':datetime.now(timezone.utc).isoformat(),
            'sources':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),*[Path(__file__).with_name(x) for x in ('delayed_bets.py','positive_bets.py')]]}}
    out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    try:result.update(run(),status='complete')
    except Exception:result.update(status='failed',failure=__import__('traceback').format_exc());raise
    finally:
        result['end_utc']=datetime.now(timezone.utc).isoformat();out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result))
