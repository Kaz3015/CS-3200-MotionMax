from functools import reduce
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import logging
from modules.nav import SideBarLinks

SideBarLinks(show_home=True)

row1 = st.columns(2)
with row1[0]:
    def plot_customer_acquisition_costs(data, title="Monthly Customer Acquisition Costs"):
        """
        Creates a bar chart showing monthly customer acquisition costs.
        """
        # makes dataframe
        df = pd.DataFrame(data)
        df['budget'] = pd.to_numeric(df['budget'])
        df['customers'] = pd.to_numeric(df['customers'])
        df['cost'] = pd.to_numeric(df['cost'])

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

    # try to get data from API first
    logger = logging.getLogger(__name__)

    data = fetch_data()
    logger.info(f"Data {data}")

    if data:
        plot_customer_acquisition_costs(data)

with row1[1]:
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
        url = "http://api:4000/s/subscriber_count"
        # send a get request to the API
        response = requests.get(url, timeout=10)
        sub_data = None
        # if the request is successful return the JSON data
        if response.status_code == 200:
            sub_data = response.json()
        url = f"http://api:4000/s/revenue"
        response = requests.get(url, timeout=10)
        revenue_data = None
        if response.status_code == 200:
            revenue_data = response.json()
        return sub_data, revenue_data

    # try to get data from API first
    data = fetch_data()
    subcount = data[0]
    subcount = reduce(lambda acc, item: acc + item['subscriber_count'], subcount, 0)
    revenue = data[1]
    revenue = reduce(lambda acc, item: acc + item['motion_max_revenue'], revenue, 0)
    st.write(subcount, revenue)
    lifetime_value = max(revenue / subcount, 0)
    data = {
        "lifetime_value": lifetime_value
    }

    if data:
        plot_customer_lifetime_value(data)