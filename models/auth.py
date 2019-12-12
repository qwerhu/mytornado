from datetime import datetime
from sqlalchemy import (Column, String, Integer, DateTime, ForeignKey)
from sqlalchemy.orm import relationship
from models.db import Base, Session


class User(Base):

    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50))
    age = Column(Integer, nullable=True)
    gender = Column(String(20))
    emial = Column(String(60))
    power = Column(Integer, nullable=False, default=0)
    creatime = Column(DateTime, default=datetime.now)


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    image_url = Column(String(200))
    thumb_url = Column(String(200))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', backref='posts', uselist=False, cascade='all')

    def __repr__(self):
        return "<Post:#{}>".format(self.id)


class LikePost(Base):
    __tablename__ = 'likepost'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=True)
    user = relationship('User', backref='likeposts', uselist=False, cascade='all')
    posts = relationship('Post', backref='likeposts', uselist=False, cascade='all')


class Quotes(Base):
    __tablename__ = 'quotes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    author = Column(String(20))
    country = Column(String(10))
    quotes_content = Column(String(3000), nullable=False)


if __name__ == '__main__':
    Base.metadata.create_all()
