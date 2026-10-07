"""
CERTIFICATE for the parity gadget behind the Triple Lemma.

Triple Lemma.  H has (7,2); E,F,G in H with E&F&G empty; N=|E u F u G|.
Then tau(H) <= floor(N/2)+1.

Proof gadget checked here, exhaustively over all Venn-cell size vectors
(a_E,a_F,a_G,a_EF,a_EG,a_FG) in {0..MAX}^6 (plus 0..2 extra outside points):
  parts  P1 = EF u E-only,  P2 = EG u G-only,  P3 = FG u F-only;
  split each part into halves (bit 0 = first ceil half, bit 1 = rest) in all
  admissible balanced ways (the script tries both orientations per part);
  Q_abc = P1^a u P2^b u P3^c for the four even-parity words abc.
We check:
  (i)  every 2-point set {x,y} (x=y allowed) meeting E,F,G lies inside some Q_j;
  (ii) the seven sets E,F,G, V\\Q_1,..,V\\Q_4 have NO transversal of size <= 2
       (V = union plus the extra outside points; complements are the largest
       sets avoiding the Q_j, so this covers every choice of avoiding edges);
  (iii) min over the tried orientations of max_j |Q_j|  <=  floor(N/2)+1.
All arithmetic is exact integer arithmetic.  Run: python3 verify_triple_gadget.py [MAX]
"""
import itertools, sys
MAX = int(sys.argv[1]) if len(sys.argv) > 1 else 4
EVEN = [(0,0,0), (0,1,1), (1,0,1), (1,1,0)]

def check(sizes, extra):
    names = ["E", "F", "G", "EF", "EG", "FG"]
    pts = []  # (type, index)
    for nm, s in zip(names, sizes):
        pts += [(nm, i) for i in range(s)]
    n0 = len(pts)
    pts += [("out", i) for i in range(extra)]
    idx = {p: i for i, p in enumerate(pts)}
    def members(letter):
        return {idx[p] for p in pts if p[0] != "out" and letter in p[0]}
    E, F, G = members("E"), members("F"), members("G")
    if not E or not F or not G: return None
    V = set(range(len(pts)))
    N = n0
    part = {}
    for p in pts:
        t = p[0]
        if t in ("EF", "E"): part[idx[p]] = 0
        elif t in ("EG", "G"): part[idx[p]] = 1
        elif t in ("FG", "F"): part[idx[p]] = 2
    parts = [[v for v in range(n0) if part[v] == j] for j in range(3)]
    best = None
    for orient in itertools.product([0, 1], repeat=3):
        bit = {}
        for j in range(3):
            L = parts[j]; h = (len(L) + 1) // 2
            for i, v in enumerate(L):
                b = 0 if i < h else 1
                bit[v] = b ^ orient[j]
        Q = []
        for w in EVEN:
            Q.append({v for v in range(n0) if bit[v] == w[part[v]]})
        # (i) every 2-transversal of E,F,G inside some Q
        for x in range(len(pts)):
            for y in range(x, len(pts)):
                pr = {x, y}
                if (pr & E) and (pr & F) and (pr & G):
                    if not any(pr <= q for q in Q):
                        return ("FAIL_i", sizes, extra, orient, x, y)
        # (ii) seven sets have no 2-transversal
        seven = [E, F, G] + [V - q for q in Q]
        for x in range(len(pts)):
            for y in range(x, len(pts)):
                pr = {x, y}
                if all(pr & S for S in seven):
                    return ("FAIL_ii", sizes, extra, orient, x, y)
        mx = max(len(q) for q in Q)
        best = mx if best is None else min(best, mx)
    if best > N // 2 + 1:
        return ("FAIL_iii", sizes, extra, best, N)
    return best - (N // 2 + 1)

count = 0; tightcnt = 0
for sizes in itertools.product(range(MAX + 1), repeat=6):
    for extra in range(3):
        r = check(sizes, extra)
        if r is None: continue
        if isinstance(r, tuple):
            print("FAILURE", r); raise SystemExit(1)
        count += 1
        if r == 0: tightcnt += 1
print("all checks passed on", count, "configurations; bound attained (max|Q|=floor(N/2)+1) in", tightcnt)
