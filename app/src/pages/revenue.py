import streamlit as st
import pandas as pd
import datetime
import requests

url = "http://api:4000/s/revenue"
#send a get request to the API
response = requests.get(url)
#if the request is successful return the JSON data
if response.status_code == 200:
    data = response.json()

st.title("MotionMAX Revenue")

# Create sample revenue data
#Make a a list of the past 6 months in "Abbreviated Month Year" format
months = [(datetime.datetime.now() - datetime.timedelta(days=30*i)).strftime("%b %Y")
          for i in range(6, 0, -1)
          ]
revenue_values = [1.2, 1.5, 1.8, 1.6, 1.9, 2.2]

#combine the months and revenues into a DF for visualization
revenue_data = pd.DataFrame({
    'month': months,
    'revenue': revenue_values
})

#set the month column as the index so it is on the x-axis
revenue_data.set_index('month', inplace=True)

#make the line chart
st.line_chart(revenue_data)

#see if the revenue value exsists
if len(revenue_values) > 0:
    #grab the the most recent revenue value of the last in the list
    current_revenue = revenue_values[-1]
    #use streamlit metric and show a compact summary value at the top
    st.metric("Current Revenue", f"{current_revenue:.2f}x")



