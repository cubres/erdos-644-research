"""Deterministic, checkpointed discovery wrapper; original checker is unchanged.

Each complete subtree is persisted in SQLite. An interrupted traversal restarts
from its root and recovers completed siblings, using a state-specific RNG seed
so the choices along its unfinished branch remain reproducible. A timeout also
records the deepest outstanding polyhedron for mathematical diagnosis.
"""
import os
for v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ.setdefault(v, '1')
import sys, json, time, pickle, hashlib, sqlite3, argparse
from pathlib import Path
sys.path.insert(0, '/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/b3c')
import search6 as lib
from fast_reps import reparr as fast_reparr
# For up to nine types preserve the historical choice of representatives;
# larger menus use the efficient complete orbit enumeration.
_old_reparr = lib.reparr
lib.reparr = lambda m: _old_reparr(m) if m <= 9 else fast_reparr(m)

ap = argparse.ArgumentParser()
ap.add_argument('lo'); ap.add_argument('hi'); ap.add_argument('regime')
ap.add_argument('prefix'); ap.add_argument('--seconds', type=float, default=600)
ap.add_argument('--facet', type=int, default=5); ap.add_argument('--requests', type=int, default=2)
ap.add_argument('--support', action='store_true'); ap.add_argument('--seed', type=int, default=0)
ap.add_argument('--zero-pair', action='store_true')
ap.add_argument('--strict-types', action='store_true')
ap.add_argument('--strong-blocker', action='store_true')
ap.add_argument('--conditional-rmin', action='store_true')
ap.add_argument('--disjoint', action='store_true')
ap.add_argument('--max-types', type=int, default=11)
ap.add_argument('--optimal-blocker', action='store_true')
ap.add_argument('--anchor-pair', action='store_true')
ap.add_argument('--terminal-partner', action='store_true')
args = ap.parse_args()
if args.max_types>11:
    # Discovery menu of all Fano assignments using at most three distinct types.
    # Full higher-color orbit arrays would grow as m**7. Any chosen tuple still
    # goes through the original exact support checker.
    import itertools
    _sparse_cache={}
    def sparse_reparr(m):
        if m<=9:return _old_reparr(m)
        if m not in _sparse_cache:
            cols=lib.np.array(list(itertools.combinations(range(m),3)),dtype=int)
            reps=_old_reparr(3)
            arr=cols[:,reps].reshape(-1,7)
            _sparse_cache[m]=lib.np.unique(arr,axis=0)
        return _sparse_cache[m]
    lib.reparr=sparse_reparr
if args.disjoint:
    import search_disjoint as lib
prefix = Path(args.prefix); prefix.parent.mkdir(parents=True, exist_ok=True)
lo = [lib.F(v) for v in args.lo.split(',')]; hi = [lib.F(v) for v in args.hi.split(',')]
reg = True if args.regime == 'balanced' else args.regime
db = sqlite3.connect(str(prefix) + '.sqlite')
db.execute('PRAGMA journal_mode=WAL'); db.execute('PRAGMA synchronous=NORMAL')
db.execute('CREATE TABLE IF NOT EXISTS nodes (key TEXT PRIMARY KEY, value BLOB NOT NULL)')

