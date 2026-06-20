"""Public package API for qaznltk."""

from typing import List
from .exceptions import InvalidInputError, QazNLTKError, ResourceLoadError, UnsupportedFormatError
from .legacy import convert2cyrillic_iso9, convert2latin_iso9
from .metrics import bleu_score, calc_cer, calc_levenshtein_distance, calc_wer
from .qaznltk import QazNLTK
from .tfidf_vectorizer import KNN, QazNLTKVectorizer

__all__ = [
    "QazNLTK",
    "QazNLTKVectorizer",
    "KNN",
    "calc_similarity",
    "calc_cer",
    "calc_wer",
    "calc_levenshtein_distance",
    "get_stop_words",
    "get_positive_words",
    "get_negative_words",
    "get_kaz_alphabet",
    "bleu_score",
    "convert2latin_iso9",
    "convert2cyrillic_iso9",
    "tokenize",
    "sentimize",
    "sent_tokenize",
    "num2word",
    "get_info_from_iin",
    "QazNLTKError",
    "InvalidInputError",
    "ResourceLoadError",
    "UnsupportedFormatError",
]

__version__ = "1.3.0.0"

_instance = QazNLTK()

def get_stop_words() -> List[str]:
    return _instance.get_stop_words()

def get_negative_words() -> List[str]:
    return _instance.get_negative_words()

def get_positive_words() -> List[str]:
    return _instance.get_positive_words()

def get_kaz_alphabet() -> List[str]:
    return _instance.get_kaz_alphabet()

def calc_similarity(text_a: str, text_b: str) -> float:
    return _instance.calc_similarity(text_a, text_b)

def tokenize(text: str):
    return _instance.tokenize(text)

def sent_tokenize(text: str):
    return _instance.sent_tokenize(text)

def sentimize(text):
    return _instance.sentimize(text)

def num2word(n: int) -> str:
    return _instance.num2word(n)

def get_info_from_iin(iin: str) -> dict:
    return _instance.get_info_from_iin(iin)