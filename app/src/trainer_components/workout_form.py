import streamlit as st
import logging
import requests
import json
from datetime import datetime
import trainer_components.pill as pill

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Initialize session state variables properly


def handle_exercise_selection():
    """Callback for when exercise type is selected"""
    selected_option = st.session_state['exercise_selection']
    if selected_option != "Select option":
        st.session_state['show_exercise_form'] = True
        st.session_state['form_type'] = selected_option
        logger.info(f"Exercise selection changed to: {selected_option}")


def add_exercise_to_workout():
    """Add an exercise to the workout - called after form processing"""
    # Get the exercise data from session state
    exercise_data = st.session_state['pending_exercise_data']

    # If we're editing an existing exercise, update it instead of adding
    if 'edit_exercise_index' in st.session_state and st.session_state['edit_exercise_index'] is not None:
        index = st.session_state['edit_exercise_index']
        st.session_state['exercises'][index] = exercise_data
        st.session_state['edit_exercise_index'] = None  # Reset edit index
    else:
        st.session_state['exercises'].append(exercise_data)

    # Clear pending data
    st.session_state['pending_exercise_data'] = None

    # Reset form state
    st.session_state['reset_form'] = True
    st.session_state['show_exercise_form'] = False
    st.session_state['form_type'] = None

    # Add this line to preserve the current workout state - this is the key fix
    st.session_state['preserve_exercises'] = True


def on_cancel_click():
    """Callback for cancel button click"""
    st.session_state['cancel_clicked'] = True
    if 'edit_exercise_index' in st.session_state:
        st.session_state['edit_exercise_index'] = None  # Clear edit mode on cancel


def on_add_new_exercise_click():
    """Callback for add new exercise button"""
    exercise_name = st.session_state.get("new_exercise_name", "")
    exercise_description = st.session_state.get("new_exercise_description", "")
    exercise_reps_min = st.session_state.get("new_min", 8)
    exercise_reps_max = st.session_state.get("new_max", 12)
    exercise_sets = st.session_state.get("new_sets", 3)

    if exercise_name:
        st.session_state['pending_exercise_data'] = {
            "title": exercise_name,
            "description": exercise_description,
            "rep_low": exercise_reps_min,
            "rep_high": exercise_reps_max,
            "sets": exercise_sets,
            "is_new": True
        }
        st.session_state['add_exercise_clicked'] = True
    else:
        st.session_state['show_error'] = "Exercise name is required"


def on_add_existing_exercise_click():
    """Callback for add existing exercise button"""
    exercise_name = st.session_state.get("existing_exercise_select", "")
    exercise_description = st.session_state.get("existing_exercise_description", "")
    exercise_reps_min = st.session_state.get("existing_min", 8)
    exercise_reps_max = st.session_state.get("existing_max", 12)
    exercise_sets = st.session_state.get("existing_sets", 3)
    emd_id = st.session_state.get("existing_exercise_emd_id")
    et_id = st.session_state.get("existing_exercise_et_id")

    if exercise_name:
        st.session_state['pending_exercise_data'] = {
            "title": exercise_name,
            "description": exercise_description,
            "rep_low": exercise_reps_min,
            "rep_high": exercise_reps_max,
            "sets": exercise_sets,
            "emd_id": emd_id,
            "et_id:"
            "is_new": False
        }
        st.session_state['add_exercise_clicked'] = True
    else:
        st.session_state['show_error'] = "Please select an exercise"


def clear_old_errors():
    """Clear expired error messages"""
    now = datetime.now().timestamp()
    # Check if any messages have expired
    expired_found = False
    for err in st.session_state['error_messages']:
        if err['expires'] <= now:
            expired_found = True
            break

    if expired_found:
        # Remove expired messages
        st.session_state['error_messages'] = [
            err for err in st.session_state['error_messages']
            if err['expires'] > now
        ]  # Make sure we rerun when errors are cleared


def show_timed_error(message, seconds=2):
    """Add error message with timestamp"""
    error_id = datetime.now().timestamp()
    st.session_state['error_messages'].append({
        'id': error_id,
        'message': message,
        'expires': datetime.now().timestamp() + seconds
    })
    # Schedule clearing old messages
    clear_old_errors()


def edit_exercise(index):
    """Set up the form to edit an existing exercise"""
    # Store the index of the exercise being edited
    st.session_state['edit_exercise_index'] = index

    # Set form to show
    st.session_state['show_exercise_form'] = True

    # Set form type based on whether exercise is new or existing
    exercise = st.session_state['exercises'][index]
    if exercise.get('is_new', True):
        st.session_state['form_type'] = "new exercise"
    else:
        st.session_state['form_type'] = "existing exercise"

    # Store current exercise data to populate form
    st.session_state['current_exercise'] = exercise


