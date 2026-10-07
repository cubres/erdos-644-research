import sys, itertools
sys.argv=[sys.argv[0]]
exec(open('w7_ref_core1_partner.py').read().split("k=int(sys.argv[1])")[0])
k=4;t=3;n=12
quad=([0,1,2,3],[2,3,4,5],[6,7,8,9],[8,9,10,11])
E=[bm(q) for q in quad]
Ts=[T for T in itertools.combinations(range(n),3) if all(e&bm(T) for e in E)]
# symmetry: blocks swap, 0<->1,4<->5 etc.; just try canonical reps: T contains 2 (wlog, block-1 point in {2,3}) or T covers block1 with 2 pts
reps=[(2,8,x) for x in range(n) if x not in (2,8)]+[(0,4,8),(2,6,10)]
for T in reps:
    T=tuple(sorted(T))
    if not all(e&bm(T) for e in E): continue
    res,it=search(n,k,t,E,list(T))
    print('T',T,'iters',it,'FOUND' if res else 'none',flush=True)
    if res:
        tt=tau(res,n); print(' tau',tt,'|H|',len(res),[sorted(v for v in range(n) if e>>v&1) for e in res]); print(' bad?',find_bad(res,n)); break
