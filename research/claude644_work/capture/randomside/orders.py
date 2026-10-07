# orbit representatives of line orders under the Fano automorphism group
import itertools
from seqgame import LINES
pts=range(7)
auts=[]
for perm in itertools.permutations(pts):
    img=[frozenset(perm[p] for p in l) for l in LINES]
    if all(i in LINES for i in img):
        auts.append(tuple(LINES.index(i) for i in img))
assert len(auts)==168
seen=set(); reps=[]
for o in itertools.permutations(range(7)):
    if o in seen: continue
    reps.append(o)
    for a in auts: seen.add(tuple(a[l] for l in o))
print(len(reps))
import pickle; pickle.dump(reps,open('order_reps.pkl','wb'))
