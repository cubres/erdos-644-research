from lib2 import *
PREF0 = [19,20,1,2,3,4,5,6,9,10,21,22,41,42]
PREF0 += [k for k in range(1,43) if k not in PREF0]
def facets(k):
    out=[]
    for u,v in FUNCS[k-1]:
        out.append(([1,0,-u,-v],0))
        out.append(([0,1,u,v],-(u+v)))
    return out
def ev(c,z): return sum(F(a)*b for a,b in zip(c[0],z))+F(c[1])
def show(cons, path=(), depth=0, PREF=PREF0, out=None):
    V = vertices(cons,4); ind='  '*depth
    if not V: print(ind,'EMPTY'); return 0
    for k in PREF:
        if all(feasible(k-1,*v) for v in V):
            print(ind,'LEAF',k,'verts',[tuple(str(c) for c in v) for v in V]); return 1
    used={b for b,_ in path}; cand=[k for k in PREF if k not in used]
    best=max(cand,key=lambda k: sum(feasible(k-1,*v) for v in V))
    fc=facets(best); n=0
    print(ind,'split by template',best,[(str(u),str(v)) for u,v in FUNCS[best-1]], 'nverts',len(V))
    for j,f in enumerate(fc):
        if all(ev(f,v)>=0 for v in V): continue
        print(ind,' facet',j,'violated piece:')
        neg=([-a for a in f[0]],-f[1])
        n+=show(cons+[neg]+[fc[i] for i in range(j)], tuple(path)+((best,j),), depth+2, PREF)
    return n
