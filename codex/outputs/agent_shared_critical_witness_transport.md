# A shared critical six-row witness compatible with the old rows

**Status: [C], exact finite positive construction at `b=100`.** The construction stays inside the existing ground set `V` of 26,000 points. It preserves all original point memberships, keeps the distinguished one-point cells intact, and realizes one shared critical witness for every clone. It is not a high-transversal example: the entire enlarged family has transversal number three. No asymptotic scaling or global incidence-minimality assertion is made.

## 1. Result

Start with the nine-row family from `outputs/agent_near_fano_outside_control_certificate.json`, at `b=100`. Retain the Section7.153 notation

`D3=I union {cells1,7,11,12,13}`,

`J0=V\(D3 union R)`, `|J0|=14,400`,

`Q=J0\{z}`, `|Q|=14,399`, `|R|=800`,

where `z` is one ordinary point of base class012, distinct from the restored point `x`.

There are six actual new rows `W1,...,W6`, each of size 14,400, with the following properties.

- Their piercing-graph endpoint set `P_W` has exactly 11,100 points, contains all 800 points of `R`, and is disjoint from `Q`.
- Their pair count is exactly 36,690,000, equal to the previous global minimum at endpoint count 11,100.
- The formal tuple `Q,W1,...,W6` is a **minimal bad seven-tuple**: no pair meets it, but every proper subfamily is two-pierceable.
- The old nine rows, these six new rows, and **all 800** actual clone rows `Q union {r}`, `r in R`, coexist with property(7,2). This is an actual 815-row finite family.
- Every six-row subfamily of that family has lexicographic endpoint/pair potential at least `(11100,36690000)`. Equality is attained only by the original six-row tuple `F1,...,F6` and the new witness tuple `W1,...,W6`.
- The full actual family has transversal number exactly three.

Thus the private activating incidence of every clone can have the same genuine width-six witness, without contradicting the old-row compatibility tests or the global endpoint/pair minimum. This is stronger than an abstract scalar witness: the mixed old/new subfamilies are checked explicitly.

## 2. The witness pattern and its incidence budget

Use the usual Fano coordinates `0,...,6`; a line is a triple whose three indices plus one have xor zero. Its six-row complementary pattern records membership in coordinates `1,...,6`.

Place the 14,400 points of `J0` in the four noneligible Fano classes assigned to lines not containing zero, 3,600 points per class. Each point has witness degree three. Both `x` and `z` are placed as separate, unsplit one-point cells within the first such class. In particular `Q=J0\{z}` remains exactly 14,399 points, not 14,300 or a rounded proportional surrogate.

Place the 11,100 endpoint points in the three eligible classes assigned to lines through zero. Each class has 3,700 points, split into:

- a base class of 3,300 points of witness degree four;
- four classes of 100 points, each obtained by deleting one of the four available witness incidences, hence of witness degree three.

Every witness row receives 7,200 points from the noneligible side and initially 7,400 from the eligible side. Its two relevant defect classes remove 200 incidences, leaving exactly 14,400 points. This accounts explicitly for the 1,200 incidences missing from the pure degree-three/degree-four pattern.

All 800 points of `R` lie in one eligible base class. Its remaining 2,500 points come from `D3`; the other endpoint types also come from `D3`. A set of 500 points of base034 is left outside all six witness rows. Thus the ground partition is

`J0:14400`, `P_W:11100`, `unused:500`.

The endpoint pattern is the same three-base/twelve-defect pattern that had pair count `3669b^2`. The four noneligible classes cannot contribute an endpoint: the relevant complementary Fano lines always have a common nonzero coordinate. The selected endpoint classes remain eligible because the corresponding base partner classes are all nonempty.

## 3. Transport into the actual old ground set

The new witness assignments subdivide existing old membership classes; they do not change an old row or identify distinct old points. The transport is integral and keeps all designated singleton points unsplit.

