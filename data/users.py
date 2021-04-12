from sqlalchemy import orm, Integer, String, Column, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .dbSession import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    surname = Column(String, nullable=True)
    name = Column(String, nullable=True)
    email = Column(String, index=True, unique=True, nullable=True)
    onRent = Column(Boolean, nullable=True);
    hashedPassword = Column(String, nullable=True)

    def __repr__(self):
        return f'<User> {self.id} {self.surname} {self.name}'

    def setPassword(self, password):
        self.hashedPassword = generate_password_hash(password)

    def checkPassword(self, password):
        return check_password_hash(self.hashedPassword, password)
