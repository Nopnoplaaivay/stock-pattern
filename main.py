import pandas as pd

from src.strategies import HeadAndShouldersStrategy
from src.pattern_detector import PatternDetector



if __name__ == '__main__':
    df = pd.read_csv('data/BTCUSDT3600.csv')

    detector = PatternDetector(df)
    detector.add_strategy(HeadAndShouldersStrategy(order=6))

    results = detector.run()

    if "Head and Shoulders" in results:
        first_hs_pattern = results["Head and Shoulders"][0]
        hs_strategy = [s for s in detector.strategies if s.name == "Head and Shoulders"][0]
        # hs_strategy.plot_pattern(candle_data=df, pat=first_hs_pattern)

        # plot 5 mẫu hình gần nhất
        for pat in results["Head and Shoulders"][:2]:
            hs_strategy.plot_pattern(candle_data=df, pat=pat)

