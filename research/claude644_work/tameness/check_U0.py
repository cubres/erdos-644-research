# exact check of Lemma U0 instance: Fano complements, every ordered pair (i,j)
import sys, itertools
sys.path.insert(0,'/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture')
import lib72 as L
lines=[(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
full=(1<<7)-1
B=[full & ~sum(1<<x for x in l) for l in lines]
assert not L.is_72(B,7)
ok=0
for i in range(7):
  for j in range(7):
    if i==j: continue
    H=[(b ^ (1<<i) ^ (1<<j)) if (b>>i&1 and not b>>j&1) else b for b in B]
    assert L.tau(H,7)<=2 and L.is_72(H,7)
    sh=[(e ^ (1<<i) ^ (1<<j)) if (e>>j&1 and not e>>i&1) else e for e in H]
    U=sorted(set(H)|set(sh)); S=sorted(set(H)|set((e ^ (1<<i) ^ (1<<j)) if ((e>>i&1)!=(e>>j&1)) else e for e in H))
    assert not L.is_72(U,7) and not L.is_72(S,7)
    ok+=1
print("Lemma U0 instance verified for",ok,"ordered pairs")
# Zykov clone (j := copy of i): delete edges with j not i, add sigma-images of edges with i not j.
okz=0
for i in range(7):
  for j in range(7):
    if i==j: continue
    H=[(b ^ (1<<i) ^ (1<<j)) if (b>>j&1 and not b>>i&1) else b for b in B]   # move j-only members to i
    assert L.tau(H,7)<=2 and L.is_72(H,7)
    Z=[e for e in H if not (e>>j&1 and not e>>i&1)]
    Z+= [e ^ (1<<i) ^ (1<<j) for e in H if (e>>i&1 and not e>>j&1)]
    Z=sorted(set(Z))
    assert all(b in Z for b in B) and not L.is_72(Z,7)
    okz+=1
print("Zykov clone: pull-back instance verified for",okz,"ordered pairs")
