import streamlit as st
import requests
import trainer_components.render_list as render_list
import trainer_components.workout_form as workout_form
import trainer_components.render_recipe_form as recipe_form

row = st.columns([3,4,3])

with row[0]:
    def on_workout_click(name, workout_id):
        st.session_state['workout_id'] = workout_id
        st.session_state['form'] = "workout form"

    def on_workout_delete(name, workout_id):
        requests.delete(f'http://api:4000/t/{st.session_state["user_id"]}/{workout_id}/deleteWorkout')
        # st.session_state['existing recipe'] = False
        # st.session_state['form'] = "recipe form"
        # st.experimental_rerun()

    workout_data = requests.get(f'http://api:4000/t/{st.session_state["user_id"]}/workoutNames').json()
    workout_names = [name['title'] for name in workout_data]
    workout_ids = [workout_id['w_id'] for workout_id in workout_data]
    st.session_state['workout_loaded'] = False

    render_list.name_button_column(title="List of Workouts", names=workout_names, on_click_function=on_workout_click,
                                   on_delete_function=on_workout_delete, ids=workout_ids, key="workout")
with row[1]:
    if st.session_state['form'] == "workout form":
        with st.container(key="bye"):
            workout_form.render_workout_form()
    elif st.session_state['form'] == "recipe form":
        recipe_form.render_recipe_form()

with row[2]:
    def on_recipe_click(name, recipe_id):
        st.session_state['recipe_id'] = recipe_id
        st.session_state['existing recipe'] = True
        st.session_state['form'] = "recipe form"
        st.session_state['used_ingredients'] = []
    def on_recipe_delete(name, recipe_id):
        requests.delete(f'http://api:4000/t/{st.session_state["user_id"]}/{recipe_id}/deleteRecipe')
        st.session_state['existing recipe'] = False
        st.session_state['form'] = "recipe form"


    recipes = requests.get(f'http://api:4000/t/{st.session_state["user_id"]}/recipes').json()
    recipe_dict = dict(zip([name['recipe_title'] for name in recipes], [recipe_id['r_id'] for recipe_id in recipes]))
    recipe_title = recipe_dict.keys()
    recipe_ids = recipe_dict.values()
    render_list.name_button_column(title="List of Recipes", names=recipe_title, on_click_function=on_recipe_click,
                               on_delete_function=on_recipe_delete, ids=recipe_ids, key="recipe")