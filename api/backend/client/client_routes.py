from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of 
# routes.
client = Blueprint('client', __name__)

@client.route('/', methods=['GET'])
def get_client_id():
    query = '''
        SELECT  u.user_id
        FROM User u
        WHERE u.first_name = 'Jane' AND u.last_name = 'Smith' AND u.role = 'client'
        LIMIT 1;
    '''
    
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of products
    cursor.execute(query)

    # fetch all the data from the cursor
    # The cursor will return the data as a 
    # Python Dictionary
    theData = cursor.fetchone()

    # Create a HTTP Response object and add results of the query to it
    # after "jasonify"-ing it.
    response = make_response(jsonify(theData))
    # set the proper HTTP Status code of 200 (meaning all good)
    response.status_code = 200
    # send the response back to the client
    return response







@client.route('/workouts/by-client/<user_id>/', methods=['GET'])
def get_all_user_made_workouts(user_id):
    query = f'''
        SELECT c.name, c.description
        FROM Circuit c
            JOIN User u ON c.created_by = u.user_id
        WHERE u.role = 'client' AND c.user_id = {user_id};
    '''
    
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

@client.route('/workouts/by-trainer/<client_user_id>', methods=['GET'])
def get_all_trainer_made_workouts_for_user(client_user_id):
    query = f'''
        SELECT c.name, c.description
        FROM Circuit c
            JOIN User u ON c.created_by = u.user_id
        WHERE u.role = 'trainer' AND c.user_id = {client_user_id};
    '''
    
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response








@client.route('/workouts/currently-scheduled-exercises/<user_id>', methods=['GET'])
def all_scheduled_e(user_id):
    query = f'''
        SELECT e.name, es.weight, es.reps, es.duration_seconds, es.is_superset, es.rest_seconds, es.completed
        FROM Circuit c
            JOIN User u ON c.user_id = u.user_id
            JOIN Exercise e ON c.circuit_id = e.circuit_id
            JOIN ExerciseSet es ON e.exercise_id = es.exercise_id
        WHERE c.scheduled_date = CURRENT_DATE AND u.user_id = {user_id}
        ORDER BY c.circuit_id, es.set_order;
    '''
    
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response






@client.route('/workouts/currently-scheduled/next-exercise/<user_id>', methods=['GET'])
def next_up_workout_exercise_information(user_id):
    query = f'''
        SELECT e.name, e.personal_notes, e.video_url
        FROM Exercise e
            JOIN Circuit c ON e.circuit_id = c.circuit_id
            JOIN User u ON c.user_id = u.user_id
            JOIN ExerciseSet es ON e.exercise_id = es.exercise_id
        WHERE c.scheduled_date = CURRENT_DATE AND u.user_id = {user_id}
        GROUP BY e.exercise_id, e.name
        HAVING COUNT(*) > SUM(IF(es.completed = TRUE, 1, 0))
        ORDER BY e.exercise_id
        LIMIT 1;
    '''
    
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

@client.route('/equipment-based-search/', defaults={'equipment_string': ''}, methods=['GET'])
@client.route('/equipment-based-search/<equipment_string>', methods=['GET'])
def make_equipment_based_search(equipment_string):
    cursor = None
    cursor = db.get_db().cursor()
    
    equipment_string = equipment_string.strip()
    
    print(f'THE OUTPUT IS: {equipment_string}')
    
    if(equipment_string == ""):
        query = '''
            SELECT e.name
            FROM Exercise e
        '''
        cursor.execute(query)
    else:
        query = '''
            SELECT e.name
            FROM Exercise e
            WHERE e.equipment_needed LIKE CONCAT('%%', %s, '%%');
        '''
        cursor.execute(query, (equipment_string,))
    
    
    theData = cursor.fetchall()
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response 