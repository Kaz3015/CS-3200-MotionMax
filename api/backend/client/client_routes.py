from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

#Create a blueprint
client = Blueprint('client', __name__)

#Route to get a client's user id based on their first and last name
@client.route('/<first_name>/<last_name>/', methods=['GET'])
def get_client_id(first_name, last_name):
    query = f'''
        SELECT  u.user_id
        FROM User u
        WHERE u.first_name = '{first_name}' AND u.last_name = '{last_name}' AND u.role = 'client'
        LIMIT 1;
    '''
    
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchone()
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

#Route to get a list of circuits made by the user for themself
@client.route('/workouts/by-client/<user_id>/', methods=['GET'])
def get_all_user_made_workouts(user_id):
    query = f'''
        SELECT c.name
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

#Route to get a list of circuits made by a trainer for a client
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

#Route to get all of the exercise sets for today's scheduled workout for a user
@client.route('/workouts/currently-scheduled-exercises/<user_id>/<circuit_id>/', methods=['GET'])
def all_scheduled_exercises(user_id, circuit_id):
    query = f'''
        SELECT c.name AS `CircuitName`, c.target_muscle, e.name, es.weight, es.reps, es.duration_seconds, es.is_superset, es.rest_seconds, es.completed, es.set_order
        FROM Circuit c
            JOIN User u ON c.user_id = u.user_id
            JOIN Exercise e ON c.circuit_id = e.circuit_id
            JOIN ExerciseSet es ON e.exercise_id = es.exercise_id
        WHERE c.scheduled_date = CURRENT_DATE AND u.user_id = {user_id} AND c.circuit_id = {circuit_id}
        ORDER BY c.circuit_id, e.name, es.set_order;
    '''
    
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

#Route to get the next incomplete exercise set for today's workout
@client.route('/workouts/currently-scheduled/next-exercise/<user_id>/', methods=['GET'])
def next_up_workout_exercise_information(user_id):
    query = f'''
        SELECT c.circuit_id, es.exerciseset_id, e.exercise_id, e.name, e.personal_notes, e.video_url, e.target_muscle, es.reps, es.duration_seconds, es.is_superset, es.weight, es.rest_seconds
        FROM Exercise e
            JOIN Circuit c ON e.circuit_id = c.circuit_id
            JOIN User u ON c.user_id = u.user_id
            JOIN ExerciseSet es ON e.exercise_id = es.exercise_id
        WHERE c.scheduled_date = CURRENT_DATE AND u.user_id = {user_id}
        GROUP BY c.circuit_id, es.exerciseset_id, e.exercise_id, es.set_order, e.name, e.personal_notes, e.video_url, e.target_muscle,
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

#Route to get the video url for the next scheduled exercise set
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

#Route to get a random general health tip
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

#Route to return a random motivational tip
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

