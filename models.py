from typing import List, Optional ,NamedTuple
from dataclasses import dataclass


class WordConfidence(NamedTuple):
    word: str
    score: float


class SimilarPayload(NamedTuple):
    words: List[WordConfidence]


class ErrorPaylod(NamedTuple):
    error: str
