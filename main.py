import pandas as pd

from src.strategies import HeadAndShouldersStrategy, FlagPennantsStrategy, DoubleTopStrategy
from src.pattern_detector import PatternDetector



if __name__ == '__main__':
    df = pd.read_csv('data/BTCUSDT3600.csv')

    detector = PatternDetector(df)
    detector.add_strategy(HeadAndShouldersStrategy(order=6))
    detector.add_strategy(FlagPennantsStrategy(order=12))
    # detector.add_strategy(DoubleTopStrategy(order=6))

    results = detector.run()

    if "Head and Shoulders" in results:
        first_hs_pattern = results["Head and Shoulders"][0]
        hs_strategy = [s for s in detector.strategies if s.name == "Head and Shoulders"][0]
        pat = results["Head and Shoulders"][0]
        hs_strategy.plot_pattern(candle_data=df, pat=pat)

    if "Flag Pennants" in results:
        first_fp_pattern = results["Flag Pennants"][0]
        fp_strategy = [s for s in detector.strategies if s.name == "Flag Pennants"][0]
        pat = results["Flag Pennants"][0]
        fp_strategy.plot_pattern(candle_data=df, pat=pat)

    if "Double Top" in results:
        first_dt_pattern = results["Double Top"][0]
        dt_strategy = [s for s in detector.strategies if s.name == "Double Top"][0]
        pat = results["Double Top"][-1]
        dt_strategy.plot_pattern(candle_data=df, pat=pat)

