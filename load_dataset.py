from abc import abstractmethod, ABC
import pandas as pd


class Loader(ABC):
    @abstractmethod
    def load_dataset(self, path: str):
        pass


class CSVLoader(Loader):
    def load_dataset(self, path: str, chunksize: int = 4096):
        reader = pd.read_csv(path, chunksize)
        for chunk in reader:
            yield chunk