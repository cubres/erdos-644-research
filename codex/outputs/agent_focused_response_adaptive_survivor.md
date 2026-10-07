# Exact survivor for the focused adaptive branch

For every even integer `b>=2`, the prescribed focused first response and
adaptive second request admit an actual second response of rank `146b`.
The resulting eight-row family has property `(7,2)` and the exact global
six-row minimum `(p,Q)=(111b,3669b^2)`. Both requests have size `109.5b`.
No point outside the original `259b`-point union is needed.

**Scope:** this finite family has transversal number **two**, not high
transversal number. It certifies compatibility of this particular request
branch with the stated finite constraints. It neither disproves the desired
upper bound nor excludes another adaptive request or a global argument.

## Construction

Use the same Fano cell names as the earlier heavier-clean-profile report.
For every Fano line `L` on `{0,...,6}` not containing `0`, the class `A_L`
has size `37b`; for each line containing `0`, `B_L` has size `33b` and each
`d_Lh` has size `b`. A point belongs to original row `Wr` if its omitted
set (`L`, or `L union {h}`) does not contain `r`.

Let `P` be the union of the three B classes and twelve defect classes,
and `A` the union of the four A classes. Choose `S` to contain the whole
class `d0564` and half of `d0563`, so `|S|=1.5b`. Choose `R` of size
`3.5b` inside `A245`. The prescribed first request and response are

```
D1 = P minus S,
G  = (A minus R) union S.
```

Project onto the five rows `[W3,W4,W5,W6,G]`, first row corresponding to
the low bit, and let `D2` be the union of cells with projected masks
`{9,11,13,15,18,22,25}`. This is exactly the request in the numerical
discovery file; the checker independently reconstructs it from the cells.
Its size is `109.5b`.

Choose `T subset B034` of size `3.5b`. The whole class `B034` is disjoint
from `D2` (its projected mask is `12`). The second response is simply

```
H = V minus (D2 union T).
```

Consequently `|H|=259b-109.5b-3.5b=146b`. A point of `B012` and a point
of `d0564` meet all eight rows. No point meets all eight, so the finite
family has transversal number exactly two.

## Exact certificate [C]

Run from the task directory:

```
python3 -S work/p644_focused_response_adaptive_check.py
```

The standard-library checker uses `Fraction` cell masses and integer
incidence masks. It verifies all eight ranks, both request budgets and
avoidances, all 28 six-row potentials, all eight seven-row conditions,
and an explicit two-point cover of the entire family. Every six-row
subfamily other than the original witnesses has endpoint count at least
`112.5b`; hence the original six rows uniquely attain `p=111b`, and have
exactly `3669b^2` piercing pairs. Smaller subfamilies have at least as many
endpoints and pairs as any containing six-row subfamily. There is no
numerical solver or minimum positive-cell cutoff in the checker.

Certificate: `outputs/agent_focused_response_adaptive_certificate.json`.

This finishes the requested bounded branch. The discovery program's
reported optimum is not used as a proof of optimality or impossibility.
