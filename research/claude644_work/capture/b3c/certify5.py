"""Attach exact rational certificates to a search3 tree (uses scipy only to find LP supports)."""
import sys, json, time
sys.path.insert(0,'/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/b3c')
from fractions import Fraction as F
import b4core as bc
from b4core import X, G, T, TAU, PATS, neg, H, TOFF
from exactcert import prove_max, prove_empty
PAIRDATA = json.load(open('/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/heavy/astra_support_capacity_minimal.json'))
def dec_d(d): return {int(k): F(v) for k, v in d.items()}
def enc_c(c): return [{str(k): str(v) for k, v in c[0].items()}, {str(k): str(v) for k, v in c[1].items()}]
STATS = {}
def cnt(k): STATS[k] = STATS.get(k, 0) + 1
def cert_ineq(ineqs, eqs, d, h, n):
    c = prove_max(ineqs, eqs, d, h, n)
    if c is not None: return ['plain'] + enc_c(c)
    A, E, dd, hh = bc.strict_system(ineqs, eqs, d, h, n)
    c = prove_max(A, E, dd, hh, n+1)
    if c is not None: cnt('strict'); return ['strict'] + enc_c(c)
    raise ValueError('no certificate')
def walk(node, ineqs, eqs, nt):
    n = TOFF + 3*nt; k = node['k']
    if k == 'EMPTY':
        c = prove_empty(ineqs, eqs, n)
        if c is not None: node['cert'] = ['farkas'] + enc_c(c); cnt('farkas'); return
        c = prove_max(ineqs, eqs, {TAU: F(1)}, F(3, 4), n)
        if c is None: raise ValueError('EMPTY without certificate')
        node['cert'] = ['tau'] + enc_c(c); cnt('taucut'); return
    if k == 'FAIL': raise ValueError('FAIL leaf')
    if k in ('TMPL', 'FACET'):
        cells, asg = bc.template_support(node['t'], PAIRDATA)
        L = bc.support_ineqs(cells, asg)
        kidm = {int(m): kid for m, kid in node.get('kids', [])}
        certs = {}
        for m, (d, h) in enumerate(L):
            if m in kidm:
                walk(kidm[m], ineqs + [(neg(d), -h)], eqs, nt)
            else:
                certs[str(m)] = cert_ineq(ineqs, eqs, d, h, n)
        node['certs'] = certs; cnt(k); return
    if k == 'MIN':
        i = node['i']; kk = nt
        tc, te = bc.type_region(kk)
        for pat, kid in node['kids']:
            walk(kid, ineqs + tc + bc.pattern_region(kk, pat), eqs + te + [({T(kk, i): F(1), G(i): F(-1)}, F(0))], nt+1)
        cnt('MIN'); return
    if k == 'RMIN':
        i, j = node['i'], node['j']; kk = nt
        tc, te = bc.type_region(kk)
        for pat, kid in node['kids']:
            walk(kid, ineqs + tc + bc.pattern_region(kk, pat), eqs + te + [({T(kk, i): F(1), H(i, j): F(-1)}, F(0))], nt+1)
        cnt('RMIN'); return
    if k == 'REQ':
        w = [dec_d(wl) for wl in node['w']]
        sw = {}
        for l in range(3):
            for a, b in w[l].items(): sw[a] = sw.get(a, 0) + b
        sw[TAU] = sw.get(TAU, 0) - 1; sw = {a: b for a, b in sw.items() if b != 0}
        vc = {'cost': cert_plain(ineqs, eqs, sw, n)}
        for l in range(3):
            if w[l]: vc['nonneg%d' % l] = cert_plain(ineqs, eqs, neg(w[l]), n)
            d = dict(w[l]); d[X(l)] = d.get(X(l), 0) - 1; d = {a: b for a, b in d.items() if b != 0}
            if d: vc['lex%d' % l] = cert_plain(ineqs, eqs, d, n)
        node['vcert'] = vc
        kk = nt; tc, te = bc.type_region(kk); rc = bc.request_region(kk, w)
        for pat, kid in node['kids']:
            walk(kid, ineqs + tc + rc + bc.pattern_region(kk, pat), eqs + te, nt+1)
        cnt('REQ'); return
    if k == 'SPLIT':
        h = dec_d(node['h'])
        walk(node['kids'][0], ineqs + [(h, F(0))], eqs, nt)
        walk(node['kids'][1], ineqs + [(neg(h), F(0))], eqs, nt)
        cnt('SPLIT'); return
    raise ValueError('unknown node ' + k)
def cert_plain(ineqs, eqs, d, n):
    c = prove_max(ineqs, eqs, d, F(0), n)
    if c is None: raise ValueError('request validity not certified')
    return ['plain'] + enc_c(c)
if __name__ == '__main__':
    src = sys.argv[1]; dst = sys.argv[2]
    D = json.load(open(src)); t0 = time.time()
    lo = [F(v) for v in D['box'][0]]; hi = [F(v) for v in D['box'][1]]
    C, E = bc.base_region(D['balanced'], D['sorted'], (lo, hi), D.get('excess', False))
    walk(D['tree'], C, E, 0)
    json.dump(D, open(dst, 'w'))
    print('CERTIFIED', src, STATS, round(time.time() - t0, 1))
