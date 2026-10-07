# Verify nerve reformulations on random 7-tuples (exhaustive over small ground sets, random).
import itertools, random
LINES=[(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
PTS=range(7)
PENCIL={p:[i for i,l in enumerate(LINES) if p in l] for p in PTS}
def two_pierce(G,V):
    for x in V:
        for y in V:
            if all(x in g or y in g for g in G): return True
    return False
def fano_labelable(G,V):
    # every x has a point p with x in no G_l, l through p
    return all(any(all(x not in G[i] for i in PENCIL[p]) for p in PTS) for x in V)
def pencils_empty(G):
    return all(not (G[a]&G[b]&G[c]) for (a,b,c) in (PENCIL[p] for p in PTS))
def split_two_stars(G):
    idx=range(7)
    for mask in range(128):
        A=[G[i] for i in idx if mask>>i&1]; B=[G[i] for i in idx if not mask>>i&1]
        def star(F):
            if not F: return True
            s=set(F[0])
            for f in F[1:]: s&=f
            return bool(s)
        if star(A) and star(B): return True
    return False
random.seed(1)
cnt=[0]*4
for trial in range(60000):
    n=random.randint(3,9); V=list(range(n))
    G=[frozenset(v for v in V if random.random()<random.choice([.3,.5,.7])) for _ in range(7)]
    if any(len(g)==0 for g in G): continue
    tp=two_pierce(G,V); fl=fano_labelable(G,V); pe=pencils_empty(G); st=split_two_stars(G)
    assert tp==st, "2-pierceable <=> two stars"
    assert fl==pe, "Fano-labelable <=> pencil triples empty"
    if fl: assert not tp, "Fano => bad"
    cnt[0]+=1; cnt[1]+=(not tp); cnt[2]+=fl
print("checked",cnt[0],"tuples; bad",cnt[1],"Fano-bad",cnt[2],": ALL PASS")
