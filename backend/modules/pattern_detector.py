import pandas as pd

from backend.modules.base_strategies import BasePatternStrategy

class PatternDetector:
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.strategies = []

    def add_strategy(self, strategy: BasePatternStrategy):
        self.strategies.append(strategy)

    def run(self):
        all_found_patterns = {}
        for strategy in self.strategies:
            found = strategy.find_patterns(self.data)
            if found:
                all_found_patterns[strategy.name] = found
                print(f"Found {len(found)} patterns for {strategy.name}")
        return all_found_patterns

