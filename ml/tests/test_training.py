"""Tests for the ML training pipeline."""

from pathlib import Path
from typing import Any

import joblib
import pandas as pd

from src.schemas.customer_support import CATEGORIES
from src.training.train import train_model


def build_dataset() -> pd.DataFrame:
    """Create a small balanced dataset for pipeline tests."""
    rows: list[dict[str, Any]] = []
    categories = [
        "ORDER",
        "SHIPPING",
        "CANCEL",
        "INVOICE",
        "PAYMENT",
        "REFUND",
        "FEEDBACK",
        "CONTACT",
        "ACCOUNT",
        "DELIVERY",
        "SUBSCRIPTION",
    ]
    intents = [
        "track_order",
        "set_up_shipping_address",
        "cancel_order",
        "get_invoice",
        "payment_issue",
        "get_refund",
        "review",
        "contact_customer_service",
        "create_account",
        "delivery_period",
        "newsletter_subscription",
    ]
    for category, intent in zip(categories, intents, strict=True):
        for repeat in range(5):
            instruction = f"{category.lower()} request {repeat}"
            rows.append(
                {
                    "instruction": instruction,
                    "intent": intent,
                    "category": category,
                    "response": f"Response for {category}",
                    "response_len": 20,
                    "instruction_len": len(instruction),
                    "flag_C": False,
                    "flag_W": False,
                    "flag_L": False,
                    "flag_M": False,
                    "flag_Q": False,
                    "flag_I": False,
                    "flag_Z": False,
                    "flag_P": False,
                    "flag_S": False,
                    "flag_E": False,
                    "flag_N": False,
                    "flag_V": False,
                    "flag_B": False,
                    "flag_K": False,
                    "has_order_number": category == "ORDER",
                    "has_invoice_number": category == "INVOICE",
                    "has_person_name": False,
                    "has_account_type": False,
                    "has_account_category": False,
                    "has_delivery_city": False,
                    "has_delivery_country": False,
                    "has_currency_symbol": False,
                    "has_refund_amount": category == "REFUND",
                }
            )
    return pd.DataFrame(rows)


def test_training_persists_full_pipeline(tmp_path: Path) -> None:
    """Training persists a loadable full pipeline artifact."""
    data_path = tmp_path / "processed.parquet"
    build_dataset().to_parquet(data_path)

    params = {
        "data": {
            "input_path": str(data_path),
            "target_column": "category",
            "text_column": "instruction",
        },
        "training": {
            "test_size": 0.2,
            "validation_size": 0.25,
            "random_state": 42,
            "max_iter": 200,
            "stop_words": "english",
        },
        "artifacts": {
            "model_path": "models/modelo_idf.joblib",
            "metadata_path": "models/model_metadata.json",
        },
    }

    metrics = train_model(params=params, project_dir=tmp_path)

    model_path = tmp_path / "models" / "modelo_idf.joblib"
    metadata_path = tmp_path / "models" / "model_metadata.json"
    pipeline = joblib.load(model_path)
    prediction = pipeline.predict(pd.DataFrame([{"instruction": "order request"}]))

    assert model_path.exists()
    assert metadata_path.exists()
    assert hasattr(pipeline, "predict")
    assert str(prediction[0]) in CATEGORIES
    assert "test_accuracy" in metrics
