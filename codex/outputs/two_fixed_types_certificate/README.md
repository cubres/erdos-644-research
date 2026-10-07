# The 3/4 theorem for two fixed types

Theorem 7.71 in the adjacent research note removes the intersecting hypothesis from the earlier two-fixed-type result. It holds over any finite number of parts. A continuous transversal coefficient above 3/4 forces a bad seven-tuple. This remains a structured theorem, not a full solution for arbitrary set families.

Run both standard-library checks:

```sh
python3 -B -S p644_astra_two_types_check.py
python3 -B -S p644_disjoint_two_types_check.py
```

The first replays the earlier 87-case intersecting proof. The second independently reconstructs all 125 nonintersecting root cases, verifies 120 exact root duals, and checks a complete 107-node refinement with 101 rational leaf duals and six branching nodes. Three additional bad-tuple construction templates are verified directly from their supports and primal/dual capacity certificates. The large 42-function catalogue is not needed for this theorem's replay.

The hand proof is essential: it gives the transversal formula, the reduction to mixed-disjoint types, the four initial constructions and the finite coordinate-witness reduction. The checker does not claim to formalize the entire mathematical note. Rational witnesses scale to suitable integral multiples only.

Discovery scripts are included and require NumPy/SciPy. Their accepted conclusions are checked by the separate replay scripts. Nothing has been published; external mathematical review and priority checks remain outstanding.
