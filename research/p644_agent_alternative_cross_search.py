"""Exact finite cross-(5,1) discovery; numerical limits are not certificates."""
import argparse,itertools,json,time
from pathlib import Path
from pysat.solvers import Cadical153
from pysat.card import CardEnc,EncType

def run(k,t,seconds):
 n=2*k; start=time.time(); edges=[sum(1<<i for i in c) for c in itertools.combinations(range(n),k)]
 clauses=[]
 for c in itertools.combinations(range(n),t-1):
  d=sum(1<<i for i in c); clauses.append([j+1 for j,e in enumerate(edges) if not e&d])
 A=(1<<k)-1;B=A<<k
 clauses.extend([[edges.index(A)+1],[edges.index(B)+1]])
 pairs=[(1<<a)|(1<<b) for a in range(k) for b in range(k,2*k)]
 status='LIMIT'; cuts=[]; chosen=[]
 with Cadical153(bootstrap_with=clauses) as out:
  while time.time()-start<seconds:
   if not out.solve(): status='UNSAT_UNCERTIFIED';break
   chosen=[v-1 for v in out.get_model() if 0<v<=len(edges)]
   card=CardEnc.atmost(list(range(1,len(chosen)+1)),5,encoding=EncType.seqcounter)
   ins=[[j+1 for j,e in enumerate(chosen) if not edges[e]&p] for p in pairs]
   with Cadical153(bootstrap_with=ins+card.clauses) as sub:
    if not sub.solve():status='EXACT_SAT';break
    bad=[chosen[v-1] for v in sub.get_model() if 0<v<=len(chosen)]
   out.add_clause([-j-1 for j in bad]);cuts.append(bad)
   if len(cuts)%1000==0: print('cuts',len(cuts),'selected',len(chosen),'seconds',round(time.time()-start,2),flush=True)
 result={'rank':k,'transversal_lower':t,'status':status,'elapsed':time.time()-start,'cuts':len(cuts),'family':[[i for i in range(n) if edges[j]>>i&1] for j in chosen]}
 root=Path('logs/astra_agent_alternative');root.mkdir(exist_ok=True);(root/('cross_%s_%s.json'%(k,t))).write_text(json.dumps(result,indent=2))
 print(json.dumps({a:b for a,b in result.items() if a!='family'}),flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('k',type=int);p.add_argument('t',type=int);p.add_argument('--seconds',type=float,default=60);a=p.parse_args();run(a.k,a.t,a.seconds)
