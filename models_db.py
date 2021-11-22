from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

films_genres = Table(
    "films_genres",
    Base.metadata,
            Column("film_id", Integer, ForeignKey("films.film_id")),
    Column("genre_id", Integer, ForeignKey("genres.genre_id"))
)


class Films(Base):
    __tablename__ = 'films'
    film_id = Column(Integer, primary_key=True)
    title = Column(String(50))
    description = Column(String)
    released_year = Column(Integer)
    director_id = Column(Integer, ForeignKey('directors.director_id'))
    user_id = Column(Integer, ForeignKey('users.user_id'))
    rating = Column(Integer)
    poster = Column(String)
    genres = relationship("Genres", secondary=films_genres, back_populates="films")


class Genres(Base):
    __tablename__ = "genres"
    genre_id = Column(Integer, primary_key=True)
    genre = Column(String(50))
    films = relationship("Films", secondary=films_genres, back_populates="genres")


class Directors(Base):
    __tablename__ = "directors"
    director_id = Column(Integer, primary_key=True)
    name = Column(String(255))
    films = relationship("Films", backref="directors")


class Users(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    user_name = Column(String(255))
    user_status = Column(String(50))
    user_password = Column(String(50))
    films = relationship("Films", backref="users")






