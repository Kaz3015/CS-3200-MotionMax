import streamlit as st
import requests
import pandas as pd

st.set_page_config(layout="wide")
st.title("All Support Tickets")

url = "http://web-api:4000/a/support"  # ← change to api:4000 if needed

try:
    response = requests.get(url)
    if response.status_code == 200:
        tickets = response.json()
        if tickets:
            df = pd.DataFrame(tickets)
            st.dataframe(df)
        else:
            st.info("No support tickets found.")
    else:
        st.error(f"Error: {response.text}")
except Exception as e:
    st.error(f"Failed to connect: {e}")
