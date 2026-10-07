# General-bound attack: a new near-core lemma using the full intersection gap

26 September 2026. Status: the local lemma below is proved by hand. It closes the previously recorded exact finite-menu hole at beta=107/125. A general bound below 6/7 is NOT yet asserted. Discovery searches are separate from the hand argument.

## New local closing lemma

Let H be k-uniform with property (7,2), and assume every pair intersection is either at most m or greater than k/2, where m<=k/2. Suppose T is an integer and tau(H)>T. Let E,F,G have empty common intersection, with x=|E intersect F|, y=|E intersect G|, z=|F intersect G|. Write

    Delta=max(0,x+y+z-T).

Assume y+z<=T and all the following inequalities:

    m+z<=T,                 k+y-z<=T,
    2k+x-2z<=2T,            2k+x+m-z<=3T,
    x+m<=T,
    k-x+y+Delta<=T,
    2k-2x+z+Delta<=2T,
    2k-z+Delta<=2T,
    3k-x-y+Delta<=3T.                       (NC)

Then four further legal responses produce a subfamily of at most seven edges which has no two-point transversal, a contradiction.

### Proof

Put X=E intersect F, Y=E intersect G, Z=F intersect G; these cells are disjoint. Request H4 avoiding Y union Z and a subset of X of size min(x,T-y-z). This is legal. The only potentially nonempty triple cell among E,F,G,H4 is

    P=E intersect F intersect H4,       p=|P|<=Delta.

Use the disjoint cells

    X'=X minus P,
    A=H4 intersect (E minus (F union G)),        a=|A|,
    B=H4 intersect (F minus (E union G)),        b=|B|,
    C=H4 intersect G,                           c=|C|,
    W=G minus (E union F union H4),              w=|W|.

Their elementary bounds are

    a<=k-x-y, b<=k-x-z, c<=k-y-z,
    p+a+b+c<=k,               c+w=k-y-z.

The complete products of candidate piercing pairs are

    P times (Y union Z union C union W),
    X' times C, Y times B, Z times A.

This is exhaustive: any point belonging to at least three of the first four edges lies in P; otherwise two covering points must lie in complementary pair cells.

Use three further requests, indexed 1,2,3. The following notation assigns each cell a set of permissible membership labels. For example {1,3} as a single label means the entire cell belongs to requests 1 and 3, while alternatives {1} or {3} mean the cell may be partitioned between them. Every splitting described below uses integer flows with integer capacities, so has no rounding loss.

**Case I: p+a<=m.** Put P in all three requests, X' in requests 1 and 3, Y and B in request 1, and Z and A in request 2. Partition C between requests 1 and 3, then W among all three. Before the last two partitions, the three loads are

    L1=x+y+b,              L2=p+z+a,              L3=x.

All are at most T: bound L1 by k+y-z, L2 by m+z, and L3 by x+m. The first partition fits since

    L1+L3+c = 2x+y+b+c <= 2k+x-2z <= 2T.

After partitioning C, W fits because the combined total load is

    L1+L2+L3+c+w = 2x+k+p+a+b
                         <=2k+x+m-z <=3T.

Every candidate pair is contained in one request: P lies in all of them; X' meets both possible C labels; Y and B share request 1; Z and A share request 2.

**Case II: p+a>m.** The global dichotomy gives p+a>k/2. Since (E intersect H4) and (G intersect H4) are disjoint, c<k/2, and consequently c<=m.

Put P in requests 1 and 2, X' and C in request 2, Y and B in request 1, and Z in requests 1 and 3. Partition A between requests 1 and 3, and W between requests 1 and 2. The base loads are

    L1=p+y+z+b,             L2=x+c,               L3=z.

All fit: L1<=Delta+k-x+y, L2<=x+m, and L3<=m+z. The two flexible cells can be assigned if and only if

    a<=2T-L1-L3,
    w<=2T-L1-L2,
    a+w<=3T-L1-L2-L3.

