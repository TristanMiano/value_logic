"""Developmental sparse-policy checks; all costs and sources retained."""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json,random,sys,time
from policy_values import add,compile_cost,execute,evaluate,upper,bank_regret,parity_dag


def serial(value):
    if isinstance(value,F):return str(value)
    if isinstance(value,dict):return {str(k):serial(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)):return [serial(v) for v in value]
    return value


def main(out):
    assert not out.exists();start=time.perf_counter_ns();rng=random.Random(13714);cases=[];world_checks=0
    for case in range(100):
        m=rng.randrange(1,7);nodes=[{'kind':'terminal','row':tuple(F(rng.randrange(-4,5),2) for _ in range(m+1))} for _ in range(3)]
        for _ in range(rng.randrange(4,13)):
            node={'kind':rng.choice(('observe','flip')),'bit':rng.randrange(m),'price':F(rng.randrange(5),4)}
            if node['kind']=='flip':node['child']=rng.randrange(len(nodes))
            else:node.update(plus=rng.randrange(len(nodes)),minus=rng.randrange(len(nodes)))
            nodes.append(node)
        root=len(nodes)-1;poly,visited=compile_cost(nodes,root,m)
        costs=[]
        for x in range(1<<m):
            v=execute(nodes,root,m,x);assert v==evaluate(poly,x);world_checks+=1;costs.append(v)
        counts=[rng.randrange(1,7) for _ in costs];total=sum(counts)
        exact=sum(F(w,total)*v for w,v in zip(counts,costs));intervals={}
        for mask in poly:
            if not mask:continue
            mu=sum(F(w,total)*(1 if (mask&x).bit_count()%2==0 else -1) for x,w in enumerate(counts))
            intervals[mask]=(max(F(-1),mu-F(1,10)),min(F(1),mu+F(1,10)))
        bound,witness=upper(poly,intervals);assert exact<=bound
        lower=-upper(add((-1,poly)),intervals)[0];assert lower<=exact
        cases.append({'m':m,'nodes':nodes,'root':root,'polynomial':poly,'visited_nodes':visited,'prior_counts':counts,
                      'exact_expected_cost':exact,'intervals':intervals,'lower':lower,'upper':bound,'algebraic_box_endpoint':witness})
    parity=[]
    for H in (1,4,16,64):
        c=F(1,40*H);nodes,plus,minus=parity_dag(H,c);begin=time.perf_counter_ns()
        a,visits=compile_cost(nodes,plus,H+1);b,_=compile_cost(nodes,minus,H+1);elapsed=time.perf_counter_ns()-begin
        mask=(1<<(H+1))-1
        assert a=={0:F(21,40),mask:F(-1,2)} and b=={0:F(21,40),mask:F(1,2)}
        assert add((1,a),(-1,b))=={mask:F(-1)}
        immediate=nodes[0]['row'];p0={0:F(1,2),1<<H:F(-1,2)};p1={0:F(1,2),1<<H:F(1,2)}
        intervals={mask:(F(3,5),F(4,5)),1<<H:(F(-1,10),F(1,10))}
        R,competitor,endpoint=bank_regret([a,b,p0,p1],0,intervals);assert R==0
        parity.append({'observations':H,'hidden_bits':H+1,'nodes':len(nodes),'visited_nodes':visits,'compiled_terms':len(a),
                       'compilation_ns':elapsed,'plus':a,'minus':b,'bank_regret':R,'intervals':intervals,
                       'scope':'four named policies only; moment bounds supplied, no global optimality or acquisition claim'})
    result={'status':'complete','evidence':'DEVELOPMENT','contributor':'Codex (GPT-6)','seed':13714,'python':sys.version,
            'sources':{p:hashlib.sha256(Path(__file__).with_name(p).read_bytes()).hexdigest() for p in ('policy_values.py','policy_probe.py')},
            'cases':cases,'world_checks':world_checks,'parity':parity,'elapsed_ns':time.perf_counter_ns()-start}
    out.write_text(json.dumps(serial(result),indent=2)+'\n',encoding='utf-8')
    print(json.dumps(serial({'status':'complete','random_dags':len(cases),'world_checks':world_checks,'parity':parity,'elapsed_ns':result['elapsed_ns']})))


if __name__=='__main__':main(Path(sys.argv[1]))
