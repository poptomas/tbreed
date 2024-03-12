from abc import abstractmethod, ABC
import pandas as pd
from utils import benchmark

class Loader(ABC):
    @abstractmethod
    def load_dataset(self, path: str):
        pass


class CSVLoader(Loader):
    @benchmark
    def load_dataset(self, path: str):
        return pd.read_csv(path, engine="c")