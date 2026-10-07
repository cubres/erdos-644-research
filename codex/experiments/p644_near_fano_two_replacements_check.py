"""Exact all-b certificate for two legal 108b requests and nine actual rows.
Standard library only. No claim of high transversal number is made.
"""
from fractions import Fraction as F
from itertools import combinations
import json
from pathlib import Path

lines=[frozenset(t) for t in combinations(range(7),3)
       if (t[0]+1)^(t[1]+1)^(t[2]+1)==0]
records=[{'type':L,'line':L,'extra':None,'weight':(33,0)} for L in lines]
records += [{'type':L|{h},'line':L,'extra':h,'weight':(1,0)}
            for L in lines for h in sorted(set(range(7))-L)]
xline=frozenset((0,1,2))
for r in records:
    r['mask']=127^sum(1<<j for j in r['type'])
    if r['line']==xline and r['extra'] is None:r['weight']=(33,-1)
records += [{'type':xline,'line':None,'extra':None,'weight':(0,1),
             'mask':(127^sum(1<<j for j in xline))|1,'name':'x'},
            {'type':None,'line':None,'extra':None,'weight':(1,0),'mask':0,'name':'Y'}]
C1spec=[(frozenset((0,1,2)),3),(frozenset((0,3,4)),5),(frozenset((0,5,6)),1)]
C2spec=[(L,h+1) for L,h in C1spec]
C1={i for i,r in enumerate(records) if(r['line'],r['extra'])in C1spec}
C2={i for i,r in enumerate(records) if(r['line'],r['extra'])in C2spec}
A={i for i,r in enumerate(records) if r['line'] is not None and 0 not in r['line']}
Adef={i for i in A if records[i]['extra'] is not None}
# The eight removed A-defects are precisely those assigned to lines 135 and 146
# in zero-based row coordinates.
R={i for i in Adef if records[i]['line'] in [frozenset((1,3,5)),frozenset((1,4,6))]}
assert len(R)==8
G=(A-R)|C1|{36};H=(A-R)|C2|{36}
for i,r in enumerate(records):r['mask']|=(int(i in G)<<7)|(int(i in H)<<8)
w=[r['weight'] for r in records];m=[r['mask'] for r in records];n=len(w)
P={i for i,r in enumerate(records) if r['line'] is not None and 0 in r['line']}|{35}
D1=P-C1;D2=P-C2

def add(u,v):return tuple(a+b for a,b in zip(u,v))
def sumw(indices):
    out=(0,0)
    for i in indices:out=add(out,w[i])
    return out

def product(u,v):
    a,c=u;b,d=v
    return(F(a*b),F(a*d+b*c),F(c*d))

def evaluate(poly,b):
    return sum(c*F(b)**(len(poly)-1-i) for i,c in enumerate(poly))

def graph(rows):
    mask=sum(1<<j for j in rows)
    edges=[(i,j)for i in range(n)for j in range(i+1,n)if(m[i]|m[j])&mask==mask]
    loops=[i for i in range(n)if m[i]&mask==mask]
    ends={i for pair in edges for i in pair}
    # Any loop type is adjacent to all other nonempty types, so already an endpoint.
    assert set(loops)<=ends
    pp=sumw(ends);qq=(F(0),F(0),F(0))
    for i,j in edges:qq=add(qq,product(w[i],w[j]))
    for i in loops:
        a,c=w[i];qq=add(qq,tuple(v/2 for v in(F(a*a),F(2*a*c-a),F(c*c-c))))
    return pp,qq

assert sumw(D1)==sumw(D2)==(108,0)
assert not(G&D1)and not(H&D2)
assert sumw(G)==sumw(H)==(144,0)
assert sumw(P)==(111,0)
ranks=[sumw(i for i in range(n)if m[i]&(1<<j))for j in range(9)]
assert ranks==[(144,1)]+[(144,0)]*8
six=[]
for rows in combinations(range(9),6):
    pp,qq=graph(rows);delta=(pp[0]-111,pp[1])
    # A linear polynomial nonnegative on all b>=1.
    assert delta[0]>=0 and sum(delta)>=0,(rows,pp)
    if delta==(0,0):
        dq=add(qq,(-3669,0,0))
        # Change variable b=u+1, and check all coefficients nonnegative.
        assert min(dq[0],2*dq[0]+dq[1],sum(dq))>=0,(rows,qq)
    elif sum(delta)==0:
        assert evaluate(qq,1)>=3669,(rows,qq)
    six.append((rows,pp,qq))
assert graph(range(1,7))==((111,0),(3669,0,0))
seven=[]
for rows in combinations(range(9),7):
    pp,qq=graph(rows)
    assert qq[0]>=0 and 2*qq[0]+qq[1]>=0 and sum(qq)>0,(rows,qq)
    seven.append((rows,pp,qq))
# The full nine-row family has transversal exactly three.
full=511
assert not any((m[i]|m[j])==full for i in range(n)for j in range(i,n))
triple=next(z for z in combinations(range(n),3)if m[z[0]]|m[z[1]]|m[z[2]]==full)

def pack(v):
    if isinstance(v,F):return int(v)if v.denominator==1 else str(v)
    if isinstance(v,(list,tuple)):return[pack(z)for z in v]
    return v
out={'status':'PASS','valid_for':'every integer b>=1','six_tuples':len(six),'seven_tuples':len(seven),
     'rank':'144b+1','endpoint_minimum':'111b','pair_minimum_at_endpoint_minimum':'3669b^2',
     'request_sizes':['108b','108b'],'tau':3,'transversal_cells':list(triple),
     'C1':sorted(C1),'C2':sorted(C2),'removed_A_defects':sorted(R),
     'G':sorted(G),'H':sorted(H),'D1':sorted(D1),'D2':sorted(D2),
     'weights_affine_b':w,'masks':m,
     'minimum_new_endpoint_at_b_100':min(int(evaluate(pp,100))for rows,pp,qq in six if 7 in rows or 8 in rows),
     'minimum_double_endpoint_at_b_100':min(int(evaluate(pp,100))for rows,pp,qq in six if 7 in rows and 8 in rows),
     'six':pack(six),'seven':pack(seven)}
Path('outputs/agent_near_fano_two_replacements_certificate.json').write_text(json.dumps(out,indent=2))
print(json.dumps({k:v for k,v in out.items()if k not in ['six','seven','weights_affine_b','masks','D1','D2','G','H']},indent=2))
