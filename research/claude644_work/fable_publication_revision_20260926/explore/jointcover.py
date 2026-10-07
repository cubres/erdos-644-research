import itertools, pickle
from multiprocessing import Pool
from mincover import closers, points
def stage_sets(stage):
    return [c for c in (closers(*p,stage) for p in points(stage,20)) ]
if __name__=='__main__':
    stages=['s1','s2','s3','fin']
    with Pool(4) as pool: data=dict(zip(stages,pool.map(stage_sets,stages)))
    names=sorted(set().union(*[set().union(*v) for v in data.values()]))
    print(names)
    for r in range(3,len(names)+1):
        sols=[]
        for sub in itertools.combinations(names,r):
            s=set(sub)
            if all(all(c & s for c in data[st]) for st in stages): sols.append(sub)
        if sols:
            print('joint min size',r); [print(' ',x) for x in sols]; break
