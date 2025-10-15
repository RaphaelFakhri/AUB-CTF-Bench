import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- Mock Data ---
# Refined mock data with more benchmarks for a richer graph
MODELS_DATA = {
    "GPT-4o": {
        "name": "GPT-4o",
        "organization": "OpenAI",
        "is_multimodal": True,
        "context_size": "128k",
        "cutoff_date": "Oct 2023",
        "cost_input_pm": 2.5,
        "cost_output_pm": 10.0,
        "max_output": "4k",
        "latency_s": 0.51,
        "speed_tps": 143,
        "color": "#9FC9FF",
        "benchmarks": {
            "MMMU": 85.3,
            "MathVista": 72.1,
            "DocVQA": 90.2,
            "ChartQA": 80.8,
            "AI2D": 88.5,
            "MMLU": 88.4,
            "HumanEval": 90.2
        }
    },
    "Claude 3.5 Sonnet": {
        "name": "Claude 3.5 Sonnet",
        "organization": "Anthropic",
        "is_multimodal": True,
        "context_size": "200k",
        "cutoff_date": "Apr 2024",
        "cost_input_pm": 3.0,
        "cost_output_pm": 15.0,
        "max_output": "8k",
        "latency_s": 1.22,
        "speed_tps": 78,
        "color": "#FC69D3",
        "benchmarks": {
            "MMMU": 82.1,
            "MathVista": 68.5,
            "DocVQA": 88.9,
            "ChartQA": 79.1,
            "AI2D": 85.2,
            "MMLU": 85.0,
            "HumanEval": 88.1
        }
    },
    "Gemini 2.5 Pro": {
        "name": "Gemini 2.5 Pro",
        "organization": "Google",
        "is_multimodal": True,
        "context_size": "1M",
        "cutoff_date": "Jun 2024",
        "cost_input_pm": 2.0,
        "cost_output_pm": 8.0,
        "max_output": "16k",
        "latency_s": 0.8,
        "speed_tps": 110,
        "color": "#88d8b0",
        "benchmarks": {
            "MMMU": 89.0,
            "MathVista": 75.0,
            "DocVQA": 91.5,
            "ChartQA": 82.3,
            "AI2D": 90.1,
            "MMLU": 90.1,
            "HumanEval": 91.3
        }
    },
    "Llama 3.1 70B": {
        "name": "Llama 3.1 70B",
        "organization": "Meta",
        "is_multimodal": False,
        "context_size": "128k",
        "cutoff_date": "Mar 2024",
        "cost_input_pm": 1.0,
        "cost_output_pm": 3.0,
        "max_output": "16k",
        "latency_s": 1.5,
        "speed_tps": 60,
        "color": "#ff6b6b",
        "benchmarks": {
            "MMMU": 65.0, 
            "MathVista": 55.3,
            "DocVQA": 70.1,
            "ChartQA": 60.5,
            "AI2D": 68.0,
            "MMLU": 82.0,
            "HumanEval": 85.1
        }
    }
}

MODEL_NAMES = list(MODELS_DATA.keys())

