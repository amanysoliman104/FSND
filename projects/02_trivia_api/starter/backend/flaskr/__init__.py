import os
from flask import Flask, request, abort, jsonify 
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import func
import random
#from frontend.src.base_url import API_URL

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  #@TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  CORS(app)#resources={r"/*/api/*":{"origins":"*"}})
    

  
  
  #@TODO: Use the after_request decorator to set Access-Control-Allow
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers','Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Credentials',"true")
    #response.headers.add('Access-Control-Allow-Origin')
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
    return jsonify({
      'success':True,
      'questions':current_question,
      'total_questions':len(Question.query.all()),
      'categories':categories_dict,
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
  def create_or_search_question():
      
    body = request.get_json()
    quest = body.get('question', None)
    answer = body.get('answer', None)
    category = body.get('category', None)
    difficulty  =body.get('difficulty',None)
    search_term = body.get('searchTerm',None)
    try:
      if search_term:  
        #questions=Question.query.filter(func.lower(Question.question).contains(search_term.lower())).all()
        questions=Question.query.filter(Question.question.ilike('%{}%'.format(search_term)))
        #formated_quest=[q.format() for q in questions]
        current_questions=paginate_questions(request,questions)

        return jsonify({
          'success': True,
          'questions':current_questions,
          'total_questions':len(questions.all())
          
            })
      else:
            
        question = Question(question=quest, answer=answer, category=category,difficulty=difficulty)
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
  Create a GET endpoint to get questions based on category. 
  
  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:catigory_id>/questions',methods=['GET'])
  def get_questions_by_cateogry(catigory_id):
    cat_questions=[]
    try:
      category=Category.query.get(catigory_id)
      category_type=category.type
      questions=Question.query.filter(Question.category==catigory_id)
      cat_questions=[q.format() for q in questions]
      return jsonify({
        'success':True,
        'questions':cat_questions,
        'total_questions':len(cat_questions),
        'current_category':category_type
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
  @app.route('/quizzes',methods=['POST']) 
  def play_quizze():
    flage=True
    quizquestion_as_dic={}
    body = request.get_json()
    previousquestions=body.get('previous_questions',None)
    quizcategory=body.get('quiz_category',None) #quizcategory is dict
    #quizcategory return type=click id=0 when choise ALL in categories list 

    if quizcategory['type']=='click':
      #pop random question from all_questions list 
      all_questions=Question.query.all()
      try:
        if previousquestions is None: 
          quizquestion_as_list=random.choices(all_questions)

          for q in quizquestion_as_list:
            quizquestion_as_dic={
            'id':q.id,
            'question':q.question,
            'category':q.category,
            'answer':q.answer
            }

          #quizquestion_as_dic=dict(((q.question,q.answer) for q in quizquestion_as_list))
          return jsonify({
            'success':True,
            'question':quizquestion_as_dic,
            'quizCategory':quizcategory,
            'total_quizequestion':len(quizquestion_as_list),
            'total_questions':len(all_questions)

            })
        else:
          #pop random question from all_questions list except  previousQuestions
          quizquestion_as_list=random.choices(all_questions)
          while flage:
            flage=False
            if previousquestions in  quizquestion_as_list:
              flage=True
              quizquestion_as_list=random.choices(all_questions)
          #quizquestion_as_dic=dict(((q.question,q.answer) for q in quizquestion_as_list)) 
          for q in quizquestion_as_list:
            quizquestion_as_dic={
            'id':q.id,
            'question':q.question,
            'category':q.category,
            'answer':q.answer
            }  
          return jsonify({
            'success':True,
            'question':quizquestion_as_dic,
            'total_quizequestion':len(quizquestion_as_list),
            'total_questions':len(all_questions)
            })
      except:
        abort(404)
    else:
      #pop random question from all_questions for spacific  category list
      category_id=quizcategory['id']
      questions_of_category=Question.query.filter(Question.category==category_id).all()
      try:
        
        if previousquestions is None:
          
          # choices return list 
          quizquestion_as_list=random.choices(questions_of_category)
          for q in quizquestion_as_list:
            quizquestion_as_dic={
            'id':q.id,
            'question':q.question,
            'category':q.category,
            'answer':q.answer
            }

          #quizquestion_as_dic=dict(((q.question,q.answer) for q in quizquestion_as_list))
          return jsonify({
            'success':True,
            'question':quizquestion_as_dic,
            'quizCategory':quizcategory,
            'total_quizequestion':len(quizquestion_as_list),
            'total_questions':len(questions_of_category)

            })
        else:
          #pop random question from all_questions list except  previousQuestions
          quizquestion_as_list=random.choices(questions_of_category)
          while flage:
            flage=False
            if previousquestions in  quizquestion_as_list:
              flage=True
              quizquestion_as_list=random.choices(questions_of_category)
          #quizquestion_as_dic=dict(((q.question,q.answer) for q in quizquestion_as_list)) 
          for q in quizquestion_as_list:
            quizquestion_as_dic={
            'id':q.id,
            'question':q.question,
            'category':q.category,
            'answer':q.answer
            }  
          return jsonify({
            'success':True,
            'question':quizquestion_as_dic,
            'total_quizequestion':len(quizquestion_as_list),
            'total_questions':len(questions_of_category)
            })

      except:
        abort(404)

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False, 
      "error": 404,
      "message": "resource not found"
      }), 404

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


  return app

    