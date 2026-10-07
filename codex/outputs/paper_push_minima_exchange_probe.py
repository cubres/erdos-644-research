"""Discovery only: test three minima against Fano, V4, and one-cut EX.

A survivor is numerical until independently rationalized. Infeasibility is
also only numerical and is not a mathematical certificate.
"""
import sys, itertools as it, json
sys.path[:0]=[
'/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/bal3',
'/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/heavy']
from advlazy import Adv, roles_from, lin
from heavylib import reps, PENCIL

class Probe(Adv):
    def keys(self):
        return ([('F',)+r for r in reps(3)]
                +[('V4',)+r for r in it.product(range(3),repeat=4)]
                +[('EX',a,b,i,j,k) for a,b in it.combinations(range(3),2)
                  for i,j,k in it.permutations(range(3))])
    def forms(self,key):
        x,T=self.x,self.T;out=[]
        if key[0]=='F':
            rows=key[1:]
            for i in range(3):
                out.append((lin(*[(1,T[a][i]) for a in rows],(-4,x[i])),0))
                for pp in PENCIL:
                    out.append((lin(*[(1,T[rows[l]][i]) for l in pp],(-2,x[i])),0))
        elif key[0]=='V4':
            d,a,b,c=key[1:]
            for i in range(3):
                out += [(lin((1,T[a][i]),(1,T[b][i]),(1,T[c][i]),(-2,x[i])),0),
                        (lin((2,T[d][i]),(1,T[b][i]),(1,T[c][i]),(-2,x[i])),0),
                        (lin((4,T[d][i]),(1,T[a][i]),(1,T[b][i]),(1,T[c][i]),(-4,x[i])),0)]
        elif key[0]=='EX':
            a,b,i,j,k=key[1:]
            for aa,bb in ((a,b),(b,a)):
                out += [(lin((2,T[aa][i]),(1,T[bb][i]),(-1,x[i])),.75),
                        (lin((5,T[aa][i]),(1,T[bb][i]),(-3,x[i])),.75)]
            for aa,bb,cc in ((a,b,k),(b,a,j)):
                out += [(lin((2,T[aa][cc]),(1,T[bb][cc]),(-1,x[cc])),0),
                        (lin((5,T[aa][cc]),(1,T[bb][cc]),(-3,x[cc])),0)]
            for ka,ca in ((2,2),(4,5)):
                for kb,cb in ((2,2),(4,5)):
                    out.append((lin((ca,T[a][j]),(1,T[b][j]),(-ka,x[j]),
                                    (cb,T[b][k]),(1,T[a][k]),(-kb,x[k])),-1))
        return out

if __name__=='__main__':
    p=Probe(roles_from('min'),eta=.001,eta2=.00001,tmpl=(),xmin=.75)
    st,data=p.run(maxit=80,tl=30,verbose=True)
    print(st,json.dumps(data),flush=True)
    if data:
        with open('outputs/paper_push_minima_exchange_survivor.json','w') as f:json.dump(data,f,indent=2)
