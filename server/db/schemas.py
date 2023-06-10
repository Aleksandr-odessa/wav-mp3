from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'
    id_user = Column(String, primary_key=True)
    token = Column(String)
    name = Column(String, unique=True)


class Audio(Base):
    __tablename__ = 'audio'
    file_id = Column(String, primary_key=True)
    audio_file = Column(String)
    users_id = Column(String, ForeignKey('users.id_user'))
    user = relationship("Users")
