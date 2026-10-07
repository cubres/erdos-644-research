import heavylib as h, collections
insts = [([0.82,0.714,1.112], [[.503,.487,.01],[.507,0,.493],[.139,.169,.691],[.003,.506,.492]]),
 ([1.072,.555,.774], [[0.414, 0.128, 0.458], [0.714, 0.129, 0.156], [0.64, 0.0, 0.36], [0.268, 0.185, 0.547], [0.546, 0.439, 0.015], [0.625, 0.375, 0.0]])]
for x, T in insts:
    print("x", x, "tau*", round(h.tau_star(x, T),4), "heavy", [[i for i in range(3) if 7*a[i] > 4*x[i]] for a in T])
    F = h.all_fano(x, T)
    cnt = collections.Counter(tuple(sorted(collections.Counter(a).values(), reverse=True)) for a in F)
    print(" #fano reps", len(F), cnt)
    # pattern: multiset of types
    c2 = collections.Counter(tuple(sorted(collections.Counter(a).items())) for a in F)
    for k, v in sorted(c2.items(), key=lambda kv: -kv[1])[:15]: print("   ", k, v)
