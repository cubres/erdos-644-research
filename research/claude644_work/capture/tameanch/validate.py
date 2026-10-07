# Validation of janson3 against notes_randomside [c10]: 1-part H_rho, static Fano typed Janson.
# fj_coarse: n=2.0 -> tau_FJ = .484 (x = 1.516, c = psi(x) = 0.972): maxmin exponent should be ~0 there,
# positive for smaller c (larger tau), negative for larger c.
import numpy as np, sys
sys.path.insert(0, '.')
from janson3 import fano_static
def psi(x): return x*np.log(x) - (x-1)*np.log(x-1)
n = 2.0
for tau in [0.40, 0.484, 0.55, 0.75]:
    x = n - tau; c = psi(x)
    cfg = fano_static({0: n}, {l: {0: 1.0} for l in range(7)})
    b = cfg.solve(c, tries=4)
    print(f'n={n} tau={tau} x={x:.3f} c={c:.4f}: maxmin = {b[0]:+.4f}  worst J={cfg.worstJ(b[1], c)}', flush=True)
