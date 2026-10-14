"""Independent PySAT RC2 checks, not a new formal proof or paid service."""
import datetime,json,os,pathlib,platform,sys,time
sys.path.insert(0,str(pathlib.Path(os.environ['TEMP'])/'value_logic_s10_deps'))
import pysat
from pysat.formula import WCNF
from pysat.examples.rc2 import RC2
from pysat.solvers import Solver
root=pathlib.Path(__file__).resolve().parent/'up50'
design=json.loads((root/'design.json').read_text(encoding='utf-8'))
rows=[]
for item in design['sources']:
    source=item['source']; name=source['name']; start=time.perf_counter_ns()
    with Solver(name='g3',bootstrap_with=source['hard']) as solver:
        sat=solver.solve()
        assert sat==item['expected_sat']
        sat_stats=solver.accum_stats()
    arms={}
    for arm in ['baseline','unit']:
        file=root/name/arm/'results.json'
        if not file.exists():
            arms[arm]={'status':'not_admitted'}
            continue
        data=json.loads(file.read_text(encoding='utf-8'))
        objectives=[]
        for objective in data['objectives']:
            q=objective['q']; f=WCNF()
            for clause in source['hard']:f.append(clause)
            constant=0
            for var,weight in zip(source['features'],q):
                if weight>0:f.append([-var],weight=weight)
                elif weight<0:f.append([var],weight=-weight);constant+=weight
            with RC2(f,solver='g3') as rc:
                model=rc.compute()
                assert model is not None
                value=rc.cost+constant
                assert value==objective['lower'],(name,value,objective['lower'])
                true={x for x in model if x>0}
                assert all(any((lit in true if lit>0 else -lit not in true) for lit in c) for c in source['hard'])
                assert sum(w for var,w in zip(source['features'],q) if var in true)==value
                objectives.append({'lower':value,'native_cost':rc.cost,'stats':rc.oracle.accum_stats()})
        arms[arm]={'status':'pass','objectives':objectives}
    row={'source':name,'sat':sat,'sat_stats':sat_stats,'arms':arms,'wall_ns':time.perf_counter_ns()-start}
    rows.append(row)
    with (root/'native_partial.jsonl').open('a',encoding='utf-8') as f:f.write(json.dumps(row)+'\n')
    print(name,'checked',flush=True)
result={'status':'pass','contributor':'Codex (GPT-6)','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'python':sys.version,'platform':platform.platform(),'pysat':pysat.__version__,'solver':'Glucose3 via PySAT RC2','rows':rows,'unknown_costs':['native instruction count','host/library work','computation tariff'],'scope':'Independent SAT status on all8selected sources and exact native weighted-objective comparisons for every admitted satisfiable diagram; no model-count independence claim.'}
(root/'native_checked.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
