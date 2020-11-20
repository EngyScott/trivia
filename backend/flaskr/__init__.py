import os
from flask import Flask, request, abort, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
# from dotenv import load_dotenv
from models import setup_db, Question, Category

# load_dotenv()

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
    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET, PATCH, DELETE, OPTIONS, POST, PUT')
        return response
    '''
  @TODO:
  Create an endpoint to handle GET requests
  for all available categories.
  '''
    @app.route('/categories')
    def get_categories():
        try:
            # RETRIEVE ALL CATEGORIES FROM DB
            categories = Category.query.all()
            # print(categories)
            # FORMAT LIST OF CATEGORIES TO JSON TYPE
            formated_categories = [category.format()
                                   for category in categories]
            # print('formated_categories:', formated_categories)
            # RETURN LIST OF CATEGORIES TYPES
            category_type = [category['type']
                             for category in formated_categories]
            # print('category_type:', category_type)

            return jsonify({'categories': category_type})
        except BaseException:
            abort(404)

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
                # FORMATT CATEGORY LIST
                formated_categories = [category.format()
                                       for category in categories]
                # RETURN LIST OF ATEGORIES TYPES
                category_type = [category['type']
                                 for category in formated_categories]
                # GET CURRENT ATEGORIES DEPENDING ON QUESTIONS SHOWING ON PAGE
                for question in current_questions:
                    current_category.append(question['category'])
                return ({
                    'questions': current_questions,
                    'total_questions': len(group),
                    'categories': category_type,
                    'current_category': current_category
                })
        except BaseException:
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
            # RETRIEVE QUESTION FROM DB USING ID
            question = Question.query.filter_by(id=id).one_or_none()
            if question is None:
                abort(422)
            else:
                # FORMAT QUESTION TO JSON TYPE TO CATCH DATA
                formatted_question = question.format()
                # DELETE QUETION FROM DB
                question.delete()

                current_category = []
                # RETRIEVE ALL QUESTIONS FROM DB
                group = Question.query.order_by(Question.id).all()
                # PAGENATE QUESTIONS
                current_questions = paginate_questions(request, group)
                # print('current_questions', current_questions)
                # RETRIEVE ALL CATEGORIES FROM DB
                categories = Category.query.all()
                # FORMAT LIST OF ATEGORIES TO JSON TYPE
                formated_categories = [category.format()
                                       for category in categories]
                # RETURN LIST OF CATEGORIES TYPES
                for question in current_questions:
                    current_category.append(question['category'])
                return jsonify({
                    'success': True,
                    'deleted': formatted_question['id'],
                    'questions': current_questions,
                    'total_questions': len(group),
                    'categories': formated_categories,
                    'current_category': current_category
                })
        except BaseException:
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
        # RETRIEVE REQUEST BODY
        body = request.get_json()
        # print(body)
        # ASSIGN REUQES BODY DATA TO VARIABLES
        question = body.get("question", None)
        answer = body.get("answer", None)
        difficulty = body.get("difficulty", None)
        category = body.get("category", None)
        q = body.get('searchTerm', None)

        try:
            # IF REQUEST BODY HAS SearchTerm:
            if q:
                current_category = []
                # print(q)
                # RETRIVE ALL QUESTIONS THAT MATCH SEARCH TERM FROM DB
                group = Question.query.filter(
                    Question.question.ilike(
                        '%{}%'.format(q))).all()
                # PAGENATE RETRIEVED QUESTIONS
                current_questions = paginate_questions(request, group)
                # LIST OF CURRENT CATEGORIES BASED ON DISPLAYED QUESTIONS
                for question in current_questions:
                    current_category.append(question['category'])
                # print('questions', current_questions,'total_questions', len(group),'current_category', current_category)

                return jsonify({
                    'questions': current_questions,
                    'total_questions': len(group),
                    'current_category': current_category
                })
            else:
                # IF REQUEST BODY HAS NEW QUESTION INFO:
                # MAKE SURE ALL FIELDS ARE NOT EMPTY
                if (question is None) or (answer is None) or (
                        difficulty is None) or (category is None):
                    abort(405)
                else:
                    # CREATE NEW QUESTION USING REQUEST BODY INFO
                    new_question = Question(
                        question=question,
                        answer=answer,
                        difficulty=difficulty,
                        category=category)
                    # INSERT NEW QUESTION INTO DB
                    new_question.insert()

                    current_category = []
                    # RETRIEVE ALL QUESTIONS FROM DB
                    group = Question.query.order_by(Question.id).all()
                    # PAGENATE QUESTIONS
                    current_questions = paginate_questions(request, group)
                    # RETURN LIST OF CURRENT CATEGORIES BASED ON DISPLAYED
                    # QUESTIONS
                    for question in current_questions:
                        current_category.append(question['category'])
                    return jsonify({
                        'created': new_question.id,
                        'questions': current_questions,
                        'total_questions': len(group),
                        'current_category': current_category
                    })
        except BaseException:
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
            # RETRIEVE ALL CATEGORIES FROM DB
            categories = Category.query.all()
            # FORMAT LIST OF CATEGORIES TO JSON TYPE
            formated_categories = [category.format()
                                   for category in categories]
            # RETURN LIST OF ATEGORIES TYPES
            category_type = [category['type']
                             for category in formated_categories]
            # RETRIEVE CATEGORY USING ID FROM DB
            current_category = Category.query.filter_by(
                id=id).first_or_404().format()
            # IF ID IS NOT VALID
            if current_category == 404:
                abort(404)
            else:
                # RETRIEVE ALL CATEGORIES FROM DB
                group = Question.query.filter_by(category=id).all()
                # PAGENATE QUESTIONS
                current_questions = paginate_questions(request, group)
                return jsonify({
                    'categories': category_type,
                    'current_category': current_category['type'],
                    'questions': current_questions,
                    'total_questions': len(group)
                })
        except BaseException:
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
            # RETRIEVE REQUEST BODY IN JSON TYPE
            body = request.get_json()
            # print('body:', body)
            # ASSIGN REQUEST BODYINFO TO VARIABLES
            previous_questions = body.get("previous_questions")
            quiz_category = body.get("quiz_category")
            # print('quiz_category', quiz_category)
            quiz_category_id = int(quiz_category['id'])
            # print('quiz_category_id:', quiz_category_id)
            # IF PLAYER CHOSES ALL CATEGORIES
            if quiz_category == 0:
                # RETRIEVE ALL QUESTIONS FOM DB
                get_questions = Question.query.all()
                # print('get_questions', get_questions, len(get_questions))
                # RANDOMLY CHOSE QUESTION TO DISPLAY IN JSON FORMAT
                random_question = random.choice(get_questions).format()
                # IF PLAYES CHOSES CATEGORY
            else:
                # print('previous_questions', previous_questions, 'quiz_category', quiz_category)
                # RETRIEVE CATEGORY THAT MATCH REQUEST ID FORM DB
                # get_category = Category.query.filter_by(id=quiz_category_id).first_or_404()
                # RETRIEVE ALL QUESTIONS UNDER THE REQUESTED CATEGORY FROM DB
                get_questions = Question.query.filter_by(
                    category=quiz_category_id).all()
                # print('get_questions', get_questions, len(get_questions))
                # RANDOMLY CHOSE QUESTION TO DISPLAY IN JSON FORMAT
                random_question = random.choice(get_questions).format()
                # print('random_question', random_question)
                # MAKE SURE THE RANDOMLY CHOSEN QUESTION IS NOT INCLUDED IN
                # PREVIOUS QUESTION TO PREVENT REPEATING
            if random_question['id'] in previous_questions:
                return
        except BaseException:
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
