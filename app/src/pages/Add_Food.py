import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import pandas as pd

st.set_page_config(layout="wide")

if st.button("Back"):
    st.switch_page("pages/User_Information.py")

meal_name = st.text_input("Meal Name", value="None")

meal_type = st.selectbox("Meal Type", ("breakfast", "lunch", "dinner", "snack", "other"), placeholder="breakfast")

meal_calories = st.number_input("Calories", 0)
meal_protein = st.number_input("Protein", 0)
meal_carbs = st.number_input("Carbohydates", 0)
meal_fats = st.number_input("Fats", 0)
meal_servings = st.number_input("Servings", 1)

if st.button("Submit Food"):
    df = requests.get(f"http://api:4000/c/select/food_log/{st.session_state['user_id']}/{meal_type}/").json()
    if df:
        food_log_id = df[0]["food_log_id"]
    else:
        food_log_id = requests.post(f"http://api:4000/c/insert/insert_food_log/{st.session_state['user_id']}/{meal_type}/").json()["food_log_id"]

    food_item_id = requests.post(f"http://api:4000/c/insert/insert_food_item/{meal_name}/{meal_calories}/{meal_protein}/{meal_carbs}/{meal_fats}/").json()["food_item_id"]
    
    response = requests.post(f"http://api:4000/c/insert/insert_food_item_to_food_log/{food_log_id}/{food_item_id}/{meal_servings}/")

    if response.ok:
        st.switch_page('pages/User_Information.py')
    else:
        st.error("Something went wrong when linking the food item. Please try again!")