from pathlib import Path

import pandas as pd
import streamlit as st


DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "recipes.csv"


@st.cache_data
def load_recipes() -> pd.DataFrame:
    recipes = pd.read_csv(DATA_PATH)
    required_columns = {
        "name",
        "cuisine",
        "ingredients",
        "tags",
        "prep_time",
        "meal_type",
    }
    missing_columns = required_columns.difference(recipes.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Recipe dataset is missing columns: {missing}")
    return recipes
