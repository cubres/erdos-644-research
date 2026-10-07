"""Exact pointwise two-anchor terminating request via two V4 downboxes.
Input diagnostic rows are rational. Outputs a request only when all unit rows
in its retained box belong to one of the two certified V4-capacity downboxes.
"""
from fractions import Fraction as F
from pathlib import Path
import itertools,json,sys

def limits(x,a,b):
    return [min(xi,2*xi-2*ai-bi,4*xi-5*ai-bi) for xi,ai,bi in zip(x,a,b)]
def outside_pair(x,u,R,S):
    if sum(u)<1:return []
    bad=[]
    for i,j in itertools.product(range(3),repeat=2):
        if i==j:
            if max(R[i],S[i])<min(u[i],F(1)):bad.append((i,j))
        elif u[i]>R[i] and u[j]>S[j] and max(F(0),R[i])+max(F(0),S[j])<1:
            bad.append((i,j))
    return bad

def pair_best(x,a,b):
    R=limits(x,a,b);S=limits(x,b,a)
    options=[sorted({xi}|{v for v in (ri,si) if 0<=v<=xi}) for xi,ri,si in zip(x,R,S)]
    best=None
    for u in itertools.product(*options):
        # Empty rank-one request only yields the known N-1 limiting bound.
        if sum(u)<1:continue
        if outside_pair(x,u,R,S):continue
        cost=sum(x)-sum(u)
        if best is None or cost<best['cost']:
            best={'cost':cost,'retained':u,'R':R,'S':S}
    return best

def enc(o):
    if isinstance(o,F):return str(o)
    if isinstance(o,dict):return {k:enc(v) for k,v in o.items()}
    if isinstance(o,(list,tuple)):return [enc(v) for v in o]
    return o
if __name__=='__main__':
    p=Path(sys.argv[1]);z=json.loads(p.read_text());x=list(map(F,z['capacities']));T=[list(map(F,t)) for t in z['types']]
    found=[]
    for i,j in itertools.combinations(range(len(T)),2):
        q=pair_best(x,T[i],T[j])
        if q:q['anchors']=[i,j];found.append(q)
    found.sort(key=lambda v:v['cost'])
    out={'best':found[0] if found else None,'global_tau':F(z['global_tau_parameter']),
         'number_anchor_pairs_with_request':len(found),'all':found}
    out['closes_point']=bool(found and found[0]['cost']<out['global_tau'])
    dest=p.with_name(p.stem+'.anchor_pair.json');dest.write_text(json.dumps(enc(out),indent=2))
    print(json.dumps(enc({k:v for k,v in out.items() if k!='all'}),indent=2))

def discovery_request(z,nt):
    """Return an affine deletion vector selected at a numerical search sample.
    Selection and branch choice are heuristic; ordinary exact request legality
    and the resulting exact template leaves remain mandatory.
    """
    from b4core import X,T,TOFF
    x=z[:3];types=z[TOFF:TOFF+3*nt].reshape(nt,3);tau=z[6]
    best=None
    for a,b in itertools.combinations(range(nt),2):
        q=pair_best(x,types[a],types[b])
        if q is not None and q['cost']<tau-1e-7 and (best is None or q['cost']<best[0]):
            best=(q['cost'],a,b,q)
    if best is None:return None
    _,a,b,q=best;out=[]
    for i,ui in enumerate(q['retained']):
        if abs(ui-x[i])<1e-10:out.append({});continue
        aa,bb=(a,b) if abs(ui-q['R'][i])<1e-10 else (b,a)
        pieces=[x[i],2*x[i]-2*types[aa,i]-types[bb,i],4*x[i]-5*types[aa,i]-types[bb,i]]
        k=min(range(3),key=lambda k:pieces[k])
        if k==0:out.append({})
        elif k==1:out.append({X(i):F(-1),T(aa,i):F(2),T(bb,i):F(1)})
        else:out.append({X(i):F(-3),T(aa,i):F(5),T(bb,i):F(1)})
    return out
