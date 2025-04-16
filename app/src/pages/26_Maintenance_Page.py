import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")
st.title("Admin: Maintenance")
SideBarLinks()


response = requests.get("http://web-api:4000/a/maintenance")
response.raise_for_status()
maintenance_mode = response.json().get("maintenance_mode", False)


toggle = st.toggle("Enable Maintenance Mode", value=maintenance_mode)

if toggle != maintenance_mode:
    put_response = requests.put("http://web-api:4000/a/maintenance", json={"maintenance_mode": toggle})
    put_response.raise_for_status()
    st.success("Maintenance mode updated!")
    st.rerun()

