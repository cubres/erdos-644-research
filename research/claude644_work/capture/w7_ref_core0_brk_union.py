"""Referee w7 core#0 BREAK-IT: the significance claim 'Q only bites for N > 4 - tau* (~3.25k)'.
Explicit k-uniform quadruples satisfying the Lemma-Q hypotheses with union exactly 5k-3t+3 (< 4k-t when 2t>k+3),
for all 4<=k<=60 and (k+2)/2 <= t <= k (t-1 >= 0, 2t-k-2 >= 0).  Pure set arithmetic (exact)."""
import itertools
MATCH=[((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2))]
def build(k,t):
    # pair cells: (0,1):a (2,3):b  [mu5];  (0,2):c (1,3):d [mu6];  (0,3):e (1,2):f [mu7]
    S5=t-1; S67=2*t-k-2
    a=S5//2; b=S5-a
    c=S67//2; d=0; e=S67-c; f=0
    cells={(0,1):a,(2,3):b,(0,2):c,(1,3):d,(0,3):e,(1,2):f}
    nxt=[0]; G=[set() for _ in range(4)]
    def new():
        nxt[0]+=1; return nxt[0]
    for (i,j),m in cells.items():
        for _ in range(m):
            v=new(); G[i].add(v); G[j].add(v)
    for i in range(4):
        if len(G[i])>k: return None
        while len(G[i])<k: G[i].add(new())
    return G
worst=None; cnt=0
for k in range(4,61):
    for t in range(1,k+1):
        if 2*t-k-2<0: continue
        G=build(k,t)
        assert G is not None,(k,t)
        I=[len((G[a]&G[b])|(G[c]&G[d])) for (a,b),(c,d) in MATCH]
        assert all(len(g)==k for g in G)
        assert I[0]<=t-1 and I[1]<=t-1 and I[2]<=t-1 and I[1]+I[2]<=2*t-k-2
        U=len(set().union(*G)); assert U==5*k-3*t+3,(k,t,U)
        cnt+=1
        if U<=4*k-t:
            if worst is None or (U-(4*k-t))<worst[0]: worst=(U-(4*k-t),k,t,U,4*k-t)
print('checked',cnt,'(k,t) pairs; all hypotheses hold with union 5k-3t+3')
print('most negative union-(4k-t):',worst)
for k,t in [(8,6),(40,30),(60,45)]:
    G=build(k,t); print(f'k={k} t={t}: union={len(set().union(*G))}, 4k-t={4*k-t}, I sizes',[len((G[a]&G[b])|(G[c]&G[d])) for (a,b),(c,d) in MATCH])
# non-uniform: small edge repeated
for k,t in [(40,30)]:
    g=set(range(t-1-k//2)) if t-1-k//2>0 else {0}
    G=[g]*4; I=[len(g)]*3
    print(f'non-uniform repeat example k={k},t={t}: |G|={len(g)}, union={len(g)}, hyp:',I[0]<=t-1 and 2*len(g)<=2*t-k-2)
