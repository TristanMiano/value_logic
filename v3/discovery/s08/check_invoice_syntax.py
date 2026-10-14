"""Restricted local arithmetic proof checker for supplied invoice circuits."""
from ast import literal_eval
from collections import Counter
from pathlib import Path
import copy
import json
import sys
import invoice_syntax as sy
import invoice_completion as ic
import g01

HERE=Path(__file__).resolve().parent
Meter=g01.kernel.Meter


def check(nodes,costs,roots,tables,root):
    ic.validate(costs,roots,{});n=len(costs);meter=Meter();supports=[0]
    if not nodes or nodes[0]!=('zero',):raise ValueError('Syntax zero terminal')
    def valid_edge(edge,index):
        if len(edge)!=2 or any(type(v)is not int for v in edge) or not 0<=edge[1]<index:raise ValueError('Syntax edge scope')
    for index,node in enumerate(nodes[1:],1):
        if node[0]=='sum':
            if len(node)!=2 or not node[1]:raise ValueError('Syntax sum arity')
            support=0
            for child,count in node[1]:
                if type(child)is not int or type(count)is not int or not 0<child<index or count<=0:raise ValueError('Syntax sum operand')
                support|=supports[child]
            meter.pay('syntax_check','sum_scope_and_support',5+3*len(node[1]))
        elif node[0]=='ite':
            if len(node)!=4 or type(node[1])is not int or not 0<=node[1]<n:raise ValueError('Syntax indicator scope')
            valid_edge(node[2],index);valid_edge(node[3],index)
            support=(1<<node[1])|supports[node[2][1]]|supports[node[3][1]]
            meter.pay('syntax_check','conditional_scope_and_support',12)
        else:raise ValueError('Unknown syntax operator')
        supports.append(support)
    demanded={m:set() for m in('ordinary','left','right')};todo=[('ordinary',0,n-1)]
    while todo:
        mode,a,b=todo.pop()
        if a>b or(a,b) in demanded[mode]:continue
        demanded[mode].add((a,b))
        if a==b and mode=='ordinary':continue
        i=a if mode=='left' else b if mode=='right' else roots[a,b]
        if mode=='left':todo.extend([('ordinary',a+1,b),('left',a+1,b)])
        elif mode=='right':todo.extend([('ordinary',a,b-1),('right',a,b-1)])
        else:todo.extend([('ordinary',a,i-1),('ordinary',i+1,b),('right',a,i-1),('left',i+1,b)])
        meter.pay('syntax_check','derive_reachable_policy_states',10)
    if set(tables)!=set(demanded) or any(set(tables[m])!=demanded[m] for m in demanded):raise ValueError('Reachable recurrence scope')
    def normalize(edges,variable=None,bit=0):
        constant=0;terms=Counter();stack=[(1,edge) for edge in edges]
        while stack:
            factor,(offset,node)=stack.pop();constant+=factor*offset;meter.pay('syntax_check','normalize_sum_or_cofactor',5)
            if node==0:continue
            entry=nodes[node]
            if entry[0]=='sum':stack.extend((factor*count,(0,child)) for child,count in entry[1])
            elif variable is not None and entry[1]==variable:stack.append((factor,entry[2+bit]))
            elif variable is not None and supports[node]&(1<<variable):raise ValueError('Identity outside restricted local proof language')
            else:terms[node]+=factor
        return constant,tuple(sorted((i,c) for i,c in terms.items() if c))
    def at(m,a,b):return tables[m][a,b] if a<=b else(0,0)
    for mode,states in demanded.items():
        for a,b in states:
            edge=tables[mode][a,b];valid_edge(edge,len(nodes))
            if a==b and mode=='ordinary':
                if normalize([edge])!=(0,()):raise ValueError('Nonzero isolated invoice')
                continue
            i=a if mode=='left' else b if mode=='right' else roots[a,b]
            if mode=='left':e=[at('ordinary',a+1,b)];m=[at('left',a+1,b)]
            elif mode=='right':e=[at('ordinary',a,b-1)];m=[at('right',a,b-1)]
            else:e=[at('ordinary',a,i-1),at('ordinary',i+1,b)];m=[at('right',a,i-1),at('left',i+1,b)]
            if any(supports[child]&(1<<i) for _,child in e+m):raise ValueError('Queried variable in child continuation')
            for bit,children in((0,e),(1,m)):
                if normalize([edge],i,bit)!=normalize([(costs[i],0)]+children):raise ValueError('False source invoice recurrence')
    if root!=tables['ordinary'][0,n-1]:raise ValueError('Final root mismatch')
    return meter.record()


def load_nodes(raw):
    result=[('zero',)]
    for node in raw[1:]:
        result.append(('sum',tuple(tuple(v) for v in node[1])) if node[0]=='sum' else('ite',node[1],tuple(node[2]),tuple(node[3])))
    return result


def run(name):
    path=HERE/'sy01'/f'{name}.json';raw=json.loads(path.read_text());nodes=load_nodes(raw['nodes']);costs=raw['case']['costs'];records=[]
    for r,policy in raw['policies'].items():
        roots={literal_eval(k):v for k,v in policy['roots'].items()}
        tables={m:{literal_eval(k):tuple(v) for k,v in table.items()} for m,table in policy['tables'].items()}
        checked=check(nodes,costs,roots,tables,tuple(policy['edge']));records.append(dict(policy=int(r),checking=checked))
    negative=[]
    bad=copy.deepcopy(tables);off,node=bad['ordinary'][0,len(costs)-1];bad['ordinary'][0,len(costs)-1]=(off+1,node)
    try:check(nodes,costs,roots,bad,bad['ordinary'][0,len(costs)-1])
    except ValueError:negative.append('wrong_fee_offset_rejected')
    else:raise AssertionError('Wrong offset accepted')
    bad=copy.deepcopy(tables);bad['ordinary'].pop((0,len(costs)-1))
    try:check(nodes,costs,roots,bad,tuple(policy['edge']))
    except ValueError:negative.append('missing_required_recurrence_rejected')
    else:raise AssertionError('Incomplete scope accepted')
    result=dict(status='checked',source_sha256=g01.sha(path),policies=records,negative_controls=negative,
        checking_named_units=sum(p['checking']['total'] for p in records),physical_audits=0)
    g01.save(HERE/'sy01'/f'{name}_checking.json',result);print(name,result['checking_named_units'])

if __name__=='__main__':run(sys.argv[1])
