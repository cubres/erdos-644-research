# Current: read work/CONTINUE_TWO_INTERVALS.md first.

# Current: read work/CONTINUE_BELOW_6_7.md, then work/CONTINUE_6_7.md.

# Current: read work/CONTINUE_6_7.md first. Historical checkpoints below.

# Superseded: read work/CONTINUE_086.md first for the general 43/50 and conditional 5/6 theorems

The following block is historical.

# Earlier authoritative continuation: c7 <= 173/200 = 0.865

This is progress, not goal completion. The user requires pursuit of the general3/4problem and concrete obstructions before stopping. Credible routes remain. No publication, notebooks, subagents, or memory updates.

VERIFIED GENERAL THEOREM7.28:
For every integer r>=1000, f(r,7)<=ceil(173r/200)+10, hencec7<=.865. See note_644.md Sections7.28-7.30. Independent p644_astra_global_bound_check.py passes exact38slab/11940node certificate logs/astra_spectrum_response_choice_173_200_23_50.json, using51statictemplates andnewadaptivelemmas. It also replays old.87and.87475checkpoints. Explicituniformintegerrounding<=9points perstaticrequest; allnewhandlemmasintegral.
Global proof: beta=.865,h=.46,low=.215. Cert excludespairinterval[.27,.46]. Capone traceath=.46, other2-beta-q-h, thenuseLemma7.18withm.27 toextenddown to.215. NEWLemma7.27extendsup to.5 usingpartialpaircore whenneeded. Once[.215,.5]forbidden, choosecaps.5 and1.5-beta-q forq in[.135,.215], givingalltriplepairs<=.215 andsmalltriplebudget.81. Thenallpairintersections<.135or>.5; invokeTheorem7.19 tau<=ceil31r/36+2. K=ceilbetar+10 dominates.

NEW HAND LEMMAS (allwritteninfull):
- Lemma7.26response-choice: forgoodtriple X=EFsizex,Y=EGsizey,Z=FGsizez, requireT>=max(S,r-x+z,r-y+z,r-x+y/2,r-y+x/2,(r+2x+2y+z)/3). FirstHavoidscoreXYZ. LetA=FH,B=GH,C=EH. Ifb<=T-x, requestX+B, thenYinbothremaining andZ+C+splitA. Symmetricifa<=T-y. Otherwise splitBoffT-x andAoffT-y, finalrequestscoreXYZ+C+remainders; costs<=T bylastinequality. r800,(308,308,43),T692 all3branches PROVER WINS LEGAL via p644_response_choice.py, logs/astra_response_choice.json.
- Lemma7.27gapupperextension forbeta.865,low.215,h.46: initialpairx in[h,.5], balancedthirdgivesy,z<low. T=ceilbetar+4.
  IfS=x+y+z<=T, avoidcoreplusE,Fprivatecutsforcingnewtraces<=floorhr, hence<lowr. Cuts p=(r-x-y-floorhr)+,t=(r-x-z-floorhr)+, costC=x+max(y,r-x-floorhr)+max(z,r-x-floorhr)<=T, padGprivate. HtraceG b<=r-T+x+p+t; splitBinto2requestswithX, finalrequestY+Z+smallHtraces. Boundr+3x+p+t<=2.58r+2, four smallparts<.86r, enough.
  IfS>T, avoidX,Y andZ0subsetZsizeT-x-y. Q=ZcapHsizeq<=S-T, A=FH\Q,B=GH\Q,C=EH. Pairgap forcesa+q<lowr,c<lowr sincebothpairtraces<=r-T+lowr<hr. b<=r-y-z. Finalbases: X+Q+Bhalf eachtwice, Y+Z+A+C. IncludeQinall3, distributeD=E\(X+Y+C) acrossremainingcapacities. Totalbase+D=r+x+z+2q+a+b <=2r+2x+z+lowr-T <=(3+2low-beta)r-4<3T. Individualbaseboundsalso<T. KillsmatchingpairsplusstarQxE. p644_triple_cell_script.py at r1000,(500,200,180),T869 PROVER WINS LEGAL, includesDdistribution.
