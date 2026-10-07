"""Small exact certificate against all Fano/V4 repeated-response partner boxes.

Run python3 -B -S. No orbit file, numerical solver, or optimizer is used.
Fix one U occurrence at Fano row6; transitivity covers all assignments with U.
The five escaped orthants and 36 cut maps certify terminal cost>=189/250.
"""
from fractions import Fraction as F
from itertools import product

X=tuple(F(v,100000) for v in (76000,75000,75000))
T=tuple(tuple(F(v,100000) for v in row) for row in
        ((50849,0,49151),(0,50099,49901),(0,49951,50049)))
PENCIL=((0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5))
# Zero coordinates impose no restriction; positive thresholds are strict.
CORNERS=tuple(tuple(F(v,1000) for v in row) for row in
              ((0,0,429),(507,251,11),(0,500,380),
               (249,626,18),(498,501,0)))


def cap_from_forms(roles,forms):
    cap=list(X)
    for coefficients,rhs in forms:
        count=sum(q for q,k in zip(coefficients,roles) if k==3)
        for i in range(3):
            fixed=sum(q*T[k][i] for q,k in zip(coefficients,roles) if k!=3)
            if not count:
                if fixed>rhs*X[i]:return None
            else:cap[i]=min(cap[i],(rhs*X[i]-fixed)/count)
    return tuple(cap)


def check_cap(cap):
    if cap is None or min(cap)<0 or sum(cap)<1:return
    assert all(any(low>0 and low>=v for low,v in zip(corner,cap))
               for corner in CORNERS),(cap,CORNERS)


def main():
    fforms=[(tuple(F(int(j in p)) for j in range(7)),F(2)) for p in PENCIL]
    fforms.append(((F(1),)*7,F(4)))
    for six in product(range(4),repeat=6):check_cap(cap_from_forms(six+(3,),fforms))
    # Roles a,b,c,d give row pattern b,c,d,d,d,d,a.
    vrows=((4,0,0,0),(0,4,0,0),(0,0,4,0),(2,2,2,0),
           (0,2,2,4),(1,1,1,4))
    vforms=[(tuple(map(F,row)),F(4)) for row in vrows]
    n=0
    for roles in product(range(4),repeat=4):
        if 3 not in roles:continue
        n+=1;check_cap(cap_from_forms(roles,vforms))
    assert n==175
    choices=[[i for i,v in enumerate(c) if v>0] for c in CORNERS]
    best=(F(0),None)
    for cutmap in product(*choices):
        u=list(X)
        for co,i in zip(CORNERS,cutmap):u[i]=min(u[i],co[i])
        if sum(u)>best[0]:best=(sum(u),tuple(u))
    assert best==(F(188,125),(F(249,500),F(313,500),F(19,50)))
    assert sum(X)-best[0]==F(189,250)
    print('PASS: all4096 Fano assignments and175 V4 role assignments miss all5 orthants.')
    print('PASS: all36 orthant-blocking cut maps retain at most188/125, hence cost>=189/250=.756>3/4.')


if __name__=='__main__':main()
