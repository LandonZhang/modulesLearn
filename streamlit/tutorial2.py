import streamlit as st

with st.chat_message("assistant"):
    st.write("Hello, I'm a robot!")
    # st.page_link("pages/page1.py", label="Go to Page 1")

prompt = st.chat_input("Your message")
if prompt and "page2" in prompt:  # 先检查 prompt 不为 None
    st.switch_page("pages/page2.py")
