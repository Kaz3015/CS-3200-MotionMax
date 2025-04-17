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

#Initialization of session states
if 'exercise_id' not in st.session_state:
    st.session_state['exercise_id'] = None
if 'exercise_name' not in st.session_state:
    st.session_state['exercise_name'] = 'default'
if 'exercise_equipment' not in st.session_state:
    st.session_state['exercise_equipment'] = 'default'
if 'exercise_target_muscle' not in st.session_state:
    st.session_state['exercise_target_muscle'] = 'default'
if 'exercise_difficulty' not in st.session_state:
    st.session_state['exercise_difficulty'] = 'beginner'
if 'exercise_type' not in st.session_state:
    st.session_state['exercise_type'] = 'strength' 
if 'exercise_description' not in st.session_state:
    st.session_state['exercise_description'] = 'default'
if 'exercise_personal_notes' not in st.session_state:
    st.session_state['exercise_personal_notes'] = 'default'
if 'video_url' not in st.session_state:
    st.session_state['video_url'] = 'example.com'  
if 'num_sets' not in st.session_state:
    st.session_state['num_sets'] = 1
if 'submitted_exercises' not in st.session_state:
    st.session_state['submitted_exercises'] = []
if 'circuit_name' not in st.session_state:
    st.session_state['circuit_name'] = "No Name"
if 'circuit_description' not in st.session_state:
    st.session_state['circuit_description'] = "No Description"
if 'circuit_scheduled_date' not in st.session_state:
    st.session_state['circuit_scheduled_date'] = 'today'
if 'reset_sets' not in st.session_state:
    st.session_state['reset_sets'] = False

#Back button
if st.button("Back"):
    st.switch_page("pages/User_Information.py")

#Create text inputs for circuit information
st.session_state["circuit_name"] = st.text_input("Circuit Name", value="No Name")
st.session_state["circuit_description"] = st.text_input("Circuit Description", value="No Description")
st.session_state["circuit_scheduled_date"] = st.date_input("Scheduled Date", value="today", min_value="today")

#Temporary array for building sets (holds a dictionary)
full_set_info = []

#Two columns 
r1c1, r1c2 = st.columns([1, 1], border=True)

#Left column: Searching for Exercises
with r1c1:
    st.header("Search For Exercise")
    #Text input for the name of the exercise
    search_input = st.text_input("Search", value="")
    
    st.header("Search Filter")
    #Additional filter inputs
    equipment = st.text_input("Equipment", value="", placeholder="")
    muscle_group = st.text_input("Muscle Group", value="", placeholder="")
    difficulty = st.selectbox("Difficulty", ("all", "beginner", "intermediate", "advanced"), placeholder="all")
    exercise_type = st.selectbox("Exercise Type", ("all", "strength", "cardiovascular", "flexibility", "balance"), placeholder="strength")
    
#Fetch exercises based on the filters
df = pd.DataFrame(requests.get(f'http://api:4000/c/exercise/search-filter/name/{search_input}/equipment/{equipment}/muscle_group/{muscle_group}/difficulty/{difficulty}/exercise_type/{exercise_type}/').json())
    
#Right column: Iterating through found exercises
with r1c2:
    
    #Display each returned exercise as a button which updates the currently editing exercise if clicked
    for index, row in df.iterrows():
        if st.button(f"{row['name']}\n\n" +
                  f"Equipment: {row['equipment_needed']}\n\n" +
                  f"Target Muscle: {row['target_muscle']}\n\n" +
                  f"Difficulty: {row['difficulty']}\n\n" +
                  f"Exercise Type: {row['exercise_type']}",
                  key=f"select_ex_{row['exercise_id']}"):
            st.session_state['exercise_id'] = row['exercise_id']
            st.session_state['exercise_name'] = row['name']
            st.session_state['exercise_equipment'] = row['equipment_needed']
            st.session_state['exercise_target_muscle'] = row['target_muscle']
            st.session_state['exercise_difficulty'] = row['difficulty']
            st.session_state['exercise_type'] = row['exercise_type']
            st.session_state['video_url'] = row['video_url']
    
#Second row of 3 columns
r2c1, r2c2, r2c3 = st.columns([1, 1, 1], border=True)

#Row 2 left column: Submitted exercises for circuit
with r2c1:
    st.header("Exercise")
    
    #Show excercises already added to the circuit
    if len(st.session_state['submitted_exercises']) != 0:
        for index in range(0, len(st.session_state['submitted_exercises'])):
            st.subheader(f"#{index + 1}: {st.session_state['submitted_exercises'][index]['exercise_name']}")
            
            for index, e_set in enumerate(st.session_state['submitted_exercises'][index]['sets']):
                string = f"Set #{index + 1}:"
                
                if e_set['reps'] != 0:
                    string += f" {e_set['reps']} reps"
                elif e_set['duration'] != 0:
                    string += f" {e_set['duration']}s"
                else:
                    string += f" superset"
                
                string += f" of {e_set['weight']}lb with {e_set['rest']}s of rest\n\n"
                st.write(string)

    else:
        st.write("No exercises recorded yet!")
    
