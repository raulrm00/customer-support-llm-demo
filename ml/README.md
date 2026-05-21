# ML Pipeline

Training pipeline for the customer support category classifier using **Qwen/Qwen3-0.6B** fine-tuning.

## Train

```powershell
cd ml
..\.venv\Scripts\python.exe -m src.training.train
```

The pipeline now performs an SFT (Supervised Fine-Tuning) on the Qwen-0.6B model using LoRA.
The default training input is `data/raw/bitext-limpio.parquet`, tracked with
DVC, and the default artifact is `models/modelo_idf.joblib` (which wraps the fine-tuned LLM).

## Qwen Fine-Tuning

The training process:
1. Loads the Qwen-0.6B base model.
2. Applies LoRA (Low-Rank Adaptation) for efficient tuning.
3. Fine-tunes on the customer support dataset for sequence classification.
4. Merges LoRA weights back into the base model.
5. Persists a scikit-learn compatible wrapper.

## DVC
...

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
