# Codebook v2: assignment, explanation and review

**Version:** Version2: action, explanation and review layers. Replaces U as the central result for one-model-only cases; retains the absence of a specific rejection explanation as a qualification.

**Research question:** Which evidence-to-construct interpretations accompany assignment versus abstention, agreement, and different labels, and where do assignment and critic explanation diverge?

**No Match design:** prompts.py:46–63 requires clear evidence, evaluates only the current packet, and specifies assignments:[] for insufficient evidence. No numerical cutoff is specified. D01 captures an intended qualitative sufficiency contrast.

**Export meaning:** export_excel.py:367–381 writes No Match when a segment has no coding results; it is not necessarily model-returned text. Current code excludes interviewer questions and separates core versus outcome results before export.

**Export limitations:** coding.py:212–214 skips parse-error results; coding.py:358 returns empty results after exhausted retries. A displayed No Match alone cannot distinguish valid abstention from every processing pathway. No case is labeled a technical failure without case-specific evidence. Current source code documents design, not verified historical run configuration.

**Packet limitation:** Model evaluates current packet only. Same packet exposure and model-independent ground truth are not established by these exports; do not claim a globally stricter model or a numerical threshold.

**Evidence boundaries:** Substantive mechanisms use only rationale, critic_rationale and critic_coverage_rationale. Assignment/No Match labels and category membership provide action metadata; prompt/export code and user clarification provide design context.

**Question exception:** Meaning-unit text was reviewed solely to classify standalone questions under the user’s instruction. No standalone questions among259 units. M01 context dependence does not mean Question.

**Coding changes:** A01 and all unchanged interpretation codes now use the completed systematic independent-coder B application. Original A decisions are retained in the historical archive, not silently changed. U is retired. D01, R01 and Q01 are new; R01 was manually reviewed from complete candidate critic text and supplemental error/boundary checks.

**Decision values:** yes requires documented support. Unlisted interpretation codes remain unclear, not no. A critic challenge records disagreement with justification, not correctness.

**Mind versus action:** Action = assignment/exported abstention. Stated interpretation = rationale. Review position = critic text. These are observable outputs, not access to hidden cognition or necessarily the same model instance acting as its own critic.

## Definitions

### D01 — Assignment–abstention sufficiency contrast

One model assigns a construct and the other supplies no assignment; under the stated coding rule this is an intended sufficient-versus-insufficient evidence contrast within evaluated packets.

**Include:** Original one-model-only categories, excluding standalone questions. Distinguish explicit opposite No Match from user-described category provenance when the opposite row is absent.

**Exclude:** Both models assigned; a No Match row alongside another assignment; verified processing failure. Does not prove identical packet exposure or identify the exact rejected inference.


### R01 — Assignment justification challenged by critic

The coder assigns a construct, while critic_rationale explicitly contests that mapping or an essential part of its justification.

**Include:** Critic says required actor, process, referent, temporal state or boundary is not established; also includes a challenged substantive rationale claim.

**Exclude:** Ordinary scope caveats with an otherwise supported mapping; an explicit technical error; criticism inferred only from a decision/status column. A challenge does not establish that the critic is correct.


### Q01 — Question

The coded unit itself is a standalone interviewer question or request for an answer, rather than substantive participant evidence.

**Include:** Inspect unit text solely for this classification. Mark Question and exclude it from substantive threshold comparisons.

**Exclude:** Answers dependent on prior question context (M01); reported questions inside participant answers; declarative What was missing/What made it easier clauses.


### A01 — Shared substantive anchor

Both explanations explicitly connect the same stated feature to the same construct meaning.

**Include:** Paired rationale passages identify the same need, action, value, or condition and its mapping. Apply systematically to every paired case; do not restrict this code to worked examples.

**Exclude:** Matching construct names alone; same label grounded in different objects.


### A02 — Shared label with different evidence readings

A shared proposed label conceals different objects, thresholds, or critic evaluations in the explanation text.

**Include:** A paired critic accepts versus challenges a mapping, or the same label is justified using different claims.

**Exclude:** Differences inferred only from critic_decision; absent critic text; merely unequal code sets.


### M01 — Context supplies missing meaning

An explanation explicitly uses or contests interviewer/question/context information to identify a missing actor, referent, or implementation link.

**Include:** Rationale names the question, or critic says the required meaning comes from it.

**Exclude:** Assuming context was used from a short statement alone; importing actual interview text.


### M02 — Condition or mention becomes a process

A condition, need, roster, result, or generic activity is extended into a specific assessment, adaptation, engagement, planning, or evaluation process.

**Include:** A rationale asserts the conversion, or critic explicitly challenges it.

**Exclude:** An explicitly described process; pure innovation-versus-implementation object distinction without a process inference.


### M03 — Innovation versus implementation target

The explanation locates evidence in the innovation's properties/materials rather than rollout, delivery processes, implementation support, or clinical work, or reverses that mapping.

**Include:** Rollout design versus product design; modifiability versus actual modification; training strategy versus packaged materials.

