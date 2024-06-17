import streamlit as st

from voluntary_work_calendar.config import Config
from voluntary_work_calendar.db.gateway import CSVGateway, DBGateway
from voluntary_work_calendar.menu import init_user_page


#: Set gateway
gateway = CSVGateway() if Config.GATEWAY_TYPE == "csv" else DBGateway()
gateway.init_db()

# Initialize st.session_state.role to None
if "role" not in st.session_state:
    st.session_state.role = None
    st.switch_page("pages/0_not_logged.py")
else:
    if st.session_state.role == "user":
        init_user_page()
    else:
        st.switch_page("pages/0_not_logged.py")
