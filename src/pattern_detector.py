from src.base_strategies import BasePatternStrategy
from src.strategies import HeadAndShouldersStrategy
import pandas as pd

class PatternDetector:
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.strategies = []

    def add_strategy(self, strategy: BasePatternStrategy):
        self.strategies.append(strategy)
        print(f"Đã thêm chiến lược: {strategy.name}")

    def run(self):
        all_found_patterns = {}
        for strategy in self.strategies:
            print(f"Đang quét bằng chiến lược: {strategy.name}...")
            found = strategy.find_patterns(self.data)
            if found:
                all_found_patterns[strategy.name] = found
                print(f"  -> Tìm thấy {len(found)} mẫu hình.")
        return all_found_patterns

