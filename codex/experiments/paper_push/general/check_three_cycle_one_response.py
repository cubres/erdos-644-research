"""Exact diagnostic for the hand directed-cycle one-response theorem.

This finite replay checks the actual displayed Fano pencils / V4 facets,
not a sufficient-region solver. The proof is in the companion hand report.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import random

LINES = ((0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5))
PENCILS = tuple(tuple(i for i,L in enumerate(LINES) if q in L) for q in range(7))


def check(x, rows):
    x=tuple(map(F,x));rows=[tuple(map(F,r)) for r in rows]
    s=tuple(rows[i][i] for i in range(3));e=tuple(x[i]-s[i] for i in range(3));E=sum(e)
    assert min(x)>=F(3,4) and E>F(3,4)
    assert all(sum(r)==1 and all(0<=r[i]<=x[i] for i in range(3)) for r in rows)
    assert all(s[i]>2*x[i]/3 for i in range(3))
    assert all(e[i]+e[j]<F(3,4) for i in range(3) for j in range(i))
    assert all(rows[i][(i+2)%3]<=e[(i+2)%3] for i in range(3))
    failed=next((i for i in range(3) if s[i]+2*rows[(i+2)%3][i]>2*x[i]),None)
    if failed is None:
        d=tuple(max(F(0),rows[(i+2)%3][i]-e[i]) for i in range(3))
        r=tuple(x[i]-d[i] for i in range(3))
        pattern=(1,1,2,0,2,0,3);kind='all_Q'
    else:
        order=((failed+2)%3,failed,(failed+1)%3)
        x=tuple(x[i] for i in order)
        rows=[tuple(rows[j][i] for i in order) for j in order]
        s=tuple(rows[i][i] for i in range(3));e=tuple(x[i]-s[i] for i in range(3))
        a,b,c=rows
        assert e[1]<F(1,4) and e[2]>F(1,4) and e[0]+e[1]<F(1,2)
        if c[0]<=e[0]:
            assert all(b[i]+2*c[i]<=2*x[i] and 2*a[i]+2*c[i]<=2*x[i]
                       and 4*a[i]+b[i]+2*c[i]<=4*x[i] for i in range(3))
            return 'failed_Q_V4'
        d=(max(F(0),2*c[0]-x[0]),a[1]-e[1],s[2]-e[2])
        r=tuple(x[i]-d[i] for i in range(3))
        raw=tuple(min(x[i],2*x[i]-2*c[i],2*x[i]-a[i]-b[i],
                      4*x[i]-2*a[i]-2*b[i]-2*c[i]) for i in range(3))
        assert r==raw
        pattern=(2,0,0,1,1,2,3);kind='failed_Q_Fano'
    assert all(0<=r[i]<=x[i] for i in range(3))
    assert sum(x)-sum(r)<F(3,4)
    extended=rows+[r]
    loads=[extended[t] for t in pattern]
    assert all(sum(loads[j][i] for j in pencil)<=2*x[i]
               for pencil in PENCILS for i in range(3))
    assert all(sum(row[i] for row in loads)<=4*x[i] for i in range(3))
    return kind


def main():
    counts=Counter()
    targets=[
        ((754,751,784),((503,497,0),(0,511,489),(477,0,523))),
        ((754,751,960),((503,497,0),(0,511,489),(240,60,700))),
        ((760,760,760),((507,493,0),(0,507,493),(493,0,507))),
        ((910,910,910),((650,175,175),(175,650,175),(175,175,650))),
    ]
    for x,r in targets:counts[check([F(v,1000) for v in x],[[F(v,1000) for v in row] for row in r])]+=1
    rng=random.Random(64492631);accepted=0
    for _ in range(100000):
        xi=[rng.randint(750,1250) for i in range(3)]
        si=[rng.randint(2*v//3+1,min(v,1000)) for v in xi]
        ei=[v-s for v,s in zip(xi,si)]
        if sum(ei)<=750 or any(ei[i]+ei[j]>=750 for i in range(3) for j in range(i)):continue
        rows=[]
        for i in range(3):
            row=[0,0,0];row[i]=si[i];left=1000-si[i]
            rev=(i+2)%3;direct=(i+1)%3
            q=rng.randint(0,min(left,ei[rev]));row[rev]=q;row[direct]=left-q;rows.append(row)
        counts[check([F(v,1000) for v in xi],[[F(v,1000) for v in row] for row in rows])]+=1
        accepted+=1
        if accepted==3000:break
    result={'status':'PASS_EXACT_DIAGNOSTIC','random_states':accepted,'targeted_states':len(targets),'branches':dict(counts),
            'scope':'Finite exact construction replay only; the universal assertion has the separate hand proof.'}
    Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))


if __name__=='__main__':main()
