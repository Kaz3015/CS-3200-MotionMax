import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# Function to get subscriber data from API
def get_subscriber_data():
    try:
        url = "http://api:4000/subscriber_count"
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()

# Get the data from the API
subscriber_data = get_subscriber_data()

# Process and display the data
if subscriber_data:
    # Convert the API response to a pandas DataFrame
    df = pd.DataFrame(subscriber_data)

    if not df.empty:
        # Make sure the date column is properly formatted
        df['date'] = pd.to_datetime(df['date'])

        # Extract month from date for monthly grouping
        df['month'] = df['date'].dt.strftime('%Y-%m')

        # Group by month and sum subscribers
        monthly_data = df.groupby('month')['subscribers'].sum().reset_index()

        # Set month as index for the chart
        monthly_data.set_index('month', inplace=True)

        # Display the line chart
        st.line_chart(monthly_data)

        # Show current total subscribers
        total_subscribers = df['subscribers'].sum()
        st.metric("Total Subscribers", f"{total_subscribers:,}")



'''

import streamlit as st
import pandas as pd
import requests

st.title("MotionMAX Subscriber Count")

# Sample data to use if API fails
sample_dates = [f"2025-04-{i:02d}" for i in range(1, 16)]
sample_subscribers = [5, 8, 12, 15, 18, 20, 22, 25, 28, 30, 32, 35, 38, 40, 42]

#put the date and the subscriber count into a df
sample_data = pd.DataFrame({
    'date': sample_dates,
    'subscribers': sample_subscribers
})

#set the 'date' column as the index so it can be ued as the x-axis of the line chart
sample_data.set_index('date', inplace=True)

#show the subscriber count line chart
st.line_chart(sample_data)

#make the API endpoint url to get marketing channels used
url = "http://api:4000/s/subscriber_count"
#send a get request to the API
response = requests.get(url)
'''