import streamlit as st

from voluntary_work_calendar.utils import menu_button, open_page


def check_login():
    if "role" in st.session_state.keys():
        if st.session_state.role != "user":
            st.switch_page("pages/0_not_logged.py")
        else:
            pass
    else:
        st.switch_page("pages/0_not_logged.py")


def init_user_page():
    #: Set page config
    st.set_page_config(
        page_title="Calendario - Home page",
        initial_sidebar_state=st.session_state.sidebar_state,
    )
    menu_button()
    set_sidebar()
    st.header("Benvenuto {}".format(st.session_state.user_name))
    st.write("Clicca il pulsante menù per accedere al pannello di controllo.")
    st.write("Una volta aperto il pannello di controllo:")
    st.write(
        "- Per vedere le persone che hanno confermato la loro presenza clicca **Calendario**  \n- Per inserire una presenza clicca **Inserisci presenza**  \n- Per rimuovere la presenza clicca **Cancella presenza**"
    )


def set_sidebar():
    #: Show a navigation menu for authenticated
    with st.sidebar:
        calendar = st.button(label="Calendario", on_click=open_page, args=("calendar",))
        insert = st.button(
            label="Inserisci presenza", on_click=open_page, args=("insert",)
        )
        delete = st.button(
            label="Cancella presenza", on_click=open_page, args=("delete",)
        )
        admin = st.button(label="Impostazioni", on_click=open_page, args=("admin",))
        logout = st.button(label="Esci", on_click=open_page, args=("logout",))
        if calendar:
            st.switch_page("pages/1_calendar.py")
        if insert:
            st.switch_page("pages/2_insert.py")
        if delete:
            st.switch_page("pages/3_delete.py")
        if admin:
            st.switch_page("pages/4_admin.py")
        if logout:
            st.switch_page("pages/0_logout.py")
