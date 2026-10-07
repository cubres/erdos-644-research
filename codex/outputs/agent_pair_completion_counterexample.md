# Pair-completion of a minimum six-edge piercing-pair count is false

Status: **hand proved**, with a small independent standard-library exact check. This is an obstruction to an unrestricted-to-paired minimum-Q reduction. It is not a counterexample to Problem 644, nor to a version of that reduction with an additional high-transversal hypothesis.

## Construction

Let a be an integer at least four. Take the sixteen even-parity binary words of length five as incidence types. Replace a word by the following number of distinct points with that type:

- the all-zero word: 3a−2 points;
- each word of Hamming weight two: one point;
- each word of Hamming weight four: a points.

For every coordinate i and bit b, let E_i^b be all points whose i-th coordinate is b. These ten edges form five complementary pairs.

The total ground size is

    n=(3a−2)+10+5a=8a+8.

For a fixed coordinate, its positive half contains four weight-two types and four weight-four types, hence has size

    k=4+4a=n/2.

Its negative half has the same size. Thus this is a complement-closed k-uniform family on 2k points.

## Property (9,2) and transversal number three

Consider any subfamily of at most nine of the ten half-edges. At some coordinate j, at most one of the two half-edges is selected. Choose two even words which agree in coordinate j and are opposite in each of the other four coordinates. If a half-edge at j is selected, let their common j-bit satisfy it. An even choice of the first word always exists, and flipping four bits preserves even parity, so the second word exists as well. These two points hit both half-edges at each other coordinate and hit any selected half-edge at j. Consequently the family has property (9,2), and in particular (7,2).

Two points could hit all ten half-edges only if their words were opposite in all five coordinates. Complementing an even word in five coordinates gives an odd word, which is absent. Thus tau≥3. The three words 00000,11110,00011 hit all ten half-edges: the first supplies every zero bit, and the other two together supply every one bit. All three have even parity and positive multiplicity. Therefore tau=3.

## Exact Q comparison

For any subfamily with empty common intersection, write Q for its number of unordered two-point transversals. Points having the same incidence word cannot pierce a subfamily containing a complementary edge pair, so contributions between two different words are the products of their multiplicities.

Coordinate permutation symmetry implies that every choice of three distinct complementary pairs has the same Q. Take the pairs at coordinates 1,2,3. Counting pairs of words according to their Hamming weights gives:

| Hamming weights of the two words | Number of unordered type pairs |
| --- | ---: |
| 0 and 4 | 2 |
| 2 and 2 | 6 |
| 2 and 4 | 8 |
| 4 and 4 | 0 |

The first three coordinates must be opposite. For the 0/4 case the weight-four word contains those three coordinates and one of the two others. For 2/2, the two words partition such a four-coordinate set into pairs, giving two choices of the fourth coordinate and three partitions. For 2/4, if the zero coordinate of the weight-four word is among the first three, there are two choices for the weight-two word, giving six; if it is among the other two, there is one choice, giving two more. This proves the table.

Hence

    Q_paired=2a(3a−2)+6+8a=6a²+4a+6.

Now instead take the six edges

    E_1^0, E_1^1, E_2^0, E_2^1, E_3^1, E_4^1.

They have empty common intersection. Their piercing pairs have the following counts:

| Hamming weights | Number of unordered type pairs |
| --- | ---: |
| 0 and 4 | 1 |
| 2 and 2 | 3 |
| 2 and 4 | 13 |
| 4 and 4 | 1 |

For a directly inspectable enumeration, use integer masks with coordinate 1 as the least significant bit. The corresponding type pairs are:

    0/4: (0,15)
    2/2: (3,12), (5,10), (6,9)
    2/4: (5,30), (6,29), (9,30), (10,29), (12,15),
         (12,23), (12,27), (15,20), (15,24), (17,30),
         (18,29), (20,27), (23,24)
    4/4: (29,30).

These pairs are exactly those with opposite bits at coordinates 1 and 2 and with at least one 1 at each of coordinates 3 and 4. Therefore

    Q_unpaired=a(3a−2)+3+13a+a²=4a²+11a+3.

A shorter calculation of the same unpaired count uses inclusion-exclusion. For only the two complementary pairs at coordinates 1,2, the four projection-class masses are 3a+1, a+3, a+3, 3a+1, so the piercing-pair count is

    Q_two_pairs=(3a+1)²+(a+3)²=10a²+12a+10.

Among these pairs, those missing E_3^1 have both third bits zero. Their first-two-coordinate projection masses are 3a−1,2,2,a+1, so their count is (3a−1)(a+1)+4=3a²+2a+3. The same count applies to pairs missing E_4^1. Pairs missing both have count 3a−1. Thus

    Q_unpaired=(10a²+12a+10)−2(3a²+2a+3)+(3a−1)
              =4a²+11a+3.

The difference is

    Q_paired−Q_unpaired=2a²−7a+3=(2a−1)(a−3)>0.

Thus the unrestricted minimum over six-edge tuples is strictly below every three-complement-pair value. Allowing repetitions does not save pair-completion: a repeated-pair tuple has fewer than three distinct complementary pairs and can be extended to three distinct pairs, which can only decrease Q.

At the smallest integer parameter used here, a=4, the construction has

    n=40, k=20, tau=3,
    Q_unpaired=111 < 118=Q_paired.

The independent exact enumeration additionally checks that 111 is the unrestricted minimum over all 210 six-edge subsets. Exact minimality is not needed for the counterexample: the single displayed value below every paired value already disproves the claim.

## Reproduction and scope

Run:

    cd /Users/cubres/Documents/Clauding/erdos-hunt
    python3 -S p644_agent_audit_pair_completion_check.py

The checker uses only Python's standard library. It checks every edge size, every nine-edge subset, tau=3, all 210 six-edge Q values, all ten choices of three distinct complement pairs, and the displayed type-pair counts. Its fresh output is `logs/astra_agent_audit_pair_completion_check.json`.

Discovery used `p644_agent_audit_pair_completion.py`: the unweighted even-parity code gives equality Q=16, while positive balanced perturbations expose the failure. The initial random discovery had k=224; the symmetric parameter family above replaces it by a hand proof at k=20.

This invalidates pair-completion under complement closure and (7,2), even with tau>2. It does not rule out a theorem conditioned on tau>(3/4+epsilon)k, nor a replacement invariant involving an additional potential beyond Q. In this family tau stays three as k grows.
