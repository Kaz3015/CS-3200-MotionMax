import streamlit as st
import requests
import pandas as pd
import logging

st.title("MotionMAX App Feedback Results")
st.write("View all user feedback submissions for the MotionMAX application.")
#get the API endpoint for submitting the survey feedback
url = "http://api:4000/s/feedback_survey_output"
#send a get request to the API
response = requests.get(url)
#if the request is successful return the JSON data
if response.status_code == 200:
    logger = logging.getLogger(__name__)
    #turn the response to a list of feedback entries
    feedback_data = response.json()
    logger.info(feedback_data)


#display the feedback entries
if feedback_data:
    #show each feedback entry
    for i, feedback in enumerate(feedback_data):
        st.subheader(f"Feedback #{i+1}")
        if i > 5:
            break

        #make a display layout for each feedback entry
        with st.container():
            col1, col2 = st.columns([1, 2])

            with col1:
                st.write("**User ID:**")
                st.write("**How did you find our app:**")
                st.write("**How are you enjoying our app:**")
                st.write("**Improvements you would like:**")
                st.write("**Similar apps you use:**")
                st.write("**Most useful feature:**")
            #get and show data for each field using .get() to handle missing values safely
            with col2:
                st.write(feedback.get('user_id', 'N/A'))
                st.write(feedback.get('app_discovery', 'N/A'))
                st.write(feedback.get('app_enjoyment', 'N/A'))
                st.write(feedback.get('improvement_suggestions', 'N/A'))
                st.write(feedback.get('similar_apps', 'N/A'))
                st.write(feedback['most_useful_feature'])




