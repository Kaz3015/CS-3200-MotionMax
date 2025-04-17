import streamlit as st
import trainer_components.pill as pill
import requests
import logging


def render_recipe_form():
    logger = logging.getLogger(__name__)
    st.session_state['ingredient_amounts'] = []
    st.session_state['measurements'] = []
    recipe_description = ""
    calories_val = 0
    protein_val = 0
    carbs_val = 0
    fat_val = 0


    with st.container(key="recipe_form"):
        ingredients = requests.get(f'http://api:4000/t/{st.session_state["user_id"]}/ingredients').json()
        ingredient_ids = {}
        measure = ["tsp", "tbsp", "cup", "pint", "quart", "gallon", "oz", "lb", "pc"]
        for ingredient in ingredients:
           ingredient_ids[ingredient['ingredient_name']] = ingredient['ing_id']
        if not st.session_state['ingredient names']:
            [st.session_state['ingredient names'].append(ingredient['ingredient_name']) for ingredient in ingredients]
        ingredient_names = st.session_state['ingredient names']


        st.markdown("""
        <style>
            .st-key-recipe_form {
                background-color: white;
                border-radius: 12px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
                border: 1px solid #edf2f7;
                transition: all 0.3s ease;
                padding: 20px;
                margin-top: 1rem;
            }
            
            .st-key-recipe_form .st-key-pill {
                margin-top: -2rem;
                margin-bottom: -1rem;
            }
            
            .st-key-recipe_form:hover {
                box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
                transform: translateY(-2px);
                transition: box-shadow 0.3s ease;
            }
        </style>
        """, unsafe_allow_html=True)

        calories_val = 0
        protein_val = 0
        carbs_val = 0
        fat_val = 0

        #Loading data from API for existing recipe
        if st.session_state['existing recipe']:
           data = requests.get(f'http://api:4000/t/{st.session_state["user_id"]}/{st.session_state["recipe_id"]}/recipe').json()
           existing_recipe_ingredients = dict(zip([ingredient['ingredient_name'] for ingredient in data], [ingredient['ing_id'] for ingredient in data]))
           st.session_state['recipe_title'] = data[0]['recipe_title']
           logger.info(f"Recipe title: {st.session_state['recipe_title']}")
           recipe_description = data[0]['recipe_description']
           calories_val = data[0]['calories']
           protein_val = data[0]['protein']
           carbs_val = data[0]['carbs']
           fat_val = data[0]['fat']

           # adding ingredients to the list of used ingredients if not already present
           if len(st.session_state['used_ingredients']) == len(data) or st.session_state['used_ingredients'] == []:
               st.session_state['used_ingredients'] = [data['ingredient_name'] for data in data]

        with st.container(key="pill"):
            pill.split_pill_selector(option_left="Workout Form", option_right="Recipe Form", key="title_pill")

        # creating the recipe form
        st.subheader("Recipe Form")
        logger.info(f"Recipe title before input: {st.session_state['recipe_title']}")
        st.text_input("Recipe Name", key="recipe_name", value=st.session_state['recipe_title'])
        logger.info(f"Recipe title after input: {st.session_state['recipe_title']}")
        logger.info(f"Recipe name after input: {st.session_state['recipe_name']}")
        st.text_area("Recipe Description", key="recipe_description", value=recipe_description)
        macros = st.columns(4)
        with macros[0]:
           calories = st.number_input("Calories", min_value=0, step=1, key="calories", value=calories_val)
        with macros[1]:
           protein = st.number_input("Protein (g)", min_value=0, step=1, key="protein", value=protein_val)
        with macros[2]:
            carbs =st.number_input("Carbs (g)", min_value=0, step=1, key="carbs", value=carbs_val)
        with macros[3]:
            fat = st.number_input("Fat (g)", min_value=0, step=1, key="fat", value=fat_val)


        used_ingredients = st.multiselect("Select ingredients", ingredient_names, default=st.session_state['used_ingredients'], key="ingredients")
        st.session_state['ingr_name'] = ""

        def add_ingredient():
            if st.session_state['ingr_name'] not in used_ingredients and st.session_state['ingr_name'] != "":
                name = st.session_state['ingr_name']
                st.session_state['ingredient names'].append(name)
                st.session_state['used_ingredients'].append(name)
                st.session_state['added_ingredients'].append(name)
                st.session_state['ingr_name'] = ""

        ingredient_details = st.expander("Ingredient Details", expanded=True)
        with ingredient_details:
            for index, ingredient in enumerate(used_ingredients):
                if st.session_state['existing recipe'] and existing_recipe_ingredients.get(ingredient) is not None:
                    row = st.columns(3, vertical_alignment="center")
                    row[0].write(ingredient)
                    row[1].number_input("Amount", min_value=0.0, step=.25, key=f"amount_{ingredient}", value=data[index]['amount'])
                    measurement = None
                    for i in range(len(measure)):
                        if measure[i] == data[index]['measurement']:
                            measurement = i
                    row[2].selectbox("Unit", measure, key=f"unit_{ingredient}", index=measurement)
                else:
                    row = st.columns(3, vertical_alignment="center")
                    row[0].write(ingredient)
                    row[1].number_input("Amount", min_value=0.0, step=.25, key=f"amount_{ingredient}")
                    row[2].selectbox("Unit", measure, key=f"unit_{ingredient}")
            ingr_row =st.columns([7,3], vertical_alignment="bottom")
            st.session_state['ingr_name'] = ingr_row[0].text_input("Ingredient", key="add_ingredient_name")
            ingr_row[1].button("Add", key="add_ingredient", on_click=add_ingredient)

        st.text_area("Instructions", key="instructions")
        ingredient_payload = {}

        def check_ingredients():
            for ig in used_ingredients:
                amount = st.session_state[f"amount_{ig}"]
                unit = st.session_state[f"unit_{ig}"]
                if amount > 0 and ig not in st.session_state['added_ingredients']:
                    ingredient_payload[ig] = (ingredient_ids[ig], amount, unit)
                elif amount > 0 :
                    ingredient_payload[ig] = (amount, unit)
                else:
                    return False
            return True

        def submit():
            logger.info(f"Trying to submit recipe, calories: {calories}, protein: {protein}, fat: {fat}, carbs: {carbs}")
            if calories > 0 and protein > 0 and fat > 0 and carbs > 0 and used_ingredients != [] and check_ingredients():
                logger.info(f"Submitting recipe with ingredients: {ingredient_payload}")
                recipe = {
                    "recipe_name": st.session_state['recipe_name'],
                    "recipe_id": st.session_state['recipe_id'],
                    "recipe_description": st.session_state['recipe_description'],
                    "calories": calories,
                    "protein": protein,
                    "carbs": carbs,
                    "fat": fat,
                    "ingredients": ingredient_payload,
                    "instructions": st.session_state['instructions']
                }
                logger.info(f"Exising: {st.session_state['existing recipe']}")
                if st.session_state['existing recipe']:
                    logger.info(f"Exising: {st.session_state['existing recipe']}")
                    response = requests.put(f'http://api:4000/t/{st.session_state["user_id"]}/addRecipe', json=recipe)
                else:
                    logger.info(f"poop: {st.session_state['existing recipe']}")
                    response = requests.post(f'http://api:4000/t/{st.session_state["user_id"]}/addRecipe', json=recipe)
                logger.info(f"Response: {response}")
                if response.status_code == 200:
                    st.success("Recipe submitted successfully!")
                    st.session_state['used_ingredients'] = []
                    st.session_state['ingredient names'] = []
                    st.session_state['ingredient_amounts'] = []
                    st.session_state['measurements'] = []
                    st.session_state['recipe_title'] = ""
                    st.session_state['recipe_description'] = ""
                    st.session_state['instructions'] = ""
                    st.session_state['existing recipe'] = False
                    st.session_state['added_ingredients'] = []
                    st.session_state['recipe_id'] = None
                else:
                    st.error("Error submitting recipe.")
        st.button("Submit Recipe", key="submit_recipe", on_click=submit)


