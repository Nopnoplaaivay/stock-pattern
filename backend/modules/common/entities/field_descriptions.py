import sqlalchemy
from sqlalchemy import text

from backend.common.consts import Consts
from backend.modules.base_entities import Base
from backend.utils.udtt_utils import UdttUtils


class FieldDescriptionEntity(Base):
    __tablename__ = "fieldDescriptions"
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
    schemaName = sqlalchemy.Column(sqlalchemy.VARCHAR(None), nullable=False)
    tableName = sqlalchemy.Column(sqlalchemy.VARCHAR(None), nullable=False)
    fieldCode = sqlalchemy.Column(sqlalchemy.VARCHAR(2048))
    mapEN = sqlalchemy.Column(sqlalchemy.VARCHAR(None))
    mapVN = sqlalchemy.Column(sqlalchemy.NVARCHAR(None))
    descriptionEN = sqlalchemy.Column(sqlalchemy.VARCHAR(None))
    descriptionVN = sqlalchemy.Column(sqlalchemy.NVARCHAR(None))
    multiplier = sqlalchemy.Column(sqlalchemy.VARCHAR(None))
    unit = sqlalchemy.Column(sqlalchemy.VARCHAR(None))

    @classmethod
    def generate_type(cls) -> str:
        sql_query = UdttUtils.generate_type(entity=cls)
        return sql_query
