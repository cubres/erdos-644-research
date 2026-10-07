"""Exact local probes of the generalized fifth-edge matching lemma.

SAT means only that this sufficient lemma leaves a response uncovered.
UNSAT is discovery, not an independently checked universal certificate.
No discovery modules are imported.
"""
from fractions import Fraction as F
from itertools import permutations, product
from pathlib import Path
import json
import sys
sys.path.insert(0, '/Users/cubres/Documents/Codex/2026-09-19/handoff-prompt-for-codex-astra-erd/work/research_dependencies')
import z3


GAPS = [(F(196,1000), F(212,1000)),
        (F(267,1000), F(356,1000)),
        (F(432,1000), F(474,1000))]
T = F(107,125)


def maximum(values):
    answer = values[0]
    for value in values[1:]:
        answer = z3.If(value > answer, value, answer)
    return answer


def local_probe(y):
    x, z = F(2,5), F(93,250)
    total = x+y+z
    result = {'triple': list(map(str, (x,y,z))), 'budget': str(T)}
    if total > T:
        return dict(result, status='WHOLE_CORE_REQUEST_ILLEGAL', excess=str(total-T))
    solver = z3.SolverFor('QF_LRA')
    solver.set(timeout=20000)
    a,b,c = z3.Reals('a b c')
    def q(v):
        return z3.RealVal(str(v)) if isinstance(v,(F,int)) else v
    for v,cap in ((a,1-x-z),(b,1-y-z),(c,1-x-y)):
        solver.add(v>=0,v<=q(cap))
        for lo,hi in GAPS:
            solver.add(z3.Or(v<q(lo),v>q(hi)))
        solver.add(z3.Or(v<=q(x),v>q(F(1,2))))
    solver.add(a+b+c<=1)
    # Pair cells for E,F,G,H: EF=x, EG=y, FG=z, FH=a, GH=b, EH=c.
    pair={(0,1):q(x),(0,2):q(y),(1,2):q(z),
          (1,3):a,(2,3):b,(0,3):c}
    cell=lambda i,j:pair[tuple(sorted((i,j)))]
    caps=GAPS+[(x,F(1,2))]
    regions=[]
    for e,f,g,h in permutations(range(4)):
        X,B=cell(e,f),cell(g,h)
        s=cell(e,g)+cell(f,g)
        t=cell(e,h)+cell(f,h)
        # Only one of G or H must have a small I-trace: B is contained
        # in each, so either conclusion suffices to bound B intersect I.
        for trace_sum,(ell,hcut) in product((s,t),caps):
            p=maximum([q(0),q(1-hcut)-trace_sum])
            u=s+t
            good=z3.And(p<=B,u+p<=q(T),X+q(ell)<=q(T),
                        X+B<=q(2*T),2*X+B+u+p<=q(3*T))
            regions.append(good)
            solver.add(z3.Not(good))
    outcome=solver.check()
    if outcome==z3.sat:
        model=solver.model()
        response=[F(str(model.eval(v))) for v in (a,b,c)]
        assert min(response)>=0 and sum(response)<=1
        for val,cap in zip(response,(1-x-z,1-y-z,1-x-y)):
            assert val<=cap and all(val<lo or val>hi for lo,hi in GAPS)
            assert val<=x or val>F(1,2)
        assert all(z3.is_false(model.eval(reg)) for reg in regions)
        result.update(status='EXACT_UNCOVERED_RESPONSE',response=list(map(str,response)))
    elif outcome==z3.unsat:
        result.update(status='UNSAT_DISCOVERY_ONLY')
    else:
        result.update(status='UNKNOWN',reason=solver.reason_unknown())
    return result


def regression():
    # Independently test all residual cardinalities for the actual last-two
    # construction, at bounded integer parameters. This checks the algebra
    # and pair coverage; the universal statement has a separate hand proof.
    count=0
    for T in range(1,9):
        for x,b,u,p,delta in product(range(T+1),repeat=5):
            if p>b or u+p>T or x+delta>T: continue
            if x+b>2*T or 2*x+b+u+p>3*T: continue
            q=min(x,T-u-p)
            for xi in range(x-q+1):
                for bi in range(min(b-p,delta)+1):
                    # X=[0,x), B=[x,x+b). Initial response occupies prefixes.
                    X=set(range(x));B=set(range(x,x+b))
                    XI=set(range(xi));BI=set(range(x,x+bi))
                    size=min(b,T-x)
                    assert bi<=size
                    B1=set(range(x,x+size))
                    D1=X|B1;D2=XI|(B-B1)
                    assert max(len(D1),len(D2))<=T
                    assert all({v,w}<=D1 or {v,w}<=D2
                               for v in X for w in B if v in XI or w in BI)
                    count+=1
    return count


if __name__=='__main__':
    count=regression()
    print('PASS bounded integer allocation regressions:',count,flush=True)
    rows=[]
    for y in (F(86,1000),F(84,1000),F(82,1000),F(80,1000),F(75,1000)):
        row=local_probe(y);rows.append(row);print(json.dumps(row),flush=True)
    output={'integer_regressions':count,'probes':rows,
            'scope':'These probes test one sufficient fifth-edge lemma after an unpadded whole-core fourth request.'}
    Path('logs/astra_agent_audit_generalized_matching.json').write_text(json.dumps(output,indent=2)+'\n')
