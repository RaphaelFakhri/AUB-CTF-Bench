import streamlit as st
import pandas as pd

def render(problems: pd.DataFrame, runs: pd.DataFrame):
    st.markdown('<div id="problems_results" class="section-anchor"></div>', unsafe_allow_html=True)
    st.header("Problems & Results")
    tab1, tab2, tab3 = st.tabs(["Problem Library", "Results & Analytics", "Leaderboards"])
    with tab1:
        st.subheader("Problem Library")
        st.dataframe(problems)
    with tab2:
        st.subheader("Results & Analytics")
        st.write("Charts and data export will be here.")
        st.dataframe(runs)
    with tab3:
        st.subheader("Leaderboards")
        st.write("Rankings for models and problems will be here.")