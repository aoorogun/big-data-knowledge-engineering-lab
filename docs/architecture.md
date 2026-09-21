# Architecture Walkthrough

This document explains the four-stage pipeline for use as lecture or lab
material spanning Big Data, Data Science and Knowledge Engineering.

## Stage 1: Big Data engineering with Spark

`dataeng/synthetic_data.py` generates weekly engagement records for a
configurable number of students across three modules and twelve weeks, using
a fixed random seed for reproducibility. `dataeng/spark_pipeline.py` then
loads this raw CSV into a Spark DataFrame, cleans null values, and performs a
group-by aggregation to produce one row per student per module: total VLE
clicks, total forum posts, attendance rate, mean assignment score, and a
weighted engagement score. This is a self-contained example of the
map-reduce style aggregation pattern central to Big Data teaching, without
requiring an external Hadoop or Spark cluster: `SparkSession.builder.master
("local[*]")` runs Spark's distributed execution engine on the local machine
using all available cores.

## Stage 2: Data Science with a from-scratch model

`datascience/features.py` derives a binary `at_risk` label from the
aggregated mean assignment score. `datascience/dataset.py` performs a
reproducible train/test split. `datascience/model.py` implements logistic
regression by hand: forward pass with the sigmoid function, gradient descent
over cross-entropy loss with L2 regularisation, and feature standardisation
before training. Building this without a library such as scikit-learn is
deliberate: it exposes the mechanics (gradients, learning rate, the sigmoid
non-linearity) that a Level 7 module would want students to understand before
they use a library implementation. `datascience/evaluate.py` computes
accuracy, precision, recall, F1 and a confusion matrix from first principles
as well.

## Stage 3: Knowledge Engineering with forward chaining

This stage is deliberately symbolic rather than statistical, to give
students a concrete contrast with Stage 2. `knowledgeeng/facts.py` defines a
`FactBase`, a simple key-value store of asserted facts about a student.
`knowledgeeng/rules.py` defines a small set of `Rule` objects, each a
condition function and an action function operating on a `FactBase`, encoding
domain knowledge such as "if engagement is low and the model predicts risk,
recommend a tutor referral". `knowledgeeng/inference_engine.py` implements
forward chaining: it repeatedly scans the rule set, firing any rule whose
condition is newly satisfied, until no rule fires in a full pass. This is the
classical knowledge engineering pattern taught alongside expert systems and
production rule systems.

## Stage 4: Statistical analysis in R

`r/statistical_analysis.R` is invoked from Python via `src/r_integration.py`,
which checks whether `Rscript` is available on the system path before
attempting to run it, so the pipeline degrades gracefully on a machine
without R installed. The R script computes Pearson correlation tests and
fits a multiple linear regression, writing a short results file that is
parsed back into the final report.

## Composition

`src/pipeline.py` is the only module that imports from all four stages. It
calls each stage's public function in sequence, passing the output of one as
the input to the next, and hands the combined result to
`reporting/report_builder.py` to produce `outputs/report.md`. This
composition root pattern keeps each stage testable and replaceable in
isolation, which is demonstrated directly in the test suite: the Spark tests,
model tests and rule tests all run independently of one another.

## Where to extend this for a lecture or lab

- Change the weighting in `aggregate_by_student_module` and discuss how
  engagement score design choices affect downstream classification.
- Add a new column to the synthetic data generator (for example, a
  self-reported wellbeing score) and route it through Stages 2 and 3.
- Add a new `Rule` that fires only when two existing facts are both present,
  to discuss rule conflict and firing order in forward chaining.
- Add an additional R model (for example, a generalised linear model with a
  logit link) and compare its coefficients with the Python logistic
  regression weights.
