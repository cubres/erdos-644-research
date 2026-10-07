# Exact fixed-menu probe after the full-S inside-union pivot

**Outcome [C]: none of the 35 tested deficit compositions is closed by
the existing two-request table at budget109.5b and residual target<111b.**
This is an exact limitation of the specified finite menu at the tested
parameter points. It is not a claim that arbitrary request allocations,
other pivots, or the desired theorem fail.

## Actual response branch

Start with the focused clean profile a=33b,c=37b,k=146b. The old four
noneligible membership types, in deficit order, are

    235,246,145,136.

Assume the response G contains both complete selected defect classes123
and124, has no outside points, and misses d_i points from the four A
classes. Its rank condition is exactly

    d_1+d_2+d_3+d_4=4b.

Replace row1 by G. The new tuple has active noneligible host146b and
endpoint count113b, with eligible group sizes38b,38b,37b. These are
actual membership masks, not an assumed type closure of the family.
The parent’s absorption correction is used: selected type123 belongs
to new cycle1235, and selected type124 belongs to new cycle1246. There
are no exceptional support points outside the Fano containing classes.

The probe sets b=1 and tests every nonnegative integer composition of4
into the four deficits: 35 points in the continuous parameter simplex.
At each point it tests all360 ordered selections of four distinct rows
from the new six-tuple. The order specifies the bit positions of the
fixed table; thus row permutations are included.

Each projection is tested twice:

1. with its exact actual membership masks;
2. after completing noneligible incidences to the containing stars
   145,136,234,256, with host masses37,37,35,37.

Completing those incidences is a sound upper model for residual
endpoints: it can add candidate piercing pairs, never remove an actual
candidate. It does not alter the eligible groups or their actual weights.

## The exact menu tested

The baseline first request includes masks1,2,3,10,12,13,14; the second
includes6,9,11,13. A chosen subpart of mask9 is added to the first
request, and a chosen subpart of mask12 is added to the second.
Projections containing unsupported positive masks4,7,15 are excluded,
as required for this particular table.

For each supported projection, compute the exact baseline costs d1,d2.
If both are at most T=219/2, use the largest permitted donors

    e9=min(m9,T-d1), e12=min(m12,T-d2).

Increasing either donor only adds a request membership bit; it cannot
create a residual pair. Therefore these maximum donors minimize the
residual endpoint count within the specified table at that projection.
The checker computes the exact residual endpoint support using only
positive pieces and the conditions

    old_mask_i union old_mask_j = 15,
    request_code_i intersect request_code_j = empty.

It does not merely use the generic upper formula when zero pieces could
remove extra endpoints. Fractions allow half-unit donors; consequently
the test even permits these fractional allocations at b=1. Integer
realizations follow after an even scaling. There is no solver, rounding
tolerance, or positive-mass cutoff.

## Results

For actual masks,31 compositions have no budget-legal table ordering.
The remaining four compositions,

    (0,0,1,3), (0,0,3,1), (1,3,0,0), (3,1,0,0),

each admit one budget-legal ordering, whose minimum residual is227/2
(113.5), above111.

For containing-star masks, every composition admits a legal ordering.
The best residual is113 at34 points. At(2,2,0,0), the best residual is
225/2 (112.5), still above111. Thus all35 points are uncovered by the
union of these actual-mask and containing-star fixed menus.

No continuous simplex covering attempt was made: these35 points already
prevent a covering of the whole simplex by this menu. No conclusion
about the rest of the simplex or a larger menu is needed or asserted.

## Reproduction

```
python3 -S work/p644_pivot_fixed_menu_check.py
```

The run completed normally. Full exact per-point data, supported and
legal ordering counts, and best table allocations are preserved in
`outputs/agent_pivot_fixed_menu_results.json`.

No process remains running and no main-note edit was made.
