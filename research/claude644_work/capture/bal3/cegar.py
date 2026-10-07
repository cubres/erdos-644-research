"""outer CEGAR: add escape roles for the cheapest blocking map of the adversary's role set."""
import sys, json, itertools, advlazy as AL, blockmap
spec, eta, rounds = sys.argv[1], float(sys.argv[2]), int(sys.argv[3]); xmin = float(sys.argv[4]) if len(sys.argv) > 4 else 0.0
roles = AL.roles_from(spec)
for rd in range(rounds):
    A = AL.Adv(roles, eta=eta, xmin=xmin)
    st, sol = A.run(verbose=False)
    print("round", rd, "roles", len(roles), st, flush=True)
    if sol is None: break
    x, T = sol['x'], sol['T']
    # cheapest blocking map over roles (require positive coordinate)
    tst, pi, u = blockmap.best_block(x, T)
    print("  tau", round(sol['tau'], 5), "tau*(roles)", round(tst, 5), "map", pi, flush=True)
    print("  x", [round(v, 4) for v in x], "T", [[round(v, 4) for v in t] for t in T], flush=True)
    if tst >= sol['tau'] - 1e-9:
        print("  GENUINE small counterexample to strategy menu", json.dumps(sol)); break
    roles.append({'kind': 'escape', 'map': {j: p for j, p in enumerate(pi)}})
