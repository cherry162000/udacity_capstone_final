import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movie, Actor

from auth import AuthError, requires_auth



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response

   
    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(payload):
        try:
            select_movies = Movie.query.order_by(Movie.id).all()   
            format_movies = [movies.format() for movies in select_movies]
            print("Select movies:",select_movies)
            print("format movies:",format_movies)
            if len(select_movies) ==0:
                abort(404)
            else:    
                return jsonify({
                'success':True,
                'movies':format_movies
            })
        except Exception as e:
            print("get movies exception",e)

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(payload):
        try:
            select_actors = Actor.query.order_by(Actor.id).all()   
            format_actors = [actors.format() for actors in select_actors]
            print("Select actors:",select_actors)
            if len(select_actors) ==0:
                abort(404)
            else:    
                return jsonify({
                'success':True,
                'actors':format_actors
            })
        except Exception as e:
            print("get actors exception",e)

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movie(payload):
        body = request.get_json()

        if body is None:
            abort(400)

        new_title = body.get('title', None)
        new_release_date = body.get('release_date', None)

        if new_title is None or new_release_date is None:
            abort(400, "Missing field for Movie")

        movie = Movie(title=new_title,
                      release_date=new_release_date)

        movie.insert()

        return jsonify({
            "success": True
        })
   


    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor(payload):
        body = request.get_json()

        if body is None:
            abort(400)

        new_name = body.get('name', None)
        new_age = body.get('age', None)
        new_gender = body.get('gender', None)
        new_movie_id = body.get('movie_id', None)

        if new_name is None or new_age is None or new_gender is None or new_movie_id is None:
            abort(400)

        actor = Actor(name=new_name, age=new_age, gender=new_gender, movie_id=new_movie_id)

        actor.insert()

        return jsonify({
            "success": True
        })
        
    
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload,movie_id):
        try:
            movies = Movie.query.get(movie_id)
            if movies is None:
                abort(404)
            else:
                movies.delete()

            return jsonify({
                'success':True,
                'deleted':movie_id
                })
        except Exception as e:
            print("Delete Exception_________",e)
            abort(422)
       

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload,actor_id):
        try:
            actors = Actor.query.get(actor_id)
            if actors is None:
                abort(404)
            else:
                actors.delete()

            return jsonify({
                'success':True,
                'deleted':actor_id
                })
        except Exception as e:
            print("Delete Exception actors______________",e)
            abort(422) 

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('update:movies')
    def update_movie(payload,movie_id):
        movies = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if not movies:
            abort(404)
        body = request.get_json()
        new_title = body.get('title', None)
        new_releae_date = body.get('release_date', None)
        movies.title = new_title
        movies.release_date = new_releae_date
        movies.update()
        return jsonify({
        'success': True
        })


    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('update:actors')
    def update_actor(payload,actor_id):
        actors = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if not actors:
            abort(404)
        body = request.get_json()
        new_name = body.get('title', None)
        new_age = body.get('age', None)
        new_gender = body.get('gender', None)
        new_movie = body.get('movie_id', None)
        actors.name = new_name
        actors.age = new_age
        actors.gender = new_gender
        actors.movie_id = new_movie
        actors.update()
        return jsonify({
        'success': True
        })


    # Error Handling

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message":  "Unprocessable entity!!",
        }),422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Data not found!!"
        }),404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": 'The request can not be processed'
        }), 400

    @app.errorhandler(AuthError)
    def auth_error(auth_error):
        return jsonify({
            "success": False,
            "error": auth_error.status_code,
            "message": auth_error.error['description']
        }), auth_error.status_code

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)