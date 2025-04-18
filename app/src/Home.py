##################################################
# This is the main/entry-point file for the 
# sample application for your project
##################################################

# Set up basic logging infrastructure
import logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# import the main streamlit library as well
# as SideBarLinks function from src/modules folder
import streamlit as st
from modules.nav import SideBarLinks
#from pages.navigation_sales import SideBarLinks
import requests

# streamlit supports reguarl and wide layout (how the controls
# are organized/displayed on the screen).
st.set_page_config(layout = 'wide')

# If a user is at this page, we assume they are not 
# authenticated.  So we change the 'authenticated' value
# in the streamlit session_state to false. 
st.session_state['authenticated'] = False

# Use the SideBarLinks function from src/modules/nav.py to control
# the links displayed on the left-side panel. 
# IMPORTANT: ensure src/.streamlit/config.toml sets
# showSidebarNavigation = false in the [client] section
SideBarLinks(show_home=True)

# Maintenance stuff
try:
    response = requests.get("http://web-api:4000/a/maintenance")
    response.raise_for_status()
    maintenance_mode = response.json().get("maintenance_mode", False)
except Exception as e:
    maintenance_mode = False

if maintenance_mode:
    st.warning("The app is currently under maintenance. Only system admins may log in. We apologize for the inconvience")


# ***************************************************
#    The major content of this page
# ***************************************************

# set the title of the page and provide a simple prompt. 
logger.info("Loading the Home page of the app")
st.title('motionMAX')
st.write('\n\n')
st.write('### HI! As which user would you like to log in?')

# For each of the user personas for which we are implementing
# functionality, we put a button on the screen that the user 
# can click to MIMIC logging in as that mock user. 

if not maintenance_mode:
    if st.button("Act as John, a Fitness Trainer",
                 type='primary',
                 use_container_width=True):
        # when user clicks the button, they are now considered authenticated
        st.session_state['authenticated'] = True
        # we set the role of the current user
        st.session_state['role'] = 'trainer'
        # we add the first name of the user (so it can be displayed on
        # subsequent pages).
        st.session_state['first_name'] = 'John'
        st.session_state['last_name'] = 'Smith'
        # finally, we ask streamlit to switch to another page, in this case, the
        # landing page for this particular user type
        st.session_state['user_id'] = requests.get('http://api:4000/t').json()['user_id']
        st.session_state['trainer_id'] = st.session_state['user_id']
        st.session_state['subscriber_id'] = requests.get('http://api:4000/t').json()['subscriber_id']
        st.session_state['doubleClicked'] = False
        st.session_state['form'] = "workout form"
        st.session_state['used_ingredients'] = []
        st.session_state['ingredient names'] = []
        st.session_state['existing recipe'] = False
        st.session_state['recipe_title'] = None
        st.session_state['workout_loaded'] = False
        st.session_state['added_ingredients'] = []
        st.session_state['recipe_id'] = None
        st.session_state['workout_id'] = None
        logger.info(f"Logging in as Fitness Trainer Persona with role as {st.session_state['role']} and authenticated as {st.session_state['authenticated']}")
        logger.info(f"User ID: {st.session_state['user_id']}")
        logger.info(f"Subscriber ID: {st.session_state['subscriber_id']}")
        st.switch_page('pages/Trainer_info_page.py')


    if st.button('Act as Sam, a workout client',
                type = 'primary',
                use_container_width=True):
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'client'
        
        st.session_state['first_name'] = 'Sam'
        st.session_state['last_name'] = 'Johnson'
        st.session_state['user_id'] = requests.get(f"http://api:4000/c/{st.session_state['first_name']}/{st.session_state['last_name']}/").json()['user_id']
        st.switch_page('pages/User_Information.py')

if st.button('Act as Jameis, System Administrator',
            type = 'primary', 
            use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'administrator'
    st.session_state['first_name'] = 'SysAdmin'
    st.switch_page('pages/20_Admin_Home.py')

if not maintenance_mode:
    if st.button('Act as Tyler, a Sales Employee',
                 type = 'primary',
                 use_container_width=True):
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'salesperson'
        st.session_state['user_id'] = 2
        st.switch_page('pages/CAC_LTV.py')






