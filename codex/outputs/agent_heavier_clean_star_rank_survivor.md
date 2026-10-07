# Rank-aware two-request survivor for the heavier clean profile

## Exact outcome

For every even integer `b>=2`, there is an explicit eight-row family on
`259b` points in which every row has size `146b`, every at most seven rows
are two-pierceable, and the global minimum six-row endpoint/pair potential
is `(111b,3669b^2)`. Its last two rows avoid requests of sizes `108b` and
`109.5b`, respectively. Thus those two fixed requests remain compatible
with all the requested finite rank, seven-row, and six-row conditions.

The finite family's transversal number is exactly three. It is **not** a
high-transversal extension and does not disprove the conjectured bound or
exclude a different adaptive strategy.

## Construction

Use the Fano lines on `{0,...,6}` defined by
`(i+1) xor (j+1) xor (k+1)=0`. The six original rows are `W1,...,W6`.
For a line `L` not containing 0, a clean class `A_L` of `37b` points is
contained in exactly the rows whose labels lie outside `L`. For a line
containing 0, use a base class `B_L` of `33b` points with the same
memberships, and for each `h` outside `L` a defect class `d_Lh` of `b`
points contained in exactly the rows outside `L union {h}`.

Project onto rows `[W2,W4,W5,W6]`, with `W2` corresponding to the low bit.
Let `D1` be the union of four-row masks `{1,2,3,10,12,13,14}`. Its size is
`108b`. Let `D2^0` be the union of masks `{6,9,11,13}`. Its size is `110b`.
Choose `Z` of size `b/2` in `A135` and set `D2=D2^0 minus Z`, of size
`109.5b`.

Inside the clean class `A245`, choose nested sets
`R3 subset R3.5`, with sizes `3b` and `3.5b`. If `V` is the original
ground set, take the actual responses

```
G = V minus (D1 union d0345 union d0346 union R3),
H = V minus (D2 union R3.5).
```

The first complement has size `151b`, from which exactly `5b` is removed;
the second complement has size `149.5b`, from which exactly `3.5b` is
removed. Consequently `|G|=|H|=146b`. Neither response uses outside points.
The two additional defect deletions in `G` remove the pairs piercing all
eight rows without destroying any seven-row piercing pair.

## Exact verification [C]

```sh
python3 -S work/p644_heavier_clean_star_rank_survivor_check.py
```

The standard-library checker uses rational cell masses and integer incidence
masks. It verifies all row sizes and request avoidances, all 28 six-row
potentials, and all eight seven-row conditions. The only six-row endpoint
minimum tie is the original six witnesses, whose pair count is exactly
`3669b^2`. It records a piercing pair for each seven-row subfamily and a
three-point transversal for the entire family; it verifies that no pair
hits all eight rows. There is no numerical optimization and no minimum
positive-cell cutoff.

Certificate:
`outputs/agent_heavier_clean_star_rank_survivor_certificate.json`.

This task makes no claim that a rank-aware search over every request or
response has failed. It closes one concrete fixed-request branch by a
scalable exact survivor.
