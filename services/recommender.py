import pandas as pd

from services.text_processing import tokenize


FIELD_WEIGHTS = {
    "name": 4,
    "ingredients": 3,
    "tags": 3,
    "cuisine": 2,
    "meal_type": 2,
}

PROTEIN_ALIASES = {
    "beef": {"beef", "steak"},
    "chicken": {"chicken", "poultry"},
    "pork": {"pork", "bacon", "ham"},
    "fish": {"fish", "salmon", "tuna", "cod"},
    "seafood": {"seafood", "prawn", "prawns", "shrimp"},
    "tofu": {"tofu"},
    "egg": {"egg", "eggs", "omelette"},
    "turkey": {"turkey"},
}

PROTEIN_COMPATIBILITY = {
    "beef": {"beef"},
    "chicken": {"chicken"},
    "pork": {"pork"},
    "fish": {"fish", "seafood"},
    "seafood": {"fish", "seafood"},
    "tofu": {"tofu"},
    "egg": {"egg"},
    "turkey": {"turkey"},
}

PROTEIN_MATCH_BONUS = 10
COMPATIBLE_PROTEIN_BONUS = 4


def recommend_recipes(recipes: pd.DataFrame, search_profile: str, limit: int = 5) -> pd.DataFrame:
    query_terms = tokenize(search_profile)
    if not query_terms:
        return pd.DataFrame()

    requested_proteins = _detect_proteins(query_terms)
    compatible_proteins = _expand_compatible_proteins(requested_proteins)

    scored_rows = []
    for _, recipe in recipes.iterrows():
        score = 0
        matched_terms = set()
        recipe_terms = _recipe_terms(recipe)
        recipe_proteins = _detect_proteins(recipe_terms)

        if requested_proteins and not recipe_proteins.intersection(compatible_proteins):
            continue

        direct_protein_matches = recipe_proteins.intersection(requested_proteins)
        compatible_protein_matches = recipe_proteins.intersection(compatible_proteins)
        if direct_protein_matches:
            score += len(direct_protein_matches) * PROTEIN_MATCH_BONUS
            matched_terms.update(direct_protein_matches)
        elif compatible_protein_matches:
            score += len(compatible_protein_matches) * COMPATIBLE_PROTEIN_BONUS
            matched_terms.update(compatible_protein_matches)

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
            scored["main_protein"] = ", ".join(sorted(direct_protein_matches or compatible_protein_matches))
            scored_rows.append(scored)

    if not scored_rows:
        return pd.DataFrame()

    return (
        pd.DataFrame(scored_rows)
        .sort_values(["score", "prep_time"], ascending=[False, True])
        .head(limit)
    )


def _recipe_terms(recipe: pd.Series) -> set[str]:
    text = " ".join(
        str(recipe.get(field, ""))
        for field in ["name", "ingredients", "tags", "cuisine", "meal_type"]
    )
    return tokenize(text)


def _detect_proteins(terms: set[str]) -> set[str]:
    detected = set()
    for protein, aliases in PROTEIN_ALIASES.items():
        if terms.intersection(aliases):
            detected.add(protein)
    return detected


def _expand_compatible_proteins(proteins: set[str]) -> set[str]:
    compatible = set()
    for protein in proteins:
        compatible.update(PROTEIN_COMPATIBILITY.get(protein, {protein}))
    return compatible
