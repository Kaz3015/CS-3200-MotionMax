import streamlit as st
import logging
import requests
from datetime import datetime
import trainer_components.pill as pill

# ────────────────────────────────────────────────────────────────
#  Basic setup
# ────────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_ROOT = "http://api:4000"

# ════════════════════════════════════════════════════════════════
#  Public entry point
# ════════════════════════════════════════════════════════════════

def render_workout_form():
    """Streamlit component that lets users **create a workout** when
    `st.session_state['workout_id']` is **None** or **view** the workout whose
    ID is stored in that key.  No sidebar selector – the caller sets the ID
    in `session_state` before invoking this function.
    """

    # ────────────────────────────────────────────────────────────
    #  Helpers
    # ────────────────────────────────────────────────────────────

    def show_timed_error(msg: str):
        st.error(msg)

    def fetch_workouts(user_id: int):
        try:
            return requests.get(f"{API_ROOT}/t/{user_id}/workouts", timeout=10).json()
        except Exception as exc:
            logger.error("Error fetching workouts: %s", exc)
            show_timed_error(f"Error fetching workouts: {exc}")
            return []

    def post_workout(user_id: int, payload: dict):
        try:
            r = requests.post(f"{API_ROOT}/t/{user_id}/addWorkout", json=payload, timeout=10)
            r.raise_for_status()
            return True, r.json()
        except Exception as exc:
            logger.error("Error saving workout: %s", exc)
            return False, str(exc)

    # ────────────────────────────────────────────────────────────
    #  Session defaults
    # ────────────────────────────────────────────────────────────

    DEFAULTS = {
        "user_id": st.session_state['user_id'],  # replace with auth
        "workout_id": st.session_state['workout_id'],  # ← determines mode
        "workout_name": "",
        "workout_description": "",
        "exercises": [],
    }
    for k, v in DEFAULTS.items():
        st.session_state.setdefault(k, v)

    # ────────────────────────────────────────────────────────────
    #  Determine mode from session_state only
    # ────────────────────────────────────────────────────────────

    creating_new = st.session_state["workout_id"] is None

    # When viewing, fetch that single workout once (if not already loaded)
    if not creating_new and not st.session_state["exercises"]:
        workouts = fetch_workouts(st.session_state["user_id"])
        wid = st.session_state["workout_id"]
        matching = [w for w in workouts if w["w_id"] == wid]
        if not matching:
            show_timed_error("Workout not found for this user")
            return
        # header (use first record)
        head = matching[0]
        st.session_state["workout_name"] = head["title"]
        st.session_state["workout_description"] = head.get("description", "")
        # exercises list
        st.session_state["exercises"] = [
            {
                "title": rec["exercise_title"],
                "description": rec.get("description", ""),
                "rep_low": rec["rep_low"],
                "rep_high": rec["rep_high"],
                "sets": rec["sets"],
            }
            for rec in matching
        ]

    # ────────────────────────────────────────────────────────────
    #  Styling
    # ────────────────────────────────────────────────────────────

    st.markdown(
        """
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
        }
        .st-key-workout_container .st-key-pill {
            margin-top: -1rem;
            margin-bottom: -1rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ────────────────────────────────────────────────────────────
    #  Main UI
    # ────────────────────────────────────────────────────────────

    with st.container(key="workout_container"):
        pill.split_pill_selector("title_pill", "Workout Form", "Recipe Form")
        st.subheader("Workout Form")

        st.text_input("Workout Name", key="workout_name", disabled=not creating_new)
        st.text_area("Workout Description", key="workout_description", disabled=not creating_new)

        if st.session_state["exercises"]:
            st.subheader("Exercises")
            for idx, ex in enumerate(st.session_state["exercises"], 1):
                st.markdown(
                    f"**{idx}. {ex['title']}** – {ex['rep_low']}-{ex['rep_high']} reps · {ex['sets']} sets"
                )
                if ex["description"]:
                    st.caption(ex["description"])

        # ───────── Create‑mode widgets ─────────
        if creating_new:
            st.divider()
            st.subheader("Add Exercise")

            title = st.text_input("Name", key="ex_title")
            c1, c2, c3 = st.columns(3)
            with c1:
                low = st.number_input("Min reps", 1, 20, 8, key="ex_low")
            with c2:
                high = st.number_input("Max reps", low, 20, 12, key="ex_high")
            with c3:
                sets = st.number_input("Sets", 1, 10, 3, key="ex_sets")
            desc = st.text_area("Description", key="ex_desc")

            if st.button("Add to workout"):
                if not title:
                    show_timed_error("Exercise name required")
                else:
                    st.session_state["exercises"].append({
                        "title": title,
                        "description": desc,
                        "rep_low": low,
                        "rep_high": high,
                        "sets": sets,
                    })

            st.divider()
            if st.button("Save workout"):
                if not st.session_state["workout_name"]:
                    show_timed_error("Workout name required")
                elif not st.session_state["exercises"]:
                    show_timed_error("Add at least one exercise")
                else:
                    payload = {
                        "title": st.session_state["workout_name"],
                        "description": st.session_state["workout_description"],
                        "user_id": st.session_state["user_id"],
                        "exercises": [
                            {**e, "sequence": i + 1} for i, e in enumerate(st.session_state["exercises"])
                        ],
                    }
                    ok, resp = post_workout(st.session_state["user_id"], payload)
                    if ok:
                        st.success("Workout created!")
                        st.balloons()
                        # reset for a brand‑new create flow
                        st.session_state.update(
                            workout_id=None, exercises=[]
                        )
                    else:
                        show_timed_error(f"Save failed: {resp}")
        else:
            st.info("Viewing existing workout – editing disabled.")
