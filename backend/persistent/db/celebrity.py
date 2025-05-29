from persistent.db.base import Base
from sqlalchemy import Column, Text, Integer

class Celebrity(Base):
    """create table MyCeleb(
    id integer primary key,
    name text not null unique
    )   """

    __tablename__ = "celebrities"

    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(Text, nullable=False, unique=True)