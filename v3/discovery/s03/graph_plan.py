"""Exact tree observation planning; ordinary three-state dynamic programming.

Codex (GPT-6). DEVELOPMENT. Inputs are supplied prizes and exact fixed costs.
"""

def solve(prizes, anchors, edges):
    n=len(prizes)
    assert n and len(anchors)==n and len(edges)==n-1
    assert all(x>=0 for x in prizes) and all(x is None or x>=0 for x in anchors)
    adjacency=[[] for _ in range(n)]
    for j,(u,v,c) in enumerate(edges):
        assert 0<=u<n and 0<=v<n and u!=v and c>=0
        adjacency[u].append((v,j,c));adjacency[v].append((u,j,c))
    parent=[None]*n;parent[0]=-1;order=[0]
    for v in order:
        for u,j,c in adjacency[v]:
            if u==parent[v]:continue
            assert parent[u] is None,'not a tree'
            parent[u]=v;order.append(u)
    assert len(order)==n
    records=[(None,None,None)]
    def node(value,left=0,right=0,action=None):
        records.append((left,right,action));return value,len(records)-1
    def pick(*options):
        return max((x for x in options if x is not None),key=lambda x:x[0],default=None)
    def join(left,right,edge=None,cost=0):
        if left is None or right is None:return None
        return node(left[0]+right[0]-cost,left[1],right[1],None if edge is None else ('edge',edge))
    states=[None]*n
    for v in reversed(order):
        N=(0,0);U=node(prizes[v]);A=None if anchors[v] is None else node(prizes[v]-anchors[v],action=('anchor',v))
        for u,j,c in adjacency[v]:
            if parent[u]!=v:continue
            nc,uc,ac=states[u];closed=pick(nc,ac)
            N,U,A=join(N,closed),pick(join(U,closed),join(U,uc,j,c)),pick(join(A,closed),join(A,uc,j,c),join(A,ac,j,c),join(U,ac,j,c))
        states[v]=(N,U,A)
    value,ref=pick(states[0][0],states[0][2]);selected_edges=[];selected_anchors=[];stack=[ref]
    while stack:
        k=stack.pop()
        if k==0:continue
        left,right,action=records[k];stack.extend((left,right))
        if action:
            (selected_edges if action[0]=='edge' else selected_anchors).append(action[1])
    assert len(selected_edges)==len(set(selected_edges)) and len(selected_anchors)==len(set(selected_anchors))
    return dict(value=value,edges=sorted(selected_edges),anchors=sorted(selected_anchors),
                states=[[None if p is None else p[0] for p in s] for s in states],records=len(records))


def check(prizes,anchors,edges,plan):
    """Independently check the plan's realized component reward and invoice."""
    n=len(prizes);parent=list(range(n))
    def root(v):
        while parent[v]!=v:
            parent[v]=parent[parent[v]];v=parent[v]
        return v
    assert len(plan['edges'])==len(set(plan['edges'])) and len(plan['anchors'])==len(set(plan['anchors']))
    cost=0
    for j in plan['edges']:
        assert 0<=j<len(edges)
        u,v,c=edges[j];parent[root(u)]=root(v);cost+=c
    known=set()
    for v in plan['anchors']:
        assert 0<=v<n and anchors[v] is not None
        known.add(root(v));cost+=anchors[v]
    covered=[v for v in range(n) if root(v) in known]
    reward=sum(prizes[v] for v in covered);value=reward-cost
    if 'value' in plan:assert plan['value']==value
    return dict(value=value,reward=reward,cost=cost,covered=covered)


def predict(n,edges,plan,edge_labels,anchor_labels,flip):
    """Use only purchased exact labels; one fair flip suffices for minimax score."""
    assert flip in (0,1) and set(edge_labels)==set(plan['edges']) and set(anchor_labels)==set(plan['anchors'])
    adjacency=[[] for _ in range(n)]
    for j in plan['edges']:
        u,v,_=edges[j];y=edge_labels[j];assert y in (0,1)
        adjacency[u].append((v,y));adjacency[v].append((u,y))
    relative={};guess=[None]*n
    for v in range(n):
        if v in relative:continue
        relative[v]=0;component=[v]
        for u in component:
            for z,y in adjacency[u]:
                if z in relative:assert relative[z]==relative[u]^y
                else:relative[z]=relative[u]^y;component.append(z)
        offsets={relative[u]^anchor_labels[u] for u in component if u in anchor_labels}
        assert len(offsets)<=1,'inconsistent exact query labels'
        offset=next(iter(offsets)) if offsets else flip
        for u in component:guess[u]=relative[u]^offset
    return guess
