import sqlalchemy
from sqlalchemy import text

from backend.common.consts import Consts
from backend.modules.base_entities import Base
from backend.utils.udtt_utils import UdttUtils


class DEISFinancialRatiosFinancialStrengthEntity(Base):
    __tablename__ = "financialRatiosFinancialStrength"
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

    RT0018 = sqlalchemy.Column(sqlalchemy.FLOAT)
    RT0019 = sqlalchemy.Column(sqlalchemy.FLOAT)
    RT0020 = sqlalchemy.Column(sqlalchemy.FLOAT)
    RT0022 = sqlalchemy.Column(sqlalchemy.FLOAT)
    RT0023 = sqlalchemy.Column(sqlalchemy.FLOAT)
    RT0024 = sqlalchemy.Column(sqlalchemy.FLOAT)
    RT0025 = sqlalchemy.Column(sqlalchemy.FLOAT)
    RT0026 = sqlalchemy.Column(sqlalchemy.FLOAT)
    RT0027 = sqlalchemy.Column(sqlalchemy.FLOAT)
    RT0033 = sqlalchemy.Column(sqlalchemy.FLOAT)
    RT0034 = sqlalchemy.Column(sqlalchemy.FLOAT)

    @classmethod
    def generate_type(cls) -> str:
        sql_query = UdttUtils.generate_type(entity=cls)
        return sql_query
