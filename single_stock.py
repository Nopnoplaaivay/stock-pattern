import pandas as pd

from backend.modules.common.repositories import StockRepo
from backend.modules.data_explorer.corporate.repositories import TradingDataDailyRepo
from backend.modules.data_explorer.index_sector.repositories import DEISTradingDataRepo
from backend.modules.strategies import (
    HeadAndShouldersStrategy,
    FlagPennantsStrategy,
    TripleTopStrategy
)
from backend.modules.pattern_detector import PatternDetector




if __name__ == '__main__':
        stock = "VCB"
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

        detector = PatternDetector(df)
        detector.add_strategy(HeadAndShouldersStrategy(order=6))
        detector.add_strategy(FlagPennantsStrategy(order=6))
        # detector.add_strategy(TripleTopStrategy(order=6))

        results = detector.run()

        if "Head and Shoulders" in results:
            first_hs_pattern = results["Head and Shoulders"][0]
            hs_strategy = [s for s in detector.strategies if s.name == "Head and Shoulders"][0]
            for i, pat in enumerate(results["Head and Shoulders"]):
                hs_strategy.plot_pattern(price_df=df, pat=pat)

        if "Flag Pennants" in results:
            first_fp_pattern = results["Flag Pennants"][0]
            fp_strategy = [s for s in detector.strategies if s.name == "Flag Pennants"][0]
            for i, pat in enumerate(results["Flag Pennants"]):
                fp_strategy.plot_pattern(price_df=df, pat=pat)

        if "Triple Top" in results:
            first_tt_pattern = results["Triple Top"][0]
            tt_strategy = [s for s in detector.strategies if s.name == "Triple Top"][0]
            for i, pat in enumerate(results["Triple Top"]):
                tt_strategy.plot_pattern(price_df=df, pat=pat)


        # export df to csv
        # df.to_csv(f"{stock}_patterns.csv")
        print(f"[DONE] Detecting patterns for stock: {stock}")


