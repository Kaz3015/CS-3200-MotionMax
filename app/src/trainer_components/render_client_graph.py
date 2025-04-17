import matplotlib.pyplot as plt
import pandas as pd
import requests
import streamlit as st
import logging
import plotly.graph_objects as go



def create_macro_donut(protein_g, carbs_g, fat_g):
    if not protein_g or not carbs_g or not fat_g:
        st.write("No data available for macronutrients.")
        return
    protein_g = int(float(protein_g))
    carbs_g = int(float(carbs_g))
    fat_g = int(float(fat_g))

    protein_cal = protein_g * 4
    carbs_cal = carbs_g * 4
    fat_cal = fat_g * 9
    total_calories = protein_cal + carbs_cal + fat_cal

    # Calculate percentages
    protein_pct = (protein_cal / total_calories) * 100
    carbs_pct = (carbs_cal / total_calories) * 100
    fat_pct = (fat_cal / total_calories) * 100

    # Data for donut chart
    labels = ['Protein', 'Carbs', 'Fat']
    values = [protein_cal, carbs_cal, fat_cal]

    # Custom text to display
    text = [f'{protein_pct:.1f}%', f'{carbs_pct:.1f}%', f'{fat_pct:.1f}%']

    # Custom colors
    colors = ['#FF6B6B', '#4ECDC4', '#FFD166']

    # Create the donut chart
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        text=text,
        textinfo='label+text',
        hovertemplate='%{label}<br>%{value} calories<br>%{text}',
        marker=dict(colors=colors, line=dict(color='#FFFFFF', width=2)),
        hole=.6,
        sort=False
    )])

    # Add annotations in the center
    fig.update_layout(
        annotations=[
            dict(
                text=f'<span style="font-size:24px;font-weight:bold">{int(total_calories)} calories</span>',
                x=0.5, y=0.65,
                font_size=10,
                showarrow=False
            ),

            dict(
                text=f'<span style="font-size:12px;font-weight:bold">Protein: {protein_g}g</span>',
                x=0.5, y=0.55,
                font_size=10,
                showarrow=False
            ),
            dict(
                text=f'<span style="font-size:12px;font-weight:bold">Carbs: {carbs_g}g</span>',
                x=0.5, y=0.45,
                font_size=10,
                showarrow=False
            ),
            dict(
                text=f'<span style="font-size:12px;font-weight:bold">Fat: {fat_g}g</span>',
                x=0.5, y=0.35,
                font_size=10,
                showarrow=False
            )
        ],
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),
        height=500,
        width=None,
        margin=dict(t=100, b=100, l=20, r=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    return fig








def render_weekly_workouts():

    logger = logging.getLogger(__name__)

    # Fetch workout data
    response = requests.get(
        f'http://api:4000/t/workouts/{st.session_state["user_id"]}/{st.session_state["subscriber_id"]}').json()
    # If no workouts, show message
    if not response:
        st.info("No workouts scheduled for this week.")
        return

    # Create DataFrame and prepare for display
    df = pd.DataFrame(response)

    # Check if 'created_at' exists and convert to datetime if it does
    if 'created_at' in df.columns:
        df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%a, %b %d')

    # Rename columns for better display
    rename_map = {
        'circuit_type': 'Workout Type',
        'created_at': 'Date',
        'difficulty': 'Difficulty',
        'name': 'Workout Name'
    }
    df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})

    # Select and reorder columns
    display_cols = [col for col in ['Date', 'Workout Name', 'Workout Type', 'Difficulty']
                    if col in df.columns]
    df = df[display_cols]

    # Display as a styled dataframe
    return df
