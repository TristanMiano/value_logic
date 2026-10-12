"""Expected-budget primal/dual advice from an already checked price profile."""
from fractions import Fraction as F
from price_profile import line, prepare

def budget(terms,prices,profile,b):
    assert isinstance(b,F) and b>=0
    answer=prepare(terms,prices,profile,'budget')
    points=sorted(set((line(terms,prices,p['bits'])[1],line(terms,prices,p['bits'])[0],p['bits']) for p in profile['pieces']))
    if b>=points[-1][0]:
        c,a,bits=points[-1];mix=[(F(1),bits)]
    else:
        high=next(i for i,p in enumerate(points) if p[0]>b)
        lo,hi=points[high-1],points[high]
        theta=(b-lo[0])/(hi[0]-lo[0])
        mix=[(1-theta,lo[2]),(theta,hi[2])]
    values=[(weight,*line(terms,prices,bits)) for weight,bits in mix]
    gain=sum((w*a for w,a,c in values),F(0));cost=sum((w*c for w,a,c in values),F(0))
    candidates=[(answer(x,'budget')[0]+x*b,x) for x in [F(0)]+[p['hi'] for p in profile['pieces']]]
    upper,lam=min(candidates)
    assert cost<=b and gain==upper and sum(w for w,_ in mix)==1
    return dict(budget=b,gain=gain,cost=cost,lambda_dual=lam,mixture=mix)
