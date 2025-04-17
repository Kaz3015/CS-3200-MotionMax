import trainer_components.render_client_graph as render_client_graph
import trainer_components.render_list as render_list
import streamlit as st
import streamlit_shadcn_ui as ui
import requests
import logging
from modules.nav import SideBarLinks

SideBarLinks(show_home=True)

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

row = st.columns([2.5, 3.5, 4])
with row[0]:
    response = requests.get(f'http://api:4000/t/{st.session_state["user_id"]}/getClients').json()
    logger = logging.getLogger(__name__)
    logger.info(f"Response: {response}")

    names = [f"{person['first_name']} {person['last_name']}" for person in response]
    logger.info(f"Names: {names}")
    st.session_state['subscriber_name'] = names[0]
    subscriber_ids = [person['subscriber_id'] for person in response]
    render_list.name_button_column(title="List of Clients", names=names, on_click_function=on_name_click,
                                   on_delete_function=None, ids=subscriber_ids, key="client")
with row[2]:
    client_macros = requests.get(
        f'http://api:4000/t/{st.session_state["user_id"]}/{st.session_state["subscriber_id"]}/macros').json()
    fig = render_client_graph.create_macro_donut(client_macros[0]["total_protein"],
                                                 client_macros[0]["total_carbs"],
                                                 client_macros[0]["total_fat"],
                                                 title=f"Macronutrient Breakdown for {st.session_state['subscriber_name']}")
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

    with row[1]:
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