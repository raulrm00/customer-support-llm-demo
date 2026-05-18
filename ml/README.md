# ML Pipeline

Training pipeline for the customer support category classifier.

## Train

```powershell
cd ml
..\.venv\Scripts\python.exe -m src.training.train
```

The default training input is `../refs/data/bitext-limpio.parquet` and the
default artifact is `models/modelo_idf.joblib`.

## Inference

```powershell
cd ml
..\.venv\Scripts\python.exe -m src.inference.predict "Where is my order?"
```

## Validation

```powershell
cd ml
..\.venv\Scripts\python.exe -m black src
..\.venv\Scripts\python.exe -m ruff check src
..\.venv\Scripts\python.exe -m mypy src
..\.venv\Scripts\python.exe -m pytest
```
