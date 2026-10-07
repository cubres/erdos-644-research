#!/usr/bin/env python3
"""w7_ref_counting0_brk_complete.py -- referee w7 BREAK-IT, claim counting#0, COMPLETE families K_n^(k).
Pure python, exact.  A 7-tuple of k-subsets of [n] is determined up to relabelling V by the multiset of
membership patterns sigma(v) in 2^[7] with every row size = k.  Exhaustive DFS over those multisets ->
exact lex (|P7|,|Pi7|) minimum; for EVERY minimiser: tau = n-k+1; (a) |W_i u {u,v}| >= tau (= transversal
of K_n^k); (b); the (d) hypothesis (q(v)>0 => d(v)>=4); slack of (b); D7.  Summary over all minimisers.
Usage: python3 w7_ref_counting0_brk_complete.py n k"""
import sys
from collections import Counter
FULL = 127
def main():
    n, k = int(sys.argv[1]), int(sys.argv[2])
    best = None; mins = []; cnt = 0; bad72 = 0; sig = []
    def dfs(start, rows, left):
        nonlocal best, mins, cnt, bad72
        if left == 0:
            if any(r != k for r in rows): return
            cnt += 1
            pairs = [(x, y) for x in range(n) for y in range(x + 1, n) if sig[x] | sig[y] == FULL]
            if not pairs: bad72 += 1; return
            key = (len(set(z for pr in pairs for z in pr)), len(pairs))
            if best is None or key < best: best = key; mins = [tuple(sig)]
            elif key == best: mins.append(tuple(sig))
            return
        for s in range(start, 128):
            nr = [rows[i] + ((s >> i) & 1) for i in range(7)]
            if any(nr[i] > k or k - nr[i] > left - 1 for i in range(7)): continue
            sig.append(s); dfs(s, nr, left - 1); sig.pop()
    dfs(0, [0] * 7, n)
    t = n - k + 1
    print(f'K_{n}^{k}: tuples(up to relabel)={cnt}, with no pair={bad72}, tau={t}, lexmin={best}, #minimisers={len(mins)}')
    if bad72: print('  NOT (7,2) -- stop'); return
    summ = Counter(); ex = {}
    for sg in mins:
        pairs = [(x, y) for x in range(n) for y in range(x + 1, n) if sg[x] | sg[y] == FULL]; Ps = set(pairs)
        W = []
        for i in range(7):
            m = FULL & ~(1 << i)
            Ai = [(x, y) for x in range(n) for y in range(x + 1, n) if (sg[x] | sg[y]) & m == m and (x, y) not in Ps]
            W.append(set(z for pr in Ai for z in pr))
            assert not any((sg[z] >> i) & 1 for z in W[i])
        for i in range(7):
            for (u, v) in pairs:
                assert len(W[i] | {u, v}) >= t, ('(a) FAIL', sg, i, (u, v))
        delta = [min(len({u, v} - W[i]) for (u, v) in pairs) for i in range(7)]
        S = sum(len(W[i]) + delta[i] for i in range(7)); assert 7 * t <= S
        d = [bin(s).count('1') for s in sg]
        q = [sum(1 for i in range(7) if v in W[i]) for v in range(n)]
        hyp = all(d[v] >= 4 for v in range(n) if q[v] > 0)
        D7 = sum(4 * q[v] - 3 * d[v] for v in range(n))
        assert 28 * t <= 3 * 7 * k + D7 + 4 * sum(delta)
        summ[('hyp', hyp)] += 1; summ[('slack', S - 7 * t)] += 1
        if hyp: assert 4 * t <= 3 * k + 8
        key = ('hyp', hyp)
        if key not in ex: ex[key] = (sg, d, q, [len(w) for w in W], delta, S - 7 * t, D7)
    print('  summary:', dict(summ))
    for key, (sg, d, q, Ws, delta, sl, D7) in ex.items():
        print(f'  example {key}: sig={[format(s,"07b") for s in sg]} d={d} q={q} |W|={Ws} delta={delta} slack={sl} D7={D7}')
    print('  ALL (a),(b),(c) checks pass on every minimiser')
main()