- Lemma7.29NEWunconditional17/20atoldstaticobstruction: T<=r andT>=max((r+S)/2,r-x+abs(y-z),r/3+x). HavoidcoreXYZ plusGprivatep=max(0,r-2(T-x)-y-z), requestsize<=T. b=GH<=2(T-x), a<=r-x-z,c<=r-x-y. Ifb<=T-x, requestthreewholematchingpairsX+B,Y+A,Z+C. Else splitBintwo withX, remainingrequestY+Z+A+C hascost<r-T+S<=T. Exactlyintegral. At(.5,.1,.1) T=.85 WITHOUTGLOBALGAP. p644_dominant_pair.py r1000T850 bothbranchesverified. This is earlier adaptivity, outside the static/last-stepobstruction.
- Lemma7.30largestsmallm: ifallpairintersections<=m or>r/2, replaceLemma7.26lastcondition byT>=m+max(x,y). Bothhardresponsesa>T-y,b>T-xwouldbe>m, henceboth>r/2, impossible sincea+b<=r. First2cases suffice. Takingm=maxintersection<=r/2 isgeneral. For m>=1-beta, balancedthirdtraces <=min(m,(2-beta-m)/2).

NEW TOOLING/FRONTIER:
- p644_matching_three.py completely enumerates18antichains of3requestlabels and5832templatesfor3matchingcomponents; exactdualarrangement10vertices. Numericalmaxresponseprobesledtohandlemmas, notnewtheoremsalone.
- p644_static_extend.py adds2newexactMILPwitnesses+permutations to51oldtemplates ->63,1110exactbudgetforms, logs/astra_static_template_facets_v2.json. General.865proofusesoriginal51; expanded63areonlyinfrontierresearch.
- p644_spectrum_expanded.py atbeta.862 and31/36stillfailsnearq.379and.375respectively despiteexpandedstaticpool. Noimpossibilityclaim.
- p644_maxsmall_cover.py usesm=maxpair<=.5, three-triplecapsmin(m,(2-beta-m)/2), expanded63static+alladaptiveincluding7.30and7.29. Atbeta31/36coversmthrough~.4444thenfails at EXACTpoint(91071/204800,310031/921600,10001/51200). This pointisinsideactualbalanced-domain, notjustboxenlargement; itsS>31/36. Finitepoolminimum705471/819200>31/36. Data logs/astra_maxsmall_dominant_31_36.json. Independentp644_astra_frontier_check.pyreconstructs63staticand79totalregionsandpasses. This is a finite-menuhole only, notfullstaticoradaptiveoptimality.
- A numericalstaticoptimizeratnearby(.445,.336,.196)yieldsexactupperbudget689/800=.86125, flagsnumericoptimal butNOEXACTLOWERBOUND. Data logs/astra_static_maxsmall_hole.json. Primarynextissue: partial-core witha largertriplecell andonlytheweakerlargest-small-mgap, ratherthanthestronggapofLemma7.27. Anotherroute is general3requestgraphwithastarQxEandmatchingpairs, optimizinglabels/adaptation afterH.

DELIVERABLES:
outputs/note_644.md andVERIFICATION.md nowcurrenttoSections7.32. ZIP89contentfiles plusSHA256manifest,484185bytes. Extractedunderwork/bundle_replay_4. All8independentcheckersfreshreplayed (global,frontier,structuredcover,pocket,twotype,obstruction,static,staticobstruction); noexternalreview.
Allresearchjobsfromthiscontinuationfinished; no livecomputations torestart. Originalbackgroundprocessesleftuntouched. Earlierblocksbelowarehistoricalwhereinconsistent.

---

Final packaging: outputs/note_644.md and outputs/VERIFICATION.md current; ZIP68contentfiles plusSHA256manifest. All7independentcheckers passed fromwork/bundle_replay_3; last packaging update only refreshednote andadded completed triangularinterval discoverylog, thenrecheckedallhashes. No live job handles fromthiscontinuation remain.

