from typing import Optional
from sqlalchemy import select, and_
from backend.modules.query_builder import BaseQueryBuilder
from backend.modules.base_entities import Base
from backend.db.mssql_connector_lake import session_scope_lake
from backend.modules.base_repositories import BaseRepo
from backend.modules.data_explorer.index_sector.entities import DEISFinancialRatiosValuationEntity


class DEISFinancialRatiosValuationRepo(BaseRepo[DEISFinancialRatiosValuationEntity]):
    entity = DEISFinancialRatiosValuationEntity
    query_builder = BaseQueryBuilder(entity=entity)
    session_scope = session_scope_lake
