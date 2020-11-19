# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.8

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

====================
** Error Handling **
====================
Errors are returnes as JSON objects in the following format: 
{
    "success": False,
    "error": 422,
    "message": "unprocessable"
}

The API will return 5 error types when request fails:

422: "unprocessable"
400: "bad request"
404: "content not found"
405: "method not allowed"
500: "internal server error"


===============
** Endpoints **
===============
GET '/categories'
GET '/questions'
DELETE '/questions/<int:id>'
POST '/questions'
GET '/categories/<int:id>/questions'
POST '/quizzes'

GET '/categories'
=================
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a list of category_string .
- Sample:  curl http://localhost:5000/categories
["Science", "Art", "Geography", "History", "Entertainment", "Sports"]

```
GET '/questions'
================
- Fetches a dictionary of questions in which the keys are: id, question, answer, difficulty, category and dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: page number
- Returns: An object of questions: [array contains objects of questions key:value pairs pagenated by 10 questions per page], total_questions:number of total questions , current_category: [array of category ids of current displayed questions], categories: [array of category_string] in key:value pairs.
- Sample:  curl http://localhost:5000/questions

{
    "categories": [
         "Science",
        "Art"
    ],
    "current_category": [
        5,
        4
    ],
    "questions": [
        {
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        },
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        }
    ],
    "total_questions": 18
}
`````
DELETE '/questions/<int:id>'
============================
- Deletes a question from database and from page when refreshed, using a question ID
- Request Arguments: question ID
- Returns: an object of success value,the deleted question id, list of questions pagenated by 10 per page, number of total questions, current category ids,  list of category string, in key:value pairs.
- Sample: curl -X DELETE http://localhost:5000/questions/3

{
    "categories": [
         "Science",
        "Art"
    ],
    "current_category": [
        5,
        4
    ],
    "questions": [
        {
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        },
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        }
    ],
    "total_questions": 17,
    'success': True,
    'deleted': 3,
}
````
POST '/questions'
=================
- Creates a new question using submitted question, answer,difficulty,category, returns the newly created question id, list of questions pagenated by 10 per page, number of total questions, current category ids in key:value pairs.

- OR performs search in questions using submitted string, returns list of questions that contains the string in any part of the question bosy pagenated by 10 per page, number of total questions, current category ids, in key:value pairs.
- Request Arguments: searchTerm

- Sample 1: curl http://localhost:5000/questions -X POST -M "Content-Type: application/json" -d "{"searchTerm": "title"}"
{
    "current_category": [
        5,
        4
    ],
    "questions": [
        {
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        },
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 25,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        }
    ],
    "total_questions": 2
}

- Sample 2: curl http://localhost:5000/questions -X POST -M "Content-Type: application/json" -d "{"question":"Which Dutch graphic artist–initials M C was a creator of optical illusions?","answer":"Escher","difficulty":1,"category":2}"
{
    "created": 28,
    "current_category": [
        5,
        4
    ],
    "questions": [
        {
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        },
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        }
    ],
    "total_questions": 19
}
`````
GET '/categories/<int:id>/questions'
===================================
- Fetches list of questions based on category, and returns an object with all categories, current category object with id:type key:value pairs, list of questions based on category, total number of questions in that category
- Sample : curl http://localhost:5000/categories/4/questions
{
    "categories": [
         "Science",
        "Art"
    ],
    "current_category": {
        "id": 4,
        "type": "History"
    },
    "questions": [
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        },
        {
            "answer": "George Washington Carver",
            "category": 4,
            "difficulty": 2,
            "id": 12,
            "question": "Who invented Peanut Butter?"
        },
        {
            "answer": "Scarab",
            "category": 4,
            "difficulty": 4,
            "id": 23,
            "question": "Which dung beetle was worshipped by the ancient Egyptians?"
        },
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 25,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        }
    ],
    "total_questions": 4
}

`````
POST '/quizzes'
===============
- Fetches list of qestions, and return a random question within the given category, if provided, and that is not one of the previous questions
- Request Arguments: category and previous questions
- Sample : curl http://localhost:5000/quizzes -X POST -M "Content-Type: application/json" -d "{"previous_questions":[],"quiz_category":4}"
{
  "question": {
    "answer": "Scarab", 
    "category": 4, 
    "difficulty": 4, 
    "id": 23, 
    "question": "Which dung beetle was worshipped by the ancient Egyptians?"
  }
}


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
================
** Deployment **
================
N/A