import streamlit as st
from src.utils import get_image_as_base64

def render(models): # The function signature must match the call in main.py
    st.markdown('<div id="home" class="section-anchor"></div>', unsafe_allow_html=True)

    logo = get_image_as_base64("assets/logo.png")
    # Apply max-width directly to the image using markdown
    st.markdown(f"""
    <div style="text-align: center;margin-top:80px">
        <img src="data:image/png;base64,{logo}" alt="Logo" style="max-width: 12%; height: auto; margin: 0 auto;">
    </div>
    """, unsafe_allow_html=True)

    # Combined Title
    st.markdown("""
    <h1 style="text-align: center; font-size: 2rem; font-weight: 700; margin-top: 20px;">
        AUB-CTF-Bench: Bridging the Vision Gap
    </h1>
    """, unsafe_allow_html=True)

    # Subtitle
    st.markdown("""
    <p class="home-subtitle">
        Benchmarking Large Language Models on Multi-Modal Capture The Flag Problems
    </p>
    """, unsafe_allow_html=True)

    st.markdown("---", unsafe_allow_html=True)

    # --- Project Team Section (Academic Paper Style) ---
    st.markdown("""
    <style>
    .home-subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #888;
    }
    body.dark-mode .home-subtitle {
        color: #a0a0a0;
    }
    .author-block {
        text-align: center;
        line-height: 1.4;
    }
    .author-block .name {
        font-size: 1.1rem;
        font-weight: 600;
        color: #212529;
        margin: 0;
    }
    .author-block .affiliation {
        font-size: 0.95rem;
        color: #6c757d;
        margin: 0;
    }
    body.dark-mode .author-block .name {
        color: #FFFFFF;
    }
    body.dark-mode .author-block .affiliation {
        color: #a0a0a0;
    }
    </style>
    """, unsafe_allow_html=True)

    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            <div class="author-block">
                <p class="name">Raphael Fakhri</p>
                <p class="affiliation">Principal Student Researcher</p>
                <p class="affiliation">Department of Computer Science</p>
                <p class="affiliation">American University of Beirut</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div class="author-block">
                <p class="name">Prof. Haidar Safa, Ph.D.</p>
                <p class="affiliation">Thesis Advisor</p>
                <p class="affiliation">Department of Computer Science</p>
                <p class="affiliation">American University of Beirut</p>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown("""
            <div class="author-block">
                <p class="name">Prof. Mohamad Nassar, Ph.D.</p>
                <p class="affiliation">Thesis Co-Advisor</p>
                <p class="affiliation">Department of Electrical & Computer Engineering</p>
                <p class="affiliation">University of New Haven</p>
            </div>
            """, unsafe_allow_html=True)