These are the elementary capacity conditions for two items whose allowed request pairs are {1,3} and {1,2}; they also follow directly from the integral max-flow theorem. Here they hold because

    L1+L3+a <= Delta+2k-2x+z <=2T,
    L1+L2+w =p+x+k+b <=Delta+2k-z <=2T,
    L1+L2+L3+a+w =p+x+k+z+a+b
                                 <=Delta+3k-x-y <=3T.

Every candidate pair is covered: P's labels {1,2} meet the labels of Y,Z,C,W; X' and C share request 2; Y and B share request 1; both possible A labels meet Z's {1,3}. Thus the three avoiding responses eliminate every possible two-point transversal of the first four rows. This proves the lemma. QED.

## It closes the exact recorded 0.856 hole

At scale k=500 take

    (x,y,z)=(200,43,186), m=200, T=428, Delta=1.

The nine left sides in (NC), compared with the corresponding right sides, are

    386<=428, 357<=428, 828<=856, 1214<=1284,
    400<=428, 344<=428, 787<=856, 815<=856, 1258<=1284.

Thus the hole of Proposition 7.52 closes with substantial slack once the *complete* global largest-small-intersection hypothesis is used. No minimum-good-triple-sum assumption and no earlier chronological gaps are needed for this local argument. The old menu minimum 2143/2500 remains a correct statement about the old menu.

For chronological coverage the hypothesis must be supplied legitimately: choose a globally largest intersection m<=k/2, or first prove the corresponding upper gap. It cannot be assumed at an arbitrary triple merely because its own largest pair cell equals m.

## Exact affine-region form

Normalize k=1. For Delta=x+y+z-beta>=0 the region is the simultaneous condition that the following expressions are at most beta:

    y+z, 2beta-x-y-z,
    m+z, 1+y-z, 1+x/2-z, (2+x+m-z)/3, x+m,
    (1+2y+z)/2, (2-x+y+2z)/3, (2+x+y)/3, (3+z)/4.

For Delta=0 replace the domain expression 2beta-x-y-z by x+y+z and replace the last four expressions by

    1-x+y, 1-x+z/2, 1-z/2, 1-(x+y)/3.

Every permutation of x,y,z is available. The encoder is `work/paper_push/general/nearcore_maxsmall.py`. Its main region combines both affine alternatives for each max(0,S-beta) term directly; this avoids artificial subdivision along S=beta.

## Discovery provenance and current computation

The existing response-allocation synthesis was run with the additional full gap (m,k/2], first with and then without the older three exclusions. It found complete covers at the displayed point. The hand proof above was extracted from two of its allocations and is independent of the numerical discovery. The files `maxsmall_response_synth.py` and `maxsmall_only_synth.py` retain those probes and rational outputs. Z3 UNSAT output is not being used in place of this proof.

The largest-small coverage probe at beta=107/125 uses the previously certified 55-step exclusions and adds the new lemma. Results and any remaining holes are pending.

## Gap-refined version of the new lemma

Suppose additionally no pair intersection lies in [ell,h]. Use the same near-core request, and require

    x+z >= k-h,               T >= k+y-h.

Since p+b<=min(Delta+k-x-z,k), the first two inequalities give p+b<=h, and the excluded interval implies p+b<ell. (Here Delta=max(0,x+y+z-T); its two alternatives are exactly the two displayed conditions.)

Retain the four Case I inequalities

    m+z<=T, k+y-z<=T,
    2k+x-2z<=2T, 2k+x+m-z<=3T,

and x+m<=T. For Case II it now suffices to replace the four Delta-dependent inequalities by

    ell+y+z<=T,
    k-x+2z+ell<=2T,
    k+x+ell<=2T,
    2k+z-y+ell<=3T.

Proof: the same Case II base load L1 is at most ell+y+z. Its Hall left sides obey

    L1+L3+a <= ell+y+2z+a <= k-x+2z+ell,
    L1+L2+w = p+x+k+b <=k+x+ell,
    L1+L2+L3+a+w =p+x+k+z+a+b <=2k+z-y+ell.

All are integer-capacity allocations and need no further rounding. This is a second hand-proved closing region.

