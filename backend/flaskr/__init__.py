import os
from flask import Flask, request, abort, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, group):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in group]
  current_questions = questions[start:end]

  return current_questions

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  cors = CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5000/"}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, PATCH, DELETE, OPTIONS, POST, PUT')
    return response
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
    try:
      categories = Category.query.all()
      formated_categories = [category.format() for category in categories]
    except:
      abort(404)
    return jsonify({'categories': formated_categories})

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions')
  def get_questions():
    try:
      current_category = []

      # RETRIEVE ALL QUESTIONS FROM DB 
      group = Question.query.order_by(Question.id).all()
      # PAGENATE QUESTIONS
      current_questions = paginate_questions(request, group)
      # print('current_questions', current_questions)
      if len(current_questions) == 0:
        abort(404)
      else:
        # RETRIEVE ALL CATEGORIES FROM DB
        categories = Category.query.all()
        # RETURN FORMATTED CATEGORY LIST
        formated_categories = [category.format() for category in categories]
        # GET CURRENT ATEGORIES DEPENDING ON QUESTIONS SHOWING ON PAGE
        for question in current_questions:
            current_category.append(question['category'])
        return ({
          'questions': current_questions,
          'total_questions': len(group),
          'categories': formated_categories,
          'current_category': current_category
        })
    except:
      abort(404)
    
  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:id>', methods=['DELETE'])
  def delete_question(id):
    try:
      question = Question.query.filter_by(id=id).one_or_none()
      if question is None:
        abort(422)
      else:
        formatted_question = question.format()
        question.delete()

        current_category = []

        group = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, group)
        # print('current_questions', current_questions)
        categories = Category.query.all()
        formated_categories = [category.format() for category in categories]
        for question in current_questions:
          current_category.append(question['category'])
        return jsonify ({
          'success': True,
          'deleted': formatted_question['id'],
          'questions': current_questions,
          'total_questions': len(group),
          'categories': formated_categories,
          'current_category': current_category
        })
    except:
      # db.session.rollback()
      abort(422)
      # db.session.close()
    

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  
  @app.route('/questions', methods=['POST'])
  def create_question():
    body = request.get_json()
    # print(body)
    question = body.get("question", None)
    answer = body.get("answer", None)
    difficulty = body.get("difficulty", None)
    category = body.get("category", None)
    q = body.get('searchTerm', None)

    try:
      if q:
        current_category = []
        # print(q)
        group = Question.query.filter(Question.question.ilike('%{}%'.format(q))).all()
        
        current_questions = paginate_questions(request, group)
        for question in current_questions:
          current_category.append(question['category'])
        # print('questions', current_questions,'total_questions', len(group),'current_category', current_category)

        return jsonify({
          'questions': current_questions,
          'total_questions': len(group),
          'current_category': current_category
        })
      else:
        if (question is None) or (answer is None) or (difficulty is None) or (category is None):
          abort(405)
        else:
          new_question = Question(question=question, answer=answer,
                                  difficulty=difficulty, category=category)
          new_question.insert()

          current_category = []

          group = Question.query.order_by(Question.id).all()
          current_questions = paginate_questions(request, group)
        
          for question in current_questions:
            current_category.append(question['category'])
          return jsonify({
                'created': new_question.id,
                'questions': current_questions,
                'total_questions': len(group),
                'current_category':  current_category
              })
    except:
      abort(422)
    
    
  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:id>/questions')
  def get_questions_by_category(id):
    try:
      categories = Category.query.all()
      formated_categories = [category.format() for category in categories]

      current_category = Category.query.filter_by(id=id).first_or_404().format()
      if current_category == 404:
        abort(404)
      else:
        group = Question.query.filter_by(category=id).all()
        current_questions = paginate_questions(request, group)
        return jsonify({
          'categories': formated_categories,
          'current_category': current_category,
          'questions': current_questions,
          'total_questions': len(group)
        })
    except:
      abort(404)
    

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def play():
    try:
      body = request.get_json()
      previous_questions = body.get("previous_questions")
      quiz_category = int(body.get("quiz_category"))

      if quiz_category == 0:
        get_questions = Question.query.all()
        # print('get_questions', get_questions, len(get_questions))
        random_question = random.choice(get_questions).format()
      else:
        # print('previous_questions', previous_questions, 'quiz_category', quiz_category)
        get_category = Category.query.filter_by(id=quiz_category).first_or_404()
        get_questions = Question.query.filter_by(category=quiz_category).all()
        # print('get_questions', get_questions, len(get_questions))

        random_question = random.choice(get_questions).format()
        # print('random_question', random_question)
      if random_question in previous_questions:
        return
    except:
      abort(400)
    return jsonify({'question': random_question})
  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400
  
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "content not found"
    }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
      return jsonify({
          "success": False,
          "error": 405,
          "message": "method not allowed"
      }), 405

      @app.errorhandler(500)
      def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500
  
  return app

    