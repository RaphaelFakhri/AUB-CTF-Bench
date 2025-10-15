import pandas as pd

def load_benchmarks():
    """Loads the benchmark data."""
    data = [
        {"Model": "Llama 2 7B", "Benchmark": "HumanEval", "Accuracy @ 20 pass": 0.8},
        {"Model": "Llama 2 7B", "Benchmark": "MMLU", "Accuracy @ 20 pass": 0.75},
        {"Model": "Code Llama 7B", "Benchmark": "HumanEval", "Accuracy @ 20 pass": 0.85},
        {"Model": "Code Llama 13B", "Benchmark": "MMLU", "Accuracy @ 20 pass": 0.9},
    ]
    return pd.DataFrame(data)