This version closes the next exact menu hole produced after adding the first version: normalize k=1 and take x=27143/64000, y=147/1000, z=179/500, beta=107/125, m=x. Use the previously proved exclusion [ell,h]=[267/1000,89/250]. In particular the former failing estimate (2+x+y)/3 is replaced by (1+x+ell)/2<beta. The region encoder includes this gap-refined version, with every gap required as a prior hypothesis.

## A third allocation removes one small-trace bottleneck

In either version above, the Case I inequality

    2k+x-2z<=2T

may instead be replaced by the following five inequalities:

    k+2x+2y+z<=3T,            x+y<=T,
    2k+2x+3y<=4T,             k+2x-z<=2T,
    3k+3x+2y-z<=5T.                              (NC+)

All the other inequalities of the chosen version remain unchanged.

Proof. Write v=p+a=|E intersect H4| and d=k+2x+y-2T. In Case I, if v>=d, use its original allocation: the formerly problematic two-bin bound now follows from p+a+b+c<=k, because

    L1+L3+c=2x+y+b+c<=2x+y+k-v<=2T.

If v<d, necessarily d>0. Use a third allocation: P belongs to all three requests; X' to requests 2,3; Y to requests 1,2; Z and A to request 1. Partition B between 1,2 and C between 2,3; then distribute W among all three. The base loads are

    L1=v+y+z,                L2=x+y,              L3=x.

They fit since d+y+z<=T is the first inequality of (NC+), and x+y<=T. The flexible B,C cells have capacities if and only if

    b<=2T-L1-L2,
    c<=2T-L2-L3,
    b+c<=3T-L1-L2-L3.

It suffices to check the stronger final condition with b+c+w on the left. The required bounds are

    L1+L2+b <= d+k+2y <=2T,
    L2+L3+c <= k+2x-z <=2T,
    L1+L2+L3+b+c+w <=d+2k+x+y-z <=3T.

After substituting d these are exactly the last three inequalities of (NC+). Thus the integer allocation exists. Candidate-pair coverage is immediate from these labels: P occurs in all requests; both B labels meet Y's {1,2}; both C labels meet X's {2,3}; A and Z meet in request 1.

This refinement closes the thin new local hole near (x,y,z)=(.424125,.098024,.356057), where the replaced inequality failed by approximately .0000107k. The first new lemma already closed the much older .4,.086,.372 hole; this third allocation enables progress past its next local barrier.

## Fully omitted core: no budget should be spent on an isolated cell

If x+y+z<=T, the first request avoids the entire pair-cell union, so P is empty. The cell W then has no candidate-pair neighbor and may be omitted from every final request.

Consequently, in the original (non-gap) lemma, replace the four Delta-dependent inequalities by just

    k-x+y<=T,                 2k-2x+z<=2T,

and add the domain condition x+y+z<=T. The Case I conditions stay as stated, either original or strengthened by (NC+).

Proof. In Case II, use the same base loads with p=0 and partition A between requests 1 and 3; W is not assigned. It suffices that all base loads fit and a<=2T-L1-L3. These are precisely x+m<=T, k-x+y<=T, z<=T, and 2k-2x+z<=2T. The other two Hall conditions from the earlier proof arose only from W and are no longer needed. All candidate products that survive when P is empty remain covered. The Case I proof already succeeds even if W is unnecessarily assigned, so needs no change.

This is used only on its explicit x+y+z<=T domain. The encoder `fullcore_regions` records that domain as one of its affine inequalities.

## Further progress and a precise surviving obstruction

The maximum-small coverage run now uses the actual initial coordinate m=x, rather than unnecessarily replacing it by the upper end of its slab. It also applies Lemma 7.46 with the full gap (m,k/2]. That lemma's proof needs only the consequence that a trace at most k/2 is at most m, so its conclusion remains valid with this open lower endpoint. This additional legitimate use closes the intermediate (.4242,.2122,.3561) barrier at a sufficient budget .8484.

With all new regions, exact-rational discovery covers 72 maximum-small slabs, through m=.428, at beta=.856. This is progress of the sufficient-region search, not a new general bound. The next actual parameter corner is

    (m,y,z)=(137/320,0,179/500)=(.428125,0,.358).

