import streamlit as st
from sqlalchemy.orm.session import Session

from voluntary_work_calendar.auth.password import check_rules_password, get_hash, verify_hash
from voluntary_work_calendar.db.crud import (
    create_table,
    get_table,
)
from voluntary_work_calendar.db.gateway import CSVGateway, DBGateway
from voluntary_work_calendar.db.models import Users


def authenticate_user(username: str, password: str) -> Users:
    gateway = CSVGateway() if st.session_state.gateway == "csv" else DBGateway()
    users_df = gateway.get_user()
    #: Check if there is almost an user
    if users_df.shape[0] == 0:
        st.switch_page("app.py")
    #: Get username if exists
    idx_username = users_df.username == username
    set_user = True
    if idx_username.sum() == 0:
        set_user = False
        st.warning("L'utente non esiste")
        raise Exception()
    #: Check password
    user_password = users_df.loc[idx_username, "hashed_password"].values[0]
    if not verify_hash(password, user_password):
        set_user = False
        st.warning("Password errata")
        raise Exception()
    #: Get username and retrieve page
    user_name = users_df.loc[idx_username, "username"].values[0]
    user_id = users_df.loc[idx_username, "id"].values[0]
    if set_user:
        st.session_state["user_name"] = user_name
        st.session_state["user_id"] = user_id
        st.session_state.role = "user"
        st.session_state.sidebar_state = 'collapsed'
        st.session_state.menu_button_clicked = False
    st.switch_page("app.py")


def create_new_user(db: Session, username: str, password: str) -> str:
    error_in_psw, type_response = check_rules_password(psw=password)
    if error_in_psw:
        raise Exception(
            "!!! Password not valid for this reason: {} !!!".format(
                type_response
            )
        )
    users_df = get_table(db_session=db, model=Users)
    if users_df.shape[0] > 0:
        #: Check if username is already used
        idx_username = users_df.username == username
        if idx_username.sum() > 0:
            raise Exception("!!! username already used !!!")
    else:
        print("Users table not set yet")
    create_table(
        db_session=db,
        model=Users,
        info=[
            {
                "username": username,
                "role": "user",
                "hashed_password": get_hash(password),
            }
        ],
    )
