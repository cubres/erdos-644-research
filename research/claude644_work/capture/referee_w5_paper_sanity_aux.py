# Referee (w5 sanity supplement): the auxiliary inequalities of Prop 4.1 that w5_paper_prop10_vertices.py
# does NOT check (u-bounds of (C), c1's 2m+3y>=346/200, c3's two branches, c4 Split A/B sub-claims),
# on the closed case polytopes, exact rationals, own vertex enumerator.  Each inequality is affine.
from fractions import Fraction as F
from itertools import combinations
b=F(173,200); e=1-b
def solve(A,B):
    import copy
    M=[list(A[i])+[B[i]] for i in range(3)]
    for c in range(3):
        p=next((i for i in range(c,3) if M[i][c]!=0),None)
        if p is None: return None
        M[c],M[p]=M[p],M[c]
        for i in range(3):
            if i!=c and M[i][c]!=0:
                f=M[i][c]/M[c][c]; M[i]=[a-f*bb for a,bb in zip(M[i],M[c])]
    return tuple(M[i][3]/M[i][i] for i in range(3))
def verts(cons):
    V=set()
    for tri in combinations(cons,3):
        s=solve([c[0] for c in tri],[c[1] for c in tri])
        if s and all(sum(a*x for a,x in zip(c[0],s))<=c[1] for c in cons): V.add(s)
    return V
def le(a,c): return (tuple(map(F,a)),F(c))
def ge(a,c): return (tuple(-F(t) for t in a),-F(c))
R=[ge((0,0,1),0),ge((0,1,-1),0),ge((1,-1,0),0),le((1,0,0),F(92,200)),le((1,2,0),2-b)]
Cc=R+[ge((0,1,0),F(73,200))]
c1=Cc+[le((2,2,1),F(319,200))]
nc1=Cc+[ge((2,2,1),F(319,200))]
c3=nc1+[ge((1,-1,1),e),le((0,1,2),F(146,200))]
c4=nc1+[ge((1,-1,1),e),ge((0,1,2),F(146,200))]
c4A=c4+[ge((-1,-1,3),e)]; c4B=c4+[le((-1,-1,3),e)]
checks={
 'C: u>=146/200':(Cc,lambda m,y,z:m+y-F(146,200)),
 'C: u<=154/200':(Cc,lambda m,y,z:F(154,200)-m-y),
 'c1: 2m+3y>=346/200':(Cc,lambda m,y,z:2*m+3*y-F(346,200)),
 'c1: y-m/2>=e':(Cc,lambda m,y,z:y-m/2-e),
 'c3: 2m+y>=219/200':(Cc,lambda m,y,z:2*m+y-F(219,200)),
 'c3Q0: 73/200-y/2<=m-e':(c3,lambda m,y,z:m-e-(F(73,200)-y/2)),
 'c3Q0: y+z<beta':(c3,lambda m,y,z:b-y-z),
 'c3Qpos: y>=2e':(c3,lambda m,y,z:y-2*e),
 'c4A: 2y+e<=3m':(c4A,lambda m,y,z:3*m-2*y-e),
 'c4A: m+e<=2y':(c4A,lambda m,y,z:2*y-m-e),
 'c4A: z>=d-e':(c4A,lambda m,y,z:z-(m-y)+e),
 'c4A: total (3e+S)/2<=beta':(c4A,lambda m,y,z:b-(3*e+m+y+z)/2),
 'c4B: z>=e-d (m1<=m)':(c4B,lambda m,y,z:z-e+(m-y)),
 'c4B: total 2e+u-z<=beta':(c4B,lambda m,y,z:b-(2*e+m+y-z)),
}
allok=True
for k,(cons,f) in checks.items():
    V=verts(cons); mn=min(f(*v) for v in V); ok=mn>=0; allok&=ok
    print(f'{k:32s} verts={len(V):2d} min slack={str(mn):>10s} {"ok" if ok else "FAIL"}')
print('ALL AUX OK' if allok else 'AUX FAILURE')
