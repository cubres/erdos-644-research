# End-to-end integer verification of the static/adaptive lemmas used in the hand proof.
# Adversary: random responses (size r, avoiding the request), mixing old and fresh points, biased to
# maximise traces. Checks: every request has size <= T, and the final <=7 edges have no 2-point transversal.
import random, itertools, sys
class Game:
    def __init__(s,r,T,seed):
        s.r=r; s.T=T; s.rng=random.Random(seed); s.nxt=0; s.edges=[]; s.maxreq=0
    def fresh(s,k):
        out=list(range(s.nxt,s.nxt+k)); s.nxt+=k; return out
    def respond(s,D):
        D=set(D); assert len(D)<=s.T, ('request too big',len(D),s.T); s.maxreq=max(s.maxreq,len(D))
        old=[p for p in range(s.nxt) if p not in D]
        mode=s.rng.random()
        if mode<0.5:
            k=min(len(old),s.r)
        else:
            k=s.rng.randint(0,min(len(old),s.r))
        # bias: prefer points of existing edges
        s.rng.shuffle(old)
        if s.rng.random()<0.5 and s.edges:
            e=s.rng.choice(s.edges); pref=[p for p in old if p in e]; rest=[p for p in old if p not in e]; old=pref+rest
        H=set(old[:k])|set(s.fresh(s.r-k))
        return H
def two_transversal(edges):
    U=sorted(set().union(*edges))
    for p in U:
        if all(p in e for e in edges): return (p,)
    # pairs: p must be in edges; for speed, pick p then need q covering complement
    for p in U:
        rest=[e for e in edges if p not in e]
        common=set.intersection(*rest) if rest else set(U)
        if common: return (p,next(iter(common)))
    return None
def triple(g,x,y,z):
    # E,F,G with X=E&F (x), Y=E&G (y), Z=F&G (z) -- lemma-notation
    r=g.r
    X=set(g.fresh(x));Y=set(g.fresh(y));Z=set(g.fresh(z))
    PE=set(g.fresh(r-x-y));PF=set(g.fresh(r-x-z));PG=set(g.fresh(r-y-z))
    E=X|Y|PE;F=X|Z|PF;G=Y|Z|PG
    g.edges=[E,F,G]
    return E,F,G,X,Y,Z,PE,PF,PG
def take(S,k):
    S=sorted(S); assert 0<=k<=len(S),(k,len(S)); return set(S[:k])
