# Referee (w4 handbound, verification claim): EXHAUSTIVE small-r check of the lemma strategies in
# w4_handbound_e2e_lemmas.py. The adaptive response H ranges over ALL region-count vectors (with several
# representative choices inside each region); the final responses are handled EXACTLY: a pair {p,q} is a
# 2-transversal of the final <=7 edges for SOME legal final responses iff every fixed edge meets {p,q} and
# no final request contains both p and q. So we check: every pair of points is missed by a fixed edge or
# contained in a final request. Also checks every request has size <= T.
import sys, itertools, random
sys.path.insert(0,'.')
import w4_handbound_e2e_lemmas as L
class ExGame:
    def __init__(s,r,T,Hspec=None,rng=None):
        s.r=r;s.T=T;s.nxt=0;s.edges=[];s.calls=0;s.Hspec=Hspec;s.reqs=[];s.firstD=None;s.rng=rng
    def fresh(s,k):
        out=list(range(s.nxt,s.nxt+k)); s.nxt+=k; return out
    def respond(s,D):
        D=set(D); assert len(D)<=s.T,('req too big',len(D),s.T)
        s.calls+=1
        if s.Hspec is not None and s.calls==1:
            s.firstD=D
            H=s.Hspec(s,D)
            s.H=H; return H
        s.reqs.append(D); return set(s.fresh(s.r))
def covered(fixed,reqs):
    U=sorted(set().union(*fixed))
    # single point transversal of fixed edges must lie in every request (impossible to avoid otherwise)
    for p in U:
        if all(p in e for e in fixed):
            if not any(p in D for D in reqs): return ('single',p)
    for i,p in enumerate(U):
        for q in U[i+1:]:
            if all((p in e) or (q in e) for e in fixed):
                if not any((p in D and q in D) for D in reqs): return (p,q)
    return None
def regions(g,D):
    E,F,G=g.edges
    reg={}
    for p in range(g.nxt):
        if p in D: continue
        key=(p in E,p in F,p in G)
        reg.setdefault(key,[]).append(p)
    return [reg[k] for k in sorted(reg)]
def make_spec(vec,repmode,seed):
    def spec(g,D):
        R=regions(g,D); H=set()
        rr=random.Random(seed)
        for pts,c in zip(R,vec):
            pts=list(pts)
            if repmode==0: ch=pts[:c]
            elif repmode==1: ch=pts[len(pts)-c:]
            else: rr.shuffle(pts); ch=pts[:c]
            H|=set(ch)
        H|=set(g.fresh(g.r-len(H))); return H
    return spec
def vecs(sizes,r):
    def rec(i,left):
        if i==len(sizes): yield (); return
        for c in range(min(sizes[i],left)+1):
            for rest in rec(i+1,left-c): yield (c,)+rest
    yield from rec(0,r)
ADAPT=(('L26',L.T_L26,L.run_L26),('L32',L.T_L32,L.run_L32),('L31',L.T_L31,L.run_L31))
def main(rmin,rmax,reps):
    st={};fails=[]
    for r in range(rmin,rmax+1):
        for x in range(r+1):
            for y in range(r+1-x):
                for z in range(r+1-max(x,y)):
                    for name,Tf,run in ADAPT:
                        T=Tf(r,x,y,z)
                        if T>r: continue
                        # probe to get request D of H and regions
                        g0=ExGame(r,T,Hspec=lambda g,D:set(g.fresh(g.r)))
                        run(g0,x,y,z); R=regions(ExGame.__new__(ExGame) if False else g0,g0.firstD) if False else None
                        g0=ExGame(r,T); g0.Hspec=None
                        # recompute regions after triple+first request
                        cap={}
                        def spec_probe(g,D):
                            cap['sizes']=[len(p) for p in regions(g,D)]; return set(g.fresh(g.r))
                        gp=ExGame(r,T,Hspec=spec_probe); run(gp,x,y,z)
                        for vec in vecs(cap['sizes'],r):
                            for rep in range(reps):
                                g=ExGame(r,T,Hspec=make_spec(vec,rep,hash((r,x,y,z,vec,rep))))
                                try:
                                    run(g,x,y,z)
                                except AssertionError as e:
                                    fails.append((name,r,x,y,z,T,vec,'assert',str(e))); continue
                                bad=covered(g.edges[:3]+[g.H],g.reqs)
                                if bad: fails.append((name,r,x,y,z,T,vec,bad))
                                st[name]=st.get(name,0)+1
        # static: L18, P0, P4
        for x in range(r+1):
            for y in range(r+1-x):
                for z in range(r+1-max(x,y)):
                    T=L.T_P0(r,x,y,z)
                    if T is not None:
                        g=ExGame(r,T); L.run_P0(g,x,y,z); bad=covered(g.edges[:3],g.reqs)
                        if bad: fails.append(('P0',r,x,y,z,T,bad))
                        st['P0']=st.get('P0',0)+1
                    for T in range(r//2,r+1):
                        sp=L.P4_splits(r,x,y,z,T)
                        if sp:
                            g=ExGame(r,T); L.run_P4(g,x,y,z,*sp); bad=covered(g.edges[:3],g.reqs)
                            if bad: fails.append(('P4',r,x,y,z,T,bad))
                            st['P4']=st.get('P4',0)+1; break
                    xs=sorted((x,y,z),reverse=True); M=xs[0]
                    if 2*M<=r:
                        B=max(L.ceil(L.Fr(3*r+M,4)),L.ceil(L.Fr(2*r+2*M,3)))
                        if B<=r:
                            g=ExGame(r,B)
                            try:
                                L.run_L18(g,*xs); bad=covered(g.edges[:3],g.reqs)
                            except AssertionError as e: bad=('assert',str(e))
                            if bad: fails.append(('L18',r,xs,B,bad))
                            st['L18']=st.get('L18',0)+1
        print('r',r,st,'fails',len(fails),fails[:3],flush=True)
    print('DONE',st,'FAILS',len(fails))
if __name__=="__main__":
    main(int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]))
