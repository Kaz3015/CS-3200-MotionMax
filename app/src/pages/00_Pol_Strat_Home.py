import logging
import pathlib

logger = logging.getLogger(__name__)

import streamlit as st
import trainer_components.render_list as render_list
import trainer_components.message_board as message_board
import trainer_components.render_client_graph as render_client_graph
import trainer_components.workout_form as workout_form
import trainer_components.render_recipe_form as recipe_form
import trainer_components.pill as pill
import streamlit_shadcn_ui as ui
import requests
import pandas as pd
import numpy as np
import os


def on_name_click(name, subscriber_id):
    if st.session_state['subscriber_id'] != subscriber_id:
        st.session_state['subscriber_id'] = subscriber_id
        st.session_state['subscriber_name'] = name
        st.session_state['doubleClicked'] = False
    elif st.session_state['subscriber_id'] == subscriber_id:
        st.session_state['doubleClicked'] = True

    if st.session_state['doubleClicked']:
        st.doubleClicked = False
        # st.switch_page('pages/01_Subscriber_Home.py')



st.title(f"Welcome Fitness Trainer, {st.session_state['first_name']}.")

row1 = st.columns([3, 2, 5])
row2 = st.columns(1, border=True)
row3 = st.columns([3, 4, 3], border=True)
current_file = os.path.basename(__file__)

# Check if we're on the specific page you want to style
if current_file == "00_Pol_Strat_Home.py":
    # Apply custom styling only for this page
    st.markdown("""
    <style>
        /* Custom theme for this page only */
        .stApp {
            background-color: #f5f7fa;
        }
    </style>
    """, unsafe_allow_html=True)

with row1[0]:
    response = requests.get(f'http://api:4000/t/{st.session_state["user_id"]}/getClients').json()
    names = [f"{person['first_name']} {person['last_name']}" for person in response]
    st.session_state['subscriber_name'] = names[0]
    subscriber_ids = [person['subscriber_id'] for person in response]
    render_list.name_button_column(title="List of Clients", names=names, on_click_function=on_name_click,
                                   on_delete_function=None, ids=subscriber_ids, key="client")
    # rev_row1 = st.columns(2)
    # rev_row2 = st.columns(2)
    # rev_row3 = st.columns(1)
    # with rev_row1[0]:
    #     ui.metric_card(title="YTD", content="$4500", description="Total Revenue", key="ytd")
    # with rev_row1[1]:
    #     ui.metric_card(title="Best Month", content="$600", description="You had 50 subscribers this month")
    # with rev_row2[0]:
    #     ui.metric_card(title="Monthly Revenue", content="$500", description="20% more than last month")
    # with rev_row2[1]:
    #     ui.metric_card(title="Subscriber Amount", content="9 Subscribers", description="20% more than last month")
    # with rev_row3[0]:
    #     chart_data = pd.DataFrame(
    #         {
    #             "col1": np.random.randn(20),
    #             "col2": np.random.randn(20),
    #             "col3": np.random.choice(["A", "B", "C"], 20),
    #         }
    #     )
    #
    #     st.line_chart(chart_data, x="col1", y="col2", color="col3")

with row1[2]:
    st.markdown("""
        <style>
        .st-key-message_board {
                background-color: white;
                border-radius: 12px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
                border: 1px solid #edf2f7;
                transition: all 0.3s ease;
                padding: 20px;
        }
        .st-key-message_board:hover {
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
            transform: translateY(-2px);
            transition: box-shadow 0.3s ease;
        }
        </style>
        """, unsafe_allow_html=True)
    with st.container(key="message_board"):
        message_board.render_message_board()

