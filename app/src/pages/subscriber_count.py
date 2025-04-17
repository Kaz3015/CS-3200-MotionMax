import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
from datetime import datetime

# Function to get subscriber data from API
def get_subscriber_data():
    url = "http://api:4000/subscriber_count"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
row1 = st.columns(2)
row2 = st.columns
# Get the data from the API
with row1[0]:
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
with row1[1]:
    url = "http://api:4000/s/revenue"
    # send a get request to the API
    response = requests.get(url)
    # if the request is successful return the JSON data
    if response.status_code == 200:
        data = response.json()

    st.title("MotionMAX Revenue")

    # Create sample revenue data
    # Make a a list of the past 6 months in "Abbreviated Month Year" format
    months = [(datetime.datetime.now() - datetime.timedelta(days=30 * i)).strftime("%b %Y")
              for i in range(6, 0, -1)
              ]
    revenue_values = [1.2, 1.5, 1.8, 1.6, 1.9, 2.2]

    # combine the months and revenues into a DF for visualization
    revenue_data = pd.DataFrame({
        'month': months,
        'revenue': revenue_values
    })

    # set the month column as the index so it is on the x-axis
    revenue_data.set_index('month', inplace=True)

    # make the line chart
    st.line_chart(revenue_data)

    # see if the revenue value exsists
    if len(revenue_values) > 0:
        # grab the the most recent revenue value of the last in the list
        current_revenue = revenue_values[-1]
        # use streamlit metric and show a compact summary value at the top
        st.metric("Current Revenue", f"{current_revenue:.2f}x")
with row2[0]:
    def plot_customer_acquisition_costs(data, title="Monthly Customer Acquisition Costs"):
        """
        Creates a bar chart showing monthly customer acquisition costs.
        """
        # makes datafram
        df = pd.DataFrame(data)

        # finds the total cost
        total_cost = df['cost'].sum()

        # show the Total Customer Acquisition Cost
        st.write(f"Total Customer Acquisition Cost: ${total_cost:.2f}")

        # make the bar chart
        fig, ax = plt.subplots(figsize=(10, 6))

        # actually creates the bars
        bars = ax.bar(
            df['month'],
            df['cost'],
            color='black',
            width=0.6,
            edgecolor='white',
            linewidth=0.7
        )

        # making the labels and title
        ax.set_xlabel('Months', fontsize=12)
        ax.set_ylabel('Cost ($)', fontsize=12, rotation=90)

        # I wanted to create a second y-axis label for "Number of Customers" because num customers ties into the
        # customer aquisition cost per month
        ax2 = ax.twinx()
        ax2.set_ylabel('Number of Customers', fontsize=12, rotation=90)
        ax2.set_yticks([])  # Hide the ticks

        # makes the title of the bar chart
        plt.title(title, fontsize=14)

        # this makes the grid lines for the chart
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()

        # this actually shows the plot
        st.pyplot(fig)

        # show the information in columns
        col1, col2, col3 = st.columns(3)

        # shows the customer aquisition cost in the first column
        with col1:
            # find the average value in the cost column
            avg_cost = df['cost'].mean()
            # displays the average cost using streamlit
            st.metric("Average CAC", f"${avg_cost:.2f}")

        # shows the total number of customer in the second columns
        with col2:
            # find the total customers if the column is there
            total_customers = df['customers'].sum() if 'customers' in df.columns else 0
            # show the total customers using streamlit
            st.metric("Total Customers", f"{total_customers}")

        # shows the max monthly Customer Aquisition Costs in the third column
        with col3:
            # finds the max value in the cost column
            max_cost = df['cost'].max()
            # show the max cost using streamlit
            st.metric("Max Monthly CAC", f"${max_cost:.2f}")


    st.title("MotionMAX Analytics")
    st.subheader("Customer Acquisition Cost Analysis")


    def fetch_data():
        # make the API endpoint url to get Customer Acquisition cost data
        url = "http://api:4000/s/CA_cost"
        # sned a get request to the API
        response = requests.get(url, timeout=10)
        # if the request is successful return the JSON data
        if response.status_code == 200:
            return response.json()
        return None


    # Sample data to test the visualization without API
    sample_data = [
        {"month": "Jan 2023", "cost": 120.50, "customers": 25, "budget": 3000},
        {"month": "Feb 2023", "cost": 95.30, "customers": 31, "budget": 2900},
        {"month": "Mar 2023", "cost": 150.80, "customers": 20, "budget": 3100},
        {"month": "Apr 2023", "cost": 85.20, "customers": 36, "budget": 3050},
        {"month": "May 2023", "cost": 110.60, "customers": 28, "budget": 3200},
        {"month": "Jun 2023", "cost": 75.40, "customers": 40, "budget": 3000},
        {"month": "Jul 2023", "cost": 135.90, "customers": 22, "budget": 3100},
        {"month": "Aug 2023", "cost": 102.30, "customers": 30, "budget": 3050},
        {"month": "Sep 2023", "cost": 89.70, "customers": 34, "budget": 3000},
        {"month": "Oct 2023", "cost": 118.40, "customers": 26, "budget": 3100},
        {"month": "Nov 2023", "cost": 105.20, "customers": 29, "budget": 3050},
        {"month": "Dec 2023", "cost": 130.70, "customers": 24, "budget": 3150}
    ]

    # try to get data from API first
    data = fetch_data()
    if data:
        plot_customer_acquisition_costs(data)
    else:
        # On initial load, use sample data
        plot_customer_acquisition_costs(sample_data)
