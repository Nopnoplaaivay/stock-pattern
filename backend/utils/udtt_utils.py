import sqlalchemy
from sqlalchemy import text
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.orm import Session
from backend.utils.logger import LOGGER


class UdttUtils:

    @classmethod
    def create_all_udtt(cls, base: DeclarativeMeta, session: Session, verbose: bool = True):
        """
        Tạo tất cả SQL Server Table Types (__sqlServerType__) cho các entity kế thừa từ `base`.

        Mỗi entity cần có:
        - __sqlServerType__: tên type theo format [schema].[type_name]
        - generate_type(): trả về câu lệnh CREATE TYPE AS TABLE (...)
        """

        for mapper in base.registry.mappers:
            entity_cls  = mapper.class_
            if hasattr(entity_cls, "__sqlServerType__") and hasattr(entity_cls, "generate_type"):
                sqlServerType = getattr(entity_cls, "__sqlServerType__")
                schema, type_name = sqlServerType.replace('[', '').replace(']', '').split('.')
                create_sql = entity_cls.generate_type()

                check_sql = f"""
                    IF NOT EXISTS (
                        SELECT * FROM sys.types t
                        JOIN sys.schemas s ON t.schema_id = s.schema_id
                        WHERE t.is_table_type = 1 AND s.name = '{schema}' AND t.name = '{type_name}'
                    )
                    BEGIN
                        {create_sql}
                    END
                    """
                if verbose:
                    LOGGER.info(f"Checking/Creating Type: {sqlServerType}")

                session.execute(text(check_sql.strip()))
        return True

    @classmethod
    def generate_type(cls, entity) -> str:
        """
        Sinh câu lệnh CREATE TYPE [schema].[name] AS TABLE (...) từ các cột của entity.
        """
        column_defs = []

        for col in entity.__table__.columns:
            col_type = col.type
            type_name = col_type.__class__.__name__

            if isinstance(col_type, (sqlalchemy.VARCHAR, sqlalchemy.NVARCHAR)):
                length = getattr(col_type, 'length', None)
                if length is None:
                    length = 255  # mặc định
                type_str = f"{type_name}({length})"
            elif isinstance(col_type, sqlalchemy.TEXT):
                type_str = "TEXT"
            elif isinstance(col_type, sqlalchemy.BIGINT):
                type_str = "BIGINT"
            elif isinstance(col_type, sqlalchemy.INTEGER):
                type_str = "INT"
            elif isinstance(col_type, sqlalchemy.FLOAT):
                type_str = "FLOAT"
            else:
                continue  # Bỏ qua kiểu chưa hỗ trợ

            column_defs.append(f"\t[{col.name}] {type_str}")

        columns_sql = ",\n".join(column_defs)

        sql_query = f"""CREATE TYPE {entity.__sqlServerType__} AS TABLE ( 
          {columns_sql}
          )""".strip()

        return sql_query
