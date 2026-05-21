"""Run inference with the persisted customer support model."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import joblib
import pandas as pd

# Add the root directory to sys.path to allow importing from backend or ml/src
sys.path.append(str(Path(__file__).resolve().parents[3]))
# Handle the module redirection used during training
try:
    import app.services.qwen_model as qwen_model
    sys.modules["app.services.qwen_model"] = qwen_model
except ImportError:
    try:
        import src.inference.qwen_model as qwen_model
        sys.modules["app.services.qwen_model"] = qwen_model
    except ImportError:
        pass

def predict_category(model_path: Path, instruction: str) -> str:
    """Predict one support category from a persisted pipeline."""
    pipeline = joblib.load(model_path)
    prediction = pipeline.predict(pd.DataFrame([{"instruction": instruction}]))[0]
    return str(prediction)


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("instruction", help="Customer support request text.")
    parser.add_argument(
        "--model-path",
        type=Path,
        default=Path("models/modelo_idf.joblib"),
        help="Path to the persisted model artifact.",
    )
    return parser.parse_args()


def main() -> None:
    """Run prediction from the command line."""
    args = parse_args()
    result = {"prediction": predict_category(args.model_path, args.instruction)}
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
