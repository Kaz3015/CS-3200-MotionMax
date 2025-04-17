import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")
st.title("All Support Tickets")
SideBarLinks()

if "resolved_ticket_id" not in st.session_state:
    st.session_state["resolved_ticket_id"] = None

url = "http://web-api:4000/a/support"

try:
    response = requests.get(url)
    if response.status_code == 200:
        tickets = response.json()
        if tickets:
            df = pd.DataFrame(tickets)
            df.fillna("N/A", inplace=True)
            st.dataframe(df)
        else:
            st.info("No support tickets found.")
    else:
        st.error(f"Error fetching tickets: {response.text}")
except Exception as e:
    st.error(f"Failed to connect to API: {e}")


if st.session_state["resolved_ticket_id"]:
    st.success(f"Ticket {st.session_state['resolved_ticket_id']} resolved successfully!")
    st.session_state["resolved_ticket_id"] = None

st.markdown("---")
st.subheader("Resolve a Support Ticket")

ticket_id = st.number_input("Enter Ticket ID to resolve", min_value=1, step=1)
admin_id  = st.number_input("Enter Your Admin ID",  min_value=1, step=1)

if st.button("Resolve Ticket", use_container_width=True, type="primary"):
    try:
        payload = {"admin_id": admin_id}
        headers = {"Content-Type": "application/json"}
        res = requests.put(f"{url}/{ticket_id}", json=payload, headers=headers)

        if res.status_code == 200:
            st.session_state["resolved_ticket_id"] = ticket_id

        elif res.status_code == 409:
            st.warning(f"Ticket {ticket_id} is already closed and cannot be resolved again.")

        elif res.status_code == 404:
            st.error(f"Ticket {ticket_id} not found.")
        else:
            st.error(f"Error resolving ticket: {res.text}")

    except Exception as e:
        st.error(f"Failed to connect to API: {e}")
