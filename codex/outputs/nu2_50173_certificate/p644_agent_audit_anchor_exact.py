"""Exact one-anchor QF_LRA certificate for a NEW residual trace candidate.

This exports the exact rational mathematical model and asks cvc5 for a CPC
proof, then checks it with the existing external Ethos installation.
"""
from pathlib import Path
import argparse,json,sys,time
WORK=Path('/Users/cubres/Documents/Codex/2026-09-19/handoff-prompt-for-codex-astra-erd/work')
sys.path.insert(0,str(WORK/'research_dependencies'))
import z3

ROOT=Path(__file__).parent/'logs/astra_agent_audit_anchor_exact'
K=140000;Q=121800
INTERVALS=[(18200,54586),(57660,57660),(60914,61054),(64155,75845),
           (78946,79086),(82340,82340),(85414,121800)]

def generate():
    s=z3.Solver()
    am=[m for m in range(1,64)if bin(m).count('1')>=3]
    bm=[m for m in range(1,64)if bin(m).count('1')>=2]
    a={m:z3.Real('a_%d'%m)for m in am};b={m:z3.Real('b_%d'%m)for m in bm}
    for v in list(a.values())+list(b.values()):s.add(v>=0)
    s.add(z3.Sum(list(a.values()))==Q,z3.Sum(list(b.values()))==Q)
    for i,m in enumerate(am):
        for n in am[i+1:]:
            if m&n==0:s.add(z3.Or(a[m]==0,a[n]==0))
        for n in bm:
            if m&n==0:s.add(z3.Or(a[m]==0,b[n]==0))
    first=[]
    for j in range(6):
        da=z3.Sum([v for m,v in a.items()if m>>j&1])
        db=z3.Sum([v for m,v in b.items()if m>>j&1])
        s.add(da+db==2*Q-K)
        tr=Q-da;first.append(tr)
        s.add(z3.Or(*[z3.And(tr>=lo,tr<=hi)for lo,hi in INTERVALS]))
    for j in range(5):s.add(first[j]<=first[j+1])
    ROOT.mkdir(exist_ok=True)
    source=ROOT/'residual.smt2';source.write_text(s.to_smt2())
    (ROOT/'instance.json').write_text(json.dumps({'rank':K,'part_sizes':[Q,Q],
        'intervals':INTERVALS,'A_minimum_complement_degree':3,'B_minimum_complement_degree':2,
        'constraints':len(s.assertions()),'source':str(source)},indent=2))
    return s

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--seconds',type=float,default=60)
    p.add_argument('--solver',choices=['cvc5','z3','generate'],default='cvc5');args=p.parse_args()
    s=generate()
    if args.solver=='cvc5':
        from p644_box_case_cvc5 import worker
        print(json.dumps(worker(('residual',args.seconds,str(ROOT))),indent=2))
    elif args.solver=='z3':
        s.set(timeout=int(1000*args.seconds));start=time.time();r=s.check()
        out={'status':str(r),'seconds':time.time()-start}
        if r==z3.sat:out['model']=str(s.model())
        if r==z3.unknown:out['reason']=s.reason_unknown()
        (ROOT/'residual_z3.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
