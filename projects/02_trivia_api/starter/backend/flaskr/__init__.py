import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
#from frontend.src.base_url import API_URL

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  #@TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  CORS(app)
    

  
  
  #@TODO: Use the after_request decorator to set Access-Control-Allow
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers','Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods','GET,POST,PATCH,DELETE')
    return response


  def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start =  (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
    categories=Category.query.all()
    # current catogory is catogeries in one page is  10
    categories_dict=dict(((c.id,c.type) for c in categories))

    return jsonify({
      'success':True,
      'categories':categories_dict,
      'total_categories':len(categories)
      })



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
    categories=Category.query.all()
    categories_dict=dict(((c.id,c.type) for c in categories))
    #temp_list=[]
    questions=Question.query.all()
    current_question=paginate_questions(request,questions)
    # for cat_id in current_question:
    #   category=Category.query.get(cat_id['category'])
    #   if not(cat_id['category'] in temp_list):
    #     categories.append(category)
    #   temp_list.append(cat_id['category'])
    # print(categories)
    # #cat_dict=dict(for c in categories)
    return jsonify({
      'success':True,
      'questions':current_question,
      'total_questions':len(Question.query.all()),
      'categories':categories_dict
      })

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()

      if question is None:
        abort(404)

      question.delete()
      questions = Question.query.order_by(Question.id).all()
      current_questions =paginate_questions(request,questions)

      return jsonify({
        'success': True,
        'deleted': question_id,
        'questions':current_questions,
        'total_questions': len(Question.query.all())
      })

    except:
      abort(404)

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def create_or_search_question():
    
    body = request.get_json()
    search_term = body.get('searchTerm')
    if search_term:
      try:
        
        print("ooooooooooooooooooo "+search_term)
        questions=Question.query.filter(func.lower(Question.question).contains(search_term.lower())).all()
        formated_quest=[q.format() for q in questions]
        
        return jsonify({
          'success': True,
          'questions':formated_quest,
          'total_questions':len(questions)

          })
      except:
        abort(404) 
    else:
    
      question = body.get('question', None)
      answer = body.get('answer', None)
      category = body.get('category', None)
      difficulty  =body.get('difficulty',None)
      try:
        question = Question(question=question, answer=answer, category=category,difficulty=difficulty)
        question.insert()

        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)
       
        return jsonify({
          'success': True,
          'created': question.id,
          'questions': current_questions,
          'total_questions': len(Question.query.all())
        })

      except:
        abort(422)

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''


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

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  return app

    