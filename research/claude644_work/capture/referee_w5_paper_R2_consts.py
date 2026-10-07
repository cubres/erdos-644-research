# Independent referee (R2) integer check of Step 1, Lemma 5.1, Lemma 5.3 numerics, worst cases looped exactly.
from fractions import Fraction as Fr
from math import ceil, floor
beta=Fr(173,200); h=Fr(23,50); l=Fr(43,200)
def cdiv(a): return ceil(a)
bad=[]
for r in range(1000,20001):
    cb=ceil(beta*r); K=cb+10; h0=floor(h*r); lr=ceil(l*r)  # pair ints < l r means <= lr-1
    ok = K<=r and beta*r+3<=K
    # Step 1
    for m in (lr, h0):
        yb = r-(K+m)//2
        ok &= yb < h0 and 200*(m+2*yb) <= 227*r and m <= K
    # Lemma 5.1
    T=cb+4; T0=cb; ok &= T<=r
    ymax=lr-1
    for x in range(ceil(h*r), r//2+1):
        g = r-(T0+x)//2; ok &= 50*g < 23*r
        # case S<=T
        C = max(x+2*ymax if x+2*ymax<=T else 0, r-h0+ymax, 2*r-x-2*h0 if r-x-h0>0 else x)
        ok &= C<=T and T<=r+x
        p=max(0,r-x-h0); t=p
        b=r-T+x+p+t; ok &= x+ceil(Fr(b,2))<=T and 4*ymax<T
        # case S>T (needs x+2ymax>T to occur)
        if x+2*ymax>T:
            ok &= x+ymax<T
            q=x+2*ymax-T; bb=r
            for yz in range(max(0,T-x+1),2*ymax+1):
                q=x+yz-T; b=r-yz
                ok &= x+q+ceil(Fr(b,2))<=T
            ok &= 2*r+2*x+ymax-T+ymax <= 3*T
    # Lemma 5.3 at beta'=beta
    ok &= Fr(5,6)<=beta and 2*floor((3*beta-2)/2*r)<=r
    mm=floor((3*beta-2)/2*r)
    ok &= ceil(max(Fr(3*r+mm,4),Fr(2*r+2*mm,3)))<=cb
    for m in range(0,r-T+1):
        x=r-(T+m)//2
        if 2*x<=r: continue
        b=r-T+x
        ok &= x+2*m<T and 4*m<=r and T>=ceil(Fr(r,2))+2*m and T>=x+m and 3*T>=2*x+b+ceil(Fr(r,2))+2*m and T<=r+x
    if not ok: bad.append(r)
print('fails',len(bad),bad[:10])
