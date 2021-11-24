from flask import Flask, request
from flask_restx import Resource, Api

app = Flask(__name__)
api = Api(app)


@api.route('/films', '/films/<film_id>')
class Films(Resource):
    def get(self, film_id=None):
        """Get all films or film by id"""
        if film_id is None:
            return {'result': "return all films"}, 200  # curl http://localhost:5000/films
        try:
            film_id = int(film_id)
            return {'result': f"get film with id = {film_id}"}, 200  # curl http://localhost:5000/films/1
        except ValueError:
            return {'result': f"Bad Request"}, 400  # curl http://localhost:5000/films/a

    def put(self, film_id):  # curl http://localhost:5000/films/1 -d "data=update something" -X PUT
        """Update film object by id"""
        return {'result': f"Film with with id = {film_id}"
                          f" was updated by data {request.form['data']}"}, 204

    def post(self):  # curl http://localhost:5000/films -d "data=something data of new film" -X POST
        """Create film object"""
        return {'result': f"New film was added with data = {request.form['data']}"}, 201

    def delete(self, film_id):  # curl http://localhost:5000/films/1 -X DELETE
        """Delete film object by id"""
        return {'result': f"Film with with id = {film_id} was deleted"}, 204

@api.route('/genres', '/genres/<genre_id>')
class Genres(Resource):
    def get(self, genre_id=None):
        """Get all genres or one genre by id"""
        if genre_id is None:
            return {'result': "return all genres"}, 200  # curl http://localhost:5000/genres
        return {'result': f"get genre with id = {genre_id}"}, 200  # curl http://localhost:5000/genres/1

    def put(self, genre_id):  # curl http://localhost:5000/genres/1 -d "data=update something" -X PUT
        """Update genre object by id"""
        return {'result': f"Genre with id = {genre_id}"
                          f" was updated by data {request.form['data']}"}, 204

    def post(self):  # curl http://localhost:5000/genres -d "data=something data of genre" -X POST
        """Create genre object"""
        return {'result': f"New genre was added with data = {request.form['data']}"}, 201

    def delete(self, genre_id):  # curl http://localhost:5000/genres/1 -X DELETE
        return {'result': genre_id}, 204


@api.route('/directors', '/directors/<director_id>')
class Directors(Resource):
    def get(self, director_id=None):
        """Get all directors or one director by id"""
        if director_id is None:
            return {'result': "return all directors"}, 200  # curl http://localhost:5000/directors
        return {'result': f"get director with id = {director_id}"}, 200  # curl http://localhost:5000/directors/1

    def put(self, director_id):  # curl http://localhost:5000/directors/1 -d "data=update something" -X PUT
        """Update director object by id"""
        return {'result': f"Director with with id"
                          f" = {director_id} was updated by data {request.form['data']}"}, 204

    def post(self):  # curl http://localhost:5000/directors -d "data=something data of director" -X POST
        """Create director object"""
        return {'result': f"New director was added with data = {request.form['data']}"}, 201

    def delete(self, director_id):  # curl http://localhost:5000/directors/1 -X DELETE
        return {'result': f"Director with with id"
                          f" = {director_id} was deleted"}, 204


@api.route('/users', '/users/<user_id>')
class Users(Resource):
    def get(self, user_id=None):
        """Get all users or one user by id"""
        if user_id is None:
            return {'result': "return all users"}, 200  # curl http://localhost:5000/users
        return {'result': f"get user with id = {user_id}"}, 200  # curl http://localhost:5000/users/1

    def put(self, user_id):  # curl http://localhost:5000/users/1 -d "data=update something" -X PUT
        return {'result': f"User with with id = {user_id} was updated by data {request.form['data']}"}, 204

    def post(self):  # curl http://localhost:5000/users -d "data=something data of user" -X POST
        return {'result': "user_id"}, 201

    def delete(self, user_id):  # curl http://localhost:5000/users/1 -X DELETE
        return {'result': f"User with with id = {user_id} was deleted"}, 204

if __name__ == '__main__':
    app.run(debug=True)



#
# @api.route('/hello')
# class HelloWorld(Resource):
#     def get(self):
#         return {'hello': 'world'}
#
#     def put(self, todo_id):
#         todos[todo_id] = request.form['data']
#         return {todo_id: todos[todo_id]}
