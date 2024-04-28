import streamlit as st


class Config(object):
    USERNAME_USER = st.secrets.db_credentials.USERNAME_USER
    PSW_USER = st.secrets.db_credentials.PSW_USER
    USERNAME_ADMIN = st.secrets.db_credentials.USERNAME_ADMIN
    PSW_ADMIN = st.secrets.db_credentials.PSW_ADMIN
    ROUNDS = st.secrets.login.ROUNDS
