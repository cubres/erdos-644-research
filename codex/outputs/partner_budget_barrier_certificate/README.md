# A precise limit of the one-round partner-box test

Proposition 7.78 in the research note gives a three-part family with continuous coefficient 39/50 that survives all 42 cheap-partner necessary tests at budget 3/4. The family itself has an explicitly certified bad two-type tuple. This is a method obstruction, not a counterexample to Erdos Problem 644.

```sh
python3 -B -S p644_partner_budget_barrier_check.py
```

The standard-library replay reconstructs all 42 LP systems, verifies 31 rational infeasibility certificates and 11 coordinate upper bounds, checks the positive capacity constructions, and checks the actual bad pair. The full hand transversal calculation and explanation of the test are in section 7.78 of the research note.
