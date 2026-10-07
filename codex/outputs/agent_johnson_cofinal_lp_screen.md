# Johnson-scheme LP with all cofinal layers: finite feasibility barrier

Status: **exact rational feasible certificates** at the three finite parameters below; **unknown** at k=80. No infeasibility signal, improved upper bound, or asymptotic feasibility theorem was obtained. The screen has been stopped without starting an SDP or a wider search.

## Scope and formulas

Let H be a nonempty complement-closed family of k-sets on 2k points. Its averaged Johnson distance distribution is

    A_i = |H|^{-1} #{(E,F) in H² : |E\F|=i},   0≤i≤k.

The necessary conditions used here are

    A_0=A_k=1,  A_i=A_{k−i},  0≤A_i≤v_i=binom(k,i)².

Only intersection sizes in

    [0,M] union [T−M,k−T+M] union [k−M,k]

are permitted. Equivalently A_i=0 whenever k−i lies outside this set.

The Johnson eigenvalue for distance i on eigenspace j is

    P_i(j)=Σ_{h=0}^i (−1)^h binom(j,h) binom(k−j,i−h)².

The implementation checks this against the independent form

    P_i(j)=Σ_{h=0}^i (−1)^{i−h} binom(k−h,i−h)
                         binom(k−j,h) binom(k+h−j,h).

The latter formula and the dual-eigenmatrix relation are given in Theorem 5.4 of M. Aljohani, J. Bamberg and P. J. Cameron, *Synchronization and separation in the Johnson schemes*, Portugaliae Mathematica 74 (2017), 213–232, available from the publisher at https://ems.press/content/serial-article-files/44790 . The nonnegative distance-transform formulation is also explicitly stated in Theorem 21 of the CWI exposition at https://ir.cwi.nl/pub/6624/6624D.pdf . These primary-source formulas were checked before implementation.

Writing m_j=binom(2k,j)−binom(2k,j−1)>0, the dual eigenmatrix entry is m_j P_i(j)/v_i. Delsarte positivity therefore gives

    Σ_{i=0}^k A_i P_i(j)/v_i ≥ 0,    0≤j≤k.

For completeness, this positivity is the nonnegativity of the quadratic form of the indicator of H against each orthogonal projection onto an eigenspace of the Johnson scheme. Complement symmetry makes odd-j sums zero; the producer imposes the even-j constraints, while the independent checker verifies every j.

## All cofinal-layer inequalities

Suppose tau(H)>T. Every T-set is avoided by an edge; by complement closure, every T-set is therefore contained in an edge.

Fix an actual E in H and count T-sets S with |S∩E|=j. There are binom(k,j)binom(k,T−j) such S. An actual F with |F∩E|=k−i contains

    binom(k−i,j)binom(i,T−j)

of them. Counting with multiplicity and then averaging over E yields the necessary inequality

    Σ_i A_i binom(k−i,j)binom(i,T−j)
        ≥ binom(k,j)binom(k,T−j),    0≤j≤T.

Every one of these inequalities is included. Summing them yields the weaker cardinality bound

    |H|=Σ_i A_i ≥ binom(2k,T)/binom(k,T).

These are exact inequalities; no floating-point coefficient approximation is used in either production or replay.

## Results

| k | T | M | Exact LP status | Formal cardinality / cofinality lower bound |
| ---: | ---: | ---: | --- | ---: |
| 20 | 15 | 7 | feasible | 1.1438117095 |
| 40 | 30 | 13 | feasible | 1.1387625483 |
| 40 | 31 | 13 | feasible | 6.3595789972 |
| 80 | 60 | 25 | unknown | no certificate returned |

The ratios in the last column are only convenient decimal summaries. All saved coordinates and all verified inequalities are rational and exact. At k=20 the integer spectrum happens to allow every distance, so this case primarily checks the formulation. The k=40 cases have genuinely forbidden distance intervals.

In particular, the strengthened LP remains feasible at T/k=.775 and M/k=.325. Thus the failure is not confined to equality at 3/4. The root's separate hand gap-amplification argument applies asymptotically when M<(3T−k)/4; these proportions satisfy that condition. The feasible formal distribution does not encode the compatibility across three actual edges that the hand argument uses.

A formal distance distribution is not asserted to come from any actual family. Exact feasibility means only that no linear combination of the listed constraints can prove a contradiction at that parameter set. These finite certificates do not establish feasibility for all sufficiently large k and hence do not, by themselves, rule out an asymptotic Delsarte argument with a different parameter regime or additional constraints.

The k=80 exact run continued consuming CPU beyond its requested 30-second solver timeout. It was manually terminated after several minutes, preserving the script and recording status UNKNOWN. No feasible point or infeasibility certificate was returned. No conclusion about that LP's feasibility is made.

## Independent replay

Producer:

    /Users/cubres/Documents/Clauding/erdos-hunt/p644_agent_audit_johnson_cofinal.py

Independent standard-library checker:

    cd /Users/cubres/Documents/Clauding/erdos-hunt
    python3 -S p644_agent_audit_johnson_cofinal_check.py

The checker uses the alternative Eberlein formula, reconstructs every spectral and cofinal-layer coefficient, and verifies the three saved rational distributions. It checks all k+1 spectral inequalities, all T+1 cofinal layers, the permitted spectrum, complement symmetry, endpoint values, and distance-valency upper bounds. Its fresh replay passed.

Data files:

    logs/astra_agent_audit_johnson_cofinal_20_15_7.json
    logs/astra_agent_audit_johnson_cofinal_40_30_13.json
    logs/astra_agent_audit_johnson_cofinal_40_31_13.json
    logs/astra_agent_audit_johnson_cofinal_80_60_25.json
    logs/astra_agent_audit_johnson_cofinal_check.json

## Why cardinality alone was insufficient

The root supplied a simple asymptotic obstruction before this strengthened screen. The union of Johnson balls of radius floor(M/2) around complementary centers has only near or far intersection sizes in the permitted spectrum. Its size is

    2 Σ_{i=0}^{floor(M/2)} binom(k,i)².

For M/k≥5/16 its exponential rate is already larger than the cofinality cardinality lower bound at T/k=3/4. Thus comparing a spectral cardinality upper bound against that single lower bound cannot yield a contradiction in this range. The full cofinal-layer constraints address that particular omission, but the exact k=40 certificates show that they still leave a relaxation gap at the tested parameters.

The next mathematically distinct ingredient would need conditional information involving more than one fixed actual edge, such as joint intersection distributions or an explicit replacement relation. No large semidefinite computation is justified by the present screen, and none was launched.
