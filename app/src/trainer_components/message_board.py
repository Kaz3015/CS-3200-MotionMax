import streamlit as st
import datetime
import requests
import logging


def render_message_board():
    # Add custom CSS for scrollable container
    st.markdown("""
    <style>
    .scrollable-messages {
        max-height: 300px;
        overflow-y: auto;
        padding-right: 10px;
        max-width: 200px;
        background-color: white;
    }
    </style>
    """, unsafe_allow_html=True)

    # Fetch messages
    messages = requests.get(f'http://api:4000/t/{st.session_state["user_id"]}/messageBoard').json()
    messageBoard = st.container(key="msgBoard")


    # Create title and container
    messageBoard.subheader("Message Board")

    # Create a scrollable container for messages
    messageBoard.markdown('<div class="scrollable-messages">', unsafe_allow_html=True)

    # Display each message
    for msg in messages:
        name = msg['first_Name'] + " " + msg["last_name"]
        user_id = msg["user_id"]
        role = st.session_state['role']
        is_user = (user_id == st.session_state['user_id'])
        is_trainer = (is_user and role == 'Fitness Trainer')

        display_message(name, msg["content"], msg["created_at"], is_user, is_trainer)

    # Close the scrollable container
    messageBoard.markdown('</div>', unsafe_allow_html=True)

    # Add a simple message input
    with st.form("message_form", clear_on_submit=True):
        message = st.text_area("New message", height=100)
        submitted = st.form_submit_button("Send")

        if submitted and message:
            # Send message to API
            response = requests.post(
                f'http://api:4000/t/{st.session_state["trainer_id"]}/messageBoard/{st.session_state["user_id"]}',
                json={"content": message}
            )
            if response.status_code == 200:
                st.success("Message sent!")
            else:
                st.error("Failed to send message.")


def display_message(name, content, date, is_user=False, is_trainer=False):
    """
    Display a simplified message bubble.
    """
    try:
        # Parse date
        date_obj = datetime.datetime.strptime(date, "%a, %d %b %Y %H:%M:%S GMT")
        date_str = date_obj.strftime("%b %d, %H:%M")
    except:
        date_str = date  # Use as is if parsing fails

    # Message styling
    if is_trainer:
        bg_color = "#FFF8E1"
        icon = "👨‍🏫 "
    elif is_user:
        bg_color = "#E8F5E9"
        icon = ""
    else:
        bg_color = "#F5F5F5"
        icon = ""

    # Alignment for user vs others
    if is_user:
        alignment = "right"
        margin = "margin-left: 20%;"
    else:
        alignment = "left"
        margin = "margin-right: 20%;"

    # Css for message bubble
    st.markdown(f"""
    <div style="
        background-color: {bg_color};
        border-radius: 12px;
        padding: 10px 14px;
        margin-bottom: 8px;
        {margin}
        text-align: {alignment};
    ">
        <div style="font-weight: bold; font-size: 0.9em; margin-bottom: 4px;">
            {icon}{name} <span style="font-weight: normal; color: #666; font-size: 0.8em;">{date_str}</span>
        </div>
        <div style="word-wrap: break-word;">{content}</div>
    </div>
    """, unsafe_allow_html=True)