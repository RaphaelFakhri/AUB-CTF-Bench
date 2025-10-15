# ruff: noqa: F401
import streamlit as st
# ruff: noqa: F401
import pandas as pd
# ruff: noqa: F401
import numpy as np
# ruff: noqa: F401
import plotly.express as px
# ruff: noqa: F401
import plotly.graph_objects as go
# ruff: noqa: F401
from plotly.subplots import make_subplots
# ruff: noqa: F401
import io
# ruff: noqa: F401
from PIL import Image
# ruff: noqa: F401
import base64
import time
import random
import streamlit.components.v1 as components

from src.data import load_mock_data, load_queue_data
from src.views import home, models as models_view, problems_results, compare, ctf, manage, create_benchmark, view_queue

# --- Page Config and State Initialization ---
st.set_page_config(page_title="AUB-CTF-Bench", page_icon="🏴", layout="wide")

if "show_modal" not in st.session_state:
    st.session_state.show_modal = None


# --- Main Page UI and Navigation Code ---

# This JS block contains the fix for the query parameter issue.
components.html("""
<script>
// ROBUST NAVIGATION SYSTEM FOR STREAMLIT - V11 (URL PRESERVE FIX)

// --- CONFIGURATION ---
const sections = ['home', 'models', 'problems_results', 'compare', 'view_queue', 'manage', 'create_benchmark'];
const navbarHeight = 80;

// --- STATE ---
let currentActiveSection = 'home';
let scrollContainer = null;
let intersectionObserver = null;
let isInitialized = false;
let initObserver = null;
let isScrollingProgrammatically = false;
let scrollTimeout = null;

// --- CORE, IFRAME-AWARE FUNCTIONS ---

function findScrollContainer() {
    const parentDoc = window.parent.document;
    const candidate = parentDoc.querySelector('[data-testid="stAppViewContainer"]');
    if (candidate && candidate.scrollHeight > candidate.clientHeight) {
        return candidate;
    }
    return window.parent;
}

function setActiveNav(sectionId) {
    if (!sectionId || currentActiveSection === sectionId) {
        return;
    }
    currentActiveSection = sectionId;
    window.parent.document.querySelectorAll('.nav-link').forEach(link => {
        const href = link.getAttribute('href');
        const linkSectionId = href ? href.substring(1) : '';
        link.classList.toggle('active', linkSectionId === sectionId);
    });
}

function scrollToSection(sectionId) {
    const anchor = window.parent.document.getElementById(sectionId);
    if (!anchor) {
        console.error('NAV | Could not find anchor for section:', sectionId);
        return;
    }

    isScrollingProgrammatically = true;
    setActiveNav(sectionId);

    anchor.scrollIntoView({ behavior: 'smooth', block: 'start' });

    if (window.parent.history.pushState) {
        // *** BUG FIX: Preserve query parameters when changing the hash ***
        const newUrl = window.parent.location.pathname + window.parent.location.search + '#' + sectionId;
        window.parent.history.pushState(null, null, newUrl);
    }

    clearTimeout(scrollTimeout);
    scrollTimeout = setTimeout(() => {
        isScrollingProgrammatically = false;
    }, 1000);
}

// --- SETUP FUNCTIONS (IFRAME-AWARE) ---

function setupClickHandlers() {
    window.parent.document.querySelectorAll('.nav-link').forEach(link => {
        const newLink = link.cloneNode(true);
        link.parentNode.replaceChild(newLink, link);
        newLink.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            const sectionId = newLink.getAttribute('href').substring(1);
            scrollToSection(sectionId);
        });
    });
}

function setupIntersectionObserver() {
    if (intersectionObserver) intersectionObserver.disconnect();

    scrollContainer = findScrollContainer();
    const rootMargin = `-${navbarHeight}px 0px -50% 0px`;

    intersectionObserver = new IntersectionObserver((entries) => {
        if (isScrollingProgrammatically) {
            return;
        }
        let mostVisibleSection = null;
        let maxRatio = 0;
        entries.forEach(entry => {
            if (entry.isIntersecting && entry.intersectionRatio > maxRatio) {
                mostVisibleSection = entry.target.dataset.sectionId;
                maxRatio = entry.intersectionRatio;
            }
        });
        if (mostVisibleSection) {
            setActiveNav(mostVisibleSection);
        }
    }, {
        root: scrollContainer === window.parent ? null : scrollContainer,
        rootMargin: rootMargin,
        threshold: 0.1
    });

    sections.forEach(id => {
        const anchor = window.parent.document.getElementById(id);
        if (anchor && anchor.parentElement) {
            const elementToObserve = anchor.parentElement;
            elementToObserve.dataset.sectionId = id;
            intersectionObserver.observe(elementToObserve);
        } else {
            console.warn('NAV | Could not find parent element to observe for section:', id);
        }
    });
}

function setupThemeToggle() {
    const toggleBtn = window.parent.document.querySelector('.theme-toggle');
    if (toggleBtn && !toggleBtn.dataset.listenerAttached) {
        toggleBtn.addEventListener('click', () => {
            window.parent.document.body.classList.toggle('dark-mode');
        });
        toggleBtn.dataset.listenerAttached = 'true';
    }
}

// --- INITIALIZATION LOGIC (IFRAME-AWARE) ---

function finalInitialization() {
    if (isInitialized) return;
    isInitialized = true;

    if (initObserver) {
        initObserver.disconnect();
    }

    setupClickHandlers();
    setupIntersectionObserver();
    setupThemeToggle();
    
    const initialHash = window.parent.location.hash.substring(1);
    if (initialHash && sections.includes(initialHash)) {
        setTimeout(() => {
            scrollToSection(initialHash);
        }, 500);
    } else {
        setActiveNav('home');
    }
}

function attemptInitialization() {
    if (isInitialized) return;

    const parentDoc = window.parent.document;
    const navbar = parentDoc.querySelector('.navbar');
    const navLinks = parentDoc.querySelectorAll('.nav-link');
    const sectionAnchors = sections.every(id => parentDoc.getElementById(id));

    if (navbar && navLinks.length > 0 && sectionAnchors) {
        finalInitialization();
    } 
}

function setupInitializationObserver() {
    if (initObserver) initObserver.disconnect();

    initObserver = new MutationObserver(() => {
        if (!isInitialized) {
            clearTimeout(window.navReinitTimeout);
            window.navReinitTimeout = setTimeout(attemptInitialization, 250);
        }
    });

    initObserver.observe(window.parent.document.body, {
        childList: true,
        subtree: true
    });
}

// --- GLOBAL API & STARTUP ---
window.parent.scrollToSection = scrollToSection;

function onDomReady() {
    if (window.parent.document.readyState === 'loading') {
        window.parent.addEventListener('DOMContentLoaded', onDomReady);
    } else {
        setupInitializationObserver();
        attemptInitialization();
    }
}

onDomReady();

</script>
""", height=0)

