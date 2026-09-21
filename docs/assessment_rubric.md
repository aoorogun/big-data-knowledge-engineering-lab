# Assessment Rubric: Extend the Analytics Pipeline

Coursework brief: extend one stage of the pipeline (Big Data, Data Science or
Knowledge Engineering), add tests for the extension, and submit a short
written justification of a design decision made.

Total: 100 marks, mapped to UK undergraduate and postgraduate degree
classification bands.

| Criterion | Weighting | Distinction (70-100) | Merit (60-69) | Pass (50-59) | Fail (0-49) |
|---|---|---|---|---|---|
| Technical correctness | 30% | Extension is correct, handles edge cases, and integrates cleanly with the existing stage's interface. | Extension is correct for the main cases; minor edge case gaps. | Extension works for typical inputs but has noticeable gaps or fragile assumptions. | Extension does not reliably produce correct output. |
| Understanding of the underlying method | 25% | Clear evidence in code and write-up of understanding the mechanics (Spark's distributed aggregation, gradient descent, or forward chaining) rather than treating the stage as a black box. | Good understanding shown with minor gaps in explanation. | Surface-level understanding; extension works but explanation is thin. | Little evidence of understanding the method being extended. |
| Software engineering practice | 20% | Follows existing module boundaries and interfaces precisely; clean, single-responsibility code with meaningful names; version controlled with clear commits. | Mostly follows existing structure; minor inconsistency. | Structure followed loosely; some duplication or unclear boundaries. | Existing structure not respected, or code is difficult to follow. |
| Testing | 15% | Comprehensive, deterministic tests covering success, failure and edge cases for the new functionality. | Good coverage of success and failure cases. | Basic tests present but shallow. | Little or no meaningful testing. |
| Written justification | 10% | Sharp, specific discussion of a real design trade-off (for example, why a particular aggregation window, feature, or rule ordering was chosen) with awareness of alternatives. | Sound discussion of a relevant trade-off. | General discussion not clearly tied to the actual extension. | Justification missing or unrelated to the work submitted. |

## Submission checklist

- Code changes confined to the relevant stage's package
  (`dataeng`, `datascience` or `knowledgeeng`), plus any necessary wiring in
  `pipeline.py`.
- New or updated tests under `tests/`.
- A written justification of 200 to 400 words.
- A short note in the pull request or submission describing which stage was
  extended and why.

## Suggested extensions for cohort variation

Big Data: add a rolling four-week engagement trend column in the Spark
aggregation. Data Science: add a second model (for example, a decision
stump) and compare its metrics against the logistic regression baseline.
Knowledge Engineering: add a rule that considers module-level cohort
averages rather than only individual student facts. Assigning different
extensions across a cohort reduces the risk of collusion while keeping the
assessment structurally identical for fair, consistent marking.
