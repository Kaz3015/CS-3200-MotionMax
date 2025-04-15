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