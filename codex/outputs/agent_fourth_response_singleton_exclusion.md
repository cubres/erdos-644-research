# Fourth-response singleton exclusion: exact repairs and a reservoir obstruction

Status: **[C] exact local extension results, plus the hand trimming lemma below.** No high-transversal counterexample or general upper bound is claimed. All starting data come from the singleton-repaired ten-row family in Section7.153, with rank `k=144b+1`, global six-row endpoint/pair minimum `(111b,3669b^2)`, and integer `b>=1`.

The work used genuine fourth avoidance requests, containing the activating singleton and an actual minimum transversal. The requests preserve the `108b` budget. Responses satisfy all the new seven-row conditions and all six-row endpoint comparisons. No positive-cell cutoff was imposed; the activating cells have their exact one-point sizes.

## 1. Setup and actual minimum covers

Read `outputs/root_third_request_singleton_repair_certificate.json`. The old nine-row family has `V=U union Y`, `|V|=260b`. Put

`I=G intersect H`, `|I|=71b`, and let `R` be the original `8b` subset of base class245.

The Section7.153 request and failed response were

`D3=I union X`, `X={1,7,11,12,13}`, `|D3|=108b`,

`J0=V\(D3 union R)`, `|J0|=144b`.

For an ordinary point `z` of base012 and an activating `r in R`, the repaired response is `J=(J0\{z}) union {r}`. Write `Q=J0\{z}`, so `|Q|=144b-1`.

The actual ten-row completion has transversal number three. There is no piercing pair; examples of three-point covers are:

- one point from base034, one point from defect cell9, and `r`;
- ordinary points from base012, base034, and base135.

The second cover avoids reliance on `r`; its base012 and base135 points lie in the large common part `Q`. These statements are checked directly from the ten actual membership masks in the scripts below.

## 2. A whole reservoir of singleton repairs coexists

**Reservoir theorem [C].** The old nine-row family can be enlarged by **all** `8b` distinct rows

`J_s=Q union {s}`, for every `s in R`,

while retaining property(7,2) and the same global six-row endpoint/pair minimum `(111b,3669b^2)`. This holds for every integer `b>=1`. The enlarged finite family still has transversal number three.

This is a statement about an unbounded number of actual response rows, not a list of individual examples. The proof reduces by symmetry to a subfamily containing `q` selected clone rows, where `q<=6` for endpoint comparisons and `q<=7` for piercing. The selected activators are separate singleton cells; the remaining reservoir has mass `8b-q>0`. All unselected clone incidences disappear on projecting to the selected subfamily, so that remaining reservoir is one homogeneous cell. The checker covers all 382 new six-row symmetry cases and all 466 new seven-row cases. Every inequality is exact and valid for all `b>=1`.

Run:

```
python3 -S work/p644_fourth_response_clone_reservoir_check.py
```

Output: `outputs/agent_fourth_response_clone_reservoir_certificate.json`.

**Consequence.** Any request `D` disjoint from `Q` and not containing all of `R` has an available response `J_s` with `s notin D`. This remains true after arbitrarily many other clone rows have already been included. Thus successively excluding the previously used activating singletons cannot exhaust this defence before the request excludes the entire `8b` reservoir. For example, `(D3 minus one ordinary point of cell4) union {r}` has size `108b`, contains `r` and a minimum cover of the ten-row family, but is avoided by every remaining clone.

The hypothesis `D intersect Q=empty` is essential. This theorem does not say arbitrary requests survive, nor does it claim the clone family has large transversal number or the global incidence-minimality properties of a hypothetical counterexample.

## 3. A request hitting the common part and a minimum cover also survives

Choose ordinary points `q0` from base012 and `q3` from base135, with `q0` distinct from `x,z`. Let `W` consist of any three points of base146, certificate cell4, which lies wholly in `D3`. Define

`D4=(D3\W) union {r,q0,q3}`.

Then `|D4|=108b`. It excludes the old activator, and contains the minimum cover `{q0, one point from base034, q3}`. Thus it hits two large common-core classes as well as the activating singleton.

