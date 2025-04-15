import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import pandas as pd

#page configurations
st.set_page_config(layout="wide")



r1c1, r1c2, r1c3 = st.columns([1, 3, 1], border=True)

# Column involving the list of user-made workouts
with r1c1:
    st.header("List of My Workouts")
    df = pd.DataFrame(requests.get(f'http://api:4000/c/workouts/by-client/{st.session_state["user_id"]}').json())

    for index, row in df.iterrows():
        st.button(row['name'])
        
    st.write('')
    st.write('')
    
    if st.button('Create Circuit'):
        st.switch_page('pages/98_Create_Circuit.py')
    
with r1c2:
    st.header("Breakdown of Today's Workout")
    df = pd.DataFrame(requests.get(f'http://api:4000/c/workouts/currently-scheduled-exercises/{st.session_state["user_id"]}').json())
    
    #Inner columns for the breakdown of today's workout
    i_c1, i_c2 = st.columns([1, 2], border=True)
    
    with i_c1:
        st.header("Muscle Group Info")
        st.write(df.iloc[0]['target_muscle'])
        
        st.header("Full Workout Info")
        
        for i, row in df.iterrows():
            color = None
            
            if row['completed']:
                color = 'green'
            else:
                color = 'red'
            
            if row['reps'] != 0 and row['reps'] != None and row['set_order'] == 1:
                st.write('')
                st.write('')
                st.write(f"Name: {row['name']}")
                st.write(f":{color}[Set #{row['set_order']}:] {row['reps']} reps with {row['rest_seconds']}s of rest with {row['weight']}lb")
            elif row['reps'] != 0 and row['reps'] != None and row['set_order'] != 1:
                st.write(f":{color}[Set #{row['set_order']}:] {row['reps']} reps with {row['rest_seconds']}s of rest with {row['weight']}lb")
            elif row['duration_seconds'] != 0 and row['duration_seconds'] != None and row['set_order'] == 1:
                st.write('')
                st.write('')
                st.write(f"Name: {row['name']}")
                st.write(f":{color}[Set #{row['set_order']}:] {row['duration_seconds']}s with {row['rest_seconds']}s of rest with {row['weight']}lb")
            elif row['duration_seconds'] != 0 and row['duratiion_seconds'] != None and row['set_order'] != 1:
                st.write(f":{color}[Set #{row['set_order']}:] {row['duration_seconds']}s with {row['rest_seconds']}s of rest with {row['weight']}lb")
            elif row['is_superset'] == True and row['is_superset'] != None and row['set_order'] == 1:
                st.write('')
                st.write('')
                st.write(f"Name: {row['name']}")
                st.write(f":{color}[Set #{row['set_order']}:] superset with {row['rest_seconds']}s of rest with {row['weight']}lb")
            elif row['is_superset'] == True and row['is_superset'] != None and row['set_order'] != 1:
                st.write(f":{color}[Set #{row['set_order']}:] superset with {row['rest_seconds']}s of rest with {row['weight']}lb")
    
    with i_c2:
        st.header("Next Up Exercise Information")
        df = pd.DataFrame(requests.get(f'http://api:4000/c/workouts/currently-scheduled/next-exercise/{st.session_state["user_id"]}').json())
        
        st.write(f"Next Up: {df.iloc[0]['name']}")
        st.write(f"Target Muscle: {df.iloc[0]['target_muscle']}")
        
        if row['reps'] != 0:
            st.write(f"Current Set: {row['reps']} reps with {row['rest_seconds']}s of rest with {row['weight']}lb")
        elif row['duration_seconds'] != 0:
            st.write(f"Current Set: {row['duration_seconds']}s with {row['rest_seconds']}s of rest with {row['weight']}lb")
        else:
            st.write(f"Current Set: superset with {row['rest_seconds']}s of rest with {row['weight']}lb")
        
        st.header("Exercise Notes")
        
        st.write(df.iloc[0]['personal_notes'])
        
        st.header("Technique Video")
        st.video(df.iloc[0]['video_url'])
        
        
        st.button("Complete Set")
        
    
with r1c3:
    st.header("Status of Workout")
    df = pd.DataFrame(requests.get(f'http://api:4000/c/workouts/next-scheduled/video-url/{st.session_state["user_id"]}').json())
    
    if df.empty:
        st.write(":green[Congrats! Your workout is completed!]")
    else:
        st.write(":red[You haven't completed your workout for today! Remember to complete it!]")
    
    st.header("Motivation")
    df = pd.DataFrame(requests.get(f'http://api:4000/c/motivation/tip/').json())
    
    st.write(df.iloc[0]['text'])
    

