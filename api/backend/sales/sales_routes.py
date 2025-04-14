from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of
# routes.
sales = Blueprint('sales', __name__)

#------------------------------------------------------------
# Post the user survey which gets their demographics
@sales.route('/user_survey', methods=['POST'])
def post_sale_survey():
    data = request.json()

    #extracting the variable
    user_id = data['user_id']
    age = data['age']
    gender = data['gender']
    ethnicity = data['ethnicity']
    fitness_experience = data['fitness_experience']

    query = f'''
        INSERT INTO Demographics (user_id, age, gender, ethnicity, fitness_experience)
        VALUES ({user_id}, {age}, '{gender}', '{ethnicity}', '{fitness_experience}')
    '''

    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of products
    cursor.execute(query)

    db.get_db().commit()

    response = make_response("Succesfully added demographics! Thank you!")
    response.status_code = 200
    return response

#------------------------------------------------------------
# Post the feedback survey which gets the users feedback on our app
@sales.route('/feedback_survey', methods=['POST'])
def post_feedback_survey():
    data = request.json

    # extracting the variables
    user_id = data['user_id']
    app_discovery = data['app_discovery']
    app_enjoyment = data['app_enjoyment']
    improvement_suggestions = data['improvement_suggestions']
    similar_apps = data['similar_apps']
    most_useful_feature = data['most_useful_feature']

    # SQL query to insert feedback data
    query = f'''
        INSERT INTO AppFeedback (user_id, app_discovery, app_enjoyment, improvement_suggestions, similar_apps,
         most_useful_feature)
        VALUES ({user_id}, '{app_discovery}', '{app_enjoyment}', '{improvement_suggestions}', '{similar_apps}',
         '{most_useful_feature}')
    '''

    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of products
    cursor.execute(query)

    db.get_db().commit()

    response = make_response("Successfully added feedback! Thank you for helping us improve MotionMAX!")
    response.status_code = 200
    return response