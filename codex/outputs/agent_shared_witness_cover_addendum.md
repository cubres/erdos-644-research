# A two-request closing lemma at the three-quarter scale

**Status: proved by the explicit hand argument below; independently checked symbolic cell arithmetic.** The lemma applies to an entire two-parameter shared-witness profile. In particular, it excludes the previously constructed actual shared witness from a high-transversal extension having the stated global endpoint minimum, despite that witness's compatibility with all the finite six-/seven-row tests.

## 1. The general theorem

Let `a>=0` and `b>=1` be integers. Suppose an actual family contains the clean noneligible Fano witness pattern:

- four noneligible classes of size `a+3b`, of witness degree three;
- three eligible base classes of size `a`, of witness degree four;
- twelve eligible one-incidence-defect classes of size `b`, four per eligible base class, of witness degree three.

Each of the six witness rows has size

`k0=4a+12b`.

Suppose every actual subfamily of at most six rows has at least

`p0=3a+12b`

piercing-graph endpoints. Then

`tau <= 3a+9b+1 = 3k0/4+1`.                       (1)

More precisely, for every integer `1<=e<=b`, two explicit requests each have size `3a+9b+e`, and any responding rows would produce a six-row graph with at most `3a+12b-2e` endpoints.

Only the actual four-row trace profile in the table below and the global endpoint lower bound are used in the proof. No equality between transversal number and endpoint number is assumed. The secondary pair minimum is not needed. Points outside the displayed witness ground set, and outside portions of the responding rows, are unrestricted.

A lower bound asserted for six distinct rows also applies to fewer rows by extension and monotonicity, since the family contains the six witness rows. Thus the two responses need not be distinct from previously selected rows.

## 2. The four-row profile

Retain witness rows `W2,W4,W5,W6`, in that order. A point's four-bit mask records its memberships in these rows. The exact nonzero trace classes are:

| Mask | Size |
|---|---:|
|0001|b|
|0010|b|
|0011|a+2b|
|0101|a+4b|
|0110|a+4b|
|1000|a+3b|
|1001|b|
|1010|b|
|1011|a+3b|
|1100|2b|
|1101|a+b|
|1110|a+b|

All other nonzero masks are absent. The zero class is arbitrary and irrelevant. In particular, there is no1111 class, so the four actual rows have empty common intersection.

These counts follow directly by projecting the specified Fano classes onto the retained four rows. The exact checker independently reconstructs them from the Fano lines and confirms all six witness row sizes `4a+12b`.

## 3. Explicit requests

Choose a set `Ue` of `e` points from class1001 and a set `Ve` of `e` points from class1100. Define

`D1 = classes{0001,0010,0011,1010,1100,1101,1110} union Ue`,

`D2 = classes{0110,1001,1011,1101} union Ve`.

Each whole-class total is `3a+9b`. Hence

`|D1|=|D2|=3a+9b+e`.                              (2)

Both choices are legal for `1<=e<=b`. Every point in `Ue` is already in the whole1001 class of `D2`; every point in `Ve` is already in the whole1100 class of `D1`. Thus those selected points belong to both requests.

## 4. Hand proof of the endpoint bound

Assume `tau>3a+9b+e`. There are actual rows `A1,A2` avoiding `D1,D2`, respectively. Consider their piercing graph together with the four retained witness rows.

Any piercing pair lies in the union of the four retained rows. Indeed, an endpoint outside all four would require its partner in their common intersection, which is empty. This rules out endpoints from all unseen outside points, without placing any restriction on the new rows themselves.

A remaining pair must satisfy both conditions:

1. its four-row masks have bitwise union1111;
2. it is not contained wholly in `D1` and is not contained wholly in `D2`.

The second condition is necessary because a pair wholly in `Di` misses `Ai`. The only possible endpoints are consequently:

- all of class0101: `a+4b`;
- class1001 outside `Ue`: `b-e`;
- all of class1010: `b`;
- all of class1011: `a+3b`;
- class1100 outside `Ve`: `2b-e`;
- all of class1110: `a+b`.

Here is the direct exclusion check. Class0001 can only pair with1110, and both lie in `D1`. Class0010 can only pair with1101, again both in `D1`. Class0011 can only pair with1100,1101,1110, all in `D1`. Class0110 can only pair with1001,1011,1101, all in `D2`. Every partner of1101 belongs to at least one of `D1,D2`, while1101 itself lies in both. A point of `Ue` can only pair with0110 or1110; these pairs are respectively inside `D2` or `D1`. A point of `Ve` can only pair with0011 or1011; these pairs are respectively inside `D1` or `D2`. Class1000 has no partner because no available mask contains all its three missing coordinates. The zero class has no partner because1111 is absent.

The endpoint count is therefore at most

`(a+4b)+(b-e)+b+(a+3b)+(2b-e)+(a+b)`

`=3a+12b-2e`.                                    (3)

This is strictly below the assumed global lower bound `p0=3a+12b`. Thus the two requests cannot both have an avoiding row. At least one is a global transversal. Setting `e=1` in(2) proves(1). ∎

## 5. Endpoint-deficit version

For the **same exact four-row profile**, suppose the global endpoint lower bound is only

`3a+12b-g`,

where `g` is an integer with `0<=g<2b`. Set `e=floor(g/2)+1`. Then `1<=e<=b`, and(3) is strictly below `3a+12b-g`. Therefore

`tau <= 3a+9b+floor(g/2)+1`.

This changes only the endpoint lower bound. It asserts no stability under changes to the four-row support: a formerly absent positive mask can activate a large endpoint set. In particular no general approximate-profile theorem is being asserted.

## 6. Concrete shared-witness specialization

The actual shared witness constructed in `agent_shared_critical_witness_transport.md` has `a=33b`. Then `k0=144b`, `p0=111b`, and the result is

`tau<=108b+1`.

For the ambient rank `k=144b+1` used in that construction,

`108b+1=ceil(3k/4)`.

At its certified finite scale `b=100`, the two requests have size10,801 and force a residual endpoint count at most11,098, below the global minimum11,100. The 815-row finite family is entirely consistent with this conclusion, because its transversal number is three. What fails is a high-transversal extension retaining both this witness profile and the endpoint minimum.

## 7. Exact checker and discovery

Run from the task directory:

```
python3 -S work/p644_shared_witness_two_request_check.py
```

Output: `outputs/agent_shared_witness_two_request_certificate.json`.

The checker uses standard-library integer tuple arithmetic with affine coefficients `(a,b,e)`. It verifies the exact class totals, both request costs `3a+9b+e`, the residual endpoint upper bound `3a+12b-2e`, nonnegative part sizes for `a>=0` and `0<=e<=b`, and witness row rank `4a+12b`. It also replays the actual `a=3300,b=100,e=1` transport and verifies the concrete residual endpoint count11,098. Arbitrary all-zero-class mass never enters a request or the endpoint computation.

The six single-neighborhood discovery runs for the concrete profile returned feasible covers of size `109b+1`, with five-row endpoint count `183b` and strict selection threshold `72b+1`. Those optimizer results are not used as lower certificates. The two-request discovery then supplied the allocation proved above. Discovery files are `work/p644_shared_witness_five_neighborhood.py`, `work/p644_shared_witness_two_requests.py`, and their output JSON files.

## 8. Scope of the progress

This is a target-scale closing lemma for the entire two-parameter clean-noneligible witness profile, including the new actual shared witness. The old difficult configuration has not been shown to force this profile. A shared critical witness may instead distribute its incidence deficits through the noneligible side or have another support. The lemma therefore does not settle the old hard case or the general Erdős644 upper bound.
