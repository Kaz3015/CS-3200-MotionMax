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


