from proof_closed2 import *
import itertools
def chain_ok(cons,chain):
    cons=list(cons)
    for (k,s,t) in chain[:-1]:
        fl=[(nm,f) for nm,f in facets(k,s,t) if not implies([c for _,c in cons],f)]
        if len(fl)!=1: return False
        cons.append(('NOT '+fl[0][0],neg(fl[0][1])))
    k,s,t=chain[-1]
    return all(implies([c for _,c in cons],f) for nm,f in facets(k,s,t))
ch=[(9,A,B),(9,B,A),(39,A,B)]
for l0 in (False,True):
  for c1 in (False,True):
    D=domain(l0,c1)
    # greedy removal of hypotheses
    cur=list(D)
    for h in list(D):
        trial=[c for c in cur if c[0]!=h[0]]
        if chain_ok(trial,ch): cur=trial
    print(l0,c1,'minimal hyps:',[n for n,_ in cur])
print('--- clean lemma test')
H=[('a>=0',lin({A:1})),('b<=1',lin({B:-1},1)),('b>=a',lin({B:1,A:-1})),
   ('H1: 7(1-a)-4y>0',lin({A:-7,Y:-4},7)),('H2: 7b-4x>0',lin({B:7,X:-4})),('G: N-7/4-(b-a)>0',lin({X:1,Y:1,B:-1,A:1},-F(7,4)))]
print('chain ok with clean hyps:',chain_ok(H,ch))
cons=list(H)
for (k,s,t) in ch[:-1]:
    for nm,f in facets(k,s,t):
        r=implies([c for _,c in cons],f)
        print('  ',nm,'<=', r and (' + '.join(f'{l}*[{cons[i][0]}]' for i,l in r[0].items())+f' + {r[1]}'))
    fl=[(nm,f) for nm,f in facets(k,s,t) if not implies([c for _,c in cons],f)]
    cons.append(('NOT '+fl[0][0],neg(fl[0][1])))
for nm,f in facets(*ch[-1]):
    r=implies([c for _,c in cons],f)
    print('  FINAL',nm,'<=', r and (' + '.join(f'{l}*[{cons[i][0]}]' for i,l in r[0].items())+f' + {r[1]}'))
