"""Fast rationally checked LPs on reusable four-request label templates."""
from fractions import Fraction as F
from itertools import permutations,product
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog
from p644_strategy_lp import recover


def minimal(L):return tuple(m for m in sorted(set(L)) if not any(n!=m and n&m==n for n in L))


def blocker(L):return minimal([m for m in range(1,16) if all(m&n for n in L)])


def templates():
    triangles=[((7,),(10,),(12,))]
    for path in ['logs/astra_static_four.json','logs/astra_gap_followup_static.json']:
        for row in json.loads(Path(path).read_text()):
            if row['status']!='EXACT_WITNESS':continue
            ls=tuple(minimal(list(map(int,P))) for P in row['parts'][:3])
            if all(ls):triangles.append(ls)
    out=[];seen=set()
    for triangle in triangles:
        for perm in permutations(range(3)):
            t=tuple(triangle[p] for p in perm)
            if t in seen:continue
            assert all(a&b for p,q in [(0,1),(0,2),(1,2)] for a,b in product(t[p],t[q]))
            seen.add(t);out.append(t)
    return out


def matrix(t):
    labs=list(t)+[blocker(t[2]),blocker(t[1]),blocker(t[0])]
    cols=[(p,m) for p,L in enumerate(labs) for m in L]
    Ae=np.zeros((6,len(cols)+1));Au=np.zeros((4,len(cols)+1));Au[:,-1]=-1
    for j,(p,m) in enumerate(cols):
        Ae[p,j]=1
        for h in range(4):Au[h,j]=(m>>h)&1
    return cols,Ae,Au


def solve(t,triple,exact=True):
    x,y,z=map(F,triple);weights=[x,y,z,1-x-y,1-x-z,1-y-z]
    if min(weights)<0:return None
    cols,Ae,Au=matrix(t);c=np.zeros(len(cols)+1);c[-1]=1
    q=linprog(c,A_eq=Ae,b_eq=np.array(weights,dtype=float),A_ub=Au,b_ub=np.zeros(4),bounds=(0,None),method='highs')
    if q.status!=0:return None
    if not exact:return q.fun
    v=recover(q.x)
    if any(a<0 for a in v) or any(sum((v[j] for j,(p,m) in enumerate(cols) if p==h),F(0))!=w for h,w in enumerate(weights)):return None
    if any(sum(v[j] for j,(p,m) in enumerate(cols) if m>>h&1)>v[-1] for h in range(4)):return None
    return {'triple':list(map(str,(x,y,z))),'budget':str(v[-1]),
            'triangle_labels':[list(L) for L in t],
            'parts':[{str(m):str(v[j]) for j,(p,m) in enumerate(cols) if p==h and v[j]>0} for h in range(6)]}


if __name__=='__main__':
    ts=templates();print('TEMPLATES',len(ts),flush=True)
    worst=(0,None);uncovered=[]
    for i in range(1,21):
        for j in range(i+1):
            for k in range(j+1):
                point=[F(i,50),F(j,50),F(k,50)]
                vals=[(solve(t,point,exact=False),n) for n,t in enumerate(ts)]
                val,idx=min((v,n) for v,n in vals if v is not None)
                if val>worst[0]:worst=(val,[str(v) for v in point]);print('WORST',worst,flush=True)
                if val>0.87+1e-8:uncovered.append({'point':list(map(str,point)),'budget':val})
        print('LAYER',i,'uncovered',len(uncovered),flush=True)
    Path('logs/astra_static_cap_grid.json').write_text(json.dumps({'templates':ts,'worst':worst,'uncovered':uncovered},indent=1))
