from flask_restx import Resource, Namespace

from app.models.genre import genres_schema, Genre, genre_schema
from app.setup_db import db

genre_ns = Namespace("genre")


@genre_ns.route("/")
class GenresView(Resource):

    def get(self):  # получить все жанры.
        genres_query = db.session.query(Genre)
        return genres_schema.dump(genres_query.all()), 200


@genre_ns.route("/<int:uid>")
class GenreView(Resource):
    def get(self, uid):  # получить жанр по ID.
        genre = db.session.query(Genre).get(uid)
        if not genre:
            return "Жанр не найден", 404
        return genre_schema.dump(genre), 200
