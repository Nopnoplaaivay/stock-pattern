import pandas as pd

from src.strategies import HeadAndShouldersStrategy, FlagPennantsStrategy
from src.pattern_detector import PatternDetector



if __name__ == '__main__':
    df = pd.read_csv('data/BTCUSDT3600.csv')

    detector = PatternDetector(df)
    detector.add_strategy(HeadAndShouldersStrategy(order=6))
    detector.add_strategy(FlagPennantsStrategy(order=12))

    results = detector.run()

    if "Head and Shoulders" in results:
        first_hs_pattern = results["Head and Shoulders"][0]
        hs_strategy = [s for s in detector.strategies if s.name == "Head and Shoulders"][0]
        # hs_strategy.plot_pattern(candle_data=df, pat=first_hs_pattern)

        # plot 5 mẫu hình gần nhất
        # for pat in results["Head and Shoulders"][-1:]:
        #     hs_strategy.plot_pattern(candle_data=df, pat=pat)

    if "Flag Pennants" in results:
        first_fp_pattern = results["Flag Pennants"][0]
        fp_strategy = [s for s in detector.strategies if s.name == "Flag Pennants"][0]
        # fp_strategy.plot_pattern(candle_data=df, pat=first_fp_pattern)

        # plot 5 mẫu hình gần nhất
        for pat in results["Flag Pennants"][0:9]:
            fp_strategy.plot_pattern(candle_data=df, pat=pat)

