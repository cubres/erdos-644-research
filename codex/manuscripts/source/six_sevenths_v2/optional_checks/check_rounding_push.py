#!/usr/bin/env python3
"""Finite exact transcription check; NOT a proof of the universal theorem.

Standard library only. The hand proof is outputs/submission_644_rounding_push.md.
All tests below use integer arithmetic and the stated branch, not menu search.
"""
from argparse import ArgumentParser


def l29(k,T,x,y,z):
    return k+x+y+z<=2*T and k-x+abs(y-z)<=T and k+3*x<=3*T

def l31(k,T,x,y,z):
    S=x+y+z
    return all((x+y<=T,k+2*x<=2*T,k+2*y<=2*T,
                k+x-y-z<=T,k-x+y-z<=T,3*k-S<=3*T,
                3*k+S<=5*T,k+x+y+2*z<=3*T,2*k+3*z<=4*T))

def l32(k,T,x,y,z):
    return all((x+y+z<=T,k+2*y<=2*T,k+2*x-y+z<=2*T,
                k+2*x+y+3*z<=3*T))

def l33(k,T,x,y,z):
    return all((x+y+z<=T,k+3*x<=3*T,k-x+z<=T,k+2*x+3*y+z<=3*T))

def s1(k,T,m,y,z):
    assert m>=y>=z
    return all((k+m-y-z<=T,k+m<=2*T,2*k+m+y-z<=3*T,
                3*k+m+y+z<=5*T))

def s0(k,T,a,b,c):
    return all((T>=a,T>=a+b,T>=a+c,T>=b+c,
                k+2*c<=2*T,k+2*b<=2*T,k+3*a<=3*T,
                2*k+b+c<=3*T,2*k+2*a+c<=4*T,
                2*k+2*a+b<=4*T,3*k+a<=4*T))

def g0(k,T,H,L,x,y,z):
    p=max(0,k-x-y-H); t=max(0,k-x-z-H)
    return all((x+y+z+p+t<=T,k+3*x+p+t<=3*T,y+z+2*L<=T))

def g1(k,T,H,L,x,y,z):
    Q=max(0,x+y+z-T)
    return all((x+y<=T,k-x-y<=H,k-x-z+Q<=H,
                2*x+2*Q+k-y-z<=2*T,y+z+2*L<=T,
                2*k+x-y+L+Q<=3*T))

def g2(k,T,H,L,x,y,z):
    g=max(0,k-y-H)
    return all((g<=x,g<=z,y+2*g<=T,x+L<=T,z+L<=T,
                k+2*y<=2*T,3*k<=4*T,3*k+x+y+z<=5*T))

def nc(k,T,m,x,y,z):
    S=x+y+z; delta=max(0,S-T)
    common=(y+z<=T,m+z<=T,k+y-z<=T,2*k+x-2*z<=2*T,
            2*k+x+m-z<=3*T,x+m<=T)
    if S<=T:
        return all((*common,k-x+y<=T,2*k-2*x+z<=2*T))
    return all((*common,k-x+y+delta<=T,2*k-2*x+z+delta<=2*T,
                2*k-z+delta<=2*T,3*k-x-y+delta<=3*T))

def endpoints(k):
    h,s=divmod(k,7);T=k-h;A=T//2;B=(4*T-2*k)//3
    C=T-(k+1)//2;D=2*k-T-2*B;L=D-1;U=2*T-k-(k+1)//2
    assert 6*k<=7*T and T<=k and B>=A and B>=3*h
    assert L<=U and 4*L<=T and k-B-1+L<=T
    assert 6*T>5*k+1 and 3*T>=2*k+(k+1)//2
    assert 4*T>=3*k+1 and 12*T>=10*k+4
    if B<k//2:
        assert 1<=D<=C
    return h,T,A,B,C,D,L

def exhaustive(k, counts):
    h,T,A,B,C,D,L=endpoints(k)
    for x in range(A+1,min(B,k//2)+1):
        assert 0<=2*k-T-x<=2*C and C<=k-x
        for y in range(C+1):
            for z in range(y+1):
                d=y-z;v=y+z
                if d>x-h:
                    okay=l32(k,T,x,y,z); label='stage1_l32'
                elif v<=3*T-k-2*x:
                    okay=l31(k,T,y,z,x); label='stage1_l31'
                else:
                    okay=s1(k,T,x,y,z); label='stage1_s1'
                assert okay,(label,k,T,x,y,z)
                counts[label]=counts.get(label,0)+1
    if B<k//2:
        for x in range(D,C+1):
            assert 0<=2*k-T-x<=2*B and B<=k-x
            for y in range(A+1):
                for z in range(y+1):
                    if x+z>=k-B:
                        okay=g2(k,T,B,A,y,x,z);label='stage2_g2'
                    else:
                        okay=s0(k,T,y,x,z);label='stage2_s0'
                    assert okay,(label,k,T,x,y,z)
                    counts[label]=counts.get(label,0)+1
        J=(h-(k-7*h))//2
        assert J==2*k-C+2*(k//2)-3*T
        for x in range(B+1,k//2+1):
            assert 0<=2*k-T-x<=2*C and C<=k-x
            for y in range(L+1):
                for z in range(y+1):
                    S=x+y+z
                    if S<=2*T-k:
                        okay=l29(k,T,x,y,z);label='stage3_l29'
                    elif S<=T and z<J:
                        okay=l33(k,T,x,z,y);label='stage3_l33'
                    elif S<=T:
                        okay=g0(k,T,C,L,x,y,z);label='stage3_g0'
                    else:
                        okay=g1(k,T,C,L,x,y,z);label='stage3_g1'
                    assert okay,(label,k,T,x,y,z)
                    counts[label]=counts.get(label,0)+1
    for m in range(A+1):
        for y in range(m+1):
            for z in range(y+1):
                S=m+y+z
                if 2*y<=2*T-k:
                    if y-z>m-h:
                        okay=l32(k,T,m,y,z);label='finish_l32a'
                    elif S<3*h:
                        okay=l32(k,T,z,y,m);label='finish_l32b'
                    else:
                        okay=l31(k,T,z,y,m);label='finish_l31'
                elif h<z and 2*z<=2*T-k:
                    okay=g2(k,T,k//2,m,m,z,y);label='finish_g2'
                elif 2*z>2*T-k:
                    okay=s1(k,T,m,y,z);label='finish_s1'
                else:
                    okay=nc(k,T,m,m,z,y);label='finish_nc'
                assert okay,(label,k,T,m,y,z)
                counts[label]=counts.get(label,0)+1

if __name__=='__main__':
    ap=ArgumentParser();ap.add_argument('--max-rank',type=int,default=84)
    args=ap.parse_args();counts={}
    for k in range(8,10001): endpoints(k)
    for k in range(8,args.max_rank+1): exhaustive(k,counts)
    print('PASS: endpoint identities ranks8..10000; prescribed branch inequalities ranks8..'+str(args.max_rank))
    print('Exact integer triple checks:',sum(counts.values()))
    for key,value in sorted(counts.items()):print(key,value)
    print('Finite transcription check only; universal proof is in the report.')
