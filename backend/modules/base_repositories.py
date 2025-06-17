import math
import threading
from typing import List, TypeVar, Generic, Dict, Callable, Union

import numpy as np
import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, func, text, bindparam, values, update, and_
from sqlalchemy.sql.elements import BinaryExpression

from backend.modules.base_entities import Base
from backend.utils.data_utils import DataUtils
from backend.modules.query_builder import BaseQueryBuilder, TextSQL

T = TypeVar("T", bound=Base)


class BaseRepo(Generic[T]):
    entity: T = None
    query_builder: BaseQueryBuilder
    session_scope: Callable[..., Session]

    @classmethod
    def count_all_by_condition(cls, condition):
        with cls.session_scope() as session:
            record = session.query(cls.entity).filter(condition).count()
        return record


    @classmethod
    def get_by_condition_(cls, conditions) -> List[T]:
        with cls.session_scope() as session:
            records = session.query(cls.entity).filter(conditions).order_by(cls.entity.id.asc()).all()
            session.expunge_all()
        return records

    @classmethod
    def get_by_condition(cls, conditions: Dict):
        condition_query = cls.query_builder.where(conditions)
        sql = """
            SELECT *
            FROM
            %s
            WHERE %s
        """ % (
            cls.query_builder.full_table_name,
            condition_query.sql,
        )
        with cls.session_scope() as session:
            cur = session.connection().exec_driver_sql(sql, tuple(condition_query.params)).cursor
            records = cls.row_factory(cur=cur)
            return records

    @classmethod
    def get_all_entity(cls) -> List[T]:
        # sql = select(cls.entity)
        # with cls.session_scope() as session:
        #     results = session.execute(str(sql)).fetchall()
        # return [cls.entity(**result) for result in results]
        with cls.session_scope() as session:
            records = session.query(cls.entity).all()
            session.expunge_all()
        return records

    @classmethod
    def get_all(cls) -> List[Dict]:
        with cls.session_scope() as session:
            sql = (
                """
                SELECT *
                FROM %s
            """
                % cls.query_builder.full_table_name
            )
            cur = session.connection().exec_driver_sql(sql).cursor
            results = cls.row_factory(cur=cur)
        return results

    # new function
    @classmethod
    def row_factory(cls, cur) -> List[Dict]:
        if cur.description is None:
            return []
        columns = [column[0] for column in cur.description]
        results = []
        for row in cur.fetchall():
            results.append(dict(zip(columns, row)))
        return results
