"""How far does each stage reach at budget t (continuous, formula lemmas only)?"""
import numpy as np, sys
from lemmas import split, asym1, asym2, four, sym, s0, g0, g1, g2, nc
def closes(x,y,z,t,gaps=(),dich=None):
    for f in (split,asym1,asym2,four,sym,s0):
        if f(x,y,z)<=t+1e-9: return True
    for lo,hi in gaps:
        if g0(x,y,z,lo,hi)<=t+1e-9 or g1(x,y,z,lo,hi,t) or g2(x,y,z,lo,hi,t): return True
    if dich is not None:
        if nc(x,y,z,dich,t) or g0(x,y,z,dich,0.5)<=t+1e-9 or g1(x,y,z,dich,0.5,t) or g2(x,y,z,dich,0.5,t): return True
    return False
def box_ok(x,cap_y,cap_z,t,N=16,**kw):
    for y in np.linspace(0,cap_y,N):
        for z in np.linspace(0,cap_z,N):
            if not closes(x,y,z,t,**kw): return (False,(x,y,z))
    return (True,None)
def finisher_reach(t,N=16):
    # largest M such that (M,y,z), y,z<=min(M,1-(t+M)/2) all close with dichotomy
    last=None
    for M in np.linspace(0.1,0.5,81):
        cap=min(M,1-(t+M)/2)
        ok,w=box_ok(M,cap,cap,t,N,dich=M)
        if not ok: return last,w
        last=M
    return last,None
def stage1_interval(t,N=16):
    # q with caps u=v=(2-t-q)/2 (balanced), no gap
    oks=[]
    for q in np.linspace(0.3,0.5,81):
        cap=(2-t-q)/2
        ok,_=box_ok(q,min(cap,1),min(cap,1),t,N)
        oks.append((round(q,4),ok))
    return oks
if __name__=='__main__':
    for t in [6/7,0.855,0.85,0.845,0.84]:
        fr=finisher_reach(t)
        s1=[q for q,ok in stage1_interval(t) if ok]
        print('t=%.4f finisher reaches M<=%s (fail %s); stage1 balanced-caps closes q in [%s..%s] (%d pts)'%(t,fr[0],fr[1],s1[0] if s1 else None,s1[-1] if s1 else None,len(s1)),flush=True)
