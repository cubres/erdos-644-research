#!/usr/bin/env python3
"""Referee w9 nonint#4: sensitivity. Both outcomes occur, and mutated staircase predicates disagree with exact SAT."""
from w9_ref_nonint4_check import setup, make_G, bad_exists
preds = {
 'claim a+b=6, <=': lambda g1,g2,d1,d2: any(g1<=a*d1 and g2<=(6-a)*d2 for a in range(1,6)),
 'mut a+b=7':       lambda g1,g2,d1,d2: any(g1<=a*d1 and g2<=(7-a)*d2 for a in range(1,7)),
 'mut a+b=5':       lambda g1,g2,d1,d2: any(g1<=a*d1 and g2<=(5-a)*d2 for a in range(1,5)),
 'mut strict <':    lambda g1,g2,d1,d2: any(g1<a*d1 and g2<(6-a)*d2 for a in range(1,6)),
}
for (k,d1,d2,w) in [(11,2,2,2),(12,2,1,2),(10,1,1,2)]:
    U1,U2,W,rows=setup(k,d1,d2,w); rs=set(rows); ground=U1+U2+W
    res=[]
    for g1 in range(k+1):
        for g2 in range(k-g1+1):
            for gw in range(min(w,k-g1-g2)+1):
                if g1+g2+gw==0: continue
                G=make_G(U1,U2,W,g1,g2,gw)
                if G in rs: continue
                res.append((g1,g2,bad_exists(ground,rows,forced=G) is not None))
    nb=sum(r[2] for r in res)
    print(f'k={k} d=({d1},{d2}): types {len(res)}, exact-bad {nb}, exact-good {len(res)-nb}')
    for name,P in preds.items():
        mism=sum(P(g1,g2,d1,d2)!=e for g1,g2,e in res)
        print(f'   {name:18s} mismatches {mism}')
