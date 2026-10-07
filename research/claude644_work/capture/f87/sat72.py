"""Independent (7,2) check of the explicit family by SAT: is there a set of <= 7 edges with no transversal of size <= 2?
Equivalently every pair {u,v} (u<=v) is AVOIDED by some chosen edge.  UNSAT => (7,2)."""
import itertools, time, sys
from pysat.formula import CNF
from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical153
from build import EDGES, V
t0=time.time()
m=len(EDGES); var={i:i+1 for i in range(m)}
cnf=CNF()
for u,v in itertools.combinations_with_replacement(V,2):
    cl=[var[i] for i,E in enumerate(EDGES) if u not in E and v not in E]
    cnf.append(cl)
card=CardEnc.atmost(lits=list(range(1,m+1)),bound=7,top_id=m,encoding=EncType.seqcounter)
cnf.extend(card.clauses)
s=Cadical153(bootstrap_with=cnf.clauses)
r=s.solve()
print('SAT (bad 7-tuple exists)' if r else 'UNSAT: family is (7,2)', f'{time.time()-t0:.0f}s',flush=True)
if r:
    mod=set(x for x in s.get_model() if x>0); ch=[EDGES[i] for i in range(m) if i+1 in mod]
    for E in ch: print(sorted(E))