# Latest research state: general coefficient 0.87 proved in the working note

Read this block before the historical checkpoint below. The active goal is NOT complete: the full 3/4 problem remains open and credible routes remain.

Completed this continuation:
- Theorem 7.24: for every r>=1000, f(r,7)<=ceil(87r/100)+10, hence c7<=0.87<7/8. Complete hand proof and exact case certificate in note_644.md Sections 7.20-7.26. Includes disjoint-edge families. No external review/publication/priority claim.
- Independent standard-library checker p644_astra_global_bound_check.py reconstructs all static budgets and validates original 0.87475 cover (6206 nodes), strengthened 0.87 cover (13904 nodes in44slabs), all global constants, and explicit integer rounding. Data logs/astra_spectrum_unbalanced_87_100_19_40.json. All51templates have <=15labels across6parts, so rounding costs<=9 extra points. No divisibility restrictions.
- Static budget exact reconstruction: complete label-price hyperplane arrangement on simplex of four request weights, dual max is max906affineforms across51templates. Checker has independent rational Gaussian implementation; discovery p644_static_dual.py uses integer determinants.
- Lemma7.18: small good triple maxintersection m<=r/2 closes at ceil(max((3r+m)/4,(2r+2m)/3)).
- Theorem7.19: pair gap <=7r/36 or>r/2 implies tau<=ceil31r/36+2. Choose LARGEST small pair m, balance third response. If newpairs small use7.18; otherwise large a>r/2 and y=m,z<=m. Ifm<=r/12 apply adaptive7.15; else fourthedge avoids allpaircells andFprivatepadding; itsanchortraces<=m, four triplecells vanish; splitlargeoppositepairB and killthreecomplementpairs by3requests.
- Lemma7.20: first response avoids allpaircells and balances F,G cuts; three final requests split partnertraces. Sufficient budget max(2max(x,y)+z,(r+2(x+y)+3z)/3,(2r+2(x+y)+2max(x,y)+3z)/5), with+1 integral. p644_early_adaptive.py verifies r100,(38,38,2),T87.
- Lemma7.23 strengthens by UNBALANCED firstcut. Conditions s+z<=T; r+3x+y+2z<=3T andmirror; 2r+3s+3z<=5T; r+2s+3z<=3T. Exactly integral. p644_unbalanced_adaptive.py verifies r270,(105,100,5),T234 PROVER WINS LEGAL. This breaks old finitepoolhole at(7/18,10/27,1/54), whose oldbudget47/54 drops to13/15.
- Global proof atbeta.87: exactexclude q in[.27,.475]; usecapsu=.475,v=2-beta-q-u toextenddown to.18; usebalancedthird+privatecutsforcinganchortraces<=.475 toextendup to.5; now pairgap<.18 or>.5, useTheorem7.19. Rounding allwritten explicitly, K=ceilbetar+10.
- Historical first coefficient3499/4000 remainsvalid (Theorem7.22) but0.87isstronger. Do not revive old statements saying no general improvement.

