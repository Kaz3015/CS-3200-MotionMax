import streamlit as st
import logging



def name_button_column(title, names, ids, on_click_function, on_delete_function, key):
    # create dictionary to map names to ids
    map = dict(zip(names, ids))
    clicked_name = None
    clicked_id = None
    #custom css for the container
    st.markdown(f"""
    <style>
        .st-key-{key} {{
            background-color: white;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            border: 1px solid #edf2f7;
            transition: all 0.3s ease;
            padding-left: 15px;
            padding-right: 15px;
            gap: 5px;
            padding-bottom: 20px;   
            justify-content: center; 
            text-align: center;
            width: 100%;      
        }}
        .st-key-{key}:hover {{
           box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
            transform: translateY(-2px);
            transition: box-shadow 0.3s ease;
        </style>
    """, unsafe_allow_html=True)
    with st.container(key=key):
        st.subheader(title, divider="gray")
        # Create a button for each name
        for name, id_value in zip(names, ids):
            buttonKey = f"{key}{name}{id_value}".replace(" ","")
            # Create a button with custom styling
            st.markdown(f"""
                <style>
                    .st-key-{key} .st-key-{buttonKey} {{
                        width: 100%;
                        text-align: left;
                        margin-top: 2px;  
                    }}    
                    .st-key-{key} .st-key-{buttonKey} button {{
                        background-color: white;
                        color: black;
                        border: 1px solid;
                        padding-left: 20px;
                        width: 100%;
                        display: block;
                        text-align: left;
                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);    
                    }}
                    .st-key-{key} .st-key-{buttonKey} button:hover {{
                        background-color: #f8fafc;
                        border-color: #3b82f6;
                    }}
                    .st-key-{key} .st-key-{buttonKey} button:focus {{
                        background-color: #eff6ff;
                        border-color: #3b82f6;
                        color: #1d4ed8;
                    }}           
                     .st-key-{key} .st-key-delete_{key} button {{
                        background-color: white;
                        color: black;
                        border: 1px solid;
                        padding-left: 20px;
                        width: 100%;
                        display: block;
                        text-align: left;
                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);    
                    }}
                    .st-key-{key} .st-key-delete_{key} button:hover {{
                        background-color: Red;
                        border-color: #black;
                    }}
                    .st-key-{key} .st-key-delete_{key} button:focus {{
                        background-color: Red;
                        border-color: black;
                        color: black;
                    }}  
                    </style>
                """, unsafe_allow_html=True)

            if st.button(name, key=buttonKey):
                # Log the button click and call the function
                on_click_function(name, id_value)
                clicked_name = name
                clicked_id = id_value

        if on_delete_function:
            # Create a delete button with custom styling
            to_delete = st.multiselect("Select to delete", names, key=f"delete_select_{key}", default=[])
            if st.button("Delete Selected", key=f"delete_{key}"):
                for name in to_delete:
                    id_value = map[name]
                    on_delete_function(name, id_value)

    return clicked_name, clicked_id