#Row 2 middle column: Exercise Information
with r2c2:
    st.header("Exercise Information")
    
    #Inner columns
    ir1c1, ir1c2 = st.columns([1, 1])
    
    #Inner left column: Editable Exercise Information
    with ir1c1:
        #Editable Exercise Details
        exercise_name = st.text_input("Exercise Name", value=st.session_state.get("exercise_name", "default"), key="workout_exercise_name")

        exercise_description = st.text_input("Exercise Description", value=st.session_state.get("exercise_description", "default"), key="workout_exercise_description")

        difficulty_options = ("beginner", "intermediate", "advanced")
        default_diff = st.session_state.get("exercise_difficulty", "beginner")
        diff_index = difficulty_options.index(default_diff) if default_diff in difficulty_options else 0
        exercise_difficulty = st.selectbox("Exercise Difficulty", options=difficulty_options, index=diff_index, key="workout_exercise_difficulty")
        
        type_options = ("strength", "cardiovascular", "flexibility", "balance")
        default_type = st.session_state.get("exercise_type", "strength")
        type_index = type_options.index(default_type) if default_type in type_options else 0
        exercise_type = st.selectbox("Exercise Type", options=type_options, index=type_index, key="workout_exercise_type")

        st.session_state["exercise_name"] = exercise_name
        st.session_state["exercise_description"] = exercise_description
        st.session_state["exercise_difficulty"] = exercise_difficulty
        st.session_state["exercise_type"] = exercise_type
        
    #Right Inner Column: Editable Exercise Details
    with ir1c2:
        #Editable Exercise Information
        st.text_input("Exercise Personal Notes", value=st.session_state.get("exercise_personal_notes", "default"))
        st.text_input("Exercise Target Muscle", value=st.session_state.get("exercise_target_muscle", "default"))
        st.text_input("Exercise Equipment", value=st.session_state.get("exercise_equipment", "default"))
        
    #Reset individual set inputs if requested
    if st.session_state["reset_sets"]:
        st.session_state["weight_1"]   = 0
        st.session_state["reps_1"]     = 0
        st.session_state["duration_1"] = 0
        st.session_state["superset_1"] = False
        st.session_state["rest_1"]     = 0
        st.session_state["reset_sets"] = False
        
    #Render respective inputs for each set
    for i in range(0, st.session_state['num_sets']):
        st.subheader(f"Set #{i+1}")
    
        weight_input = st.number_input("Weight (lb)", 0, key=f"weight_{i+1}")
        reps_input = st.number_input("Reps", 0, key=f"reps_{i+1}")
        duration_input = st.number_input("Duration (s)", 0, key=f"duration_{i+1}")
        superset_input = st.checkbox("Superset?", False, key=f"superset_{i+1}")
        rest_input = st.number_input("Rest (s)", 0, key=f"rest_{i+1}")
    
    #Inner columns
    ir2c1, ir2c2 = st.columns([1, 1])
    
    #Inner Row 2 left column: Adding Set Button
    with ir2c1:
        #Add another blank set
        if st.button("Add Set"):
            st.session_state['num_sets']+=1
            
            weight_input = 0
            reps_input = 0
            duration_input = 0
            superset_input = False
            rest_input = 0
        
    #Inner Row 2 Right Column: Submit Exercise
    with ir2c2:
        
        #Button to finalize the current exercise and respective sets
        if st.button("Submit Exercise"):
            fail = False
            
            #Ensure sets meet the conditions and validate
            for i in range (0, st.session_state['num_sets']):
                if st.session_state.get(f"reps_{i+1}") == 0 and st.session_state.get(f"duration_{i+1}") == 0 and st.session_state.get(f"superset_{i+1}") == False:
                    st.write(":red[You have conflicting information. Reps and duration are set to 0 while superset is set to false. Please establish a valid set tracker before submitting!]")
                    fail = True
                    break
                elif st.session_state.get(f"reps_{i+1}") != 0 and st.session_state.get(f"duration_{i+1}") != 0:
                    st.write(":red[You have conflicting information. A set has Reps and Duration as both non-zero numbers! Please fix before submitting!]")
                    st.write(st.session_state.get(f"reps_{i+1}"))
                    st.write(st.session_state.get(f"duration_{i+1}"))
                    fail = True
                    break
                elif st.session_state.get(f"reps_{i+1}") != 0 and st.session_state.get(f"superset_{i+1}") != False:
                    st.write(":red[You have conflicting information. A set has Reps and Superset as both non-zero numbers! Please fix before submitting!]")
                    fail = True
                    break
                elif st.session_state.get(f"duration_{i+1}") != 0 and st.session_state.get(f"superset_{i+1}") != False:
                    st.write(":red[You have conflicting information. A set has Duration and Superset as both non-zero numbers! Please fix before submitting!]")
                    fail = True
                    break
                
                #If valid, collect and append set info
                new_set = {
                    "weight": st.session_state.get(f"weight_{i+1}"),
                    "reps": st.session_state.get(f"reps_{i+1}"),
                    "duration": st.session_state.get(f"duration_{i+1}"),
                    "superset": st.session_state.get(f"superset_{i+1}"),
                    "rest": st.session_state.get(f"rest_{i+1}"),
                }
                
                full_set_info.append(new_set)
                
            #If sets are valid, append the exercise to the circuit
            if fail == False:
                exercise_info = {
                    "exercise_id": st.session_state["exercise_id"],
                    "exercise_name": st.session_state["exercise_name"],
                    "exercise_description": st.session_state["exercise_description"],
                    "exercise_equipment": st.session_state["exercise_equipment"],
                    "exercise_target_muscle": st.session_state["exercise_target_muscle"],
                    "exercise_difficulty": st.session_state["exercise_difficulty"],
                    "exercise_type": st.session_state["exercise_type"],
                    "exercise_personal_notes": st.session_state["exercise_personal_notes"],
                    "video_url": st.session_state["video_url"],
                    "sets": full_set_info
                }

                #Set session states back to defaults
                st.session_state['submitted_exercises'].append(exercise_info)
                st.session_state['num_sets'] = 1
                st.session_state['exercise_name'] = 'default'
                st.session_state['exercise_equipment'] = 'default'
                st.session_state['exercise_target_muscle'] = 'default'
                st.session_state['exercise_difficulty'] = 'beginner'
                st.session_state['exercise_type'] = 'strength'
                st.session_state['exericse_description'] = 'default'
                st.session_state['exercise_personal_notes'] = 'default'
                st.session_state['video_url'] = 'example.com'
                st.session_state['reset_sets'] = True
                
