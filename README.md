# Big Data, Data Science and Knowledge Engineering Lab

A modular, end-to-end teaching pipeline built as a Level 7 exemplar covering
three distinct disciplines in one coherent workflow: Big Data engineering
with Apache Spark, applied Data Science with a from-scratch machine learning
model, and Knowledge Engineering with a symbolic rule-based inference engine.
An R script is included for classical statistical analysis, run alongside
the Python pipeline.

## What the pipeline does

Synthetic student engagement data (VLE clicks, forum activity, attendance and
periodic assignment scores across three modules and twelve weeks) is
generated, then processed through four stages:

1. Big Data (`src/dataeng`): a PySpark job ingests the raw weekly records,
   cleans them, and aggregates them into one row per student per module,
   computing a weighted engagement score.
2. Data Science (`src/datascience`): a logistic regression classifier,
   implemented from first principles with gradient descent in NumPy rather
   than a library call, predicts which student-module records are at risk
   based on engagement features, and is evaluated with accuracy, precision,
   recall and F1.
3. Knowledge Engineering (`src/knowledgeeng`): a small forward-chaining
   inference engine applies a declarative rule set (facts and conditions, not
   statistical weights) to the model's predictions to generate human-readable
   intervention recommendations.
4. Statistical analysis (`r/statistical_analysis.R`): an R script computes
   correlation tests and a multiple linear regression over the same
   aggregated dataset, run from Python via `subprocess` when R is available.

A markdown report combining all four stages is written to `outputs/report.md`.

## Why it is structured this way

The three Python packages are deliberately independent: `dataeng` knows
nothing about machine learning, `datascience` knows nothing about Spark, and
`knowledgeeng` knows nothing about either. `src/pipeline.py` is the only
module that wires them together. This mirrors how a Level 7 module might
teach each topic (Big Data, Data Science, Knowledge Engineering) as a
separate block before showing students how the blocks compose into a single
applied system.

## Requirements

- Python 3.9 or later
- Java 11 or later (required by PySpark; no separate Hadoop or Spark cluster
  installation is needed, PySpark runs in local mode)
- R with base packages (optional; the pipeline skips the statistical
  analysis stage gracefully if `Rscript` is not on the system path)

Install Python dependencies:

```
pip install -r requirements.txt
```

## Running the pipeline

From the repository root:

```
PYTHONPATH=src python -m cli run-all
```

This generates the synthetic dataset, runs the Spark ETL job, trains and
evaluates the model, runs the knowledge engineering inference over every
student-module record, runs the R statistical analysis if available, and
writes `outputs/report.md`.

Individual stages can also be run on their own:

```
PYTHONPATH=src python -m cli generate-data --students 150 --seed 7
PYTHONPATH=src python -m cli run-etl --input data/raw/engagement.csv --output data/processed/aggregated.csv
```

Or programmatically:

```python
from pipeline import run_full_pipeline

result = run_full_pipeline(number_of_students=150, seed=7)
print(result.metrics)
```

## Running the tests

```
pip install -r requirements.txt
pytest
```

The Spark-backed tests start a local Spark session and take a few seconds
longer than the rest of the suite; all tests are otherwise fast and
deterministic thanks to fixed random seeds.

## Curriculum use

- `docs/architecture.md` - a stage-by-stage explanation of the pipeline for
  lecture or lab use.
- `docs/assessment_rubric.md` - a marking rubric for a coursework assignment
  built around extending one stage of the pipeline.
- `docs/student_exercises.md` - a progressive sequence of exercises spanning
  all three disciplines.

## Data note

All data in this repository is synthetically generated with a fixed random
seed. No real student records are used or required.

## License

MIT
