import pandas as pd

from backend.modules.data_explorer.corporate.repositories import TradingDataDailyRepo
from backend.modules.strategies import HeadAndShouldersStrategy
from backend.modules.pattern_detector import PatternDetector


if __name__ == '__main__':
    stock = "BSI"
    raw_data = TradingDataDailyRepo.get_by_condition({"ticker": stock})
    df = pd.DataFrame(raw_data)
    df = df[["paramDate", "OpenPrice", "HighPrice", "LowPrice", "ClosePrice"]].copy().dropna()
    df["date"] = pd.to_datetime(df["paramDate"])
    df = df.set_index("date")
    df = df.sort_index()
    df = df.rename(columns={"OpenPrice": "open", "HighPrice": "high", "LowPrice": "low", "ClosePrice": "close"})


    detector = PatternDetector(df)
    detector.add_strategy(HeadAndShouldersStrategy(order=6))

    results = detector.run()

    if "Head and Shoulders" in results:
        first_hs_pattern = results["Head and Shoulders"][0]
        hs_strategy = [s for s in detector.strategies if s.name == "Head and Shoulders"][0]
        pat = results["Head and Shoulders"][1]
        for i, p in enumerate(results["Head and Shoulders"]):
            print(f"Pattern {i}: {p}")
            hs_strategy.plot_pattern(candle_data=df, pat=p)


