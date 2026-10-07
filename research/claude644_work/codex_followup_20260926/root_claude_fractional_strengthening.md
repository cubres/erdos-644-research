# Stronger fractional and actual-subfamily consequences of Claude's dual pencil

26 September 2026. Status: full hand proofs below. Claude's new input is the
dual-pencil request lemma in `claude644_work/capture/notes_core.md`, sections
c1--c2. The additional steps retain unions instead of replacing them by sums,
and apply the resulting ambient fractional cover to the earlier pruning
programme. These results do not improve the general coefficient 6/7 or prove
the desired three-quarter bound.

Throughout H is a finite family of nonempty sets of rank at most k, with
property (7,2) for subfamilies of AT MOST seven edges, and t=tau(H).
The fractional covering number tau_f is the usual LP invariant, not the
continuous type-family coefficient denoted tau* elsewhere in the note.

## 1. Dual-pencil lemma, including a self-contained proof

Take any four indexed edges G1,...,G4, allowing repetitions. Their three
perfect matchings are M5={12,34}, M6={13,24}, M7={14,23}. Write

    I_j = union of (G_a intersect G_b) over ab in M_j,
    a_j = |I_j|.

If all a_j<=t-1, then

    a_i+a_j >= 2t-k-1    for any two distinct i,j in {5,6,7}.       (1)

Proof. Relabel the matchings so a6+a7<=2t-k-2, and request G5
avoiding I5. Request G6 avoiding I6 together with an arbitrary subset
Y of G5 minus I6 of size min(|G5 minus I6|,t-1-a6). Both requests have
size at most t-1, and

    |G5 intersect G6| <= max(0,k-t+1+a6).

Consequently I7 union (G5 intersect G6) has size at most t-1: use
a7<=t-1 if the maximum is zero, and a6+a7<=2t-k-2 otherwise.
Request G7 avoiding that union. Each G_j, j=5,6,7, avoids I_j, and
G5 intersect G6 intersect G7 is empty.

Any pair piercing all seven indexed edges would have a point x in two
of G5,G6,G7 and a point y in the remaining one. For example, if x is
in G5 intersect G6, its membership among G1,...,G4 contains no pair
from M5 or M6, hence has size at most two. If size two, it is a pair
of M7 and its complement is the other M7 pair. If size at most one,
the complement still contains an M7 pair. In either case y would
have to lie in I7, contrary to y in G7. The other choices of two
last rows are symmetric. Thus no two points pierce all the rows,
contradicting (7,2). Repetitions do not affect the argument. QED.

Order the a_j increasingly. Either the largest is at least t or the
two smallest sum to at least 2t-k-1. In the latter case their total
is at least ceil(3(2t-k-1)/2). We have therefore proved the UNION
inequality

    a5+a6+a7 >= m,
    m = min(t, ceil(3(2t-k-1)/2)).                              (2)

In particular m=t whenever 4t>=3k+2. Unlike a bound on the sum of
all six pairwise intersection sizes, (2) counts a point lying in
all four initial rows only three times, rather than six.

## 2. A sharper fractional-cover constant

Assume m>0 and put beta=m/k. Since a maximal matching has at most
two edges, their union covers H; hence t<=2k and 0<beta<=2. Then

    tau_f(H) <= C(beta) := 6/beta - beta/12.                    (3)

More precisely, tau_f(H) is at most the unique w>=2 satisfying

    6/w - 3/w^3 = beta.                                      (4)

Proof. By fractional matching-cover duality, normalize an optimal
fractional matching of weight W=tau_f(H) to a probability distribution
on actual edges. For each vertex v its inclusion probability p_v
satisfies p_v<=1/W, and sum_v p_v<=k. Sample four edges independently.
For each of the three matchings, the probability that v belongs to
its union I_j is 2p_v^2-p_v^4. Taking expectations in (2) gives

    m <= sum_v (6p_v^2-3p_v^4).                              (5)

For W>=2, the function 6p-3p^3 is increasing on [0,1/W]. Thus

    beta <= 6/W - 3/W^3.                                    (6)

The right side strictly decreases for W>=2, has value 21/8 at 2,
and tends to zero. This proves (4); W<2 is covered trivially because
the root is larger than 2. Inequality (6) first gives W<=6/beta;
substituting 1/W^2>=beta^2/36 in beta W<=6-3/W^2 gives (3).
For W<2, (3) again holds, since C(beta)>=17/6 for beta<=2. QED.

For 4t>=3k+2, beta=t/k>3/4, so a convenient rational consequence is

    tau_f(H) <= 127/16 = 7.9375.                             (7)

