# A new three-role support and a quantified endpoint-family theorem

Status: the capacity formula is **[C], exact and independently replayable**. The endpoint-family theorem below has an elementary covering argument and 24 exact rational primal certificates. It proves a continuous type-closed statement, not the unrestricted Erdős 644 conjecture. No publication or external edit has been made.

All scripts and certificates named below are in `work/paper_push/three_cert/` in this Codex workspace. The Clauding originals remain unchanged.

## 1. The support and its exact capacity formula [C]

Number the seven rows 0 through 6. Use role assignment

\[
(a,a,b,b,c,c,c)
\]

and maximal parent cells, in bitmask notation,

\[
\mathcal D=(11,19,46,54,60,78,86,92,101,102,106,114,120).
\]

No two cells of \(\mathcal D\) have union 127. Hence any masses placed on these cells, or on their subsets, give a seven-row family which cannot be met by two points.

For nonnegative scalar loads \(a,b,c\) in one part, let \(M(a,b,c)\) be the least total mass needed to realize these seven row loads. Then

\[
\begin{split}
M(a,b,c)=\max\{&b/3+c,\ 2b/3+2c/3,\ 2a/5+b/5+c,\ 2a/5+4b/5+2c/5,\\
&a/2+c,\ a/2+b/2+3c/4,\ a/2+b,\ 2a/3+2b/3+c/3,\\
&7a/10+b/2+7c/10,\ 3a/4+b/4+3c/4,\\
&3a/4+3b/4+c/4,\ 4a/5+2b/5+3c/5,\ a+c/2,\ a+b/2\}.
\end{split}
\]

Here is the complete proof mechanism. Put nonnegative masses \(y_S\) on the parent cells and require \(\sum_{S\ni j}y_S\ge d_j\) for each row demand. The dual polytope is

\[
P=\{w\in\mathbb R^7_{\ge0}:\ \sum_{j\in S}w_j\le1\quad(S\in\mathcal D)\}.
\]

It is bounded, since every coordinate occurs in a cell, and full-dimensional, since a sufficiently small positive vector satisfies every cell inequality strictly. Thus every vertex has seven linearly independent active constraints among its thirteen cell inequalities and seven nonnegativity inequalities. Enumerating all \(\binom{20}{7}=77520\) such bases by exact integer elimination is complete. The independent checker obtains 36 vertices including the origin. Projection by the sums of coordinates in the three roles gives 24 points including zero; exactly the fourteen vectors displayed above are maximal in the coordinatewise order. Every other projected vector is dominated by one of them. Linear-programming duality now proves the formula for all nonnegative loads.

The covering LP initially supplies row loads at least as large as requested. Delete excess membership in each row independently. Every new cell is a subset of an old cell, so no covering pair is introduced and total mass does not increase. This proves the exact-load interpretation used here.

`endpoint_new_template.py` discovered the formula with Claude's original support enumerator. The independent `check_new223_facets.py` uses a different enumeration: every full basis of all twenty inequalities, including the origin, solved by fraction-free Bareiss elimination. It imports no original research module and no numerical package. It compares the complete result with `endpoint_new_template.template.json` and the fourteen stated forms.

Replay:

```sh
python3 work/paper_push/three_cert/check_new223_facets.py
```

Observed result: `PASS 77520 bases; 36 vertices including origin; 24 projected; 14 exact capacity forms`, in 6.84 CPU seconds. The machine-readable receipt is `check_new223_facets.json`.

## 2. A full interval theorem

Work in the continuous type-closed model, with three part capacities \(x\), admissible unit types \(C\subseteq[0,x]\), and property \((7,2)\). Write \(\tau^*(C)\) for the total capacity minus the supremal size of a box containing no admissible type. No convexity assumption on \(C\) is needed.

**Theorem.** For \(0\le t\le1/100\), suppose

\[
x=(3/4+t,3/4,3/4)
\]

and \(C\) contains the three types

\[
\begin{aligned}
A&=(1/2+849t/1000,\ 0,\ 1/2-849t/1000),\\
B&=(0,\ 1/2+99t/1000,\ 1/2-99t/1000),\\
C_0&=(0,\ 1/2-49t/1000,\ 1/2+49t/1000).
\end{aligned}
\]

Then

