"""Adaptive final request: avoid every endpoint of a two-piercer.

Given at most six edges with empty common intersection, let K be the union of their occupied Venn cells
that have a partner cell covering all rows. Avoiding K destroys every
two-piercer. On a fixed pick branch, maximal feasible support is attained
by averaging feasible points. If that support has local (7,2), configurations
with that support are dense in the branch, so the supremum of |K| is exactly
an ordinary LP objective on the cells in the maximal-support core.

All used primal vectors and duals have exact Fraction checks. Matrix input
has the same integer/dyadic qualification as p644_strategy_budget.py.
"""
from fractions import Fraction as F
from p644_strategy_budget import model,choices,minimize
from p644_strategy_lp import support_condition


def core_bound(script,seconds=30,want=False,max_branches=4096):
    assert 1<=script.J<=6
    m=model(script);branches=list(choices(m));out=[]
    if len(branches)>max_branches:return {'status':'UNKNOWN','reason':'branch limit'}
    for ys in branches:
        support=set();points=[]
        for iteration in range((1<<script.J)+1):
            c=[-int(E not in support) for E,L in m['atoms']]
            q=minimize(m,script.J,ys,c,seconds=seconds,want=True)
            if q['status']=='EMPTY':out.append({'branch':ys,'status':'EMPTY','certificate':q});break
            if q['status']!='BOUND' or 'primal' not in q:
                return {'status':'UNKNOWN','reason':'support recovery','branch':ys,'result':q}
            x=list(map(F,q['primal']));points.append(x)
            new={E for (E,L),v in zip(m['atoms'],x) if v>0}
            old=set(support);support.update(new)
            if support!=old:continue
            if F(q['lower'])<0:return {'status':'UNKNOWN','reason':'support dual not tight'}
            obstruction=support_condition(script,support)
            if obstruction is not None:
                out.append({'branch':ys,'status':'PREFIX_ALREADY_WINS','obstruction':obstruction,'certificate':q});break
            Q=frozenset(range(1,script.J+1))
            if Q in support:
                # A common point plus any point of the next edge is a
                # two-piercer, even if that second point is outside the
                # entire previous union. Empty outside cells cannot be
                # discarded in this case.
                out.append({'branch':ys,'status':'ONE_POINT_PREFIX','certificate':q})
                break
            core={E for E in support if any(E|G==Q for G in support)}
            c=[-int(E in core) for E,L in m['atoms']]
            b=minimize(m,script.J,ys,c,seconds=seconds,want=want)
            if b['status']!='BOUND':return {'status':'UNKNOWN','reason':'core bound','result':b}
            row={'branch':ys,'status':'CORE_BOUND','support':[sorted(E) for E in support],
                 'core':[sorted(E) for E in core],'upper':str(-F(b['lower'])),'bound_certificate':b,
                 'support_certificate':q}
            if want:
                mean=[sum(P[j] for P in points)/len(points) for j in range(len(x))]
                row['maximal_support_point']=[str(v) for v in mean]
                row['atoms']=[{'edges':sorted(E),'picks':sorted(L)} for E,L in m['atoms']]
            out.append(row);break
        else:return {'status':'UNKNOWN','reason':'support iteration bound'}
    return {'status':'FINAL_REQUEST_LEGAL' if all(b['status']!='ONE_POINT_PREFIX' and
            (b['status']!='CORE_BOUND' or F(b['upper'])<=F(str(script.budget))) for b in out)
            else 'CORE_EXCEEDS_BUDGET','branches':out}


if __name__=='__main__':
    from pathlib import Path
    import json
    from p644_fkw_check import fkw_script
    from p644_strategy import Script
    report=[]
    for budget in (14,13):
        s=fkw_script(2,8,4,2,budget)
        s=Script(6,s.D,s.budget,{j:st for j,st in s.steps.items() if j<=6},False,s.hyps)
        q=core_bound(s,want=True)
        print(budget,q['status'],max((F(b['upper']) for b in q.get('branches',[]) if b['status']=='CORE_BOUND'),default=None),flush=True)
        report.append({'budget':budget,'result':q})
    from p644_astra_gap_script import script as gap_script
    s=gap_script()
    s=Script(6,s.D,s.budget,{j:st for j,st in s.steps.items() if j<=6},False,s.hyps)
    q=core_bound(s,want=True)
    assert q['status']=='FINAL_REQUEST_LEGAL'
    report.append({'name':'gap_prefix','budget':85,'result':q})
    print('gap_prefix',q['status'],flush=True)
    q=core_bound(Script(6,1,1,{},False),want=True)
    assert q['status']=='CORE_EXCEEDS_BUDGET' and q['branches'][0]['status']=='ONE_POINT_PREFIX'
    report.append({'name':'common_point_regression','result':q})
    print('common_point_regression',q['status'],flush=True)
    Path('logs/astra_core_request_checks.json').write_text(json.dumps(report,indent=1))
