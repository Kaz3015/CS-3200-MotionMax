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

# Column involving the list of user-made workouts
r1c1, r1c2, r1c3 = st.columns([1, 3, 1], border=True)

#Left column: List of User-made Workouts
with r1c1:
    st.header("List of My Workouts")
    
    #Get all circuits created by the user and iterate through them, displaying them
    df = pd.DataFrame(requests.get(f'http://api:4000/c/workouts/by-client/{st.session_state["user_id"]}').json())
    for index, row in df.iterrows():
        st.subheader(row['name'])
        
    st.write('')
    st.write('')
    
    #Button to navigate to create a new circuit
    if st.button('Create Circuit'):
        st.switch_page('pages/Create_Circuit.py')
    
#Middle Column: Breakdown of Today's Workout
with r1c2:
    st.header("Breakdown of Today's Workout")
    
    #Fetch the next up exercise
    next_exercise = pd.DataFrame(requests.get(f'http://api:4000/c/workouts/currently-scheduled/next-exercise/{st.session_state["user_id"]}').json())
    
    #If there is no next up exercise, then workout is complete and respond accordingly
    if next_exercise.empty:
        st.write("Workout completed for today! Great job!")
    else:
        #else, identify the circuit we're looking at and fetch its exercise information
        associated_circuit_id = next_exercise.iloc[0]['circuit_id']
        #Grab the currently scheduled exercises for the circuit
        df = pd.DataFrame(requests.get(f'http://api:4000/c/workouts/currently-scheduled-exercises/{st.session_state["user_id"]}/{associated_circuit_id}/').json())
        
        #Inner columns for the breakdown of today's workout
        i_c1, i_c2 = st.columns([1, 2], border=True)
            
        #Lefter inner column: Muscle group and full workout details
        with i_c1:
            st.header("Muscle Group Info")
            st.write(df.iloc[0]['target_muscle'])
            
            st.header("Full Workout Info")
            
            #Loop through each exercise in the circuit, color coding whether a set is completed or not
            for i, row in df.iterrows():
                color = None
                
                if row['completed']:
                    color = 'green'
                else:
                    color = 'red'
                
                #Determine the text to display, depending on whether it uses reps, duration, or superset
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
        
        #Right inner column: Next up exercise information
        with i_c2:
            st.header("Next Up Exercise Information")
            
            #Fetch next up exercise details
            df = pd.DataFrame(requests.get(f'http://api:4000/c/workouts/currently-scheduled/next-exercise/{st.session_state["user_id"]}').json())

            #Display next up exercise information
            st.write(f"Next Up: {df.iloc[0]['name']}")
            st.write(f"Target Muscle: {df.iloc[0]['target_muscle']}")
            st.session_state['video_url'] = df.iloc[0]['video_url']
            
            #Display current set details
            if row['reps'] != 0:
                st.write(f"Current Set: {row['reps']} reps with {row['rest_seconds']}s of rest with {row['weight']}lb")
            elif row['duration_seconds'] != 0:
                st.write(f"Current Set: {row['duration_seconds']}s with {row['rest_seconds']}s of rest with {row['weight']}lb")
            else:
                st.write(f"Current Set: superset with {row['rest_seconds']}s of rest with {row['weight']}lb")
            
            st.header("Exercise Notes")
            st.write(df.iloc[0]['personal_notes'])
            
            st.header("Technique Video")
            
            #Display the video
            try:
                st.video(st.session_state['video_url'])
            except Exception:  
                st.write("Cannot find the video! Please double check the video URL!")
            
            #Button to mark a set as complete
            if st.button("Complete Set"):
                df = pd.DataFrame(requests.get(f"http://api:4000/c/workouts/currently-scheduled/next-exercise/{st.session_state['user_id']}").json())
                exerciseset_id = df.iloc[0]['exerciseset_id']
                exercise_id   = df.iloc[0]['exercise_id']
                circuit_id    = df.iloc[0]['circuit_id']

                df_set = requests.put(f"http://api:4000/c/update/complete_exercise_set/{exercise_id}/{exerciseset_id}/").json()

                if df_set.get('status') == 'success':
                    st.success("Set completed!")

                    #Fetch details about if other sets remain, if not then log the workout
                    df = pd.DataFrame(requests.get(f"http://api:4000/c/workouts/currently-scheduled/next-exercise/{st.session_state['user_id']}").json())

                    if df.empty:
                        df = requests.post(f"http://api:4000/c/insert/workout_log/{st.session_state['user_id']}/{circuit_id}/").json()

                        if df.get("status") == "success":
                            st.success("Entire circuit complete—workout logged!")
                        else:
                            st.error(f"Failed to log workout: {df.get('message')}")
                else:
                    st.error(f"Error completing set: {df_set.get('message')}")
    
