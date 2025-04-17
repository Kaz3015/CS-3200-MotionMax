import matplotlib.pyplot as plt
import pandas as pd
import requests
import streamlit as st

def plot_customer_acquisition_costs(data, title="Monthly Customer Acquisition Costs"):
    """
    Creates a bar chart showing monthly customer acquisition costs.
    """
    #makes datafram
    df = pd.DataFrame(data)

    #finds the total cost
    total_cost = df['cost'].sum()

    #show the Total Customer Acquisition Cost
    st.write(f"Total Customer Acquisition Cost: ${total_cost:.2f}")

    #make the bar chart
    fig, ax = plt.subplots(figsize=(10, 6))

    #actually creates the bars
    bars = ax.bar(
        df['month'],
        df['cost'],
        color='black',
        width=0.6,
        edgecolor='white',
        linewidth=0.7
    )

    #making the labels and title
    ax.set_xlabel('Months', fontsize=12)
    ax.set_ylabel('Cost ($)', fontsize=12, rotation=90)

    #I wanted to create a second y-axis label for "Number of Customers" because num customers ties into the
    #customer aquisition cost per month
    ax2 = ax.twinx()
    ax2.set_ylabel('Number of Customers', fontsize=12, rotation=90)
    ax2.set_yticks([])  # Hide the ticks

    #makes the title of the bar chart
    plt.title(title, fontsize=14)

    #this makes the grid lines for the chart
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    #this actually shows the plot
    st.pyplot(fig)

    #show the information in columns
    col1, col2, col3 = st.columns(3)

    #shows the customer aquisition cost in the first column
    with col1:
        #find the average value in the cost column
        avg_cost = df['cost'].mean()
        #displays the average cost using streamlit
        st.metric("Average CAC", f"${avg_cost:.2f}")

    #shows the total number of customer in the second columns
    with col2:
        #find the total customers if the column is there
        total_customers = df['customers'].sum() if 'customers' in df.columns else 0
        #show the total customers using streamlit
        st.metric("Total Customers", f"{total_customers}")

    #shows the max monthly Customer Aquisition Costs in the third column
    with col3:
        #finds the max value in the cost column
        max_cost = df['cost'].max()
        #show the max cost using streamlit
        st.metric("Max Monthly CAC", f"${max_cost:.2f}")

st.title("MotionMAX Analytics")
st.subheader("Customer Acquisition Cost Analysis")

def fetch_data():
    #make the API endpoint url to get Customer Acquisition cost data
    url = "http://api:4000/s/CA_cost"
    #sned a get request to the API
    response = requests.get(url, timeout=10)
    #if the request is successful return the JSON data
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


#try to get data from API first
data = fetch_data()
if data:
    plot_customer_acquisition_costs(data)
else:
    # On initial load, use sample data
    plot_customer_acquisition_costs(sample_data)