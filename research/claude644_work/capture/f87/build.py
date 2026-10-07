"""Explicit 8-uniform family on 15 points found by the type-closed CEGAR (cegar_found_k8_t7_1_1_6_7.json).
Vertices: 0=a, 1=b, 2..7 = C (6), 8..14 = D (7).  Edge E (|E|=8) iff profile (|E&{a}|,|E&{b}|,|E&C|,|E&D|) in T."""
import itertools, json
T=[tuple(t) for t in json.load(open('/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/tame/cegar_found_k8_t7_1_1_6_7.json'))['T']]
A=[0];B=[1];C=list(range(2,8));D=list(range(8,15));V=list(range(15))
def prof(E): return (len(set(E)&set(A)),len(set(E)&set(B)),len(set(E)&set(C)),len(set(E)&set(D)))
EDGES=[frozenset(E) for E in itertools.combinations(V,8) if prof(E) in T]
if __name__=='__main__':
    print(len(EDGES),'edges; types',T)
    # tau: smallest transversal, brute force
    for s in range(1,9):
        hit=None
        for S in itertools.combinations(V,s):
            S=set(S)
            if all(E&S for E in EDGES): hit=S; break
        if hit is not None: print('tau =',s,'transversal',sorted(hit)); break
        else: print('no transversal of size',s)
