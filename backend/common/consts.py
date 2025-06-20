import os
import urllib.parse
import datetime
import ast


class Consts:
    BASE_DIR = os.path.abspath(os.path.join(__file__, "../" * 3))
    TMP_DIR = os.path.join(BASE_DIR, "tmp")
    DATABASE_TIME_FORMAT = "yyyy-MM-dd HH:mm:ss"
    DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
    DATE_FORMAT = "%Y-%m-%d"
    TIME_FORMAT = "%H:%M:%S"
    GMT_7_NOW = f"SWITCHOFFSET(SYSUTCDATETIME(), '+07:00')"
    GMT_7_NOW_VARCHAR = f"FORMAT(SWITCHOFFSET(SYSUTCDATETIME(), '+07:00'), 'yyyy-MM-dd HH:mm:ss')"

    APP_FIINX_COMMON_SCHEMA = "appFiinxCommon"
    APP_FIINX_DATA_EXPLORER_CORPORATE_SCHEMA = "appFiinxDataExplorerCorporate"
    APP_FIINX_DATA_EXPLORER_INDEX_SECTOR_SCHEMA = "appFiinxDataExplorerIndexSector"
    APP_FIINX_MARKET_DERIVATIVE_SCHEMA = "appFiinxMarketDerivative"
    APP_FIINX_MARKET_FUND_SCHEMA = "appFiinxFund"
    APP_FIINX_MASTER_DATA_SCHEMA = "appFiinxMasterData"
    APP_FIINX_FINANCIAL_STATEMENT_SCHEMA = "appFiinxFinancialStatement"
    APP_FIINX_MACRO_SCHEMA = "appFiinxMacro"

    ISO_LEVEL_UNCOMMITTED = "SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;"

    MAP_FIELD_CODE_CONFIG_FOLDER = os.path.join(BASE_DIR, "backend/map_field_code_configs")
    FIINX_AUTH_URL = "https://auth.fiingroup.vn"
    FIINX_API_URL = "https://fiinx-product-api.fiingroup.vn"
    DATA_EXPLORER_CORPORATE_URL = f"{FIINX_API_URL}/search/v1/DataExplorer/Corporate/Query"
    DATA_EXPLORER_INDEX_SECTOR_URL = f"{FIINX_API_URL}/search/v1/DataExplorer/IndexSector/Query"

    FINANCIAL_STATEMENT_BS_URL = f"{FIINX_API_URL}/profile/v1/Corporate/GetFinancialDataBalanceSheet?Consolidated=true&CommonSize=false"
    FINANCIAL_STATEMENT_IS_URL = f"{FIINX_API_URL}/profile/v1/Corporate/GetFinancialDataIncomeStatement?Consolidated=true&CommonSize=false"
    FINANCIAL_STATEMENT_CF_URL = f"{FIINX_API_URL}/profile/v1/Corporate/GetFinancialDataCashFlow?Consolidated=true&CommonSize=false"
    FINANCIAL_STATEMENT_NO_URL = f"{FIINX_API_URL}/profile/v1/Corporate/GetFinancialDataNote?Consolidated=true&CommonSize=false"

    EXCHANGE_RATE_URL = f"{FIINX_API_URL}/economy/v1/Economy/Monetary/Currency/ExchangeRate"
    INTEREST_RATE_BANK_URL = f"{FIINX_API_URL}/economy/v1/Economy/InterestRate/StatisticOtherBank"
    INTEREST_RATE_SBV_URL = f"{FIINX_API_URL}/economy/v1/Economy/InterestRate/StatisticStateBank"

    FIINX_USER_NAME = os.environ["FIINX_USER_NAME"]
    FIINX_PASSWORD = os.environ["FIINX_PASSWORD"]
    FIINX_DEVICE_ID = os.environ["FIINX_DEVICE_ID"]
    FIINX_INIT_AUTH_TIME = os.environ["FIINX_INIT_AUTH_TIME"]

    START_TRADING_DAY = datetime.datetime(day=1, month=1, year=2014) # datetime.datetime(day=24, month=2, year=2009)
    START_TRADING_MONTH = '2014-01'
    START_FINANCIAL_STATEMENT_QUARTER = '2007-Q1'
    START_YEAR = 2009
    TRADING_DAY_FORMAT = "%Y-%m-%d"
    YEAR_FORMAT = "%Y"
