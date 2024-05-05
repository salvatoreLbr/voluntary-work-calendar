import datetime
import streamlit as st

from voluntary_work_calendar.db.gateway import CSVGateway, DBGateway
from voluntary_work_calendar.menu import check_login, set_sidebar
from voluntary_work_calendar.utils import hide_sidebar, menu_button


#: Set gateway
gateway = CSVGateway() if st.session_state.gateway == "csv" else DBGateway()

#: Set page config
st.set_page_config(
    page_title="Calendario - inserisci presenza",
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
    with st.form("inserisci_presenza_form"):
        #: Create columns for date and volunteer
        col_data, col_volunteer = st.columns(2)
        with col_data:
            data = st.date_input(label="Data", format="DD/MM/YYYY")
        with col_volunteer:
            nome_volontario = st.selectbox(
                label="Volontario", options=sorted(volunteers_name_list)
            )
        st.write("Seleziona l'orario di inizio e di fine del turno")
        #: Create columns for time
        col_from, col_to = st.columns(2)
        with col_from:
            orario_from = st.time_input(label="Dalle", value=datetime.time(10, 00))
            orario_from_str = (
                str(orario_from.hour) + ":" + str(orario_from.minute).zfill(2)
            )
        with col_to:
            orario_to = st.time_input(label="Alle", value=datetime.time(18, 00))
            orario_to_str = str(orario_to.hour) + ":" + str(orario_to.minute).zfill(2)

        submit_button = st.form_submit_button("Conferma")
        if submit_button:
            if orario_to <= orario_from:
                st.warning(
                    "!!! Attenzione è stato selezionato un orario di fine turno anteriore all'orario di inizio turno !!!"
                )
                raise Exception(
                    "!!! Attenzione è stato selezionato un orario di fine turno anteriore all'orario di inizio turno !!!"
                )
            gateway.insert_presence(
                data=data,
                orario_from=orario_from_str,
                orario_to=orario_to_str,
                name=nome_volontario,
            )
            st.success("Presenza inserita con successo")
else:
    st.warning(
        "Non c'è alcun volontario registrato. Inserisci almeno un volontario dal pannello 'Impostazioni' prima di aggiungere il suo turno."
    )

#: Hide sidebar
if (st.session_state.sidebar_state == "expanded") and (
    st.session_state.menu_button_clicked == False
):
    hide_sidebar()
    st.rerun()
