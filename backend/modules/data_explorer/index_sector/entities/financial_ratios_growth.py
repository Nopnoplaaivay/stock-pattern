import sqlalchemy
from sqlalchemy import text

from backend.common.consts import Consts
from backend.modules.base_entities import Base
from backend.utils.udtt_utils import UdttUtils


class DEISFinancialRatiosGrowthEntity(Base):
    __tablename__ = "financialRatiosGrowth"
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

    RT0096 = sqlalchemy.Column(sqlalchemy.FLOAT)
    RT0097 = sqlalchemy.Column(sqlalchemy.FLOAT)
    RT0098 = sqlalchemy.Column(sqlalchemy.FLOAT)
    RT0099 = sqlalchemy.Column(sqlalchemy.FLOAT)
    RT0100 = sqlalchemy.Column(sqlalchemy.FLOAT)
    RT0101 = sqlalchemy.Column(sqlalchemy.FLOAT)
    RT0110 = sqlalchemy.Column(sqlalchemy.FLOAT)
    RT0111 = sqlalchemy.Column(sqlalchemy.FLOAT)
    RT0115 = sqlalchemy.Column(sqlalchemy.FLOAT)
    RT0116 = sqlalchemy.Column(sqlalchemy.FLOAT)
    RT0117 = sqlalchemy.Column(sqlalchemy.FLOAT)
    RT0118 = sqlalchemy.Column(sqlalchemy.FLOAT)
    RT0119 = sqlalchemy.Column(sqlalchemy.FLOAT)
    RT0124 = sqlalchemy.Column(sqlalchemy.FLOAT)
    RT0125 = sqlalchemy.Column(sqlalchemy.FLOAT)
    RT0131 = sqlalchemy.Column(sqlalchemy.FLOAT)
    RT0169 = sqlalchemy.Column(sqlalchemy.FLOAT)
    RT0109 = sqlalchemy.Column(sqlalchemy.FLOAT)
    RTD0059 = sqlalchemy.Column(sqlalchemy.FLOAT)

    @classmethod
    def generate_type(cls) -> str:
        sql_query = UdttUtils.generate_type(entity=cls)
        return sql_query
