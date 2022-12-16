from flask_restx import Resource, Namespace

from app.models.director import directors_schema, Director, director_schema
from app.setup_db import db

director_ns = Namespace("director")


@director_ns.route("/")
class DirectorsView(Resource):
    def get(self):  # получить всех режиссеров.
        directors = db.session.query(Director)
        return directors_schema.dump(directors.all()), 200


@director_ns.route("/<int:uid>")  # +
class DirectorView(Resource):
    def get(self, uid):  # получить режиссера по ID.
        try:
            director = db.session.query(Director).get(uid)
            return director_schema.dump(director), 200
        except Exception as e:
            return str(e), 404
