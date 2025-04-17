import streamlit as st
import requests

# Title
st.title("Different Marketing Channels Used")

# Sample data (used if API fails)
sample_channels = [
    {"channel_id": 1, "channel_name": "Instagram", "description": "Displays photos and videos about the application."},
    {"channel_id": 2, "channel_name": "Facebook", "description": "Displays photos and videos about the application."},
    {"channel_id": 3, "channel_name": "TikTok", "description": "Short-form videos about the application."},
    {"channel_id": 4, "channel_name": "Google Ads", "description": "Pay-per-click advertising on Google using photos and videos."}
]

#if it is available display the first channel
if len(sample_channels) > 0:
    #get the first channel object
    channel = sample_channels[0]
    with st.container():
        #use the expander so users can show and hide the content
        with st.expander(f"Marketing Channel 1: {channel['channel_name']}", expanded=True):
            #give the description in the expander
            st.write(channel['description'])
    st.write("")

#if it is available display the second channel
if len(sample_channels) > 1:
    #get the channel object
    channel = sample_channels[1]
    with st.container():
        #use the expander so users can show and hide the content
        with st.expander(f"Marketing Channel 2: {channel['channel_name']}", expanded=True):
            #give the description in the expander
            st.write(channel['description'])
    st.write("")

#if it is available display the third channel
if len(sample_channels) > 2:
    #get the channel object
    channel = sample_channels[2]
    with st.container():
        #use the expander so users can show and hide the content
        with st.expander(f"Marketing Channel 3: {channel['channel_name']}", expanded=True):
            #give the description in the expander
            st.write(channel['description'])
    st.write("")

#if it is available display the fourth channel
if len(sample_channels) > 3:
    #get the channel object
    channel = sample_channels[3]
    with st.container():
        #use the expander so users can show and hide the content
        with st.expander(f"Marketing Channel 4: {channel['channel_name']}", expanded=True):
            #give the description in the expander
            st.write(channel['description'])
    st.write("")

def get_marketing_channels():
    #make the API endpoint url to get marketing channels used
    url = "http://api:4000/marketing_channels"
    #send a get request to the API
    response = requests.get(url)
    #if the request is successful return the JSON data
    if response.status_code == 200:
        return response.json()
    else:
        return sample_channels


# Make the API call at the end
api_channels = get_marketing_channels()