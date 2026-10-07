# Referee w5 (paper): exact-integer, construction-level check of Lemmas 5.1 and 5.3 (with 5.2 and 3.1
# conditions) as written, exhaustive over all cell sizes, with worst-case response traces
# (every size bound is monotone in the response counts).  No use of the paper's numeric shortcuts:
# each set size is recomputed from its definition.
import sys
from math import ceil
def cdiv(a,b): return -((-a)//b)
def check51(r):
    T0=cdiv(173*r,200); T=T0+4; h0=(23*r)//50
    assert T<=r
    ingap=lambda v: 200*v>=43*r and 50*v<=23*r
    Lm=max(v for v in range(r) if 200*v<43*r)
    n=0
    for x in range(0,r//2+1):
        if 50*x<23*r: continue
        yb=r-(T0+x)//2               # balanced request bound
        assert 50*yb<23*r            # < hr, so the gap forces y,z < lr
        ymax=min(yb,Lm)
        for y in range(ymax+1):
            for z in range(ymax+1):
                S=x+y+z
                if S<=T:
                    p=max(0,r-x-y-h0); t=max(0,r-x-z-h0)
                    assert p<=r-x-y and t<=r-x-z
                    C=x+y+z+p+t; assert C<=T
                    W=T-C; assert 0<=W<=r-y-z
                    eH=r-x-y-p; fH=r-x-z-p*0-t
                    assert 50*eH<=23*r and 50*fH<=23*r   # so gap applies
                    eH=min(eH,Lm); fH=min(fH,Lm)
                    b=r-y-z-W
                    assert x+cdiv(b,2)<=T
                    assert y+z+eH+fH<=T
                else:
                    assert x+y<=T and T-x-y<=z
                    cmax=r-x-y; fmax=r-(T-y)
                    assert 50*cmax<=23*r and 50*fmax<=23*r
                    cmax=min(cmax,Lm); qa=min(fmax,Lm)
                    qmax=min(S-T,qa); bmax=r-y-z
                    assert x+qmax+cdiv(bmax,2)<=T
                    assert y+z+qa+cmax<=T       # a<=q+a
                    tot=r+x+z+qmax+qa+bmax     # r+x+z+2q+a+b with q+a<=qa
                    assert tot<=3*T
                n+=1
    return n
def check53(r,bn=173,bd=200):
    T=cdiv(bn*r,bd)+4; assert T<=r
    assert 6*bn>=5*bd
    mcap=((3*bn-2*bd)*r)//(2*bd)
    n=0
    for m in range(0,mcap+1):
        # branch 1 / sub-branch: L18 budget
        B=max(cdiv(3*r+m,4),cdiv(2*r+2*m,3)); assert B<=T and 2*m<=r
        xmax=r-(T+m)//2
        for x in range(r//2+1,xmax+1):
            assert m<=r-T and 4*m<=r
            assert x+2*m<T
            for z in range(0,min(m,r-x)+1):
                pad=T-x-m-z; assert 1<=pad<=r-m-z
                assert 2*(r-x-m)<r and 2*(r-x-z)<r
                bmax=r-T+x
                if 2*bmax>r:
                    hr=cdiv(r,2)
                    assert T>=hr+2*m and T>=x+m and 3*T>=2*x+bmax+hr+2*m
                n+=1
    return n
if __name__=='__main__':
    lo,hi=int(sys.argv[1]),int(sys.argv[2])
    tot51=tot53=0
    for r in range(lo,hi+1):
        tot51+=check51(r); tot53+=check53(r)
    print('PASS r in [%d,%d]: 5.1 cases %d, 5.3 cases %d'%(lo,hi,tot51,tot53))