\[
\boxed{\tau^*(C)\le3/4-1047t/1000.}
\]

In particular, at \(t=1/100\) the upper bound is \(73953/100000=.73953\).

**Proof.** Consider the retained request box

\[
u=(3/4+t,\ 3/4,\ 1047t/1000).
\]

Its deletion cost is \(3/4-1047t/1000\). If the claimed bound fails, this box must contain an admissible unit type \(U\). We show that every such \(U\) produces a bad seven-row realization with the three anchors.

The following four boxes are partner boxes: if \(U\) lies below one of them, its indicated support realizes a bad tuple.

| Box | Coordinate caps | Support row assignment |
| --- | --- | --- |
| \(R\) | \((3/4+t,\ 1/2-347t/1000,\ 1047t/1000)\) | V4: \((A,U,B,B,B,B,C_0)\) |
| \(S\) | \((1/2-245t/1000,\ 3/4,\ 1797t/1000)\) | V4: \((B,U,A,A,A,A,A)\) |
| \(P\) | \((5/8+651t/1000,\ 1/2+49t/2000,\ 12t/5)\) | NEW223: \((C_0,C_0,U,U,A,A,A)\) |
| \(Q\) | \((1/2+151t/500,\ 5/8+49t/1000,\ 12t/5)\) | NEW223: \((A,A,U,U,C_0,C_0,C_0)\) |

The V4 support in the stated row order has parent cells

\[
(3,60,77,86,92,106,108,113,116,120).
\]

The NEW223 support is that of Section 1. Each support's capacity claim is certified at both interval endpoints by nonnegative rational masses for each of the three parts. There are \(2\cdot4\cdot3=24\) such certificates. At each endpoint the masses cover the seven loads obtained by substituting the entire partner cap for \(U\), and their total is at most the corresponding part capacity. All capacities and row loads are affine in \(t\). Convex interpolation of the two endpoint allocations therefore proves every claim throughout the interval. Trimming excess membership handles every \(U\) below the cap. This argument is independent of the complete dual enumeration in Section 1.

It remains to prove that these boxes cover the requested unit slice. Suppose \(U\le u\) lies outside all four boxes. The third requested coordinate fits all four, while \(R_0=x_0\) and \(S_1=x_1\). Thus

\[
U_1>R_1,\qquad U_0>S_0.
\]

If escape from \(P\) occurred through \(U_0>P_0\), then

\[
U_0+U_1>P_0+R_1=9/8+304t/1000>1,
\]

which is impossible for a nonnegative unit type. Hence \(U_1>P_1\). If escape from \(Q\) occurred through \(U_1>Q_1\), then

\[
U_0+U_1>S_0+Q_1=9/8-196t/1000>1
\]

on the whole interval. Hence \(U_0>Q_0\). Finally,

\[
U_0+U_1>Q_0+P_1=1+653t/2000\ge1,
\]

again impossible. This covers the entire request slice and proves the theorem. \(\square\)

The independent endpoint checker uses only standard-library rational arithmetic. It verifies nonnegativity, total mass, all seven row demands, the noncovering-pair property, the endpoint covering inequalities, and the exact request cost:

```sh
python3 work/paper_push/three_cert/check_endpoint_interval.py
```

Observed result: `PASS 24 rational endpoint part certificates; convex interpolation covers 0<=t<=1/100; tau*<=3/4−1047t/1000`.

The data are `endpoint_interval_model.py` and `endpoint_interval_certificate.json`; `certify_endpoint_interval.py` is the optional numerical producer. The verifier does not import SciPy. The parent agent has independently replayed this certificate and checked the hand covering proof.

## 3. The full fan-in parameter cone

The same support roles prove a broader statement, independently derived by the theory agent in `outputs/paper_push_endpoint_repair.md`.

**Cone theorem.** Let

\[
0\le t\le1/50,\qquad g\ge2t/3,\qquad h,j\ge0,\qquad g+h+j\le t.
\]

Suppose a continuous type-closed family with property \((7,2)\), part capacities \(x=(3/4+t,3/4,3/4)\), contains

\[
A=(1/2+g,0,1/2-g),\quad
B=(0,1/2+h,1/2-h),\quad
C_0=(0,1/2-j,1/2+j).
\]

Then

