import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}/{}".format('postgres:amany@localhost:5432', self.database_name)
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
    def test_get_paginated_questions(self):
        response = self.client().get('/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        
   
    # test delete fun
    def test_delete_question_failed(self):
        response = self.client().delete('/questions/<int:question_id>')
        #self.assertEqual(response.status_code, 200)
        # Test to see if it exists, should return a 404 (not found)
        #re = self.client().get('/questions/<int:question_id>')
        self.assertEqual(response.status_code, 404)
       
        
    def test_question_creation(self):
        response = self.client().get('/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
       
    # def test_question_search(self):
    #     res = self.client().post('/books', json={'search': 'applejacks'})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(data['total_books'], 0)
    #     self.assertEqual(len(data['books']), 0)

          


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()