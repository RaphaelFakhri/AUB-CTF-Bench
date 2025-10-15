import pandas as pd

def load_mock_data():
    models = pd.DataFrame([
        {'Country': '🇺🇸', 'Organization': 'Google', 'Model': 'GPT-4V', 'License': 'Proprietary', 'Parameters (B)': 175, 'Context': '128K', 'Input $/M': 0.01, 'Output $/M': 0.03, 'Knowledge Cutoff': '2023-04'},
        {'Country': '🇺🇸', 'Organization': 'Anthropic', 'Model': 'Claude-3 Opus', 'License': 'Proprietary', 'Parameters (B)': None, 'Context': '200K', 'Input $/M': 0.015, 'Output $/M': 0.075, 'Knowledge Cutoff': '2023-12'},
        {'Country': '🇫🇷', 'Organization': 'Mistral', 'Model': 'Llama-3 70B', 'License': 'Open Source', 'Parameters (B)': 70, 'Context': '8K', 'Input $/M': 0.0008, 'Output $/M': 0.0008, 'Knowledge Cutoff': '2023-03'},
    ])

    benchmarks = pd.DataFrame([
        {'id': 1, 'title': 'Web Vuln 1', 'statement': 'Find the flag in the web page.', 'assets': 'image.png', 'category': 'Web', 'difficulty': 'Easy', 'expected_flag': 'flag{...}', 'scorer': 'exact_match'},
        {'id': 2, 'title': 'Pwn Buffer', 'statement': 'Exploit the buffer overflow.', 'assets': 'binary', 'category': 'Pwn', 'difficulty': 'Medium', 'expected_flag': 'flag{...}', 'scorer': 'exact_match'},
        {'id': 3, 'title': 'Crypto RSA', 'statement': 'Decrypt the message.', 'assets': 'crypto.txt', 'category': 'Crypto', 'difficulty': 'Hard', 'expected_flag': 'flag{...}', 'scorer': 'exact_match'},
    ])

    environments = pd.DataFrame([
        {'id': 1, 'name': 'Kali Linux', 'image/tag': 'kalilinux/kali-rolling:latest', 'tools': 'pwntools, nmap', 'limits': '2 CPU, 4GB RAM', 'digest': 'sha256:...'},
        {'id': 2, 'name': 'Headless Browser', 'image/tag': 'browserless/chrome:latest', 'tools': 'selenium', 'limits': '1 CPU, 2GB RAM', 'digest': 'sha256:...'},
    ])

    runs = pd.DataFrame([
        {'id': 1, 'problem_id': 1, 'environment_id': 2, 'model_id': 1, 'params': {'temp': 0.5}, 'status': 'succeeded', 'metrics': [{'solved': True, 'ttf': 120, 'tokens': 1500, 'cost': 0.015}], 'artifacts': 'log.txt', 'logs': '...', 'flag_found': 'flag{...}', 'timestamps': '...', 'success_rate': 85},
        {'id': 2, 'problem_id': 2, 'environment_id': 1, 'model_id': 3, 'params': {'temp': 0.7}, 'status': 'failed', 'metrics': [{'solved': False, 'ttf': None, 'tokens': 3000, 'cost': 0.0024}], 'artifacts': 'log.txt', 'logs': '...', 'flag_found': None, 'timestamps': '...', 'success_rate': 60},
        {'id': 3, 'problem_id': 1, 'environment_id': 1, 'model_id': 3, 'params': {'temp': 0.6}, 'status': 'succeeded', 'metrics': [{'solved': True, 'ttf': 100, 'tokens': 1000, 'cost': 0.001}], 'artifacts': 'log.txt', 'logs': '...', 'flag_found': 'flag{...}', 'timestamps': '...', 'success_rate': 75},
    ])
    
    return models, benchmarks, environments, runs

def load_queue_data():
    running_jobs = pd.DataFrame({
        'Job ID': ['J-84B12', 'J-92C8F', 'J-A1D05'],
        'User': ['Alice', 'Bob', 'Charlie'],
        'Model': ['GPT-4o', 'Claude 3 Opus', 'Llama 3 70B'],
        'Benchmark': ['Code-Gen-Python', 'Doc-Q&A', 'Creative-Writing'],
        'Started': ['8m ago', '3m ago', '1m ago']
    })
    queued_jobs = pd.DataFrame({
        'Position': [1],
        'User': ['David'],
        'Model': ['Gemini 1.5 Pro'],
        'Benchmark': ['Code-Gen-Python']
    })
    return running_jobs, queued_jobs