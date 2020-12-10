import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
import random


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
        self.assertEqual(len(data['questions']),10)
        self.assertTrue(data['total_questions'])
        
   
    # test delete fun
    # def test_delete_question(self):
    #     res = self.client().delete('/questions/7')
    #     data = json.loads(res.data)
    #     question=Question.query.filter(Question.id==4).one_or_none()

    #     self.assertEqual(res.status_code,200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(data['deleted'], 7)
    #     self.assertEqual(question,None )

       
        
    def test_question_search_with_results(self):
        res = self.client().post('/questions',json={'searchTerm': 'title'})
        data = json.loads(res.data)
        #print(data)


        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        #self.assertTrue(data['total_questions'])
        self.assertEqual(data['total_questions'], 1)

    def test_get_questions_by_category(self):
        res = self.client().get('categories/3/questions')
        data = json.loads(res.data)
       
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertEqual(len(data['questions']), 3)
        self.assertEqual(data['current_category'], 'Geography')


    def test_get_allquestions_clicking_on_ALL(self):
        res = self.client().post('/quizzes',json={
            'previousQuestions':[],
            'quiz_category':{'type':'click','id':0}

            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_quizequestion'], 1)
        self.assertTrue(data['total_questions'],18)

    def test_get_allquestions_clicking_on_spacific_category(self):
        res = self.client().post('/quizzes',json={
            'previousQuestions':[],
            'quiz_category':{'type':'Art','id':2}

            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_quizequestion'], 1)
        self.assertTrue(data['total_questions'],5)
        


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()