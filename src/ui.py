import streamlit as st
import base64
import streamlit.components.v1 as components
from src.utils import get_image_as_base64

def render_navbar_and_styles():
    logo_base64 = get_image_as_base64("assets/logo-cropped.png")
    github_base64 = get_image_as_base64("assets/github-mark.svg")

    components.html("""
    <script>
    // ROBUST NAVIGATION SYSTEM FOR STREAMLIT - V10 (CLEANED)

    // --- CONFIGURATION ---
    const sections = ['home', 'models', 'benchmarks', 'compare', 'ctf', 'about', 'thesis'];
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
            window.parent.history.pushState(null, null, '#' + sectionId);
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

    st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" integrity="sha512-DTOQO9RWCH3ppGqcWaEA1BIZOC6xxalwEsw9c2QQeAIftl+Vegovlnee1c9QX4TctnWMn13TZye+giMm8e2LwA==" crossorigin="anonymous" referrerpolicy="no-referrer" />
    """, unsafe_allow_html=True)

    st.markdown("""
    <style>
        /* Bulletproof navigation highlighting */
        * {font-family: 'Roboto', sans-serif !important;}
        
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
            <a href="#benchmarks" class="nav-link">Benchmarks</a>
            <a href="#compare" class="nav-link">Compare</a>
            <a href="#ctf" class="nav-link">CTF</a>
            <a href="#about" class="nav-link">About</a>
            <a href="#thesis" class="nav-link">Thesis</a>
        </div>
        <div class="navbar-right">
            <a href="https://github.com" class="github-link" target="_blank" title="GitHub">
                <img src="data:image/svg+xml;base64,{github_base64}" alt="GitHub" class="github-icon">
            </a>
            <button class="theme-toggle" onclick="toggleTheme()" title="Toggle Theme">🌙</button>
        </div>
    </div>
    """, unsafe_allow_html=True)
