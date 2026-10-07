exec(open('xi1_lp.py').read().split("NQ=[S for S")[0])
for S in sorted(xi):
    print(S, str(xi[S]), 'opp in steps', [j for j in binding if arow[j][S]])
