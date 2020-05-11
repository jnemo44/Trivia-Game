import os
from flask import Flask, request, abort, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
  page = request.args.get('page',1,type=int)
  start = (page-1)*QUESTIONS_PER_PAGE
  end = start+QUESTIONS_PER_PAGE

  formated_questions = [question.format() for question in selection]
  current_questions = formated_questions[start:end]

  return current_questions

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  #Enable CORS. Allow '*' for origins.
  CORS(app, resources={r"/api/*": {"origins": '*'}})

  #Use the after_request decorator to set Access-Control-Allow
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    #response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response
 
  #Endpoint to handle GET requests for all available categories.
  @app.route('/categories', methods=['GET'])
  def view_categories():
    categories = Category.query.all()
    formated_categories = {cat.id:cat.type for cat in categories}

    if formated_categories == {}:
      abort(404)

    return jsonify({
      'success':True,
      'categories': formated_categories
    })

 
  #Endpoint to handle GET requests for questions, 
  #including pagination (every 10 questions).
  
  #TEST: At this point, when you start the application
  #you should see questions and categories generated,
  #ten questions per page and pagination at the bottom of the screen for three pages.
  #Clicking on the page numbers should update the questions. 

  @app.route('/questions', methods=['GET'])
  def view_questions():
    questions = Question.query.all()
    current_questions = paginate_questions(request,questions)

    if len(current_questions) == 0:
      abort(404)
      return jsonify({
        'success':False
      })

    #Provide list of categories
    categories = Category.query.all()
    formated_categories = {cat.id:cat.type for cat in categories}

    return jsonify ({
      'success':True,
      'questions': current_questions,
      'total_questions': len(questions),
      'categories': formated_categories,
      'currentCategory': 1
    })


  #Endpoint to DELETE question using a question ID. 
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    deleted_question = Question.query.filter(Question.id == question_id).one_or_none()

    try:
      if delete_question is None:
        abort(404)
      else:
        deleted_question.delete()

        questions = Question.query.all()
        current_questions = paginate_questions(request,questions)      

        return ({
          'success':True,
          'questions':current_questions
        })
    except:
      abort(422)


  # POST endpoint that takes a search parameter
  #or new question parameters to either search 
  #the questions db or add a new question respectivly.

  #TEST: When you submit a question on the "Add" tab, 
  #the form will clear and the question will appear at the end of the last page
  #of the questions list in the "List" tab.  
  @app.route('/questions', methods=['POST'])
  def add_question():
    body = request.get_json()
    try:
      new_search = body.get('searchTerm',None)
      #If no search term a new question is being added
      if new_search is None:
      
        new_question = body.get('question',None)
        new_answer = body.get('answer',None)
        new_category = body.get('category',None)
        new_difficulty = body.get('difficulty',None)
        #Build new question from model
        question = Question(question=new_question,answer=new_answer,category=new_category,difficulty=new_difficulty)
        #Insert question into the DB
        question.insert()

        return jsonify({
          'success':True
        })
        
    #Search is being performed
      else:
        question_results = Question.query.filter(Question.question.ilike('%'+new_search+'%'))
        current_results = paginate_questions(request,question_results)

        return jsonify({
          'success':True,
          'questions':current_results,
          'total_questions':len(question_results.all()),
          'current_category':{}
        })
    except:
      abort(422)

  #GET endpoint to get questions based on category. 

  #TEST: In the "List" tab / main screen, clicking on one of the 
  #categories in the left column will cause only questions of that 
  #category to be shown. 
  @app.route('/categories/<int:cat_id>/questions')
  def view_question_category(cat_id):
    questions = Question.query.filter(Question.category == cat_id).all()
    current_questions = paginate_questions(request,questions)
    
    if len(current_questions) == 0:
      abort(404)

    return jsonify({
      'success':True,
      'questions':current_questions,
      'total_questions':len(questions),
      'current_category':cat_id
    })

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
  def play_quiz():
    #Init previous_questions to handle first question
    previous_questions = []
    body = request.get_json()
    try:
      #Get category id
      cat_id = body['quiz_category']['id']
      #A different way to get something from JSON
      previous_questions = body.get('previous_questions', None)
      #If ALL categories is selected
      if cat_id == 0:
        quiz_questions = Question.query.all()
      #Else filter questions by cat_id
      else:
        quiz_questions = Question.query.filter(Question.category == cat_id).all()

      #Decide if the quiz is finished
      if len(previous_questions) == len(quiz_questions):
        return jsonify({
          'success':True,
          'question':False
        })
      #Randomly select a question that hasn't been asked  
      else: 
        current_question = random.choice([question for question in quiz_questions if question.id not in previous_questions])
        previous_questions.append(current_question.id)
        return jsonify({
          'success':True,
          'question':{
            'question':current_question.question,
            'answer':current_question.answer,
            'id':current_question.id,
            'category':current_question.category,
            'difficulty':current_question.difficulty
            }
        })
    except:
      abort(422)

  #Error handler creation
  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
          'success':False,
          'error':404,
          'message':'Resource not found!'
      }),404

  @app.errorhandler(422)
  def unproccesable(error):
    return jsonify({
          'success':False,
          'error':422,
          'message':'Unprocessable'
      }),422

  
  return app

    