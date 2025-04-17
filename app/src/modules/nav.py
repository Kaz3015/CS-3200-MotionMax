# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

# This file has function to add certain functionality to the left side bar of the app

import streamlit as st


#### ------------------------ General ------------------------
def HomeNav():
    st.sidebar.page_link("Home.py", label="Home", icon="🏠")


def AboutPageNav():
    st.sidebar.page_link("pages/30_About.py", label="About", icon="🧠")

def SalesPageNav():
    st.sidebar.page_link("feedback_survey.py", label="Feedback Survey", icon="📝")
    st.sidebar.page_link("feedback_survey_output.py", label="Survey Output", icon="📄")
    st.sidebar.page_link("CAC_LTV.py", label="CAC vs LTV", icon="💸")
    st.sidebar.page_link("sales_report.py", label="Sales Report", icon="📊")
    st.sidebar.page_link("user_survey.py", label="User Survey", icon="👤")
    st.sidebar.page_link("user_survey_output.py", label="User Survey Output", icon="📈")



#### ------------------------ System admin Role ------------------------
def AdminPageNav():
    st.sidebar.page_link("pages/20_Admin_Home.py", label="System admin", icon="🖥️")
    st.sidebar.page_link(
        "pages/21_ML_Model_Mgmt.py", label="ML Model Management", icon="🏢"
    )


# --------------------------------Links Function -----------------------------------------------
def SideBarLinks(show_home=False):
    """
    This function handles adding links to the sidebar of the app based upon the logged-in user's role, which was put in the streamlit session_state object when logging in.
    """

    # add a logo to the sidebar always
    st.sidebar.image("assets/logo.png", width=300)

    # If there is no logged in user, redirect to the Home (Landing) page
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")

    if show_home:
        # Show the Home page link (the landing page)
        HomeNav()

    # Show the other page navigators depending on the users' role.
    if st.session_state["authenticated"]:

        # Show World Bank Link and Map Demo Link if the user is a political strategy advisor role.
        if st.session_state["role"] == "trainer":
            st.sidebar.page_link(
                "pages/Trainer_info_page.py", label="Trainer informatics", icon="👤"
            )
            st.sidebar.page_link(
                "pages/Trainer_form.py", label="User informatics", icon="📝"
            )
            st.sidebar.page_link(
                "pages/Client_info_page.py", label="Client informatics", icon="🏋️"
            )

        # If the user role is usaid worker, show the Api Testing page
        if st.session_state["role"] == "salesperson":
            SalesPageNav()


        # If the user is an administrator, give them access to the administrator pages
        if st.session_state["role"] == "administrator":
            AdminPageNav()

    # Always show the About page at the bottom of the list of links
    AboutPageNav()

    if st.session_state["authenticated"]:
        # Always show a logout button if there is a logged in user
        if st.sidebar.button("Logout"):
            del st.session_state["role"]
            del st.session_state["authenticated"]
            st.switch_page("Home.py")
