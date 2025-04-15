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

@client.route('/workouts/by-trainer/<client_user_id>/', methods=['GET'])
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



@client.route('/workouts/currently-scheduled-exercises/<user_id>/', methods=['GET'])
def all_scheduled_exercises(user_id):
    query = f'''
        SELECT c.name AS `CircuitName`, c.target_muscle, e.name, es.weight, es.reps, es.duration_seconds, es.is_superset, es.rest_seconds, es.completed, es.set_order
        FROM Circuit c
            JOIN User u ON c.user_id = u.user_id
            JOIN Exercise e ON c.circuit_id = e.circuit_id
            JOIN ExerciseSet es ON e.exercise_id = es.exercise_id
        WHERE c.scheduled_date = CURRENT_DATE AND u.user_id = {user_id}
        ORDER BY c.circuit_id, e.name, es.set_order;
    '''
    
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response


@client.route('/test/<user_id>', methods=['GET'])
def blagkwfannfa(user_id):
    query = f'''
    SELECT c.name
        FROM Circuit c
            JOIN User u ON c.user_id = u.user_id
        WHERE u.user_id = {user_id}
        ''' 
    
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response



@client.route('/workouts/currently-scheduled/next-exercise/<user_id>/', methods=['GET'])
def next_up_workout_exercise_information(user_id):
    query = f'''
        SELECT e.name, e.personal_notes, e.video_url, e.target_muscle, es.reps, es.duration_seconds, es.is_superset, es.weight, es.rest_seconds
        FROM Exercise e
            JOIN Circuit c ON e.circuit_id = c.circuit_id
            JOIN User u ON c.user_id = u.user_id
            JOIN ExerciseSet es ON e.exercise_id = es.exercise_id
        WHERE c.scheduled_date = CURRENT_DATE AND u.user_id = {user_id}
        GROUP BY e.exercise_id, es.set_order, e.name, e.personal_notes, e.video_url, e.target_muscle,
            es.reps, es.duration_seconds, es.is_superset, es.weight, es.rest_seconds
        HAVING COUNT(*) > SUM(IF(es.completed = TRUE, 1, 0))
        ORDER BY e.exercise_id, es.set_order
        LIMIT 1;
    '''
    
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

@client.route('/equipment-based-search/', defaults={'equipment_string': ''}, methods=['GET'])
@client.route('/equipment-based-search/<equipment_string>/', methods=['GET'])
def make_equipment_based_search(equipment_string):
    cursor = None
    cursor = db.get_db().cursor()
    
    equipment_string = equipment_string.strip()
    
    if(equipment_string == ""):
        query = '''
            SELECT e.name, e.equipment_needed
            FROM Exercise e
        '''
        cursor.execute(query)
    else:
        query = '''
            SELECT e.name, e.equipment_needed
            FROM Exercise e
            WHERE e.equipment_needed LIKE CONCAT('%%', %s, '%%');
        '''
        cursor.execute(query, (equipment_string,))
    
    
    theData = cursor.fetchall()
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response 


@client.route('/difficulty-based-search/<beginner>/<intermediate>/<advanced>/', methods=['GET'])
def make_difficulty_based_search(beginner, intermediate, advanced):
    query = '''
            SELECT e.name, e.difficulty
            FROM Exercise e
        '''
    
    prevDifficulty = False
    
    if beginner:
        query += " WHERE e.difficulty = 'beginner'"
        prevDifficulty = True
    
    if intermediate and prevDifficulty:
        query += " OR e.difficulty = 'intermediate'"
        prevDifficulty = True
    elif intermediate:
        query += " WHERE e.difficulty = 'intermediate'"

    if advanced and prevDifficulty:
        query += " OR e.difficulty = 'advanced'"
        prevDifficulty = True
    elif advanced:
        query += " WHERE e.difficulty = 'advanced'"    
    
    query += ";"
    
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response 


