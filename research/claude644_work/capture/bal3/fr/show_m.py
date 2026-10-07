import sys; sys.path.insert(0,'.')
exec(open('test_p1.py').read().split('for nm, (x, T)')[0])
for nm in ['7.79','m3s0a','m3s0b','fpgW5']:
    x, T = INST[nm]; x=[float(v) for v in x]; T=[[float(v) for v in t] for t in T]
    ts = b3lib.tau_star(x, T)
    (bm, basg) = p1_best(x, T, ts)
    v, m = fr_lp(x, T, basg, True)
    print(nm, 'x', np.round(x,3), 'tau*', round(ts,4), 'asg', basg, 'maxlight', round(v,4))
    for li in range(4): print('   line', LINES[li], 'type', np.round(T[basg[li]],3))
    names = ['p0','a','a2','b','b2','c','c2']  # points 0..6: line0=(0,1,2): p0,a,a' ; line1=(0,3,4) b ; line2=(0,5,6) c ; line3=(1,3,5) = q1 {a,b,c}
    for q in range(7): print('   pt', q, names[q], np.round(m[q],4))
    for li in range(4,7): print('   light', LINES[li], round(m[list(LINES[li])].sum(),4))
