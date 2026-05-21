"""Train and fine-tune Qwen for customer support classification."""

from __future__ import annotations

import argparse
import json
import os
import shutil
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
import torch
import yaml
from datasets import Dataset
from dvclive import Live  # type: ignore[attr-defined]
from peft import LoraConfig, get_peft_model
from sklearn.model_selection import train_test_split
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    DataCollatorWithPadding,
    Trainer,
    TrainingArguments,
)

from src.evaluation.metrics import classification_metrics
from src.inference.qwen_model import QwenClassifier
from src.preprocessing.cleaning import load_dataset
from src.schemas.customer_support import CATEGORIES, ProcessedCustomerSupportSchema


def load_params(path: Path) -> dict[str, Any]:
    """Load training parameters from YAML."""
    with path.open(encoding="utf-8") as file:
        params = yaml.safe_load(file) or {}
    if not isinstance(params, dict):
        raise ValueError("params.yaml must contain a mapping.")
    return params


def log_experiment(
    project_dir: Path,
    training_params: dict[str, Any],
    metrics: dict[str, float],
) -> None:
    """Log metrics with DVCLive when DVC is initialized."""
    live_dir = project_dir / "dvclive"
    live_dir.mkdir(parents=True, exist_ok=True)

    if (project_dir / ".dvc").exists():
        with Live(
            dir=str(live_dir),
            save_dvc_exp=False,
            dvcyaml=False,
        ) as live:
            live.log_params(training_params)
            for name, value in metrics.items():
                live.log_metric(name, value)
        return

    with (live_dir / "metrics.json").open("w", encoding="utf-8") as file:
        json.dump(metrics, file, indent=2, sort_keys=True)
    with (live_dir / "params.json").open("w", encoding="utf-8") as file:
        json.dump(training_params, file, indent=2, sort_keys=True)


def train_model(params: dict[str, Any], project_dir: Path) -> dict[str, float]:
    """Fine-tune Qwen, evaluate, and persist the model pipeline."""
    data_params = params["data"]
    qwen_params = params["qwen"]
    artifact_params = params["artifacts"]

    input_path = (project_dir / data_params["input_path"]).resolve()
    model_path = project_dir / artifact_params["model_path"]
    metadata_path = project_dir / artifact_params["metadata_path"]
    qwen_output_dir = project_dir / artifact_params["qwen_output_dir"]
    
    model_path.parent.mkdir(parents=True, exist_ok=True)
    metadata_path.parent.mkdir(parents=True, exist_ok=True)
    qwen_output_dir.mkdir(parents=True, exist_ok=True)

    dataframe = load_dataset(input_path)
    validated = ProcessedCustomerSupportSchema.validate(dataframe)

    text_column = str(data_params["text_column"])
    target_column = str(data_params["target_column"])
    
    # Label mapping
    label2id = {label: i for i, label in enumerate(CATEGORIES)}
    id2label = {i: label for i, label in enumerate(CATEGORIES)}

    # Prepare datasets
    train_df, test_df = train_test_split(
        validated,
        test_size=params["training"]["test_size"],
        random_state=params["training"]["random_state"],
        stratify=validated[target_column],
    )
    
    # HuggingFace Datasets
    train_dataset = Dataset.from_pandas(train_df[[text_column, target_column]])
    test_dataset = Dataset.from_pandas(test_df[[text_column, target_column]])

    # Tokenizer
    model_name = qwen_params["model_name"]
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    def tokenize_function(examples):
        tokens = tokenizer(
            examples[text_column], 
            truncation=True, 
            padding="max_length", 
            max_length=qwen_params["max_length"]
        )
        tokens["labels"] = [label2id[label] for label in examples[target_column]]
        return tokens

    tokenized_train = train_dataset.map(tokenize_function, batched=True)
    tokenized_test = test_dataset.map(tokenize_function, batched=True)

    # Model
    model = AutoModelForSequenceClassification.from_pretrained(
        model_name,
        num_labels=len(CATEGORIES),
        id2label=id2label,
        label2id=label2id,
        torch_dtype="auto",
    )
    model.config.pad_token_id = tokenizer.pad_token_id

    # LoRA
    lora_config = LoraConfig(
        r=qwen_params["lora_r"],
        lora_alpha=qwen_params["lora_alpha"],
        target_modules=["q_proj", "v_proj"],
        lora_dropout=qwen_params["lora_dropout"],
        bias="none",
        task_type="SEQ_CLS",
    )
    model = get_peft_model(model, lora_config)

    # Training Arguments
    training_args = TrainingArguments(
        output_dir=str(qwen_output_dir / "checkpoints"),
        learning_rate=float(qwen_params["learning_rate"]),
        per_device_train_batch_size=int(qwen_params["per_device_train_batch_size"]),
        gradient_accumulation_steps=int(qwen_params["gradient_accumulation_steps"]),
        num_train_epochs=int(qwen_params["num_train_epochs"]),
        weight_decay=0.01,
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        logging_dir=str(qwen_output_dir / "logs"),
        remove_unused_columns=True,
        push_to_hub=False,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_train,
        eval_dataset=tokenized_test,
        processing_class=tokenizer,
        data_collator=DataCollatorWithPadding(tokenizer=tokenizer),
    )

    trainer.train()

    # Save final model
    final_model_dir = qwen_output_dir / "final"
    trainer.save_model(str(final_model_dir))
    
    # Merge LoRA weights for easier inference
    merged_model = model.merge_and_unload()
    merged_model.save_pretrained(str(final_model_dir / "merged"))
    tokenizer.save_pretrained(str(final_model_dir / "merged"))

    # Evaluation
    predictions = trainer.predict(tokenized_test)
    y_pred = [id2label[p.item()] for p in torch.argmax(torch.tensor(predictions.predictions), dim=-1)]
    y_true = test_df[target_column].tolist()
    
    metrics = classification_metrics(y_true, y_pred, "test")
    # Add loss from trainer
    metrics["train_loss"] = float(trainer.state.log_history[-1].get("train_loss", 0.0))

    # Save wrapper for backend
    # Trick to ensure backend can load the class
    QwenClassifier.__module__ = "app.services.qwen_model"
    
    # Point the wrapper to the merged model directory
    # The backend will resolve this path relative to repo root
    relative_model_path = os.path.relpath(final_model_dir / "merged", project_dir.parent)
    classifier_wrapper = QwenClassifier(
        model_name_or_path=relative_model_path,
        labels=list(CATEGORIES)
    )
    
    joblib.dump(classifier_wrapper, model_path)

    metadata = {
        "model_version": "2.0.0",
        "pipeline_version": "2.0.0",
        "artifact_name": model_path.name,
        "created_at": datetime.now(UTC).isoformat(),
        "input_schema": {"required_columns": [text_column]},
        "target_column": target_column,
        "training_rows": int(len(train_df)),
        "test_rows": int(len(test_df)),
        "metrics": metrics,
        "base_model": model_name
    }
    with metadata_path.open("w", encoding="utf-8") as file:
        json.dump(metadata, file, indent=2, sort_keys=True)

    log_experiment(project_dir, qwen_params, metrics)
    return metrics


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--params",
        type=Path,
        default=Path("params.yaml"),
        help="Path to params.yaml relative to the ml directory.",
    )
    return parser.parse_args()


def main() -> None:
    """Train the model from the command line."""
    args = parse_args()
    project_dir = Path.cwd()
    params = load_params(project_dir / args.params)
    metrics = train_model(params=params, project_dir=project_dir)
    print(json.dumps(metrics, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
