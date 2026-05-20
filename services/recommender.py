import pandas as pd

from services.text_processing import tokenize


FIELD_WEIGHTS = {
    "name": 4,
    "ingredients": 3,
    "tags": 3,
    "cuisine": 2,
    "meal_type": 2,
}


def recommend_recipes(recipes: pd.DataFrame, search_profile: str, limit: int = 5) -> pd.DataFrame:
    query_terms = tokenize(search_profile)
    if not query_terms:
        return pd.DataFrame()

    scored_rows = []
    for _, recipe in recipes.iterrows():
        score = 0
        matched_terms = set()

        for field, weight in FIELD_WEIGHTS.items():
            field_terms = tokenize(str(recipe[field]))
            matches = query_terms.intersection(field_terms)
            if matches:
                score += len(matches) * weight
                matched_terms.update(matches)

        if score > 0:
            scored = recipe.copy()
            scored["score"] = score
            scored["matched_terms"] = ", ".join(sorted(matched_terms))
            scored_rows.append(scored)

    if not scored_rows:
        return pd.DataFrame()

    return (
        pd.DataFrame(scored_rows)
        .sort_values(["score", "prep_time"], ascending=[False, True])
        .head(limit)
    )
