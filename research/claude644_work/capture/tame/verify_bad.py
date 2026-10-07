import itertools
from tc_lib import *
def realize(n, cells, y, c, a, k):
    """build explicit vertices and 7 edges from ILP solution; brute-force verify."""
    p=len(n); verts=[]  # (part, cell)
    for i in range(p):
        for j,cnt in enumerate(y[i]): verts += [(i,cells[j])]*cnt
    N=len(verts); edges=[]
    for l in range(7):
        win=[x for x in range(N) if verts[x][1]>>l&1]
        # choose k-subset of window with right parity: brute force over part counts
        found=None
        for E in itertools.combinations(win,k):
            s=[0]*len(a)
            for x in E:
                for b in range(len(a)): s[b]^=c[verts[x][0]][b]
            if tuple(s)==tuple(a): found=E; break
        assert found is not None, l
        edges.append(set(found))
    # verify no 2-transversal
    for x in range(N):
        for z in range(x,N):
            if all((x in E) or (z in E) for E in edges): return False, (x,z)
    return True, edges
k=8; n=[8,7]; c=[(1,),(0,)]; a=(1,)
r=is72_code(n,c,a,k); print(r[0], r[1][:2])
ok,edges=realize(n, r[1][1], r[1][2], c, a, k)
print("bad tuple verified:",ok)
for E in edges: print(sorted(E), "P-count", sum(1 for x in E if x<8))
