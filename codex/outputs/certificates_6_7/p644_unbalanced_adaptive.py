"""Integer witness for Lemma 7.23: r=270, (x,y,z)=(105,100,5), T=234."""
from p644_strategy import Script,Aff,mass,contains,cellin,both,notin,inpick
from p644_strategy_lp import solve
from p644_strategy_budget import check_budget
from pathlib import Path
import json


def script():
    base=(1,2,3);X=contains(1,2);Y=contains(1,3);Z=contains(2,3)
    A=contains(2,4);B=contains(3,4);H=contains(1,4)
    steps={
        4:{'picks':[('PF',cellin(base,2),7),('PG',cellin(base,3),17)],'avoid':[X,Y,Z,'PF','PG']},
        5:{'picks':[('B1',B,124),('H1',H,Aff(124)-mass(inpick('B1')))],'avoid':[Z,X,'B1','H1']},
        6:{'picks':[('A2',A,129),('H2',both(H,notin('H1')),Aff(129)-mass(inpick('A2')))],'avoid':[Z,Y,'A2','H2']},
        7:{'avoid':[Z,X,Y,both(A,notin('A2')),both(B,notin('B1')),both(both(H,notin('H1')),notin('H2'))]}}
    hs=[(mass(X),105,105,(1,2)),(mass(Y),100,100,(1,3)),(mass(Z),5,5,(2,3)),
        (mass(contains(1,2,3)),0,0,(1,2,3))]
    return Script(7,270,234,steps,False,hs)


if __name__=='__main__':
    s=script();q=solve(s,want=True);print('SOLVE',q['status'],flush=True)
    b=check_budget(s,want=True);print('BUDGET',b['status'],flush=True)
    assert q['status']=='PROVER WINS' and b['status']=='LEGAL'
    Path('logs/astra_unbalanced_adaptive.json').write_text(json.dumps({'solve':q,'budget':b},indent=1))
