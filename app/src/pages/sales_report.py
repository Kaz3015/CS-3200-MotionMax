from functools import reduce
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import logging
import altair as alt
from modules.nav import SideBarLinks
SideBarLinks(show_home=True)


def get_subscriber_data():
    # get the API endpoint for submitting the subscriber count
    url = "http://api:4000/s/subscriber_count"
    # send a get request to the API
    response = requests.get(url).json()

    return response

row1 = st.columns(2)
# Get the data from the API
with row1[0]:
    st.title("Monthly Subscribers")

    subscriber_data = get_subscriber_data()

    # Process and display the data
    if subscriber_data:
        # Convert the API response to a pandas DataFrame
        df = pd.DataFrame(subscriber_data)
        if not df.empty:
            #sum the month and subscriber count
            monthly_data = df.groupby('month', as_index=False)['subscriber_count'].sum()
            #turn the month and the subsciber count as an int
            monthly_data['month'] = monthly_data['month'].astype(int)
            monthly_data['subscriber_count'] = monthly_data['subscriber_count'].astype(int)

            # Display the line chart
            chart = (
                alt.Chart(monthly_data)
                .mark_line(point=True)
                .encode(
                    x=alt.X('month:Q',
                            title="Month",
                            axis=alt.Axis(format="d", tickMinStep=1)),
                    y=alt.Y('subscriber_count:Q',
                            title="Subscribers",
                            axis=alt.Axis(format="d", tickMinStep=1)),
                )
                .properties(width=700, height=400)
            )


            st.altair_chart(chart, use_container_width=True)

            #show current total subscribers
            total_subscribers = df['subscriber_count'].sum()
            st.metric("Total Subscribers", f"{total_subscribers:,}")

get_subscriber_data()

with row1[1]:
    # get the API endpoint for submitting the revenue
    url = "http://api:4000/s/revenue"
# send a get request to the API
response = requests.get(url)
# if the request is successful return the JSON data
if response.status_code == 200:
    data = response.json()

st.title("MotionMAX Revenue")

df = pd.DataFrame(data)
df
# make sure month is numeric
df['month'] = pd.to_numeric(df['month'])

# define month mapping
month_map = {
    1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr",
    5: "May", 6: "Jun", 7: "Jul", 8: "Aug",
    9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
}

# add month names
df = df.sort_values(by='month', ascending=True)
df['month'] = df['month'].map(month_map)
#list the month map value in order
order = list(month_map.values())
#categorize the data
df['month'] = pd.Categorical(df['month'], categories=order, ordered=True)

# Convert revenue to numeric
df['motion_max_revenue'] = pd.to_numeric(df['motion_max_revenue'])

# Make the line chart
sorted = df.sort_values('month')
st.line_chart(sorted.set_index('month')['motion_max_revenue'])


