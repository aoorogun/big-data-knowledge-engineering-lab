# Student Exercises

A progressive sequence of exercises spanning all three disciplines covered
by this pipeline, suitable for a Level 7 Big Data, Data Science and
Knowledge Engineering module.

## Exercise 1: Extend the Spark aggregation

Add a new aggregated column, `max_weekly_clicks`, computed with a Spark
window or group-by aggregation over the raw weekly records. Write a test
confirming the new column appears in the processed output with correct
values for a small hand-checked dataset.

## Exercise 2: Engineer a new feature

Add a `posts_per_click` feature in `datascience/features.py`, guarding
against division by zero, and include it in the feature set used by
`make_train_test_split`. Retrain the model and report whether accuracy,
precision or recall change on the test split.

## Exercise 3: Add a knowledge engineering rule

Add a new `Rule` that recommends a peer study group when engagement is
medium and attendance is above 0.8 but the assignment score is still below
60. Write tests confirming the rule fires only when all three conditions
hold, using the existing tests in `tests/test_rules.py` as a model.

## Exercise 4: Compare Python and R regression

Add a second R model to `r/statistical_analysis.R` that includes an
interaction term between `total_clicks` and `attendance_rate`. Compare its
R-squared against the existing model and discuss, in a short paragraph,
whether the interaction term is justified by the improvement in fit.

## Exercise 5: Trace an inference chain

For a single synthetic student, print the `FactBase` contents after each
pass of forward chaining (modify `run_forward_chaining` to accept an
optional callback invoked after each round). Use this to produce a written
trace showing exactly which rule fired at which step and why, suitable as
a worked example for explaining forward chaining to a class.

## Stretch exercise: distribute across a real cluster

Read the Spark documentation on cluster deployment modes and describe, in
250 words, what would need to change in `dataeng/spark_pipeline.py` (if
anything) to run the same job against a real multi-node Hadoop YARN or
Kubernetes cluster instead of local mode, and what would stay the same.
