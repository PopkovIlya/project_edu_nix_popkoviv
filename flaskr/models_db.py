from flaskr import db, login_manager  # , ma
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


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
    director_id = db.Column(db.Integer, db.ForeignKey('directors.director_id'), default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), default=0)
    rating = db.Column(db.Integer, nullable=False)
    poster = db.Column(db.String, nullable=False)
    genres = db.relationship("Genres", secondary=films_genres, back_populates="films")


class Genres(db.Model):
    __tablename__ = "genres"
    genre_id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String(50), nullable=False)
    films = db.relationship("Films", secondary=films_genres, back_populates="genres")


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(Users).get(user_id)


class Users(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(255), unique=True)
    is_admin = db.Column(db.Boolean, default=False)
    user_password = db.Column(db.Text)
    user_email = db.Column(db.String(50), unique=True)
    films = db.relationship("Films", backref="users")

    def set_password(self, password):
        self.user_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.user_password, password)



if __name__ == '__main__':
#     db.create_all()
    db.drop_all()
