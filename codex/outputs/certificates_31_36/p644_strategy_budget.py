"""Exact-checked conservative request budgets for the strict-support game.

Every numerical primal/dual used below is checked with Fraction arithmetic.
The source builder's finite decimal matrix entries are the exact input data;
use integer/dyadic scripts, or audit non-dyadic expressions separately.
No local piercing/intersecting constraints are imposed: a LEGAL result bounds
all geometric prefix configurations and is therefore conservative. An excess
is NOT asserted to be a reachable adversary. Picks are checked for a
nonnegative requested size before their min(size, host) constraint is imposed.
"""
import itertools as it
from fractions import Fraction as F
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix, vstack, hstack
from p644_strategy import Script, Aff, inpick
from p644_strategy2 import build
from p644_strategy_lp import frac, exact_rows, dot, recover


def model(script):
    relaxed=Script(script.J,script.D,script.budget,script.steps,False,script.hyps)
    if hasattr(script,'final_picks'):relaxed.final_picks=script.final_picks
    return build(relaxed,continuous=True,eps=0,subfamilies=[])


def choices(m):
    out=[]
    for host,placed,size in m['pickhost'].values():
        zero=(isinstance(size,Aff) and not size.terms and size.const==0) or (not isinstance(size,Aff) and size==0)
        out.append((1,) if zero else (0,1))
    return it.product(*out)


def minimize(m,J,ys,c,constant=F(0),seconds=30,want=False):
    """Certified lower bound for c.x+constant, or exact infeasibility."""
    n=len(m['atoms']);fixed=np.r_[np.ones((1<<J)-1),ys]
    rhs=m['A'][:,n:]@fixed
    lo=m['lbs']-rhs;hi=m['ubs']-rhs;A=m['A'][:,:n].tocsr()
    eq=np.isfinite(lo)&np.isfinite(hi)&(lo==hi)
    upp=np.isfinite(hi)&~eq;low=np.isfinite(lo)&~eq
    Ae=A[eq];be=hi[eq];Au=vstack([A[upp],-A[low]],format='csr');bu=np.r_[hi[upp],-lo[low]]
    er=exact_rows(Ae);ur=exact_rows(Au);eb=list(map(frac,be));ub=list(map(frac,bu))
    c=list(map(F,c));constant=F(constant)
    q=linprog(np.array(c,dtype=float),A_ub=Au,b_ub=bu,A_eq=Ae,b_eq=be,bounds=(0,None),
              method='highs',options={'time_limit':seconds})
    if q.status==2:
        D=hstack([Au.T,Ae.T],format='csr');rhsdual=np.r_[bu,be]
        dq=linprog(np.zeros(len(rhsdual)),A_ub=vstack([D,csr_matrix(-rhsdual[None,:])]),
                   b_ub=np.r_[np.zeros(n),-1],bounds=[(None,0)]*len(bu)+[(None,None)]*len(be),
                   method='highs',options={'time_limit':seconds})
        if dq.status!=0:return {'status':'UNKNOWN','reason':'Farkas discovery'}
        yu=recover(dq.x[:len(bu)]);ye=recover(dq.x[len(bu):]);infeasible=True
    elif q.status==0:
        ye=recover(q.eqlin.marginals);yu=recover(q.ineqlin.marginals);infeasible=False
    else:return {'status':'UNKNOWN','reason':q.message}
    if any(y>0 for y in yu):return {'status':'UNKNOWN','reason':'dual sign'}
    grad=[F(0)]*n
    for rows,weights in [(er,ye),(ur,yu)]:
        for row,y in zip(rows,weights):
            for j,a in row:grad[j]+=y*a
    val=sum((y*b for y,b in zip(ye,eb)),F(0))+sum((y*b for y,b in zip(yu,ub)),F(0))
    target=[F(0)]*n if infeasible else c
    if any(a>b for a,b in zip(grad,target)) or (infeasible and val<=0):
        return {'status':'UNKNOWN','reason':'exact dual recovery'}
    result={'status':'EMPTY' if infeasible else 'BOUND','lower':str(val+constant),
            'dual_eq':list(map(str,ye)),'dual_ub':list(map(str,yu))}
    if not infeasible:
        x=recover(q.x)
        if all(v>=0 for v in x) and all(dot(r,x)==b for r,b in zip(er,eb)) and all(dot(r,x)<=b for r,b in zip(ur,ub)):
            result['primal_value']=str(sum((a*b for a,b in zip(c,x)),constant))
            if want:result['primal']=list(map(str,x))
    return result