#Route to get all food items logged today for a specific meal type
@client.route('/food/food_intake_information/<meal_type>/<user_id>/', methods=['GET'])
def food_intake_information(meal_type, user_id):
    query = f'''
        SELECT log.meal_type, item.name, item.calories, item.protein, item.carbs, item.fats, logItem.servings
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

#Route to summarize macro intake for the past <num_days> days
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

#Route to filter exericses by name, equipment, muscle group, difficulty, and exercise type
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

    filters = []
    params = []

    if difficulty.lower() != 'all':
        filters.append("e.difficulty = %s")
        params.append(difficulty)

    if exercise_type.lower() != 'all':
        filters.append("e.exercise_type = %s")
        params.append(exercise_type)

    if name:
        filters.append("e.name LIKE %s")
        params.append(f"%{name}%")

    if equipment:
        filters.append("e.equipment_needed LIKE %s")
        params.append(f"%{equipment}%")

    if muscle_group:
        filters.append("e.target_muscle LIKE %s")
        params.append(f"%{muscle_group}%")

    query = """
        SELECT
          MIN(e.exercise_id) AS exercise_id,
          e.name,
          ANY_VALUE(e.equipment_needed) AS equipment_needed,
          ANY_VALUE(e.target_muscle) AS target_muscle,
          ANY_VALUE(e.difficulty) AS difficulty,
          ANY_VALUE(e.exercise_type) AS exercise_type,
          ANY_VALUE(e.video_url) AS video_url,
          ANY_VALUE(e.description) AS description
        FROM Exercise e
    """

    if filters:
        query += " WHERE " + " AND ".join(filters)

    query += """
        GROUP BY e.name
        ORDER BY e.name;
    """

    cursor = db.get_db().cursor()
    cursor.execute(query, tuple(params))
    rows = cursor.fetchall()
    cursor.close()
    return jsonify(rows), 200

#Route to create a new circuit enty for a specific user id
@client.route('/insert/circuit/<user_id>/<circuit_name>/<circuit_description>/<scheduled_date>/', methods=["POST"])
def insert_circuit(user_id, circuit_name, circuit_description, scheduled_date):
    query = '''
        INSERT INTO Circuit(user_id, created_by, name, description, circuit_type, difficulty, target_muscle, equipment_needed, scheduled_date)
        VALUES (%s, %s, %s, %s, 'strength', 'beginner', 'No Target Muscle', 'No Equipment Needed', %s);
    '''
    
    connection = db.get_db()
    cursor = connection.cursor()
    try:
        cursor.execute(query, (user_id, user_id, circuit_name, circuit_description, scheduled_date))
        connection.commit()
        response = make_response(jsonify({"status": "success", "message": "Circuit inserted successfully."}))
        response.status_code = 200
    except Exception as e:
        connection.rollback()
        response = make_response(jsonify({"error": str(e)}))
        response.status_code = 400
    finally:
        cursor.close()
    return response

#Route to retrieve the most recently created circuit id for a specific user
@client.route('/select/newly-made-circuit-id/<user_id>/', methods=["GET"])
def get_newly_made_circuit_id(user_id):
    query = '''
        SELECT c.circuit_id
        FROM Circuit c
        ORDER BY circuit_id DESC
        LIMIT 1;
    '''
    
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

#Route to insert an exercise into a specific circuit id
@client.route('/insert/exercise_to_circuit/<circuit_id>/', methods=["POST"])
def insert_exercise_to_circuit(circuit_id):
    exercise_info = request.get_json()
    name = exercise_info["exercise_name"]
    exercise_id = exercise_info["exercise_id"]
    exercise_type = exercise_info["exercise_type"]
    exercise_difficulty = exercise_info["exercise_difficulty"]
    exercise_target_muscle = exercise_info["exercise_target_muscle"]
    exercise_equipment = exercise_info["exercise_equipment"]
    video_url = exercise_info["video_url"]
    full_set_info = exercise_info["sets"]
    
    query = f'''
        INSERT INTO Exercise(circuit_id, name, description, exercise_type, difficulty, target_muscle, equipment_needed, video_url, personal_notes)
        VALUES({circuit_id}, '{name}', 'no description', '{exercise_type}', '{exercise_difficulty}', '{exercise_target_muscle}', '{exercise_equipment}', '{video_url}', 'no notes');
    '''
    
    connection = db.get_db()
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        response = make_response(jsonify({"status": "success", "message": "Exercise inserted successfully."}))
        response.status_code = 200
    except Exception as e:
        connection.rollback()
        response = make_response(jsonify({"error": str(e)}))
        response.status_code = 400
    finally:
        cursor.close()
    return response
    
#Route to get the last added exercise to a circuit
@client.route('/select/last_exercise_added_to_circuit/<user_id>/<circuit_id>/', methods=["GET"])
def get_last_exercise_added_to_circuit(user_id, circuit_id):
    query = f'''
        SELECT e.exercise_id, e.name
        FROM Circuit c
            JOIN Exercise e ON c.circuit_id = e.circuit_id
            JOIN User u ON c.user_id = u.user_id
        WHERE u.user_id = {user_id} AND c.circuit_id = {circuit_id}  
        ORDER BY e.exercise_id DESC
        LIMIT 1;
    '''
    
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response
    
#Route to add an exercise set to a exercise in a circuit
@client.route('/insert/exercise_set_to_circuit/<exercise_id>/<set_order>/<weight>/<reps>/<duration>/<superset>/<rest>/', methods=["POST"])
def insert_exercise_set_to_exercise(exercise_id, set_order, weight, reps, duration, superset, rest):
    query = f'''
        INSERT INTO ExerciseSet(exercise_id, weight, reps, duration_seconds, is_superset, rest_seconds, completed, set_order)
            VALUES({exercise_id}, {weight}, {reps}, {duration}, {superset}, {rest}, FALSE, {set_order})
    '''   
    
    connection = db.get_db()
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        response = make_response(jsonify({"status": "success", "message": "ExerciseSet inserted successfully."}))
        response.status_code = 200
    except Exception as e:
        connection.rollback()
        response = make_response(jsonify({"error": str(e)}))
        response.status_code = 400
    finally:
        cursor.close()
    return response 

#Route to mark a specific exercise set as completed
@client.route('/update/complete_exercise_set/<exercise_id>/<exerciseset_id>/', methods=["PUT"])
def update_exerciseset_to_mark_set_completed(exercise_id, exerciseset_id):
    query = f'''
            UPDATE ExerciseSet es
                SET es.completed = TRUE
                WHERE es.exercise_id = {exercise_id} AND es.exerciseset_id = {exerciseset_id}
        '''   
    
    connection = db.get_db()
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        response = make_response(jsonify({"status": "success", "message": "ExerciseSet inserted successfully."}))
        response.status_code = 200
    except Exception as e:
        connection.rollback()
        response = make_response(jsonify({"error": str(e)}))
        response.status_code = 400
    finally:
        cursor.close()
    return response 

#Route to get the food log for a specific meal type
@client.route('/select/food_log/<user_id>/<meal_type>/', methods=["GET"])
def get_food_log(user_id, meal_type):
    query = '''
        SELECT fl.food_log_id
        FROM FoodLog fl
            JOIN User u ON fl.user_id = u.user_id
        WHERE fl.meal_type = %s AND fl.user_id = %s AND fl.date_logged = CURRENT_DATE
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (meal_type, user_id))
    rows = cursor.fetchall()
    cursor.close()
    return jsonify(rows), 200

