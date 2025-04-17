import requests
import streamlit as st

with st.form("MotionMAX Survey"):
    #reset the age change tracking in session state
    st.session_state["change age"] = False
    #make a small caption for context
    st.caption("User Demographics")
    #age selection with slider
    age = st.slider("How old are you?")
    #multiselect for user to choose one or more cultural backgrounds
    ethnicity = st.multiselect("What is your cultural background?", ["Caucasian", "Hispanic",
                               "African American", "Native American", "Asian", "Middle Eastern"])
    #gender selection using dropdown
    gender = st.selectbox("What is your gender?", ["Male", "Female"],
                          index = None)
    #fitness experience level selection using selectbox
    fitness_experience = st.selectbox("What is your fitness experience", ["Beginner", "Intermediate", "Advanced"],
                                      index = None)
    #submit button
    if st.form_submit_button("Submit"):
        #see if all inputs are there
        if age != 0 and ethnicity is not None and gender is not None and fitness_experience is not None:
            #list of selected ethnicities to comma-separated string
            ethnicity = ",".join(ethnicity)
            #make data dictionary to send in API request
            data = {
                "user_id": st.session_state["user_id"],
                "age": age,
                "ethnicity": ethnicity,
                "gender": gender,
                "fitness_experience": fitness_experience,
            }
            #API endpoint for survey submission
            url = "http://api:4000/s/user_survey"
            #send POST request with JSON payload
            response = requests.post(
                url,
                json=data,
            )

