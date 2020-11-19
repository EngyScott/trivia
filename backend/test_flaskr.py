import os
import unittest
import json
import random

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
        self.database_path = "postgresql://{}:{}@{}/{}".format('postgres', '0000', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
        
        self.new_question = {
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?",
            "answer": "Tom Cruise",
            "difficulty": 4,
            "category": 5
        }
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_pagenated_questions(self):
        """TEST PAENATE QUESTION"""
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data['questions']), 10)
        self.assertTrue(data['total_questions'])
    
    def test_404_sent_requesting_invalid_page(self):
        res = self.client().get('/questions?page=1000')
        # print('response:', res)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'content not found')


    def test_delete_question(self):
        """TEST DELETE QUESTION"""
        res = self.client().delete('/questions/22')
        data = json.loads(res.data)
        qestion = Question.query.filter_by(id=22).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 22)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertEqual(qestion, None)

    def test_422_delete_invalid_question_id(self):
        """TEST FAILUIR DELETE QUESTION"""
        res = self.client().delete('/questions/500')
        # print('response:', res)
        data = json.loads(res.data)
        # print('data:', data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_create_new_question(self):
        """TEST CREATE NEW QUESTION"""
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['created'])
        self.assertTrue(data['total_questions'])

    def test_405_create_new_question_not_allowed(self):
        res = self.client().post('/questions/30', json=self.new_question)
        # print('response: ',res)
        # data = json.loads(res.data)
        # print('data: ', data)

        self.assertEqual(res.status_code, 405)
        # self.assertEqual(data['success'], False)
        # self.assertEqual(data['message'], "method not allowed")
    
    def test_search_questions(self):
        res = self.client().post('/questions', json={"searchTerm":"title"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['total_questions'])
        self.assertEqual(len(data['questions']), 2)

    def test_invalid_search_questions(self):
        res = self.client().post('/questions', json={"searchTerm":"sunlight"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['total_questions'], 0)
        self.assertEqual(len(data['questions']), 0)

    def test_get_questions_by_category(self):
        res = self.client().get('/categories/5/questions')
        data = json.loads(res.data)
        current_category = Category.query.filter_by(id=5).first_or_404()
        questions = Question.query.filter_by(category=5).all()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['current_category'])
        self.assertTrue(data['questions'])
        self.assertTrue(len(data['questions']))

    def test_404_get_questions_beyond_category_ids(self):
        res = self.client().get('/categories/15/questions')
        # print('response:',res)
        data = json.loads(res.data)
        current_category = Category.query.filter_by(id=15).one_or_none()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(current_category, None)
        self.assertEqual(data['message'], "content not found")
        self.assertEqual(data['success'], False)

    def test_play(self):
        res = self.client().post('/quizzes', json={"previous_questions":[],"quiz_category":{"id": 5, "type": "Entertainment"}})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['question'])



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()