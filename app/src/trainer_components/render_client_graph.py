import matplotlib.pyplot as plt
import pandas as pd
import requests
import streamlit as st



def plot_macro_pie_chart(protein_g, carbs_g, fat_g, title="Macronutrient Breakdown"):
    # Calculate calories from each macronutrient
    # 1g protein = 4 calories, 1g carbs = 4 calories, 1g fat = 9 calories
    protein_cal = protein_g * 4
    carbs_cal = carbs_g * 4
    fat_cal = fat_g * 9

    # Data for pie chart
    labels = ['Protein', 'Carbs', 'Fat']
    sizes = [protein_cal, carbs_cal, fat_cal]
    colors = ['#ff9999', '#66b3ff', '#ffcc99']

    # Calculate percentages
    total_calories = sum(sizes)
    st.write (f"Total Calories: {total_calories:.0f}")
    percentages = [100 * size / total_calories for size in sizes]

    # Create pie chart
    fig, ax = plt.subplots(figsize=(10, 6))
    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=labels,
        colors=colors,
        autopct='%1.1f%%',
        startangle=90,
        wedgeprops={'edgecolor': 'w', 'linewidth': 1}
    )

    # Equal aspect ratio ensures that pie is drawn as a circle
    ax.axis('equal')

    # Add title and legend with grams
    plt.title(f"{title}\nTotal Calories: {total_calories:.0f}", fontsize=14)
    legend_labels = [
        f'Protein: {protein_g}g ({protein_cal:.0f} cal)',
        f'Carbs: {carbs_g}g ({carbs_cal:.0f} cal)',
        f'Fat: {fat_g}g ({fat_cal:.0f} cal)'
    ]
    plt.legend(wedges, legend_labels, loc='center left', bbox_to_anchor=(1, 0.5))

    return st.plotly.pyplot(fig)

def weekly_workout(creator_id, subscriber_id, name):
    st.write(f"### {name}'s Weekly Workout")
    df = pd.dataframe(requests.get(f'http://api:4000/t/{creator_id}/{subscriber_id}').json())
    return st.dataframe(df)
