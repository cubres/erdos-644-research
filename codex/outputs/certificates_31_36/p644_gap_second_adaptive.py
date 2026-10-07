"""Seven-edge proof: a second adaptive response beats the fixed matching barrier."""
from itertools import combinations
from pathlib import Path
import json
from p644_strategy import Script,Aff,mass,contains,cellin,both,notin
from p644_strategy_lp import solve
from p644_strategy_budget import check_budget


def script(branch,fixed=False):
    if fixed:r,x,y,z,m,T=3900,2000,500,500,500,3254
    else:r,x,y,z,m,T=1200,603,190,180,190,1004
    half=(r+1)//2;s=y+z
    X=contains(1,2);Y=contains(1,3);Z=contains(2,3)
    A=contains(2,4);B=contains(3,4);C=contains(1,4)
    U=lambda E,L,placed:any(p(E,L,placed) for p in [Y,Z,A,C])
    hs=[(mass(X),x,x,(1,2)),(mass(Y),y,y,(1,3)),(mass(Z),z,z,(2,3))]
    hs.extend((mass(contains(*p)),0,0,p) for p in combinations(range(1,5),3))
    if fixed:
        hs.extend([(mass(A),500,500,(2,4)),(mass(C),500,500,(1,4)),(mass(B),2600,2600,(3,4))]);steps={}
    else:
        hs.extend([(mass(A),0,m,(2,4)),(mass(C),0,m,(1,4)),(mass(B),r//2+1,r,(3,4))])
        steps={4:{'picks':[('G0',cellin((1,2,3),3),T-x-y-z)],'avoid':[X,Y,Z,'G0']}}
    if branch==0:
        hs.append((mass(A)+mass(C),s,2*m,(1,2,3,4)))
        p=half-s;q=Aff(T-half)-mass(A)-mass(C)
    else:
        hs.append((mass(A)+mass(C),0,s,(1,2,3,4)))
        p=Aff(half)-mass(A)-mass(C);q=T-half-s
    hs.extend([(mass(contains(3,5)),0,m,(3,5)),(mass(contains(4,5)),0,m,(4,5))])
    I=contains(5);BI=both(B,I);BnI=lambda E,L,placed:B(E,L,placed) and not I(E,L,placed)
    steps.update({5:{'picks':[('B0',B,p),('X0',X,q)],'avoid':[U,'B0','X0']},
      6:{'picks':[('Bextra',BnI,Aff(T-x)-mass(BI))],'avoid':[X,BI,'Bextra']},
      7:{'avoid':[both(X,I),both(BnI,notin('Bextra'))]}})
    return Script(7,r,T,steps,False,hs)


if __name__=='__main__':
    rows=[]
    for branch,fixed in [(0,False),(1,False),(0,True)]:
        s=script(branch,fixed);q=solve(s,want=True);b=check_budget(s,want=True)
        print(branch,fixed,q['status'],b['status'],flush=True)
        assert q['status']=='PROVER WINS' and b['status']=='LEGAL'
        rows.append({'branch':branch,'fixed_obstruction_quadruple':fixed,'support':q,'budget':b})
    Path('logs/astra_gap_second_adaptive.json').write_text(json.dumps(rows,indent=1))
