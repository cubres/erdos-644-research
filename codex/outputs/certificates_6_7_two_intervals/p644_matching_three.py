"""Three static requests covering three disjoint candidate-pair components.

Used to discover a fourth-edge response-dependent template. The complete
antichain list and complete dual arrangement are finite and exact. Numerical
optimization over fourth-edge responses is only a search heuristic.
"""
from fractions import Fraction as F
from itertools import combinations,product
from functools import lru_cache
import numpy as np


def minimal(L):return tuple(m for m in sorted(set(L)) if not any(n!=m and n&m==n for n in L))


def blockers(L):return minimal([m for m in range(1,8) if all(m&n for n in L)])


def solve3(rows,rhs):
    A=[list(map(F,row))+[F(b)] for row,b in zip(rows,rhs)]
    for j in range(3):
        pivot=next((i for i in range(j,3) if A[i][j]),None)
        if pivot is None:return None
        A[j],A[pivot]=A[pivot],A[j];z=A[j][j];A[j]=[x/z for x in A[j]]
        for i in range(3):
            if i!=j:
                z=A[i][j];A[i]=[x-z*y for x,y in zip(A[i],A[j])]
    return tuple(row[-1] for row in A)


@lru_cache(None)
def model():
    ants=[]
    for mask in range(1,128):
        L=tuple(i+1 for i in range(7) if mask>>i&1)
        if minimal(L)==L:ants.append(L)
    assert len(ants)==18
    planes={tuple(int(i==j) for i in range(3)) for j in range(3)}
    for L in ants:
        for a,b in combinations(L,2):
            d=tuple(((a>>i)&1)-((b>>i)&1) for i in range(3))
            if next(v for v in d if v)<0:d=tuple(-v for v in d)
            planes.add(d)
    vertices=set()
    for pair in combinations(planes,2):
        p=solve3([(1,1,1)]+list(pair),[1,0,0])
        if p is not None and min(p)>=0:vertices.add(p)
    vertices=sorted(vertices)
    costs={L:tuple(min(sum(p[j] for j in range(3) if m>>j&1) for m in L) for p in vertices) for L in ants}
    templates=list(product(ants,repeat=3));coeff=[]
    for triple in templates:
        labs=[x for L in triple for x in (L,blockers(L))]
        forms=list(zip(*(costs[L] for L in labs)))
        coeff.append(forms)
    denominator=12
    arr=np.array([[[int(a*denominator) for a in f] for f in fs] for fs in coeff],dtype=np.int16)
    assert all(a*denominator==int(a*denominator) for fs in coeff for f in fs for a in f)
    return templates,vertices,arr,denominator


def best(weights,exact=False):
    templates,vertices,arr,den=model();w=np.asarray([float(F(x)) if isinstance(x,str) else float(x) for x in weights])
    costs=np.max(np.einsum('ijk,k->ij',arr,w),axis=1)/den
    i=int(np.argmin(costs))
    if not exact:return float(costs[i]),i
    w=list(map(F,weights));vals=[sum(F(int(a),den)*b for a,b in zip(row,w)) for row in arr[i]]
    return {'template':[list(L) for L in templates[i]],'budget':str(max(vals)),'index':i}


if __name__=='__main__':
    print('templates',len(model()[0]),'vertices',len(model()[1]),flush=True)
    for w in [('1/2',)*4+('0','0'),('77/200','2/5','77/200','2/5','43/800','1/5')]:
        print(w,best(w,True),flush=True)
