import streamlit as st
import pandas as pd

def render(problems: pd.DataFrame, models: pd.DataFrame, environments: pd.DataFrame):
    st.markdown('<div id="ctf" class="section-anchor"></div>', unsafe_allow_html=True)
    st.header("CTF")
    tab1, tab2 = st.tabs(["New Evaluation", "Queue / Active Jobs"])
    with tab1:
        st.subheader("New Evaluation Wizard")
        st.write("A multi-step form to create a new run will be here.")
    with tab2:
        st.subheader("Queue / Active Jobs")
        st.write("Operational view of runs.")