New credible route being investigated:
- p644_interval_closure.py certifies local boxes after subtracting previously excluded pairintervals, rather than insisting every first-stage box be covered without global information. Version2 atbeta.865 excluded[.215,.365] and[.405,.46] in41steps; record logs/astra_interval_closure_173_200.json. It is discovery only; independent stage-order replay and global finish required before claimingnewbound.
- NEW HAND LEMMA7.25: triangular finalallocation. WithS=x+y+z, sufficient T<=r and r+2S<=3T and S+sum_w max(0,r-2T+2w)<=T. FirstH avoidscore plusprivatecuts on ALL3anchors; Ecut lower x+y+max(0,r-2T+2z), Fcut x+z+max(0,r-2T+2y), Gcut y+z+max(0,r-2T+2x), sumcutsT+S. Finalrequestbases X+Y,X+Z,Y+Z; partnertracesB split1,2;A split1,3;C split2,3. Hall/flow conditions follow. Exactlyintegral. Nine affinebudgetforms from8subsetsJ plus(r+2S)/3. Added triangular_region() to p644_case_cover.py.
- p644_interval_closure.py nowversion3includestriangularregion(index57after51static+3balanced+3unbalanced). The beta.865 run in execsession41418 completed: same41steps and sameexcludedintervals[.215,.365] and[.405,.46], so the triangular lemma did not enlarge this particular coarse closure. Output logs/astra_interval_triangular_173_200.json. No stronger general coefficient claimed yet. All known research jobs launched in this continuation are complete.
- p644_spectrum_fast.py stillversion2 (withouttriangularlemma); usesfloatingpointrankingbutexactFractionleafchecks; independentreplaynecessary. Its optional facet-aligned splits were less effective and aredisabled. Defaultmidpointdepth70. Old0.87midpointfailurewasNOTimpossibility; tighterlemmafixedit. Lowerbetas.865,.867,.868gaveuncoveredpoints/LIMITlogs, notmethodlowerbounds.

No subagents used. No notebooks touched. No externalmessages or publication. Original backgroundprocesses preserved. Outputs are a review checkpoint, not a stopping declaration.

---

# Historical checkpoint below (superseded where inconsistent)

# Active research continuation — 19 September 2026

## Latest continuation: read this before the older checkpoint below

The research note is now current through §§7.14–7.19, and its opening summary was rewritten to remove stale inherited overclaims. The general problem is still unresolved and the active goal has not met its stopping condition.

New completed work:
- `p644_strategy_budget.py`: exact-checked conservative union-budget bounds, with requested pick sizes checked for nonnegativity before imposing min constraints. All21 FKW budgets at14/16 legal. Negative picks and overlapping avoids have regression tests. Same integer/dyadic matrix qualification as the support verifier.
- Sharp four-static-request obstruction at pair proportions(1/2,1/10,1/10): complete166-antichain enumeration,151341 compatible templates after swappingY/Z,8312 request-permutation orbits,77 exact duals; minimum budget7/8. `p644_static_obstruction.py`, certificate `logs/astra_static_obstruction.json`, standalone `python3 -S p644_astra_static_obstruction_check.py` passes.
- Lemma7.14: with tau>T>=ceil(r/2), choose global minimum pair intersectionm<=r-T and balanced third edge, obtaining two new intersections <=r-floor((T+m)/2). Every subsequent pair >=m. Nine S8 scripts at r100,T87,(50,10,10) with all-pair lower10 still survive; rational witnesses in `logs/astra_minimum_pair_probes.json`.
- Lemma7.15 generalizes FKWCase4: X=E∩G size x,Y=E∩F size y,Z=F∩G size z; suppose any edge avoidingX+Y+Z has traces inE,G <=m. Withq=T-x require q>=y+z,y+m,z+m andr<=4q-y-z-2m. PartitionF with capacities(q,q,q-y-m,q-z-m); firstresponseH4avoidsX+B1, secondX+B2, thirdX+B3+Y+(H4∩G), fourthX+B4+Z+(H4∩E). Allfour legal and killallpairs. Global pair gap<=m or>=h plusr-x-y<h,r-x-z<h supplies trace assumption. At(.5,.1,.1),m=.1,h=.5 givesT=.85. `p644_astra_gap_script.py` at r100,T85 verifiedPROVER WINS LEGAL.
- Lemma7.16 and `p644_core_request.py`: after <=6edges with emptycommonintersection, K=unionofoccupiedcells with partner coveringallrows. AvoidingK killsall2piercers. Onfixedminpickbranch maximal-support configurations dense inpolyhedron, so maximumKmass anLP. Fullcommoncell requires separateONE_POINT_PREFIX rejection: acommonpoint plusanypointofnextedge always2pierces, includingoutsidepoints. Tests: FKWprefix core14 atT14, core16 atT13; gap prefix core85 atT85; commonpointregression rejected.
- Lemma7.17 now PROVES last-step-only adaptivity cannot improve static budget belowr. Given3staticavoidsets, K0=endpoints of candidatepairs notcontainedinanyDi. Select proportionrho=min(1,r/|K0|) fromeachpositiveK0 Venn/avoid-labelclass, obtainingS; respondHi withS\Di plusfreshoutsidefiller. EverypointinS haspartnerinS, soactual6edgecore >=min(r,|K0|). ThusT<r allows anadaptivefinalrequest onlyifK0<=T, inwhichcaseK0 itself isstaticfinalrequest. Combineswithstaticexactobstruction: cannotbeat7/8 at(.5,.1,.1) whenfirst3requestsstatic. Earlieradaptivity, globalrestrictions, othertriple, orlongerscript required. This is handproof, not numericalbarrier.
- Discovery beforethatlemma: `p644_core_static_search.py` tested2000 three-static allocations at r100,T87; bestcoreupper89. Logretained but makesnooptimalityclaim. Do not repeat this dead route; lemma explainsfailure.

