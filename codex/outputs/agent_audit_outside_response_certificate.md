# Independent verification of the new five-pair response exclusion

Status: **computer-assisted conditional lemma, independently checked with exact rational arithmetic**. This is a new response exclusion for one fixed finite state, not a general upper bound for Erdős 644. The earlier numerical value approximately .23906471317 is not asserted to be the global optimum and is not used in this proof.

## Exact finite state and conclusion

Five old disjoint pairs are represented by five bits. Label them by the original pair labels 1,2,3,4,6. Their union is a ground set U of size 2k, partitioned into the following ten incidence cells:

| Five-bit type | Cell size / k | Maximum permitted R trace / k |
| --- | ---: | ---: |
| 00001 | 1/4 | 1/4 |
| 00010 | 1/4 | 1/4 |
| 01100 | 1/4 | 1/8 |
| 01111 | 1/4 | 0 |
| 10011 | 6/25 | 1/8 |
| 11111 | 6/25 | 6/25 |
| 10100 | 1/4 | 0 |
| 10111 | 1/100 | 0 |
| 11000 | 1/4 | 1/4 |
| 11011 | 1/100 | 1/100 |

Each bit-half has size k. The first three old pairs have exactly (6/25)k² two-point transversals; each of the other nine choices of three of these five old pairs has exactly k²/4.

**Certified response statement.** Let R,H be disjoint sets of rank at most k. They may have arbitrary points outside U. Suppose the trace of R in each old cell is at most the third column of the table. Then, for at least one choice of two of the five old pairs, those two pairs together with R,H have fewer than

    (239999/1000000) k² < (6/25) k²

two-point transversals.

Consequently, suppose a family has this five-pair state, the first three old pairs attain the global minimum Q over all triples of actual disjoint pairs, and every actual edge has an actual disjoint partner. Then

    tau ≤ k−2 floor(k/8) ≤ 3k/4+1.

The exact state forces 100 to divide k. To obtain the displayed avoidance request, leave floor(k/8) points undeleted in each of cells 01100 and 10011, retain every point in the other five cells with positive R allowance, and delete every remaining point of U. The five wholly retained cells have total size k. Hence the deletion has size k−2 floor(k/8). Both partial trace caps are at most k/8, so the certified continuous inequalities apply exactly. If tau exceeded that deletion size, an actual avoiding R and its disjoint partner H would violate global Q minimality.

When 200 divides k, the deletion has size exactly 3k/4. No limiting argument or large-k assumption is needed for this exact-state conclusion.

## Independent geometric checks

I independently aggregated the twenty source atoms in `outputs/agent_global_eight_pair_mixed_survivor.json` using source columns [0,1,2,3,5]. The result is exactly the ten types and masses above. The source deletion indices [5,6,7,9,12,13,14] have total mass 3/4 and give the stated continuous R caps.

The response theorem itself requires only the ten-cell table, not those finer twenty source atoms or the extra old pairs used during discovery. The independent checker therefore hardcodes this exact coarse state and compares all certificate input fields against it.

Outside points do not contribute to the relevant Q counts. A two-point transversal of R,H uses one point from each, because R and H are disjoint. If either point lay outside U, it would miss every old row. The other point cannot hit both sides of even one old disjoint pair. Thus both endpoints of every relevant piercing pair lie in U.

Accordingly the old-ground traces satisfy inequalities

    Σ_i r_i≤1,   Σ_j h_j≤1,

rather than equalities. This is essential: the proof permits either new edge to use points outside U. The disjointness constraints are r_i+h_i≤w_i for every cell supporting an R variable. All zero traces are permitted; no positive-mass cutoff occurs.

For two selected old coordinates a,b, the Q polynomial is

    Q_ab=Σ_(i,j) c_ab(i,j) r_i h_j,

where c_ab(i,j)=1 exactly when the two old cell types differ at both a and b. This counts unordered point pairs correctly: disjointness of R,H determines which endpoint is the R endpoint, so no factor 1/2 is needed. All ten choices of a,b are included; the earlier reduced three- or four-average systems are insufficient and are not used.

## Exact relaxation checked at each box

There are seven R variables, ten H variables, seventy product variables p_ij, and one objective variable t, for 88 variables in total. In each closed R box l_i≤r_i≤u_i, the checker independently expands the four nonnegative products

    (r_i−l_i)h_j,
    (u_i−r_i)(w_j−h_j),
    (u_i−r_i)h_j,
    (r_i−l_i)(w_j−h_j).

After substituting p_ij for r_i h_j, these give the four McCormick envelope inequalities with exact signs. It also reconstructs the cell and rank constraints, the valid product-rank inequalities

    Σ_j p_ij≤r_i,   Σ_i p_ij≤h_j,

and all ten inequalities t≤Q_ab. There are 316 reconstructed inequalities.

The independent finite bounds are

    r_i∈[l_i,u_i], h_j∈[0,w_j], p_ij∈[0,u_i w_j], t∈[0,1].

The bound t≤1 is valid because every actual Q_ab is at most (Σr_i)(Σh_j)≤1. To contradict the target it would also suffice to set t=6/25 whenever all ten actual Q values were at least that target.

For each leaf, the supplied nonnegative rational multipliers y are checked by the exact residual formula

    d=e_t−A^T y,
    upper=y·b+Σ_j max(d_j lower_j,d_j upper_j).

Thus the check does not assume that rationalized floating-point dual multipliers solve exact dual equations. Every residual coefficient is explicitly bounded. The checker reconstructs A,b and all variable bounds rather than importing a producer matrix.

## Full coverage and results

The certificate contains 219 nodes: 109 binary splits and 110 dual leaves. There are no rank-empty leaves. The checker verifies that:

- the root is exactly the closed box from zero to the seven stated R caps;
- every split lies strictly inside its parent's coordinate interval;
- the two children are exactly the two closed half-boxes, so their shared boundary is included and no gap is introduced;
- every node is visited exactly once, with no cycles, reused children, or orphan nodes;
- every leaf bound is exact and strictly less than 239999/1000000.

The largest rational leaf bound is

    7311447002656233783991033409856629096440880795500837
    /30464596252227010033057141636484255605605008873280000,

approximately .23999815858783146. Its exact margin below 6/25 is positive and approximately 0.00000184141216854. The clean displayed bound .239999 is therefore valid for every response box.

## Reproduction

Run from the task directory:

    python3 -S work/p644_agent_audit_outside_certificate_check.py

This independent checker uses only the Python standard library and does not import optimization software or any producer module. The successful output is saved in

    outputs/agent_audit_outside_certificate_check.json.

Certificate:

    outputs/agent_global_outside_certificate.json

SHA-256:

    59a106d6d3b1c62fb2b652825632611140dcf4f9da19246635ff0c8d27efe18a

The certificate producer is `work/p644_agent_global_outside_certificate.py`, but neither its solver status nor its self-check is trusted by the independent replay.

The exact result closes this particular arbitrary-outside response branch. It does not show that an arbitrary hypothetical counterexample reaches the displayed five-pair state, and it does not furnish a universal case tree or the full 3/4 upper bound.
