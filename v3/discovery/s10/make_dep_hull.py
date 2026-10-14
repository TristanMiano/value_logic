from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'dependence.py').read_text()
before='    states=[(a,b,int(a+2*b<Q)) for a in range(k+1) for b in range(k-a+1)]'
after='''    raw=[(a,b,int(a+2*b<Q)) for a in range(k+1) for b in range(k-a+1)]
    hull_units=6*len(raw);states=[]
    def cross(o,a,b):
        nonlocal hull_units
        hull_units+=8
        return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    for event in [0,1]:
        points=sorted(x for x in raw if x[2]==event)
        hull_units+=len(points)*max(1,len(points).bit_length())
        if len(points)<=1:
            states+=points
            continue
        low=[];high=[]
        for pt in points:
            while len(low)>=2 and cross(low[-2],low[-1],pt)<=0:low.pop()
            low.append(pt)
        for pt in reversed(points):
            while len(high)>=2 and cross(high[-2],high[-1],pt)<=0:high.pop()
            high.append(pt)
        states+=low[:-1]+high[:-1]
    states=sorted(set(states));hull_units+=8*len(states)'''
assert before in s;s=s.replace(before,after).replace('30*bases+8*checks+20*len(states)','hull_units+30*bases+8*checks+20*len(states)').replace('"dep01"','"dep02"').replace('["dependence.py","dependent_scores.md"]','["dependence_hull.py","dependent_scores.md","dependence_hulls.md"]')
(p/'dependence_hull.py').write_text(s)
