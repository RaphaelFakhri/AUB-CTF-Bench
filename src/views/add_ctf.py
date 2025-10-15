import streamlit as st
import pandas as pd
import re
import json
import hashlib

def simple_slugify(text):
    """A simple, dependency-free slugify function."""
    text = text.lower()
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'[^a-z0-9-]', '', text)
    return text.strip('-')

def render():
    """Renders a more complete and functional UI for adding a single CTF challenge."""

    mock_categories = ["Web", "Cryptography", "Reverse Engineering", "Pwn", "Forensics", "Misc"]
    mock_tags = ["SQLi", "XSS", "RSA", "AES", "Buffer Overflow", "Heap Exploitation", "Steganography"]
    mock_scorers = ["exact_match", "regex_match", "judge_program", "llm_judge"]
    mock_licenses = ["Proprietary", "CC-BY", "CC-BY-SA", "CC0", "Other"]
    mock_attachment_roles = ["web_root", "sample_image", "pcap", "binary", "doc", "archive", "audio", "video",
"other"]
    mock_collections = ["None", "Google CTF 2024", "DEF CON CTF 2023", "picoCTF 2023", "(Create New Collection...)"]

    if 'ctf_hints' not in st.session_state:
        st.session_state.ctf_hints = []
    if 'ctf_title_prev' not in st.session_state:
        st.session_state.ctf_title_prev = ""
    if 'ctf_notes_admin' not in st.session_state:
        st.session_state.ctf_notes_admin = ""

    st.header("Add CTF Challenge")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Basics")

        title = st.text_input("Title", key="ctf_title", help="The main title of the CTF challenge.")

        if title != st.session_state.ctf_title_prev:
            st.session_state.ctf_title_prev = title
            st.session_state.ctf_slug = simple_slugify(title)

        st.text_input("Slug", key="ctf_slug", help="URL-friendly identifier. Auto-generated from title but can be edited.")

        st.selectbox("Category", mock_categories, key="ctf_category", help="The primary category of the challenge.")
        st.selectbox("Difficulty", ["Easy", "Medium", "Hard", "Insane"], key="ctf_difficulty")
        st.number_input("Points", min_value=0, max_value=100000, value=100, step=50, key="ctf_points", help="Optional. Can be left at 0.")
        st.multiselect("Tags", options=mock_tags, default=[], key="ctf_tags")

    with col2:
        st.subheader("Problem & Flag")
        st.text_area("Statement (Markdown)", height=220, key="ctf_statement_md", help="The problem description. Markdown is supported.")

        st.markdown("<h6>Flag Configuration</h6>", unsafe_allow_html=True)
        flag_type = st.selectbox("Flag Type", ["Static", "Regex", "Dynamic", "Multiple"], key="ctf_flag_type")

        if flag_type == "Static":
            st.text_input("Flag Value", key="ctf_flag_value", placeholder="e.g., flag{s3cr3t_v4lu3}")
        elif flag_type == "Regex":
            st.text_input("Flag Regex", key="ctf_flag_regex", placeholder="e.g., flag\\{[a-zA-Z0-9_]+\}")
        elif flag_type == "Multiple":
            st.text_area("Flag List (one per line)", key="ctf_flag_list", help="Enter multiple correct flags, one on each line.")

        c1, c2 = st.columns(2)
        with c1:
            st.checkbox("Case sensitive", value=True, key="ctf_flag_case")
            st.checkbox("Strip whitespace", value=True, key="ctf_flag_strip")
        with c2:
            st.number_input("Max submissions", min_value=0, max_value=100, value=0, key="ctf_flag_max_sub", help="0 for unlimited.")
            if flag_type == "Multiple":
                st.checkbox("Enable partial scoring", value=False, key="ctf_flag_partial")

    st.markdown("---")

    with st.expander("Hints"):
        for i in range(len(st.session_state.ctf_hints)):
            st.text_input(f"Hint #{i+1} Text", key=f"ctf_hint_text_{i}")
            st.number_input(f"Unlock Delay (sec)", min_value=0, max_value=86400, key=f"ctf_hint_delay_{i}")
            st.markdown("---")

        if st.button("+ Add hint", key="ctf_hint_add"):
            st.session_state.ctf_hints.append({}) # Add a placeholder for a new hint
            st.rerun()

    with st.expander("Attachments"):
        uploaded_files = st.file_uploader(
            "Upload files",
            accept_multiple_files=True,
            type=["png","jpg","jpeg","webp","gif","txt","md","pdf","pcap","zip","tar","gz","xz","bin","exe","html","js","wasm","wav","mp3","mp4"],
            key="ctf_files"
        )
        if uploaded_files:
            for uploaded_file in uploaded_files:
                file_bytes = uploaded_file.getvalue()
                sha256_hash = hashlib.sha256(file_bytes).hexdigest()
                col1, col2, col3 = st.columns([3, 2, 3])
                with col1:
                    st.text(uploaded_file.name)
                with col2:
                    st.selectbox("Role", mock_attachment_roles, key=f"ctf_role_{uploaded_file.id}")
                with col3:
                    st.caption(f"Size: {round(len(file_bytes) / 1024, 2)} KB")
                    st.caption(f"SHA-256: {sha256_hash[:16]}...")

    with st.expander("Evaluation"):
        st.info("The Flag defines *what* the correct answer is (e.g., a specific string or regex). The Scorer defines *how* a submission is evaluated against that flag (e.g., exact match, judge program).")
        st.selectbox("Scorer", mock_scorers, key="ctf_scorer")
        st.text_area("Expected outputs (JSON)", key="ctf_expected_outputs_json", help="Optional. For challenges with complex, multi-part answers.")
        st.text_input("Score weights (JSON)", value='{"flag":1.0}', key="ctf_score_weights_json")

    with st.expander("Provenance"):
        collection = st.selectbox("Collection", mock_collections, key="ctf_collection", help="Optionally assign this challenge to a collection.")
        if collection == "(Create New Collection...)":
            st.text_input("New Collection Name", key="ctf_new_collection_name", placeholder="e.g., My Custom CTF")

        st.text_input("Author", key="ctf_author", placeholder="e.g., John Doe")
        st.text_input("Source URL", key="ctf_source_url", placeholder="e.g., https://original.ctf/challenge")
        st.selectbox("License", mock_licenses, key="ctf_license")
        st.text_area("Admin Notes", key="ctf_notes_admin", help="Internal notes, not visible to players.")


    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Save CTF", type="primary", use_container_width=True, key="ctf_save"):
        errors = []
        if not st.session_state.ctf_title: errors.append("Title is required.")
        if not st.session_state.ctf_slug: errors.append("Slug is required.")
        if not re.match(r'^[a-z0-9-]+$', st.session_state.ctf_slug): errors.append("Slug contains invalid characters.")
        if not st.session_state.ctf_statement_md: errors.append("Statement is required.")

        flag_type = st.session_state.ctf_flag_type
        if flag_type == "Static" and not st.session_state.ctf_flag_value: errors.append("Flag Value is required for Static flag type.")
        if flag_type == "Regex" and not st.session_state.ctf_flag_regex: errors.append("Flag Regex is required for Regex flag type.")
        if flag_type == "Multiple" and not st.session_state.ctf_flag_list: errors.append("Flag List is required for Multiple flag type.")

        try:
            json.loads(st.session_state.ctf_score_weights_json)
        except json.JSONDecodeError:
            errors.append("Score weights is not valid JSON.")

        collection = st.session_state.ctf_collection
        if collection == "(Create New Collection...)" and not st.session_state.ctf_new_collection_name: errors.append("New Collection Name cannot be empty.")
        if errors:
            for error in errors:
                st.error(error)
        else:
            final_collection = st.session_state.ctf_new_collection_name if collection == "(Create New Collection...)" else collection

            payload = {
                'basics': {
                    'title': st.session_state.ctf_title,
                    'slug': st.session_state.ctf_slug,
                    'category': st.session_state.ctf_category,
                    'difficulty': st.session_state.ctf_difficulty,
                    'points': st.session_state.ctf_points,
                    'tags': st.session_state.ctf_tags,
                    'collection': final_collection if final_collection != "None" else None,
                },
                'problem': {
                    'statement_md': st.session_state.ctf_statement_md,
                    'flag_config': {
                        'type': flag_type,
                        'value': st.session_state.get('ctf_flag_value'),
                        'regex': st.session_state.get('ctf_flag_regex'),
                        'list': st.session_state.get('ctf_flag_list', '').splitlines(),
                        'case_sensitive': st.session_state.ctf_flag_case,
                        'strip_whitespace': st.session_state.ctf_flag_strip,
                        'max_submissions': st.session_state.ctf_flag_max_sub,
                        'partial_scoring': st.session_state.get('ctf_flag_partial', False),
                    }
                },
                'evaluation': {
                    'scorer': st.session_state.ctf_scorer,
                    'expected_outputs_json': st.session_state.ctf_expected_outputs_json,
                    'score_weights_json': st.session_state.ctf_score_weights_json,
                },
                'provenance': {
                    'author': st.session_state.ctf_author,
                    'source_url': st.session_state.ctf_source_url,
                    'license': st.session_state.ctf_license,
                    'admin_notes': st.session_state.ctf_notes_admin,
                }
            }
            st.toast("CTF Challenge Saved!")
            st.subheader("Generated Payload Summary")
            st.json(payload)
