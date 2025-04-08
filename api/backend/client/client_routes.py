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

