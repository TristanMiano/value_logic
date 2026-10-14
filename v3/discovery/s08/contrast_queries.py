"""Checked minimax acquisition of only a residual invoice contrast."""
from itertools import product
from fractions import Fraction as F
from pathlib import Path
import copy
import json
import sys
import edge_invoices as ev
import invoice_add as ia
import invoice_bandit as ib
import pruned_bandit as pb
import paired_invoices as pi
import markov_paths as mk
import g01

HERE=Path(__file__).resolve().parent
Meter=g01.kernel.Meter


class Planner:
    def __init__(self,arena,costs):
        self.arena=arena;self.costs=costs;self.meter=Meter();self.supports=[0];self.cofs={};self.values={0:0};self.choices={0:None}
    def support(self,node):
        while len(self.supports)<len(self.arena.nodes):
            var,a,delta,b=self.arena.nodes[len(self.supports)];self.supports.append((1<<var)|self.supports[a]|self.supports[b])
            self.meter.pay('target_planning','canonical_function_support',5)
        return [i for i in range(self.arena.n) if self.supports[node]>>i&1]
    def cofactor(self,edge,var,bit):
        offset,node=edge;key=node,var,bit;self.meter.pay('target_planning','cofactor_cache_lookup',2)
        if key not in self.cofs:
            if node==0 or self.arena.var(node)>var:value=(0,node)
            elif self.arena.var(node)==var:value=self.arena.cofactor((0,node),var,bit)
            else:
                top,a,delta,b=self.arena.nodes[node]
                value=self.arena.branch(top,self.cofactor((0,a),var,bit),self.cofactor((delta,b),var,bit))
            self.cofs[key]=value;self.meter.pay('target_planning','retain_arbitrary_variable_cofactor',5)
        shift,child=self.cofs[key];return offset+shift,child
    def restrict(self,edge,observed):
        for var,bit in sorted(observed.items()):edge=self.cofactor(edge,var,bit)
        return edge
    def quote(self,node):
        if node in self.values:return self.values[node]
        if len(self.values)>=100000:raise ia.BudgetExceeded('Minimax state cap')
        options=[]
        for var in self.support(node):
            low=self.cofactor((0,node),var,0);high=self.cofactor((0,node),var,1)
            value=self.costs[var]+max(self.quote(low[1]),self.quote(high[1]))
            options.append((value,var));self.meter.pay('target_planning','minimax_query_option',7)
        self.values[node],self.choices[node]=min(options);self.meter.pay('target_planning','retain_minimax_quote',3)
        return self.values[node]


def check_plan(planner):
    arena=planner.arena;checker=ev.IdentityChecker(arena);ev.structure(arena,checker.meter)
    support=[0]
    for var,a,delta,b in arena.nodes[1:]:support.append((1<<var)|support[a]|support[b])
    if planner.values.get(0)!=0 or planner.choices.get(0)is not None:raise ValueError('Terminal target quote')
    for node,bound in planner.values.items():
        if not node:continue
        options=[]
        for var in range(arena.n):
            if not support[node]>>var&1:continue
            lo=planner.cofs[node,var,0];hi=planner.cofs[node,var,1]
            if support[lo[1]]>>var&1 or support[hi[1]]>>var&1:raise ValueError('Cofactor retained observed variable')
            checker.conditional((0,node),var,0,[lo],[hi])
            options.append((planner.costs[var]+max(planner.values[lo[1]],planner.values[hi[1]]),var))
            checker.meter.pay('target_check','all_query_bellman_equalities',8)
        if (bound,planner.choices[node])!=min(options):raise ValueError('Invalid target minimax recurrence')
    return checker.meter.record()


def prepare(costs):
    meter=Meter();data=ib.source(costs);bank,ranges,syntax=pb.prepare(data,meter);arena=ev.Arena(len(costs));functions={};proofs={}
    if len(bank)!=2:raise ValueError('This prospective service screen has exactly two invoice classes')
    for r,roots in bank.items():
        tables=ia.compile_policy(arena,costs,roots);checked=ev.check_policy(arena,costs,roots,tables)
        meter.pay('preparation','independent_invoice_diagram_check',checked['total'])
        functions[r]=tables['ordinary'][0,len(costs)-1];proofs[r]=dict(roots=roots,tables=tables,checking=checked)
    a,b=sorted(bank);edge=arena.apply('sub',functions[a],functions[b]);checker=ev.IdentityChecker(arena)
    checker.linear([(1,edge),(-1,functions[a]),(1,functions[b])]);meter.pay('preparation','independent_contrast_identity',checker.meter.total)
    meter.pay('preparation','invoice_diagram_compilation',arena.meter.total)
    return arena,edge,bank,dict(syntax=syntax,policies=proofs,contrast=edge),meter