\[
\boxed{\tau^*(C)\le3/4-g+j\le3/4-t/3.}
\]

In particular the bound is strictly below \(3/4\) for every \(t>0\). If \(g>2t/3\), or if \(h>0\), the second inequality is strict.

**Proof.** Set \(r=g-j\). The domain gives \(r\ge t/3\). Use the same four supports and row assignments as in Section 2, now with caps

\[
\begin{aligned}
R&=(3/4+t,\ 1/2-4h,\ r),\\
S&=(1/2+4t-5g,\ 3/4,\ r),\\
P&=(5/8+3t/2-g,\ 1/2+j/2,\ r),\\
Q&=(1/2+2t-2g,\ 5/8+j,\ r).
\end{aligned}
\]

Their capacity validity follows by substituting their loads into the six V4 forms and the fourteen NEW223 forms from Section 1. Each resulting inequality is affine in \((t,g,h,j)\). The parameter polytope is the convex hull of the origin and the four points at \(t=1/50\) with

\[
(g/t,h/t,j/t)\in\{(2/3,0,0),(1,0,0),(2/3,1/3,0),(2/3,0,1/3)\}.
\]

To see completeness of this vertex list, for \(t>0\) put \(\alpha=g/t-2/3\). Then \(\alpha,h/t,j/t\) are nonnegative and sum to at most \(1/3\), a tetrahedron with exactly the four listed vertices; varying \(t\) adds the origin. The independent checker verifies every capacity inequality at all five vertices, and hence on the whole polytope. There are 600 such exact checks in total.

Request \(u=(x_0,x_1,r)\). Its deletion cost is \(3/4-g+j\). An escaping unit response would again satisfy \(U_1>R_1\) and \(U_0>S_0\). The two alternatives that would escape \(P\) through its first coordinate or \(Q\) through its second are impossible, because

\[
P_0+R_1=9/8+3t/2-g-4h\ge9/8-t/2>1,
\]

\[
S_0+Q_1=9/8+4t-5g+j\ge9/8-t>1.
\]

Consequently \(U_1>P_1\) and \(U_0>Q_0\). But

\[
P_1+Q_0=1+2t-2g+j/2\ge1,
\]

which contradicts the unit sum. Thus the request box is covered by the four partner boxes and cannot contain an admissible type. This proves the first bound. Finally \(j\le t-g-h\) gives

\[
g-j\ge2g+h-t\ge t/3,
\]

with the stated strictness. \(\square\)

Replay:

```sh
python3 work/paper_push/three_cert/check_new223_facets.py
python3 work/paper_push/three_cert/check_endpoint_cone.py
```

The second command reports `PASS five parameter vertices; 600 exact capacity inequalities; four-box cover; tau*<=3/4-g+j<=3/4-t/3`. It uses the NEW223 formula whose independent completeness is established by the first command, and the previously proved six-form V4 capacity lemma. Both use only the Python standard library. The narrower interval theorem in Section 2 retains its sharper numerical bound \(3/4-1.047t\); the cone theorem applies to a larger domain.

## 4. What this resolves and what remains open

The endpoint \(t=.01\) was an exact obstruction to the previous one-request support menu. With the new response allowed to repeat, all Fano assignments, V4 roles, all 42 two-type capacity functions, and the prior mixed1321 support still required deletion cost at least \(.8321\). `check_endpoint_menu_barrier.py` exactly verified that restricted optimum. The initial exactly-one-occurrence response menu had cost \(.98855\). Neither figure was an obstruction to all possible supports.

The new support was discovered by testing the concrete escaped response \(U_*=(.498,.502,0)\) with an unrestricted seven-row support MILP. Its bad tuple has roles \((A,A,B,B,U_*,U_*,U_*)\). Exact primal and dual masses were then reconstructed, and the reusable support formula extracted. Its full partner menu yields the four-box request above, overcoming the earlier obstruction for an entire parameter interval.

This is a quantified positive result, stronger than a sampled state closure. It does not establish the balanced three-part theorem for all configurations, nor the unrestricted \(3/4\) upper bound in Problem 644. The broader near-critical cube \([.75,.765]^3\) remains unproved by this pipeline. Earlier finite-grid success and timed-out search trees are preserved as discovery history, not promoted to theorems.
