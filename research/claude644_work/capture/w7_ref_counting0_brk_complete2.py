#!/usr/bin/env python3
"""w7_ref_counting0_brk_complete2.py -- as w7_ref_counting0_brk_complete.py but branch-and-bound:
the partial key (|P|,|Pi|) over already-placed vertices is monotone, so prune when it exceeds the incumbent.
Exact (keeps ALL minimisers).  Usage: n k"""
import sys
from collections import Counter
FULL = 127
def main():
    n, k = int(sys.argv[1]), int(sys.argv[2])
    best = [None]; mins = []; sig = []; nodes = [0]
    def dfs(start, rows, left, Pset, npairs):
        nodes[0] += 1
        key = (len(Pset), npairs)
        if best[0] is not None and key > best[0]: return
        if left == 0:
            if npairs == 0: return      # no pair (only possible if not (7,2)); reported separately
            if best[0] is None or key < best[0]: best[0] = key; mins.clear()
            mins.append(tuple(sig)); return
        for s in range(start, 128):
            nr = [rows[i] + ((s >> i) & 1) for i in range(7)]
            if any(nr[i] > k or k - nr[i] > left - 1 for i in range(7)): continue
            idx = len(sig)
            newP = set(); add = 0
            for j, tt in enumerate(sig):
                if tt | s == FULL: add += 1; newP.add(j); newP.add(idx)
            sig.append(s); dfs(s, nr, left - 1, Pset | newP, npairs + add); sig.pop()
    dfs(0, [0] * 7, n, frozenset(), 0)
    t = n - k + 1
    print(f'K_{n}^{k}: nodes={nodes[0]} tau={t} lexmin={best[0]} #minimisers={len(mins)}', flush=True)
    summ = Counter(); ex = {}
    for sg in mins:
        pairs = [(x, y) for x in range(n) for y in range(x + 1, n) if sg[x] | sg[y] == FULL]; Ps = set(pairs)
        W = []
        for i in range(7):
            m = FULL & ~(1 << i)
            Ai = [(x, y) for x in range(n) for y in range(x + 1, n) if (sg[x] | sg[y]) & m == m and (x, y) not in Ps]
            W.append(set(z for pr in Ai for z in pr))
        for i in range(7):
            for (u, v) in pairs: assert len(W[i] | {u, v}) >= t, ('(a) FAIL', sg)
        delta = [min(len({u, v} - W[i]) for (u, v) in pairs) for i in range(7)]
        S = sum(len(W[i]) + delta[i] for i in range(7)); assert 7 * t <= S
        d = [bin(s).count('1') for s in sg]
        q = [sum(1 for i in range(7) if v in W[i]) for v in range(n)]
        hyp = all(d[v] >= 4 for v in range(n) if q[v] > 0)
        D7 = sum(4 * q[v] - 3 * d[v] for v in range(n))
        summ[('hyp', hyp)] += 1; summ[('slack', S - 7 * t)] += 1; summ[('D7', D7)] += 1
        key = ('hyp', hyp)
        if key not in ex: ex[key] = (sg, d, q, [len(w) for w in W], delta, S - 7 * t, D7)
    print('  summary:', dict(summ))
    for key, (sg, d, q, Ws, delta, sl, D7) in ex.items():
        print(f'  example {key}: sig={[format(s,"07b") for s in sg]} d={d} q={q} |W|={Ws} delta={delta} slack={sl} D7={D7}')
    print('  ALL (a),(b) checks pass on every minimiser')
main()
