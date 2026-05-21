import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import pandas as pd
import numpy as np
from typing import List, Any
import os

class QwenClassifier:
    """
    A scikit-learn compatible wrapper for Qwen sequence classification.
    """
    def __init__(self, model_name_or_path: str, labels: List[str]):
        self.model_name_or_path = model_name_or_path
        self.labels = labels
        self.label2id = {label: i for i, label in enumerate(labels)}
        self.id2label = {i: label for i, label in enumerate(labels)}
        self._model = None
        self._tokenizer = None
        self._device = "cuda" if torch.cuda.is_available() else "cpu"

    def _resolve_path(self, path: str) -> str:
        """Resolve path relative to current file if needed."""
        if os.path.isabs(path):
            return path
        # Assuming we are in backend/app/services/qwen_model.py
        # The repo root is 3 levels up
        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
        return os.path.join(repo_root, path)

    def _ensure_loaded(self) -> None:
        if self._model is None:
            resolved_path = self._resolve_path(self.model_name_or_path)
            self._tokenizer = AutoTokenizer.from_pretrained(resolved_path)
            if self._tokenizer.pad_token is None:
                self._tokenizer.pad_token = self._tokenizer.eos_token
            
            self._model = AutoModelForSequenceClassification.from_pretrained(
                resolved_path,
                num_labels=len(self.labels),
                id2label=self.id2label,
                label2id=self.label2id,
                torch_dtype="auto",
            ).to(self._device)
            self._model.eval()

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        self._ensure_loaded()
        if "instruction" not in X.columns:
            raise ValueError("Input DataFrame must contain 'instruction' column")
        
        instructions = X["instruction"].tolist()
        inputs = self._tokenizer(
            instructions, 
            return_tensors="pt", 
            padding=True, 
            truncation=True,
            max_length=512
        ).to(self._device)
        
        with torch.no_grad():
            outputs = self._model(**inputs)
            predictions = torch.argmax(outputs.logits, dim=-1)
        
        return np.array([self.id2label[p.item()] for p in predictions])

    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        self._ensure_loaded()
        if "instruction" not in X.columns:
            raise ValueError("Input DataFrame must contain 'instruction' column")
        
        instructions = X["instruction"].tolist()
        inputs = self._tokenizer(
            instructions, 
            return_tensors="pt", 
            padding=True, 
            truncation=True,
            max_length=512
        ).to(self._device)
        
        with torch.no_grad():
            outputs = self._model(**inputs)
            probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
        
        return probs.cpu().numpy()

    def __getstate__(self) -> dict[str, Any]:
        state = self.__dict__.copy()
        state["_model"] = None
        state["_tokenizer"] = None
        return state

    def __setstate__(self, state: dict[str, Any]) -> None:
        self.__dict__.update(state)
