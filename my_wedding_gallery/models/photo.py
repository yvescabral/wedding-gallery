from sqlalchemy import (
    Column,
    String,
    Integer,
    Boolean,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import relationship
from .meta import Base
from .like import Like


class Photo(Base):
    __tablename__ = 'photos'

    id = Column(Integer, primary_key=True)
    filename = Column(String, nullable=False)
    approved = Column(Boolean)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    uploaded_at = Column(DateTime, nullable=False)
    user = relationship("User", back_populates="photos")
    likes = relationship(Like)

    def get_url(self):
        return "https://s3.amazonaws.com/my-wedding-gallery/photos/%s" % self.filename

    def get_thumbnail_url(self):
        return "https://s3.amazonaws.com/my-wedding-gallery/photos/%s_t" % self.filename