import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import pandas as pd

st.set_page_config(layout="wide")

#Back button
if st.button("Back"):
    st.switch_page("pages/User_Information.py")

#Editable details for adding a food item
meal_name = st.text_input("Meal Name", value="None")
meal_type = st.selectbox("Meal Type", ("breakfast", "lunch", "dinner", "snack", "other"), placeholder="breakfast")
meal_calories = st.number_input("Calories", 0)
meal_protein = st.number_input("Protein", 0)
meal_carbs = st.number_input("Carbohydates", 0)
meal_fats = st.number_input("Fats", 0)
meal_servings = st.number_input("Servings", 1)

#Submit the food item button
if st.button("Submit Food"):
    #Check if the needed food log exists
    df = requests.get(f"http://api:4000/c/select/food_log/{st.session_state['user_id']}/{meal_type}/").json()
    if df:
        food_log_id = df[0]["food_log_id"]
    else:
        #If not, create a new food log and grab it's id
        food_log_id = requests.post(f"http://api:4000/c/insert/insert_food_log/{st.session_state['user_id']}/{meal_type}/").json()["food_log_id"]

    #Insert the food item and get its id
    food_item_id = requests.post(f"http://api:4000/c/insert/insert_food_item/{meal_name}/{meal_calories}/{meal_protein}/{meal_carbs}/{meal_fats}/").json()["food_item_id"]
    
    #Inset the food item to the food log through a bridge table
    response = requests.post(f"http://api:4000/c/insert/insert_food_item_to_food_log/{food_log_id}/{food_item_id}/{meal_servings}/")

    #Respond depending on the insertion of the food item to food log's response
    if response.ok:
        st.switch_page('pages/User_Information.py')
    else:
        st.error("Something went wrong when linking the food item. Please try again!")