"""Exact finite linear description of a static request template's budget.

Distributing each Venn part among its allowed request labels is a fractional
load-balancing LP. Its dual ranges over probability weights on four requests.
Within each region cut out by equal label prices it is linear, so enumerate
the vertices of that hyperplane arrangement in the probability simplex.
"""
from fractions import Fraction as F
from itertools import combinations
from math import gcd
from functools import reduce
from pathlib import Path
import json


def minimal(L):return tuple(m for m in sorted(set(L)) if not any(n!=m and n&m==n for n in L))
def blocker(L):return minimal([m for m in range(1,16) if all(m&n for n in L)])
def det(a,b,c):return a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0])


def facets(triangle):
    labs=list(triangle)+[blocker(triangle[2]),blocker(triangle[1]),blocker(triangle[0])]
    planes={tuple(int(i==j) for i in range(4)) for j in range(4)}
    for L in labs:
        for a,b in combinations(L,2):
            row=tuple(((a>>i)&1)-((b>>i)&1) for i in range(4))
            if not any(row):continue
            g=reduce(gcd,map(abs,row));sign=1 if next(x for x in row if x)!=abs(next(x for x in row if x)) else -1
            planes.add(tuple(sign*x//g for x in row))
    eqs=[([a[i]-a[3] for i in range(3)],-a[3]) for a in sorted(planes)]
    vertices=set()
    for three in combinations(eqs,3):
        A=[row for row,b in three];b=[b for row,b in three];d=det(*A)
        if not d:continue
        point=[]
        for j in range(3):
            B=[[b[i] if h==j else A[i][h] for h in range(3)] for i in range(3)]
            point.append(F(det(*B),d))
        point.append(1-sum(point))
        if min(point)>=0:vertices.add(tuple(point))
    forms=set()
    for p in vertices:
        v=[min(sum(p[j] for j in range(4) if m>>j&1) for m in L) for L in labs]
        forms.add((v[3]+v[4]+v[5],v[0]-v[3]-v[4],v[1]-v[3]-v[5],v[2]-v[4]-v[5]))
    return sorted(forms),sorted(vertices)


if __name__=='__main__':
    from p644_static_templates import templates,solve
    import random
    rng=random.Random(644);out=[]
    for t in templates():
        fs,vs=facets(t)
        for j in range(4):
            point=[F(rng.randrange(21),50) for h in range(3)]
            exact=max(f[0]+sum(a*b for a,b in zip(f[1:],point)) for f in fs)
            numeric=solve(t,point,exact=False)
            assert numeric is not None and abs(float(exact)-numeric)<1e-8,(t,point,exact,numeric)
        out.append({'triangle':t,'forms':[list(map(str,f)) for f in fs],'vertices':[list(map(str,p)) for p in vs]})
    Path('logs/astra_static_template_facets.json').write_text(json.dumps(out,separators=(',',':')))
    print('PASS:',len(out),'templates;',sum(len(r['forms']) for r in out),'exact budget forms; numerical LP cross-checks agree')
