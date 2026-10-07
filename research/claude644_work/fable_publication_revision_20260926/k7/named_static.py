from explore import *
from game import static_solution
def named_solution(names, cells):
    st=(len(names), tuple(sorted(cells.items())))
    sol=static_solution(st)
    if sol is None: return None
    out=[]
    for req in sol:
        out.append(' '.join(''.join(names[i] for i in range(len(names)) if m>>i&1)+':'+str(k) for m,k in req))
    return out
if __name__=='__main__':
    import sys
    names=['A','B','C']; cells={0b011:4,0b101:1,0b110:1,0b001:2,0b010:2,0b100:5}
    for reqs in sys.argv[1:]:
        req=parse_req(names,reqs)
        print('=== request',req)
        out=responses(names,cells,req,'D',maxdrop=0,quiet=True)
        for h,n2,c2,v in out:
            print('  response',fmt_h(names,h),' state',show(n2,c2))
            print('     cover:',named_solution(n2,c2))