Latest deliverables have been repackaged with6standalonecheckers andnewlogs. Extracted underwork/bundle_replay_2; SHA256manifest verified. Original researchprocesses were left untouched.

Next credible routes: earlier-adaptive requests informed by global gaps; a complete pair-intersection case split combining locallemmas; two-convex-component TheoremP extension (extractingonehigh-taupair fails,but feasible mixed Fano-downset LP may stillwork). Generalnu2stillopen. Do not markgoalcomplete orclaimimprovedgeneralbound.


The user asks for sustained work on Erdős 644 and permits stopping only after concrete obstructions and a judgment that no credible near-term route remains. **That stopping condition has not been met. The goal remains active.** This is a verified checkpoint, not a claimed resolution or final abandonment. Do not mark the goal complete merely because this checkpoint is substantial.

## Sources and files

Working research directory: `/Users/cubres/Documents/Clauding/erdos-hunt`.
Updated `note_644.md` now contains §§7.1–7.13 with all proofs and corrections; `notes_644.md` has progress entries. Original files were backed up in this task's `work/inherited_snapshot_20260919/` before editing. The original `p644_nu2_cover_refine.py` process was left untouched; its slow inclusion-exclusion computation is superseded by our complete exact certificate.

User-facing checkpoint copies: `outputs/note_644.md`, `outputs/VERIFICATION.md`, `outputs/erdos644_astra_certificates.zip`. ZIP was extracted to `work/bundle_replay/erdos644_astra_checkpoint`, all SHA-256 hashes checked, and all five certificate checkers passed under `python3 -S` (no site packages).

## Completed mathematics

1. **sigma_2=11/20 in the continuous structured model**, with exact upper/lower certificates. Upper: 20 polygons, 84 rational vertex witnesses covering c-d<=9/20. Lower: F(d,c), d=1/4-e,c=7/10+e, all rational 0<e<=1/1000, all integral scales; 28 row-type multisets, 2036 proof nodes, 95 rational interval duals, 6127 maximal intersecting triple families covered (118 typed orbits needed for the hard 3s4t case). Pure stdlib replays: `p644_astra_certificate_check.py`, `p644_astra_pocket_check.py`. Explicit finite construction for every k divisible by20,k>=1000: traces k/4-1 and7k/10+1 plus anchors; tau=11k/20 exactly.
2. **Intersecting two-point-type theorem in any number of parts:** tau*>3r/4 implies a continuous bad seven-tuple. Two Fano-downset templates suffice after choosing type orientation at a coordinate forcing cross-intersection:
   M1(a,b)=max(a,a/4+3b/2), for1a6b rows;
   M5(a,b)=max(3a/2,5a/4+b/2,a/2+b), for5a2b rows.
   The dichotomy is certified by87 LP cases (25 exact gamma<=0 duals;62 infeasibility duals). Pure checker `p644_astra_two_types_check.py`. Suitable integral multiples are justified; do not overclaim all-large-scale rounding or union-of-two-convex-component results.
