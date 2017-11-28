from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

# engine = create_engine(location, echo = True)
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    name = Column(String, nullable=False) # Cannot be Empty
    username = Column(String, unique=True, nullable=False) # cannot be empty
    password = Column(String, nullable=False) # cannot be empty
    birth_date = Column(String, nullable=False)
    comments = relationship('Comment')

    def __repr__(self):
        return "<User(name='%s', username='%s', password='%s', birth_date='%s')>" % (
                self.name, self.username, self.password, self.birth_date)

class Game(Base):
    __tablename__ = 'game'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    title = Column(String, nullable=False)
    summary = Column(String)
    rating = Column(Integer, nullable=False)
    genre = relationship('Genre')
    developed_by = relationship('Developer')
    published_by = relationship('Published')
    comments = relationship('Comment')

    def __repr__(self):
        return "<Game(title='%s', summary='%s', rating='%s')>" % (
                self.title, self.summary, self.rating)


class Genre(Base):
    __tablename__ = 'Genre'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    genre = Column(String, nullable=False)
    game_id = Column(Integer, ForeignKey('game.id'))


class Console(Base):
    __tablename__ = 'console'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    name = Column(String, unique=True, nullable=False)
    bio = Column(String, nullable=False)
    release = Column(String, nullable=False)

    def __repr__(self):
        return "<Console(name='%s', bio='%s', release='%s')>" % (
         self.name, self.bio, self.release)

class Company(Base):
    __tablename__ = 'company'

    id = Column(Integer, primary_key=True,unique=True, nullable=False)
    name = Column(String, unique=True, nullable=False)
    location = Column(String, nullable=False)
    established = Column(String, nullable=False)
    # games produced
    # games developed
    # consoles made
    publishers = relationship("Publisher")
    developers = relationship("Developer")

    def __repr__(self):
        return "<Company(name='%s', location='%s')>" % (
            self.name, self.location)


# Company child class, indicates if a company is a developer
class Publisher(Base):
    __tablename__ = 'publisher'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    company_id = Column(Integer, ForeignKey('company.id'))
    published = relationship('Published')


# Company child class, indicates if a company is a developer
class Developer(Base):
    __tablename__ = 'developer'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    company_id = Column(Integer, ForeignKey('company.id'))
    developed = relationship("Developed")


# The user rates a game
class Rate(Base):
    __tablename__= 'Rate'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    rating = Column(Integer, nullable=False)

    user_id = Column(Integer, ForeignKey('user.id'))
    game_id = Column(Integer, ForeignKey('game.id'))

    user = relationship('User', back_populates='rated')

    def __repr__(self):
        return "<Rate(rating='%d')>" % (
            self.rating)


class Comment(Base):
    __tablename__ = 'comment'

    id = Column(Integer, primary_key=True)
    com = Column(String, nullable=False)

    user_id = Column(Integer, ForeignKey('user.id'))
    game_id = Column(Integer, ForeignKey('game.id'))


# this table holds developers and the games they have developed
class Developed(Base):
    __tablename__ = 'developed'

    id = Column(Integer, primary_key=True)
    developer_id = Column(Integer, ForeignKey('developer.id'))
    game_id = Column(Integer, ForeignKey('game.id'))


# this table holds publishers and the games they have published
class Published(Base):
    __tablename__ = 'published'

    id = Column(Integer, primary_key=True)
    publisher_id = Column(Integer, ForeignKey('publisher.id'))
    game_id = Column(Integer, ForeignKey('game.id'))


class Available(Base):
    __tablename__ = 'available'

    id = Column(Integer, primary_key=True)
    console_id = Column(Integer, ForeignKey='console.id')
    game_id = Column(Integer, ForeignKey='game.id')


class Created(Base):
    __tablename__ = 'created'

    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey='company.id')
    console_id = Column(Integer, ForeignKey='console.id')