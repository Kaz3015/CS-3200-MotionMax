import streamlit as st
import requests
import pandas as pd

st.set_page_config(layout="wide")
st.title("Admin: Search User Profiles")
search_mode = st.selectbox("Search By", ["User ID", "Last Name"])

columns = [
    "user_id", "first_name", "last_name", "email", "gender",
    "height_ft", "height_in", "weight", "date_of_birth", "role"
]

if search_mode == "User ID":
    user_id = st.number_input("Enter User ID to Search", min_value=1, step=1)
    if st.button("Search", use_container_width=True, type="primary"):
        try:
            url = f"http://web-api:4000/a/users/{user_id}"
            response = requests.get(url)
            if response.status_code == 200:
                user = response.json()
                st.success("User profile found")
                st.dataframe(pd.DataFrame([user], columns=columns))
            elif response.status_code == 404:
                st.warning("User not found.")
            else:
                st.error(f"Unexpected error: {response.text}")
        except Exception as e:
            st.error(f"Connection error: {e}")
elif search_mode == "Last Name":
    last_name = st.text_input("Enter Last Name")
    if st.button("Search", use_container_width=True, type="primary"):
        if last_name:
            url = f"http://web-api:4000/a/users/search?last_name={last_name}"
            response = requests.get(url)
            if response.status_code == 200:
                users = response.json()
                if users:
                    st.success(f"Found {len(users)} user(s)")
                    df = pd.DataFrame(users)
                    st.dataframe(df[columns])
                else:
                    st.info("No users found with that last name.")
            else:
                st.error(f"Unexpected error: {response.text}")