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

if 'exercise_id' not in st.session_state:
    st.session_state['exercise_id'] = None
if 'exercise_name' not in st.session_state:
    st.session_state['exercise_name'] = 'default'
if 'exercise_equipment' not in st.session_state:
    st.session_state['exercise_equipment'] = 'default'
if 'exercise_target_muscle' not in st.session_state:
    st.session_state['exercise_target_muscle'] = 'default'
if 'exercise_difficulty' not in st.session_state:
    st.session_state['exercise_difficulty'] = 'default'
if 'exercise_type' not in st.session_state:
    st.session_state['exercise_type'] = 'default' 
if 'video_url' not in st.session_state:
    st.session_state['video_url'] = None  
if 'num_sets' not in st.session_state:
    st.session_state['num_sets'] = 1
if 'submitted_exercises' not in st.session_state:
    st.session_state['submitted_exercises'] = []
if 'circuit_name' not in st.session_state:
    st.session_state['circuit_name'] = "No Name"
if 'circuit_description' not in st.session_state:
    st.session_state['circuit_description'] = "No Description"

st.session_state["circuit_name"] = st.text_input("Circuit Name", value="No Name")
st.session_state["circuit_description"] = st.text_input("Circuit Description", value="No Description")


r1c1, r1c2 = st.columns([1, 1], border=True)

with r1c1:
    st.header("Search For Exercise")
    search_input = st.text_input("Search", value="")
    
    st.header("Search Filter")
    equipment = st.text_input("Equipment", value="", placeholder="")
    muscle_group = st.text_input("Muscle Group", value="", placeholder="")
    difficulty = st.selectbox("Difficulty", ("beginner", "intermediate", "advanced"), placeholder="beginner")
    exercise_type = st.selectbox("Exercise Type", ("strength", "cardiovascular", "flexibility", "balance"), placeholder="strength")
    
df = pd.DataFrame(requests.get(f'http://api:4000/c/exercise/search-filter/name/{search_input}/equipment/{equipment}/muscle_group/{muscle_group}/difficulty/{difficulty}/exercise_type/{exercise_type}/').json())
    
with r1c2:
    for index, row in df.iterrows():
        if st.button(f"{row['name']}\n\n" +
                  f"Equipment: {row['equipment_needed']}\n\n" +
                  f"Target Muscle: {row['target_muscle']}\n\n" +
                  f"Difficulty: {row['difficulty']}\n\n" +
                  f"Exercise Type: {row['exercise_type']}"):
            st.session_state['exercise_id'] = row['exercise_id']
            st.session_state['exercise_name'] = row['name']
            st.session_state['exercise_equipment'] = row['equipment_needed']
            st.session_state['exercise_target_muscle'] = row['target_muscle']
            st.session_state['exercise_difficulty'] = row['difficulty']
            st.session_state['exercise_type'] = row['exercise_type']
            st.session_state['video_url'] = row['video_url']
  
if 'sets_dict' not in st.session_state:
    st.session_state['sets_dict'] = {}
if 'exercise_dict' not in st.session_state:
    st.session_state['exercise_dict'] = {}
    
sets_dict = st.session_state["sets_dict"]
exercise_dict = st.session_state["exercise_dict"]
    
r2c1, r2c2, r2c3 = st.columns([1, 1, 1], border=True)

with r2c1:
    st.header("Exercise")
    
    if len(st.session_state['submitted_exercises']) != 0:
        for index in range(1, len(st.session_state['submitted_exercises'])):
            st.header(st.session_state['submitted_exercises'][index]['exercise_name'])
    
with r2c2:
    st.header("Workout Information")
    
    ir1c1, ir1c2 = st.columns([1, 1])
    
    with ir1c1:
        st.write(f"Exercise Name: {st.session_state['exercise_name']}")
        st.write(f"Difficulty: {st.session_state['exercise_difficulty']}")
        st.write(f"Exercise Type: {st.session_state['exercise_type']}")
        
        
    with ir1c2:
        st.write(f"Muscle Group: {st.session_state['exercise_target_muscle']}")
        st.write(f"Equipment: {st.session_state['exercise_equipment']}")
        
    for i in range(0, st.session_state['num_sets']):
        st.subheader(f"Set #{i+1}")
    
        reps_input = st.number_input("Reps", 0, key=f"reps_{i+1}")
        duration_input = st.number_input("Duration", 0, key=f"duration_{i+1}")
        superset_input = st.checkbox("Superset?", False, key=f"superset_{i+1}")
        rest_input = st.number_input("Rest", 0, key=f"rest_{i+1}")
    
    
    ir2c1, ir2c2 = st.columns([1, 1])
    
    with ir2c1:
        if st.button("Add Set"):
            st.session_state['num_sets']+=1
            
            reps_input = 0
            duration_input = 0
            superset_input = False
            rest_input = 0
    with ir2c2:
        if st.button("Submit Exercise"):
            full_set_info = []
            fail = False
            
            for i in range (0, st.session_state['num_sets']):
                if st.session_state.get(f"reps_{i+1}") != 0 and st.session_state.get(f"duration_{i+1}") != 0:
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
                
            if fail == False:
                exercise_info = {
                    "exercise_id": st.session_state["exercise_id"],
                    "exercise_name": st.session_state["exercise_name"],
                    "exercise_equipment": st.session_state["exercise_equipment"],
                    "exercise_target_muscle": st.session_state["exercise_target_muscle"],
                    "exercise_difficulty": st.session_state["exercise_difficulty"],
                    "exercise_type": st.session_state["exercise_type"],
                    "video_url": st.session_state["video_url"],
                    "sets": full_set_info
                }

                st.session_state['submitted_exercises'].append(exercise_info)
                st.session_state['num_sets'] = 1
                     
with r2c3:
    st.header("Technique Video")
    
    if st.session_state['video_url'] == None:
        st.write("There's no associated video url! Please add one!")
    else:
        st.video(st.session_state['video_url'])
    