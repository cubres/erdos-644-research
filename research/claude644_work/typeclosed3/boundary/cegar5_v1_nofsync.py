"""INCREMENTAL region CEGAR (exact engine gen_cert3, strong branching, streamed leaves).
One depth-first certification tree is grown for the whole run.  When a node is an adversary (no role disjunction
violated, no template succeeds), the escape-box request of its valid roles is ADDED to the strategy and the SAME node
is pushed back: every leaf certified so far stays valid (its Motzkin certificate only uses rows that are still
present), every internal node still branches on one disjunction with all its alternatives, so the final tree is a
certificate for the FINAL strategy.  Leaves go to certs/gcert5_<name>.body.gz; on completion the certificate
certs/gcert5_<name>.jsonl.gz = header (final strategy) + body.  Checkpoint (pickle of spec + stack) every 2000 nodes
-> resumable with resume=1.
usage: python3 cegar5.py <start.json> <name> [pi0=0] [menu=F,V,T3,R,W] [fk=7] [rk=4] [strong=4] [resume=0]
                        [maxroles=40]"""
import sys, json, time, os, gzip, pickle, shutil
from fractions import Fraction as F
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, HERE)
from gen_cert3 import Engine3, Strategy3
from cegar_exact import escape_request


def main():
    name = sys.argv[2]
    kw = dict(a.split('=') for a in sys.argv[3:])
    pi0 = F(kw.get('pi0', '0')); fk = int(kw.get('fk', 7)); rk = int(kw.get('rk', 4))
    strong = int(kw.get('strong', 4)); menu = tuple(kw.get('menu', 'F,V,T3,R,W').split(','))
    maxroles = int(kw.get('maxroles', 40))
    ck = os.path.join(HERE, 'certs', 'ck5_%s.pkl' % name)
    body = os.path.join(HERE, 'certs', 'gcert5_%s.body.gz' % name)
    log = open(os.path.join(HERE, 'cx5_%s.log' % name), 'a')

    def say(m):
        print(m, flush=True); log.write(time.strftime('%H:%M:%S ') + m + '\n'); log.flush()

    if kw.get('resume', '0') == '1':
        st = pickle.load(open(ck, 'rb')); spec = st['spec']; stack = st['stack']; nodes = st['nodes']; nleaves = st['nleaves']
        # the body may contain leaves written after the checkpoint: truncate to the checkpointed count
        tmp = body + '.tmp'
        with gzip.open(body, 'rt') as fi, gzip.open(tmp, 'wt') as fo:
            for k, line in enumerate(fi):
                if k >= nleaves: break
                fo.write(line)
        os.replace(tmp, body)
        out = gzip.open(body, 'at')
        say('RESUME nodes %d leaves %d stack %d roles %d' % (nodes, nleaves, len(stack), len(spec['roles'])))
    else:
        spec = json.load(open(sys.argv[1])); stack = [((), [])]; nodes = 0; nleaves = 0
        out = gzip.open(body, 'wt')
        say('START %s pi0 %s roles %s menu %s' % (sys.argv[1], pi0, [r['name'] for r in spec['roles']], menu))

    def build(spec):
        S = Strategy3(spec, pi0, fk=fk, menu=menu, lazy=True); E = Engine3(S); E.rk = rk; E.strong = strong
        return S, E

    S, E = build(spec)
    t0 = time.time(); nadv = 0; last_ck = nodes
    while stack:
        path, extra = stack.pop(); nodes += 1
        rows = S.BASE + extra
        beta, v = E.lp(rows)
        if beta is None:
            say('LPERROR at %s' % (path,)); return
        if beta <= 1e-9:
            c = E.cert(rows)
            if c is None:
                say('CERTFAIL at %s' % (path,)); return
            out.write(json.dumps((list(path), [[{k: str(x) for k, x in co}, str(rhs), st_, str(l)] for (co, rhs, st_), l in c])) + '\n')
            nleaves += 1
            continue
        d_ok, d_sc = E.disj_status(v)
        bad = np.nonzero(~d_ok)[0]
        pick = E.names[bad[0]] if len(bad) else None
        if pick is None:
            cands = E.top_templates(v, k=strong)
            best = None
            for nm in cands:
                feas = 0
                for alt in E.disj(nm):
                    b2, v2 = E.lp(rows + list(alt))
                    if b2 is not None and b2 > 1e-9: feas += 1
                    if best is not None and feas >= best[0]: break
                if best is None or feas < best[0]: best = (feas, nm)
                if best[0] == 0: break
            if best is not None: pick = best[1]
        if pick is None:
            # ADVERSARY: add the escape box and retry this node
            nadv += 1
            valid = [n for n in S.names if not E.is_void(n, v)]
            say('adversary #%d at depth %d (nodes %d leaves %d) beta %.5f x=%s tau=%.4f roles %s' % (
                nadv, len(path), nodes, nleaves, beta, [round(float(v[S.VI['x%d' % i]]), 4) for i in range(3)],
                v[S.VI['tau']], {n: [round(float(v[S.VI[S.c(n, j)]]), 4) for j in range(3)] for n in valid}))
            json.dump({'v': dict(zip(S.VARS, map(float, v))), 'beta': beta, 'valid': valid, 'path': list(path)},
                      open(os.path.join(HERE, 'certs', 'gadv5_%s_%d.json' % (name, nadv)), 'w'))
            role, cost = escape_request(S, v, valid, 'X%d' % (len(spec['roles'])))
            if cost >= v[S.VI['tau']] - 1e-12:
                say('NO escape box (tau*(roles) = %.4f >= tau): candidate genuine family -- STOP' % cost); out.close(); return
            if len(spec['roles']) >= maxroles:
                say('STOP: maxroles reached'); out.close(); return
            if kw.get('esc', 'margin') == 'margin' and role['strict']:
                # MARGIN escape: move every threshold t_j (j in J) down by (tau - cost)/(2|J|), cost = sum_J (x_j - t_j):
                # closed box of cost (tau + cost)/2 < tau (valid iff the strict escape is), excluding every type
                # within that margin of the thresholds -- no creeping; plus its lex answers (one per part of J).
                J = role['strict']; k = len(J)
                sh = {'tau': F(-1, 2 * k)}
                for j in J:
                    (owner_var, _), = role['u'][j][0].items()
                    sh[owner_var] = sh.get(owner_var, 0) - F(1, 2 * k)
                    sh['x%d' % j] = sh.get('x%d' % j, 0) + F(1, 2 * k)
                u = [[] for _ in range(3)]
                for j in J:
                    (owner_var, _), = role['u'][j][0].items()
                    e = dict(sh); e[owner_var] = e.get(owner_var, 0) + 1
                    u[j] = [{kk: str(vv) for kk, vv in e.items() if vv != 0}]
                base = {'name': role['name'] + 'm', 'kind': 'req', 'u': u}
                new = [base] + [{'name': role['name'] + 'm%d' % l, 'kind': 'req', 'u': u, 'lex': l} for l in J]
            elif kw.get('lex', '1') == '1' and role['strict']:
                # LEX escapes: the closed box, answer minimising c_l (one role per threshold part l).  The strict escape
                # box is avoided because the adversary answers it by creeping (a type just below the threshold);
                # a lex answer a has the free box {c_l < a_l} below it, so a_l <= threshold - (tau - cost): a jump.
                new = [role]          # keep the strict escape too (it excludes boundary/pure types exactly)
                for l in role['strict']:
                    r = {'name': role['name'] + 'l%d' % l, 'kind': 'req', 'u': role['u'], 'lex': l}
                    new.append(r)
            else:
                new = [role]
            say('  ADD escape %s cost %.4f u=%s strict=%s' % ([r['name'] for r in new], cost, role['u'], role['strict']))
            spec = dict(spec); spec['roles'] = spec['roles'] + new
            S, E = build(spec)
            stack.append((path, extra)); nodes -= 1
            continue
        for ai, alt in enumerate(E.disj(pick)):
            stack.append((path + ((pick, ai),), extra + list(alt)))
        if nodes - last_ck >= 5000:
            last_ck = nodes
            out.flush()
            pickle.dump({'spec': spec, 'stack': stack, 'nodes': nodes, 'nleaves': nleaves}, open(ck + '.tmp', 'wb'))
            os.replace(ck + '.tmp', ck)
            say('nodes %d leaves %d stack %d depth %d roles %d (%.0fs)' % (nodes, nleaves, len(stack), len(path), len(spec['roles']), time.time() - t0))
    out.close()
    fin = os.path.join(HERE, 'certs', 'gcert5_%s.jsonl.gz' % name)
    with gzip.open(fin, 'wt') as fo, gzip.open(body, 'rt') as fi:
        fo.write(json.dumps({'pi0': str(pi0), 'strategy': spec, 'fk': fk, 'rk': rk, 'menu': list(menu), 'format': 'jsonl-v1'}) + '\n')
        shutil.copyfileobj(fi, fo)
    say('CERTIFIED leaves %d nodes %d roles %d -> %s (%.0fs)' % (nleaves, nodes, len(spec['roles']), fin, time.time() - t0))


if __name__ == '__main__':
    main()
