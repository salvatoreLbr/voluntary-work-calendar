from datetime import datetime
import streamlit as st

from voluntary_work_calendar.db.gateway import CSVGateway, DBGateway
from voluntary_work_calendar.menu import check_login, set_sidebar
from voluntary_work_calendar.utils import (
    hide_sidebar,
    menu_button,
    show_available_volunteers,
)


#: Set gateway
gateway = CSVGateway() if st.session_state.gateway == "csv" else DBGateway()

#: Streamlit set_page_config method has a 'initial_sidebar_state' argument that controls sidebar state.
st.set_page_config(
    page_title="Calendario presenze",
    initial_sidebar_state=st.session_state.sidebar_state,
)

#: Show menu button
menu_button()

#: Init check
check_login()
set_sidebar()

calendar_df = gateway.get_calendar()
if calendar_df.shape[0] == 0:
    st.warning(
        "Non è stata inserita ancora nessuna presenza. \n Clicca su 'Inserisci presenza' per definire un calendario."
    )
else:
    with st.container():
        st.write("Seleziona una data per vedere chi sarà presente in struttura")
        data_selected = st.date_input(
            label="Calendario",
            on_change=show_available_volunteers,
            key="selected_date",
            value=datetime.strptime(st.session_state["selected_date_str"], "%Y-%m-%d")
            if "selected_date_str" in st.session_state.keys()
            else datetime.today().date(),
            format="DD/MM/YYYY",
        )

        #: Show presences
        if "selected_date_str" in st.session_state.keys():
            if "calendar_df" in st.session_state.keys():
                selected_date_str = st.session_state["selected_date_str"]
                idx = calendar_df.data == selected_date_str
                if idx.sum() > 0:
                    availables_volunteers = calendar_df.loc[
                        idx, ["name", "orario_da", "orario_a"]
                    ].values
                    st.write("Volontari presenti il {}:".format(selected_date_str))
                    for v in availables_volunteers:
                        st.write(
                            "- {} sarà presente dalle {} alle {}".format(
                                v[0], v[1], v[2]
                            )
                        )
                else:
                    st.warning("Nessun volontario sarà presente in questa data")

#: Hide sidebar
if (st.session_state.sidebar_state == "expanded") and (
    st.session_state.menu_button_clicked == False
):
    hide_sidebar()
    st.rerun()
