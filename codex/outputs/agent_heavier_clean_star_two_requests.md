# Heavier clean-star profile: one bounded two-request test

## Scope and outcome

This tests the new exact symmetric profile with three eligible base classes of
size `a`, twelve eligible one-incidence-defect classes of size `b`, and four
clean noneligible Fano classes of size `c=a+4b`. Its six witness rows have rank
`k=4a+14b` and endpoint mass `p=3a+12b`.

For `a=33b`, the requested target is `3k/4=109.5b`, whereas `p=111b`.
The generic two-request search on the empty-common four-row core
`[W2,W4,W5,W6]` did not attain the target. Both strict and weak endpoint
targets returned minimum maximum-request cost `111b` numerically. The exact
allocation below attains that cost and leaves only `110b` endpoints. It gives
no improvement over the already available endpoint transversal of size `p`.

There is **no exact proof here that all two-request allocations cost at least
111b**. In particular the numerical dual bound is not promoted to an exact
infeasibility certificate for budget `109.5b`. No other four-row core or
parameter grid was searched in this task.

## Exact graph and feasible allocation [C]

The four-row incidence masks and masses, with least-significant bit belonging
to `W2`, are:

| Mask | Mass | D1-only | D2-only | Both | Neither |
|---:|---:|---:|---:|---:|---:|
|1|b|0|0|0|b|
|2|b|0|0|0|b|
|3|a+2b|0|0|0|a+2b|
|5|c+b|0|c+b|0|0|
|6|c+b|c|b|0|0|
|8|c|0|0|0|c|
|9|b|b|0|0|0|
|10|b|0|b|0|0|
|11|c|0|0|c|0|
|12|2b|2b|0|0|0|
|13|a+b|a+b|0|0|0|
|14|a+b|0|a+b|0|0|

All other positive four-row masks are absent. Mask 8 is isolated and can be
left out of both requests. The four rows have empty common intersection, so
points outside their union cannot be endpoints of a pair piercing them.

Each request has size `a+2c+4b`. For two points with old masks `s,t` and
request categories `q,r`, a pair can survive two actual responses avoiding
the requests only if `s|t=15` and `q&r=0`. Inspecting these exact conditions
in the table gives residual endpoint parts

`(1,neither), (2,neither), (3,neither), (6,D2-only), (9,D1-only),`
`(10,D2-only), (12,D1-only), (13,D1-only), (14,D2-only)`.

Their total mass is `3a+11b`, strictly below `p=3a+12b`. Thus the two-request
lemma gives `tau <= a+2c+4b`; at `c=a+4b` this is exactly `tau<=p`, not the
desired `tau<=3k/4+O(1)`. At `a=3300,b=100,c=3700`, both requests cost
11100 and the residual endpoint count is 11000; the desired budget is 10950.

The checker derives the four-row masses and each six-row rank from the Fano
construction, verifies the original endpoint mass, verifies every symbolic
part, and recomputes the entire residual endpoint support by integer masks.
It uses no floating point and no positive-cell cutoff:

```sh
python3 -S work/p644_heavier_clean_star_allocation_check.py
```

Output: `outputs/agent_heavier_clean_star_allocation_certificate.json`.

## Numerical discovery only

The MILP allows arbitrary continuous partial masses in all four request
categories. A support binary is only an upper gate `x<=w*z`; no constraint
imposes a minimum positive cell mass. False positive supports can only add
endpoints, so they cannot make a feasible discovery witness unsound. Isolated
mask 8 can be omitted without affecting an optimal request.

```sh
python3 work/p644_heavier_clean_star_two_requests.py --requests 2 --endpoint 110.99 --time 20
python3 work/p644_heavier_clean_star_two_requests.py --requests 2 --endpoint 111 --time 20
```

Both runs reported optimum and numerical dual bound 111. The first threshold
means 11099 endpoints when `b=100`; the second permits endpoint equality
11100, which could in principle be useful with the pair-count tie criterion.
Neither discovers any allocation below 11100, so neither discovers a
target-scale tie opportunity. These statements describe the solver runs,
not an exact exclusion theorem.

The separate fixed-table obstruction from `critical_literature` is narrower:
the old allocation starts at request costs `108b,110b` and residual `113b`.
At budget `110b` its available overlap removes only `b` endpoints; at budget
`111b` it can reach residual `111b` but not strict improvement. The present
new allocation reaches residual `110b` at budget `111b`, so the fixed-table
obstruction must not be mistaken for a lower bound for arbitrary allocations.
