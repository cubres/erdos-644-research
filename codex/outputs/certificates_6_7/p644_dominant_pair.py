"""Two exact branches at the former static 7/8 obstruction, now T=17/20."""
from p644_strategy import Script,Aff,mass,contains,cellin,both,notin,inpick
from p644_strategy_lp import solve
from p644_strategy_budget import check_budget
from pathlib import Path
import json


def script(branch):
    X=contains(1,2);Y=contains(1,3);Z=contains(2,3)
    A=contains(2,4);B=contains(3,4);C=contains(1,4)
    hs=[(mass(X),500,500,(1,2)),(mass(Y),100,100,(1,3)),(mass(Z),100,100,(2,3)),
        (mass(contains(1,2,3)),0,0,(1,2,3))]
    steps={4:{'picks':[('PG',cellin((1,2,3),3),100)],'avoid':[X,Y,Z,'PG']}}
    if branch==1:
        hs.append((mass(B),0,350,(1,2,3,4)))
        steps.update({5:{'avoid':[X,B]},6:{'avoid':[Y,A]},7:{'avoid':[Z,C]}})
    else:
        hs.append((mass(B),351,1000,(1,2,3,4)))
        steps.update({5:{'picks':[('B1',B,350)],'avoid':[X,'B1']},
          6:{'avoid':[X,both(B,notin('B1'))]},7:{'avoid':[Y,Z,A,C]}})
    return Script(7,1000,850,steps,False,hs)

if __name__=='__main__':
    out=[]
    for branch in [1,2]:
        s=script(branch);q=solve(s,want=True);b=check_budget(s,want=True)
        print('branch',branch,q['status'],b['status'],flush=True)
        assert q['status']=='PROVER WINS' and b['status']=='LEGAL'
        out.append({'branch':branch,'support':q,'budget':b})
    Path('logs/astra_dominant_pair.json').write_text(json.dumps(out,indent=1))
