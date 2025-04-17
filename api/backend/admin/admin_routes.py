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

    # ------------------------------------------------------------

@admin.route('/users/<int:user_id>', methods=['GET'])
def get_user_profile(user_id):
    try:
        cursor = db.get_db().cursor()
        query = '''
            SELECT user_id, first_name, last_name, email, gender,
                   height_ft, height_in, weight, date_of_birth, role
            FROM User
            WHERE user_id = %s
        '''

        cursor.execute(query, (user_id,))
        row = cursor.fetchone()

        if row is None:
            return jsonify({"error": "User not found"}), 404
        return jsonify(row), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

   # ------------------------------------------------------------

@admin.route('/users/search', methods=['GET'])
def search_users_by_last_name():
    try:
        last_name = request.args.get('last_name')
        if not last_name:
            return jsonify({"error": "Missing 'last_name' parameter"}), 400

        cursor = db.get_db().cursor()
        query = '''
               SELECT user_id, first_name, last_name, email, gender,
                      height_ft, height_in, weight, date_of_birth, role
               FROM User
               WHERE last_name LIKE %s
           '''
        cursor.execute(query, (f"%{last_name}%",))
        users = cursor.fetchall()

        if not users:
            return jsonify([]), 200
        return jsonify(users), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ------------------------------------------------------------

@admin.route('/users/<int:user_id>', methods=['PUT'])
def update_user_profile(user_id):
    try:
        data = request.json

        query = f"""
            UPDATE User
            SET first_name='{data["first_name"]}', 
                last_name='{data["last_name"]}', 
                email='{data["email"]}', 
                gender='{data["gender"]}',
                height_ft='{data["height_ft"]}', 
                height_in='{data["height_in"]}', 
                weight='{data["weight"]}', 
                date_of_birth='{data["date_of_birth"]}',
                role='{data["role"]}'
            WHERE user_id={user_id}
        """

        cursor = db.get_db().cursor()
        cursor.execute(query)
        db.get_db().commit()
        return jsonify({"message": "User profile updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ------------------------------------------------------------

@admin.route("/maintenance", methods=["GET"])
def get_maintenance_status():
    try:
        cursor = db.get_db().cursor()
        cursor.execute("SELECT setting_value "
                       "FROM App_State "
                       "WHERE setting_key = 'maintenance_mode'")
        result = cursor.fetchone()
        if result and "setting_value" in result:
            is_on = result["setting_value"] == "on"
        return jsonify({"maintenance_mode": is_on}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ------------------------------------------------------------

@admin.route("/maintenance", methods=["PUT"])
def update_maintenance_status():
    try:
        data = request.get_json()
        new_value = data.get("maintenance_mode")

        if new_value:
            value_str = "on"
        else:
            value_str = "off"

        cursor = db.get_db().cursor()
        cursor.execute(
            "UPDATE App_State "
            "SET setting_value = %s "
            "WHERE setting_key = 'maintenance_mode'", (value_str,)
        )
        db.get_db().commit()

        return jsonify({"message": f"Maintenance mode set to {value_str}"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ------------------------------------------------------------

@admin.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute("DELETE FROM User WHERE user_id = %s", (user_id,))
        db.get_db().commit()

        return jsonify({"message": f"User {user_id} deleted successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ------------------------------------------------------------

@admin.route('/support/<int:ticket_id>', methods=['PUT'])
def resolve_support_ticket(ticket_id):
    try:
        data = request.json
        admin_id = data.get("admin_id")

        if not admin_id:
            return jsonify({"error": "Missing admin_id"}), 400

        cursor = db.get_db().cursor()

        cursor.execute(
            "SELECT status "
            "FROM Support_Tickets "
            "WHERE support_ticket_id = %s", (ticket_id,)
        )
        ticket = cursor.fetchone()

        if not ticket:
            return jsonify({"error": "Ticket not found"}), 404
        if ticket["status"].lower() == "closed":
            return jsonify({"message": "Ticket is already closed"}), 409

        query = f"""
            UPDATE Support_Tickets
            SET status='closed',
                date_resolved=NOW(),
                resolved_by_admin={admin_id}
            WHERE support_ticket_id={ticket_id}
        """
        cursor.execute(query)
        db.get_db().commit()

        return jsonify({"message": "Ticket resolved successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
