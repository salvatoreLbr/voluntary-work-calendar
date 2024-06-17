import streamlit as st


class Config(object):
    DATABASE_NAME = st.secrets.db_credentials.DATABASE_NAME
    DATABASE_USER = st.secrets.db_credentials.DATABASE_USER
    DATABASE_PSW = st.secrets.db_credentials.DATABASE_PSW
    DATABASE_URL_AIVEN = "mysql+pymysql://{}:{}@calendar-voluntary-db-calendar-voluntary.g.aivencloud.com:28967/{}".format(
        DATABASE_USER, DATABASE_PSW, DATABASE_NAME
    )
    GATEWAY_TYPE = st.secrets.db_credentials.GATEWAY_TYPE
    USERNAME_USER = st.secrets.db_credentials.USERNAME_USER
    PSW_USER = st.secrets.db_credentials.PSW_USER
    USERNAME_ADMIN = st.secrets.db_credentials.USERNAME_ADMIN
    PSW_ADMIN = st.secrets.db_credentials.PSW_ADMIN
    ROUNDS = st.secrets.login.ROUNDS
