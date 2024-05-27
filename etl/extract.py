import pandas as pd
from abc import ABC, abstractmethod

class DataLoader(ABC):
    @abstractmethod
    def load_data(self, file_path: str) -> pd.DataFrame:
        pass

class CSVDataLoader(DataLoader):
    def __init__(self, sheet_name: str=""):
        pass

    def load_data(self, file_path: str) -> pd.DataFrame:
        return pd.read_csv(file_path)