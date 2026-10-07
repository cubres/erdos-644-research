"""Representative integral checks of both branches of Lemma 7.33."""
from p644_strategy import Script,Aff,mass,contains,cellin,both,notin,inpick
from p644_strategy_lp import solve
from p644_strategy_budget import check_budget
from pathlib import Path
import json


def script(branch):
    r,x,y,z,T=1000,482,164,82,850
    X=contains(1,2);Y=contains(1,3);Z=contains(2,3)
    Gprivate=cellin((1,2,3),3)
    A=contains(2,4);B=contains(3,4);C=contains(1,4)
    hs=[(mass(X),x,x,(1,2)),(mass(Y),y,y,(1,3)),(mass(Z),z,z,(2,3)),(mass(contains(1,2,3)),0,0,(1,2,3))]
    steps={4:{'picks':[('P',Gprivate,max(0,r-2*(T-x)-y-z))],'avoid':[X,Y,Z,'P']}}
    B2=both(B,notin('B1'))
    if branch==0:
        hs.append((mass(B),r+y+z-T+1,r,(1,2,3,4)))
        steps.update({5:{'picks':[('B1',B,T-x)],'avoid':[X,'B1']},6:{'avoid':[X,B2]},7:{'avoid':[Y,Z,A,C]}})
    else:
        hs.append((mass(B),0,r+y+z-T,(1,2,3,4)))
        Ar=both(A,notin('A1'));Alast=both(Ar,notin('A2'))
        steps.update({5:{'picks':[('B1',B,T-x-y),('A1',A,Aff(T-x-y)-mass(inpick('B1')))],'avoid':[X,Y,'B1','A1']},
          6:{'picks':[('A2',Ar,Aff(T-x-y)-mass(B2))],'avoid':[X,Y,B2,'A2']},7:{'avoid':[Y,Z,C,Alast]}})
    return Script(7,r,T,steps,False,hs)


if __name__=='__main__':
    rows=[]
    for branch in range(2):
        s=script(branch);q=solve(s,want=True);b=check_budget(s,want=True)
        print(branch,q['status'],b['status'],flush=True)
        assert q['status']=='PROVER WINS' and b['status']=='LEGAL'
        rows.append({'branch':branch,'support':q,'budget':b})
    Path('logs/astra_padded_dominant.json').write_text(json.dumps(rows,indent=1))
