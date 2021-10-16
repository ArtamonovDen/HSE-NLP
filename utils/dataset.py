import pandas as pd
from torch.utils.data import Dataset
from .embedding import W2V


class NewsDataset(Dataset):
    """
    Dataset wrapper over pandas.DataFrame news corpus.
    """
    def __init__(self, news_df: pd.DataFrame, w2v_model: W2V, embeding_size: int = 300):

        self.w2v_model = w2v_model
        self.embeding_size = embeding_size
        self.tokens = news_df.tokens
        self.labels = news_df.labels

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        """
        Easy way to create embedding for a document - just get mean over all tokens
        """
        label = self.labels[idx]
        doc_embedding = self.w2v_model.make_doc_embedding(self.tokens[idx])
        return doc_embedding, label
