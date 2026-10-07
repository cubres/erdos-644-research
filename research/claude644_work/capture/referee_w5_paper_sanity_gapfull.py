# Referee (w5, sanity supplement): FULL integer enumeration (no worst-case reductions) of every numerical
# inequality in Lemma 5.1 (gap extension) and Lemma 5.3 (finish, beta'=173/200) of paper_0865.tex,
# written from the paper text, independent of w5_paper_constants.py.  numpy int64 (exact integers).
import sys, numpy as np
def cdiv(a, b): return -((-a) // b)
def check_r(r):
    fails = []
    cb = cdiv(173*r, 200); K = cb + 10; T = cb + 4; h0 = (23*r)//50
    if not (T <= r and K <= r): fails.append('T<=r')
    # ---- Lemma 5.1: all x in [hr, r/2] (x integer, 50x >= 23r), balanced G: y,z <= r - floor((cb+x)/2)
    for x in range(cdiv(23*r, 50), r//2 + 1):
        bnd = r - (cb + x)//2
        if not (50*bnd < 23*r): fails.append(('51 trace<hr', x)); continue
        # gap => y,z < l r  i.e. 200y < 43r ; all such y,z
        ys = np.arange(0, bnd+1); ys = ys[200*ys < 43*r]
        Y, Z = np.meshgrid(ys, ys, indexing='ij'); Y = Y.ravel(); Z = Z.ravel()
        S = x + Y + Z
        c1 = S <= T
        # Case S <= T
        p = np.maximum(0, r-x-Y-h0); t = np.maximum(0, r-x-Z-h0)
        C = x + Y + Z + p + t
        ok = (C <= T) & (T - C <= r - Y - Z)                      # W fits
        EH = np.minimum(r-x-Y, h0); FH = np.minimum(r-x-Z, h0)
        ok &= (50*EH <= 23*r) & (50*FH <= 23*r)                    # traces <= hr, so gap applies
        lmax = cdiv(43*r, 200) - 1                                 # traces then < l r
        b = r - T + x + p + t                                      # |G cap H| bound
        ok &= (x + (b+1)//2 <= T)                                  # X u B_i
        ok &= (Y + Z + 2*lmax <= T)                                # Y u Z u (E cap H) u (F cap H)
        bad1 = c1 & ~ok
        # Case S > T
        c2 = ~c1
        ok2 = (x + Y <= T) & (T - x - Y <= Z)                      # Z0 exists
        cmax = r - x - Y; qa = r - (T - Y)
        ok2 &= (50*cmax <= 23*r) & (50*qa <= 23*r)                 # traces <= hr -> < l r by gap
        q = S - T; bb = r - Y - Z
        ok2 &= (x + q + (bb+1)//2 <= T)                            # R_1,R_2
        ok2 &= (Y + Z + lmax + lmax <= T)                          # R_3 : y+z+a+c, a+c<= (q+a)+c < 2 l r
        # total = r+x+z+2q+a+b with a <= lmax - q (q+a<=lmax), b<=bb
        tot = r + x + Z + 2*q + np.maximum(0, lmax - q) + bb
        ok2 &= (tot <= 3*T)
        bad2 = c2 & ~ok2
        if bad1.any() or bad2.any(): fails.append(('51', x, int(bad1.sum()), int(bad2.sum())))
    # ---- Lemma 5.3 (beta' = beta): m <= floor(119r/400) (hypothesis), full enumeration of m and x
    Tf = T
    for m in range(0, (119*r)//400 + 1):
        B18 = max(cdiv(3*r+m, 4), cdiv(2*r+2*m, 3))
        if B18 > cb: fails.append(('53 L18', m))
        xmax = r - (Tf + m)//2
        if xmax <= r//2 + (r % 2 == 0 and 0):   # no x > r/2 possible -> branch vacuous
            pass
        for x in range(r//2 + 1, xmax + 1):   # x > r/2
            if not (m <= r - Tf): fails.append(('53 m<=r-T', m, x)); break
            z = r - x  # worst (largest) z; z <= m required
            if x + 2*m >= Tf: fails.append(('53 pad>0', m, x))
            b = r - (Tf - x)
            if b > r//2:
                if not (cdiv(r,2) + 2*m <= Tf and x + m <= Tf and 3*Tf >= 2*x + b + cdiv(r,2) + 2*m and 4*m <= r):
                    fails.append(('53 L41', m, x))
    return fails
R = [int(a) for a in sys.argv[1:]] or list(range(1000, 1041))
allf = []
for r in R:
    f = check_r(r); allf += [(r, f)] if f else []
print('checked', len(R), 'values of r from', min(R), 'to', max(R), '; failing r:', len(allf), allf[:5])
