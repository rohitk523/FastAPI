from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from db_database import Base


class User(Base):
    __tablename__ = "users"

    uuid = Column(String, primary_key=True, index=True)
    username = Column(String)

    textFiles = relationship('file_data',back_populates='creator')

    
class file_data(Base):
    __tablename__ = "textFiles"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    length = Column(Integer)
    user_id = Column(Integer,ForeignKey("users.uuid"))
    creator = relationship("User", back_populates="textFiles")