**Exclude:** External/inner/individual level alone (M04); actual versus anticipated timing alone (M12).


### M04 — Different locus or resource classification

The same condition is interpreted at different organizational levels or as different resource types.

**Include:** External financing versus internal funds; general infrastructure versus task-specific resources; system support versus individual attributes.

**Exclude:** Parent/subconstruct specificity alone; raw differences in construct names without a rationale mapping.


### M05 — Role or personal attribute inferred

An occupation, title, action, or support cue is extended to a specific role, authority level, capability, or motivation, or that extension is challenged.

**Include:** Unspecified leaders become high-level leaders; choosing pilot teams becomes implementation leadership; effort becomes motivation.

**Exclude:** Explicitly identified roles with parallel interpretations; actual reach or outcome inferred from a role (M11).


### M06 — Episode generalized to culture

A specific experience, activity, need, or reaction becomes a general shared cultural value or norm, or the critic challenges that move.

**Include:** One participation episode becomes shared centeredness; workload becomes culture; coaching becomes a learning culture.

**Exclude:** Explicit shared cultural statements accepted on the same grounds by both models.


### M07 — Specificity or detail threshold

Explanations differ or explicitly debate whether a broad label or limited detail is enough to support a construct or subtype.

**Include:** Parent versus child because detail is absent; label repetition accepted versus concrete criteria required.

**Exclude:** Inferring a stricter threshold from the other model's absence; role or time distinction alone.


### M08 — Different claim or aspect emphasized

Available rationales emphasize different substantive clauses or analytical aspects of the same meaning unit.

**Include:** Actor versus activity, funding condition versus data work, involvement versus preference gathering.

**Exclude:** Different labels alone; missing comparator; assigning error merely because emphases are complementary.


### M09 — Additional comparative or causal relationship

Need, benefit, fit, pressure, credibility, or affordability is extended into an additional relationship not separately stated in the explanation's described evidence.

**Include:** Need becomes relative advantage; credibility becomes competition; affordability becomes financial availability; tracking becomes incentives.

**Exclude:** Direct comparisons described by both rationales; process inference alone (M02).


### M10 — Label and explanation mismatch

An attached construct is inconsistent with the construct or exclusion explicitly named in its own rationale.

**Include:** Assessing Needs rationale explicitly invokes Assessing Context; Financing rationale explicitly says not external funding.

**Exclude:** Debatable mapping without an explicit internal mismatch; critic disagreement alone.


### M11 — Determinant or activity promoted to outcome

A role, resource, feature, plan, measure, or implementation activity is interpreted as actual implementation, effectiveness, reach, or impact, or that move is challenged.

**Include:** Recipient identity becomes reach; a plan becomes implementation; workflow measures become clinical effectiveness.

**Exclude:** Explicitly reported outcomes; a prediction-versus-actual boundary without a determinant/activity promotion (M12).


### M12 — Time or actuality boundary

Explanations distinguish or conflate needed/intended, predicted, preexisting, and currently achieved states.

**Include:** Needed resources versus available resources; goals versus progress; current results versus preexisting evidence; retrospective step versus advance plan.

**Exclude:** Valence of an actual state (M14); generic missing detail with no temporal distinction.


### M13 — Word or referent substitution

A rationale changes a term's object or ordinary meaning in order to map it to another construct.

**Include:** Adaptability becomes adoptability; privacy becomes physical space; people's clinical suitability becomes the innovation's advantage.

**Exclude:** Any keyword overlap without an observable semantic substitution; reasonable alternative emphases alone.


### M14 — Negative evidence treated as non-applicability

A critic treats absence, deficiency, or negative quality as insufficient because it is not positive evidence of the construct.

**Include:** Incomplete design rejected for not demonstrating good design; missing information treated as inability to code design absence.

**Exclude:** A justified scope distinction; absence of any evidence; a generic omission by one model.


### M15 — Communication and relationship extension

Information-sharing quality or contact knowledge is extended to relationship quality/trust, or vice versa.

**Include:** Candid exchange becomes trust; knowing whom to call becomes strong relationships.

**Exclude:** Explicit direct relationship statements; process inference from a roster without a relationship claim.


### M16 — Critic text unavailable after technical failure

The critic_rationale itself records a technical failure instead of an evaluative explanation.

**Include:** An explicit empty-response or error message in an allowed rationale field.

**Exclude:** Missing cell alone; inferred routing failure; reconstructing an error from status columns.


### C01 — Coverage split across claims

Coverage text explicitly says an assignment addresses one claim/aspect but leaves another out.

**Include:** A specific omitted claim or acknowledged partial scope in critic_coverage_rationale.

**Exclude:** No separate claims; construct-fit failure alone; treating a row-level omission as a model-wide omission.


### C02 — Different coverage assessment scope

Coverage explanations for comparable material use different units: whole meaning unit versus only claims relevant to a construct, or different judgments about claim segmentation.

**Include:** One critic checks design-only claims while another flags a separate benefit; one reads a single claim, another multiple claims.

**Exclude:** Unequal text length; missing coverage text; asserting that broader coverage equals better fit.

