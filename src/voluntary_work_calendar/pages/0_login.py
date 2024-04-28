import streamlit as st

from voluntary_work_calendar.auth.authorization import authenticate_user


#: Set gateway
st.session_state["gateway"] = "csv"
with st.container():
    _, middle_col, _ = st.columns(3)
    with middle_col:
        st.subheader("Login")
        with st.form("login_form", clear_on_submit=True):
            user_name = st.text_input("Username")
            user_psw = st.text_input("Password", type="password")
            login_button = st.form_submit_button("Entra")
        if login_button:
            authenticate_user(username=user_name, password=user_psw)
