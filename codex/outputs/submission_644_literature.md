# Erdős 644: literature, novelty, and journal fit

Checked 26 September 2026. This is a primary-source literature and policy review, not an independent proof audit of the proposed new theorem. No messages were sent and nothing was submitted or published.

## Assessment

**The published comparison bound located is \(f(k,7)\le\lceil7k/8\rceil\), due to Fon-Der-Flaass, Kostochka, and Woodall (1999). No later published improvement, including a \(6/7\) coefficient, was located in this search.** Consequently an independently correct unrestricted theorem \(f(k,7)\le6k/7+O(1)\) would improve that established bound. The responsible manuscript wording is “improving the bound of Fon-Der-Flaass, Kostochka, and Woodall,” rather than an unqualified claim to be the first improvement in 27 years. [FKW author-hosted paper](https://kostochk.web.illinois.edu/docs/2000/dm1999FlaWoo.pdf).

My venue judgment: **Discrete Mathematics is the natural initial target for a concise paper centered on this coefficient improvement**, because its scope explicitly includes hypergraphs and extremal set theory and it published the direct predecessor. **Electronic Journal of Combinatorics is also a plausible target** for a self-contained paper with a clear structural contribution and accessible verification material. Neither is a low-barrier outlet. This is a scope judgment, not an acceptance forecast. [DM official scope](https://shop.elsevier.com/journals/discrete-mathematics/0012-365X), [E-JC official scope](https://www.combinatorics.org/ojs/index.php/eljc/about/index).

The coefficient change is \(1/56\). Relative to the interval between the conjectured \(3/4\) and the published \(7/8\), it removes one seventh of that gap. This elementary comparison describes a definite partial advance; it does not resolve the conjecture. Correctness, a clean new mechanism, and proportionate claims should drive the submission.

## Direct mathematical sources

### FKW 1999 — benchmark verified from the paper

D. G. Fon-Der-Flaass, A. V. Kostochka, D. R. Woodall, *Transversals in uniform hypergraphs with property (7,2)*, Discrete Mathematics **207** (1999), 277–284, DOI [10.1016/S0012-365X(99)00114-4](https://doi.org/10.1016/S0012-365X(99)00114-4).

Theorem 2 produces at most seven edges with transversal number greater than two whenever \(\tau>\lceil7r/8\rceil\). Its proof starts with \(r=8k+s\), \(k\ge1\), so the verified comparison is for \(r\ge8\). Theorem 1 gives the odd-intersection construction with \(\tau=3m+1\) at uniformity \(4m\), initially for \(m\ge10\); its remark extends this to \(m\ge4\) and records failure at \(m=2\). [Full paper](https://kostochk.web.illinois.edu/docs/2000/dm1999FlaWoo.pdf).

### Attribution of the proof mechanism

The basic framework is inherited from FKW: a large transversal number guarantees an edge avoiding each small requested set; triples with empty common intersection are completed to a forbidden seven-edge family; intersection-size exclusions constrain subsequent responses. FKW's final case already uses a maximal small intersection. These ideas, and the general use of an intersection gap, should not be advertised as new. [FKW, Lemma 1 and Theorem 2](https://kostochk.web.illinois.edu/docs/2000/dm1999FlaWoo.pdf).

The present candidate's identifiable advance is **stronger local completion constructions and a combination of gap extensions that work with avoidance budget \(6k/7+O(1)\)**. In the current hand proof, three stages exclude the intervals \([3/7,10/21]\), \([4/21,5/14]\), and \([10/21,1/2]\) of normalized pair intersections. A stronger conditional finishing theorem then closes the remaining families. In particular, S0 supplies an integral allocation of private cells among four requests; the newer closing lemmas handle response configurations beyond the cited FKW construction. These statements describe the contents of the local proof files, not a separate priority determination for every subsidiary lemma.

The clearest positioning is therefore “we refine the avoidance method of FKW by …,” followed by the concrete new local lemma and the three-stage argument. Explain why the original parameter inequalities do not give the claimed coefficient, and then show exactly which replacement construction removes that obstruction. The existing lemma L18 is explicitly labeled an extracted FKW construction and should retain that attribution. The exact integer allocation refinement is useful supplementary structure; it should be stated as optimality for its specified construction, not optimality among every possible proof.

Local comparison sources read: `outputs/paper_push_six_sevenths_hand_proof.md`, `outputs/paper_push_six_sevenths_hand_dependencies.md`, and `outputs/submission_644_integer_refinement.md`. The first is an earlier \(+4\) presentation; the last records the current unrestricted \(+1\) bound and a sharper conditional finisher. The submission must use the latest consolidated finite statement, rather than copying the older header.

### Kostochka 2002 — different asymptotic regime

A. V. Kostochka, *Transversals in Uniform Hypergraphs with Property (p,2)*, Combinatorica **22** (2002), 275–285, DOI [10.1007/s004930200013](https://link.springer.com/article/10.1007/s004930200013).

The publisher's abstract explicitly separates the earlier \(p=7\) bounds from its new result for large \(p\) and much larger uniformity. The indexed text of the actual paper states a bound of the form \(1.3r/(\sqrt p-o(\sqrt p))\); its introduction repeats the earlier \(7/8\) estimate. This asymptotic statement cannot be specialized by discarding its error at the fixed value \(p=7\). [Publisher record](https://link.springer.com/article/10.1007/s004930200013), [indexed journal facsimile](https://electronicsandbooks.com/edt/manual/Magazine/C/Combinatorica/Volume22-Number2-April-2002/Transversals%20in%20Uniform%20Hypergraphs%20with%20Property%20.pdf).

**Access limitation:** the journal landing page was read, but its PDF redirects to the subscription preview. The public facsimile's title, abstract, introduction and theorem were available in indexed excerpts; fetching the complete file failed. Worse, the author's publication-list link `docs/2004/comb02.pdf` currently serves an unrelated 2010 Gyárfás–Sárközy–Szemerédi paper. That file was checked and excluded. Do not cite it as the 2002 full text. This review verifies the relevant stated scope, not every detail of that proof.

### Bucić–Korándi–Sudakov 2021 — full text checked

M. Bucić, D. Korándi, B. Sudakov, *Covering Graphs by Monochromatic Trees and Helly-Type Results for Hypergraphs*, Combinatorica **41** (2021), 319–352, DOI [10.1007/s00493-020-4292-9](https://doi.org/10.1007/s00493-020-4292-9); preprint [arXiv:1902.05055](https://arxiv.org/abs/1902.05055).

Section 1.4 defines \(h_r(p,\ell)\), corresponding here to \(f(k,7)=h_k(7,2)\). Their main uniformity-dependent regime takes \(\ell=r\). Theorem 5.3 does give a general upper bound, but assumes

\[
p\ge {r+t\choose t}^{1/\lfloor t/\ell\rfloor}\,2r\ell\log(r\ell).
\]

With \(\ell=2\), the right side is at least \(4r\log(2r)>7\) for \(r\ge2\). Thus this theorem does not apply at local parameter \(p=7\). Their general and partite results do not supply the sought coefficient improvement. References 13, 16, 17 and 32 identify the historical line. [Author-hosted final paper, Sections 1.4 and 5](https://people.math.ethz.ch/~sudakovb/covering-by-monochromatic-trees.pdf).

### Later citing papers checked for scope

| Source | Relevant scope and conclusion |
| --- | --- |
| D. Bradač and M. Bucić, *Covering random graphs with monochromatic trees*, Random Structures & Algorithms **62** (2023), DOI [10.1002/rsa.21120](https://onlinelibrary.wiley.com/doi/10.1002/rsa.21120); [author preprint, arXiv:2109.02569v3](https://arxiv.org/pdf/2109.02569) | Full introduction and definitions checked. The new parameter concerns partite hypergraphs with consistently intersecting chosen covers. These are additional structural assumptions, not a bound for arbitrary property-(7,2) families. |
| M. A. Henning, C. Löwenstein, A. Yeo, *The Tuza–Vestergaard Theorem*, SIAM J. Discrete Math. **37** (2023), 1275–1310, DOI [10.1137/22M1475508](https://epubs.siam.org/doi/10.1137/22M1475508) | Publisher abstract checked. This is a theorem for 3-regular, 6-uniform hypergraphs in terms of their number of vertices; it is a different extremal problem. |
| M. A. Henning and A. Yeo, *Transversals in regular uniform hypergraphs*, J. Graph Theory **105** (2024), 468–485, DOI [10.1002/jgt.23051](https://onlinelibrary.wiley.com/doi/10.1002/jgt.23051) | Publisher abstract and displayed bounds checked. Regularity assumptions and order-dependent bounds do not establish the unrestricted local-cover theorem. |
| M. A. Henning and A. Yeo, *Extensions and applications of the Tuza-Vestergaard theorem*, European J. Combin. **130** (2025), 104201, DOI [10.1016/j.ejc.2025.104201](https://www.sciencedirect.com/science/article/pii/S0195669825000897) | Publisher abstract checked. It extends the preceding fixed-6-uniform, bounded-degree theory and estimates \(\tau/(n+m)\). Its “Tuza constant \(c_6\)” is unrelated to our asymptotic coefficient \(c_7\). |

Erdős–Hajnal–Tuza's original local-to-global formulation expressly uses subsystems of **at most** the prescribed size. [1991 primary abstract](https://www.sciencedirect.com/science/article/pii/009731659190074Q). State that convention in the new paper. FKW's actual upper-bound theorem also has an at-most-seven witness, notwithstanding the exactly-seven wording in its introduction.

## How strong is the novelty check?

The public OpenAlex citing-work query for the 1999 DOI returned four records: Kostochka 2002, BKS 2021, Bradač–Bucić, and Bradač's associated thesis. The 2002 DOI returned five records, adding the regular/6-uniform papers above. These metadata queries were used to locate papers, not as mathematical evidence or an exhaustive citation count. Responses are saved locally in `work/submission_literature/fkw_citing_openalex.json` and `kostochka_citing_openalex.json`.

Title, author, notation and coefficient searches did not locate a published \(6/7\) bound or a later unrestricted coefficient below \(7/8\). The current problem page still labels the \(3/4\) question open, but itself warns that its literature coverage may be incomplete; it is not a priority certificate. [Problem page](https://www.erdosproblems.com/644).

Search results included AI-generated problem reports and GitHub candidate solutions. Their assertions were not counted as independent evidence. No comprehensive MathSciNet or subscription citation search was available, unpublished results can be missed, and indexing is incomplete. The defensible conclusion is **“no competing result located,” not “novelty proved.”** The direct comparison with the verified 1999 theorem is secure if the new theorem is correct.

## Journal policies checked from official sources

### Discrete Mathematics

The publisher's current catalogue expressly includes hypergraph theory and extremal set theory, offers Contributions and shorter Notes, and excludes work primarily consisting of applied problems or experimental results. A proof-centered paper therefore fits better than an account of search campaigns. [Official scope and article types](https://shop.elsevier.com/journals/discrete-mathematics/0012-365X).

The live [Guide for Authors](https://www.sciencedirect.com/journal/discrete-mathematics/publish/guide-for-authors) returned HTTP 403/internal errors in this environment, including its alternate journal-ID URL. Consequently I have **not verified its current page cutoff, formatting details, submission-portal URL or charges**. Older copies and third-party templates were not promoted to current policy. This does not prevent preparing the paper; the human submitter should inspect the official guide before upload.

Elsevier's current publisher policy permits AI assistance with literature synthesis, idea generation and manuscript preparation, under human oversight. It requires a declaration naming tools, purposes and oversight; research-process or code-generation assistance should additionally be described reproducibly in the methodology. AI tools cannot be authors. Authors remain responsible for the work, citations and final text. Put the manuscript-preparation declaration immediately before the references. The present project's assistance was substantive, so describing it as grammar correction would be inaccurate. [Official Elsevier AI policy](https://www.elsevier.com/about/policies-and-standards/generative-ai-policies-for-journals).

### Electronic Journal of Combinatorics

E-JC covers all branches of discrete mathematics and requires substantial, original, correct work. It is free for authors and readers. Its AI policy permits assistance with research and writing but requires the authors themselves to check proofs and provide enough detail for another human to check them. It also stresses source attribution and accuracy of the final prose. Editorial decisions remain human; the journal may use an LLM for a final check. I found **no blanket ban on AI-assisted prose** and no prescribed author declaration template on the live page. [Official scope and AI policy](https://www.combinatorics.org/ojs/index.php/eljc/about/index).

Initial submission is a PDF with an abstract through the journal's web system; separate appendices may be uploaded, but sources should not be uploaded at that stage. There is no page limit. Manuscripts must be self-contained and in the authors' own words; concurrent journal submission is prohibited. Following acceptance, the journal requests its LaTeX style, one combined TeX file, and all required source materials. The checklist explicitly requires AI-policy compliance and agreement to the possible final AI check. [Official submission instructions](https://www.combinatorics.org/ojs/index.php/eljc/about/submissions).

For this project, both policies support a transparent human-authored submission based on fully understood, verified mathematics. Independent model agreement alone does not fulfill the author's mathematical responsibility. This observation comes from the journals' actual policies, not a request for permission to continue drafting.

## Recommended submission-facing refinement

1. Center the title, abstract and introduction on the unrestricted \(6/7\) upper bound and the precise finite statement actually proved. State that the \(3/4\) problem remains open.
2. Separate inherited FKW lemmas from the new selection or avoidance argument. A reviewer should be able to locate the exact step responsible for the better coefficient.
3. Make the main theorem's proof self-contained and hand-checkable. Retain computational exploration as provenance, not a substitute for a missing lemma. Keep the structured-family results and failed-search catalogue separate from the present focused submission.
4. State uniformity, finiteness, the at-most-seven convention, rounding and small-rank exceptions explicitly. The literature's symbols differ: explain the translation once.
5. Prepare an honest AI-assistance statement describing proof exploration, code/certificate work and prose assistance. Let the human author check and own the final argument and words before submission. A reproducibility appendix should list precisely which claims depend on computation, if any.
6. On current evidence, prepare first in a neutral LaTeX layout suitable for a DM Note or Contribution; use E-JC if the final paper needs substantial self-contained structural development. Do not optimize around unverified page limits or reported acceptance rates.

## Search record and retained evidence

Representative queries executed on 26 September 2026 (including punctuation variants):

```text
Fon-Der-Flaass Kostochka Woodall 1999 Discrete Mathematics 207 277 284 transversals
"Transversals in uniform hypergraphs with property"
"Transversals in Uniform Hypergraphs with Property (p,2)" Kostochka pdf
"s004930200013" pdf
Kostochka 2002 "Transversals" "Combinatorica"
Bucić Korándi Sudakov 2021 local covering hypergraphs transversal
"Fon-Der-Flaass" "7/8"
"Fon-Der-Flaass" "6/7"
"property (7,2)" hypergraphs "6/7"
"property (7, 2)" hypergraphs "bound"
"f(k,7)" hypergraphs
"f(r,7,2)"
"h_r(7,2)"
"hypergraphs" "6r/7" "transversal"
"hypergraphs" "six sevenths" transversal
uniform hypergraphs seven edges two vertices transversal upper bound
"644" "Erdős" "6/7"
"644" "Erdos" "7/8"
"property" "7,2" "transversals" "2025"
"property" "7,2" "transversals" "2026"
"local constraints" "small representing sets" 2025 2026
"Small transversals in uniform hypergraphs" pdf
"Extensions and applications of the Tuza-Vestergaard theorem"
"The Tuza–Vestergaard theorem" transversal regular
"Electronic Journal of Combinatorics" "artificial intelligence"
"Discrete Mathematics" "Guide for authors" AI
"Discrete Mathematics" "Aims and scope" site:sciencedirect.com
"Discrete Mathematics" "Guide for authors" site:elsevier.com
site:elsevier.com "generative AI" "authors" "scientific writing"
site:sciencedirect.com/journal/discrete-mathematics/publish/guide-for-authors "generative"
"Discrete Mathematics" "Notes" "seven pages"
"Discrete Mathematics" "Guide for Authors" "Editorial Manager"
```

Public metadata queries:

- `https://api.openalex.org/works/https://doi.org/10.1016/S0012-365X(99)00114-4`
- `https://api.openalex.org/works?filter=cites:W2094192912&per-page=100`
- `https://api.openalex.org/works/https://doi.org/10.1007/s004930200013`
- `https://api.openalex.org/works?filter=cites:W1990371368&per-page=100`

Fetched official E-JC pages, Elsevier's AI policy, the BKS final PDF and extracted text, publisher metadata, the erroneous author-hosted PDF, and citation-query responses are preserved in `work/submission_literature/`. They are local research evidence, not a redistribution bundle. HTTP-error pages remain labeled as failed retrievals. The failed Sweering thesis fetch was not used to establish a theorem. No originals in the Clauding research directory were modified.
