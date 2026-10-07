# Arbitrary types over three equal parts

Theorem 7.80: at rank r and part capacities (4r/5,4r/5,4r/5), every type-closed family of continuous transversal coefficient greater than 3r/4 has a bad seven-tuple. No convexity, intersectingness or grid restriction on actual types is assumed. This fixed-capacity theorem does not resolve arbitrary families.

Run these two independent standard-library checks from this directory:

```sh
python3 -B -S p644_continuous_type_cells_check.py logs/astra_continuous_type_cells/40_32_32_32_T30_fano_regions_parents
python3 -B -S p644_lrat_rup_check.py logs/astra_continuous_type_cells/40_32_32_32_T30_fano_regions_parents.cnf logs/astra_continuous_type_cells/40_32_32_32_T30_fano_regions_parents.lrat.gz
```

The first reconstructs every geometric condition and all 538035 clauses, including the exact positive construction certificates. The second checks 74164 derived clauses by exact unit propagation, with no SAT solver. The 42-function completeness theorem is not needed. The hand triangular-cover argument and Fano capacity lemma are in the accompanying research note. Nothing has been published.
