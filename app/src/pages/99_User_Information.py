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
