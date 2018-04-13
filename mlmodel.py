from gensim.models import KeyedVectors
from typing import List, NamedTuple
from models import WordConfidence

filename = 'GoogleNews-vectors-negative300-SLIM.bin'
model = KeyedVectors.load_word2vec_format(filename, binary=True)


def get_words(positive: List[str], negative: List[str] = [], num_words: int = 5) -> List[WordConfidence]:
    res = model.most_similar(positive=positive, negative=negative, topn=num_words)
    words_res = [WordConfidence(word=r[0], score=r[1]) for r in res]
    return words_res