def run(directory,n):
    directory.mkdir(exist_ok=False);(directory/'impl.py').write_bytes(Path(__file__).read_bytes())
    costs=next(c['costs'] for c in json.loads((HERE/'cs01/design.json').read_text())['cases'] if len(c['costs'])==n)
    g01.save(directory/'design.json',dict(stage='DEVELOPMENT',contributor='Codex (GPT-6)',n=n,costs=costs,source_sha256=g01.sha(__file__),
        declaration_sha256=g01.sha(HERE/'contrast_queries.md'),all_indicator_worlds=2**n,physical_audits=0))
    arena,edge,bank,proof,meter=prepare(costs);planner=Planner(arena,costs);records=[];a,b=sorted(bank)
    for bits in product((0,1),repeat=n):
        fees={r:pi.direct_fee(costs,roots,bits)[0] for r,roots in bank.items()};truth=fees[a]-fees[b]
        assert ev.evaluate(arena,edge,bits)==truth
        for logger,roots in bank.items():
            _,queried=pi.direct_fee(costs,roots,bits);known={i:bits[i] for i in queried}
            residual=planner.restrict(edge,known);bound=planner.quote(residual[1]);direct=[];current=residual
            while current[1]:
                var=planner.choices[current[1]];assert var not in known and var not in direct
                direct.append(var);current=planner.cofactor(current,var,bits[var])
            assert current[0]==truth
            target_fee=sum(costs[i] for i in direct);assert target_fee<=bound
            other=b if logger==a else a;state=[known.get(i,-1) for i in range(n)];replay=[]
            while True:
                var=mk.pc.next_query(state,bank[other])
                if var is None:break
                assert var not in known and var not in replay;replay.append(var);state[var]=bits[var]
            replay_fee=sum(costs[i] for i in replay);full_fee=sum(costs[i] for i in range(n) if i not in known)
            records.append(dict(bits=bits,logger=logger,known=known,contrast=truth,quote=bound,target_queries=direct,target_fee=target_fee,
                replay_queries=replay,replay_fee=replay_fee,full_fee=full_fee))
    checked=check_plan(planner);meter.pay('planning','all_target_query_planning',planner.meter.total)
    meter.pay('planning','new_edge_nodes_during_cofactoring',arena.meter.total-sum(v['units'] for v in [])) if False else None
    # Arena is shared: add only the construction increment after original preparation.
    initial_graph_units=next(x['units'] for x in meter.record()['operations'] if x['operation']=='invoice_diagram_compilation')
    meter.pay('planning','residual_cofactor_graph_construction',arena.meter.total-initial_graph_units)
    meter.pay('checking','independent_target_quote_checks',checked['total'])
    expected=[]
    for r in (2,4,8):
        for logger in bank:
            selected=[v for v in records if v['logger']==logger]
            expected.append(dict(r=r,logger=logger,**{key:sum(mk.world_probability(v['bits'],r)*v[key] for v in selected) for key in('target_fee','replay_fee','full_fee','quote')}))
    negative=[];node=next((v for v in planner.values if v),None)
    if node is not None:
        old=planner.values[node];planner.values[node]=old-1
        try:check_plan(planner)
        except ValueError:negative.append('underquoted_target_rejected')
        else:raise AssertionError('Underquote accepted')
        planner.values[node]=old
    result=dict(status='complete',n=n,world_logger_cases=len(records),target_fee_sum=sum(v['target_fee'] for v in records),
        replay_fee_sum=sum(v['replay_fee'] for v in records),full_fee_sum=sum(v['full_fee'] for v in records),
        cheaper_target_cases=sum(v['target_fee']<v['replay_fee'] for v in records),more_expensive_target_cases=sum(v['target_fee']>v['replay_fee'] for v in records),
        zero_target_cases=sum(not v['target_queries'] for v in records),planning_states=len(planner.values),cofactor_states=len(planner.cofs),
        evbdd_nodes=len(arena.nodes),expected=expected,negative_controls=negative,invoice=meter.record(),physical_audits=0)
    g01.save(directory/'certificate.json',ib.cp.normalize(dict(costs=costs,nodes=arena.nodes,source_proof=proof,values=planner.values,
        choices=planner.choices,cofactors=planner.cofs,checking=checked)))
    g01.save(directory/'worlds.json',records);g01.save(directory/'result.json',result)
    print(json.dumps({k:v for k,v in result.items() if k not in('expected','invoice')}))

if __name__=='__main__':run(Path(sys.argv[1]),int(sys.argv[2]))
