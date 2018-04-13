from typing import List, NamedTuple


class WordConfidence(NamedTuple):
    word: str
    score: float


class SimilarPayload(NamedTuple):
    words: List[WordConfidence]


class ErrorPaylod(NamedTuple):
    error: str
