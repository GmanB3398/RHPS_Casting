import pandas as pd
from streamlit_dynamic_filters import DynamicFilters

import streamlit as st
from src.classes.cast_generator import CastGenerator

st.title("Get All Rocky Horror Casts")
roles_file = st.file_uploader("Upload Roles", type="csv")
preferences_file = st.file_uploader("Upload Preferences", type="csv")

if roles_file is not None and preferences_file is not None:
    roles = pd.read_csv(roles_file)
    preferences = pd.read_csv(preferences_file)
    available_members = preferences["member"].to_list()
    cg = CastGenerator(available_members=available_members, roles=roles, preferences=preferences)
    df = cg.get_all_casts()

    filters = DynamicFilters(df, filters=cg.roles_list)

    with st.sidebar:
        filters.display_filters()

    filters.display_df()
