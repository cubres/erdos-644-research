# Referee: S1 continuous closed form vs INTEGER split existence (integrality gap examples)
exec(open('referee_w4_handbound_s1s2.py').read().split("import random")[0].split("n1=n2=0")[0])
exec("def s1closed"+open('referee_w4_handbound_s1s2.py').read().split("def s1closed")[1].split("import random")[0])
ex=[]
for r in range(1,40):
  for x in range(r+1):
    for y in range(r+1-x):
      for z in range(r+1-max(x,y)):
        if y+z>r: continue
        for T in range((r+1)//2,r+1):
          if s1closed(r,x,y,z,T):
            ok=any(x1+y1+z1<=T and y1+z1>=r+x-T and x1+z1>=r+y-T and x1+y1>=r+z-T
                   for x1 in range(x+1) for y1 in range(y+1) for z1 in range(z+1))
            if not ok: ex.append((r,x,y,z,T))
  if len(ex)>=5: break
print(len(ex),ex[:5])
