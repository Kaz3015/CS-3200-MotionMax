import requests
import streamlit as st

with st.form("MotionMAX App Feedback"):
    # how did you find our app question
    st.subheader("How did you find our app:")
    find_app = st.text_input("Enter:", placeholder="Social media, friend recommendation, etc.")

    # how are you enjoying our app question rating using star feedback
    st.subheader("How are you enjoying our app:")
    enjoyment_stars = st.feedback("stars")

    sentiment_mapping = ["one", "two", "three", "four", "five"]

    # turn star rating to text for data storage
    enjoyment = None
    if enjoyment_stars is not None:
        enjoyment = f"{sentiment_mapping[enjoyment_stars]} star(s)"
        st.markdown(f"You selected {enjoyment}.")

    # are there any improvements you would like question
    st.subheader("Are there any improvement you would like:")
    improvements = st.text_area("Enter:", placeholder="Suggestions for improvements...", height=100)

    #are there similar apps that you use question
    st.subheader("Are there any other similar apps you use:")
    similar_apps = st.text_input("Enter:", placeholder="Names of other fitness apps you use...")

    #what is the most useful feature question
    st.subheader("What feature do you find most useful:")
    useful_feature = st.text_input("Enter:", placeholder="Your favorite feature...")

    if st.form_submit_button("Submit"):
        if find_app and enjoyment_stars is not None and improvements and similar_apps and useful_feature:
            data = {
                "user_id": st.session_state.get("user_id", "unknown"),
                "app_discovery": find_app,
                "app_enjoyment": enjoyment,
                "improvement_suggestions": improvements,
                "similar_apps": similar_apps,
                "most_useful_feature": useful_feature
            }

            url = "http://api:4000/s/feedback_survey"
            response = requests.post(
                 url,
                 json=data,
            )

            st.success("Thank you for your feedback! We appreciate your input.")