def save_workout_to_database():
    """Save the workout to the database"""
    workout_data = {
        "title": st.session_state.get("workout_name", ""),
        "description": st.session_state.get("workout_description", ""),
        "user_id": st.session_state["user_id"],
        "exercises": []
    }

    for i, exercise in enumerate(st.session_state['exercises']):
        # Add sequence number to each exercise
        exercise_data = {
            "title": exercise.get("title", ""),
            "description": exercise.get("description", ""),
            "rep_low": exercise.get("rep_low", 8),
            "rep_high": exercise.get("rep_high", 12),
            "sets": exercise.get("sets", 3),
            "sequence": i + 1  # 1-based sequence
        }

        # Add existing ID if available
        if "emd_id" in exercise:
            exercise_data["emd_id"] = exercise["emd_id"]
        if "et_id" in exercise:
            exercise_data["et_id"] = exercise["et_id"]

        workout_data["exercises"].append(exercise_data)

    # Add workout ID if we're updating
    if st.session_state['workout_id']:
        workout_data["w_id"] = st.session_state['workout_id']

    try:
        # Determine if this is a create or update operation
        if st.session_state['workout_id']:
            # Update existing workout
            logger.info(f"Updating workout {st.session_state['workout_id']} with data: {workout_data}")
            response = requests.put(
                f'http://api:4000/t/{st.session_state["user_id"]}/addWorkout/{st.session_state["workout_id"]}',
                json=workout_data
            )
        else:
            # Create new workout
            logger.info("Creating new workout")
            response = requests.post(
                f'http://api:4000/t/{st.session_state["user_id"]}/addWorkout',
                json=workout_data
            )

        if response.status_code in (200, 201):
            logger.info(f"Workout saved successfully: {response.json()}")
            return True, "Workout saved successfully!"
        else:
            logger.error(f"Error saving workout: {response.text}")
            return False, f"Error saving workout: {response.text}"
    except Exception as e:
        logger.error(f"Exception saving workout: {e}")
        return False, f"Error communicating with server: {e}"


