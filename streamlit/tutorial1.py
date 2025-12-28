import streamlit as st
import time

if "game" not in st.session_state:
    st.session_state.game = ""


@st.cache_data(ttl=60)
def get_cached_data():
    time.sleep(3)
    return "The last of US partII"


def after_click():
    game = get_cached_data()
    st.session_state.game = game


st.button("Click me to get data!", on_click=after_click)
st.markdown(f"The **game** show is: {st.session_state.game}")