class Resumable(lib.Search):
    def __init__(self):
        super().__init__(maxfacet=args.facet, maxreq=args.requests, tlimit=args.seconds,
                         usesupp=args.support, log=False, seed=args.seed)
        self.userm = reg is True; self.cache_hits = 0; self.saved = 0
        self.max_types=args.max_types;self.optimal_blocker=args.optimal_blocker;self.terminal_partner=args.terminal_partner
        self.deepest_saved = False; self.last_report = time.time()
    def solve(self, cons, eqs, nt, fdepth, nreq, path):
        payload = (cons, eqs, nt, fdepth, nreq, self.info,
                   args.facet, args.requests, args.support, args.seed)
        if args.zero_pair or args.strict_types or args.strong_blocker or args.conditional_rmin:
            payload += (('modes',args.zero_pair,args.strict_types,args.strong_blocker,args.conditional_rmin),)
        if args.disjoint:payload += (('disjoint',True),)
        if args.anchor_pair:payload += (('anchor-pair',True),)
        if args.terminal_partner:payload += (('terminal-partner',True),)
        if args.max_types!=11 or args.optimal_blocker:
            payload += (('depth-options',args.max_types,args.optimal_blocker),)
        raw = pickle.dumps(payload, protocol=4)
        key = hashlib.sha256(raw).hexdigest()
        cached = db.execute('SELECT value FROM nodes WHERE key=?', (key,)).fetchone()
        if cached:
            self.cache_hits += 1
            return pickle.loads(cached[0])
        previous_rng = self.rng
        previous_forms=getattr(self,'current_forms',[])
        if args.strict_types:
            from strict_types import strict_forms
            self.current_forms=strict_forms(cons,lib.nv(nt))
        self.rng = lib.np.random.default_rng(int(key[:16], 16))
        try:
            if args.conditional_rmin and nt>=3 and reg is not True:
                pats=[f[2] if f[0]=='M' else f[3] if f[0]=='H' else f[1]
                      for f in self.info if f[0] in ('M','H','R')]
                done={(f[1],f[2]) for f in self.info if f[0]=='H'}
                for f in self.info:
                    if f[0]!='M':continue
                    i,p=f[1],f[2]
                    for j in range(3):
                        if j!=0 or i==0:continue
                        if i==j or not p[j] or (i,j) in done:continue
                        if any(q[i] and not q[j] for q in pats):
                            tree=self.rminimiser(cons,eqs,nt,nreq,path+'w',i,j)
                            db.execute('INSERT OR REPLACE INTO nodes VALUES (?,?)',
                                       (key,pickle.dumps(tree,protocol=4)))
                            db.commit();self.saved+=1
                            return tree
            if args.strict_types and nt>=3:
                mat=self.mats(cons,eqs,lib.nv(nt))
                if self.strict_ok({},lib.F(-1),mat,lib.nv(nt)):
                    self.cnt('STRICT_EMPTY')
                    tree={'k':'TMPL','t':['F',[0]*7]}
                    db.execute('INSERT OR REPLACE INTO nodes VALUES (?,?)',
                               (key,pickle.dumps(tree,protocol=4)))
                    db.commit();self.saved+=1
                    return tree
            use_pair = args.zero_pair and nt >= 3
            done = {f[1] for f in self.info if f[0]=='ZE'}
            if use_pair and len(done)<2:
                n=lib.nv(nt); mat=self.mats(cons,eqs,n)
                if self.empty_check(mat,n):
                    tree={'k':'EMPTY'}
                else:
                    # These requests are legal throughout a region only after
                    # the unchanged request routine proves their validity (or
                    # makes covering halfspace splits). The choice is heuristic.
                    centre=self.samples(mat,n)[0]
                    if centre[0]<min(.5,centre[lib.TAU])-1e-7:
                        j=next(j for j in (1,2) if j not in done)
                        w=[{}, {}, {}]; w[0]={lib.X(0):lib.F(1)}
                        w[j]={lib.TAU:lib.F(1),lib.X(0):lib.F(-1)}
                        self.info.extend([('ZE',j),('Z',0)])
                        try: tree=self.request(cons,eqs,nt,nreq,path+'e'+str(j),w)
                        finally: self.info.pop();self.info.pop()
                    else:
                        tree=super().solve(cons,eqs,nt,fdepth,nreq,path)
            else:
                tree = super().solve(cons, eqs, nt, fdepth, nreq, path)
            db.execute('INSERT OR REPLACE INTO nodes VALUES (?,?)',
                       (key, pickle.dumps(tree, protocol=4)))
            db.commit(); self.saved += 1
            if time.time() - self.last_report > 25:
                print('PROGRESS', self.stats, 'saved', self.saved, 'hits', self.cache_hits,
                      'cpu', round(time.process_time()-self.c0, 1), flush=True)
                self.last_report = time.time()
            return tree
        except RuntimeError:
            if not self.deepest_saved:
                frontier = {'cons': cons, 'eqs': eqs, 'nt': nt, 'fdepth': fdepth,
                            'nreq': nreq, 'path': path, 'info': list(self.info), 'key': key}
                with open(str(prefix)+'.frontier.pkl', 'wb') as f:
                    pickle.dump(frontier, f)
                Path(str(prefix)+'.frontier.json').write_text(json.dumps(lib.enc(frontier)))
                self.deepest_saved = True
            raise
        finally:
            self.rng = previous_rng
            self.current_forms=previous_forms
    def samples(self,M,n):
        if args.strict_types and len(self.current_forms)>1:
            A,b,Ae,be=M
            rows=[];bounds=[]
            for form,h in self.current_forms:
                row=lib.np.zeros(n)
                for j,v in form.items():row[j]=-float(v)
                rows.append(row);bounds.append(-float(h))
            for eps in (1e-4,1e-6,1e-8):
                Mp=(lib.np.vstack([A,rows]),lib.np.concatenate([b,lib.np.array(bounds)-eps]),Ae,be)
                if lib.lp(lib.np.zeros(n),Mp,n).status==0:
                    return super().samples(Mp,n)
        return super().samples(M,n)
    def blocker_request(self,z,nt):
        if args.strong_blocker:
            from strong_blocker import blocker
            return blocker(self,z,nt)
        return super().blocker_request(z,nt)
    def request_candidates(self,z,nt):
        reqs=super().request_candidates(z,nt)
        if args.strong_blocker:
            from strong_blocker import rank_requests
            reqs=rank_requests(z,nt,reqs)
        if args.anchor_pair:
            from anchor_pair_request import discovery_request
            w=discovery_request(z,nt)
            if w is not None:
                self.cnt('ANCHOR_PAIR_REQUEST');reqs.insert(0,w)
        return reqs
    def strict_ok(self,d,rhs,M,n):
        if not args.strict_types:return super().strict_ok(d,rhs,M,n)
        A,b,Ae,be=M
        rows=[];bounds=[]
        for form,h in [(d,rhs)]+self.current_forms:
            row=lib.np.zeros(n+1)
            for j,v in form.items():row[j]=-float(v)
            row[-1]=1;rows.append(row);bounds.append(-float(h))
        A2=lib.np.vstack([lib.np.hstack([A,lib.np.zeros((len(A),1))]),rows])
        b2=lib.np.concatenate([b,bounds])
        Ae2=lib.np.hstack([Ae,lib.np.zeros((len(Ae),1))]) if len(Ae) else None
        obj=lib.np.zeros(n+1);obj[-1]=-1
        r=lib.linprog(obj,A_ub=A2,b_ub=b2,A_eq=Ae2,b_eq=be if len(Ae) else None,
                      bounds=[(None,None)]*n+[(None,1)],method='highs')
        return r.status==0 and -r.fun<=lib.TOL

s = Resumable()
C, E = lib.bc.base_region(reg, True, (lo, hi), excess=True)
metadata = {'box': [[str(v) for v in lo], [str(v) for v in hi]],
            'balanced': reg, 'sorted': True, 'excess': True, 'core': 'b4'}
metadata['extensions']=[x for x,b in [('strict-types',args.strict_types),
                                    ('conditional-rmin',args.conditional_rmin)] if b]
try:
    tree = s.solve(C, E, 0, 0, 0, '')
    nf = lib.count_fail(tree)
    metadata['tree'] = lib.enc(tree)
    Path(str(prefix)+'.json').write_text(json.dumps(metadata))
    status = 'CLOSED' if nf == 0 else 'FAIL'
except RuntimeError:
    status = 'TIMEOUT'; nf = None
summary = {'status': status, 'fails': nf, 'stats': s.stats, 'saved': s.saved,
           'cache_hits': s.cache_hits, 'wall_seconds': round(time.time()-s.t0, 2),
           'cpu_seconds': round(time.process_time()-s.c0, 2), 'parameters': vars(args)}
Path(str(prefix)+'.status.json').write_text(json.dumps(summary, indent=2))
print(json.dumps(summary), flush=True)
db.close()
