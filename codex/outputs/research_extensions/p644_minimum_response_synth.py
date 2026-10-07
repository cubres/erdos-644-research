"""Counterexample-guided synthesis for one minimum-sum triple response.

Discovery only until a separate proof/model audit is completed. Each template
has an exact piecewise-linear budget, from the ten price vertices for three
requests. No mass occupancy cutoff is used.
"""
from fractions import Fraction as F
from itertools import combinations, permutations, product
import json
from pathlib import Path
import sys
import time
import numpy as np
sys.path.insert(0,'/Users/cubres/Documents/Codex/2026-09-19/handoff-prompt-for-codex-astra-erd/work/research_dependencies')
import z3


def minimal(a):return tuple(m for m in sorted(set(a)) if not any(n!=m and n&m==n for n in a))
def blocker(a):return minimal([m for m in range(1,8) if all(m&n for n in a)])


def template_pool():
    ants=[a for n in range(1,8) for a in combinations(range(1,8),n) if minimal(a)==a]
    assert len(ants)==18
    comp=[[j for j,b in enumerate(ants) if all(x&y for x,y in product(a,b))] for a in ants]
    idx={a:i for i,a in enumerate(ants)};blocks=[idx[blocker(a)] for a in ants]
    transforms=[]
    for perm in permutations(range(3)):
        def move(m):return sum(1<<perm[j] for j in range(3) if m>>j&1)
        transforms.append([idx[tuple(sorted(move(m) for m in a))] for a in ants])
    # Price vertices scaled by twelve.
    prices=sorted(set(permutations((12,0,0)))|set(permutations((6,6,0)))|
                  set(permutations((6,3,3)))|{(4,4,4)})
    assert len(prices)==10
    cost=[[min(sum(q[j] for j in range(3) if m>>j&1) for m in a) for q in prices] for a in ants]
    seen=set();out=[];forms=[]
    for c in range(18):
        for y,z,g in product(comp[c],repeat=3):
            core=(c,y,z,g)
            canonical=min(tuple(t[i] for i in core) for t in transforms)
            if canonical in seen:continue
            seen.add(canonical)
            # Cells P,X',Y,Z,E-only-in-H,F-only-in-H,G-in-H,G-only.
            labs=(c,blocks[g],y,z,blocks[z],blocks[y],g,blocks[c])
            fs=sorted(set(tuple(cost[t][q] for t in labs) for q in range(10)))
            out.append([list(ants[j]) for j in labs]);forms.append(fs)
    matrix=np.array([fs+[fs[-1]]*(10-len(fs)) for fs in forms],dtype=np.int16)
    return out,forms,matrix


def run(minimum=True,limit=200,partial=0,gaps=False):
    root=Path('logs/astra_minimum_response_synth'+('_minimum' if minimum else '_plain')+('_gaps' if gaps else '')+'_p%d'%partial)
    root.mkdir(parents=True,exist_ok=True);started=time.time()
    labels,forms,matrix=template_pool();print('Canonical templates',len(labels),flush=True)
    z3.set_param(proof=True)
    p,e,f,g=z3.Reals('p e f g');variables=[p,e,f,g]
    s=z3.SolverFor('QF_LRA');s.set(timeout=60000)
    original=[200,43,186];x=original[partial];y,z=[a for i,a in enumerate(original) if i!=partial]
    caps=[500-x-y,500-x-z,500-y-z]
    s.add(p>=0,p<=1,e>=0,e<=caps[0],f>=0,f<=caps[1],g>=0,g<=caps[2],p+e+f+g<=500)
    if minimum:s.add(p+e+g>=x+z,p+f+g>=x+y)
    if gaps:
        for trace in (p+e,p+f,g):
            for lo,hi in ((98,106),(F(267,2),178),(216,237)):
                s.add(z3.Or(trace<str(lo),trace>str(hi)))
    weights=[p,x-p,z3.RealVal(y),z3.RealVal(z),e,f,g,caps[2]-g]
    selected=[];result=None
    for step in range(limit):
        answer=s.check()
        if answer==z3.unsat:
            (root/'coverage.smt2').write_text(s.to_smt2());proof=s.proof().sexpr();(root/'coverage.proof').write_text(proof)
            result={'status':'UNSAT_REQUIRES_INDEPENDENT_AUDIT','steps':step};break
        if answer!=z3.sat:result={'status':'UNKNOWN','reason':s.reason_unknown()};break
        model=s.model();point=[F(str(model.eval(v,model_completion=True))) for v in variables]
        pw=[point[0],x-point[0],F(y),F(z),point[1],point[2],point[3],caps[2]-point[3]]
        scores=(matrix@np.array(list(map(float,pw)))).max(axis=1)/12
        order=np.argsort(scores);winner=None
        for j in order:
            val=max(sum(a*b for a,b in zip(row,pw)) for row in forms[j])/12
            if val<=428:winner=int(j);break
            if scores[j]>428.001:break
        if winner is None:
            # An exact lower certificate for this finite template menu only.
            exact=[max(sum(a*b for a,b in zip(row,pw)) for row in fs)/12 for fs in forms]
            assert min(exact)>428
            result={'status':'EXACT_MENU_HOLE','point':list(map(str,point)),
                    'minimum_budget':str(min(exact)),'all_response_cells_positive':all(a>0 for a in pw)};break
        assert winner not in selected
        selected.append(winner)
        s.add(z3.Or(*[z3.Sum(*[int(a)*b for a,b in zip(row,weights)])>12*428 for row in forms[winner]]))
        print('Step',step,'counterexample',list(map(str,point)),'winning template',winner,'budget',str(val),flush=True)
    if result is None:result={'status':'UNKNOWN','reason':'iteration limit'}
    result.update(minimum_hypothesis=minimum,gap_hypothesis=gaps,partial_pair=partial,triple=[x,y,z],templates_in_pool=len(labels),selected_count=len(selected),elapsed=time.time()-started)
    (root/'result.json').write_text(json.dumps(result,indent=2))
    (root/'selected_templates.json').write_text(json.dumps([{'id':j,'labels':labels[j],'price_forms':forms[j]} for j in selected],indent=2))
    print(json.dumps(result,indent=2),flush=True)
    return result


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--plain',action='store_true');parser.add_argument('--limit',type=int,default=200)
    parser.add_argument('--partial',type=int,choices=range(3),default=0)
    parser.add_argument('--gaps',action='store_true')
    args=parser.parse_args();run(not args.plain,args.limit,args.partial,args.gaps)
