# AUB-CTF-Bench (Streamlit Version - Attempt 3)

## Overview
AUB-CTF-Bench is a multi-modal LLM benchmarking platform for Capture The Flag (CTF) challenges. This Streamlit implementation provides a complete frontend with mocked backend functionalities, focusing on image uploads for vision analysis, model leaderboards, benchmarks, evaluations, and comparisons. All data is mocked locally for demonstration.

## Features
- **Home**: Image upload with mock vision analysis (flag detection, accuracy sim), dynamic metrics (solve rate, token efficiency), quick actions, top models teaser.
- **Models**: Interactive table with sorting/filtering (provider, category), actions (run CTF, view stats).
- **Benchmarks**: Filterable card grid (modality, categories), details with Plotly line charts (solve/vision rates) and evaluations table.
- **Compare**: Select two models, Plotly line chart comparison, summary table with winner.
- **CTF**: Mock challenges table, analyze buttons with success messages.
- **About**: Team bios in columns.
- **Thesis**: Mock PDF preview, download/BibTeX buttons.
- **UX**: Sidebar navigation, responsive layout, session state for persistence, Plotly for visualizations, PIL for image handling.

All backend (e.g., API calls, DB) is mocked with local dataframes and random simulations.

## Setup
1. Navigate to the project: `cd /home/raph/thesis/attempt-3`
2. Activate virtual environment: `source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`

## Run the App
- Start the Streamlit server: `streamlit run main.py`
- Open in browser: http://localhost:8501
- Use sidebar to navigate.

## Dependencies
See `requirements.txt` for full list (streamlit, pandas, plotly, pillow, numpy, requests).

## Testing
- **Upload**: Home page, drag PNG/JPG → see analysis toast, metrics update.
- **Models**: Filter by provider/category, select for actions.
- **Benchmarks**: Filter, click details → view chart/table.
- **Compare**: Select models → see comparison plot/table.
- **CTF**: Select challenge → Analyze button.
- Responsive: Works on mobile/desktop.
- No errors: Console clean, all interactions mocked.

## Mocking Notes
- Vision analysis: Random flag/accuracy on upload.
- Metrics: Update via session_state on interactions.
- Data: Static DataFrames, no real backend.
- Charts: Plotly for interactive viz.

## Future
- Integrate real backend (Flask/FastAPI).
- Add auth, real LLM calls (OpenAI API).
- Docker support.
- Kali Linux integration for CTF tools.

For issues: Check terminal for Streamlit logs.
