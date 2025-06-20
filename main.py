import pandas as pd

from backend.modules.common.repositories import StockRepo
from backend.modules.data_explorer.corporate.repositories import TradingDataDailyRepo
from backend.modules.strategies import HeadAndShouldersStrategy
from backend.modules.pattern_detector import PatternDetector


if __name__ == '__main__':
    stocks = StockRepo.get_all()
    stocks = [s["ticker"] for s in stocks if s["exchangeCode"] in ["HOSE", "HNX", "UPCOM"]]

    for stock in stocks:
        print("=" * 50)
        print(f"[PROCESSING] Detecting patterns for stock: {stock}")
        raw_data = TradingDataDailyRepo.get_by_condition({"ticker": stock})
        df = pd.DataFrame(raw_data)
        df = df[["paramDate", "ticker", "OpenPrice", "HighPrice", "LowPrice", "ClosePrice"]].copy().dropna()
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
            for i, p in enumerate(results["Head and Shoulders"]):
                hs_strategy.plot_pattern(candle_data=df, pat=p)
        print(f"[DONE] Detecting patterns for stock: {stock}")


