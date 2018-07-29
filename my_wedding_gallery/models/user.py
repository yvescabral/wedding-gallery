from sqlalchemy import (
    Column,
    String,
    Integer,
    ARRAY
)
from sqlalchemy.orm import relationship
from .meta import Base
from .photo import Photo
from .like import Like


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    groups = Column(ARRAY(String))
    photos = relationship(Photo, back_populates="user")
    likes = relationship(Like)

    def __init__(self, name, email, password, groups=None):
        self.name = name
        self.email = email
        self.password = password
        self.groups = groups or []
