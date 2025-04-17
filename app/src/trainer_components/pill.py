import streamlit as st
import logging


def split_pill_selector(key, option_left, option_right):
    logger = logging.getLogger(__name__)
    def on_click_left():
        st.session_state[f"{key}_selected"] = True
        st.session_state['form'] = option_left.lower()
        logger.info(f"Left option clicked: {st.session_state['form']}")
    def on_click_right():
        st.session_state[f"{key}_selected"] = False
        st.session_state['recipe_id'] = None
        st.session_state['existing recipe'] = False
        st.session_state['recipe_title'] = ""
        st.session_state['recipe_description'] = ""
        st.session_state['calories'] = 0
        st.session_state['protein'] = 0
        st.session_state['carbs'] = 0
        st.session_state['fat'] = 0
        st.session_state['instructions'] = ""
        st.session_state['used_ingredients'] = []
        st.session_state['form'] = option_right.lower()
        logger.info(f"Right option clicked: {st.session_state['form']}")

    # Initialize session state
    st.session_state['left_clicked'] = False
    st.session_state['right_clicked'] = False
    if f"{key}_selected" not in st.session_state:
        st.session_state[f"{key}_selected"] = True

    # Set color for currently selected form
    background_right = "#6f90f2" if st.session_state['form'] == 'workout form' else "#FFFFFF"
    background_left = "#FFFFFF" if st.session_state['form'] == 'workout form' else "#6f90f2"


    left_class = f"pill-option-active-{key}"
    right_class = f"pill-option-inactive-{key}"

    # CSS for the pill component
    st.markdown(f"""
    <style>
    .st-key-pill-container-{key} {{
        display: flex;
        flex-direction: row;
        gap: 0px;
        width: 100%;
        max-width: 400px;
        border-radius: 50px;
        overflow: hidden;
        justify-content: right;
    }}
    
    
    
    .st-key-pill-container-{key} .st-key-pill-option-active-{key} {{
        border-top-left-radius: 50px;
        border-bottom-left-radius: 50px;
        border-right: 1px solid #e0e0e0;
    }}

    .st-key-pill-container-{key} .st-key-pill-option-inactive-{key} {{
        color: #333;
        border-top-right-radius: 50px;
        border-bottom-right-radius: 50px;
        
    }}

    .st-key-pill-container-{key} .st-key-pill-option-active-{key} button {{
        width: 100%;
        background-color: {background_right};
        border-top-left-radius: 50px;
        border-bottom-left-radius: 50px;
        transition: background-color .5s ease;
    }}

    .st-key-pill-container-{key} .st-key-pill-option-inactive-{key} button {{
        width: 100%;
        background-color: {background_left};
        color: #333;
        border-top-right-radius: 50px;
        border-bottom-right-radius: 50px;
        transition: background-color .5s ease;
    }}
    
    .st-key-pill-container-{key} .st-key-pill-option-inactive-{key} button p {{
        font-size: 12px;
    }}
    
    .st-key-pill-container-{key} .st-key-pill-option-active-{key} button p {{
        font-size: 12px;
    }}
    

    .st-key-pill-option-{key}:hover {{
        opacity: 0.9;
    }}

    .st-key-pill-left-{key} {{
        border-top-left-radius: 50px;
        border-bottom-left-radius: 50px;
        border-right: 1px solid #e0e0e0;
    }}

    .st-key-pill-right-{key} {{
        border-top-right-radius: 50px;
        border-bottom-right-radius: 50px;
    }}
    </style>
    """, unsafe_allow_html=True)

    pill_container = st.container(key=f"pill-container-{key}")

    pill_container.button(option_left, key=left_class, on_click=on_click_left)

    pill_container.button(option_right, key=right_class, on_click=on_click_right)


