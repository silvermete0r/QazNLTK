from __future__ import annotations

from typing import Sequence
from collections import Counter
from math import exp, log

from .utils import levenshtein_distance, normalize_text

def calc_cer(true_text: str, pred_text: str) -> float:
    """Calculate Character Error Rate (CER)."""
    true_text = normalize_text(true_text)
    pred_text = normalize_text(pred_text)
    if not true_text:
        return 0.0 if not pred_text else 1.0
    return levenshtein_distance(true_text, pred_text) / len(true_text)


def calc_wer(true_text: str, pred_text: str) -> float:
    """Calculate Word Error Rate (WER)."""
    true_text = normalize_text(true_text)
    pred_text = normalize_text(pred_text)
    true_words = tuple(true_text.split())
    pred_words = tuple(pred_text.split())
    if not true_words:
        return 0.0 if not pred_words else 1.0
    return levenshtein_distance(true_words, pred_words) / len(true_words)


def calc_levenshtein_distance(s1: str, s2: str) -> int:
    """Convenience wrapper for Levenshtein distance."""
    return levenshtein_distance(s1, s2)

def _extract_ngrams(tokens: list[str], n: int) -> Counter:
    return Counter(
        tuple(tokens[i : i + n])
        for i in range(len(tokens) - n + 1)
    )

def bleu_score(
    reference: Sequence[str],
    hypothesis: Sequence[str],
    max_n: int = 4,
    smooth: bool = True,
) -> float:
    """
    Compute corpus-level BLEU score.

    Parameters
    ----------
    reference : Sequence[str]
        Reference sentences.
    hypothesis : Sequence[str]
        Predicted sentences.
    max_n : int, default=4
        Maximum n-gram order.
    smooth : bool, default=True
        Apply add-one smoothing.

    Returns
    -------
    float
        BLEU score in [0, 1].
    """
    if not reference or not hypothesis:
        return 0.0

    ref_tokens = [
        token
        for sentence in reference
        for token in sentence.split()
    ]

    hyp_tokens = [
        token
        for sentence in hypothesis
        for token in sentence.split()
    ]

    if not hyp_tokens:
        return 0.0

    precisions = []

    for n in range(1, max_n + 1):
        hyp_ngrams = _extract_ngrams(hyp_tokens, n)

        if not hyp_ngrams:
            precisions.append(1.0 if smooth else 0.0)
            continue

        ref_ngrams = _extract_ngrams(ref_tokens, n)

        overlap = sum(
            min(count, ref_ngrams[ngram])
            for ngram, count in hyp_ngrams.items()
        )

        total = sum(hyp_ngrams.values())

        if smooth:
            precision = (overlap + 1) / (total + 1)
        else:
            precision = overlap / total if total else 0.0

        precisions.append(precision)

    # Geometric mean
    if min(precisions) == 0:
        geo_mean = 0.0
    else:
        geo_mean = exp(
            sum(log(p) for p in precisions) / max_n
        )

    # Brevity penalty
    ref_len = len(ref_tokens)
    hyp_len = len(hyp_tokens)

    if hyp_len == 0:
        return 0.0

    if hyp_len > ref_len:
        bp = 1.0
    else:
        bp = exp(1 - ref_len / hyp_len)

    return bp * geo_mean