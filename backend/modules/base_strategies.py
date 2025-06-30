
from abc import ABC, abstractmethod
import pandas as pd

class BasePatternStrategy(ABC):
    @abstractmethod
    def find_patterns(self, data: pd.DataFrame):
        pass

    @abstractmethod
    def plot_pattern(self, price_df: pd.DataFrame, pat):
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass