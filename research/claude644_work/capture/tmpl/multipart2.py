# smarter search: branch only on possible failures, report tree
import sys
exec(open('multipart.py').read().split("leaves=0; nodes=0")[0])
leaves=0
def feasible(states,fails): return build(states,fails)
def tree(states,fails,order,depth=0):
    global leaves
    ind='  '*depth
    if not feasible(states,fails): leaves+=1; return True
    if depth>=len(order): print(ind,'OPEN',states,fails); return False
    name=order[depth]
    br=[]
    for i in range(len(states)+1):
        for s in (STATES if i==len(states) else [None]):
            st=states+[s] if s else states
            for (u,v) in TEMPL[name]:
                if feasible(st,fails+[(i,u,v)]): br.append((i,s,u,v,st))
    print(ind,f'{name} can fail at:',[(i,s,(u,v)) for i,s,u,v,_ in br], 'states',states)
    ok=True
    for i,s,u,v,st in br:
        ok&=tree(st,fails+[(i,u,v)],order,depth+1)
    return ok
order=sys.argv[1].split(',')
ok=tree([],[],order)
print('OK' if ok else 'FAIL','branches',leaves)
