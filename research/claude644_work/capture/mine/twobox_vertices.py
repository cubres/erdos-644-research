"""Two one-sided boxes A,B (+ merged light part L): which line->box assignments (PSL(2,7) orbit reps,
rows' non-box mass anywhere) are feasible at EVERY vertex of the closed domain with tau*>=3/4?
Vertices: A,B in {(0,0),(1,1),(7/4,1)}, x_L in {0,7/4}, subject to d_A+d_B+(3/7)x_L>=3/4, t_A+t_B+x_L>=1."""
import itertools, numpy as np
from scipy.optimize import linprog
from threebox_fano import LSET, REPS as REP3
LINES = [sorted(l) for l in LSET]
def feasible(xs, ths, box):
    # parts: 0=A,1=B,2=L (L has no box); explicit class-mass LP
    p = 3; nA = 7*p; nv = nA + 7*p
    ai = lambda l,i: l*p+i; ci = lambda i,q: nA+i*7+q
    A=[];b=[]
    for i in range(p):
        r=np.zeros(nv)
        for q in range(7): r[ci(i,q)]=1
        A.append(r); b.append(xs[i])
    for l,line in enumerate(LINES):
        for i in range(p):
            r=np.zeros(nv); r[ai(l,i)]=1
            for q in range(7):
                if q not in line: r[ci(i,q)]=-1
            A.append(r); b.append(0)
        r=np.zeros(nv)
        for i in range(p): r[ai(l,i)]=-1
        A.append(r); b.append(-1)
    bounds=[((ths[i] if box[l]==i else 0), xs[i]) for l in range(7) for i in range(p)]+[(0,None)]*(7*p)
    return linprog(np.zeros(nv),A_ub=np.array(A),b_ub=np.array(b),bounds=bounds,method='highs').status==0
tri=[(0,0),(1,1),(1.75,1)]
verts=[]
for a in tri:
    for bb in tri:
        for xL in (0,1.75):
            d=(a[0]-a[1])+(bb[0]-bb[1])+3/7*xL; th=a[1]+bb[1]+xL
            if d>=0.75-1e-12 and th>=1-1e-12: verts.append(((a[0],bb[0],xL),(a[1],bb[1],0)))
print(len(verts),"vertices")
reps2=sorted({tuple(min(v,1) for v in r) for r in REP3})  # 2-colourings (boxes 0,1) up to symmetry-ish
reps2=[r for r in reps2]
good=[]
for box in reps2:
    if all(feasible(xs,ths,box) for xs,ths in verts): good.append(box)
print("assignments feasible at all vertices:", good)
