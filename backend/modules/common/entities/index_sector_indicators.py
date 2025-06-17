import sqlalchemy
from sqlalchemy import text

from backend.common.consts import Consts
from backend.modules.base_entities import Base
from backend.utils.udtt_utils import UdttUtils


class IndexSectorIndicatorEntity(Base):
    __tablename__ = "indexSectorIndicators"
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

    groupId = sqlalchemy.Column(sqlalchemy.VARCHAR(36), server_default=text("LOWER(NEWID())"))
    indicatorAlias = sqlalchemy.Column(sqlalchemy.VARCHAR(36), server_default=text("LOWER(NEWID())"))
    indicatorId = sqlalchemy.Column(sqlalchemy.INT)
    parentIndicatorId = sqlalchemy.Column(sqlalchemy.INT)
    indicatorGroup = sqlalchemy.Column(sqlalchemy.VARCHAR(None))
    conditionType = sqlalchemy.Column(sqlalchemy.VARCHAR(None))
    orderNumber = sqlalchemy.Column(sqlalchemy.INT)
    indicatorName = sqlalchemy.Column(sqlalchemy.NVARCHAR(None))
    fieldCode = sqlalchemy.Column(sqlalchemy.VARCHAR(None))
    multiplier = sqlalchemy.Column(sqlalchemy.FLOAT)
    unit = sqlalchemy.Column(sqlalchemy.NVARCHAR(64))
    typeOf = sqlalchemy.Column(sqlalchemy.VARCHAR(64))
    pairIndicator = sqlalchemy.Column(sqlalchemy.INT)
    condition = sqlalchemy.Column(sqlalchemy.VARCHAR(None))

    @classmethod
    def generate_type(cls) -> str:
        sql_query = UdttUtils.generate_type(entity=cls)
        return sql_query