with row2[0]:
    client_macros = requests.get(
        f'http://api:4000/t/{st.session_state["user_id"]}/{st.session_state["subscriber_id"]}/macros').json()
    fig = render_client_graph.create_macro_donut(client_macros[0]["total_protein"],
                                                 client_macros[0]["total_carbs"],
                                                 client_macros[0]["total_fat"],
                                                 title=f"Macronutrient Breakdown for {st.session_state['subscriber_name']}")
    info = st.columns([5, 5])
    with info[1]:
        st.markdown("""
                <style>
                .st-key-macro_chart {
                        background-color: white;
                        border-radius: 12px;
                        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
                        border: 1px solid #edf2f7;
                        transition: all 0.3s ease;
                        padding: 20px;
                }
                .st-key-macro_chart:hover {
                    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
                    transform: translateY(-2px);
                    transition: box-shadow 0.3s ease;
                }
                </style>
                """, unsafe_allow_html=True)

        macro_chart = st.container(key="macro_chart")
        macro_chart.markdown(f"""
                <h3 style="margin-bottom: 15px;">{st.session_state['subscriber_name']}'s Macros for today</h3>
                """, unsafe_allow_html=True)
        macro_chart.plotly_chart(fig, use_container_width=True)
    with info[0]:
        st.markdown("""
                    <style>
                    .st-key-weekly_workouts {
                            background-color: white;
                            border-radius: 12px;
                            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
                            border: 1px solid #edf2f7;
                            transition: all 0.3s ease;
                            padding: 20px;
                            max-width: 500px;
                    }
                    .st-key-weekly_workouts:hover {
                        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
                        transform: translateY(-2px);
                        transition: box-shadow 0.3s ease;
                    }
                    </style>
                    """, unsafe_allow_html=True)

        # Create a container with custom styling
        weekly_workouts = st.container(key="weekly_workouts")
        # Title with styling
        weekly_workouts.markdown(f"""
            <h3 style="margin-bottom: 15px;">{st.session_state['subscriber_name']}'s Weekly Workout</h3>
            """, unsafe_allow_html=True)
        df = render_client_graph.render_weekly_workouts()
        with weekly_workouts:
            ui.table(df)


with row3[0]:
    def on_workout_click(name, workout_id):
        st.session_state['workout_id'] = workout_id
        st.session_state['form'] = "workout form"

    def on_workout_delete(name, workout_id):
        requests.delete(f'http://api:4000/t/{st.session_state["user_id"]}/{workout_id}/deleteWorkout')
        # st.session_state['existing recipe'] = False
        # st.session_state['form'] = "recipe form"
        # st.experimental_rerun()

    workout_data = requests.get(f'http://api:4000/t/{st.session_state["user_id"]}/workoutNames').json()
    workout_names = [name['title'] for name in workout_data]
    workout_ids = [workout_id['w_id'] for workout_id in workout_data]
    st.session_state['workout_loaded'] = False

    render_list.name_button_column(title="List of Workouts", names=workout_names, on_click_function=on_workout_click,
                                   on_delete_function=on_workout_delete, ids=workout_ids, key="workout")
with row3[1]:
    if st.session_state['form'] == "workout form":
        with st.container(key="bye"):
            workout_form.render_workout_form()
    elif st.session_state['form'] == "recipe form":
        recipe_form.render_recipe_form()

with row3[2]:
    def on_recipe_click(name, recipe_id):
        st.session_state['recipe_id'] = recipe_id
        st.session_state['existing recipe'] = True
        st.session_state['form'] = "recipe form"
        st.session_state['used_ingredients'] = []
    def on_recipe_delete(name, recipe_id):
        requests.delete(f'http://api:4000/t/{st.session_state["user_id"]}/{recipe_id}/deleteRecipe')
        st.session_state['existing recipe'] = False
        st.session_state['form'] = "recipe form"


    recipes = requests.get(f'http://api:4000/t/{st.session_state["user_id"]}/recipes').json()
    recipe_dict = dict(zip([name['recipe_title'] for name in recipes], [recipe_id['r_id'] for recipe_id in recipes]))
    logger.info(f"Recipe data: {recipe_dict}")
    recipe_title = recipe_dict.keys()
    recipe_ids = recipe_dict.values()
    render_list.name_button_column(title="List of Recipes", names=recipe_title, on_click_function=on_recipe_click,
                               on_delete_function=on_recipe_delete, ids=recipe_ids, key="recipe")


if st.button('View World Map Demo',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/02_Map_Demo.py')
