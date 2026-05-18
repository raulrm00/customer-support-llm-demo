"""Cleaning helpers based on the reference notebooks."""

from pathlib import Path

import pandas as pd

ENTITY_COLUMNS = {
    "{{Order Number}}": "has_order_number",
    "{{Invoice Number}}": "has_invoice_number",
    "{{Person Name}}": "has_person_name",
    "{{Account Type}}": "has_account_type",
    "{{Account Category}}": "has_account_category",
    "{{Delivery City}}": "has_delivery_city",
    "{{Delivery Country}}": "has_delivery_country",
    "{{Currency Symbol}}": "has_currency_symbol",
    "{{Refund Amount}}": "has_refund_amount",
}

FLAG_COLUMNS = tuple(f"flag_{flag}" for flag in "CWLMQIZPSENVBK")


def load_dataset(path: Path) -> pd.DataFrame:
    """Load a CSV or parquet dataset."""
    if path.suffix.lower() == ".csv":
        return pd.read_csv(path)
    if path.suffix.lower() == ".parquet":
        return pd.read_parquet(path)
    raise ValueError(f"Unsupported dataset format: {path.suffix}")


def clean_raw_dataset(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Clean the raw Bitext dataset into the training schema."""
    df = dataframe.copy()
    if "instruction_clean" not in df.columns:
        df["instruction_clean"] = df["instruction"]

    df.loc[df["category"] == "ORDER", "instruction_clean"] = df.loc[
        df["category"] == "ORDER", "instruction"
    ].str.replace(r"(\d{2,20})", "{{Order Number}}", regex=True)
    df.loc[df["category"] == "INVOICE", "instruction_clean"] = df.loc[
        df["category"] == "INVOICE", "instruction"
    ].str.replace(r"(\#\d{2,20})", "{{Invoice Number}}", regex=True)

    df["instruction"] = df["instruction_clean"]
    df["response_len"] = df["response"].str.len()
    df["instruction_len"] = df["instruction"].str.len()

    for entity, column_name in ENTITY_COLUMNS.items():
        if column_name not in df.columns:
            df[column_name] = df["instruction"].str.contains(entity, regex=False)

    if "flags" in df.columns:
        for column_name in FLAG_COLUMNS:
            flag = column_name.removeprefix("flag_")
            df[column_name] = df["flags"].fillna("").str.contains(flag, regex=False)
        df = df.drop(columns=["flags"])

    if "instruction_clean" in df.columns:
        df = df.drop(columns=["instruction_clean"])
    return df
