import streamlit as st

def init_navigation():
    """
    Initialize the navigation bar for the workout app.
    This should be imported and called at the top of each page.
    """
    # Add logo or app title to the sidebar
    st.sidebar.title("Workout App")
    st.sidebar.markdown("---")

    # Main navigation links
    st.sidebar.header("Analytics")

    # Marketing section
    marketing_expander = st.sidebar.expander("Marketing", expanded=False)
    with marketing_expander:
        st.page_link("marketing_channel.py", label="Marketing Channels", icon="📊")
        st.page_link("marketing_channel_performance.py", label="Channel Performance", icon="📈")
        st.page_link("marketing_channels.py", label="All Channels", icon="🔍")

    # User data section
    user_expander = st.sidebar.expander("User Data", expanded=False)
    with user_expander:
        st.page_link("user_survey.py", label="User Survey", icon="📝")
        st.page_link("user_survey_output.py", label="Survey Results", icon="📋")
        st.page_link("subscriber_count.py", label="Subscriber Count", icon="👥")

    # Financial data section
    financial_expander = st.sidebar.expander("Financial Data", expanded=False)
    with financial_expander:
        st.page_link("CA_cost.py", label="Customer Acquisition Cost", icon="💰")
        st.page_link("lifetime_value.py", label="Customer Lifetime Value", icon="⏱️")
        st.page_link("revenue.py", label="Revenue Analysis", icon="💵")

    # Feedback section
    feedback_expander = st.sidebar.expander("Feedback", expanded=False)
    with feedback_expander:
        st.page_link("feedback_survey.py", label="Feedback Survey", icon="🔄")
        st.page_link("feedback_survey_output.py", label="Feedback Results", icon="📊")

    st.sidebar.markdown("---")

    # Settings and help
    st.sidebar.header("Settings")
    if st.sidebar.button("Logout", use_container_width=True):
        # Handle logout logic here (if you have authentication)
        st.session_state.clear()
        st.experimental_rerun()

    # Help and about
    st.sidebar.info("This Workout App Dashboard provides analytics and insights about your marketing channels, user data, and financial metrics.")

def show_page_header(title, description=None):
    """
    Displays a consistent header for each page
    """
    st.title(title)
    if description:
        st.markdown(description)
    st.markdown("---")