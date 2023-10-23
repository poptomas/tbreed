from abc import ABC, abstractmethod


class Vectorizer(ABC):
    @abstractmethod
    def vectorize(self, data: str):
        pass


class DummyVectorizer(Vectorizer):
    def vectorize(self, data: str):
        return data