For the `J0` side, the ordinary old classes are distributed into the four noneligible witness classes with the prescribed totals, after reserving one point each for `x` and `z`. For the endpoint side, all points of `R` are assigned to one base witness type. The remaining endpoint mass comes from `D3`, with the 500 unused points removed from old base034. Each remaining eligible old class is distributed among the fifteen endpoint witness types.

The discovery script first puts one point in every permitted ordinary old-class/new-type cell. It then fills an integral proportional allocation and balances the remaining row and column sums exactly. Consequently the construction uses no small-positive-mass cutoff: its entries are actual positive integers. The exact subdivision is stored in the `cells` array of

`outputs/agent_shared_witness_transport_discovery.json`.

Each entry gives its point cardinality, original nine-row membership mask, new six-row membership mask, membership in `Q`, old source class, and role. The checker independently sums these cells back to each original point class and each witness row.

## 4. Exact verification

From the task directory, run

```
python3 -S work/p644_shared_witness_transport_check.py
```

The checker uses only Python's standard library and integer arithmetic. It does not call the discovery algorithm, an optimizer, or NumPy. It writes

`outputs/agent_shared_witness_transport_certificate.json`.

The following are checked directly:

1. Every old source class has its original integer cardinality and nine-row memberships; `x,z` remain separate singleton cells.
2. The ground size is 26,000, the common clone core has size 14,399, and every old/new actual row has the prescribed rank.
3. The new witness endpoint set is exactly the specified 11,100-point set, contains all of `R`, avoids `Q`, and has pair count 36,690,000.
4. `Q` and all six witness rows form a bad seven-tuple; deleting any one of its seven rows yields a piercing pair.
5. Every actual six-row and seven-row subfamily passes the required test, with all 800 clone rows present simultaneously.
6. A concrete three-point transversal of the full 815-row family exists, and even the old nine rows plus one clone have no two-point transversal.

For step5, all `R` points have identical memberships in the fifteen nonclone rows. A subfamily containing `q` distinct clones therefore consists of `q` individually represented activating points and an unselected reservoir of size `800-q`. This reduces the complete verification to **9,949 six-row cases** and **16,384 seven-row cases**, for `0<=q<=7`. The unselected reservoir and each selected one-point activator remain positive. Smaller subfamilies and repeated rows follow by extension and monotonicity.

The checker obtains the following least endpoint counts by number of selected clones:

| Selected clones | Least endpoint count among six-row cases |
|---:|---:|
|0|11,100|
|1|14,201|
|2|17,800|
|3|21,700|
|4|21,700|
|5|26,000|
|6|26,000|

Only the two stated six-tuples reach 11,100 endpoints, and both have the required pair count.

For the full-family three-point cover, the checker selects transport cells0,5,10. Their old nine-row masks are `248,158,341`, their six-row witness masks are `42,22,25`, and all three lie in `Q`. Their old masks cover all nine old rows, their witness masks cover all six new rows, and each lies in every clone. These are three actual distinct points in positive cells.

The optional regeneration command is

```
python3 work/p644_shared_witness_transport_discover.py
```

This deterministic script uses NumPy integer arrays to construct and initially test the same integral transport. Its output is subsequently checked by the separate standard-library program.

## 5. What this establishes and what remains open

The construction realizes simultaneous singleton-incidence criticality for all clone rows: deleting the private point `r` from `Q union {r}` produces `Q`, and the same six actual witness rows certify the resulting failure of property(7,2). All witness rows are compatible with the original nine rows and every clone. Therefore these shared-witness obligations alone cannot eliminate the current finite configuration.

The family has `tau=3`. It does not realize a global high-transversal avoidance oracle, minimum vertex count at a hypothetical large transversal number, global minimum total incidence, or criticality of every other incidence. No claim is made that the construction automatically scales while retaining singleton sizes, or that additional critical witnesses for the remaining incidences are compatible. Those are separate obligations.