#Row 2 Right Column: Technique Video     
with r2c3:
    st.header("Technique Video")
    
    #Show video preview if a URL is present
    if st.session_state['video_url'] == None:
        st.write("There's no associated video url! Please add one!")
    else:
        video_url = st.text_input("Video URL", value=st.session_state['video_url'])
        st.session_state['video_url'] = video_url
        
        try:
            st.video(st.session_state['video_url'])
        except Exception:
            st.write("This URL is not valid! Please find another one!")
        
#Submit Circuit button
if st.button("Submit Circuit"):
    
    if len(st.session_state["submitted_exercises"]) == 0:
        st.write(":red[There must be atleast one workout!]")
    else:
        for idx, exercise in enumerate(st.session_state["submitted_exercises"]):
            exercise['sets']
        
        if st.session_state["circuit_name"] == None:
            st.write(":red[Please specify a circuit name!]")
        elif st.session_state["circuit_description"] == None:
            st.write(":red[Please specify a circuit description!]")
        
        #Request to create a circuit
        circuit_response = requests.post(f"http://api:4000/c/insert/circuit/{st.session_state['user_id']}/{st.session_state['circuit_name']}/{st.session_state['circuit_description']}/{st.session_state['circuit_scheduled_date']}").json()
        
        if circuit_response.get('status') == 'success':
            #Grab the created circuit id
            circuit_id = (pd.DataFrame(requests.get(f"http://api:4000/c/select/newly-made-circuit-id/{st.session_state['user_id']}/").json())).iloc[0]['circuit_id']
        
            #Add each exercise and its sets to the circuit
            for index, exercise in enumerate(st.session_state["submitted_exercises"]):
                exercise_response = requests.post(f"http://api:4000/c/insert/exercise_to_circuit/{circuit_id}/", json=exercise).json()

                #Fetch the last added exercise
                df = pd.DataFrame(requests.get(f"http://api:4000/c/select/last_exercise_added_to_circuit/{st.session_state['user_id']}/{circuit_id}/").json())
                exercise_id = df.iloc[0]['exercise_id']
                
                #Add sets to the last added exercise
                for index, e_set in enumerate(exercise["sets"]):
                    exercise_set_response = requests.post(f"http://api:4000/c/insert/exercise_set_to_circuit/{exercise_id}/{index + 1}/{e_set['weight']}/{e_set['reps']}/{e_set['duration']}/{e_set['superset']}/{e_set['rest']}/").json()
                
                #Reset session states to defaults
                st.session_state['exercise_name'] = 'default'
                st.session_state['exercise_equipment'] = 'default'
                st.session_state['exercise_target_muscle'] = 'default'
                st.session_state['exercise_difficulty'] = 'beginner'
                st.session_state['exercise_type'] = 'strength'
                st.session_state['exercise_description'] = 'default'
                st.session_state['exercise_personal_notes'] = 'default'
                st.session_state['video_url'] = 'example.com'
                st.session_state['num_sets'] = 1
                st.session_state['submitted_exercises'] = []
                st.session_state['circuit_name'] = 'No Name'
                st.session_state['circuit_description'] = 'No Description'
                st.session_state['circuit_scheduled_date'] = 'today'
                st.session_state['reset_sets'] = False
                st.session_state['video_url'] = 'example.com'          
            
            #Redirect back to the main page
            st.switch_page('pages/User_Information.py')
        else:
            st.write(circuit_response.get('message'))