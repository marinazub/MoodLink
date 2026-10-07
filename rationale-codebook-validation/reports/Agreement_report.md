# Independent-agent reliability

Original coder A compared with fresh agent B; no adjudication or changes to A. Ratings are documented yes versus unclear, not present versus absent.

| Scope | Cases × codes | Agreement | Cohen κ | Positive agreement |
|---|---:|---:|---:|---:|
| Primary: M01–M15, paired cases | 137 × 15 | 92.1% | 0.686 | 73.1% |
| M01–M15, all cases | 259 × 15 | 94.2% | 0.694 | 72.5% |
| All21 codes, all cases | 259 × 21 | 93.0% | 0.704 | 74.3% |
| All codes except A01 and U | 259 × 19 | 94.7% | 0.735 | 76.4% |

Primary descriptive 95% segment-bootstrap interval for κ: 0.635–0.733; 2,000 resamples of 45 parent segments. This does not make these cases independent interviews.

## Per-code agreement

| Code | Mechanism / pattern | A yes | B yes | Both yes | A only | B only | Both unclear | Agreement | κ | Positive agreement |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| A01 | Shared substantive anchor | 3 | 121 | 3 | 0 | 118 | 138 | 54.4% | 0.026 | 4.8% |
| A02 | Shared label with different evidence readings | 35 | 50 | 33 | 2 | 17 | 207 | 92.7% | 0.734 | 77.6% |
| M01 | Context supplies missing meaning | 25 | 37 | 24 | 1 | 13 | 221 | 94.6% | 0.745 | 77.4% |
| M02 | Condition or mention becomes a process | 65 | 78 | 57 | 8 | 21 | 173 | 88.8% | 0.721 | 79.7% |
| M03 | Innovation versus implementation target | 33 | 40 | 29 | 4 | 11 | 215 | 94.2% | 0.761 | 79.5% |
| M04 | Different locus or resource classification | 49 | 43 | 37 | 12 | 6 | 204 | 93.1% | 0.762 | 80.4% |
| M05 | Role or personal attribute inferred | 39 | 39 | 33 | 6 | 6 | 214 | 95.4% | 0.819 | 84.6% |
| M06 | Episode generalized to culture | 16 | 24 | 16 | 0 | 8 | 235 | 96.9% | 0.784 | 80.0% |
| M07 | Specificity or detail threshold | 30 | 30 | 21 | 9 | 9 | 220 | 93.1% | 0.661 | 70.0% |
| M08 | Different claim or aspect emphasized | 14 | 43 | 10 | 4 | 33 | 212 | 85.7% | 0.293 | 35.1% |
| M09 | Additional comparative or causal relationship | 34 | 55 | 32 | 2 | 23 | 202 | 90.3% | 0.665 | 71.9% |
| M10 | Label and explanation mismatch | 3 | 3 | 3 | 0 | 0 | 256 | 100.0% | 1.000 | 100.0% |
| M11 | Determinant or activity promoted to outcome | 24 | 21 | 17 | 7 | 4 | 231 | 95.8% | 0.732 | 75.6% |
| M12 | Time or actuality boundary | 12 | 33 | 10 | 2 | 23 | 224 | 90.3% | 0.404 | 44.4% |
| M13 | Word or referent substitution | 4 | 13 | 4 | 0 | 9 | 246 | 96.5% | 0.458 | 47.1% |
| M14 | Negative evidence treated as non-applicability | 2 | 3 | 2 | 0 | 1 | 256 | 99.6% | 0.798 | 80.0% |
| M15 | Communication and relationship extension | 2 | 5 | 2 | 0 | 3 | 254 | 98.8% | 0.567 | 57.1% |
| M16 | Critic text unavailable after technical failure | 1 | 1 | 1 | 0 | 0 | 258 | 100.0% | 1.000 | 100.0% |
| C01 | Coverage split across claims | 91 | 96 | 91 | 0 | 5 | 163 | 98.1% | 0.958 | 97.3% |
| C02 | Different coverage assessment scope | 4 | 18 | 4 | 0 | 14 | 241 | 94.6% | 0.347 | 36.4% |
| U | Missing comparator explanation | 122 | 122 | 122 | 0 | 0 | 137 | 100.0% | 1.000 | 100.0% |

## Category comparison, M01–M15

| Category | Decisions | Agreement | κ |
|---|---:|---:|---:|
| GPT6_Only_Assignments | 1575 | 96.7% | 0.638 |
| Medgemma_Only_Assignments | 255 | 96.1% | 0.817 |
| Total_Construct_Match | 60 | 98.3% | 0.880 |
| Partial_Construct_Match | 1785 | 91.7% | 0.663 |
| Different_Constructs | 210 | 93.8% | 0.806 |

Whole-case exact code-set agreement: 28.6% for all21 codes; 42.5% for M01–M15. The complete mismatch file contains 381 case-code disagreements. All 1269 B evidence excerpts passed exact source-substring and locator checks.

## Review priorities

The lowest reproducibility among the main interpretive codes occurs for **M08 (different claim/aspect emphasized, κ=0.293)**, **M12 (time/actuality boundary, κ=0.404)**, and **M13 (word/referent substitution, κ=0.458)**. The coverage-scope code **C02 (κ=0.347)** also needs boundary clarification. B records substantially more positives for each, which warrants reviewing the threshold rather than assuming either coder is right. These are priorities for adjudication after initial human ratings are saved.

M10 and M16 have perfect observed agreement but only three and one shared positive cases respectively; this is weak evidence of general reproducibility. A01's very low κ=0.026 reflects the original illustrative versus fresh systematic use and should not be interpreted as a model disagreement rate. The frozen original decisions remain untouched.

## Interpretation and limitations

A01 was illustrative in the original pass, whereas B applies the definition systematically; its discrepancy is partly procedural, so it is separate from the primary mechanism summary. U is determined by missing comparator data and M16 is a technical-message flag. Easy agreement on those flags should not stand in for interpretive reproducibility. High percent agreement can reflect many jointly unclear decisions; positive agreement and per-code κ expose this.

The original pass was iterative and focused on salient observations; B is a fresh systematic pass. This is a reproducibility audit of that existing analysis, not a preplanned blind two-coder study. A separate agent is not a separate model family or a human. Definitions and cases were shared; original coded examples and decisions were withheld. A comparison-unit clarification was sent after the first batch. No coded case answers were supplied.

Cohen κ uses observed and marginal expected agreement, following [scikit-learn’s official definition](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.cohen_kappa_score.html). Blank human responses must be treated as missing, never converted into unclear. Human validation is prepared but has not occurred.