#Right column: Workout Status and Motivation
with r1c3:
    #Displays the current status of the workout along with a reminder if they haven't completed it yet
    st.header("Status of Workout")
    df = pd.DataFrame(requests.get(f'http://api:4000/c/workouts/next-scheduled/video-url/{st.session_state["user_id"]}').json())
    next_exercise = pd.DataFrame(requests.get(f'http://api:4000/c/workouts/currently-scheduled/next-exercise/{st.session_state["user_id"]}').json())
    
    #Displays a nice message if the workout is complete, a reminder to complete if not
    if df.empty or next_exercise.empty:
        st.write(":green[Congrats! Your workout is completed!]")
    else:
        st.write(":red[You haven't completed your workout for today! Remember to complete it!]")
    
    #Displays some motivation to motivate the user
    st.header("Motivation")
    
    #Fetch motivation message
    df = pd.DataFrame(requests.get(f'http://api:4000/c/motivation/tip/').json())
    
    #If there is an error getting the motivation message, send text saying that 
    if df.empty:
        st.write("No motivation tip available right now.")
    else:
        st.write(df.iloc[0]['text'])


#Second row of columns
r2c1, r2c2, r2c3 = st.columns([1, 3, 1], border=True)

#Left Column: List of Workouts Assigned By Trainer For User
with r2c1:
    st.header("List of Trainer Workouts for You")
    
    #Fetch workouts assigned by trainer for a user
    df = pd.DataFrame(requests.get(f'http://api:4000/c/workouts/by-trainer/{st.session_state["user_id"]}').json())
    
    #Iterate through circuits and display them
    for index, row in df.iterrows():
        st.button(row['name'])
      
#Middle Column: Food Intake Data  
with r2c2:
    st.header("Food Intake Data")
    
    
    st.subheader("Breakfast")
    #Fetch breakfast food intake data
    df = pd.DataFrame(requests.get(f'http://api:4000/c/food/food_intake_information/"breakfast"/{st.session_state["user_id"]}/').json())
    
    #Iterate through breakfast food intake data
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
    #Fetch lunch food intake data
    df = pd.DataFrame(requests.get(f'http://api:4000/c/food/food_intake_information/"lunch"/{st.session_state["user_id"]}/').json())
    
    #Iterate through lunch food intake data
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
    #Fetch dunner food intake data
    df = pd.DataFrame(requests.get(f'http://api:4000/c/food/food_intake_information/"dinner"/{st.session_state["user_id"]}/').json())
    
    #Iterate through dinner food intake data
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
    #Fetch snack food intake data
    df = pd.DataFrame(requests.get(f'http://api:4000/c/food/food_intake_information/"snack"/{st.session_state["user_id"]}/').json())
    
    #Iterate through snack food intake data
    if df.empty:
        st.write(f"#### Nothing logged yet!")
    else:
        for index, row in df.iterrows():
            st.write(f"##### {row['name']}")
            st.write(f"Calories: {row['calories']} calories")
            st.write(f"Protein: {row['protein']}g")
            st.write(f"Carbohydrates: {row['carbs']}g")
            st.write(f"Fats: {row['fats']}g")
    
    #Fetch other food intake data
    df = pd.DataFrame(requests.get(f'http://api:4000/c/food/food_intake_information/"other"/{st.session_state["user_id"]}/').json())
    
    #Iteate through other food intake data
    if not df.empty:
        st.subheader("Other")
        
        for index, row in df.iterrows():
            st.write(f"##### {row['name']}")
            st.write(f"Calories: {row['calories']} calories")
            st.write(f"Protein: {row['protein']}g")
            st.write(f"Carbohydrates: {row['carbs']}g")
            st.write(f"Fats: {row['fats']}g")
         
    #Arbituary spacing   
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    
    #Button to Add a Food Item
    if st.button("Add Food Item"):
        st.switch_page('pages/Add_Food.py')
            
#Right Column: Macro Intake Over Time and Health Tips
with r2c3:
    st.header(f"Macro Intake Over Time")
    
    #Filter information for the macro intake chart
    num_days = st.slider("Chart Time Frame", 1, 30, 6)
    nutrients_option = st.selectbox("Type of Nutrients", ("Calories", "Protein", "Carbohydrates", "Fats"), placeholder="Calories")
    
    #Fetch aggregated nutrients for current day
    df = pd.DataFrame(requests.get(f'http://api:4000/c/food/food_intake_information/all-nutrients-combined-for-day/{num_days}/{st.session_state["user_id"]}/').json())
    
    #Convert date strings to datetime and sort
    df['date'] = pd.to_datetime(df['Date'])
    df = df.sort_values(by='Date')

    #Plot line chart
    st.line_chart(df, x='Date', y={nutrients_option}, x_label='Date', y_label={nutrients_option})
    
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    
    st.header("General Health Tips")
    #Fetch a general health tip and display it
    df = pd.DataFrame(requests.get(f'http://api:4000/c/health/tip/').json())
    
    st.write(df.iloc[0]['text'])