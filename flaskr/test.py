import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor

from dotenv import load_dotenv

load_dotenv()
database = os.getenv("DATABASE")
password = os.getenv("PASSWORD")
hostname = os.getenv("HOSTNAME")
assitant = os.getenv("ASSITANT")
director = os.getenv("DIRECTOR")
producer = os.getenv("PRODUCER")

database_name = 'casting_testdb'
database_path = "postgresql://{}:{}@{}/{}".format(database,password,hostname, database_name)


class CastingTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = database_name
        self.database_path = database_path
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass



    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_retrieve_movies(self):
        res = self.client().get(
            "/movies",
            headers={
                'Authorization': 'Bearer '+producer
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movies"])

    def test_retrieve_actors(self):
        res = self.client().get(
            "/actors",
            headers={
                'Authorization': 'Bearer '+producer
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["actors"])

    def test_delete_movies(self):
        res = self.client().delete(
            "/movies/2",
            headers={
                'Authorization': 'Bearer '+producer
            })
        data = json.loads(res.data)

        movies = Movie.query.filter(Movie.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 2)

    def test_delete_actors(self):
        res = self.client().delete(
            "/actors/2",
            headers={
                'Authorization': 'Bearer '+producer
            })
        data = json.loads(res.data)

        actors = Actor.query.filter(Actor.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 2)
    
    def test_post_movies(self):
        new_movie = {
            'title': 'New Movie',
            'release_date': '23'
        }
        res = self.client().post(
            "/movies",
            headers={
                'Authorization': 'Bearer '+producer
            },json=new_movie)
        data = res.get_json()
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['movies'])

    def test_post_actors(self):
        new_actor = {
            'name': 'New Actor',
            'age' : 24,
            'gender': 'm',
            'movie_id': 2
        }
        res = self.client().post(
            "/movies",
            headers={
                'Authorization': 'Bearer '+producer
            },json=new_actor)
        data = res.get_json()
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['actors'])

    def test_patch_movies(self):
        test_movie = Movie(title='new Movie test', release_date='24')
        res = self.client().patch(
            "/movies/2",
            headers={
                'Authorization': 'Bearer '+producer
            },json=test_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
    
    
    def test_patch_actors(self):
        test_actor = Actor(name='test actor',age=25,gender='m',movie_id=1)
        res = self.client().patch(
            "/actors/2",
            headers={
                'Authorization': 'Bearer '+producer
            },json=test_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_delete_movies(self):
        res = self.client().delete(
            "/movies/5",
            headers={
                'Authorization': 'Bearer '+producer
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Data not found!!')

    def test_delete_actors(self):
        res = self.client().delete(
            "/actors/4",
            headers={
                'Authorization': 'Bearer '+producer
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Data not found!!')

    def test_delete_movies_assistant(self):
        res = self.client().delete(
            "/movies/5",
            headers={
                'Authorization': 'Bearer '+assitant
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
    
    def test_retrieve_movies_assistant(self):
        res = self.client().get(
            "/movies",
            headers={
                'Authorization': 'Bearer '+assitant
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movies"])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()