with row2[1]:
    def plot_customer_lifetime_value(data, title="Customer Lifetime Value Analysis"):
        """
        Creates a curved line chart showing customer lifetime value over time.
        """
        # get the lifetime value from data
        ltv = data['lifetime_value']

        # make a times range
        years = np.linspace(0, 5, 100)

        # create a bell-shaped curve that shows the Lifetime Value changing overtime
        values = ltv * np.exp(-((years - 2.5) ** 2) / 2)

        # make the plot
        fig, ax = plt.subplots(figsize=(10, 6))

        # make the curve
        ax.plot(years, values, 'b-', linewidth=2)

        # this fills the specific areas under the curve to shows phases of the Lifetime Value
        ax.fill_between(years[years <= 1.5], 0, values[years <= 1.5], alpha=0.3, label='CLV 1', color='lightblue')
        ax.fill_between(years[(years > 1.5) & (years < 3.5)], 0, values[(years > 1.5) & (years < 3.5)], alpha=0.3,
                        label='CLV 2', color='royalblue')
        ax.fill_between(years[years >= 3.5], 0, values[years >= 3.5], alpha=0.3, label='CLV 3', color='lightblue')

        # this makes the text labels in the areas
        ax.text(0.75, ltv / 4, 'CLV 1', fontsize=12)
        ax.text(2.5, ltv / 2, 'CLV 2', fontsize=14)
        ax.text(4.25, ltv / 4, 'CLV 3', fontsize=12)

        # this makes the axis labels and title
        ax.set_xlabel('Time (Years)', fontsize=12)
        ax.set_ylabel('Customer Value ($)', fontsize=12)
        ax.set_title(title, fontsize=14)

        # this gets rid of the top and right spines to clean up the chart borders
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # show the plot
        st.pyplot(fig)

        # shows key performance metrics below the chart
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
        # get the API endpoint for submitting the CLV
        url = "http://api:4000/s/CLV"
        # send a get request to the API
        response = requests.get(url, timeout=10)
        # if the request is successful return the JSON data
        if response.status_code == 200:
            return response.json()


    # Sample data to test the visualization without API
    sample_data = {
        "lifetime_value": 750.25
    }

    # try to get data from API first
    data = fetch_data()
    if data:
        plot_customer_lifetime_value(data)

    else:
        # On initial load, use sample data
        plot_customer_lifetime_value(sample_data)




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