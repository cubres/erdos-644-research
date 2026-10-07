import sys
from explore import *
names=['A','B','C']; cells={0b011:4,0b101:1,0b110:1,0b001:2,0b010:2,0b100:5}
for reqs in sys.argv[1:]:
    req=parse_req(names,reqs)
    for md in (0,1):
        print('=== request',req,'maxdrop',md)
        out=responses(names,cells,req,'D',maxdrop=md,quiet=False)
