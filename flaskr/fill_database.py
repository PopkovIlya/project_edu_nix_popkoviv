import json
from flask import jsonify

from flaskr import db
from flaskr.models_db import Films, Genres, Directors, Users, films_genres


def fill_directors(file_name):
    with open(file_name, "r") as read_file:
        data = json.load(read_file)
        directors = data["directors"]
        try:
            for i in directors:
                db.session.add(Directors(director_id=i['director_id'], full_name=i['full_name']))
            db.session.commit()
        except Exception as e:
            print(e, 'except')


def fill_users(file_name):
    with open(file_name, "r") as read_file:
        data = json.load(read_file)
        users = data["users"]
        users_added = []
        try:
            for i in users:
                new_user = Users()
                new_user.id = i['user_id']
                new_user.user_name = i['user_name']
                new_user.is_admin = i['is_admin']
                new_user.user_email = i['user_email']
                new_user.set_password(i['users_password'])
                db.session.add(new_user)
                users_added.append({i['user_id']: i['user_name']})
            db.session.commit()
            return users_added
        except Exception as e:
            print(e, 'fill_users except')


def fill_films(file_name):
    with open(file_name, "r") as read_file:
        data = json.load(read_file)
        films = data["films"]
        films_added = []
        try:
            for current_film_data in films:
                film_adds = Films(
                    film_id=current_film_data['film_id'],
                    title=current_film_data['title'],
                    description=current_film_data['description'],
                    released_year=current_film_data['released_year'],
                    director_id=current_film_data['director_id'],
                    user_id=current_film_data['user_id'],
                    rating=current_film_data['rating'],
                    poster=current_film_data['poster']
                )
                for j in current_film_data["genres"]:
                    genre_1 = Genres.query.filter_by(genre_id=j).first()
                    film_adds.genres.append(genre_1)
                    db.session.add(film_adds)
                films_added.append({current_film_data['film_id']: current_film_data['title']})
            db.session.commit()
            return films_added
        except Exception as e:
            print(e, 'except')


def fill_genres(file_name):
    with open(file_name, "r") as read_file:
        data = json.load(read_file)
        genres = data["genres"]
        genres_added = []
        try:
            for current_genre_data in genres:
                db.session.add(Genres(genre_id=current_genre_data['genre_id'], genre=current_genre_data['genre']))
                genres_added.append({current_genre_data['genre_id']: current_genre_data['genre']})
            db.session.commit()
            return genres_added
        except Exception as e:
            print(e, 'except')


def del_table_data(model_data):
    all_data = model_data.query.all()
    entities_deleted = []
    try:
        for entity in all_data:
            db.session.delete(entity)
            entities_deleted.append(str(entity))
        db.session.commit()
        return f'{entities_deleted} were deleted'
    except Exception as e:
        print('Except!!!', e)


def del_all_data():
    tables = [Films, Genres, Directors, Users]
    all_entities_deleted = []
    for model in tables:
        all_entities_deleted.append(del_table_data(model))
    return all_entities_deleted


def del_entity_by_id(model: Films, id_entity: int):
    entity_del = model.query.get(id_entity)
    db.session.delete(entity_del)
    db.session.commit()
    return f"{entity_del} was deleted"


def fill_db(file_name):
    data_fill = [
        i for i in
        (
            fill_genres(file_name),
            fill_directors(file_name),
            fill_users(file_name),
            fill_films(file_name)
        )
    ]
    return f'{data_fill} were added'


if __name__ == '__main__':
    print(fill_db("data_to_populate_db.json"))
    # print(del_all_data())
# #     # print(del_entity_by_id(Films, 1))

