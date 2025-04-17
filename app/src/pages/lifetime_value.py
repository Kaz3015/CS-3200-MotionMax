import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import streamlit as st

def plot_customer_lifetime_value(data, title="Customer Lifetime Value Analysis"):
    """
    Creates a curved line chart showing customer lifetime value over time.
    """
    #get the lifetime value from data
    ltv = data['lifetime_value']

    #make a times range
    years = np.linspace(0, 5, 100)

    #create a bell-shaped curve that shows the Lifetime Value changing overtime
    values = ltv * np.exp(-((years - 2.5) ** 2) / 2)

    #make the plot
    fig, ax = plt.subplots(figsize=(10, 6))

    #make the curve
    ax.plot(years, values, 'b-', linewidth=2)

    #this fills the specific areas under the curve to shows phases of the Lifetime Value
    ax.fill_between(years[years <= 1.5], 0, values[years <= 1.5], alpha=0.3, label='CLV 1', color='lightblue')
    ax.fill_between(years[(years > 1.5) & (years < 3.5)], 0, values[(years > 1.5) & (years < 3.5)], alpha=0.3,
                    label='CLV 2', color='royalblue')
    ax.fill_between(years[years >= 3.5], 0, values[years >= 3.5], alpha=0.3, label='CLV 3', color='lightblue')

    #this makes the text labels in the areas
    ax.text(0.75, ltv/4, 'CLV 1', fontsize=12)
    ax.text(2.5, ltv/2, 'CLV 2', fontsize=14)
    ax.text(4.25, ltv/4, 'CLV 3', fontsize=12)

    #this makes the axis labels and title
    ax.set_xlabel('Time (Years)', fontsize=12)
    ax.set_ylabel('Customer Value ($)', fontsize=12)
    ax.set_title(title, fontsize=14)

    #this gets rid of the top and right spines to clean up the chart borders
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    #show the plot
    st.pyplot(fig)

    #shows key performance metrics below the chart
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Customer Lifetime Value", f"${ltv:.2f}")

    with col2:
        # Calculate the area under the curve (approximate total value)
        total_value = np.trapz(values, years)
        st.metric("Estimated Total Value", f"${total_value:.2f}")

st.title("MotionMAX Analytics")
st.subheader("Customer Lifetime Value Analysis")

def fetch_data():
    #get the API endpoint for submitting the CLV
    url = "http://api:4000/s/CLV"
    #send a get request to the API
    response = requests.get(url, timeout=10)
    #if the request is successful return the JSON data
    if response.status_code == 200:
        return response.json()

# Sample data to test the visualization without API
sample_data = {
    "lifetime_value": 750.25
}

#try to get data from API first
data = fetch_data()
if data:
    plot_customer_lifetime_value(data)

else:
    # On initial load, use sample data
    plot_customer_lifetime_value(sample_data)