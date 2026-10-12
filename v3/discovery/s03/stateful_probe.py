"""Mutable predictor toy and exact policy enumeration. DEVELOPMENT.

Codex (GPT-6), 2026-10-12. No sampled empirical generalization is claimed.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib,json,sys,time


class Actor:
    def __init__(self):self.binding=lambda:0
    def bind(self,a):self.binding=lambda:a


class Predictor:
    def __init__(self,kind,actor):
        self.kind,self.actor,self.original,self.cache=kind,actor,actor.binding,None
    def call(self):
        if self.kind=='frozen':return self.original()
        if self.kind=='cached':
            if self.cache is None:self.cache=self.actor.binding()
            return self.cache
        assert self.kind=='live'
        return self.actor.binding()


KINDS=('live','cached','frozen')


def run(kind,experiment,action):
    actor=Actor();predictor=Predictor(kind,actor)
    saved_binding,saved_cache=actor.binding,predictor.cache
    obs=[]
    if experiment!='none':
        actor.bind(1);obs.append(predictor.call());actor.binding=saved_binding
        if experiment=='two':obs.append(predictor.call())
        if experiment=='restored':predictor.cache=saved_cache
        assert experiment in ('one','two','restored')
    actor.bind(action);prediction=predictor.call()
    return tuple(obs),10*prediction-action


def optimal(prior,experiment,pure_information=False,price=F(0)):
    table={h:[run(h,experiment,a) for a in (0,1)] for h in KINDS}
    observations=sorted({table[h][0][0] for h in KINDS})
    rows=[]
    for actions in product((0,1),repeat=len(observations)):
        policy=dict(zip(observations,actions));forecast=actual=F(0)
        for h,p in zip(KINDS,prior):
            a=policy[table[h][0][0]];cost=table[h][a][1]
            forecast+=p*(run(h,'none',a)[1] if pure_information else cost)
            actual+=p*cost
        rows.append((forecast+price,actual+price,actions))
    forecast,actual,actions=min(rows)
    return {'forecast':str(forecast),'actual':str(actual),
            'policy':[{'observation':list(o),'action':a} for o,a in zip(observations,actions)],
            'enumerated_policies':len(rows)}


def main(out):
    assert not out.exists();start=time.perf_counter_ns()
    priors={'uniform':(F(1,3),)*3,'cache_heavy':(F(1,40),F(38,40),F(1,40))}
    result={'status':'running','evidence':'DEVELOPMENT','contributor':'Codex (GPT-6)',
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'python':sys.version,'loss_tables':{},'policies':{}}
    for experiment in ('none','one','two','restored'):
        result['loss_tables'][experiment]={h:[{'observation':list(run(h,experiment,a)[0]),'loss':run(h,experiment,a)[1]} for a in (0,1)] for h in KINDS}
    for label,prior in priors.items():
        rows={e:{'state_aware':optimal(prior,e),'pure_information':optimal(prior,e,True)} for e in ('none','one','two','restored')}
        rows['paid_restoration']={str(c):optimal(prior,'restored',price=c) for c in (F(0),F(1,5),F(2,5))}
        result['policies'][label]={'prior':[str(x) for x in prior],'results':rows}
    u=result['policies']['uniform']['results'];c=result['policies']['cache_heavy']['results']
    assert u['one']['pure_information']['forecast']=='-1/3'
    assert u['one']['pure_information']['actual']=='3'
    assert u['two']['state_aware']['actual']=='8/3'
    assert u['restored']['state_aware']['actual']=='-1/3'
    assert c['one']['pure_information']['actual']=='379/40'
    assert c['one']['state_aware']['actual']=='35/4'
    assert c['one']['state_aware']['policy']!=c['one']['pure_information']['policy']
    result.update(status='complete',elapsed_ns=time.perf_counter_ns()-start)
    out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':result['status'],'elapsed_ns':result['elapsed_ns'],'uniform_one':u['one'],'cache_heavy_one':c['one']}))


if __name__=='__main__':main(Path(sys.argv[1]))
