import uuid

from sqlalchemy import Column
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils import Timestamp, UUIDType

Base = declarative_base()


class CoreModel(Base, Timestamp):
    __abstract__ = True

    id = Column(UUIDType(binary=False), primary_key=True, index=True, default=uuid.uuid4)
