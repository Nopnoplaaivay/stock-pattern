from typing import Optional
from sqlalchemy import select, and_
from backend.modules.query_builder import BaseQueryBuilder
from backend.modules.base_entities import Base
from backend.db.mssql_connector_lake import session_scope_lake
from backend.modules.base_repositories import BaseRepo
from backend.modules.common.entities import StockEntity


class StockRepo(BaseRepo[StockEntity]):
    entity = StockEntity
    query_builder = BaseQueryBuilder(entity=entity)
    session_scope = session_scope_lake

    @classmethod
    def get_all(cls):
        with cls.session_scope() as session:
            sql = (
                    """
                    SELECT *
                    FROM %s
                    order by id
                """
                    % cls.query_builder.full_table_name
            )
            cur = session.connection().exec_driver_sql(sql).cursor
            results = cls.row_factory(cur=cur)
            results = [result for result in results if result['exchangeCode'] in ['HOSE', 'HNX', 'UPCoM', 'OTC']]
            return results
