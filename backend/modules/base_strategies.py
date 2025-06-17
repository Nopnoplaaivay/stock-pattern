
from abc import ABC, abstractmethod
import pandas as pd

class BasePatternStrategy(ABC):
    @abstractmethod
    def find_patterns(self, data: pd.DataFrame):
        pass

    @abstractmethod
    def plot_pattern(self, candle_data: pd.DataFrame, pattern_instance):
        pass

    @abstractmethod
    def transform_data(self, data: pd.DataFrame) -> pd.DataFrame:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass