# A precise limitation of merely retuning the new three-gap proof

The new hand proof gives coefficient 6/7. Its existence does not by itself
justify a coefficient below 6/7 after changing the rational endpoints.
The following elementary calculation identifies one obstruction to that
particular retuning.

Suppose a proposed proof at normalized request budget beta has all three
of these features:

1. Its first excluded interval begins at a and is obtained from the usual
   two-edge cap request, with retained caps u,v satisfying
   u+v=2-beta-a at the left endpoint.
2. The proof of that first response box requires both u and v to be at
   most beta-1/2, so that every resulting trace satisfies the L31/L32
   half-plus-trace budget inequalities without another case split.
3. That first interval supplies the final upper-gap lower endpoint, with
   a<=beta/2, as needed when the finishing argument uses 2m<=beta for the
   largest small pair intersection m.

Then necessarily beta>=6/7. Indeed, conditions 1 and 2 give

    2-beta-a <= 2beta-1, hence a>=3-3beta.

Combining with condition 3 yields 3-3beta<=beta/2, or beta>=6/7.
Equality forces a=3/7 and u=v=5/14, exactly the endpoints in the new proof.

This is only an obstruction to preserving those three design choices.
A new branch for traces above beta-1/2, another gap-extension stage, or a
finisher that avoids the condition 2m<=beta could invalidate one of the
hypotheses and improve the coefficient. It is not a lower bound on f(k,7),
nor an impossibility theorem for the general avoidance-request method.