r2c1, r2c2, r2c3 = st.columns([1, 3, 1], border=True)

with r2c1:
    st.header("List of Trainer Workouts for You")
    df = pd.DataFrame(requests.get(f'http://api:4000/c/workouts/by-trainer/{st.session_state["user_id"]}').json())
    
    for index, row in df.iterrows():
        st.button(row['name'])
        
with r2c2:
    st.header("Food Intake Data")
    
    st.subheader("Breakfast")
    df = pd.DataFrame(requests.get(f'http://api:4000/c/food/food_intake_information/"breakfast"/{st.session_state["user_id"]}/').json())
    
    if df.empty:
        st.write(f"#### Nothing logged yet!")
    else:
        for index, row in df.iterrows():
            st.write(f"##### {row['name']}")
            st.write(f"Calories: {row['calories']} calories")
            st.write(f"Protein: {row['protein']}g")
            st.write(f"Carbohydrates: {row['carbs']}g")
            st.write(f"Fats: {row['fats']}g")
    
    st.subheader("Lunch")
    df = pd.DataFrame(requests.get(f'http://api:4000/c/food/food_intake_information/"lunch"/{st.session_state["user_id"]}/').json())
    
    if df.empty:
        st.write(f"#### Nothing logged yet!")
    else:
        for index, row in df.iterrows():
            st.write(f"##### {row['name']}")
            st.write(f"Calories: {row['calories']} calories")
            st.write(f"Protein: {row['protein']}g")
            st.write(f"Carbohydrates: {row['carbs']}g")
            st.write(f"Fats: {row['fats']}g")
    
    st.subheader("Dinner")
    df = pd.DataFrame(requests.get(f'http://api:4000/c/food/food_intake_information/"dinner"/{st.session_state["user_id"]}/').json())
    
    if df.empty:
        st.write(f"#### Nothing logged yet!")
    else:
        for index, row in df.iterrows():
            st.write(f"##### {row['name']}")
            st.write(f"Calories: {row['calories']} calories")
            st.write(f"Protein: {row['protein']}g")
            st.write(f"Carbohydrates: {row['carbs']}g")
            st.write(f"Fats: {row['fats']}g")
    
    
    st.subheader("Snack")
    df = pd.DataFrame(requests.get(f'http://api:4000/c/food/food_intake_information/"snack"/{st.session_state["user_id"]}/').json())
    
    if df.empty:
        st.write(f"#### Nothing logged yet!")
    else:
        for index, row in df.iterrows():
            st.write(f"##### {row['name']}")
            st.write(f"Calories: {row['calories']} calories")
            st.write(f"Protein: {row['protein']}g")
            st.write(f"Carbohydrates: {row['carbs']}g")
            st.write(f"Fats: {row['fats']}g")
    
    df = pd.DataFrame(requests.get(f'http://api:4000/c/food/food_intake_information/"other"/{st.session_state["user_id"]}/').json())
    
    if not df.empty:
        st.subheader("Other")
        
        for index, row in df.iterrows():
            st.write(f"##### {row['name']}")
            st.write(f"Calories: {row['calories']} calories")
            st.write(f"Protein: {row['protein']}g")
            st.write(f"Carbohydrates: {row['carbs']}g")
            st.write(f"Fats: {row['fats']}g")
            
with r2c3:
    st.header("Calorie Intake Over Time")
    
    num_days = st.slider("Chart Time Frame", 1, 30, 6)
    nutrients_option = st.selectbox("Type of Nutrients", ("Calories", "Protein", "Carbohydrates", "Fats"), placeholder="Calories")
    
    df = pd.DataFrame(requests.get(f'http://api:4000/c/food/food_intake_information/all-nutrients-combined-for-day/{num_days}/{st.session_state["user_id"]}/').json())
    
    df['date'] = pd.to_datetime(df['Date'])
    df = df.sort_values(by='Date')

    st.line_chart(df, x='Date', y={nutrients_option}, x_label='Date', y_label={nutrients_option})
    
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    
    st.header("General Health Tips")
    df = pd.DataFrame(requests.get(f'http://api:4000/c/health/tip/').json())
    
    st.write(df.iloc[0]['text'])    