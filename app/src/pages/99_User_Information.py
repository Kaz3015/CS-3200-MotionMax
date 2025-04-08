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


st.header('Client/User Information')

# You can access the session state to make a more customized/personalized app experience
st.write(f"### Hi, {st.session_state['first_name']}.")

#LIST OF USER-MADE WORKOUTS
st.write(f"## List of Current User-made Workouts")

df = pd.DataFrame(requests.get(f'http://api:4000/c/workouts/by-client/{st.session_state["user_id"]}').json())
st.dataframe(df)

#LIST OF TRAINER-MADE WORKOUTS FOR USER
st.write(f"## List of Current Trainer-made Workouts")

df = pd.DataFrame(requests.get(f'http://api:4000/c/workouts/by-trainer/{st.session_state["user_id"]}').json())
st.dataframe(df)

#BREAKDOWN OF ALL EXERCISES SCHEDULED WORKOUT FOR TODAY
st.write(f"## Breakdown of currently scheduled exercises in the workout for today")

df = pd.DataFrame(requests.get(f'http://api:4000/c/workouts/currently-scheduled-exercises/{st.session_state["user_id"]}').json())
st.dataframe(df)

#BREAKDOWN OF CURRENTLY SCHEDULED WORKOUT FOR TODAY
st.write(f"## Breakdown of currently scheduled workout for today")

df = pd.DataFrame(requests.get(f'http://api:4000/c/workouts/currently-scheduled/next-exercise/{st.session_state["user_id"]}').json())
st.dataframe(df)

#MAKE AN EQUIPMENT-BASED SEARCH
st.write(f"## Make an equipment based search")

equipment_string = st.text_input("Equipment", "")

df = pd.DataFrame(requests.get(f'http://api:4000/c/equipment-based-search/{equipment_string}').json())
st.dataframe(df)

#MAKE A DIFFICULTY-BASED SEARCH
st.write(f"## Make a difficulty based search")

beginner = st.checkbox("Beginner", value=False)
intermediate = st.checkbox("Intermediate", value=True)
advanced = st.checkbox("Advanced", value=True)

df = pd.DataFrame(requests.get(f'http://api:4000/c/difficulty-based-search/{beginner}/{intermediate}/{advanced}/').json())
st.dataframe(df)

#MAKE A TARGET MUSCLE BASED SEARCH
st.write(f"## Make a target muscle based search")

target_muscle_string = st.text_input("Target Muscle", "")

df = pd.DataFrame(requests.get(f'http://api:4000/c/target-muscle-based-search/{target_muscle_string}').json())
st.dataframe(df)

#MAKE A EXERCISE TYPE BASED SEARCH
st.write(f"## Make an exercise type based search")

exercise_type_string = st.text_input("Exercise Type", "")

df = pd.DataFrame(requests.get(f'http://api:4000/c/exercise-type-based-search/{exercise_type_string}').json())
st.dataframe(df)

#GRAB THE NEXT UP EXERCISES VIDEO URL
st.write(f"## Next up exercise's video URL")

df = pd.DataFrame(requests.get(f'http://api:4000/c/workouts/next-scheduled/video-url/{st.session_state["user_id"]}').json())
st.dataframe(df)

#GET A RANDOM HEALTH TIP
st.write(f'## Random health tip')

df = pd.DataFrame(requests.get(f'http://api:4000/c/health/tip/').json())
st.dataframe(df)

#GET A RANDOM MOTIVATION TIP
st.write(f'## Random motivation tip')

df = pd.DataFrame(requests.get(f'http://api:4000/c/motivation/tip/').json())
st.dataframe(df)