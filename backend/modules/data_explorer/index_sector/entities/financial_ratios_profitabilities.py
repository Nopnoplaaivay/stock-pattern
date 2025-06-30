import sqlalchemy
from sqlalchemy import text

from backend.common.consts import Consts
from backend.modules.base_entities import Base
from backend.utils.udtt_utils import UdttUtils


class DEISFinancialRatiosProfitabilitiesEntity(Base):
    __tablename__ = "financialRatiosProfitabilities"
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

    RT0003 = sqlalchemy.Column(sqlalchemy.FLOAT)
    RT0004 = sqlalchemy.Column(sqlalchemy.FLOAT)
    RT0048 = sqlalchemy.Column(sqlalchemy.FLOAT)
    RT0049 = sqlalchemy.Column(sqlalchemy.FLOAT)
    RT0050 = sqlalchemy.Column(sqlalchemy.FLOAT)
    RT0051 = sqlalchemy.Column(sqlalchemy.FLOAT)
    RT0052 = sqlalchemy.Column(sqlalchemy.FLOAT)
    RT0053 = sqlalchemy.Column(sqlalchemy.FLOAT)
    RT0054 = sqlalchemy.Column(sqlalchemy.FLOAT)
    RT0348 = sqlalchemy.Column(sqlalchemy.FLOAT)

    @classmethod
    def generate_type(cls) -> str:
        sql_query = UdttUtils.generate_type(entity=cls)
        return sql_query
