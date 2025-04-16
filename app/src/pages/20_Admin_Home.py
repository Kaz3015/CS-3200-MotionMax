import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('System admin Home Page')
st.session_state['search'] = False
st.session_state['selected_user'] = None

if st.button('Update ML Models', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/21_ML_Model_Mgmt.py')

if st.button('Submit Support Ticket',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/22_Admin_Support_tickets.py')

if st.button("View All Support Tickets",
             type='primary',
             use_container_width=True):
  st.switch_page("pages/24_View_Support_Tickets.py")

if st.button("Search and Edit User Profiles",
             type='primary',
             use_container_width=True):
  st.switch_page("pages/25_View_User_Profile.py")


