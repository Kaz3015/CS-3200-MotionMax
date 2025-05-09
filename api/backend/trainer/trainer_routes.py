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
import logging

# ------------------------------------------------------------
# Create a new Blueprint object, which is a collection of
# routes.
trainer = Blueprint('trainer', __name__)


@trainer.route('/', methods=['GET'])
# ------------------------------------------------------------
# Get user personas id
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


@trainer.route('/workouts/<creator_id>/<subscriber_id>', methods=['GET'])
# ------------------------------------------------------------
# Get the workouts for a specific subscriber
def get_workouts(creator_id, subscriber_id):
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
# Gets all the specified trainers clients
@trainer.route('/<creator_id>/getClients')
def get_clients(creator_id):
    query = f'''
        SELECT u.first_name, u.last_name, s.subscriber_id
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
# Route to get the messages for a specific trainer
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
# This is a get route to get users macros
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
WHERE s.creator_id = {creator_id} AND DATE(fi.created_at) = DATE(CURDATE())
  AND s.subscriber_id = {subscriber_id}
GROUP BY s.subscriber_id, u.first_name, u.last_name;
    '''

    current_app.logger.info(query)

    # executing and committing the insert statement
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response


# ------------------------------------------------------------
### Gets all the workouts for a specific trainer
@trainer.route('/<trainer_id>/workouts', methods=['GET'])
def get_workout(trainer_id):
    query = f'''
       SELECT wt.w_id, wt.title, wt.description, et.et_id, emd.emd_id, emd.title AS exercise_title,
       emd.description AS exercise_description, et.rep_low, et.rep_high, et.sets, wet.sequence
FROM  Trainer_Meta_Data tmd
JOIN User u ON tmd.train_id = u.user_id
JOIN Workout_Template wt ON u.user_id = wt.user_id
JOIN Workout_Exercise_Template wet ON wt.w_id = wet.w_id
JOIN Exercise_Template et ON wet.et_id = et.et_id
JOIN Exercise_Template_Meta_Data etmd ON et.et_id = etmd.et_id
JOIN Exercise_Meta_Data emd ON etmd.emd_id = emd.emd_id
WHERE tmd.train_id = {trainer_id}
ORDER BY wt.w_id, wet.sequence;
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

log = logging.getLogger(__name__)
#Gets the name of the workouts for a specific trainer
@trainer.route('/<trainer_id>/workoutNames', methods=['GET'])
def get_workout_names(trainer_id):
    query = f'''
       SELECT wt.w_id, wt.title
       FROM Workout_Template wt
       WHERE wt.user_id = {trainer_id};
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

#Insert and update for work outs to updated exercises and the workout
@trainer.route("/<int:trainer_id>/addWorkout", methods=["POST"])
def create_workout(trainer_id: int):
    """Create a brand‑new workout with its exercises; no update logic."""
    data  = request.get_json(force=True)
    conn  = db.get_db()
    cur   = conn.cursor()

    try:
        # 1. Workout_Template
        cur.execute(
            "INSERT INTO Workout_Template (user_id, title, description) "
            "VALUES (%s, %s, %s)",
            (data["user_id"], data["title"], data.get("description")),
        )
        w_id = cur.lastrowid
        log.info("New workout w_id=%s created", w_id)

        # 2. Loop over exercises
        for ex in data["exercises"]:
            cur.execute(
                "INSERT INTO Exercise_Template (rep_low, rep_high, sets) "
                "VALUES (%s, %s, %s)",
                (ex["rep_low"], ex["rep_high"], ex["sets"]),
            )
            et_id = cur.lastrowid

            cur.execute(
                "INSERT INTO Workout_Exercise_Template (w_id, et_id, sequence) "
                "VALUES (%s, %s, %s)",
                (w_id, et_id, ex["sequence"]),
            )

            cur.execute(
                "INSERT INTO Exercise_Meta_Data (title, description) "
                "VALUES (%s, %s)",
                (ex["title"], ex.get("description", "")),
            )
            emd_id = cur.lastrowid

            cur.execute(
                "INSERT INTO Exercise_Template_Meta_Data (et_id, emd_id) "
                "VALUES (%s, %s)",
                (et_id, emd_id),
            )

        conn.commit()
        return jsonify({"status": "success", "w_id": w_id}), 201

    except Exception as err:
        conn.rollback()
        log.exception("Unexpected error while creating workout")
        return jsonify({"status": "error", "message": str(err)}), 500
    finally:
        cur.close()


