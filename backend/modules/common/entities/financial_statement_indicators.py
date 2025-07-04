import sqlalchemy
from sqlalchemy import text

from backend.common.consts import Consts
from backend.modules.base_entities import Base
from backend.utils.udtt_utils import UdttUtils


class FinancialStatementIndicatorEntity(Base):
    __tablename__ = "financialStatementIndicators"
    __table_args__ = ({"schema": Consts.APP_FIINX_COMMON_SCHEMA},)
    __sqlServerType__ = f"[{Consts.APP_FIINX_COMMON_SCHEMA}].[{__tablename__}]"

    createdAt = sqlalchemy.Column(
        sqlalchemy.VARCHAR(20),
        nullable=False,
        server_default=text(f"FORMAT(SWITCHOFFSET(SYSUTCDATETIME(), '+07:00'), '{Consts.DATABASE_TIME_FORMAT}')"),
    )
    updatedAt = sqlalchemy.Column(
        sqlalchemy.VARCHAR(20),
        nullable=False,
        server_default=text(f"FORMAT(SWITCHOFFSET(SYSUTCDATETIME(), '+07:00'), '{Consts.DATABASE_TIME_FORMAT}')"),
        default=text(f"FORMAT(SWITCHOFFSET(SYSUTCDATETIME(), '+07:00'), '{Consts.DATABASE_TIME_FORMAT}')"),
        onupdate=text(f"FORMAT(SWITCHOFFSET(SYSUTCDATETIME(), '+07:00'), '{Consts.DATABASE_TIME_FORMAT}')"),
    )
    id = sqlalchemy.Column(sqlalchemy.BIGINT, primary_key=True, nullable=False, autoincrement=True)

    indicatorMappingId = sqlalchemy.Column(sqlalchemy.INT)
    statement = sqlalchemy.Column(sqlalchemy.VARCHAR(None))
    comGroup = sqlalchemy.Column(sqlalchemy.VARCHAR(None))
    indicator = sqlalchemy.Column(sqlalchemy.VARCHAR(None))
    fieldName = sqlalchemy.Column(sqlalchemy.VARCHAR(None))
    parentField = sqlalchemy.Column(sqlalchemy.NVARCHAR(None))
    multiplier = sqlalchemy.Column(sqlalchemy.FLOAT)
    formating = sqlalchemy.Column(sqlalchemy.VARCHAR(None))
    formatingCommonSize = sqlalchemy.Column(sqlalchemy.VARCHAR(None))
    unit = sqlalchemy.Column(sqlalchemy.VARCHAR(None))
    order = sqlalchemy.Column(sqlalchemy.INT)

    @classmethod
    def generate_type(cls) -> str:
        sql_query = UdttUtils.generate_type(entity=cls)
        return sql_query