def render(models: pd.DataFrame):
    st.markdown('<div id="compare" class="section-anchor"></div>', unsafe_allow_html=True)

    # --- Custom CSS for Styling (with Dark Mode support) ---
    st.markdown("""
    <style>
        /* Light Mode Styles */
        .compare-header h3, .compare-header h5 {
            color: #212529;
        }
        .compare-header p, .vs-text {
            color: #6c757d;
        }
        .model-card {
            background-color: #FFFFFF;
            border: 1px solid #dee2e6;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }
        .model-card-name {
            color: #212529;
        }
        .detail-item {
            background-color: #f8f9fa;
        }
        .detail-item-label {
            color: #6c757d;
        }
        .detail-item-value {
            color: #212529;
        }

        /* Dark Mode Overrides */
        body.dark-mode .compare-header h3, body.dark-mode .compare-header h5 {
            color: #FFFFFF;
        }
        body.dark-mode .compare-header p, body.dark-mode .vs-text {
            color: #a0a0a0;
        }
        body.dark-mode .model-card {
            background-color: #1E1E1E;
            border: 1px solid #333;
        }
        body.dark-mode .model-card-name {
            color: #FFFFFF;
        }
        body.dark-mode .detail-item {
            background-color: #2a2a2a;
        }
        body.dark-mode .detail-item-label {
            color: #a0a0a0;
        }
        body.dark-mode .detail-item-value {
            color: #FFFFFF;
        }

        /* General Styles */
        .compare-header h3 {
            font-size: 1.75rem; font-weight: bold;
        }
        .compare-header h5 {
             font-size: 1.2rem; font-weight: bold; margin-bottom: 1rem;
        }
        .compare-header p {
            font-size: 1.1rem;
        }
        .vs-text {
            text-align: center; padding-top: 2rem; font-size: 1.5rem;
        }
        .model-card {
            border-radius: 10px;
            padding: 1.5rem;
            height: 100%;
        }
        .model-card-header {
            display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1.5rem;
        }
        .model-color-dot {
            width: 14px; height: 14px; border-radius: 50%;
        }
        .model-card-name {
            font-size: 1.25rem; font-weight: bold;
        }
        .multimodal-badge {
            font-size: 0.75rem; padding: 3px 8px; border-radius: 15px; color: white; font-weight: 500;
        }
        .multimodal-true {
            background-color: #007bff;
        }
        .multimodal-false {
            background-color: #6c757d;
        }
        .detail-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
        }
        .detail-item {
            padding: 0.75rem; border-radius: 6px;
        }
        .detail-item-label {
            font-size: 0.8rem; margin-bottom: 0.25rem;
        }
        .detail-item-value {
            font-size: 1rem; font-weight: 500;
        }
    </style>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="compare-header"><h3>Compare models</h3><p>Select two models to compare</p></div>', unsafe_allow_html=True)

        # --- Model Selection ---
        col1, vs_col, col2 = st.columns([5, 1, 5])
        with col1:
            model1_name = st.selectbox("Model 1", MODEL_NAMES, index=0, key="compare_model1")
        with vs_col:
            st.markdown('<div class="vs-text">vs</div>', unsafe_allow_html=True)
        with col2:
            model2_name = st.selectbox("Model 2", MODEL_NAMES, index=1, key="compare_model2")

        model1_data = MODELS_DATA[model1_name]
        model2_data = MODELS_DATA[model2_name]

        st.write("""<div style="margin-top: 2rem;"></div>""", unsafe_allow_html=True)

        # --- Comparison Body ---
        if model1_name and model2_name:
            body_col1, body_col2 = st.columns([6, 6])

            # --- Left Column: Model Details Cards ---
            with body_col1:
                st.markdown("<div class='compare-header'><h5>Model Details</h5></div>", unsafe_allow_html=True)
                
                card_col1, card_col2 = st.columns(2)
                
                def make_card(model_data, col):
                    mm_class = "multimodal-true" if model_data['is_multimodal'] else "multimodal-false"
                    mm_text = "Multimodal" if model_data['is_multimodal'] else "Text-Only"
                    with col:
                        st.markdown(f'''
                        <div class="model-card">
                            <div class="model-card-header">
                                <div class="model-color-dot" style="background-color:{model_data['color']};"></div>
                                <div class="model-card-name">{model_data['name']}</div>
                                <span class="multimodal-badge {mm_class}">{mm_text}</span>
                            </div>
                            <div class="detail-grid">
                                <div class="detail-item"><div class="detail-item-label">Context</div><div class="detail-item-value">{model_data['context_size']}</div></div>
                                <div class="detail-item"><div class="detail-item-label">Cutoff</div><div class="detail-item-value">{model_data['cutoff_date']}</div></div>
                                <div class="detail-item"><div class="detail-item-label">I/O Cost ($/M)</div><div class="detail-item-value">{model_data['cost_input_pm']}/{model_data['cost_output_pm']}</div></div>
                                <div class="detail-item"><div class="detail-item-label">Max Output</div><div class="detail-item-value">{model_data['max_output']}</div></div>
                                <div class="detail-item"><div class="detail-item-label">Latency (s)</div><div class="detail-item-value">{model_data['latency_s']}</div></div>
                                <div class="detail-item"><div class="detail-item-label">Speed (t/s)</div><div class="detail-item-value">{model_data['speed_tps']}</div></div>
                            </div>
                        </div>
                        ''', unsafe_allow_html=True)

                make_card(model1_data, card_col1)
                make_card(model2_data, card_col2)

            # --- Right Column: Benchmark Graph ---
            with body_col2:
                st.markdown("<div class='compare-header'><h5>Standard Benchmarks</h5></div>", unsafe_allow_html=True)
                
                benchmarks1 = model1_data['benchmarks']
                benchmarks2 = model2_data['benchmarks']
                
                labels = list(benchmarks1.keys())
                values1 = list(benchmarks1.values())
                values2 = [benchmarks2.get(key, 0) for key in labels]

                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=labels,
                    y=values1,
                    name=model1_name,
                    marker=dict(
                        color=f'rgba({int(model1_data["color"][1:3], 16)}, {int(model1_data["color"][3:5], 16)}, {int(model1_data["color"][5:7], 16)}, 0.6)',
                        line=dict(color=model1_data['color'], width=2)
                    )
                ))
                fig.add_trace(go.Bar(
                    x=labels,
                    y=values2,
                    name=model2_name,
                    marker=dict(
                        color=f'rgba({int(model2_data["color"][1:3], 16)}, {int(model2_data["color"][3:5], 16)}, {int(model2_data["color"][5:7], 16)}, 0.6)',
                        line=dict(color=model2_data['color'], width=2)
                    )
                ))

                fig.update_layout(
                    barmode='group',
                    xaxis_tickangle=-45,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)', # Transparent background
                    font_color='#888', # Neutral font color
                    yaxis=dict(gridcolor='rgba(128,128,128,0.2)', gridwidth=1, zeroline=False, ticksuffix='%'),
                    xaxis=dict(showgrid=False),
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                    margin=dict(l=20, r=20, t=40, b=20),
                    bargap=0.15,
                    hovermode="x unified"
                )
                fig.update_traces(marker_cornerradius=5)
                st.plotly_chart(fig, use_container_width=True)
