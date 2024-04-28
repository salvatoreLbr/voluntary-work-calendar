from datetime import datetime
import streamlit as st

from voluntary_work_calendar.db.gateway import DBGateway


def hide_sidebar():
    st.session_state.sidebar_state = 'collapsed'


def menu_button():
    st.markdown(
        """
        <style>
            div[data-testid="column"]
            {
                text-align: center;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    col_menu = st.columns([1])
    #: Toggle sidebar state between 'expanded' and 'collapsed'.
    with col_menu[0]:
        menu_button = st.button('Menù')
        if menu_button:
            st.session_state.menu_button_clicked = True
            st.session_state.sidebar_state = 'expanded'
            st.rerun()


def open_page(page: str):
    st.session_state.menu_button_clicked = False


def show_available_volunteers():
    gateway = DBGateway()
    calendar_df = gateway.get_calendar()
    selected_date = st.session_state.selected_date
    st.session_state["selected_date_str"] = datetime.strftime(selected_date, "%Y-%m-%d")
    st.session_state["calendar_df"] = calendar_df
