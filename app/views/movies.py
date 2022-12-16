# здесь контроллеры/хендлеры/представления для обработки запросов (flask ручки).
# сюда импортируются сервисы из пакета service
from flask import request
from flask_restx import Resource, Namespace

from app.models.movie import Movie, movies_schema, movie_schema
from app.setup_db import db

movies_ns = Namespace("movies")


@movies_ns.route('/')
class MoviesView(Resource):
    def get(self):  # получить все фильмы.
        movies_query = db.session.query(Movie)  # +

        director_id = request.args.get("director_id")  # получить все фильмы режиссера.
        if director_id is not None:
            movies_query = movies_query.filter(Movie.director_id == director_id)

        genre_id = request.args.get("genre_id")  # получить все фильмы жанра.
        if genre_id is not None:
            movies_query = movies_query.filter(Movie.genre_id == genre_id)

        year = request.args.get("year")  # получить все фильмы за год.
        if year is not None:
            movies_query = movies_query.filter(Movie.year == year)

        return movies_schema.dump(movies_query.all()), 200

    def post(self):  # создать фильм.
        request_json = request.json
        new_movie = Movie(**request_json)

        with db.session.begin():
            db.session.add(new_movie)

        return "Movie created", 201


@movies_ns.route("/<int:uid>")  # +
class MovieView(Resource):
    def get(self, uid):  # получить фильм по ID.
        movie = db.session.query(Movie).get(uid)
        if not movie:
            return "Фильм не найден", 404
        return movie_schema.dump(movie), 200

    def put(self, uid):  # изменить информацию о фильме.
        updated_rows = db.session.query(Movie).filter(Movie.id == uid).update(request.json)  # int

        if updated_rows != 1:
            return "not updated", 400

        db.session.commit()
        return "", 204

    def delete(self, uid):  # удалить фильм.
        movie = db.session.query(Movie).get(uid)
        if not movie:
            return "Фильм не найден", 404

        db.session.delete(movie)
        db.session.commit()

        return "", 204