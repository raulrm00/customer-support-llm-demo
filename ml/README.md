# ML Pipeline

Training pipeline for the customer support category classifier.

## Train

```powershell
cd ml
..\.venv\Scripts\python.exe -m src.training.train
```

The default training input is `data/raw/bitext-limpio.parquet`, tracked with
DVC, and the default artifact is `models/modelo_idf.joblib`.

## DVC

```powershell
cd ml
..\.venv\Scripts\python.exe -m dvc status
..\.venv\Scripts\python.exe -m dvc repro
..\.venv\Scripts\python.exe -m dvc metrics show
```

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