Choose three fresh points `R' subseteq R\{r}` and put

`K=(J\{r,q0,q3}) union R'`.

The response has size `144b` and avoids `D4`. **[C]** For all integer `b>=1`, all 252 new six-row subfamilies have strictly more than `111b` endpoints and all 210 new seven-row subfamilies have a piercing pair. The least endpoint value is `142b+3`, reached by old five-tuples `(1,2,6,G,H)` and `(2,5,6,G,H)` followed by `K`.

Run:

```
python3 -S work/p644_fourth_response_mincover_check.py
```

Output: `outputs/agent_fourth_response_mincover_certificate.json`.

This demonstrates a finite-point exchange repair for the specific minimum-cover exclusion above. It is not a universal theorem for arbitrary deletions from `Q`.

## 4. Excluding the entire reservoir changes the response, but still admits one

To move beyond singleton substitution, take the four defect cells

`T={9,15,22,24} subseteq I`

and request

`D4=R union base034 union (I\T)`.

The costs are `8b+33b+(71b-4b)=108b`. This request contains all of `R`, hence the activating singleton, and contains the actual minimum cover represented by cells `{1,20,r}`.

Its complement in `V` has size `152b`. Remove any `8b` ordinary points of base012, leaving `25b-2` points in the same old membership cell, and call the resulting set `K`. Then `|K|=144b`, `K intersect D4=empty`, and `K` has **no R-point at all**.

**[C]** For every integer `b>=1`, all 252 new six-row subfamilies have strictly more than `111b` endpoints, and all 210 new seven-row subfamilies have a piercing pair. The smallest new endpoint count is `177b`, for old rows `(2,3,5,6,H)` followed by `K`.

Run:

```
python3 -S work/p644_fourth_response_full_R_check.py
```

Output: `outputs/agent_fourth_response_full_R_certificate.json`.

The unchanged old rows retain the original global six-row minimum and pair count. The new rows have strictly larger endpoint counts, so no separate lower bound on their pair counts is being assumed.

## 5. Why rank trimming need not remove the useful support

**Hand lemma.** Fix an old family `B`, a prospective new row `K0`, and a set `C subseteq K0` of points with identical memberships in every old row. Let `W` be a proper subset of `C`, and let `K=K0\W`. For every old subfamily `S`,

`P(S union {K}) contains P(S union {K0})\W`.

In particular its endpoint count falls by at most `|W|`. Also, every old piercing pair extendible to meet `K0` has a corresponding piercing pair meeting `K`.

**Proof.** Let `u notin W` be an endpoint of a piercing pair `{u,v}` for `S union {K0}`. If that pair already meets `K`, there is nothing to prove. Otherwise the endpoint meeting `K0` must be `v in W`, and `u notin K0`. Choose `v' in C\W`. The points `v,v'` have identical memberships in `S`, so `{u,v'}` meets `S`; it also meets `K`. They are distinct because `u notin K0` and `v' in K0`. Thus `u` remains an endpoint. The same replacement argument preserves existence of a piercing pair whenever the old pair used a deleted point to meet the new row. ∎

The fourth response in Section4 uses exactly this mechanism: the eight units needed to satisfy the rank bound are removed within a major cell while a large positive portion of that cell remains. A method that relies only on the total rank deficit cannot treat this as destruction of an available membership type.

## 6. Exact scope of the obstruction

The requested singleton exclusion, actual minimum-cover exclusion, and whole-reservoir exclusion have each been made concrete at budget `108b` and admit rigorously certified responses. The reservoir theorem explains a whole adaptive family of singleton substitutions rather than presenting repeated isolated repairs. The trimming lemma explains how the stronger whole-reservoir request reopens a different response shape.

These results do not establish that every possible fourth request survives. In particular, they do not realize the complete high-transversal avoidance oracle simultaneously for arbitrary sets. Further progress must couple more global obligations, or select a request that prevents both a replacement activator and a rank correction that preserves the useful old membership types. No global3/4 proof follows from the present branch.
