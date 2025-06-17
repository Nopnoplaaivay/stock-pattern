from sqlalchemy.schema import CreateSchema

from backend.db.mssql_connector_lake import session_scope_lake
from backend.common.consts import Consts
from backend.utils.udtt_utils import UdttUtils

with session_scope_lake() as session:
    if Consts.APP_FIINX_COMMON_SCHEMA not in session.connection().dialect.get_schema_names(session.connection()):
        session.execute(CreateSchema(Consts.APP_FIINX_COMMON_SCHEMA))
    if Consts.APP_FIINX_DATA_EXPLORER_CORPORATE_SCHEMA not in session.connection().dialect.get_schema_names(session.connection()):
        session.execute(CreateSchema(Consts.APP_FIINX_DATA_EXPLORER_CORPORATE_SCHEMA))
    if Consts.APP_FIINX_DATA_EXPLORER_INDEX_SECTOR_SCHEMA not in session.connection().dialect.get_schema_names(session.connection()):
        session.execute(CreateSchema(Consts.APP_FIINX_DATA_EXPLORER_INDEX_SECTOR_SCHEMA))
    if Consts.APP_FIINX_MARKET_DERIVATIVE_SCHEMA not in session.connection().dialect.get_schema_names(session.connection()):
        session.execute(CreateSchema(Consts.APP_FIINX_MARKET_DERIVATIVE_SCHEMA))
    if Consts.APP_FIINX_MARKET_FUND_SCHEMA not in session.connection().dialect.get_schema_names(session.connection()):
        session.execute(CreateSchema(Consts.APP_FIINX_MARKET_FUND_SCHEMA))
    if Consts.APP_FIINX_MASTER_DATA_SCHEMA not in session.connection().dialect.get_schema_names(session.connection()):
        session.execute(CreateSchema(Consts.APP_FIINX_MASTER_DATA_SCHEMA))
    if Consts.APP_FIINX_FINANCIAL_STATEMENT_SCHEMA not in session.connection().dialect.get_schema_names(session.connection()):
        session.execute(CreateSchema(Consts.APP_FIINX_FINANCIAL_STATEMENT_SCHEMA))
    if Consts.APP_FIINX_MACRO_SCHEMA not in session.connection().dialect.get_schema_names(session.connection()):
        session.execute(CreateSchema(Consts.APP_FIINX_MACRO_SCHEMA))

from backend.modules.base_entities import Base


from backend.modules.common.entities import *
from backend.modules.data_explorer.corporate.entities import *

with session_scope_lake() as session:
    Base.metadata.create_all(bind=session.connection())
    UdttUtils.create_all_udtt(Base, session)

