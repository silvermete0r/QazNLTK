from __future__ import annotations

import re
from collections import Counter
from functools import lru_cache
from typing import Iterable, List, Sequence, Union

from .exceptions import InvalidInputError, ResourceLoadError


def normalize_text(text: str) -> str:
    """Normalize whitespace and lower-case text for comparisons."""
    if not isinstance(text, str):
        raise InvalidInputError("text must be a string")
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def tokenize_words(text: str) -> List[str]:
    """Split text into word tokens using a regex-based approach."""
    if not isinstance(text, str):
        raise InvalidInputError("text must be a string")
    return re.findall(r"\w+(?:-\w+)*", text.lower())


def compute_jaccard_similarity(str1: str, str2: str) -> float:
    """Calculate Jaccard similarity between two strings."""
    set1 = set(str1)
    set2 = set(str2)
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union else 0.0


@lru_cache(maxsize=None)
def levenshtein_distance(s1: Union[str, Sequence[str]], s2: Union[str, Sequence[str]]) -> int:
    """Calculate the Levenshtein distance between two strings or sequences."""
    if not isinstance(s1, (str, list, tuple)) or not isinstance(s2, (str, list, tuple)):
        raise InvalidInputError("Inputs must be strings or sequences of strings")

    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)

    previous_row = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def frequency_tokens(tokens: Iterable[str]) -> List[tuple]:
    """Return tokens sorted by frequency descending."""
    freqs = Counter(tokens)
    return sorted(freqs.items(), key=lambda item: item[1], reverse=True)