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
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres', 'password','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question':'You are here?',
            'answer':'YES!!!!!!!',
            'category':'Sports',
            'difficulty':1
        }

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
    #Test GET categories method
    def test_get_categories(self):
        "Test to verify all categories are returned"
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['categories'])

    #def test_fail_get_categories(self):
    #    "Test to fail the GET request on categories"
    #    res = self.client().get('/categories')

    def test_get_questions(self):
        "Test to verify all questions are returned"
        res = self.client().get('/questions/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestions'])

    def test_fail_get_questions(self):
        "Test to fail the GET request on questions"
        res = self.client().get('/questions/?page=400')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)

    #def test_post_add_question(self):
    #    "Test to see if question is added"
    #    res = self.client().post('/questions/', json=self.new_question)
    #    data = json.loads(res.data)

    #    self.assertEqual(res.status_code,200)
    #    self.assertEqual(data['success'],True)

    #def test_fail_post_add_question(self):
    #    "Test to fail adding a question"
    #    res = self.client().post('/questions/400', json=self.new_question)
        #data = json.loads(res.data)
    #    self.assertEqual(res.status_code,405)
        #self.assertEqual(data['success'],False)

    # TypeError: 'dict' object is not callable
    #def test_delete_question(self):
    #    "Test to delete a question"
    #    res = self.client().delete('/questions/30')
        #data = json.loads(res.data)

    #    question = Question.query().filter(Question.id == 30).one_or_none()

    #    self.assertEqual(res.status_code,200)
        #self.assertEqual(data['success'],True)
    #    self.assertEqual(question,None)



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()