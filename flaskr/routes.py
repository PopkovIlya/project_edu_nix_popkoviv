from flask import request, jsonify, make_response
from flask_restx import Resource
from flaskr import api
from flaskr import db
from flaskr.models_db import Films, Genres, Directors, Users, films_genres

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
        """Create director object"""
        new_director_param = request.json['new_director']
        new_director = Directors(full_name=new_director_param) #request.json['new_director'])
        db.session.add(new_director)
        db.session.commit()
        return make_response(jsonify({"New director id": new_director.director_id}), 201)


@api.route('/directors/<int:director_id>')
class DirectorsApi(Resource):
    def get(self, director_id):
        director = Directors.query.get(director_id)
        if director is None:
            return make_response(jsonify({"Director is not exists, director id = ": director_id}), 404)
        return make_response(jsonify({director.director_id: director.full_name}), 200)

    def put(self, director_id):
        """Update director object by id"""
        director_to_update = Directors.query.get(director_id)
        if director_to_update is None:
            return make_response(jsonify({"Director is not exists, director id = ": director_id}), 404)
        request_data = request.get_json()
        director_to_update.full_name = request_data['full_name']
        db.session.commit()
        return make_response(jsonify({"Director updated": director_id}), 200)

    def delete(self, director_id):
        director_to_delete = Directors.query.get(director_id)
        if director_to_delete is None:
            return make_response(jsonify({"Director is not exists, director_id = ": director_id}), 404)
        db.session.delete(director_to_delete)
        db.session.commit()
        return make_response(jsonify({"Director was deleted, director_id =": director_id}), 200)


@api.route('/films')
class FilmsAllAPI(Resource):
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

    def post(self):
        """Create new film"""
        #try:
        new_film = Films(
            title=request.json['title'],
            description=request.json['description'],
            released_year=request.json['released_year'],
            director_id=request.json['director_id'],
            user_id=request.json['user_id'],
            rating=request.json['rating'],
            poster=request.json['poster'],
            genres=request.json['genres']
        )
        db.session.add(new_film)
        db.session.commit()
        return make_response(jsonify({"New film was added, it id is ": new_film.film_id}), 201)


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

@api.route('/films/<int:film_id>')
class FilmsApi(Resource):
    def get(self, film_id=None):
        """Get one film by id"""
        film = Films.query.get(film_id)
        if film is None:
            return make_response(jsonify({"Director is not exists, director id = ": film_id}), 404)
        return make_response(jsonify({
            "film_id": film.film_id,
            "title": film.title,
            "description": film.description,
            "released_year": film.released_year,
            "director_id": film.director_id,
            "user_id": film.user_id,
            "rating": film.rating,
            "poster": film.poster,
            "genres": film.genres
        }), 200)

    def put(self, film_id):
        """Update film object by id"""
        film_to_update = Films.query.get(film_id)
        if film_to_update is None:
            return make_response(jsonify({"Film is not exists, film_id = ": film_id}), 404)
        film_to_update.title = request.json['title']
        film_to_update.description = request.json['description']
        film_to_update.released_year = request.json['released_year']
        film_to_update.director_id = request.json['director_id']
        film_to_update.user_id = request.json['user_id']
        film_to_update.rating = request.json['rating']
        film_to_update.genres = request.json['genres']
        db.session.commit()
        return make_response(jsonify({"Film updated, film_id": film_to_update.film_id}), 200)

    def delete(self, film_id):
        """Delete film object by id"""
        film_to_delete = Films.query.get(film_id)
        if film_to_delete is None:
            return make_response(jsonify({"Film is not exists, film_id = ": film_id}), 404)
        db.session.delete(film_to_delete)
        db.session.commit()
        return make_response(jsonify({"Film was deleted, film_id = ": film_id}), 200)


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

    def put(self, genre_id):
        """Update genre by id"""
        genre_to_update = Genres.query.get(genre_id)
        if genre_to_update is None:
            return make_response(jsonify({"Genre is not exists, genre id = ": genre_id}), 404)
        genre_to_update.genre = request.json['genre']
        db.session.commit()
        return make_response(jsonify({"Genre was update, id": genre_id}), 200)

    def delete(self, genre_id):
        genre_to_delete = Genres.query.get(genre_id)
        if genre_to_delete is None:
            return make_response(jsonify({"Genre is not exists, genre_id = ": genre_id}), 404)
        db.session.delete(genre_to_delete)
        db.session.commit()
        return make_response(jsonify({"Genre was deleted, genre_id =": genre_id}), 200)


@api.route('/users')
class UsersApi(Resource):
    def get(self):
        """Get all users"""
        users_list_db = Users.query.all()
        users_list_j = []
        for i in range(len(users_list_db)):
            users_list_j.append({
                "user_id": users_list_db[i].user_id,
                "user_name": users_list_db[i].user_name,
                "user_status": users_list_db[i].user_status,
                "user_password": users_list_db[i].user_password
            })
        return make_response(jsonify({"All users": users_list_j}), 200)

    def post(self):
        """Create user"""
        new_user = Users(
            user_name=request.json['user_name'],
            user_status=request.json['user_status'],
            user_password=request.json['user_password'],
        )
        db.session.add(new_user)
        db.session.commit()
        return make_response(jsonify({"New user added, user_id": new_user.user_id}), 201)


@api.route('/users/<int:user_id>')
class UsersApi(Resource):
    def get(self, user_id):
        """Get user by id"""
        user_data = Users.query.get(user_id)
        if user_data is None:
            return make_response(jsonify({"User is not exists, user_id = ": user_id}), 404)
        return make_response(jsonify({
            "user_id": user_data.user_id,
            "user_name": user_data.user_name,
            "user_status": user_data.user_status
        }), 200)

    def put(self, user_id):
        """Update user by id"""
        user_to_update = Users.query.get(user_id)
        if user_to_update is None:
            return make_response(jsonify({"Genre is not exists, genre id = ": user_id}), 404)
        user_to_update.user_name = request.json['user_name']
        user_to_update.user_status = request.json['user_status']
        user_to_update.user_password = request.json['user_password']
        db.session.commit()
        return make_response(jsonify({"User was update, user_id": user_to_update.user_id}), 200)

    def delete(self, user_id):
        user_to_delete = Users.query.get(user_id)
        if user_to_delete is None:
            return make_response(jsonify({"User is not exists, user_id = ": user_id}), 404)
        db.session.delete(user_to_delete)
        db.session.commit()
        return make_response(jsonify({"User was deleted, user_id =": user_id}), 200)