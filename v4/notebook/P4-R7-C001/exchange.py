"""W7.4. External solvency tests for local judgments with revisable standpoints."""
from fractions import Fraction as F
from itertools import permutations,product


def simple_cycles(vertices,bids):
    for length in range(1,len(vertices)+1):
        for v in permutations(vertices,length):
            if v[0]!=min(v):
                continue
            edges=tuple(zip(v,v[1:]+v[:1]))
            if all(e in bids for e in edges):
                yield edges


def potential(vertices,bids):
    # Start a free path at every state. With no positive cycles, longest paths
    # have a simple representative of length at most |V|-1.
    u={v:F(0) for v in vertices}
    for _ in range(len(vertices)-1):
        v=u.copy()
        for (i,j),amount in bids.items():
            v[j]=max(v[j],u[i]+amount)
        u=v
    assert all(u[j]-u[i]>=v for (i,j),v in bids.items())
    return u


def test_network():
    vertices=("A","B","C","D")
    bids={("A","B"):F(1),("B","C"):F(1),("C","A"):F(1),
          ("B","A"):F(-2),("A","D"):F(3),("D","A"):F(-3)}
    cycles=list(simple_cycles(vertices,bids))
    fee=max(F(0),max(sum(bids[e] for e in c)/len(c) for c in cycles))
    assert fee==1
    uniform={e:v-fee for e,v in bids.items()}
    tailored=bids.copy()
    tailored["C","A"]-=3
    for name,adjusted in [("uniform",uniform),("targeted",tailored)]:
        u=potential(vertices,adjusted)
        print("Style / potential / reserve bound",name,u,max(u.values())-min(u.values()))
        for path in product(vertices,repeat=6):
            moves=list(zip(path,path[1:]))
            if all(e in adjusted for e in moves):
                assert sum(adjusted[e] for e in moves)<=u[path[-1]]-u[path[0]]
    assert uniform["A","D"]==2 and tailored["A","D"]==3
    # One previously unseen signal earns decision value, despite ending at
    # the same physical desk and paying to traverse the circuit.
    q=F(3,4); charge=F(9,50)
    assert q-F(1,2)-charge==F(7,100)
    print("First information circuit net, then rereading its record",F(7,100),-charge)


if __name__=="__main__":
    test_network()
