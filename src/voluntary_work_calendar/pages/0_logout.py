import streamlit as st

st.session_state.user_name = None
st.session_state.role = None
st.session_state["admin"] = False
st.switch_page("app.py")
