import numpy as np
from typing import List
from gensim.models.keyedvectors import KeyedVectors


class W2V:
    """
    Wrapper for Gensim W2V model
    """
    def __init__(self, model: KeyedVectors, embeding_size: int):
        self.model = model
        self.embeding_size = embeding_size

    def make_embedding(self, token: str):
        """
        Makes embedding for single token
        """
        emb = np.zeros(self.embeding_size)
        try:
            emb = self.model[token]
        except KeyError:
            ...

        return emb

    def make_doc_embedding(self, doc: List[str]):
        """
        Makes embedding for a document as mean of tokens embedding
        """
        embeddings = np.zeros([len(doc), self.embeding_size])
        for i, token in enumerate(doc):
            embeddings[i] = self.make_embedding(token)

        return embeddings.mean(axis=0)