def render_workout_form():
    if 'workout_id' not in st.session_state:
        st.session_state['workout_id'] = None
    if 'exercise_id' not in st.session_state:
        st.session_state['exercise_id'] = None
    if 'exercises' not in st.session_state:
        st.session_state['exercises'] = []
    if 'show_exercise_form' not in st.session_state:
        st.session_state['show_exercise_form'] = False
    if 'form_type' not in st.session_state:
        st.session_state['form_type'] = None
    if 'reset_form' not in st.session_state:
        st.session_state['reset_form'] = False
    if 'cancel_clicked' not in st.session_state:
        st.session_state['cancel_clicked'] = False
    if 'add_exercise_clicked' not in st.session_state:
        st.session_state['add_exercise_clicked'] = False
    if 'pending_exercise_data' not in st.session_state:
        st.session_state['pending_exercise_data'] = None
    if 'error_messages' not in st.session_state:
        st.session_state['error_messages'] = []
    if 'edit_exercise_index' not in st.session_state:
        st.session_state['edit_exercise_index'] = None
    if 'current_exercise' not in st.session_state:
        st.session_state['current_exercise'] = None
    if 'workout_loaded' not in st.session_state:
        st.session_state['workout_loaded'] = False
    if 'show_error' not in st.session_state:
        st.session_state['show_error'] = None
    if 'save_clicked' not in st.session_state:
        st.session_state['save_clicked'] = False
    # Add this check for the new preserve_exercises flag
    if 'preserve_exercises' not in st.session_state:
        st.session_state['preserve_exercises'] = False

    # Handle cancel action at the beginning
    if st.session_state['cancel_clicked']:
        st.session_state['show_exercise_form'] = False
        st.session_state['form_type'] = None
        st.session_state['reset_form'] = True
        st.session_state['cancel_clicked'] = False
        st.session_state['edit_exercise_index'] = None  # Clear edit mode on cancel

    # Handle add exercise action at the beginning
    if st.session_state['add_exercise_clicked'] and st.session_state['pending_exercise_data']:
        add_exercise_to_workout()
        st.session_state['add_exercise_clicked'] = False

    # Handle save workout action
    if st.session_state['save_clicked']:
        success, message = save_workout_to_database()
        if success:
            # Reset state after successful save
            st.session_state['workout_id'] = None
            st.session_state['exercises'] = []
            st.session_state['show_exercise_form'] = False
            st.session_state['form_type'] = None
            st.session_state['reset_form'] = True
            st.session_state['workout_loaded'] = False
            st.success(message)
        else:
            st.error(message)

        st.session_state['save_clicked'] = False

    # Handle any error that needs to be shown
    if st.session_state['show_error']:
        show_timed_error(st.session_state['show_error'])
        st.session_state['show_error'] = None

    # Clear expired error messages
    if st.session_state['error_messages']:
        now = datetime.now().timestamp()
        expired_found = False
        for err in st.session_state['error_messages']:
            if err['expires'] <= now:
                expired_found = True
                break

        if expired_found:
            # Remove expired messages
            st.session_state['error_messages'] = [
                err for err in st.session_state['error_messages']
                if err['expires'] > now
            ]

    # Display any active error messages
    for error in st.session_state['error_messages']:
        st.error(error['message'])

    try:
        # Fetch workout data
        workouts = requests.get(f'http://api:4000/t/{st.session_state["user_id"]}/workouts').json()
        exercise_list = [x.get('exercise_title', '') for x in workouts if 'exercise_title' in x]
    except Exception as e:
        logger.error(f"Error fetching workout data: {e}")
        show_timed_error(f"Error loading workout data: {e}")
        workouts = []
        exercise_list = []

    # Main workout container css
    st.markdown("""
            <style>
            .st-key-workout_container {
                    background-color: white;
                    border-radius: 12px;
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
                    border: 1px solid #edf2f7;
                    transition: all 0.3s ease;
                    padding: 20px;
            }
            .st-key-workout_container:hover {
                box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
                transform: translateY(-2px);
                transition: box-shadow 0.3s ease;
            }
            .st-key-workout_container .st-key-pill {
                margin-top: -1rem;
                margin-bottom: -1rem;
            }

            .st-key-workout_container .st-key-save_workout {
                width: 100%;
                text-align: left;
                margin-top: 2px;  
            }
            .st-key-workout_container .st-key-save_workout button {
                background-color: white;
                color: black;
                border: 1px solid;
                padding-left: 20px;
                width: 100%;
                display: block;
                text-align: center;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);    
            }

            .st-key-workout_container .st-key-save_workout button:hover {
                background-color: #f8fafc;
                border-color: #3b82f6;
            }

            .st-key-workout_container .st-key-save_workout button:focus {
                background-color: #eff6ff;
                border-color: #3b82f6;
                color: #1d4ed8;
            }  
            </style>
            """, unsafe_allow_html=True)
    workout_container = st.container(key="workout_container")

    with workout_container:
        with st.container(key="pill"):
            pill.split_pill_selector(option_left="Workout Form", option_right="Recipe Form", key="title_pill")
        st.subheader("Workout Form")

        # Workout Details Section
        if not st.session_state['workout_id']:
            # Creating a new workout
            workout_name = st.text_input("Workout Name", key="workout_name")
            workout_description = st.text_area("Workout Description", key="workout_description")
        else:
            # Editing existing workout
            matching_workouts = [w for w in workouts if w.get('w_id') == st.session_state['workout_id']]
            if matching_workouts and not st.session_state['workout_loaded']:
                # Only clear existing exercises if we're not preserving them
                if not st.session_state['preserve_exercises']:
                    st.session_state['exercises'] = []
                st.session_state['workout_loaded'] = True

                workout = matching_workouts[0]
                workout_name = st.text_input("Workout Name", value=workout.get('title', ''), key="workout_name")
                workout_description = st.text_area("Workout Description", value=workout.get('description', ''),
                                                   key="workout_description")

                # Only reload exercises from DB if not preserving them
                if not st.session_state['preserve_exercises']:
                    st.session_state['exercises'] = []
                    for exercise in matching_workouts:
                        exercise_data = {
                            "title": exercise['exercise_title'],
                            "description": exercise.get('description', ''),
                            "rep_low": exercise['rep_low'],
                            "rep_high": exercise['rep_high'],
                            "sets": exercise['sets'],
                            "sequence": exercise.get('sequence', 0),
                            "is_new": False,
                            # Keep track of DB IDs for update operations
                            "et_id": exercise.get('et_id'),
                            "emd_id": exercise.get('emd_id')
                        }
                        st.session_state['exercises'].append(exercise_data)

                # Reset the preserve flag after loading
                st.session_state['preserve_exercises'] = False
            elif matching_workouts:
                workout = matching_workouts[0]
                workout_name = st.text_input("Workout Name", value=workout.get('title', ''), key="workout_name")
                workout_description = st.text_area("Workout Description", value=workout.get('description', ''),
                                                   key="workout_description")

        # Display current exercises
        if st.session_state['exercises']:
            st.subheader("Exercises")
            for i, exercise in enumerate(st.session_state['exercises']):
                with st.expander(f"Exercise {i + 1}: {exercise.get('title', 'Unnamed')}"):
                    st.write(f"Description: {exercise.get('description', '')}")
                    st.write(f"Reps: {exercise.get('rep_low', 0)}-{exercise.get('rep_high', 0)}")
                    st.write(f"Sets: {exercise.get('sets', 0)}")

                    # Add buttons in columns for edit and remove
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Edit", key=f"edit_{i}"):
                            edit_exercise(i)
                    with col2:
                        if st.button("Remove", key=f"remove_{i}"):
                            st.session_state['exercises'].pop(i)

        # Check if the form needs to be reset (after adding an exercise)
        if st.session_state['reset_form']:
            # Default index to show "Select option"
            selectbox_index = 0
            st.session_state['reset_form'] = False
        else:
            # Keep the current selection if form is active
            selectbox_index = 0  # Default to "Select option"

        # Exercise Selection
        st.subheader("Add Exercise")
        exercise_option = st.selectbox(
            "Select Exercise Type",
            ["Select option", "new exercise", "existing exercise"],
            index=selectbox_index,
            key="exercise_selection",
            on_change=handle_exercise_selection
        )

        # Exercise Form (only shown after selection)
        if st.session_state['show_exercise_form']:
            form_type = st.session_state['form_type']
            exercise_form_container = st.container(key="exercise_container")
            st.markdown(f"""
                    <style>
                        .st-key-exercise_container .st-key-cancel_new {{
                            width: 100%;
                            text-align: left;
                            margin-top: 2px;  
                        }}    
                        .st-key-exercise_container .st-key-cancel_new button {{
                            background-color: white;
                            color: black;
                            border: 1px solid;
                            padding-left: 20px;
                            display: block;
                            width: 100%;
                            text-align: center;
                            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);    
                        }}
                        .st-key-exercise_container .st-key-cancel_new button:hover {{
                            background-color: #f8fafc;
                            border-color: #3b82f6;
                        }}
                        .st-key-exercise_container .st-key-cancel_new button:focus {{
                            background-color: #eff6ff;
                            border-color: #3b82f6;
                            color: #1d4ed8;
                        }}

                        .st-key-exercise_container .st-key-add_new {{
                            width: 100%;
                            text-align: left;
                            margin-top: 2px;  
                        }}    
                        .st-key-exercise_container .st-key-add_new button {{
                            background-color: white;
                            color: black;
                            border: 1px solid;
                            padding-left: 20px;
                            width: 100%;
                            display: block;
                            text-align: center;
                            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);    
                        }}
                        .st-key-exercise_container .st-key-add_new button:hover {{
                            background-color: #f8fafc;
                            border-color: #3b82f6;
                        }}
                        .st-key-exercise_container .st-key-add_new button:focus {{
                            background-color: #eff6ff;
                            border-color: #3b82f6;
                            color: #1d4ed8;
                        }}

                        </style>
                    """, unsafe_allow_html=True)

            with exercise_form_container:
                is_editing = st.session_state['edit_exercise_index'] is not None
                editing_label = "Edit Exercise" if is_editing else "New Exercise"

                if form_type == "new exercise":
                    st.subheader(editing_label)

                    # Pre-populate fields if editing
                    default_name = ""
                    default_description = ""
                    default_min = 8
                    default_max = 12
                    default_sets = 3

                    if is_editing:
                        exercise = st.session_state['exercises'][st.session_state['edit_exercise_index']]
                        default_name = exercise.get('title', '')
                        default_description = exercise.get('description', '')
                        default_min = exercise.get('rep_low', 8)
                        default_max = exercise.get('rep_high', 12)
                        default_sets = exercise.get('sets', 3)

                    exercise_name = st.text_input("Exercise Name", key="new_exercise_name", value=default_name)
                    exercise_description = st.text_area("Exercise Description", key="new_exercise_description",
                                                        value=default_description)

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        exercise_reps_min = st.number_input("Minimum Reps", min_value=1, max_value=20,
                                                            value=default_min,
                                                            key="new_min")
                    with col2:
                        exercise_reps_max = st.number_input("Maximum Reps", min_value=exercise_reps_min, max_value=20,
                                                            value=default_max, key="new_max")
                    with col3:
                        exercise_sets = st.number_input("Sets", min_value=1, max_value=10, value=default_sets,
                                                        key="new_sets")

                    col1, col2 = st.columns(2)

                    with col1:
                        st.button("Cancel", key="cancel_new", on_click=on_cancel_click)
                    with col2:
                        button_label = "Update Exercise" if is_editing else "Add to Workout"
                        st.button(button_label, key="add_new", on_click=on_add_new_exercise_click)

                elif form_type == "existing exercise":
                    st.subheader("Select Existing Exercise")

                    if exercise_list:
                        # Pre-populate selection if editing
                        default_index = 0
                        if is_editing:
                            exercise = st.session_state['exercises'][st.session_state['edit_exercise_index']]
                            title = exercise.get('title', '')
                            if title in exercise_list:
                                default_index = exercise_list.index(title) + 1  # +1 because we add "" at the beginning

                        exercise_name_select = st.selectbox(
                            "Select Exercise",
                            options=[""] + exercise_list,
                            index=default_index,
                            key="existing_exercise_select"
                        )

                        if exercise_name_select:
                            try:
                                # Find the selected exercise details
                                exercise_info = list(
                                    filter(lambda x: x.get('exercise_title') == exercise_name_select, workouts))

                                if exercise_info:
                                    selected_exercise = exercise_info[0]
                                    logger.info(f"Selected exercise: {selected_exercise}")

                                    # Store emd_id for use in callbacks
                                    st.session_state["existing_exercise_emd_id"] = selected_exercise.get('emd_id')
                                    st.session_state["existing_exercise_et_id"] = selected_exercise.get('et_id')

                                    # Default values - either from DB or from the exercise being edited
                                    default_description = selected_exercise.get('description', '')
                                    default_min = selected_exercise.get('rep_low', 8)
                                    default_max = selected_exercise.get('rep_high', 12)
                                    default_sets = selected_exercise.get('sets', 3)

                                    if is_editing:
                                        exercise = st.session_state['exercises'][
                                            st.session_state['edit_exercise_index']]
                                        if exercise.get('title') == exercise_name_select:
                                            default_description = exercise.get('description', default_description)
                                            default_min = exercise.get('rep_low', default_min)
                                            default_max = exercise.get('rep_high', default_max)
                                            default_sets = exercise.get('sets', default_sets)

                                    # Add description field
                                    exercise_description = st.text_area(
                                        "Exercise Description",
                                        value=default_description,
                                        key="existing_exercise_description"
                                    )

                                    col1, col2, col3 = st.columns(3)
                                    with col1:
                                        exercise_reps_min = st.number_input(
                                            "Minimum Reps",
                                            min_value=1,
                                            max_value=20,
                                            value=default_min,
                                            key="existing_min"
                                        )
                                    with col2:
                                        exercise_reps_max = st.number_input(
                                            "Maximum Reps",
                                            min_value=exercise_reps_min,
                                            max_value=20,
                                            value=default_max,
                                            key="existing_max"
                                        )
                                    with col3:
                                        exercise_sets = st.number_input(
                                            "Sets",
                                            min_value=1,
                                            max_value=10,
                                            value=default_sets,
                                            key="existing_sets"
                                        )

                                    col1, col2 = st.columns(2)
                                    with col1:
                                        # Use on_click instead of direct function call
                                        st.button("Cancel", key="cancel_existing", on_click=on_cancel_click)
                                    with col2:
                                        button_label = "Update Exercise" if is_editing else "Add to Workout"
                                        st.button(button_label, key="add_existing",
                                                  on_click=on_add_existing_exercise_click)
                                else:
                                    show_timed_error("Exercise not found in database")
                            except Exception as e:
                                logger.error(f"Error processing exercise: {e}")
                                show_timed_error(f"Error selecting exercise: {e}")
                    else:
                        show_timed_error("No existing exercises found")

        # Save workout button with callback for database operation
        def on_save_workout():
            """Callback for save workout button"""
            if not st.session_state.get("workout_name", ""):
                st.session_state['show_error'] = "Workout name is required"
                return

            if not st.session_state['exercises']:
                st.session_state['show_error'] = "Please add at least one exercise"
                return

            st.session_state['save_clicked'] = True

        st.button("Save Workout", key="save_workout", on_click=save_workout_to_database)