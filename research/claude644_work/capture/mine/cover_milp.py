import pickle, itertools, time, sys, numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix
chosen, edges = pickle.load(open(sys.argv[1],'rb')); n = int(sys.argv[2]); tl = float(sys.argv[3])
pairs = list(itertools.combinations(range(n), 2)); m = len(edges)
A = lil_matrix((len(pairs), m))
for j, e in enumerate(edges):
    es = set(e)
    for i, (x, y) in enumerate(pairs):
        if x not in es and y not in es: A[i, j] = 1
t0 = time.time()
res = milp(c=np.ones(m), constraints=LinearConstraint(A.tocsr(), lb=np.ones(len(pairs)), ub=np.inf),
           integrality=np.ones(m), bounds=Bounds(0, 1), options={'time_limit': tl, 'disp': False})
print("status", res.status, res.message, "time %.1f" % (time.time()-t0))
if res.x is not None:
    sel = [edges[j] for j in range(m) if res.x[j] > 0.5]
    print("cover size", len(sel), "(<=7 means NOT (7,2))")
    if len(sel) <= 7: print("bad tuple:", sel)
print("dual bound", getattr(res, 'mip_dual_bound', None))
