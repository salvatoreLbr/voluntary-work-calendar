import streamlit as st


#: init sidebar
st.session_state["sidebar_state"] = 'collapsed'
st.switch_page("pages/0_login.py")
