import sys, itertools
sys.argv=[sys.argv[0]]
exec(open('w7_ref_core1_partner.py').read().split("k=int(sys.argv[1])")[0])
k=4;t=3
for n in (10,11):
  for (E1,F1,E2,F2) in [([0,1,2],[2,3,4],[5,6,7],[7,8,9]), ([0,1,2,3],[2,3,4,5],[5,6,7],[7,8,9]) if n>=11 else None]:
    if E1 is None if False else False: pass
for n,quad in [(10,([0,1,2],[2,3,4],[5,6,7],[7,8,9])),(11,([0,1,2],[2,3,4],[5,6,7],[7,8,9])),(10,([0,1,2],[0,3,4],[5,6,7],[5,8,9]))]:
  E=[bm(q) for q in quad]
  B1=set(quad[0])|set(quad[1]); B2=set(quad[2])|set(quad[3])
  Ts=set()
  for T in itertools.combinations(range(n),3):
    m=bm(T)
    if all(e&m for e in E): Ts.add(T)
  found=None
  for T in sorted(Ts):
    res,it=search(n,k,t,E,list(T))
    if res: found=(T,res); break
  print('n',n,'quad',quad,'#T tried',len(Ts) if not found else 'stopped', 'FOUND' if found else 'none')
  if found:
    T,res=found; tt=tau(res,n)
    print(' T',T,'tau',tt,'|H|',len(res),[sorted(v for v in range(n) if e>>v&1) for e in res]); print(' bad?',find_bad(res,n))
