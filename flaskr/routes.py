from flask import request, jsonify, make_response
from flask_restx import Resource
from flaskr import api, app
from flaskr import db
from flaskr.models_db import Films, Genres, Directors, Users, films_genres 
from flask_login import login_required, current_user, login_user, logout_user


@api.route('/login/')
class Login(Resource):
    """Method for authorizing a user"""
    def post(self):
        if current_user.is_authenticated:
            return {f"User {current_user.user_name}": "already authenticated"}
        else:
            user_email = request.json['user_email']
            password = request.json['user_password']
            user = Users.query.filter_by(user_email=user_email).first()
            print('user = ', user)
            if user and user.check_password(password):
                login_user(user)
                return {user.user_name: user.id}
        return {"Invalid": " username/password"}


@api.route('/logout/')
class Logout(Resource):
    """Method for logg out current user"""
    @login_required
    def get(self):
        user_name = current_user.user_name
        logout_user()

        return make_response(jsonify({f"{user_name}": ", have been logged out."}), 200)


@api.route('/directors')
class AllDirectorsAPI(Resource):
    def get(self):
        directors_list_db = Directors.query.all()
        directors_list_j = []
        for i in range(len(directors_list_db)):
            directors_list_j.append({"full_name": directors_list_db[i].full_name,
                                     "id": directors_list_db[i].director_id})
        return make_response(jsonify({"All directors": directors_list_j}), 200)

    def post(self):
        """Add new director"""
        new_director = Directors(full_name=request.json['full_name'])  # new_director_param) #)
        db.session.add(new_director)
        db.session.commit()
        return make_response(jsonify({"New director id": new_director.director_id}), 201)


@api.route('/directors/<int:director_id>')
class DirectorsApi(Resource):
    """Get, put, delete director by id"""
    def get(self, director_id):
        """Get director by id"""
        director = Directors.query.get(director_id)
        if director is None:
            return make_response(jsonify({"Director is not exists, director id = ": director_id}), 404)
        return make_response(jsonify({director.director_id: director.full_name}), 200)

    def put(self, director_id):
        """Update director by id"""
        director_to_update = Directors.query.get(director_id)
        if director_to_update is None:
            return make_response(jsonify({"Director is not exists, director id = ": director_id}), 404)
        request_data = request.get_json()
        director_to_update.full_name = request_data['full_name']
        db.session.commit()
        return make_response(jsonify({"Director updated": director_id}), 200)

    def delete(self, director_id):
        """Delete director by id"""
        director_to_delete = Directors.query.get(director_id)
        if director_to_delete is None:
            return make_response(jsonify({"Director is not exists, director_id = ": director_id}), 404)
        db.session.delete(director_to_delete)
        db.session.commit()
        return make_response(jsonify({"Director was deleted, director_id =": director_id}), 200)


@api.route('/films')
class FilmsAllAPI(Resource):
    """get all films or post film"""
    def get(self):
        films_list_db = Films.query.all()
        films_list_j = []
        for i in range(len(films_list_db)):
            films_list_j.append({
                "id": films_list_db[i].film_id,
                "title": films_list_db[i].title,
                "description": films_list_db[i].description,
                "released_year": films_list_db[i].released_year,
                "director_id": films_list_db[i].director_id,
                "added by user, id": films_list_db[i].user_id,
                "rating": films_list_db[i].rating,
                "poster": films_list_db[i].poster,
                "genres": films_list_db[i].genres
            })
        return make_response(jsonify({"All films": films_list_j}), 200)

    @login_required
    def post(self):
        """Create new film"""
        new_film = Films(
            title=request.json['title'],
            description=request.json['description'],
            released_year=request.json['released_year'],
            director_id=request.json['director_id'],
            user_id=request.json['user_id'],
            rating=request.json['rating'],
            poster=request.json['poster'],
        )

        for i in request.json['genres']:
            genre_1 = Genres.query.filter_by(genre_id=i).first()
            new_film.genres.append(genre_1)
        db.session.add(new_film)
        db.session.commit()
        return make_response(jsonify({"New film was added, it id is ": new_film.film_id}), 201)


@api.route('/films/<int:film_id>')
class FilmsApi(Resource):
    """get, put or delete film by id"""
    def get(self, film_id=None):
        """Get one film by id"""
        film = Films.query.get(film_id)
        if film is None:
            return make_response(jsonify({"Director is not exists, director id = ": film_id}), 404)
        director = Directors.query.filter_by(director_id=film.director_id)
        genres = [Genres.query.get(i).genre for i in film.genres]
        user = Users.query.filter_by(id=film.user_id)
        return make_response(jsonify({
            "film_id": film.film_id,
            "title": film.title,
            "description": film.description,
            "released_year": film.released_year,
            "director_id": director.full_name,
            "user_id": user.user_name,
            "rating": film.rating,
            "poster": film.poster,
            "genres": genres,
        }), 200)

    @login_required
    def put(self, film_id):
        """Update film object by id"""
        film_to_update = Films.query.get(film_id)
        if film_to_update is None:
            return make_response(jsonify({"Film is not exists, film_id = ": film_id}), 404)
        if current_user.id == film_to_update.user_id or current_user.is_admin:
            film_to_update.title = request.json['title']
            film_to_update.description = request.json['description']
            film_to_update.released_year = request.json['released_year']
            film_to_update.director_id = request.json['director_id']
            film_to_update.user_id = request.json['user_id']
            film_to_update.rating = request.json['rating']
            film_to_update.genres = request.json['genres']
            db.session.commit()
            return make_response(jsonify({"Film updated, film_id": film_to_update.film_id}), 200)
        return make_response(jsonify({current_user.user_name: ", you aren't admin"}), 403)

    @login_required
    def delete(self, film_id):
        """Delete film object by id"""
        film_to_delete = Films.query.get(film_id)
        if film_to_delete is None:
            return make_response(jsonify({"Film is not exists, film_id = ": film_id}), 404)
        if current_user.id == film_to_delete.user_id or current_user.is_admin:
            db.session.delete(film_to_delete)
            db.session.commit()
            return make_response(jsonify({"Film was deleted, film_id = ": film_id}), 200)
        return make_response(jsonify({current_user.user_name: ", you aren't admin"}), 403)