def check_budget(script,seconds=30,max_branches=4096,want=False):
    report=[]
    for j in range(2,script.J+1):
        st=script.steps.get(j,{})
        if not st.get('avoid') and not st.get('picks'):continue
        placed=frozenset(range(1,j))
        hs=[h for h in script.hyps if len(h)>=4 and frozenset(h[3])<=placed]
        pre=Script(j-1,script.D,script.budget,{i:s for i,s in script.steps.items() if i<j},False,hs)
        pre.final_picks=[]
        # A negative requested size can make every full branch infeasible.
        # Check before imposing that pick, so it cannot create a false win.
        for name,host,size in st.get('picks',[]):
            if isinstance(size,Aff) and size.terms:
                m=model(pre);c=[sum((frac(w) for p,w in size.terms if p(E,L,placed)),F(0)) for E,L in m['atoms']]
                branches=list(choices(m))
                if len(branches)>max_branches:return {'status':'UNKNOWN','reason':'branch limit','steps':report}
                for ys in branches:
                    out=minimize(m,pre.J,ys,c,frac(size.const),seconds,want)
                    report.append({'step':j,'check':'pick nonnegative','pick':name,'branch':ys,'result':out})
                    if out['status']=='UNKNOWN':return {'status':'UNKNOWN','steps':report}
                    if out['status']=='BOUND' and F(out['lower'])<0:
                        return {'status':'UNPROVED','reason':'negative pick size not excluded','steps':report}
            else:
                val=frac(size.const if isinstance(size,Aff) else size)
                if val<0:return {'status':'INVALID','reason':'negative constant pick size','step':j,'pick':name}
            pre.final_picks.append((name,host,size))
        m=model(pre);preds=[inpick(p) if isinstance(p,str) else p for p in st.get('avoid',[])]
        c=[-int(any(p(E,L,placed) for p in preds)) for E,L in m['atoms']]
        branches=list(choices(m))
        if len(branches)>max_branches:return {'status':'UNKNOWN','reason':'branch limit','steps':report}
        for ys in branches:
            out=minimize(m,pre.J,ys,c,seconds=seconds,want=want)
            report.append({'step':j,'check':'union budget','branch':ys,'result':out})
            if out['status']=='UNKNOWN':return {'status':'UNKNOWN','steps':report}
            if out['status']=='BOUND' and -F(out['lower'])>frac(script.budget):
                return {'status':'UNPROVED','reason':'geometric prefix exceeds budget','steps':report}
    return {'status':'LEGAL','steps':report}


if __name__=='__main__':
    import json
    from pathlib import Path
    from p644_strategy import contains, mass
    from p644_fkw_check import fkw_script
    cases=[('fkw14',fkw_script(2,8,4,2,14)),('fkw13',fkw_script(2,8,4,2,13)),
           ('overlapping_avoids',Script(2,16,16,{2:{'avoid':[contains(1),contains(1)]}},False)),
           ('negative_constant',Script(2,16,16,{2:{'picks':[('P',contains(1),-1)],'avoid':['P']}},False)),
           ('negative_affine',Script(2,16,16,{2:{'picks':[('P',contains(1),mass(contains(1))-17)],'avoid':['P']}},False))]
    report=[]
    for name,S in cases:
        out=check_budget(S,want=True);report.append({'name':name,'result':out})
        print(name,out['status'],out.get('reason',''),flush=True)
    Path('logs/astra_budget_checks.json').write_text(json.dumps(report,indent=1))
