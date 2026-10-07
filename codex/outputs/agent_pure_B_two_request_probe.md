# Bounded two-request probe of the pure-B rank-escape witness

**Outcome: no target-budget allocation found.** Three retained four-row
choices were tested with arbitrary splitting among all four request codes.
This is numerical negative evidence for those three allocation models,
not an exact obstruction or a proof of optimality. No new target-scale
theorem is asserted.

The tested witness is exactly the support in
`outputs/agent_shared_witness_incidence.md`, including the finite constants
in the class sizes. The discovery scale is `b=1000`, and all masses below
are divided by `b`. The endpoint target is at most `110.999`, corresponding
to an actual endpoint count at most `111b-1`. The desired request budget
is `3(144b+1)/4`, or `108.00075` in these units.

| Retained witness rows | Reported best budget | Reported dual bound | Status |
|---|---:|---:|---|
| 2,3,5,6 | 109.001 | 109.001 | Numerical optimum |
| 2,4,5,6 | 109.001 | 109.001 | Numerical optimum |
| 1,2,3,5 | 109.000 | 109.000 | Numerical optimum |

All three solves terminated normally in under one second each, within
the authorized 60-second limits. The rows have empty common intersection
in each tested projection. Thus points outside their union cannot become
endpoints through an old common-point partner, and omitting outside points
from these request allocation models is justified.

For each old membership mask `s`, the model distributes its full mass
among codes `q=0,1,2,3`, meaning neither request, first only, second only,
and both. Potential residual partners have old-mask union `15` and
disjoint request codes. Binary support flags have only the constraint
`mass <= cell_capacity * support_flag`; **there is no minimum positive
mass and no fixed positive-cell cutoff**. Binary endpoint flags and
linearized endpoint masses bound the worst-case residual endpoint count.
The numerical model does not impose the ranks of the response edges.

The strict endpoint reduction of one actual point is an output target,
not an occupancy threshold. No numerical infeasibility or reported lower
bound has been promoted to a mathematical impossibility claim. The
three four-row choices do not exhaust all choices or prove an orbit
reduction for the asymmetric incidence-loss profile.

Reproduce with:

```
python3 work/p644_pure_B_two_request_discover.py --old 2356 --time 60
python3 work/p644_pure_B_two_request_discover.py --old 2456 --time 60
python3 work/p644_pure_B_two_request_discover.py --old 1235 --time 60
```

Detailed solver outputs, including discovered allocations, are preserved
in `outputs/agent_pure_B_two_request_2356_1000.json`,
`outputs/agent_pure_B_two_request_2456_1000.json`, and
`outputs/agent_pure_B_two_request_1235_1000.json`.

The bounded probe is complete; no further search is running.
