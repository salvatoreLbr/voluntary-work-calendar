import streamlit as st

from voluntary_work_calendar.auth.authorization import verify_hash
from voluntary_work_calendar.db.gateway import CSVGateway, DBGateway
from voluntary_work_calendar.menu import check_login, set_sidebar
from voluntary_work_calendar.utils import hide_sidebar, menu_button


#: Set gateway
gateway = CSVGateway() if st.session_state.gateway == "csv" else DBGateway()

#: Set page config
st.set_page_config(
    page_title="Calendario - Area Admin",
    initial_sidebar_state=st.session_state.sidebar_state,
)

#: Show menu button
menu_button()

#: Init check
check_login()
set_sidebar()

with st.container():
    _, middle_col, _ = st.columns(3)
    with middle_col:
        st.header("Area amministratore")
        with st.form("admin_form", clear_on_submit=True):
            user_psw = st.text_input("Password", type="password")
            login_button = st.form_submit_button("Sblocca area")
        if login_button:
            users_df = gateway.get_user()
            users_df = users_df.loc[users_df.username == "admin"]
            if users_df.shape[0] == 0:
                st.warning("Non vi è stato definito un admin per questo sito")
            else:
                hashed_psw = users_df["hashed_password"].values[0]
                if verify_hash(user_psw, hashed_psw):
                    st.session_state["admin"] = True
                else:
                    st.session_state["admin"] = False

#: Panel showed only if you are admin and you put corret password
if "admin" in st.session_state.keys():
    if st.session_state["admin"]:
        with st.container():
            st.subheader("Gestisci volontari")
            #: Add volunteer
            with st.expander("Inserisci nuovi volontari"):
                with st.form("add_volunteer", clear_on_submit=True):
                    volunteer_name = st.text_input("Nome volontario")
                    add_volunteer_button = st.form_submit_button("Aggiungi")
                    if add_volunteer_button:
                        gateway.insert_new_volunteer(name=volunteer_name)
            #: Remove volunteer
            with st.expander("Rimuovi volontari"):
                volunteers_name_list = gateway.get_volunteers_name()
                if len(volunteers_name_list) > 0:
                    with st.form("delete_volunteer", clear_on_submit=True):
                        volunteer_name_selected = st.selectbox(
                            label="Seleziona il volontario da eliminare",
                            options=sorted(volunteers_name_list),
                        )
                        remove_volunteer_button = st.form_submit_button("Rimuovi")
                        if remove_volunteer_button:
                            gateway.delete_volunteer(name=volunteer_name_selected)
                else:
                    st.info("Non ci sono volontari in lista")

#: Hide sidebar
if (st.session_state.sidebar_state == "expanded") and (
    st.session_state.menu_button_clicked == False
):
    hide_sidebar()
    st.rerun()
