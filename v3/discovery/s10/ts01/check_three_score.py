from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
import json, hashlib
root=Path(__file__).resolve().parent
def planes(k,h,x,y):
    result=[F(1),F(2*k-x-2*y,2*k-h),F(k-y,k-h//2)]
    if h<k:result.append(F(k-x-y,k-h))
    return min(result)
polygons=allocations=0
for k in range(1,33):
    for Q in range(1,2*k+1):
        h=Q-1;r=h//2
        # Axes, sum cap, score cap, parity cut: exact all feasible vertices.
        lines=[(1,0,0),(0,1,0),(1,1,k),(1,2,h),(0,1,r)]
        vertices=set()
        for (a,b,c),(d,e,f) in combinations(lines,2):
            det=a*e-b*d
            if not det:continue
            x,y=F(c*e-b*f,det),F(a*f-c*d,det)
            if x>=0 and y>=0 and x+y<=k and x+2*y<=h and y<=r:
                assert x.denominator==y.denominator==1
                vertices.add((x,y))
        assert vertices;polygons+=1
        for p1 in range(9):
            for p2 in range(9-p1):
                x,y=F(k*p1,8),F(k*p2,8);w=planes(k,h,x,y)
                assert 0<=w<=1
                s=max(F(0),x+y-(1-w)*k);f2=max(F(0),s-x);f1=s-f2
                assert 0<=f1<=x and 0<=f2<=y and f1+f2<=w*k
                assert f1+2*f2<=w*h and f2<=w*r
                assert 0<=(x-f1)+(y-f2)<=(1-w)*k
                if w==0:assert f1==f2==0
                if w==1:assert f1==x and f2==y
                allocations+=1
selection={'true_Y_one_probability':[1,2],'observed_Y_one_probability':[0,1],'X_sample_one_probability':[1,2],'rule':'X=Y; observe X always, Y iff X=0. First-purchase X is unbiased, later unique Y is selected.'}
result={'status':'pass','contributor':'Codex (GPT-6)','source_hashes':{f:hashlib.sha256((root/f).read_bytes()).hexdigest() for f in ['three_score_sharp.md','correlated_learning.md','check_three_score.py']},'integer_polygons':polygons,'exact_failure_mass_allocations':allocations,'marginal_grid_denominator':8,'maximum_prefix':32,'selection_counterexample':selection,'scope':'Finite exact screening of the separately written universal argument; includes all marginal-grid edges and vertices. No fee purchases or empirical calibration claim.'}
(root/'three_score_checked.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
