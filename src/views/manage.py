import streamlit as st
import pandas as pd
from src.views import add_ctf

def render():
    st.markdown('<div id="manage" class="section-anchor"></div>', unsafe_allow_html=True)
    st.header("ADD CTF")
    tab1, tab2, tab3 = st.tabs(["Add CTF", "Add CTF (Bulk)", "Search"])

    with tab1:
        add_ctf.render()

    with tab2:
        st.subheader("Add CTF Challenges in Bulk")
        st.file_uploader("Upload a zip file containing CTF challenges", type=["zip"])

    with tab3:
        st.subheader("Search")
        st.write("A searchable store of run outputs will be here.")