#Route to add a food log for a specific meal type for a specific user id
@client.route('/insert/insert_food_log/<user_id>/<meal_type>/', methods=["POST"])
def insert_food_log(user_id, meal_type):
    query = """
        INSERT INTO FoodLog (user_id, meal_type, date_logged)
        VALUES (%s, %s, CURRENT_DATE)
    """
    conn = db.get_db()
    cursor = conn.cursor()
    try:
        cursor.execute(query, (user_id, meal_type))
        conn.commit()
        food_log_id = cursor.lastrowid
        return jsonify({"food_log_id": food_log_id}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()

#Route to add a new food item to the database
@client.route('/insert/insert_food_item/<meal_name>/<calories>/<protein>/<carbs>/<fats>/', methods=["POST"])
def insert_food_item(meal_name, calories, protein, carbs, fats):
    query = f"""
        INSERT INTO FoodItem(name, calories, protein, carbs, fats)
        VALUES('{meal_name}', {calories}, {protein}, {carbs}, {fats})
    """
    conn = db.get_db()
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        conn.commit()
        # return the new ID back as JSON
        return jsonify({"food_item_id": cursor.lastrowid}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()

#Route to add a new food item to a specific food log
@client.route('/insert/insert_food_item_to_food_log/<food_log_id>/<food_item_id>/<servings>/', methods=["POST"])
def insert_food_item_to_food_log(food_log_id, food_item_id, servings):
    query = f'''    
        INSERT INTO FoodLog_FoodItem(food_log_id, food_item_id, servings)
            VALUES({food_log_id}, {food_item_id}, {servings});
    '''
    
    connection = db.get_db()
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        response = make_response(jsonify({"status": "success", "message": "FoodLog_FoodItem inserted successfully."}))
        response.status_code = 200
    except Exception as e:
        connection.rollback()
        response = make_response(jsonify({"error": str(e)}))
        response.status_code = 400
    finally:
        cursor.close()
    return response 

#Route to log the completion of a circuit workout session
@client.route('/insert/workout_log/<user_id>/<circuit_id>/', methods=["POST"])
def insert_workout_log(user_id, circuit_id):
    query = """
        INSERT INTO WorkoutLog (user_id, circuit_id, datetime_logged, duration, description, calories_burned)
            VALUES (%s, %s, NOW(), NULL, '', NULL)
    """
    conn = db.get_db()
    cursor = conn.cursor()
    try:
        cursor.execute(query, (user_id, circuit_id))
        conn.commit()
        return jsonify({"status": "success", "workoutlog_id": cursor.lastrowid}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"status": "error", "message": str(e)}), 400
    finally:
        cursor.close()