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
# get the sales persona user_id
@sales.route('/', methods=['GET'])
def get_sales_id():
    query = '''
    SELECT u.user_id
    FROM User u
    WHERE u.first_name = 'Tyler' AND u.last_name = 'Davis' AND u.role = 'salesperson'
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    # set the proper HTTP Status code of 200 (meaning all good)
    response.status_code = 200
    # send the response back to the client
    return response

#Adds the user_survey asking demographic information about the users of the app
@sales.route('/user_survey', methods=['POST'])
def post_sale_survey():
    data = request.json

    #extracting the variable
    user_id = data['user_id']
    age = data['age']
    gender = data['gender']
    ethnicity = data['ethnicity']
    fitness_experience = data['fitness_experience']

    query = f'''
        INSERT INTO Demographics (user_id, age, gender, cultural_background, fitness_experience)
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
        INSERT INTO Feedback (user_id, app_discovery, app_enjoyment, improvement_suggestions, similar_apps,
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

#------------------------------------------------------------
# Get Customer Aquisition cost of the users
@sales.route('/CA_cost', methods=['GET'])
def get_customer_aquisition_cost():
    query = """
        SELECT
            DATE_FORMAT(m.date, '%b %Y') AS month,
            SUM(m.budget) AS budget,
            SUM(DISTINCT s.new_subscribers) AS customers,
            SUM(m.budget) / NULLIF(SUM(s.new_subscribers), 0) AS cost
        FROM Sales_Report s
        JOIN Marketing_Channels m ON m.user_id = s.user_id
        GROUP BY month
        ORDER BY MIN(m.date)
        """

    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of products
    cursor.execute(query)

    # fetch all the data from the cursor
    # The cursor will return the data as a
    # Python Dictionary
    theData = cursor.fetchall()

    # Create a HTTP Response object and add results of the query to it
    # after "jasonify"-ing it.
    response = make_response(jsonify(theData))
    # set the proper HTTP Status code of 200 (meaning all good)
    response.status_code = 200
    # send the response back to the client
    return response

#------------------------------------------------------------
#this gets the output that user inputted about their demographics and displays it to the sales admin
@sales.route('/user_survey_output', methods=['GET'])
def get_user_survey_output():
    query = """
        SELECT u.age, u.gender, u.cultural_background, 
               u.fitness_experience, COUNT(*) AS engagement_count
        FROM Demographics u
        JOIN WorkoutLog wl ON u.user_id = wl.user_id
        GROUP BY u.age, u.gender, u.cultural_background, u.fitness_experience
        ORDER BY engagement_count DESC;
        """

    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of products
    cursor.execute(query)

    # fetch all the data from the cursor
    # The cursor will return the data as a
    # Python Dictionary
    theData = cursor.fetchall()

    # Create a HTTP Response object and add results of the query to it
    # after "jasonify"-ing it.
    response = make_response(jsonify(theData))
    # set the proper HTTP Status code of 200 (meaning all good)
    response.status_code = 200
    # send the response back to the client
    return response

#------------------------------------------------------------
#this gets the output that user inputted about their feedback on the app and displays it to the sales admin
@sales.route('/feedback_survey_output', methods=['GET'])
def get_feedback_survey_output(rows=None):
    query = """
        SELECT 
            f.user_id,
            f.app_discovery,
            f.app_enjoyment,
            f.improvement_suggestions,
            f.similar_apps,
            f.most_useful_feature
        FROM Feedback f
        JOIN User_Feedback uf ON f.feedback_id = uf.feedback_id
        """

    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of products
    cursor.execute(query)

    # fetch all the data from the cursor
    # The cursor will return the data as a
    # Python Dictionary
    theData = cursor.fetchall()

    # Create a HTTP Response object and add results of the query to it
    # after "jasonify"-ing it.
    response = make_response(jsonify(theData))
    # set the proper HTTP Status code of 200 (meaning all good)
    response.status_code = 200
    # send the response back to the client
    return response

#------------------------------------------------------------
#this gets the count of the subscribers that we have in a certain month
@sales.route('/subscriber_count', methods=['GET'])
def get_subscriber_count():
    query = """
    SELECT MONTH(created_at) AS month, COUNT(*) AS subscriber_count
FROM Subscription
GROUP BY month
ORDER BY month;
    """

    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of products
    cursor.execute(query)

    # fetch all the data from the cursor
    # The cursor will return the data as a
    # Python Dictionary
    theData = cursor.fetchall()

    # Create a HTTP Response object and add results of the query to it
    # after "jasonify"-ing it.
    response = make_response(jsonify(theData))
    # set the proper HTTP Status code of 200 (meaning all good)
    response.status_code = 200
    # send the response back to the client
    return response

#------------------------------------------------------------
#this gets the revenue we have gotten from the application
@sales.route('/revenue', methods=['GET'])
def get_revenue():
    query = """
    SELECT SUM(trainer_revenue) AS motion_max_revenue, month
    FROM (
        SELECT COUNT(s.subscriber_id) * t.subscription_price * 0.4 AS trainer_revenue, MONTH(s.created_at) AS month
        FROM Subscription s
        JOIN Trainer_Meta_Data t ON t.train_id = s.creator_id
        GROUP BY t.train_id, MONTH(s.created_at)
     ) AS revenue
    GROUP BY month;
    """

    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of products
    cursor.execute(query)

    # fetch all the data from the cursor
    # The cursor will return the data as a
    # Python Dictionary
    theData = cursor.fetchall()

    # Create a HTTP Response object and add results of the query to it
    # after "jasonify"-ing it.
    response = make_response(jsonify(theData))
    # set the proper HTTP Status code of 200 (meaning all good)
    response.status_code = 200
    # send the response back to the client
    return response
