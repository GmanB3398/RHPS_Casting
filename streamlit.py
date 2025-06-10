import pandas as pd
from streamlit_dynamic_filters import DynamicFilters

import streamlit as st
from src.classes.cast_generator import CastGenerator, clean_inputs

st.title("Get All Rocky Horror Casts")

roles_file = st.file_uploader("Upload Allowed Roles", type="csv")
preferences_file = st.file_uploader("Upload Preferred Roles", type="csv")
roles = None
preferences = None
config = {}
error = False

if roles_file is not None:
    roles = clean_inputs(pd.read_csv(roles_file))
    if isinstance(roles, str):
        st.error("Error in Allowed Roles File: " + roles)
        error = True

if preferences_file is not None:
    preferences = clean_inputs(pd.read_csv(preferences_file))
    if isinstance(preferences, str):
        st.error("Error in Preferences File: " + preferences)
        error = True

if roles is not None and preferences is not None and not error:
    # for role in roles_list:
    #     config[role] = st.number_input(role, default_score_config.get(role))
    available_members = preferences["member"].to_list()
    cg = CastGenerator(available_members=available_members, roles=roles, preferences=preferences)
    df = cg.get_all_casts()

    filters = DynamicFilters(df, filters=cg.roles_list)

    if not df.empty:
        with st.sidebar:
            filters.display_filters()
        filters.display_df()
    else:
        st.markdown("## No Casts Able to Be Made with Current Roles/Actors")
