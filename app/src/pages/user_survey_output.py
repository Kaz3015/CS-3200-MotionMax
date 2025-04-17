import streamlit as st
import pandas as pd
import requests

def display_user_survey(data):
    #find overall statistics
    total_users = sum(item['engagement_count'] for item in data)

    #age Distribution
    st.subheader("Age Distribution")
    #find ages into groups
    age_ranges = {
        "Teens (13-17)": 0,
        "Young Adults (18-24)": 0,
        "Adults (25-44)": 0,
        "Middle-Aged Adults(45-64)": 0,
        "Seniors (65+)": 0
    }

    for item in data:
        age = item['age']
        count = item['engagement_count']

        if 13 <= age <= 17:
            age_ranges["Teens (13-17)"] += count
        elif 18 <= age <= 24:
            age_ranges["Young Adults (18-24)"] += count
        elif 25 <= age <= 44:
            age_ranges["Adults (25-44)"] += count
        elif 45 <= age <= 64:
            age_ranges["Middle-Aged Adults(45-64)"] += count
        elif age >= 65:
            age_ranges["Seniors (65+)"] += count

    #display age percentages
    col1, col2 = st.columns(2)
    with col1:
        for age_group, count in age_ranges.items():
            percentage = count / total_users * 100 if total_users > 0 else 0
            st.write(f"{age_group}: {percentage:.1f}%")

    #gender distribution
    st.subheader("Gender Distribution")

    #calculate gender counts
    gender_counts = {"Male": 0, "Female": 0}

    for item in data:
        gender = item['gender']
        count = item['engagement_count']

        if gender in gender_counts:
            gender_counts[gender] += count

    #display gender percentages
    col1, col2 = st.columns(2)
    with col1:
        for gender, count in gender_counts.items():
            percentage = count / total_users * 100 if total_users > 0 else 0
            st.write(f"{gender}: {percentage:.1f}%")

    #cultural Background
    st.subheader("Cultural Background")

    #calculate cultural background counts
    cultural_counts = {}

    for item in data:
        cultural_backgrounds = item['cultural_background'].split(',')
        count = item['engagement_count']

        for bg in cultural_backgrounds:
            bg = bg.strip()
            if bg not in cultural_counts:
                cultural_counts[bg] = 0
            cultural_counts[bg] += count

    #display cultural background percentages
    col1, col2 = st.columns(2)
    with col1:
        for bg, count in cultural_counts.items():
            percentage = count / total_users * 100 if total_users > 0 else 0
            st.write(f"{bg}: {percentage:.1f}%")

    #fitness Experience
    st.subheader("Fitness Experience")

    #find fitness experience counts
    fitness_counts = {"Beginner": 0, "Intermediate": 0, "Advanced": 0}

    for item in data:
        experience = item['fitness_experience']
        count = item['engagement_count']

        if experience in fitness_counts:
            fitness_counts[experience] += count

    #display fitness experience percentages
    col1, col2 = st.columns(2)
    with col1:
        for exp, count in fitness_counts.items():
            percentage = count / total_users * 100 if total_users > 0 else 0
            st.write(f"{exp}: {percentage:.1f}%")


#main app
st.title("MotionMAX Demographics Dashboard")
st.header("User Demographics Overview")

#api call at the end in exactly the requested format
url = "http://api:4000/s/user_survey_output"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()

#display data
display_user_survey(data)