def get_image_as_base64(path):
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

logo_base64 = get_image_as_base64("assets/logo-cropped.png")
github_base64 = get_image_as_base64("assets/github-mark.svg")  

st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" integrity="sha512-DTOQO9RWCH3ppGqcWaEA1BIZOC6xxalwEsw9c2QQeAIftl+Vegovlnee1c9QX4TctnWMn13TZye+giMm8e2LwA==" crossorigin="anonymous" referrerpolicy="no-referrer" />
""", unsafe_allow_html=True)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
    /* Bulletproof navigation highlighting */
    * {font-family: 'Roboto', sans-serif !important;}
    
    /* Override for Material Icons */
    [data-testid="stIconMaterial"] {
        font-family: "Material Symbols Rounded" !important;
    }
    
    /* Core navbar styles */
    body {
        margin: 0 !important;
        transition: background-color 0.3s, color 0.3s;
    }
    
    /* Dark mode styles */
    body.dark-mode {
        background-color: #121212 !important;
        color: #ffffff !important;
    }
    body.dark-mode .stAppViewContainer,
    body.dark-mode [data-testid="stAppViewContainer"] {
        background-color: #121212 !important;
        color: #ffffff !important;
    }
    body.dark-mode .stMarkdown,
    body.dark-mode .stMarkdown > * {
        color: #ffffff !important;
    }
    body.dark-mode .navbar {
        background-color: #1e1e1e !important;
    }
    body.dark-mode .nav-link {
        color: #ffffff !important;
    }
    body.dark-mode .nav-link:hover {
        background-color: #333 !important;
        color: #840132 !important;
    }
    body.dark-mode .nav-link.active {
        background-color: #840132 !important;
        color: #ffffff !important;
    }
    
    /* Navbar container */
    .stAppViewContainer {
        padding-top: 80px !important;
    }
    .navbar {
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        z-index: 1000 !important;
        background-color: #ffffff !important;
        padding: 10px 20px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        gap: 20px !important;
        height: 70px !important;
    }
    
    /* Logo section */
    .navbar-left {
        display: flex !important;
        align-items: center !important;
        height: 100% !important;
    }
    .navbar-logo {
        height: 40px !important;
        margin-left: 20% !important;
        width: auto !important;
        object-fit: contain !important;
    }
    .navbar-logo-text {
        color: #840132 !important;
        font-weight: bold !important;
        font-size: 20px !important;
        margin-left: 10px !important;
        text-decoration: none !important;
    }
    .navbar-left a {
        display: flex !important;
        align-items: center !important;
        text-decoration: none !important;
        background-color: transparent !important;
    }
    
    /* Navigation center */
    .navbar-center {
        display: flex !important;
        justify-content: center !important;
        gap: 30px !important;
        flex: 1 !important;
    }
    
    /* Navigation links - base styles */
    .nav-link {
        color: #333 !important;
        text-decoration: none !important;
        font-weight: 500 !important;
        padding: 8px 16px !important;
        border-radius: 4px !important;
        transition: all 0.2s !important;
        position: relative !important;
        display: inline-block !important;
        line-height: 1.4 !important;
        background-color: transparent !important;
        border: none !important;
        margin: 0 !important;
        cursor: pointer !important;
    }
    
    .nav-link:hover {
        background-color: #f0f0f0 !important;
        color: #840132 !important;
    }
    
    /* Active state for nav links */
    .nav-link.active {
        background-color: #840132 !important;
        color: #ffffff !important;
    }
    
    /* Dark mode nav links */
    body.dark-mode .nav-link {
        color: #ffffff !important;
    }
    body.dark-mode .nav-link:hover {
        background-color: #333 !important;
        color: #840132 !important;
    }
    body.dark-mode .nav-link.active {
        background-color: #840132 !important;
        color: #ffffff !important;
    }
    
    /* Right side */
    .navbar-right {
        display: flex !important;
        align-items: center !important;
        gap: 20px !important;
    }
    .github-link {
        color: #333 !important;
        text-decoration: none !important;
        padding: 8px 12px !important;
        border-radius: 4px !important;
        transition: all 0.2s !important;
        display: flex !important;
        align-items: center !important;
    }
    .github-link:hover {
        background-color: #f0f0f0 !important;
        color: #840132 !important;
    }
    .github-icon {
        width: 24px !important;
        height: 24px !important;
        vertical-align: middle !important;
        margin-right: 4px !important;
    }
    .theme-toggle {
        background: none !important;
        border: none !important;
        font-size: 20px !important;
        cursor: pointer !important;
        padding: 8px !important;
        border-radius: 4px !important;
        transition: all 0.2s !important;
        color: #333 !important;
    }
    .theme-toggle:hover {
        background-color: #f0f0f0 !important;
        color: #840132 !important;
    }
    
    /* Dark mode right side */
    body.dark-mode .github-link {
        color: #ffffff !important;
    }
    body.dark-mode .github-link:hover {
        background-color: #333 !important;
        color: #840132 !important;
    }
    body.dark-mode .theme-toggle {
        color: #ffffff !important;
    }
    body.dark-mode .theme-toggle:hover {
        background-color: #333 !important;
        color: #840132 !important;
    }
    
    /* Streamlit component fixes */
    body.dark-mode .stMetric > div > div {
        color: #ffffff !important;
    }
    body.dark-mode .stDataFrame {
        background-color: #1e1e1e !important;
    }
    body.dark-mode .stDataFrame th, 
    body.dark-mode .stDataFrame td {
        color: #ffffff !important;
        border-color: #333 !important;
    }
    
    /* Hide Streamlit header */
    .stAppHeader.st-emotion-cache-1ffuo7c.e3g0k5y1 {
        display: none !important;
    }
    
    /* Block container fixes */
    .block-container {
        padding-top: 0rem !important;
        color: inherit !important;
    }

    .section-anchor {
        display: block;
        position: relative;
        top: -100px; /* Adjust this value to be slightly more than your navbar height */
        visibility: hidden;
    }
</style>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="navbar">
    <div class="navbar-left">
        <a href="#home">
            <img src="data:image/png;base64,{logo_base64}" alt="Logo" class="navbar-logo">
            <span class="navbar-logo-text">aubctf.com</span>
        </a>
    </div>
    <div class="navbar-center">
        <a href="#home" class="nav-link">Home</a>
        <a href="#models" class="nav-link">Models</a>
        <a href="#problems_results" class="nav-link">Problems & Results</a>
        <a href="#compare" class="nav-link">Compare</a>
    </div>
    <div class="navbar-right">
        <a href="https://github.com" class="github-link" target="_blank" title="GitHub">
            <img src="data:image/svg+xml;base64,{github_base64}" alt="GitHub" class="github-icon">
        </a>
        <button class="theme-toggle" onclick="toggleTheme()" title="Toggle Theme">🌙</button>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Data Loading ---
models, benchmarks, environments, runs = load_mock_data()
running_jobs, queued_jobs = load_queue_data()

# --- Main Page Section Rendering ---
home.render(models)
models_view.render(models, benchmarks, runs)
problems_results.render(benchmarks, runs)
compare.render(models)
manage.render()
create_benchmark.render()
view_queue.render(running_jobs, queued_jobs)


# --- Floating Action Buttons (FABs) ---
st.markdown("""
<style>
    .fab-container-final { position: fixed; bottom: 30px; right: 30px; z-index: 1002; display: flex; flex-direction: column; gap: 15px; align-items: flex-end; }
    .fab-final { width: auto; height: 56px; padding: 0 20px; background-color: #840132; border-radius: 30px; display: flex; align-items: center; justify-content: center; color: white; text-decoration: none; box-shadow: 0 4px 8px rgba(0,0,0,0.2); transition: all 0.3s ease; flex-basis: content; }
    .fab-final:hover { background-color: #6a0128; box-shadow: 0 6px 12px rgba(0,0,0,0.3); transform: translateY(-2px); }
    .fab-final svg { width: 24px; height: 24px; margin-right: 12px; }
    .fab-final span { font-weight: 500; }
</style>
<div class="fab-container-final">
    <a href="#manage" class="fab-final nav-link" title="Add CTF">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
        <span>Add CTF</span>
    </a>
    <a href="#create_benchmark" class="fab-final nav-link" title="Create Benchmark">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
        <span>Create Benchmark</span>
    </a>
    <a href="#view_queue" class="fab-final nav-link" title="View Queue">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 22h14"/><path d="M5 2h14"/><path d="M17 2v6l-4 4 4 4v6H7v-6l4-4-4-4V2h10z"/></svg>
        <span>View Queue</span>
    </a>
</div>
""", unsafe_allow_html=True)

# --- Footer ---
st.markdown("&copy; 2025 AUB-CTF-Bench | Multi-modal benchmarking by Raphael Fakhri et al.")