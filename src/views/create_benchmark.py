import streamlit as st
import pandas as pd

def render():
    """Renders the Create Benchmark page."""
    st.markdown('<div id="create_benchmark" class="section-anchor"></div>', unsafe_allow_html=True)
    st.header("Create Benchmark")
    st.caption("Define a benchmark that selects a set of CTFs and owns the environment/tools, evaluation metrics, and limits.")


    with st.expander("1. Definition", expanded=True):
        st.text_input("Name", key="bm_name", placeholder="e.g., AI Safety Hardening Q1")
        st.text_area("Description (Markdown)", key="bm_desc_md", placeholder="A benchmark to test AI model resilience against prompt injection attacks...")
        
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox("Visibility", ["Private", "Unlisted", "Public"], key="bm_visibility", help="Private: Only you can see. Unlisted: Anyone with the link. Public: Discoverable by all.")
            st.selectbox("Tasks Modality", ["Text", "Image", "Code", "Binary", "Mixed"], key="bm_modality")
        with col2:
            st.multiselect("Domains", ["Web", "Pwn", "Crypto", "Forensics", "Rev", "OSINT", "Stego", "Mobile", "Cloud", "AI", "Misc"], key="bm_domains")


    with st.expander("2. Dataset"):
        source = st.radio("Source", ["Select existing CTFs", "Upload ZIP of CTFs"], key="bm_dataset_source", horizontal=True)
        
        if source == "Select existing CTFs":

            st.multiselect("Select CTFs by slug", ["ctf-101", "pwn-pro", "web-warrior"], key="bm_ctf_slugs")
        else:
            st.file_uploader("Upload CTF bundle (.zip)", type=["zip"], key="bm_ctf_zip")

        split_mode = st.selectbox("Split", ["test: all", "custom"], key="bm_split_mode", help="Future support for custom train/test splits.")
        if split_mode == "custom":
            st.warning("Custom split configuration is not yet implemented.", icon="⚠️")


        col1, col2 = st.columns(2)
        with col1:
            st.number_input("Random seed", 0, 1_000_000, 42, key="bm_seed")
        with col2:
            st.selectbox("Dedupe by", ["slug", "attachment_hash"], key="bm_dedupe", help="Ensure no duplicate problems are included.")
            
        st.markdown("**Dataset Preview**")

        preview_data = {'Category': ['Web', 'Pwn', 'Crypto'], 'Count': [5, 3, 2], 'Total Items': [10, 10, 10]}
        st.dataframe(pd.DataFrame(preview_data), use_container_width=True, hide_index=True)


    with st.expander("3. Environment & Tools"):
        profile = st.selectbox("Environment profile", ["Headless Kali (Docker)", "Python Tools", "Headless Browser", "Custom"], key="bm_env_profile")

        st.markdown("<h6>Common Configuration</h6>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        c1.number_input("CPU", 1, 64, 2, key="bm_env_cpu")
        c2.number_input("Memory (GB)", 1, 512, 4, key="bm_env_mem")
        c3.number_input("Disk scratch (GB)", 1, 2048, 4, key="bm_env_disk")
        
        c1, c2, c3 = st.columns(3)
        c1.selectbox("GPU", ["none", "rtx", "a100"], key="bm_env_gpu")
        c2.selectbox("Network", ["None", "Egress-only", "Full"], key="bm_env_net")
        c3.number_input("Timeout per task (sec)", 60, 86400, 900, step=30, key="bm_env_timeout")

        st.text_area("ENV vars (KEY=VALUE per line)", key="bm_env_envvars", placeholder="API_KEY=your_secret_key\nANOTHER_VAR=value")
        st.text_area("Startup script (bash)", key="bm_env_startup", placeholder="#!/bin/bash\napt-get update && apt-get install -y ...")
        st.checkbox("Lock images (pin digest)", value=True, key="bm_env_lock")

        st.markdown(f"<h6>Profile-specific: {profile}</h6>", unsafe_allow_html=True)
        if profile == "Headless Kali (Docker)":
            st.text_input("Image", "kalilinux/kali-rolling:latest", key="bm_env_img_kali", disabled=True)
            st.multiselect("Toolpacks", ["Pwn", "Forensics", "Web", "Crypto", "Cracking"], key="bm_env_toolpacks")
            st.text_input("Extra apt packages (space-separated)", "", key="bm_env_apt_extra", placeholder="nmap dnsutils")
        elif profile == "Python Tools":
            st.text_input("Image", "python:3.11-slim", key="bm_env_img_python", disabled=True)
            st.file_uploader("requirements.txt", type=["txt"], key="bm_env_reqs_file")
            st.multiselect("Quick-add libraries", ["pwntools", "pycryptodome", "numpy", "pillow"], key="bm_env_quick_libs")
        elif profile == "Headless Browser":
            st.text_input("Image", "browserless/chrome:latest", key="bm_env_img_browser", disabled=True)
            st.text_input("BROWSERLESS_TOKEN", type="password", key="bm_env_browser_token")
        elif profile == "Custom":
            st.text_input("Docker image", "ubuntu:24.04", key="bm_env_image_custom")
            st.text_input("Command/entrypoint", "bash -lc", key="bm_env_cmd_custom")


    with st.expander("4. Evaluation"):
        judging_method = st.selectbox("Judging", ["automatic", "llm_judge"], key="bm_eval_judging")
        if judging_method == "llm_judge":
            st.text_input("Rubric ID / name", key="bm_eval_rubric", placeholder="e.g., concise-code-explainer-v2")

        st.markdown("<h6>Metrics & Weights</h6>", unsafe_allow_html=True)
        metrics = {"Solve Rate": 1.0, "Avg Time to Flag": 0.5, "Token Efficiency": 0.2, "Cost USD": 0.2, "First Try Pass": 0.8, "Partial Credit": 0.0}
        
        active_metrics = {}
        for name, default_w in metrics.items():
            if st.checkbox(name, value=default_w > 0.0, key=f"bm_metric_{name}_active"):
                active_metrics[name] = st.number_input("Weight", 0.0, 10.0, default_w, key=f"bm_metric_{name}_w")


        st.selectbox("Aggregation", ["macro", "micro", "per-category"], key="bm_eval_agg", help="How to average scores across tasks.")
        
        st.markdown("<h6>Limits</h6>", unsafe_allow_html=True)
        l1, l2, l3, l4 = st.columns(4)
        l1.number_input("Max wallclock (sec)", 60, 86400, 900, key="bm_eval_wallclock")
        l2.number_input("Max tokens (input)", 0, 10_000_000, 0, key="bm_eval_toks_in", help="0 for unlimited")
        l3.number_input("Max tokens (output)", 0, 10_000_000, 0, key="bm_eval_toks_out", help="0 for unlimited")
        l4.number_input("Reruns per task", 1, 10, 1, key="bm_eval_reruns")


    with st.expander("5. Leaderboard & Reproducibility"):
        st.checkbox("Public leaderboard", value=False, key="bm_lb_public")
        st.checkbox("Anonymize submissions", value=True, key="bm_lb_anon")
        st.checkbox("Show artifacts publicly", value=False, key="bm_lb_artifacts", help="Allow viewers to see code, logs, and other files from submissions.")
        st.multiselect("Allowed environment profiles for submissions", 
                      ["Headless Kali (Docker)", "Python Tools", "Headless Browser", "Custom"], 
                      default=["Headless Kali (Docker)"], 
                      key="bm_repro_allowed")


    st.divider()
    if st.button("Create Benchmark", type="primary", key="bm_create", use_container_width=True):

        errors = []
        if not st.session_state.bm_name:
            errors.append("Benchmark Name is required.")
        
        if st.session_state.bm_dataset_source == "Select existing CTFs" and not st.session_state.bm_ctf_slugs:
            errors.append("Please select at least one CTF for the dataset.")

        if st.session_state.bm_env_profile == "Headless Browser" and not st.session_state.bm_env_browser_token:
            errors.append("BROWSERLESS_TOKEN is required for the Headless Browser profile.")

        if not any(st.session_state.get(f"bm_metric_{name}_active") for name in metrics):
            errors.append("At least one metric must be selected for evaluation.")

        if errors:
            for error in errors:
                st.error(f"Validation failed: {error}")
        else:

            st.success("Benchmark created successfully! (Mock)")
            payload = {
                "name": st.session_state.bm_name,
                "description": st.session_state.bm_desc_md,
                "visibility": st.session_state.bm_visibility,
                "modality": st.session_state.bm_modality,
                "domains": st.session_state.bm_domains,
                "dataset": {
                    "source": st.session_state.bm_dataset_source,
                    "ctf_slugs": st.session_state.bm_ctf_slugs if st.session_state.bm_dataset_source == "Select existing CTFs" else "from_zip",
                    "split_mode": st.session_state.bm_split_mode,
                    "seed": st.session_state.bm_seed,
                    "dedupe_by": st.session_state.bm_dedupe
                },
                "environment": {
                    "profile": st.session_state.bm_env_profile,
                    "cpu": st.session_state.bm_env_cpu,
                    "memory_gb": st.session_state.bm_env_mem,
                    "disk_gb": st.session_state.bm_env_disk,
                    "gpu": st.session_state.bm_env_gpu,
                    "network": st.session_state.bm_env_net,
                    "timeout_sec": st.session_state.bm_env_timeout,
                    "env_vars": st.session_state.bm_env_envvars,
                    "startup_script": st.session_state.bm_env_startup,
                    "lock_images": st.session_state.bm_env_lock,
                },
                "evaluation": {
                    "judging": st.session_state.bm_eval_judging,
                    "rubric": st.session_state.get("bm_eval_rubric"),
                    "metrics": active_metrics,
                    "aggregation": st.session_state.bm_eval_agg,
                    "limits": {
                        "wallclock_sec": st.session_state.bm_eval_wallclock,
                        "max_tokens_in": st.session_state.bm_eval_toks_in,
                        "max_tokens_out": st.session_state.bm_eval_toks_out,
                        "reruns": st.session_state.bm_eval_reruns
                    }
                },
                "leaderboard": {
                    "public": st.session_state.bm_lb_public,
                    "anonymize": st.session_state.bm_lb_anon,
                    "show_artifacts": st.session_state.bm_lb_artifacts,
                    "allowed_environments": st.session_state.bm_repro_allowed
                }
            }
            

            if st.session_state.bm_env_profile == "Headless Kali (Docker)":
                payload['environment']['toolpacks'] = st.session_state.bm_env_toolpacks
                payload['environment']['extra_apt_packages'] = st.session_state.bm_env_apt_extra
            elif st.session_state.bm_env_profile == "Python Tools":
                payload['environment']['requirements_file'] = st.session_state.bm_env_reqs_file
                payload['environment']['quick_add_libs'] = st.session_state.bm_env_quick_libs
            elif st.session_state.bm_env_profile == "Headless Browser":
                payload['environment']['browserless_token'] = "********" # Mask token
            elif st.session_state.bm_env_profile == "Custom":
                payload['environment']['docker_image'] = st.session_state.bm_env_image_custom
                payload['environment']['command'] = st.session_state.bm_env_cmd_custom


            st.json(payload)
