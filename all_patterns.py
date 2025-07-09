import pandas as pd
import numpy as np

from backend.modules.common.repositories import StockRepo
from backend.modules.data_explorer.corporate.repositories import TradingDataDailyRepo
from backend.modules.data_explorer.index_sector.repositories import DEISTradingDataRepo
from backend.modules.strategies import (
    HeadAndShouldersStrategy,
    FlagPennantsStrategy,
    TripleTopStrategy,
    DoubleTopStrategy
)
from backend.modules.pattern_detector import PatternDetector


if __name__ == '__main__':
    stocks = StockRepo.get_all()
    stocks = [s["ticker"] for s in stocks if s["exchangeCode"] in ["HOSE", "HNX", "UPCOM"]]
    # them vnindex

    all_patterns_df = pd.DataFrame()
    for stock in stocks:
        print("=" * 50)
        print(f"[PROCESSING] Detecting patterns for stock: {stock}")
        raw_data = TradingDataDailyRepo.get_by_condition({"ticker": stock})
        raw_df = pd.DataFrame(raw_data)
        df = raw_df[["date", "ticker", "OpenPrice", "HighPrice", "LowPrice", "ClosePrice"]].copy().dropna()
        df["date"] = pd.to_datetime(df["date"])
        df["label"] = 0
        df["sessions_num"] = 0
        df = df.set_index("date")
        df = df.sort_index()
        df = df.rename(columns={"OpenPrice": "open", "HighPrice": "high", "LowPrice": "low", "ClosePrice": "close"})
        # df["close"] = np.log(df["close"])

        detector = PatternDetector(df)
        detector.add_strategy(HeadAndShouldersStrategy(order=6))
        # detector.add_strategy(FlagPennantsStrategy(order=6))
        # detector.add_strategy(TripleTopStrategy(order=6))
        # detector.add_strategy(DoubleTopStrategy(order=6))


        results = detector.run()

        if "Head and Shoulders" in results:
            first_hs_pattern = results["Head and Shoulders"][0]
            hs_strategy = [s for s in detector.strategies if s.name == "Head and Shoulders"][0]
            for i, p in enumerate(results["Head and Shoulders"]):
                hs_strategy.plot_pattern(price_df=df, pat=p)

        if "Flag Pennants" in results:
            first_hs_pattern = results["Flag Pennants"][0]
            hs_strategy = [s for s in detector.strategies if s.name == "Flag Pennants"][0]
            for i, pat in enumerate(results["Flag Pennants"]):
                hs_strategy.plot_pattern(price_df=df, pat=pat)

        if "Triple Top" in results:
            first_tt_pattern = results["Triple Top"][0]
            tt_strategy = [s for s in detector.strategies if s.name == "Triple Top"][0]
            for i, pat in enumerate(results["Triple Top"]):
                tt_strategy.plot_pattern(price_df=df, pat=pat)

        if "Double Top" in results:
            first_dt_pattern = results["Double Top"][0]
            dt_strategy = [s for s in detector.strategies if s.name == "Double Top"][0]
            for i, pat in enumerate(results["Double Top"]):
                dt_strategy.plot_pattern(price_df=df, pat=pat)

        all_patterns_df = pd.concat([all_patterns_df, df], axis=0)
        print(f"[DONE] Detecting patterns for stock: {stock}")
    # export all patterns df to csv
    # all_patterns_df.to_csv("all_patterns.csv", index=False)

