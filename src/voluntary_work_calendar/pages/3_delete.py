import streamlit as st

from voluntary_work_calendar.config import Config
from voluntary_work_calendar.db.gateway import CSVGateway, DBGateway
from voluntary_work_calendar.menu import check_login, set_sidebar
from voluntary_work_calendar.utils import menu_button, hide_sidebar


#: Set gateway
gateway = CSVGateway() if Config.GATEWAY_TYPE == "csv" else DBGateway()

#: Set page config
st.set_page_config(
    page_title="Calendario - rimuovi presenza",
    initial_sidebar_state=st.session_state.sidebar_state,
)

#: Show menu button
menu_button()

#: Init check
check_login()
set_sidebar()
#: Get volunteer name list
volunteers_name_list = gateway.get_volunteers_name()

if len(volunteers_name_list) > 0:
    with st.form("rimuovi_presenza_form"):
        #: Create columns for date and volunteer
        col_data, col_volunteer = st.columns(2)
        with col_data:
            data = st.date_input(label="Data", format="DD/MM/YYYY")
        with col_volunteer:
            nome_volontario = st.selectbox(
                label="Volontario", options=sorted(volunteers_name_list)
            )

        submit_button = st.form_submit_button("Conferma")
        if submit_button:
            result = gateway.delete_presence(data=data, name=nome_volontario)
            if result:
                st.success("Presenza eliminata con successo")
else:
    st.warning(
        "Non c'è alcun volontario registrato. Inserisci almeno un volontario dal pannello 'Impostazioni'."
    )

#: Hide sidebar
if (st.session_state.sidebar_state == "expanded") and (
    st.session_state.menu_button_clicked == False
):
    hide_sidebar()
    st.rerun()
