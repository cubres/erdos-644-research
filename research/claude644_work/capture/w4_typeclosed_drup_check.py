"""Independent DRUP (RUP-only DRAT) proof checker, standard library only.
Every added lemma must follow by unit propagation from the current clause database (formula +
earlier lemmas, minus deleted clauses; deleting only weakens so honouring deletions is sound).
The proof must contain the empty clause.  Watched-literal propagation.
usage: python3 w4_typeclosed_drup_check.py formula.cnf proof.drat
"""
import sys, time

def parse_cnf(path):
    clauses = []; cur = []
    with open(path) as f:
        for line in f:
            if not line.strip() or line[0] in 'cp': continue
            for v in map(int, line.split()):
                if v == 0: clauses.append(cur); cur = []
                else: cur.append(v)
    return clauses

class Checker:
    def __init__(self, nvars):
        self.val = {}            # var -> bool (permanent + temporary)
        self.watches = {}        # literal -> list of clause ids watching it
        self.clauses = {}        # id -> list of literals (first two are watched)
        self.next_id = 0
        self.index = {}          # frozenset -> list of ids (for deletions)
        self.perm_trail = []
        self.conflict_at_top = False

    def value(self, lit):
        v = self.val.get(abs(lit))
        if v is None: return None
        return v if lit > 0 else (not v)

    def propagate(self, trail, start):
        """unit propagation from trail[start:]; returns True on conflict. Appends to trail."""
        i = start
        while i < len(trail):
            lit = trail[i]; i += 1
            false_lit = -lit
            wl = self.watches.get(false_lit)
            if not wl: continue
            j = 0
            while j < len(wl):
                cid = wl[j]
                c = self.clauses.get(cid)
                if c is None:
                    wl[j] = wl[-1]; wl.pop(); continue
                if c[0] == false_lit: c[0], c[1] = c[1], c[0]
                if self.value(c[0]) is True: j += 1; continue
                found = False
                for k in range(2, len(c)):
                    if self.value(c[k]) is not False:
                        c[1], c[k] = c[k], c[1]
                        self.watches.setdefault(c[1], []).append(cid)
                        wl[j] = wl[-1]; wl.pop(); found = True; break
                if found: continue
                v0 = self.value(c[0])
                if v0 is False: return True
                if v0 is None:
                    self.val[abs(c[0])] = c[0] > 0; trail.append(c[0])
                j += 1
        return False

    def add(self, lits):
        lits = list(dict.fromkeys(lits))
        cid = self.next_id; self.next_id += 1
        self.index.setdefault(frozenset(lits), []).append(cid)
        if len(lits) == 0:
            self.conflict_at_top = True; return
        # order: non-false literals first
        lits.sort(key=lambda l: 0 if self.value(l) is not False else 1)
        self.clauses[cid] = lits
        if len(lits) == 1:
            v = self.value(lits[0])
            if v is False: self.conflict_at_top = True
            elif v is None:
                self.val[abs(lits[0])] = lits[0] > 0; start = len(self.perm_trail)
                self.perm_trail.append(lits[0])
                if self.propagate(self.perm_trail, start): self.conflict_at_top = True
            self.watches.setdefault(lits[0], []).append(cid)
            return
        self.watches.setdefault(lits[0], []).append(cid)
        self.watches.setdefault(lits[1], []).append(cid)
        v0, v1 = self.value(lits[0]), self.value(lits[1])
        if v0 is False:
            self.conflict_at_top = True
        elif v1 is False and v0 is None:
            self.val[abs(lits[0])] = lits[0] > 0; start = len(self.perm_trail)
            self.perm_trail.append(lits[0])
            if self.propagate(self.perm_trail, start): self.conflict_at_top = True

    def delete(self, lits):
        key = frozenset(dict.fromkeys(lits))
        ids = self.index.get(key)
        if not ids: return
        cid = ids.pop()
        c = self.clauses.get(cid)
        # do not delete reason-carrying unit clauses at top level (keeps permanent trail sound)
        if c is not None and len(c) == 1: ids.append(cid); return
        self.clauses.pop(cid, None)

    def rup(self, lits):
        if self.conflict_at_top: return True
        trail = []
        for l in lits:
            v = self.value(l)
            if v is True:
                for t in trail: del self.val[abs(t)]
                return True
            if v is None:
                self.val[abs(l)] = (l < 0); trail.append(-l)
        confl = self.propagate(trail, 0)
        for t in trail: self.val.pop(abs(t), None)
        return confl

def main(cnf, proof):
    t0 = time.time()
    clauses = parse_cnf(cnf)
    ch = Checker(0)
    for c in clauses: ch.add(c)
    n_add = 0; empty = False
    with open(proof) as f:
        for line in f:
            tok = line.split()
            if not tok: continue
            if tok[0] == 'd':
                ch.delete([int(v) for v in tok[1:-1]]); continue
            lits = [int(v) for v in tok[:-1]]
            assert tok[-1] == '0'
            if not ch.rup(lits):
                print('FAIL: lemma not RUP:', lits[:20]); return False
            n_add += 1
            if not lits: empty = True; break
            ch.add(lits)
            if n_add % 20000 == 0: print('checked', n_add, round(time.time()-t0, 1), 's', flush=True)
    if not empty and ch.conflict_at_top:
        empty = True
    print('PASS' if empty else 'FAIL: no empty clause', 'lemmas', n_add, 'sec', round(time.time()-t0, 1))
    return empty

if __name__ == '__main__':
    ok = main(sys.argv[1], sys.argv[2])
    sys.exit(0 if ok else 1)
