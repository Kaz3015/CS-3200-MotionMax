########################################################
# Sample customers blueprint of endpoints
# Remove this file if you are not using it in your project
########################################################

from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of 
# routes.
trainer = Blueprint('trainer', __name__)

#------------------------------------------------------------
# Get all the products from the database, package them up,
# and return them to the client
@trainer.route('/', methods=['GET'])
def get_trainer_id():
    query = '''
        SELECT  u.user_id, s.subscriber_id
        FROM User u
        JOIN Subscription s ON s.creator_id = u.user_id
        WHERE u.first_name = 'John' AND u.last_name = 'Smith' AND u.role = 'trainer'
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

# ------------------------------------------------------------
# get product information about a specific product
# notice that the route takes <id> and then you see id
# as a parameter to the function.  This is one way to send 
# parameterized information into the route handler.
@trainer.route('/workouts/<creator_id>/<subscriber_id>', methods=['GET'])
def get_workouts (creator_id, subscriber_id):

    query = f'''
    SELECT u.first_name, u.last_name, cir.name, cir.circuit_type, cir.difficulty, wl.created_at
FROM WorkoutLog wl
JOIN Circuit cir ON cir.circuit_id = wl.circuit_id
JOIN User u ON wl.user_id = u.user_id
JOIN Subscription s ON s.subscriber_id = u.user_id
WHERE s.creator_id = {creator_id} AND s.subscriber_id = {subscriber_id}
  AND DATE(wl.created_at) = DATE(CURDATE())
ORDER BY u.last_name DESC;
    '''
    
    # logging the query for debugging purposes.  
    # The output will appear in the Docker logs output
    # This line has nothing to do with actually executing the query...
    # It is only for debugging purposes. 
    current_app.logger.info(f'GET /workouts/<creator_id>\<subscriber_id> query={query}')

    # get the database connection, execute the query, and 
    # fetch the results as a Python Dictionary
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    
    # Another example of logging for debugging purposes.
    # You can see if the data you're getting back is what you expect. 
    current_app.logger.info(f'GET /workouts/<creator_id>\<subscriber_id> Result of query = {theData}')
    
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response
    
# ------------------------------------------------------------
# Get the top 5 most expensive products from the database
@trainer.route('/<creator_id>/getClients')
def get_clients(creator_id):

    query = f'''
        SELECT u.first_name, u.last_name s.subscriber_id
FROM Subscription as s
JOIN User u ON s.subscriber_id = u.user_id
WHERE s.creator_id = {creator_id} AND MONTH(s.created_at) = MONTH(CURRENT_DATE);
        '''
    
    # Same process as handler above
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
 
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

# ------------------------------------------------------------
# Route to get the 10 most expensive items from the 
# database.
@trainer.route('/<creator_id>/messageBoard', methods=['GET'])
def get_trainer_messages(creator_id):
    
    query = f'''
        SELECT DISTINCT m.content, sender.first_Name, sender.last_name, m.created_at, sender.user_id
FROM Message m
JOIN User sender ON m.sender_id = sender.user_id
JOIN Subscription s ON m.receiver_id = s.creator_id
WHERE s.creator_id = {creator_id} and WEEK(Date(m.created_at)) >= WEEK(DATE_SUB(NOW(), INTERVAL 1 WEEK))
ORDER BY m.created_at;
    '''
    
    # Same process as above
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response
    

# ------------------------------------------------------------
# This is a POST route to add a new product.
# Remember, we are using POST routes to create new entries
# in the database. 
@trainer.route('/<creator_id>/<subscriber_id>/macros', methods=['Get'])
def get_client_macros(creator_id, subscriber_id):

    
    query = f'''
        SELECT s.subscriber_id, u.first_name, u.last_name, SUM(fi.calories * fli.servings) AS total_calories,
       SUM(fi.protein * fli.servings) AS total_protein, SUM(fi.carbs * fli.servings) AS total_carbs,
       SUM(fi.fats * fli.servings) AS total_fat, CURDATE() AS today
FROM Subscription s
JOIN FoodLog fl ON s.subscriber_id = fl.user_id
JOIN FoodLog_FoodItem fli ON fl.food_log_id = fli.food_log_id
JOIN FoodItem fi ON fli.food_item_id = fi.food_item_id
JOIN User u ON u.user_id = s.subscriber_id
WHERE s.creator_id = :creator_id AND DATE(fi.created_at) = DATE(CURDATE())
  AND s.subscriber_id = :subscriber_id
GROUP BY s.subscriber_id, u.first_name, u.last_name;
    '''

    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    response = make_response("Successfully added product")
    response.status_code = 200
    return response

# ------------------------------------------------------------
### Get all product categories
@trainer.route('/<trainer_id>/workouts', methods = ['GET'])
def get_workout():
    query = '''
       SELECT wt.w_id, wt.title, wt.description, et.et_id, emd.title AS exercise_title,
       emd.description AS exercise_description, et.rep_low, et.rep_high, et.sets, wet.sequence
FROM  Trainer_Meta_Data tmd
JOIN User u ON tmd.train_id = u.user_id
JOIN Workout_Template wt ON u.user_id = wt.user_id
JOIN Workout_Exercise_Template wet ON wt.w_id = wet.w_id
JOIN Exercise_Template et ON wet.et_id = et.et_id
JOIN Exercise_Template_Meta_Data etmd ON et.et_id = etmd.et_id
JOIN Exercise_Meta_Data emd ON etmd.emd_id = emd.emd_id
WHERE tmd.train_id = :train_id
ORDER BY wt.w_id, wet.sequence;
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
        
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

# ------------------------------------------------------------
# This is a stubbed route to update a product in the catalog
# The SQL query would be an UPDATE. 
@trainer.route('/<trainer_id>/recipes', methods = ['GET'])
def get_recipes():
    query = '''
           SELECT r.r_id, r.title AS recipe_title, r.description AS recipe_description, r.calories,
r.protein, r.carbs, r.fat, i.title AS ingredient_name, ri.amount, ri.measurement, r_id
FROM Trainer_Meta_Data tmd
JOIN User u ON tmd.train_id = u.user_id
JOIN Recipe r ON u.user_id = r.user_id
LEFT JOIN RecipeIngredient ri ON r.r_id = ri.r_id
LEFT JOIN Ingredients i ON ri.ing_id = i.ing_id
WHERE tmd.train_id = :train_id
ORDER BY r.r_id, i.title;
        '''

    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response