3. **Seven-edge good-triple lemma** (§7.9): good triple E,F,G, X=E∩G size x,Y=E∩F size y,Z=F∩G size z. If x+ceil(r/2)<=T and y,z<=T-r+x, partitionF intohalves B1⊇Y,B2⊇Z; requestavoiding X+B1,X+B2,(E-X)+Z,(G-X)+Y. At r16,T13,(x,y,z)=(5,2,2), inherited8-edgewin reduces tothis7-edgeproof by omitting unusedA4.
4. **Static four-request lemma** (§7.13) at pair intersections(.5,.25,.25)r hasbudget6r/7. With sixparts X=12,Y=13,Z=23,U=1,V=2,W=3, split X1=2r/7,X2=3r/14 andW1=W2=r/14,W3=5r/14. Avoid X1+Y+V+W1; X1+Z+U+W2; X2+Y+Z+W1+W2; X1+X2+W3. Nearby budgets =19r/14-x+y-z,19r/14-x-y+z,x+y+z-r/7,6r/7+x-y-z. Hence a closed radius3r/700 box around(.5,.25,.25) iscovered atT=.87r. This is local only.

## Exact obstructions and audit corrections

- Standard shifts can lower tau and destroy(7,2) even for intersecting4-uniformfamilies. Explicit9-edgeexample and deletionpiercertable in§7.2; purechecker `p644_astra_obstruction_check.py`.
- Random exponentially sparse subfamilies of K_N^k atN≈7k/4 have tau≈3k/4 buteveryexacttype-closedsubfamily onboundedlymanyparts has tau≤numberparts. This defeats unconditional exacttype-closedextraction (§7.3).
- Addingonecommonpoint toFanoedges makes them1-pierceable despiteo(k)perturbation; approximateFano structure isnot enough (§7.4).
- Intersectingnonconvextwo-typeexample: capacities(40,139,99)m, edge types(20,0,80)m and(0,80,20)m. tau=78m+2; noexactoro(k)-approximateFano tuple, but explicitintegerbadtuple exists. Fano-downset templates are needed instead (§7.7).
- Refining its parts intochunks≤k/10 givesunionoftwoconvexpolytopes withtau≈.78k buteachfixedtwo-type subfamily has tau*≤.2k. Thus selectingonepointfromeachcomponent doesnotreduce the general two-convex-component extension (§7.11).
- Correcttwo-typecoefficient ismin(1-d,1+d-c,c). Finitegapformula tau=r-maxgap+2. Prior omissionofendpointgaps repaired.
- Attained3/4 lowercoefficient doesnotkillbudgetproofs. A cross-piercing.6example cannotobstructa.75bound. Finitegrids donotproveforallalpha.
- Some inherited integer/scaled smallcaseclaims remainunrerun and arelabelledas such; don'tpromotethemtoindependentlycertified facts.

## New strategy verifier: useful for T2/T3

`p644_strategy_lp.py` is a strict-support verifier. On each fixed min-pick branch, feasible atom vectors form a convex polyhedron; supports unite by averaging. Local2pierceability andintersectingness aremonotonein support. LP support discovery therefore replaces occupancy MILPs. Every used primal vector anddual ischecked byFraction arithmetic; failed reconstruction returnsUNKNOWN. Request legality remains separate.

The inherited verifier's continuous eps=1e-3 is actually unsound: forcinga7-edgecommoncellmass1e-6, all2..6cellszero, andprivatecells1-1e-6 yields aglobally1-pierceablefamily, butoldverifierreportsPROVERWINS. Newverifier returns anexactsurvivor. Recorded in `logs/astra_strategy_lp_checks.json`.

