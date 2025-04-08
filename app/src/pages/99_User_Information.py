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