@client.route('/target-muscle-based-search/', defaults={'target_muscle_string': ''}, methods=['GET'])
@client.route('/target-muscle-based-search/<target_muscle_string>/', methods=['GET'])
def make_target_muscle_based_search(target_muscle_string):
    cursor = None
    cursor = db.get_db().cursor()
    
    equipment_string = target_muscle_string.strip()
    
    if(target_muscle_string == ""):
        query = '''
            SELECT e.name, e.target_muscle
            FROM Exercise e
        '''
        cursor.execute(query)
    else:
        query = '''
            SELECT e.name, e.target_muscle
            FROM Exercise e
            WHERE e.target_muscle LIKE CONCAT('%%', %s, '%%');
        '''
        cursor.execute(query, (target_muscle_string,))
    
    
    theData = cursor.fetchall()
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response 




@client.route('/exercise-type-based-search/', defaults={'exercise_type_string': ''}, methods=['GET'])
@client.route('/exercise-type-based-search/<exercise_type_string>/', methods=['GET'])
def make_exercise_type_based_search(exercise_type_string):
    cursor = None
    cursor = db.get_db().cursor()
    
    equipment_string = exercise_type_string.strip()
    
    if(exercise_type_string == ""):
        query = '''
            SELECT e.name, e.exercise_type
            FROM Exercise e
        '''
        cursor.execute(query)
    else:
        query = '''
            SELECT e.name, e.exercise_type
            FROM Exercise e
            WHERE e.exercise_type LIKE CONCAT('%%', %s, '%%');
        '''
        cursor.execute(query, (exercise_type_string,))
    
    
    theData = cursor.fetchall()
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response 

   
   
   
@client.route('/workouts/next-scheduled/video-url/<user_id>/', methods=['GET'])
def next_up_workout_exercise_video_url(user_id):
    query = f'''
        SELECT e.name, e.video_url
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

@client.route('/health/tip/', methods=['GET'])
def get_health_tip():
    query = f'''
        SELECT ht.text
        FROM HealthTips ht
        ORDER BY RAND()
        LIMIT 1;
    '''
    
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

@client.route('/motivation/tip/', methods=['GET'])
def get_motivation_tip():
    query = f'''
        SELECT m.text
        FROM Motivation m
        ORDER BY RAND()
        LIMIT 1;
    '''
    
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

@client.route('/health/today-meal-breakdown/<user_id>/', methods=['GET'])
def todays_meal_breakdown(user_id):
    query = f'''
        SELECT fl.meal_type, SUM(fi.calories) AS `calories`, SUM(fi.protein) AS `protein`, SUM(fi.carbs) AS `carbs`, SUM(fi.fats) AS `fats`
        FROM User u
            JOIN FoodLog fl ON u.user_id = fl.user_id
            JOIN FoodLog_FoodItem flfi on fl.food_log_id = flfi.food_log_id
            JOIN FoodItem fi on flfi.food_item_id = fi.food_item_id
        WHERE fl.date_logged = CURRENT_DATE AND u.user_id = {user_id}
        GROUP BY fl.meal_type;
    '''
    
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response


   
@client.route('/food/food_intake_information/<meal_type>/<user_id>/', methods=['GET'])
def food_intake_information(meal_type, user_id):
    query = f'''
        SELECT log.meal_type, item.name, item.calories, item.protein, item.carbs, item.fats
        FROM FoodLog log
            JOIN FoodLog_FoodItem logItem ON log.food_log_id = logItem.food_log_id
            JOIN FoodItem item ON logItem.food_item_id = item.food_item_id
            JOIN User u ON log.user_id = u.user_id
        WHERE log.date_logged = CURRENT_DATE AND u.user_id = {user_id} AND log.meal_type = {meal_type}
        ORDER BY log.meal_type;
    '''
    
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

@client.route('/food/food_intake_information/all-nutrients-combined-for-day/<num_days>/<user_id>/', methods=['GET'])
def all_nutrients_for_that_day(num_days, user_id):
    query = f'''
        SELECT log.date_logged AS `Date`, SUM(item.calories) AS `Calories`, SUM(item.protein) AS `Protein`, SUM(item.carbs) AS `Carbohydrates`, SUM(item.fats) AS `Fats`
        FROM FoodLog log
            JOIN FoodLog_FoodItem logItem ON log.food_log_id = logItem.food_log_id
            JOIN FoodItem item ON logItem.food_item_id = item.food_item_id
            JOIN User u ON log.user_id = u.user_id
        WHERE log.date_logged BETWEEN DATE_SUB(CURRENT_DATE, INTERVAL {num_days} DAY) AND CURRENT_DATE AND u.user_id = {user_id}
        GROUP BY log.date_logged
        ORDER BY log.date_logged;
    '''
    
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

@client.route('/exercise/search-filter/name/equipment/muscle_group/difficulty/<difficulty>/exercise_type/<exercise_type>/', 
              defaults={'name': '', 'equipment': '', 'muscle_group': ''}, methods=['GET'])
@client.route('/exercise/search-filter/name/<name>/equipment/muscle_group/difficulty/<difficulty>/exercise_type/<exercise_type>/', 
              defaults={'equipment': '', 'muscle_group': ''}, methods=['GET'])
@client.route('/exercise/search-filter/name/equipment/<equipment>/muscle_group/difficulty/<difficulty>/exercise_type/<exercise_type>/', 
              defaults={'name': '', 'muscle_group': ''}, methods=['GET'])
@client.route('/exercise/search-filter/name/equipment/muscle_group/<muscle_group>/difficulty/<difficulty>/exercise_type/<exercise_type>/', 
              defaults={'name': '', 'equipment': ''}, methods=['GET'])
@client.route('/exercise/search-filter/name/<name>/equipment/<equipment>/muscle_group/difficulty/<difficulty>/exercise_type/<exercise_type>/', 
              defaults={'muscle_group': ''}, methods=['GET'])
@client.route('/exercise/search-filter/name/<name>/equipment/muscle_group/<muscle_group>/difficulty/<difficulty>/exercise_type/<exercise_type>/', 
              defaults={'equipment': ''}, methods=['GET'])
@client.route('/exercise/search-filter/name/equipment/<equipment>/muscle_group/<muscle_group>/difficulty/<difficulty>/exercise_type/<exercise_type>/', 
              defaults={'name': ''}, methods=['GET'])
@client.route('/exercise/search-filter/name/<name>/equipment/<equipment>/muscle_group/<muscle_group>/difficulty/<difficulty>/exercise_type/<exercise_type>/', methods=['GET'])
def exercise_search(name, equipment, muscle_group, difficulty, exercise_type):
    name = name.strip()
    equipment = equipment.strip()
    muscle_group = muscle_group.strip()
    
    params = [difficulty, exercise_type]

    query = '''
            SELECT e.exercise_id, e.name, e.equipment_needed, e.target_muscle, e.difficulty, e.exercise_type, e.video_url
            FROM Exercise e
            WHERE e.difficulty = %s AND e.exercise_type = %s
        '''
        
    if name != "" and name != None:
        query += " AND e.name LIKE CONCAT('%%', %s, '%%')"
        params.append(name)
    if equipment != "" and equipment != None:
        query += " AND e.equipment_needed LIKE CONCAT('%%', %s, '%%')"
        params.append(equipment)
    if muscle_group != "" and muscle_group != None:
        query += " AND e.target_muscle LIKE CONCAT('%%', %s, '%%')"
        params.append(muscle_group)
        
    query += ";"    
    
    cursor = db.get_db().cursor()
    cursor.execute(query, tuple(params))
    theData = cursor.fetchall()
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

@client.route('/insert/circuit/<user_id>/<circuit_name>/<circuit_description>/', methods=["POST"])
def insert_circuit(user_id, circuit_name, circuit_description):
    query = '''
        INSERT INTO Circuit(user_id, created_by, name, description, circuit_type, difficulty, target_muscle, equipment_needed)
        VALUES (%s, %s, %s, %s, 'strength', 'beginner', 'No Target Muscle', 'No Equipment Needed')
    '''
    
    connection = db.get_db()
    cursor = connection.cursor()
    try:
        cursor.execute(query, (user_id, user_id, circuit_name, circuit_description))
        connection.commit()
        # Return a success message (no rows are returned by an INSERT)
        response = make_response(jsonify({"status": "success", "message": "Circuit inserted successfully."}))
        response.status_code = 200
    except Exception as e:
        connection.rollback()
        response = make_response(jsonify({"error": str(e)}))
        response.status_code = 400
    finally:
        cursor.close()
    return response