Validation: all21FKWtriples atbudget14/16 win evenwith `intersecting=False` (avoidsvacuitywhena23=0), about14seconds total. First-seven-truncation of8-edgeexample surviveswithrationalwitness.24clustered-menu scripts at3cells allsurvive (13seconds). SameoldS8variantA at r16,(x,y,z)=(5,2,2),(6,2,2),(7,2,2):39,21,6eligibleintegerparameterchoices; only x5,beta0=0,beta1=8wins. Others exactsurvivors. Standalone reproduction `p644_astra_s8_sweep.py` was created butnotrerun afteritscreation; itsloop is the tested loop. FifteenS8probes nearx=.5atT=.87r allsurvive, in `logs/astra_beta87_s8_probes.json`.

Important implementation qualification: exact checks certifythe rationalmatrix reconstructedfromexistingfloatbuilder entries. Verifiedtests useinteger/dyadicdata. Arbitrarynon-dyadicsymboliccoefficients needexplicitexacthandling.

## Concrete next routes

1. Add an exact LP request-budget checker using each prefix, final_picks, andthe union (not sum) ofavoidpredicates. For a branch whose maximal support survives, local-property configurations aredense initsmasspolyhedron (mix anypointwith amaxsupportpoint), so linearobjective supremum equalsordinaryLPsupremum. Could conservativelyboundallgeometricbranches evenwithoutlocalproperty. Existingstrategy2.check_budget sums overlappingavoids (safeupperbound butneedlesslyweak).
2. Try new whole-cell/adaptive T2/T3 scripts withthenewverifier; do notblindlyrepeatoldpickmenus already certifiedsurviving. Moreprobesremainuseful because all7subfamiliescanbechecked on maximal supportfast.
3. Improveoutergoodtriple selection instead ofcoveringall680oldgridcells. Withtau>T, chooseaminimum-intersectionpair ofsizem≤r-T andathirdedgeavoiding theirintersection plus abalanced amountfromtheirprivateparts. Then bothnewintersections≤r-(T+m)/2; forr16,T13,largest≤9.5-m/2, soverylargeclusteredcells10..16 areunnecessary forthisouterchoice. Globalminimumalsoforces everynewpairintersection≥m. Theold680grid startsat1 andomitsnormalizedsmallpositiveintersections(0,1), anadditionalcoveragegap.
4. FKWCase4usesa globalabsenceofmediumintersections, notonlygoodtriplemasses. Thiscanboundnewprobe∩anchor bym afteravoidinglargeW. Generalizingits4-partpartition yieldsbudgetconditionm≤3T-(5/2)r, so thisparticularbalancedCase4can'treach13/16 evenatm0 (needsatleast5/6). This is anobstructiontothatformula, notalladaptivestrategies. Mightcombinewithnewstaticlemmasforamodestimprovementbelow7/8.
5. Staticfour-request optimization is `p644_static_four.py`; labels may beempty(mask0), essentialwhena Vennpart hasnoneighbour ofpositivemass. Exactwitnesses, no certifiednumericoptimalitylowerbounds. Candidatepairgraphon6parts istriangleXYZ pluspendantsXW,YV,ZU. Testedbudgets: (.5,.25,.25)->6/7;(.5,.25,0)->5/6;(.5,.1,.1)->7/8;(.5625,.0625,.0625)->43/48;(.5,.375,.125)->7/8;(.4375,.25,.125)->41/48. Purechecker `p644_astra_static_check.py` passesall6.

Useful FME forone statictemplate: variables t=|X1|,p=|W1|,q=|W2|, with 0<=t<=x,p,q>=0,p+q<=r-y-z andthe4budgets. Eliminating t,p,q gives these lowerbounds onT (plusx>=0,y+z<=r): y+z; x; r-x-y+z; r-x+y-z; r/2+z; (r+y-z)/2; r/2+y; (r+x)/2; (r+x+2y)/3; (2r+x-y+z)/3; (2r+x+y-z)/3; (2r+2x+y-z)/4; (3r-x-y-z)/3; (3r+x+y+z)/5; (5r+3x-y-z)/7. These areexactFMEinequalitiesbutnotyetpackagedasacompletecover proof.

No subagents were used (notauthorized). No externalmessages/publication, no notebookmutations, andno memoryupdates were performed. Keep these boundaries.
