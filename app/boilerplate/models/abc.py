import datetime
import enum
import uuid
import numpy

from psycopg2.extensions import register_adapter, AsIs
from sqlalchemy import inspect

from app import db


class BaseModel:
    print_filter = ()
    to_json_filter = ()

    def __init__(self,  **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self):
        """ Define a base way to print models
            Columns inside `print_filter` are excluded """
        return "%s(%s)" % (self.__class__.__name__, {
            column: value
            for column, value in self._to_dict().items()
            if column not in self.print_filter
        })

    @property
    def json(self):
        return self.to_json()

    def to_json(self, allow_none=False):
        """ Define a base way to jsonify models
            Columns inside `to_json_filter` are excluded """

        def get_value(value):
            if isinstance(value, BaseModel):
                return None
            if isinstance(value, uuid.UUID):
                return str(value)
            if isinstance(value, datetime.date):
                return value.isoformat()
            if isinstance(value, enum.Enum):
                return value.value
            return value

        return {
            column: get_value(value)
            for column, value in self._to_dict(allow_none).items()
            if not isinstance(value, list) and column not in self.to_json_filter
        }

    def _to_dict(self, allow_none=False):
        """ This would more or less be the same as a `to_json`
            But putting it in a "private" function
            Allows to_json to be overriden without impacting __repr__
            Or the other way around
            And to add filter lists """
        if allow_none:
            return {
                column.key: getattr(self, column.key)
                for column in inspect(self.__class__).attrs
            }
        return {
            column.key: getattr(self, column.key)
            for column in inspect(self.__class__).attrs if getattr(self, column.key)
        }

    # Method to save user to DB
    def save(self, commit=False, flush=False):
        db.session.add(self)
        if commit:
            db.session.commit()
        elif flush:
            db.session.flush()
            db.session.refresh(self)

    # Method to remove user from DB
    def remove(self, commit=False, flush=False):
        db.session.delete(self)
        if commit:
            db.session.commit()
        elif flush:
            db.session.flush()
            db.session.refresh(self)

    def refresh(self):
        db.session.refresh(self)


def addapt_numpy_float64(numpy_float64):
    return AsIs(numpy_float64)


def addapt_numpy_int64(numpy_int64):
    return AsIs(numpy_int64)


register_adapter(numpy.float64, addapt_numpy_float64)
register_adapter(numpy.int64, addapt_numpy_int64)
