import sqlalchemy
from sqlalchemy import text

from backend.common.consts import Consts
from backend.modules.base_entities import Base
from backend.utils.udtt_utils import UdttUtils


class DEISFinancialRatiosBankingRatioEntity(Base):
    __tablename__ = "financialRatiosBankingRatio"
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

    EquityPerAssets = sqlalchemy.Column(sqlalchemy.FLOAT)
    EquityPerLiability = sqlalchemy.Column(sqlalchemy.FLOAT)
    EquityPerLoan = sqlalchemy.Column(sqlalchemy.FLOAT)
    RT0234 = sqlalchemy.Column(sqlalchemy.FLOAT)
    RT0237 = sqlalchemy.Column(sqlalchemy.FLOAT)
    RT0238 = sqlalchemy.Column(sqlalchemy.FLOAT)
    RT0239 = sqlalchemy.Column(sqlalchemy.FLOAT)
    RT0251 = sqlalchemy.Column(sqlalchemy.FLOAT)
    RT0252 = sqlalchemy.Column(sqlalchemy.FLOAT)
    RT0265 = sqlalchemy.Column(sqlalchemy.FLOAT)
    RT0266 = sqlalchemy.Column(sqlalchemy.FLOAT)
    RT0267 = sqlalchemy.Column(sqlalchemy.FLOAT)
    RT0269 = sqlalchemy.Column(sqlalchemy.FLOAT)
    RT0270 = sqlalchemy.Column(sqlalchemy.FLOAT)
    RT0271 = sqlalchemy.Column(sqlalchemy.FLOAT)
    RT0272 = sqlalchemy.Column(sqlalchemy.FLOAT)
    RT0273 = sqlalchemy.Column(sqlalchemy.FLOAT)
    RT0274 = sqlalchemy.Column(sqlalchemy.FLOAT)
    RT0277 = sqlalchemy.Column(sqlalchemy.FLOAT)
    RT0282 = sqlalchemy.Column(sqlalchemy.FLOAT)
    RT0285 = sqlalchemy.Column(sqlalchemy.FLOAT)
    RT0286 = sqlalchemy.Column(sqlalchemy.FLOAT)
    RT0287 = sqlalchemy.Column(sqlalchemy.FLOAT)
    RT0288 = sqlalchemy.Column(sqlalchemy.FLOAT)
    RT0295 = sqlalchemy.Column(sqlalchemy.FLOAT)
    RT0298 = sqlalchemy.Column(sqlalchemy.FLOAT)
    RT0300 = sqlalchemy.Column(sqlalchemy.FLOAT)
    RT0301 = sqlalchemy.Column(sqlalchemy.FLOAT)

    @classmethod
    def generate_type(cls) -> str:
        sql_query = UdttUtils.generate_type(entity=cls)
        return sql_query
