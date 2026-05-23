from __future__ import annotations

import re

import pandas as pd

from services.text_processing import tokenize


NON_INGREDIENT_WORDS = {
    "bowl",
    "cuisine",
    "dish",
    "food",
    "ingredient",
    "meal",
    "plate",
    "recipe",
    "table",
}

ALIASES = {
    "beef": {"beef", "steak"},
    "chicken": {"chicken", "poultry"},
    "pork": {"pork", "bacon", "ham"},
    "salmon": {"salmon"},
    "tuna": {"tuna"},
    "prawns": {"prawn", "prawns", "shrimp"},
    "tofu": {"tofu"},
    "egg": {"egg", "eggs", "omelette"},
    "turkey": {"turkey"},
    "rice": {"rice"},
    "noodles": {"noodle", "noodles", "udon"},
    "pasta": {"pasta", "spaghetti"},
    "tomato": {"tomato", "tomatoes"},
    "avocado": {"avocado"},
    "broccoli": {"broccoli"},
    "lettuce": {"lettuce"},
    "cucumber": {"cucumber"},
    "carrot": {"carrot", "carrots"},
    "spinach": {"spinach"},
    "mushroom": {"mushroom", "mushrooms"},
    "beans": {"bean", "beans"},
    "corn": {"corn"},
    "banana": {"banana"},
    "berries": {"berry", "berries"},
    "pumpkin": {"pumpkin"},
}


def enrich_image_analysis_with_ingredients(
    image_analysis: dict,
    recipes: pd.DataFrame,
) -> dict:
    enriched = dict(image_analysis)
    enriched["ingredients"] = detect_image_ingredients(image_analysis, recipes)
    return enriched


def detect_image_ingredients(image_analysis: dict, recipes: pd.DataFrame) -> list[str]:
    source_text = " ".join(
        [
            image_analysis.get("caption", ""),
            " ".join(image_analysis.get("keywords", [])),
            image_analysis.get("ocr_text", ""),
        ]
    )
    source_terms = tokenize(source_text)
    source_phrase = _normalise_text(source_text)

    detected = set()
    for ingredient in _recipe_ingredient_catalog(recipes):
        ingredient_terms = tokenize(ingredient)
        if not ingredient_terms or ingredient_terms.intersection(NON_INGREDIENT_WORDS):
            continue

        ingredient_phrase = _normalise_text(ingredient)
        if ingredient_phrase and ingredient_phrase in source_phrase:
            detected.add(ingredient)
            continue

        if ingredient_terms.issubset(source_terms):
            detected.add(ingredient)

    for canonical, aliases in ALIASES.items():
        if source_terms.intersection(aliases):
            detected.add(canonical)

    return sorted(detected)


def _recipe_ingredient_catalog(recipes: pd.DataFrame) -> set[str]:
    ingredients = set()
    for ingredient_list in recipes["ingredients"].dropna():
        for ingredient in str(ingredient_list).split(","):
            cleaned = _normalise_text(ingredient)
            if cleaned:
                ingredients.add(cleaned)
    return ingredients


def _normalise_text(text: str) -> str:
    words = re.findall(r"[a-zA-Z]+", text.lower())
    return " ".join(words)
