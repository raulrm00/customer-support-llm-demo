# Decisions

## 2026-05-18 - Backend inference contract

### Context
The reference notebooks include both a dictionary artifact named
`modelo_idf.joblib` and a scikit-learn `Pipeline` with a `ColumnTransformer` and
`TfidfVectorizer` over the `instruction` column.

### Decision
The production `modelo_idf.joblib` artifact is a complete scikit-learn
`Pipeline`. The backend prediction endpoint accepts a single `instruction` field
and passes a one-row pandas `DataFrame` with that column to the loaded pipeline.

### Rationale
This preserves the requested artifact name while satisfying the project rule
that production inference must persist preprocessing and estimator together.

### Consequences
The configured artifact at `MODEL_ARTIFACT_PATH` must be a complete pipeline that
exposes `predict`, and confidence is only returned when the pipeline also exposes
`predict_proba`.
