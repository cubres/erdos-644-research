"""Independent symbolic-q input reconstruction and bound CPC replay.

The generic stdlib parser/checker is reused from the concrete certificate;
the parametric equations below are rebuilt independently of its exporter.
"""
from pathlib import Path
import argparse,json
import p644_agent_audit_anchor_check as base
from p644_agent_audit_anchor_check import Q,add,scale,const,var,sub,atom,boolean,le,eq

base.NAMES=base.NAMES|{'q'}

def reconstruct():
    q=var('q');ans={le({},var(n))for n in base.NAMES if n!='q'}
    ans.add(le(const(Q(87,100)),q));ans.add(atom('lt',sub(q,const(Q(7,8)))))
    for side in base.SETS:
        ans.add(eq(add(*(var(side+'_'+str(m))for m in base.SETS[side])),q))
    aa=list(base.SETS['a'])
    for i,m in enumerate(aa):
        for n in aa[i+1:]:
            if base.SETS['a'][m].isdisjoint(base.SETS['a'][n]):
                ans.add(boolean('or',[eq(var('a_'+str(m)),{}),eq(var('a_'+str(n)),{})]))
        for n in base.SETS['b']:
            if base.SETS['a'][m].isdisjoint(base.SETS['b'][n]):
                ans.add(boolean('or',[eq(var('a_'+str(m)),{}),eq(var('b_'+str(n)),{})]))
    # Independently expanded affine endpoints. No delta/epsilon expression
    # or interval array is imported from the exporter.
    end=add(const(Q(473,160)),scale(-Q(59,20),q))
    isolated=add(const(Q(113,80)),scale(-Q(23,20),q))
    lo=add(const(Q(7,160)),scale(Q(9,20),q))
    hi=add(const(Q(21,160)),scale(Q(7,20),q))
    middle=add(const(-Q(219,160)),scale(Q(21,10),q))
    reflect=lambda x:sub(const(1),x)
    intervals=[(reflect(q),end),(isolated,isolated),(lo,hi),
               (middle,reflect(middle)),(reflect(hi),reflect(lo)),
               (reflect(isolated),reflect(isolated)),(reflect(end),q)]
    traces=[]
    for i in range(6):
        da=add(*(var('a_'+str(m))for m,s in base.SETS['a'].items()if i in s))
        db=add(*(var('b_'+str(m))for m,s in base.SETS['b'].items()if i in s))
        ans.add(eq(add(da,db),sub(scale(2,q),const(1))))
        t=sub(q,da);traces.append(t)
        ans.add(boolean('or',[boolean('and',[le(a,t),le(t,b)])for a,b in intervals]))
    for i in range(5):ans.add(le(traces[i],traces[i+1]))
    return ans

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--root',default=str(Path(__file__).parent/'logs/astra_agent_audit_anchor_parametric'))
    p.add_argument('--ethos',default=str(base.WORK/'proof_checkers/ethos-0.2.4/ethos'))
    p.add_argument('--signatures',default=str(base.WORK/'proof_checkers/cvc5-1.4.0-signatures/cpc'))
    p.add_argument('--report');a=p.parse_args()
    base.expected=reconstruct
    result=base.check(a.root,a.ethos,a.signatures,stem='parametric')
    if a.report:Path(a.report).write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))
