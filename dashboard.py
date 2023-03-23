import streamlit as st
from streamlit_autorefresh import st_autorefresh
import pandas as pd
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode
import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
try:
    socket.bind("tcp://*:5555")
except:
    pass
temp = 0
st.set_page_config(
    page_title="Sofa",
    page_icon="❅",
    layout="wide",
)

st.title('Smart operational fridge App')

placeholder = st.empty()

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        .css-r698ls {visibility: hidden;}
        .css-qri22k {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)
st_autorefresh(interval=2 * 1000, key="dataframerefresh")


def aggrid_interactive_table(df: pd.DataFrame, height: int, side_bar: bool):
    """Creates an st-aggrid interactive table based on a dataframe.

    Args:
        df (pd.DataFrame]): Source dataframe

    Returns:
        dict: The selected row
    """
    options = GridOptionsBuilder.from_dataframe(
        df, enableRowGroup=True, enableValue=True, enablePivot=True
    )
    if side_bar:
        options.configure_side_bar()

    options.configure_selection("single")
    selection = AgGrid(
        df,
        enable_enterprise_modules=True,
        gridOptions=options.build(),
        theme="light",
        update_mode=GridUpdateMode.MODEL_CHANGED,
        allow_unsafe_jscode=True,
        height=height
    )
    return selection


with placeholder.container():
    st.markdown("###           ")
    kpi1, kpi2 = st.columns(2)
    kpi1.metric(
        label="Temperature actuelle",
        value="{}C°".format(temp),
    )

    kpi2.metric(
        label="Temperature maximale",
        value="{}C°".format(4),
    )

temp = socket.recv()
