import streamlit as st
import pandas as pd

def render(models: pd.DataFrame, benchmarks: pd.DataFrame, runs: pd.DataFrame):
    st.markdown('<div id="models" class="section-anchor"></div>', unsafe_allow_html=True)
    st.header("Model Hub")
    st.write("Pick what to run with; manage configs.")
 
    # Custom CSS for shadcn/ui feel
    st.markdown("""
    <style>
        [data-testid="stDataFrame"] {
            border: none;
        }
        [data-testid="stDataFrame"] thead th {
            background-color: #fafafa;
            border-bottom: 1px solid #d0d0d0;
            font-size: 14px;
            font-weight: 600;
            padding: 12px 16px;
        }
        [data-testid="stDataFrame"] tbody tr {
            border-bottom: 1px solid #f0f0f0;
        }
        [data-testid="stDataFrame"] tbody td {
            padding: 12px 16px;
            font-size: 14px;
            vertical-align: middle;
        }
        [data-testid="stDataFrameColumnMenu"] div[role="menuitem"] {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 8px 12px;
            line-height: 1.5;
            min-height: 32px;
        }
    </style>
    """, unsafe_allow_html=True)
 
    # Merge data to get benchmark results
    merged_data = pd.merge(runs, benchmarks, left_on='problem_id', right_on='id')
     
    # Assign model names to runs
    model_id_to_name = models.set_index('Model').reset_index().reset_index().set_index('index')['Model']
    merged_data['Model'] = merged_data['model_id'].map(model_id_to_name)
 
    # Pivot to get benchmarks as columns
    pivot_df = merged_data.pivot_table(index='Model', columns='title', values='success_rate').reset_index()
 
    # Merge with models dataframe
    models_with_benchmarks = pd.merge(models, pivot_df, on='Model', how='left')
 
    # Allow user to select benchmarks
    all_benchmarks = benchmarks['title'].tolist()
    selected_benchmarks = st.multiselect("Select benchmarks to display:", all_benchmarks, default=all_benchmarks[:2])
 
    # Filter columns to display
    base_columns = ['Organization', 'Model', 'License', 'Parameters (B)', 'Context', 'Input $/M', 'Output $/M', 'Knowledge Cutoff']
    columns_to_show = base_columns + selected_benchmarks
     
    # Ensure selected benchmark columns exist, fill missing with NaN
    for bench in selected_benchmarks:
        if bench not in models_with_benchmarks.columns:
            models_with_benchmarks[bench] = pd.NA
 
    models_display = models_with_benchmarks[columns_to_show].copy()
     
    # Display interactive dataframe
    st.dataframe(
        models_display,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Organization": st.column_config.TextColumn("Organization"),
            "Input $/M": st.column_config.TextColumn("Input $/M"),
            "Output $/M": st.column_config.TextColumn("Output $/M"),
            "Context": st.column_config.NumberColumn("Context", format="%.0f"),
            **{bench: st.column_config.NumberColumn(bench, format="%.1f%%") for bench in selected_benchmarks}
        }
    )
 
   
   