# ------------------------------------------------------------
# Gets all the recipes for a specific trainer
@trainer.route('/<trainer_id>/recipes', methods=['GET'])
def get_recipes(trainer_id):
    query = f'''
           SELECT r.r_id, r.title AS recipe_title, r.description AS recipe_description, r.calories,
r.protein, r.carbs, r.fat, i.title AS ingredient_name, ri.amount, ri.measurement, i.ing_id
FROM Trainer_Meta_Data tmd
JOIN User u ON tmd.train_id = u.user_id
JOIN Recipe r ON u.user_id = r.user_id
LEFT JOIN RecipeIngredient ri ON r.r_id = ri.r_id
LEFT JOIN Ingredients i ON ri.ing_id = i.ing_id
WHERE tmd.train_id = {trainer_id}
ORDER BY r.r_id, i.title;
        '''

    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

#Gets all ingredients for a specific trainer
@trainer.route('/<trainer_id>/ingredients', methods=['GET'])
def get_ingredients(trainer_id):
    query = f'''
    SELECT DISTINCT i.ing_id, i.title AS ingredient_name
    FROM Ingredients i
    JOIN RecipeIngredient ri ON i.ing_id = ri.ing_id
    JOIN Recipe r ON ri.r_id = r.r_id
    JOIN User u ON r.user_id = u.user_id
    WHERE u.user_id = {trainer_id}
    ORDER BY i.title;
        '''

    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

#Adds and updates a recipes from the ingredient table and the recipe table
@trainer.route('/<trainer_id>/addRecipe', methods=['POST', 'PUT'])
def add_recipe(trainer_id):
    the_data = request.json
    current_app.logger.info(the_data)
    current_app.logger.setLevel('DEBUG')

    # Extracting the variable
    title = the_data['recipe_name']
    description = the_data['recipe_description']
    calories = the_data['calories']
    protein = the_data['protein']
    carbs = the_data['carbs']
    fat = the_data['fat']
    ingredients = the_data['ingredients']
    recipe_id = the_data['recipe_id']
    cursor = db.get_db().cursor()
    if request.method == 'POST':
        query = f'''
            INSERT INTO Recipe (title, description, calories, protein, carbs, fat, user_id)
            VALUES ('{title}', '{description}', {calories}, {protein}, {carbs}, {fat}, {trainer_id})
        '''
        cursor = db.get_db().cursor()
        cursor.execute(query)
        db.get_db().commit()
        recipe_id = cursor.lastrowid
        # Insert ingredients into the Ingredients table
        for name, info in ingredients.items():
            # Check if the ingredient doesn't exist
            if len(info) == 2:
                ingredient_name = name
                amount, measurement = info[0], info[1]
                query = f'''
                INSERT INTO Ingredients (title)
                VALUES ('{ingredient_name}')
                '''
                cursor.execute(query)
                db.get_db().commit()
                ingredient_id = cursor.lastrowid
                query = f'''
                            INSERT INTO RecipeIngredient (r_id, ing_id, amount, measurement)
                            VALUES ({recipe_id}, {ingredient_id}, {amount}, '{measurement}')
                        '''
                cursor.execute(query)
                db.get_db().commit()
            elif len(info) == 3:
                # If the ingredient exists, use its ID
                ingredient_id = info[0]
                amount, measurement = info[1], info[2]
                query = f'''
                            INSERT INTO RecipeIngredient (r_id, ing_id, amount, measurement)
                            VALUES ({recipe_id}, {ingredient_id}, {amount}, '{measurement}')
                        '''
                cursor.execute(query)
                db.get_db().commit()
    elif request.method == 'PUT':
        # Update the recipe in the Recipe table
        query = f'''UPDATE Recipe
                    SET title = '{title}', description = '{description}', calories = {calories},
                    protein = {protein}, carbs = {carbs}, fat = {fat}
                    WHERE r_id = {recipe_id};
                '''
        cursor.execute(query)
        db.get_db().commit()
        query = f''' SELECT ri.ing_id, ri.r_id, i.title
        FROM RecipeIngredient ri
        JOIN Ingredients i ON ri.ing_id = i.ing_id
        WHERE ri.r_id = {recipe_id};
        '''
        cursor.execute(query)
        theData = cursor.fetchall()
        current_app.logger.info(f"Data from put {theData}")
        print(f"Data from put {theData}")
        current_app.logger.info(f"Ingredient data {ingredients.values()}")
        print(f"Ingredient data {ingredients.values()}")
        ids = [data[0] for data in ingredients.values()]
        current_app.logger.info(f"Ids {ids}")
        # checks if the ingredient is in the ingredients table to decide to update or insert
        for data in theData:
            ingredient_id = data['ing_id']
            current_app.logger.info(f"Ingredient id {ingredient_id}")
            recipe_id = data['r_id']
            if ingredient_id in ids:
                name = data['title']
                amount, measurement = ingredients[name][1], ingredients[name][2]
                current_app.logger.info(f"Updating Ingredient {name} with {amount} {measurement}")
                query = f'''
                    UPDATE RecipeIngredient
                    SET amount = {amount}, measurement = '{measurement}'
                    WHERE r_id = {recipe_id} AND ing_id = {ingredient_id};
                '''
                cursor.execute(query)
                db.get_db().commit()
                current_app.logger.info(f"Deleting Ingredient {ingredients.pop(name)}")
                deleted = ingredients.pop(name, 'couldnt find')
                print(f"Deleting Ingredient {deleted}")
            else:
                current_app.logger.info(f"Deleting Ingredient {data}")
                query = f'''
                    DELETE FROM RecipeIngredient
                    WHERE r_id = {recipe_id} AND ing_id = {ingredient_id};
                '''
                cursor.execute(query)
                db.get_db().commit()
        # Insert new ingredients into the RecipeIngredient table
        for name, info in ingredients.items():
            if len(info) == 2:
                ingredient_name = name
                amount, measurement = info[0], info[1]
                query = f'''
                    INSERT INTO Ingredients (title)
                    VALUES ('{ingredient_name}')
                '''
                cursor.execute(query)
                db.get_db().commit()
                ingredient_id = cursor.lastrowid
                query = f'''
                    INSERT INTO RecipeIngredient (r_id, ing_id, amount, measurement)
                    VALUES ({recipe_id}, {ingredient_id}, {amount}, '{measurement}')
                '''
                cursor.execute(query)
                db.get_db().commit()
            elif len(info) == 3:
                ingredient_id = info[0]
                amount, measurement = info[1], info[2]
                query = f'''
                    INSERT INTO RecipeIngredient (r_id, ing_id, amount, measurement)
                    VALUES ({recipe_id}, {ingredient_id}, {amount}, '{measurement}')
                '''
                cursor.execute(query)
                db.get_db().commit()

    response = make_response("Successfully added recipe")
    response.status_code = 200
    return response

