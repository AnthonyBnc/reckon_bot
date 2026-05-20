import re


STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "for",
    "i",
    "in",
    "is",
    "it",
    "me",
    "of",
    "on",
    "or",
    "the",
    "to",
    "want",
    "with",
}


def tokenize(text: str) -> set[str]:
    words = re.findall(r"[a-zA-Z]+", text.lower())
    return {word for word in words if len(word) > 2 and word not in STOP_WORDS}
