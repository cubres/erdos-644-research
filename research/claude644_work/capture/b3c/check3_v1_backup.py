#!/usr/bin/env python3
"""STANDARD-LIBRARY checker for balanced-regime certificates (Erdos 644, Th(3)).  Imports only b3core (stdlib).
Verifies, exactly: region construction, support badness, exact support vertices (template inequalities),
every LP-duality certificate, the covering structure of every node (MIN: all class patterns with in_i=1;
REQ: all 7 patterns + validity cost<=tau, 0<=w<=x; FACET: every inequality certified or has a kid with the
reversed inequality; SPLIT: both halves).  Usage: check3.py certfile.json [more ...]"""
import sys, json
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from fractions import Fraction as F
import b3core as bc
from b3core import X, G, T, TAU, PATS, neg
PAIRDATA = json.load(open(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '..', 'heavy', 'astra_support_capacity_minimal.json')))
def dec_d(d): return {int(k): F(v) for k, v in d.items()}
def dec_c(c): return c[0], {int(k): F(v) for k, v in c[1].items()}, {int(k): F(v) for k, v in c[2].items()}
N = {'leaf': 0, 'ineq': 0}
def fail(msg): raise SystemExit('CHECK FAILED: ' + msg)
def chk(node, ineqs, eqs, nt):
    n = 7 + 3*nt; k = node['k']
    if k == 'EMPTY':
        kind, y, ye = dec_c(node['cert'])
        if kind not in ('farkas', 'tau') or not bc.check_empty([kind, y, ye], ineqs, eqs, n): fail('EMPTY cert')
        N['leaf'] += 1; return
    if k in ('TMPL', 'FACET'):
        cells, asg = bc.template_support(node['t'], PAIRDATA)
        if not bc.is_bad_support(cells): fail('support not bad')
        if len(asg) != 7 or any(not (0 <= a < nt) for a in asg): fail('bad assignment')
        L = bc.support_ineqs(cells, asg)
        kidm = {int(m): kid for m, kid in node.get('kids', [])}
        if k == 'TMPL' and kidm: fail('TMPL with kids')
        for m, (d, h) in enumerate(L):
            if m in kidm:
                chk(kidm[m], ineqs + [(neg(d), -h)], eqs, nt)
            else:
                c = node['certs'].get(str(m))
                if c is None: fail('missing inequality certificate')
                kind, y, ye = dec_c(c)
                if kind not in ('plain', 'strict') or not bc.check_ineq([kind, y, ye], ineqs, eqs, d, h, n): fail('ineq cert')
                N['ineq'] += 1
        if k == 'TMPL': N['leaf'] += 1
        return
    if k == 'MIN':
        i = node['i']
        if not (0 <= i < 3): fail('MIN index')
        pats = [tuple(p) for p, _ in node['kids']]
        if sorted(pats) != sorted(p for p in PATS if p[i]): fail('MIN patterns')
        kk = nt; tc, te = bc.type_region(kk)
        for pat, kid in node['kids']:
            chk(kid, ineqs + tc + bc.pattern_region(kk, pat), eqs + te + [({T(kk, i): F(1), G(i): F(-1)}, F(0))], nt+1)
        return
    if k == 'REQ':
        w = [dec_d(wl) for wl in node['w']]
        if any(a >= n for wl in w for a in wl): fail('request refers to unknown variable')
        sw = {}
        for l in range(3):
            for a, b in w[l].items(): sw[a] = sw.get(a, 0) + b
        sw[TAU] = sw.get(TAU, 0) - 1; sw = {a: b for a, b in sw.items() if b != 0}
        vc = node['vcert']
        need = [('cost', sw)]
        for l in range(3):
            need.append(('nonneg%d' % l, neg(w[l])))
            d = dict(w[l]); d[X(l)] = d.get(X(l), 0) - 1; need.append(('lex%d' % l, {a: b for a, b in d.items() if b != 0}))
        for name, d in need:
            if not d: continue
            kind, y, ye = dec_c(vc[name])
            if kind != 'plain' or not bc.check_max((y, ye), ineqs, eqs, d, F(0)): fail('request validity ' + name)
        pats = [tuple(p) for p, _ in node['kids']]
        if sorted(pats) != sorted(PATS): fail('REQ patterns')
        kk = nt; tc, te = bc.type_region(kk); rc = bc.request_region(kk, w)
        for pat, kid in node['kids']:
            chk(kid, ineqs + tc + rc + bc.pattern_region(kk, pat), eqs + te, nt+1)
        return
    if k == 'SPLIT':
        h = dec_d(node['h'])
        if len(node['kids']) != 2: fail('SPLIT')
        chk(node['kids'][0], ineqs + [(h, F(0))], eqs, nt)
        chk(node['kids'][1], ineqs + [(neg(h), F(0))], eqs, nt)
        return
    fail('unknown node kind ' + str(k))
if __name__ == '__main__':
    for f in sys.argv[1:]:
        D = json.load(open(f))
        if D.get('balanced') is not True: fail('only the balanced regime is certified by this checker')
        lo = [F(v) for v in D['box'][0]]; hi = [F(v) for v in D['box'][1]]
        C, E = bc.base_region(True, D['sorted'], (lo, hi))
        N['leaf'] = 0; N['ineq'] = 0
        chk(D['tree'], C, E, 0)
        print('PASS', f, 'box', D['box'], 'sorted', D['sorted'], 'leaves', N['leaf'], 'inequality certificates', N['ineq'])