The complete desired coverage is unfinished. The JSON `maxsmall_nearcore_107_125.json` retains accepted trees and the failed corner; it has not been independently replayed as a new theorem.

A second route legitimately chooses a globally minimum-sum good triple after obtaining a starting sum bound; its pair cells need not retain the original maximum m. The global maximum-small gap remains available. The probe `minsum_exchange_probe.py` tests S<=6289/8000, global m=137/320, all prior gaps, the minimum-sum inequalities for a full-core fourth response, and the possibility of closing any of the four resulting good triples by the old or new local menu. A padded version uses every remaining point of first-request budget on the private part of F. This does not yet close even the branch in which all initial pair sizes are at most m.

### Exact obstruction to that padded four-edge finish [C]

At rank k=64000 and budget T=54784, use pair-cell sizes

    x=27400, y=22786, z=2,

for a good triple E,F,G. Its sum is S=50188. A legal fourth response H, after avoiding X,Y,Z and T-S=4596 private points of F, has

    a=|E intersect H|=4597,
    b=|F intersect H|=32001,
    c=|G intersect H|=27400.

All four triple intersections vanish; all six pair cells are positive. Every pair intersection is at most m=27400 or greater than k/2=32000. The three prior exclusion intervals at this scale are

    [12544,13568], [17088,22784], [27648,30336],

and all six intersections avoid them. The original triple has minimum pair sum among the four triples, since

    x+a+b=63998, y+a+c=54783, z+b+c=59403,

all at least S=50188. The padded response bound b<=k-T+y=32002 is satisfied.

Every three simultaneous final requests covering the candidate pairs have maximum size at least **54787**, strictly greater than T. This lower bound is exact: split C into two equal 13700-point parts and take requests

    X union Z union A union C1,
    X union C2,
    Y union B.

Their sizes are 45699,41100,54787, and they cover respectively the three candidate products X times C, Y times B, Z times A.

The standard-library checker `work/paper_push/general/check_padded_minimum_barrier.py` verifies every rank, all gaps, the minimum-sum inequalities, and the first-request legality. It enumerates the complete 18^3=5832 antichain label assignments for the three disjoint candidate-pair components. Each assignment admits one of ten rational request-price vectors whose lower bound is at least 54787. This certifies the exact optimum without numerical optimization.

This is an obstruction to the specified padded fourth response followed by three simultaneously chosen requests. It does not prove existence of a high-transversal (7,2) family realizing the state, and does not exclude a different distribution of the first-request padding, later adaptive requests, or use of further seven-edge subsets. Global minimum-sum selection is valid but, by itself, does not remove this particular finishing obstruction.

### A tested alternative first request and the remaining issue

At the last exact barrier, leaving 2 points of Y unrequested permits spending 2 additional points in F's private part. Then every fourth response has F-trace at most k/2, hence at most m by the full gap. This request is legal and leaves only an EGH triple cell of size at most2. The rational discovery probe `forcedhalf_synth.py` still finds a three-simultaneous-request menu survivor, even with the applicable minimum-sum inequalities. Those probe outputs have not been promoted to an independently checked obstruction theorem.

The reason is concrete: a positive EGH cell, however small, has candidate pairs with every point in the opposite edge F, including its large private remainder. Eliminating those pairs requires the final requests collectively to cover that remainder. This support cost does not vanish with the mass of the triple cell. Therefore an argument that simply ignores o(k)-sized Venn cells would be invalid. Later adaptive responses, a different first-request distribution, or a genuine global reduction could still overcome this obstacle.

For the mixed-trace route with disjoint anchors E,G, maximize |F intersect(E union G)| only over rows meeting BOTH anchors. Maximizing over all rows is useless because E and G themselves attain k. A response with larger trace sum contradicts the mixed maximum only when both its anchor traces are positive; pure-response branches need separate arguments. This route has not yet produced a theorem.

## End-of-task status

New proved contributions are the near-core closing lemma, its gap refinement, the NC+ allocation, and its fully omitted-core refinement. Root independently checked all four hand arguments. A standard-library exact certificate establishes the padded minimum-sum finishing obstruction. The recorded complete general upper coefficient remains 6/7; no improvement below it has been established in this task.
