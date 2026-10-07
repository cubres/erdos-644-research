# Same as referee_w5_paper_e2e.py but samples case (c) (y > 73r/200) and b1/b2/b3 boundaries heavily.
exec(open('referee_w5_paper_e2e.py').read().split('stats={};fails=0')[0])
stats={};fails=0
for it in range(4000):
    r=random.choice(range(60,121)); T=ceil(b*r+3)
    ylo=floor(Fr(73,200)*r)+1
    if it%2==0:
        y=random.randint(ylo, floor(Fr(227,600)*r)); mhi=min(floor(Fr(23,50)*r), floor((Fr(227,200)*r-2*y)))
        if mhi<y: continue
        m=random.randint(y,mhi); z=random.randint(0,y)
    else:
        m=random.randint(floor(Fr(119,400)*r)+1,floor(Fr(23,50)*r)); y=random.randint(0,min(m,floor(Fr(73,200)*r))); z=random.randint(0,y)
        if 200*(m+2*y)>227*r: continue
    nm,ed,reqs,Bud=run_case(r,T,m,y,z)
    if ed is None: fails+=1; print('CONSTRUCT FAIL',nm,reqs,r,m,y,z); continue
    msg=check(ed,reqs,Bud)
    if msg is None and it%20==0:
        fam=ed+[respond(r,R,list(set().union(*ed))) for R in reqs]
        if len(fam)>7 or not no2transversal(fam): msg='NOT BAD'
    stats[nm]=stats.get(nm,0)+1
    if msg: fails+=1; print('FAIL',nm,msg,r,T,m,y,z)
print(stats,'fails',fails)
