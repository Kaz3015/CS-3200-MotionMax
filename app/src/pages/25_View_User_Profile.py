import streamlit as st
import requests
import pandas as pd

st.set_page_config(layout="wide")
st.title("Admin: Search and Edit User Profile")
search_mode = st.selectbox("Search By", ["User ID", "Last Name"])

# Shared column order
columns = [
    "user_id", "first_name", "last_name", "email", "gender",
    "height_ft", "height_in", "weight", "date_of_birth", "role"
]


selected_user = None

# Search by ID
if search_mode == "User ID":
    user_id = st.number_input("Enter User ID", min_value=1, step=1)
    if st.button("Search", use_container_width=True, type="primary"):
        url = f"http://web-api:4000/a/users/{user_id}"
        response = requests.get(url)
        if response.status_code == 200:
            st.session_state['search'] = True
            user = response.json()
            st.session_state['selected_user'] = user
            st.success("User profile found")
            st.dataframe(pd.DataFrame([user])[columns])
            selected_user = user
        elif response.status_code == 404:
            st.warning("User not found.")
        else:
            st.error(f"Unexpected error: {response.text}")

# Search by last name
else:
    last_name = st.text_input("Enter Last Name")
    if st.button("Search", use_container_width=True, type="primary"):
        if last_name:
            url = f"http://web-api:4000/a/users/search?last_name={last_name}"
            response = requests.get(url)
            if response.status_code == 200:
                users = response.json()
                if users:
                    st.success(f"Found {len(users)} user(s)")
                    user_options = [f"{u['first_name']} {u['last_name']} (ID: {u['user_id']})" for u in users]
                    selection = st.selectbox("Select a user to edit", user_options)
                    st.session_state['selected_user'] = users[user_options.index(selection)]
                    st.dataframe(pd.DataFrame([selected_user])[columns])
                else:
                    st.info("No users found with that last name.")
            else:
                st.error(f"Unexpected error: {response.text}")

# Show edit form if a user is selected
if selected_user or st.session_state['search']:
    st.subheader("Edit User Profile")
    selected_user = st.session_state['selected_user']

    # Name and email
    first_name = st.text_input("First Name", selected_user["first_name"])
    last_name = st.text_input("Last Name", selected_user["last_name"])
    email = st.text_input("Email", selected_user["email"])

    #Gender stuff
    gender_options = ["Male", "Female", "Other"]
    gender = st.selectbox("Gender", gender_options, index=gender_options.index(selected_user["gender"].capitalize()))

    # Height and Weight
    height_ft = st.number_input("Height (ft)", min_value=0.0, max_value=8.0, value=float(selected_user["height_ft"]))
    height_in = st.number_input("Height (in)", min_value=0.0, max_value=11.0, value=float(selected_user["height_in"]))
    weight = st.number_input("Weight (lbs)", min_value=0.0, value=float(selected_user["weight"]))

    # DOB
    dob = st.date_input("Date of Birth", pd.to_datetime(selected_user["date_of_birth"]))

    # Role stuff
    role_options = ["client", "trainer", "admin"]
    role = st.selectbox("Role", role_options, index=role_options.index(selected_user["role"].lower()))

    if st.button("Save Changes", type="primary", use_container_width=True):
        payload = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "gender": gender,
            "height_ft": height_ft,
            "height_in": height_in,
            "weight": weight,
            "date_of_birth": dob.strftime("%Y-%m-%d"),
            "role": role
        }

        url = f"http://web-api:4000/a/users/{selected_user['user_id']}"
        response = requests.put(url, json=payload)

        if response.status_code == 200:
            st.success("User profile updated successfully!")
        else:
            st.error(f"Update failed: {response.text}")
