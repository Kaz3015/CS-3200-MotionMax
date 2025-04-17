import streamlit as st
import requests
import pandas as pd

st.title("Marketing Channel Performance")
st.subheader("Total Customers Acquired by Channel")

# Sample data (used if API fails)
sample_performance = [
    {"channel_name": "Instagram", "total_customers_acquired": 1250},
    {"channel_name": "Facebook", "total_customers_acquired": 950},
    {"channel_name": "TikTok", "total_customers_acquired": 2100},
    {"channel_name": "Google Ads", "total_customers_acquired": 780}
]

# Use sample data initially
performance_data = sample_performance

# Convert to DataFrame for easier manipulation
df = pd.DataFrame(performance_data)

#get and display the bar chart using bar chart with streamlit
st.bar_chart(
    #set channel name as the index
    df.set_index('channel_name')['total_customers_acquired'],
    #chart goes the whole width of the window
    use_container_width=True
)

#show the data in a table below the chart
st.subheader("Channel Performance Data")

st.dataframe(
    #sort the dataframe in descending order by performance so the most effective channels appear
    df.sort_values(by='total_customers_acquired', ascending=False),
    #customize the appearance and the label of the columns in the table
    column_config={
        #rename the channel name column to a more user-friendly label
        "channel_name": "Marketing Channel",
        #define the 'total_customers_aquired' column is displayed
        "total_customers_acquired": st.column_config.NumberColumn(
            "Total Customers Acquired",
            format="%d",
        )
    },
    #do not display the default index column from the DF
    hide_index=True,
    #let the table to expand and use the full width of the app window
    use_container_width=True
)

# Function to get marketing performance data - moved to the end as requested
def get_marketing_performance():
    #make the API endpoint url to get marketing channel performance
    url = "http://api:4000/marketing_channel_performance"
    #send a get request to the API
    response = requests.get(url)
    #if the request is successful return the JSON data
    if response.status_code == 200:
        return response.json()
    else:
        return sample_performance

# Make the API call at the end
api_performance_data = get_marketing_performance()