@api.route('/films/order_by/<by_director>')
class FilmsGroupByApi(Resource):
    def get(self, by_director):
        """Get films order by director"""
        order_by = by_director
        films_list_db = Films.query.filter_by(director=order_by)
        films_list_j = []
        for i in range(len(films_list_db)):
            films_list_j.append({
                "id": films_list_db[i].film_id,
                "title": films_list_db[i].title,
                "description": films_list_db[i].description,
                "released_year": films_list_db[i].released_year,
                "director_id": films_list_db[i].director_id,
                "added by user, id": films_list_db[i].user_id,
                "rating": films_list_db[i].rating,
                "poster": films_list_db[i].poster,
                "genres": films_list_db[i].genres
            })
        return make_response(jsonify({"All films": films_list_j}), 200)


@api.route('/genres')
class GenresAllAPI(Resource):
    def get(self):
        genres_list_db = Genres.query.all()
        genres_list_j = []
        for i in range(len(genres_list_db)):
            genres_list_j.append({
                "id": genres_list_db[i].genre_id,
                "genre": genres_list_db[i].genre
            })
        return make_response(jsonify({"All genres": genres_list_j}), 200)

    def post(self):
        """Create director object"""
        new_genre = Genres(genre=request.json['genre'])
        db.session.add(new_genre)
        db.session.commit()
        return make_response(jsonify({"New genre added, id": new_genre.genre_id}), 201)


@api.route('/genres/<genre_id>')
class GenresApi(Resource):
    def get(self, genre_id):
        """Get genre by id"""
        genre = Genres.query.get(genre_id)
        if genre is None:
            return make_response(jsonify({"Genre is not exists, genre_id id = ": genre_id}), 404)
        return make_response(jsonify({genre.genre_id: genre.genre}), 200)

    @login_required
    def put(self, genre_id):
        """Update genre by id"""
        genre_to_update = Genres.query.get(genre_id)
        if genre_to_update is None:
            return make_response(jsonify({"Genre is not exists, genre id = ": genre_id}), 404)
        if current_user.is_admin:
            genre_to_update.genre = request.json['genre']
            db.session.commit()
            return make_response(jsonify({"Genre was update, id": genre_id}), 200)
        return make_response(jsonify({current_user.user_name: ", you aren't admin"}), 403)

    @login_required
    def delete(self, genre_id):
        genre_to_delete = Genres.query.get(genre_id)
        if genre_to_delete is None:
            return make_response(jsonify({"Genre is not exists, genre_id = ": genre_id}), 404)
        if current_user.is_admin:
            db.session.delete(genre_to_delete)
            db.session.commit()
            return make_response(jsonify({"Genre was deleted, genre_id =": genre_id}), 200)
        return make_response(jsonify({current_user.user_name: ", you aren't admin"}), 403)


@api.route('/users')
class UsersApi(Resource):
    def get(self):
        """Get all users"""
        users_list_db = Users.query.all()
        users_list_j = []
        for i in range(len(users_list_db)):
            users_list_j.append({
                "user_id": users_list_db[i].id,
                "user_name": users_list_db[i].user_name,
                "user_status": users_list_db[i].is_admin
            })
        return make_response(jsonify({"All users": users_list_j}), 200)

    def post(self):
        """Create user"""
        new_user = Users(
            user_name=request.json['user_name'],
            is_admin=request.json['is_admin'],
            user_email=request.json['user_email']
        )
        new_user.set_password(request.json['user_password'])
        db.session.add(new_user)
        db.session.commit()
        return make_response(jsonify({"New user added, user_id": new_user.id}), 201)


@api.route('/users/<int:user_id>')
class UsersApi(Resource):
    def get(self, user_id):
        """Get user by id"""
        user_data = Users.query.get(int(user_id))
        if user_data is None:
            return make_response(jsonify({"User is not exists, user_id = ": user_id}), 404)
        return make_response(jsonify({
            "user_id": user_data.id,
            "user_name": user_data.user_name,
            "is_admin": user_data.is_admin
        }), 200)

    @login_required
    def put(self, user_id):
        """Update user by id"""
        user_to_update = Users.query.get(user_id)
        if user_to_update is None:
            return make_response(jsonify({"Genre is not exists, genre id = ": id}), 404)
        if current_user.id == user_id or current_user.is_admin:
            user_to_update.user_name = request.json['user_name']
            user_to_update.is_admin = request.json['is_admin']
            user_to_update.set_password(request.json['user_password'])
            db.session.commit()
            return make_response(jsonify({"User was update, user_id": user_to_update.id}), 200)
        return make_response(jsonify({current_user.user_name: f"can't change data of user with id = {user_id}"}), 403)

    @login_required
    def delete(self, user_id):
        """Delete user by id"""
        user_to_delete = Users.query.get(user_id)
        if user_to_delete is None:
            return make_response(jsonify({"User is not exists, user_id = ": id}), 404)
        if current_user.is_admin:
            db.session.delete(user_to_delete)
            db.session.commit()
            return make_response(jsonify({"User was deleted, user_id =": id}), 200)
        return make_response(jsonify({current_user.user_name: f"can't delete user with id = {user_id}"}), 403)
