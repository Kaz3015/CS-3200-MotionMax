import logging


logger = logging.getLogger(__name__)

import streamlit as st
from app.src.trainer_components.render_list import name_button_column
from app.src import trainer_components as message_board
from app.src import trainer_components as render_client_graph
import requests

def on_name_click(name, subscriber_id):
  if st.session_state['subscriber_id'] != subscriber_id:
    st.session_state['subscriber_id'] = subscriber_id
    st.session_state['subscriber_name'] = name
    st.session_state['doubleClicked'] = False
  elif st.session_state['subscriber_id'] == subscriber_id:
    st.session_state['doubleClicked'] = True

  if st.session_state['doubleClicked']:
    st.doubleClicked = False
    st.switch_page('pages/01_Subscriber_Home.py')


st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user


st.title(f"Welcome Fitness Trainer, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')
response = requests.get(f'http://api:4000/t/{st.session_state["user_id"]}').json()
first_name = response['first_name']
last_name = response['last_name']
names = [f"{first_name} {last_name}"]
row1 = st.columns([1,2,1])
row2 = st.columns([1,2,1])
with row1[0]:
  name_button_column(title="List of clients", names=names, on_name_click=on_name_click, ids=response['subscriber_id'])
with row1[1,2]:
    message_board.render_message_board()
with row1[2]:
  client_macros = requests.get(f'http://api:4000/t/{st.session_state["user_id"]}/{st.session_state["subscriber_id"]}/macros').json()
  st.container(
    render_client_graph.plot_macro_pie_chart(client_macros["total_protein"],
                                             client_macros["total_carbs"],
                                             client_macros["total_fat"],
                                             title=f"Macronutrient Breakdown for {st.session_state['subscriber_name']}"),
    st.render_client_graph.weekly_workout(st.session_state['creator_id'],
                                              st.session_state['subscriber_id'],
                                              name=st.session_state['subscriber_name'])
  )
with row2[0]:
    meals = requests.get(f'http://api:4000/t/{st.session_state["user_id"]}/recipes').json()
name_button_column(title="List of Recipes", names=meals['recipe_title'], on_name_click=on_name_click, ids=meals['recipe_id'])
with row2[1]:
    st.write('### List of Workouts')

with row2[2]:
    workouts = requests.get(f'http://api:4000/t/{st.session_state["user_id"]}/workouts').json()
name_button_column(title="List of workouts", names=workouts['title'], on_name_click=on_name_click, ids=workouts['workout_id'])




if st.button('View World Map Demo', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/02_Map_Demo.py')