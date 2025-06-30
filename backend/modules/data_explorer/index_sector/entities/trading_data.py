import sqlalchemy
from sqlalchemy import text

from backend.common.consts import Consts
from backend.modules.base_entities import Base
from backend.utils.udtt_utils import UdttUtils


class DEISTradingDataEntity(Base):
    __tablename__ = "tradingData"
    __table_args__ = ({"schema": Consts.APP_FIINX_DATA_EXPLORER_INDEX_SECTOR_SCHEMA},)
    __sqlServerType__ = f"[{Consts.APP_FIINX_DATA_EXPLORER_INDEX_SECTOR_SCHEMA}].[{__tablename__}]"

    __createdAt__ = sqlalchemy.Column(
        sqlalchemy.VARCHAR(20),
        nullable=False,
        server_default=text(f"FORMAT(SWITCHOFFSET(SYSUTCDATETIME(), '+07:00'), '{Consts.DATABASE_TIME_FORMAT}')"),
    )
    __updatedAt__ = sqlalchemy.Column(
        sqlalchemy.VARCHAR(20),
        nullable=False,
        server_default=text(f"FORMAT(SWITCHOFFSET(SYSUTCDATETIME(), '+07:00'), '{Consts.DATABASE_TIME_FORMAT}')"),
        default=text(f"FORMAT(SWITCHOFFSET(SYSUTCDATETIME(), '+07:00'), '{Consts.DATABASE_TIME_FORMAT}')"),
        onupdate=text(f"FORMAT(SWITCHOFFSET(SYSUTCDATETIME(), '+07:00'), '{Consts.DATABASE_TIME_FORMAT}')"),
    )
    __id__ = sqlalchemy.Column(sqlalchemy.BIGINT, primary_key=True, nullable=False, autoincrement=True)
    __hashID__ = sqlalchemy.Column(sqlalchemy.VARCHAR(32), nullable=False, unique=True)
    date = sqlalchemy.Column(sqlalchemy.VARCHAR(10))
    paramDate = sqlalchemy.Column(sqlalchemy.VARCHAR(None))
    id = sqlalchemy.Column(sqlalchemy.VARCHAR(None))
    icbCode = sqlalchemy.Column(sqlalchemy.VARCHAR(None))
    level = sqlalchemy.Column(sqlalchemy.INT)
    name = sqlalchemy.Column(sqlalchemy.NVARCHAR(None))
    dataType = sqlalchemy.Column(sqlalchemy.VARCHAR(None))

    Beta2Y = sqlalchemy.Column(sqlalchemy.FLOAT)
    Beta6M = sqlalchemy.Column(sqlalchemy.FLOAT)
    BetaAdjust2Y = sqlalchemy.Column(sqlalchemy.FLOAT)
    BetaAdjust6M = sqlalchemy.Column(sqlalchemy.FLOAT)
    CloseIndex = sqlalchemy.Column(sqlalchemy.FLOAT)
    ForeignBuyValueDeal = sqlalchemy.Column(sqlalchemy.FLOAT)
    ForeignBuyValueMatched = sqlalchemy.Column(sqlalchemy.FLOAT)
    ForeignBuyValueTotal = sqlalchemy.Column(sqlalchemy.FLOAT)
    ForeignBuyVolumeDeal = sqlalchemy.Column(sqlalchemy.FLOAT)
    ForeignBuyVolumeMatched = sqlalchemy.Column(sqlalchemy.FLOAT)
    ForeignBuyVolumeTotal = sqlalchemy.Column(sqlalchemy.FLOAT)
    ForeignCurrentRoom = sqlalchemy.Column(sqlalchemy.FLOAT)
    ForeignSellValueDeal = sqlalchemy.Column(sqlalchemy.FLOAT)
    ForeignSellValueMatched = sqlalchemy.Column(sqlalchemy.FLOAT)
    ForeignSellValueTotal = sqlalchemy.Column(sqlalchemy.FLOAT)
    ForeignSellVolumeDeal = sqlalchemy.Column(sqlalchemy.FLOAT)
    ForeignSellVolumeMatched = sqlalchemy.Column(sqlalchemy.FLOAT)
    ForeignSellVolumeTotal = sqlalchemy.Column(sqlalchemy.FLOAT)
    ForeignTotalRoom = sqlalchemy.Column(sqlalchemy.FLOAT)
    HighIndex = sqlalchemy.Column(sqlalchemy.FLOAT)
    IndexChange = sqlalchemy.Column(sqlalchemy.FLOAT)
    LowIndex = sqlalchemy.Column(sqlalchemy.FLOAT)
    OpenIndex = sqlalchemy.Column(sqlalchemy.FLOAT)
    PercentIndexChange = sqlalchemy.Column(sqlalchemy.FLOAT)
    TotalBidCount = sqlalchemy.Column(sqlalchemy.FLOAT)
    TotalBidVolume = sqlalchemy.Column(sqlalchemy.FLOAT)
    TotalBuyValue = sqlalchemy.Column(sqlalchemy.FLOAT)
    TotalBuyVolume = sqlalchemy.Column(sqlalchemy.FLOAT)
    TotalDealBuyValue = sqlalchemy.Column(sqlalchemy.FLOAT)
    TotalDealBuyVolume = sqlalchemy.Column(sqlalchemy.FLOAT)
    TotalDealSellValue = sqlalchemy.Column(sqlalchemy.FLOAT)
    TotalDealSellVolume = sqlalchemy.Column(sqlalchemy.FLOAT)
    TotalDealValue = sqlalchemy.Column(sqlalchemy.FLOAT)
    TotalDealVolume = sqlalchemy.Column(sqlalchemy.FLOAT)
    TotalMatchBuyValue = sqlalchemy.Column(sqlalchemy.FLOAT)
    TotalMatchBuyVolume = sqlalchemy.Column(sqlalchemy.FLOAT)
    TotalMatchSellValue = sqlalchemy.Column(sqlalchemy.FLOAT)
    TotalMatchSellVolume = sqlalchemy.Column(sqlalchemy.FLOAT)
    TotalMatchValue = sqlalchemy.Column(sqlalchemy.FLOAT)
    TotalMatchVolume = sqlalchemy.Column(sqlalchemy.FLOAT)
    TotalOfferCount = sqlalchemy.Column(sqlalchemy.FLOAT)
    TotalOfferVolume = sqlalchemy.Column(sqlalchemy.FLOAT)
    TotalSellValue = sqlalchemy.Column(sqlalchemy.FLOAT)
    TotalSellVolume = sqlalchemy.Column(sqlalchemy.FLOAT)
    TotalValue = sqlalchemy.Column(sqlalchemy.FLOAT)
    TotalVolume = sqlalchemy.Column(sqlalchemy.FLOAT)

    @classmethod
    def generate_type(cls) -> str:
        sql_query = UdttUtils.generate_type(entity=cls)
        return sql_query
