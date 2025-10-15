import streamlit as st
import pandas as pd
import time

def render(running_jobs, queued_jobs):
    """
    Renders the view queue page.
    """
    st.markdown('<div id="view_queue" class="section-anchor"></div>', unsafe_allow_html=True)
    st.header("Job Queue")


    with st.container():
        c1, c2, c3 = st.columns(3)
        with c1:
            st.selectbox("Filter by Benchmark", ["All", "Benchmark A", "Benchmark B"], key="queue_filter_bm")
        with c2:
            st.selectbox("Filter by Model", ["All", "Model X", "Model Y"], key="queue_filter_model")
        with c3:
            st.text_input("Filter by User", key="queue_filter_user", placeholder="Username...")

    st.divider()


    with st.container():
        col1, col2 = st.columns([1, 1])
        with col1:
            st.subheader("System Status")
            sc1, sc2, sc3 = st.columns(3)
            sc1.metric("GPU Utilization", "78%", "-2%")
            sc2.metric("CPU Utilization", "54%", "+5%")
            sc3.metric("Active Jobs", "3")
            if st.button("Refresh", key="queue_refresh"):
                st.rerun()
            st.caption(f"Last updated: {time.strftime('%Y-%m-%d %H:%M:%S')}")

        with col2:
            st.subheader("Estimated Wait Time")
            st.info("Your job would be **#2** in the queue. Estimated start in **~5 minutes**.")

    st.divider()


    st.subheader("Running Jobs")

    running_data = {
        'Job ID': ['job-123', 'job-456', 'job-789'],
        'User': ['user-a', 'user-b', 'user-a'],
        'Model': ['Model X', 'Model Y', 'Model X'],
        'Benchmark': ['Benchmark A', 'Benchmark B', 'Benchmark A'],
        'Profile': ['Kali', 'Python', 'Kali'],
        'GPU': ['A100', 'None', 'RTX'],
        'Network': ['Egress', 'Full', 'Egress'],
        'Started': ['5m ago', '12m ago', '20m ago'],
        'Progress %': [75, 50, 25]
    }
    running_df = pd.DataFrame(running_data)
    st.dataframe(running_df, use_container_width=True, hide_index=True)


    st.subheader("Queued Jobs")

    queued_data = {
        'Position': [1, 2, 3, 4],
        'User': ['user-c', 'user-d', 'user-e', 'user-f'],
        'Model': ['Model Z', 'Model Y', 'Model X', 'Model Z'],
        'Benchmark': ['Benchmark C', 'Benchmark B', 'Benchmark A', 'Benchmark C'],
        'Profile': ['Custom', 'Python', 'Kali', 'Custom'],
        'Requested At': ['2m ago', '8m ago', '15m ago', '30m ago'],
        'Est. Start': ['~2m', '~5m', '~10m', '~15m']
    }
    queued_df = pd.DataFrame(queued_data)
    st.dataframe(queued_df, use_container_width=True, hide_index=True)