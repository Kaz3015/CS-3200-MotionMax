import requests
import streamlit as st

with st.form("MotionMAX Survey"):
    st.session_state["change age"] = False
    st.caption("User Demographics")
    age = st.slider("How old are you?")
    ethnicity = st.multiselect("What is your cultural background?", ["Caucasian", "Hispanic",
                               "African American", "Native American", "Asian", "Middle Eastern"])
    gender = st.selectbox("What is your gender?", ["Male", "Female"],
                          index = None)
    fitness_experience = st.selectbox("What is your fitness experience", ["Beginner", "Intermediate", "Advanced"],
                                      index = None)
    if st.form_submit_button("Submit"):
        if age != 0 and ethnicity is not None and gender is not None and fitness_experience is not None:
            ethnicity = ",".join(ethnicity)
            data = {
                "user_id": st.session_state["user_id"],
                "age": age,
                "ethnicity": ethnicity,
                "gender": gender,
                "fitness_experience": fitness_experience,
            }

            url = "http://api:4000/s/user_survey"
            response = requests.post(
                url,
                json=data,
            )











