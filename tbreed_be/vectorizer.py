from sentence_transformers import SentenceTransformer
from gensim.models import Doc2Vec, Word2Vec
from gensim.models.doc2vec import TaggedDocument
from abc import ABC, abstractmethod
from typing import List

class VectorizerBase(ABC):
    def __init__(self, model_name: str):
        self.model_name = model_name

    @abstractmethod
    def vectorize(self, emails: List[str]):
        pass

class SentenceTransformerVectorizer(VectorizerBase):
    def __init__(self, model_name: str):
        super().__init__(model_name)
        self.model = SentenceTransformer(model_name)

    def vectorize(self, emails: List[str]):
        return self.model.encode(emails, show_progress_bar=True)

class BaseWordEmbeddingVectorizer(VectorizerBase):
    @abstractmethod
    def _train_model(self, tagged_documents, model_params=None):
        pass

    @abstractmethod
    def _infer_vectors(self, model, tagged_data):
        pass

    def vectorize(self, emails: List[str]):
        tagged_data = [TaggedDocument(words=email.split(), tags=[str(i)]) for i, email in enumerate(emails)]
        model = self._train_model(tagged_data)
        vectors = self._infer_vectors(model, tagged_data)
        return vectors

class Doc2VecVectorizer(BaseWordEmbeddingVectorizer):
    def _train_model(self, tagged_documents, vector_size=384, window=10, epochs=20, min_count=3):
        print("Doc2Vec chosen")
        model = Doc2Vec(
            vector_size=vector_size,
            window=window,
            epochs=epochs,
            workers=16,
            min_count=min_count
        )
        print(f"Training model with {len(tagged_documents)} documents")
        model.build_vocab(tagged_documents)
        model.train(tagged_documents, total_examples=model.corpus_count, epochs=model.epochs)
        return model

    def _infer_vectors(self, model, tagged_data):
        return [model.infer_vector(email.words) for email in tagged_data]

class Word2VecVectorizer(BaseWordEmbeddingVectorizer):
    def _train_model(self, tagged_documents, vector_size=100, window=5, epochs=20, min_count=5):
        print("Word2Vec chosen")
        model = Word2Vec(
            vector_size=vector_size,
            window=window,
            epochs=epochs,
            min_count=min_count,
            workers=16
        )
        print(f"Training model with {len(tagged_documents)} documents")
        model.build_vocab(tagged_documents)
        model.train(tagged_documents, total_examples=model.corpus_count, epochs=model.epochs)
        return model

    def _infer_vectors(self, model, tagged_data):
        return [model.wv[email.words] for email in tagged_data]