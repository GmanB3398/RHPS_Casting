import streamlit as st
import pandas as pd
from src.classes.cast_generator import CastGenerator
    

st.title("All Casts")
roles_file = st.file_uploader('Upload Roles', type='csv')
preferences_file = st.file_uploader('Upload Preferences', type='csv')

if roles_file is not None and preferences_file is not None:
    roles = pd.read_csv(roles_file)
    preferences =pd.read_csv(preferences_file)
    available_members = preferences["member"].to_list()
    df = CastGenerator(
    available_members=available_members, roles=roles, preferences=preferences
    ).get_all_casts()
    
    st.write(df)