The limiting root in (4) at beta=3/4 is approximately 7.93650.
Claude's sum-of-pairwise-intersections corollary gave 6k/t, with
limiting value 8. This is a small but strict improvement of that
fractional constant. Its more substantial use below comes from
combining either constant bound with the earlier pruning arguments.

## 3. Every small actual subfamily can be covered efficiently

If an ambient fractional cover has total weight at most C>1, let

    gamma(C) = -log(1-1/C).

Any actual subfamily A of H with M>=1 edges satisfies

    tau(A) <= floor(log(M)/gamma(C))+1.                       (8)

Proof. Normalize the cover weights to a probability distribution.
Every edge is hit with probability at least 1/C. After s independent
draws, the expected number of missed rows is at most M(1-1/C)^s.
Taking s=floor(log(M)/gamma(C))+1 makes this less than one, so some
outcome hits every row. Repeated sampled vertices only lower the
number of points. The cover can be chosen on the original support.
QED.

Consequently

    M >= exp(gamma(C)(tau(A)-1)).                            (9)

Apply (8) with the ambient cover from (3), or use C=127/16 under
4t>=3k+2. In particular any such H has

    |H| >= (127/111)^(t-1).                                 (10)

At t=(3/4+o(1))k this lower bound is exp((0.10099266...+o(1))k).
This strengthens the exp(Omega(k^(2/3))) necessary count obtained
earlier from the general bound tau_f<=(35k)^(1/3). It is a necessary
condition for a hypothetical counterexample, not an upper bound
on the integral transversal number.

## 4. Arbitrarily overlapping private families of subexponential size

Suppose E is critical, B is a (t-1)-cover of H minus {E} disjoint
from E, and P is the family of ALL actual rows with B-trace of size
one. Let M=|P|>=1. With C as in (3), there are Q contained in E and
Z outside E such that Q is nonempty,

    |Q|+|Z| <= floor(log(M)/gamma(C))+2,                      (11)

Q union Z meets E and all P, and the ACTUAL residual avoiding that
set has transversal number at least t minus the right side of (11).
Every surviving row has B minus Z trace of size at least two.

Proof. Apply (8) to P to get a cover S. Set Q=S intersect E and
Z=S minus E; if Q is empty, add any point of E. All original rows
other than E meet B, all its private rows have been hit, and surviving
rows avoid B intersect Z, proving the trace assertion. Adjoining
Q union Z to a cover of the residual covers H, proving the bound.
No projection, saturation, or trace-overlap hypothesis is involved.

Thus log M=o(k) suffices to preserve the entire fixed linear excess
above 3k/4. The older cube-root argument required log M=o(k^(2/3)).
This conclusion permits |Q|=o(k); it does not retain the stronger
|Q|<=2 of the common-color argument.

There is also a quantitative count-tail alternative. Order the
private counts at the s=|B| centers as q1>=...>=qs, let p=tau(P),
and let M_r=sum_{i>r}q_i. Paying the first r centers and applying
(8) to the remaining private rows gives, for 0<=r<p-1,

    q_(r+1) >= exp(gamma(C)(p-r-1))/(s-r).                   (12)

Hence linear private transversal number requires linearly many
centers, each supporting exp(Omega(k)) actual private rows. Large
private counts alone do not imply a large private transversal.

## 5. Pruning several cover-trace layers at once

Let B be ANY transversal of H, and let L>=1 be an integer. Denote
by A_L all actual rows with B-trace size at most L, and M_L=|A_L|.
If M_L=0, take D=Z=empty and K=H, with no transversal loss. In the
following bounds assume M_L>=1.
Use the ambient fractional cover w of total at most C and set

    D={b in B: w_b>=1/(2L)},      |D|<=2LC.

Any row of A_L avoiding D receives less than 1/2 of its cover
weight from B. Thus 2w restricted outside B covers all those rows
fractionally, with total at most 2C. If M_L>=1, choose an outside-B
integral cover Z with

    |Z| <= floor(log(M_L)/gamma(2C))+1.                      (13)

If no such row survives D, take Z empty. The actual residual

    K={F in H: F avoids D union Z}

satisfies

    tau(K)>=t-2LC-floor(log(M_L)/gamma(2C))-1,               (14)

and every surviving B minus D trace has size at least L+1.
In particular L=o(k) and log M_L=o(k) preserve any fixed linear
excess. For a critical cover B that misses E alone, also pay one
arbitrary point of E; this adds at most one to the loss.

All rows in K are actual original edges. Rank and (7,2) pass to K.
However the maximum rank need not fall, B minus D need not remain
minimum or critical, and the cover cost per trace layer is not
small enough to force a contradiction just from |B|. These are
the remaining limitations of this reduction.
