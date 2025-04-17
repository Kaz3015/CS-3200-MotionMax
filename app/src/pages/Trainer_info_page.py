import streamlit as st
import trainer_components.message_board as message_board
import datetime
import calendar
import pandas as pd
import requests

row = st.columns([5, 5])

with row[0]:
    st.markdown("""
              <style>
              .st-key-finacials{
                      background-color: white;
                      border-radius: 12px;
                      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
                      border: 1px solid #edf2f7;
                      transition: all 0.3s ease;
                      padding: 20px;
                      overflow: hidden;
              }
              .st-key-finacials:hover {
                  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
                  transform: translateY(-2px);
                  transition: box-shadow 0.3s ease;
              }
              </style>
              """, unsafe_allow_html=True)
    with st.container(key = "finacials", border = True):
        # Get financial data from API
        data = requests.get(f'http://api:4000/t/{st.session_state["user_id"]}/finacials').json()

        # Filter for current year
        current_year = datetime.datetime.now().year
        data = [item for item in data if item['year'] == current_year]

        # Create a DataFrame with all months (even those with no data)
        all_months = pd.DataFrame({
            'month_num': range(1, 13),
            'month_name': [calendar.month_abbr[i] for i in range(1, 13)]
        })

        # Convert API data to DataFrame
        if data:
            # Create DataFrame from the API data
            df = pd.DataFrame(data)

            # Merge with all_months to ensure all months are included
            df_merged = pd.merge(all_months, df, left_on='month_num', right_on='month', how='left')

            # Fill missing revenue values with 0
            df_merged['total_revenue'] = df_merged['total_revenue'].fillna(0)

            # Set month_name as index for the chart
            chart_df = df_merged[['month_name', 'total_revenue']].set_index('month_name')

            # Make sure months are in correct order
            chart_df = chart_df.reindex([calendar.month_abbr[i] for i in range(1, 13)])
        else:
            # Create empty DataFrame with all months if no data
            chart_df = pd.DataFrame({
                'total_revenue': [0] * 12
            }, index=[calendar.month_abbr[i] for i in range(1, 13)])

        # Display the chart
        st.subheader("Monthly Revenue")
        st.bar_chart(chart_df, use_container_width=True)
with row[1]:
    st.markdown("""
           <style>
           .st-key-message_board {
                   background-color: white;
                   border-radius: 12px;
                   box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
                   border: 1px solid #edf2f7;
                   transition: all 0.3s ease;
                   padding: 20px;
           }
           .st-key-message_board:hover {
               box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
               transform: translateY(-2px);
               transition: box-shadow 0.3s ease;
           }
           </style>
           """, unsafe_allow_html=True)
    with st.container(key="message_board"):
        message_board.render_message_board()