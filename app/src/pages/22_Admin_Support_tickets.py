import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")
st.title("Submit a Support Ticket")
SideBarLinks()

with st.form("support_form"):
    user_id = st.number_input("User ID", min_value=1, step=1)
    description = st.text_area("Describe the issue you're experiencing")

    submitted = st.form_submit_button("Submit Ticket")

    if submitted:
        if user_id and description:
            data = {
                "user_id": user_id,
                "description": description
            }

            # url = "http://localhost:4001/a/support"
            url = "http://web-api:4000/a/support"

            try:
                response = requests.post(url, json=data)
                if response.status_code == 200:
                    st.success("Support ticket submitted!")
                else:
                    st.error(f"Error: {response.text}")
            except Exception as e:
                st.error(f"Failed to connect: {e}")
        else:
            st.warning("Please fill in all fields.")
