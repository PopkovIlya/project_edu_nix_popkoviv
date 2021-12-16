from flaskr import db


class Directors(db.Model):
    __tablename__ = "directors"
    director_id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), default="unknown")
    films = db.relationship("Films", backref="directors")


films_genres = db.Table(
    "films_genres",
    db.Column("film_id", db.Integer, db.ForeignKey("films.film_id"), primary_key=True),
    db.Column("genre_id", db.Integer, db.ForeignKey("genres.genre_id"), primary_key=True)
)


class Films(db.Model):
    __tablename__ = "films"
    film_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    released_year = db.Column(db.Date, nullable=False)
    director_id = db.Column(db.Integer, db.ForeignKey('directors.director_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    poster = db.Column(db.String, nullable=False)
    genres = db.relationship("Genres", secondary=films_genres, back_populates="films")


class Genres(db.Model):
    __tablename__ = "genres"
    genre_id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String(50), nullable=False)
    films = db.relationship("Films", secondary=films_genres, back_populates="genres")


class Users(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(255))
    user_status = db.Column(db.String(50))
    user_password = db.Column(db.String(50))
    user_email = db.Column(db.String(50))
    films = db.relationship("Films", backref="users")


