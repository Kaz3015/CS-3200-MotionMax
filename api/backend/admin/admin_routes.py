from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of
# routes.
admin = Blueprint('admin', __name__)

#------------------------------------------------------------
# Post the user survey which gets their demographics

@admin.route('/support', methods=['POST'])
def post_support_ticket():
    try:
        data = request.json

        #extracting the variable
        user_id = data['user_id']
        description = data['description']

        query = f'''
             INSERT INTO Support_Tickets (status, date_created, description, created_by_user)
             VALUES ('open', NOW(), '{description}', {user_id})
            '''

        # get a cursor object from the database
        cursor = db.get_db().cursor()

        # use cursor to query the database for a list of products
        cursor.execute(query)
        db.get_db().commit()

        response = make_response("Support ticket submitted successfully!")
        response.status_code = 200
        return response


    except Exception as e:
        response = make_response(f"Error: {str(e)}")
        response.status_code = 500
        return response

#------------------------------------------------------------

@admin.route('/support', methods=['GET'])
def get_all_support_tickets():
    try:
        cursor = db.get_db().cursor()
        query = '''
            SELECT support_ticket_id, status, date_created, date_resolved, description, created_by_user, resolved_by_admin
            FROM Support_Tickets
            ORDER BY date_created DESC
        '''
        cursor.execute(query)
        tickets = cursor.fetchall()
        return jsonify(tickets), 200
    except Exception as e:
        return {"error": str(e)}, 500