# ------------------------------------------------------------
# Gets a specific recipe for a specific trainer
@trainer.route('/<trainer_id>/<recipe_id>/recipe', methods=['GET'])
def get_recipe(trainer_id, recipe_id):
    query = f'''
        SELECT r.r_id, r.title AS recipe_title, r.description AS recipe_description, r.calories,
r.protein, r.carbs, r.fat, i.title AS ingredient_name, ri.amount, ri.measurement, i.ing_id
FROM Recipe r
JOIN RecipeIngredient ri ON r.r_id = ri.r_id
JOIN Ingredients i ON ri.ing_id = i.ing_id
WHERE r.r_id = {recipe_id} AND r.user_id = {trainer_id}
ORDER BY i.title;
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

# ------------------------------------------------------------
# Deletes a specific recipe for a specific trainer
@trainer.route('/<trainer_id>/<recipe_id>/deleteRecipe', methods=['DELETE'])
def delete_recipe(trainer_id, recipe_id):
    query = f'''
        DELETE FROM Recipe WHERE r_id = {recipe_id} AND user_id = {trainer_id};
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    response = make_response("Successfully deleted recipe")
    response.status_code = 200
    return response

# ------------------------------------------------------------
# Deletes a specific workout for a specific trainer
@trainer.route('/<trainer_id>/<workout_id>/deleteWorkout', methods=['DELETE'])
def delete_workout(trainer_id, workout_id):
    query = f'''
        DELETE FROM Workout_Template WHERE w_id = {workout_id} AND user_id = {trainer_id};
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    response = make_response("Successfully deleted workout")
    response.status_code = 200
    return response

# ------------------------------------------------------------
# Gets the financials for a specific trainer
@trainer.route('/<trainer_id>/financials', methods=['GET'])
# ------------------------------------------------------------
# Get the financials for a trainer
def get_financials(trainer_id):
    query = f'''
    SELECT 
    YEAR(s.created_at) AS year,
    MONTH(s.created_at) AS month,
    COUNT(s.subscriber_id) * tmd.subscription_price * .6 AS total_revenue
FROM Subscription s
JOIN Trainer_Meta_Data tmd ON s.creator_id = tmd.train_id
Where s.creator_id = {trainer_id}
GROUP BY YEAR(s.created_at), MONTH(s.created_at)
ORDER BY year, month;
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

# ------------------------------------------------------------
# Sends the messages from subscribers or trainer to the trainer
@trainer.route('/<trainer_id>/messageBoard/<subscriber_id>', methods=['POST'])
# ------------------------------------------------------------
# Send a message to a subscriber or trainer
def send_message(trainer_id, subscriber_id):
    the_data = request.json
    current_app.logger.info(the_data)
    current_app.logger.setLevel('DEBUG')

    # Extracting the variable
    content = the_data['content']
    cursor = db.get_db().cursor()
    query = f'''
        INSERT INTO Message (content, sender_id, receiver_id)
        VALUES ('{content}', {trainer_id}, {subscriber_id})
    '''
    cursor.execute(query)
    db.get_db().commit()

    response = make_response("Successfully sent message")
    response.status_code = 200
    return response
