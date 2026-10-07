"""Integer witness for Lemma 7.20: r=100, (x,y,z)=(38,38,2), T=87."""
from p644_strategy import Script,Aff,mass,contains,cellin,both,notin,inpick
from p644_strategy_lp import solve
from p644_strategy_budget import check_budget
from pathlib import Path
import json


def script():
    base=(1,2,3);X=contains(1,2);Y=contains(1,3);Z=contains(2,3)
    A=contains(2,4);B=contains(3,4);H=contains(1,4)
    steps={
        4:{'picks':[('PF',cellin(base,2),4),('PG',cellin(base,3),5)],'avoid':[X,Y,Z,'PF','PG']},
        5:{'picks':[('B1',B,47),('H1',H,Aff(47)-mass(inpick('B1')))],'avoid':[Z,X,'B1','H1']},
        6:{'picks':[('A2',A,47),('H2',both(H,notin('H1')),Aff(47)-mass(inpick('A2')))],'avoid':[Z,Y,'A2','H2']},
        7:{'avoid':[Z,X,Y,both(A,notin('A2')),both(B,notin('B1')),both(both(H,notin('H1')),notin('H2'))]}}
    hs=[(mass(X),38,38,(1,2)),(mass(Y),38,38,(1,3)),(mass(Z),2,2,(2,3)),
        (mass(contains(1,2,3)),0,0,(1,2,3))]
    return Script(7,100,87,steps,False,hs)


if __name__=='__main__':
    s=script();q=solve(s,want=True);print('SOLVE',q['status'],flush=True)
    b=check_budget(s,want=True);print('BUDGET',b['status'],flush=True)
    assert q['status']=='PROVER WINS' and b['status']=='LEGAL'
    Path('logs/astra_early_adaptive.json').write_text(json.dumps({'solve':q,'budget':b},indent=1))
