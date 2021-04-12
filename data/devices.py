from sqlalchemy import orm, Integer, String, Column, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.orderinglist import ordering_list
from .dbSession import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin

class Device(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'devices'

    id = Column(Integer, primary_key=True, autoincrement=True)
    state = Column(Boolean, nullable=True)
    count = Column(Integer, nullable=True)

    def __repr__(self):
        return f'<Device> {self.id} {self.state}'