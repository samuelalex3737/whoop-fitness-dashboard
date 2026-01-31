"""
🏋️ WHOOP FITNESS ANALYTICS DASHBOARD
=====================================
Advanced Data Visualization for University Final Project
Created with ❤️ using Streamlit, Plotly, and Machine Learning

Author: Samuel
Date: January 2026
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="WHOOP Fitness Analytics Dashboard",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    /* ═══════════════════════════════════════════════════════════════════════
       🎨 WHOOP ANALYTICS PRO - PREMIUM DARK THEME
       University Final Project - Professional Dashboard Styling
    ═══════════════════════════════════════════════════════════════════════ */
    
    /* Import premium fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* ═══════════════════════════════════════════════════════════════════════
       ROOT VARIABLES & GLOBAL STYLES
    ═══════════════════════════════════════════════════════════════════════ */
    :root {
        --primary: #00D4AA;
        --primary-dark: #00A080;
        --primary-glow: rgba(0, 212, 170, 0.4);
        --secondary: #6366F1;
        --accent: #F59E0B;
        --success: #10B981;
        --warning: #F59E0B;
        --danger: #EF4444;
        --bg-dark: #0A0E17;
        --bg-card: #111827;
        --bg-card-hover: #1F2937;
        --text-primary: #F9FAFB;
        --text-secondary: #9CA3AF;
        --text-muted: #6B7280;
        --border-color: rgba(255, 255, 255, 0.08);
        --glass-bg: rgba(17, 24, 39, 0.8);
    }
    
    /* Global font override */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: var(--bg-dark);
    }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, var(--primary) 0%, var(--primary-dark) 100%);
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: var(--primary);
    }
    
    /* Main container */
    .main {
        padding: 0rem 1rem;
        background: linear-gradient(180deg, var(--bg-dark) 0%, #0F172A 100%);
    }
    
    .block-container {
        padding-top: 2rem !important;
        max-width: 100% !important;
    }
    
    /* ═══════════════════════════════════════════════════════════════════════
       ANIMATED HEADER
    ═══════════════════════════════════════════════════════════════════════ */
    .main-header {
        background: linear-gradient(135deg, #00D4AA 0%, #00A080 50%, #008066 100%);
        padding: 2.5rem 3rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 
            0 20px 60px rgba(0, 212, 170, 0.3),
            0 0 100px rgba(0, 212, 170, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
        position: relative;
        overflow: hidden;
        animation: headerGlow 3s ease-in-out infinite alternate;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: shimmer 4s linear infinite;
    }
    
    @keyframes headerGlow {
        0% { box-shadow: 0 20px 60px rgba(0, 212, 170, 0.3), 0 0 100px rgba(0, 212, 170, 0.1); }
        100% { box-shadow: 0 25px 80px rgba(0, 212, 170, 0.4), 0 0 120px rgba(0, 212, 170, 0.2); }
    }
    
    @keyframes shimmer {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .main-header h1 {
        color: white;
        font-size: 2.8rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 20px rgba(0, 0, 0, 0.3);
        letter-spacing: -0.5px;
        position: relative;
        z-index: 1;
    }
    
    .main-header p {
        color: rgba(255, 255, 255, 0.95);
        font-size: 1.15rem;
        font-weight: 400;
        position: relative;
        z-index: 1;
    }
    
    /* ═══════════════════════════════════════════════════════════════════════
       GLASSMORPHISM METRIC CARDS
    ═══════════════════════════════════════════════════════════════════════ */
    [data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 700 !important;
        background: linear-gradient(135deg, var(--primary) 0%, #00E5BB 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        color: var(--text-secondary) !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 0.8rem !important;
        font-weight: 500 !important;
    }
    
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, var(--bg-card) 0%, rgba(31, 41, 55, 0.8) 100%) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 16px !important;
        padding: 1.25rem !important;
        backdrop-filter: blur(10px);
        box-shadow: 
            0 4px 20px rgba(0, 0, 0, 0.25),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    [data-testid="metric-container"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 3px;
        background: linear-gradient(90deg, var(--primary), var(--secondary), var(--primary));
        background-size: 200% 100%;
        animation: gradientMove 3s linear infinite;
    }
    
    [data-testid="metric-container"]:hover {
        transform: translateY(-4px);
        border-color: var(--primary) !important;
        box-shadow: 
            0 12px 40px rgba(0, 212, 170, 0.2),
            0 4px 20px rgba(0, 0, 0, 0.3);
    }
    
    @keyframes gradientMove {
        0% { background-position: 0% 50%; }
        100% { background-position: 200% 50%; }
    }
    
    /* ═══════════════════════════════════════════════════════════════════════
       PREMIUM TAB NAVIGATION
    ═══════════════════════════════════════════════════════════════════════ */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background: var(--bg-card);
        padding: 8px;
        border-radius: 16px;
        border: 1px solid var(--border-color);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        color: var(--text-secondary) !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        transition: all 0.3s ease !important;
        border: none !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(0, 212, 170, 0.1) !important;
        color: var(--primary) !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 15px rgba(0, 212, 170, 0.4) !important;
    }
    
    .stTabs [data-baseweb="tab-border"] {
        display: none !important;
    }
    
    .stTabs [data-baseweb="tab-highlight"] {
        display: none !important;
    }
    
    /* ═══════════════════════════════════════════════════════════════════════
       SIDEBAR PREMIUM STYLING
    ═══════════════════════════════════════════════════════════════════════ */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0D1117 0%, #161B22 100%) !important;
        border-right: 1px solid var(--border-color) !important;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1rem;
    }
    
    /* Sidebar expanders */
    [data-testid="stExpander"] {
        background: rgba(17, 24, 39, 0.6) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 12px !important;
        margin-bottom: 8px !important;
        overflow: hidden;
    }
    
    [data-testid="stExpander"] summary {
        padding: 0.75rem 1rem !important;
        font-weight: 600 !important;
        color: var(--primary) !important;
    }
    
    [data-testid="stExpander"] summary:hover {
        background: rgba(0, 212, 170, 0.05) !important;
    }
    
    /* ═══════════════════════════════════════════════════════════════════════
       FORM ELEMENTS - SLIDERS, MULTISELECT, INPUTS
    ═══════════════════════════════════════════════════════════════════════ */
    /* Sliders */
    .stSlider > div > div > div > div {
        background: var(--primary) !important;
    }
    
    .stSlider > div > div > div[role="slider"] {
        background: white !important;
        border: 3px solid var(--primary) !important;
        box-shadow: 0 2px 10px rgba(0, 212, 170, 0.4) !important;
    }
    
    /* Multiselect */
    .stMultiSelect > div > div {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 10px !important;
        transition: all 0.2s ease !important;
    }
    
    .stMultiSelect > div > div:hover {
        border-color: var(--primary) !important;
    }
    
    .stMultiSelect > div > div:focus-within {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(0, 212, 170, 0.2) !important;
    }
    
    /* Selected tags */
    .stMultiSelect [data-baseweb="tag"] {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%) !important;
        border-radius: 6px !important;
        font-weight: 500 !important;
    }
    
    /* Date input */
    .stDateInput > div > div {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 10px !important;
    }
    
    .stDateInput > div > div:hover {
        border-color: var(--primary) !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--bg-card) 0%, var(--bg-card-hover) 100%) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 10px !important;
        color: var(--text-primary) !important;
        font-weight: 500 !important;
        padding: 0.5rem 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%) !important;
        border-color: var(--primary) !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0, 212, 170, 0.3) !important;
    }
    
    /* ═══════════════════════════════════════════════════════════════════════
       CHART CONTAINERS
    ═══════════════════════════════════════════════════════════════════════ */
    [data-testid="stPlotlyChart"] {
        background: var(--bg-card) !important;
        border-radius: 16px !important;
        padding: 1rem !important;
        border: 1px solid var(--border-color) !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2) !important;
    }
    
    /* ═══════════════════════════════════════════════════════════════════════
       MARKDOWN & TEXT STYLING
    ═══════════════════════════════════════════════════════════════════════ */
    h1, h2, h3 {
        color: var(--text-primary) !important;
        font-weight: 700 !important;
    }
    
    h3 {
        color: var(--primary) !important;
        font-size: 1.3rem !important;
        margin-top: 1.5rem !important;
        margin-bottom: 0.75rem !important;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Blockquote styling for insights */
    blockquote {
        background: linear-gradient(135deg, rgba(0, 212, 170, 0.08) 0%, rgba(0, 160, 128, 0.05) 100%) !important;
        border-left: 4px solid var(--primary) !important;
        border-radius: 0 12px 12px 0 !important;
        padding: 1rem 1.25rem !important;
        margin: 1rem 0 !important;
        color: var(--text-secondary) !important;
        font-size: 0.9rem !important;
        backdrop-filter: blur(5px);
    }
    
    blockquote strong {
        color: var(--primary) !important;
    }
    
    /* Horizontal rules */
    hr {
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent 0%, var(--border-color) 50%, transparent 100%) !important;
        margin: 2rem 0 !important;
    }
    
    /* ═══════════════════════════════════════════════════════════════════════
       INFO, WARNING, SUCCESS BOXES
    ═══════════════════════════════════════════════════════════════════════ */
    .stAlert {
        border-radius: 12px !important;
        border: none !important;
    }
    
    [data-baseweb="notification"] {
        border-radius: 12px !important;
    }
    
    /* ═══════════════════════════════════════════════════════════════════════
       DATAFRAME STYLING
    ═══════════════════════════════════════════════════════════════════════ */
    [data-testid="stDataFrame"] {
        border-radius: 12px !important;
        overflow: hidden !important;
    }
    
    [data-testid="stDataFrame"] > div {
        background: var(--bg-card) !important;
    }
    
    /* ═══════════════════════════════════════════════════════════════════════
       LOADING SPINNER
    ═══════════════════════════════════════════════════════════════════════ */
    .stSpinner > div {
        border-color: var(--primary) transparent transparent transparent !important;
    }
    
    /* ═══════════════════════════════════════════════════════════════════════
       HIDE STREAMLIT BRANDING
    ═══════════════════════════════════════════════════════════════════════ */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* ═══════════════════════════════════════════════════════════════════════
       RESPONSIVE ADJUSTMENTS
    ═══════════════════════════════════════════════════════════════════════ */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 1.8rem;
        }
        .main-header {
            padding: 1.5rem;
        }
        [data-testid="stMetricValue"] {
            font-size: 1.5rem !important;
        }
    }
    
    /* ═══════════════════════════════════════════════════════════════════════
       CUSTOM ANIMATION CLASSES
    ═══════════════════════════════════════════════════════════════════════ */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    .animate-fade-in {
        animation: fadeInUp 0.5s ease-out forwards;
    }
    
    .animate-pulse {
        animation: pulse 2s ease-in-out infinite;
    }
    
    /* ═══════════════════════════════════════════════════════════════════════
       SCROLLABLE TABS - Horizontal scroll for many tabs
    ═══════════════════════════════════════════════════════════════════════ */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: var(--bg-card);
        padding: 8px 12px;
        border-radius: 16px;
        border: 1px solid var(--border-color);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        overflow-x: auto !important;
        overflow-y: hidden !important;
        flex-wrap: nowrap !important;
        white-space: nowrap !important;
        -webkit-overflow-scrolling: touch;
        scrollbar-width: thin;
        scrollbar-color: var(--primary) var(--bg-dark);
    }
    
    .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar {
        height: 6px;
    }
    
    .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar-track {
        background: var(--bg-dark);
        border-radius: 3px;
    }
    
    .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar-thumb {
        background: var(--primary);
        border-radius: 3px;
    }
    
    .stTabs [data-baseweb="tab"] {
        flex-shrink: 0 !important;
        min-width: fit-content !important;
    }
    
    /* ═══════════════════════════════════════════════════════════════════════
       FILTER CLICK EFFECTS - Shadow/glow when clicked
    ═══════════════════════════════════════════════════════════════════════ */
    /* Multiselect click/focus effect */
    .stMultiSelect > div > div:focus-within {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(0, 212, 170, 0.3), 0 0 20px rgba(0, 212, 170, 0.2) !important;
        transform: scale(1.01);
        transition: all 0.2s ease !important;
    }
    
    /* Multiselect when has selections - subtle glow */
    .stMultiSelect [data-baseweb="tag"] {
        animation: tagPulse 0.3s ease-out;
    }
    
    @keyframes tagPulse {
        0% { transform: scale(0.8); opacity: 0; }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); opacity: 1; }
    }
    
    /* Button click effect */
    .stButton > button:active {
        transform: scale(0.95) !important;
        box-shadow: 0 0 20px rgba(0, 212, 170, 0.5), inset 0 0 10px rgba(0, 212, 170, 0.2) !important;
    }
    
    /* Slider click effect */
    .stSlider > div > div > div[role="slider"]:active {
        transform: scale(1.2);
        box-shadow: 0 0 20px rgba(0, 212, 170, 0.6) !important;
    }
    
    /* Date picker click effect */
    .stDateInput > div > div:focus-within {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(0, 212, 170, 0.3), 0 0 15px rgba(0, 212, 170, 0.2) !important;
    }
    
    /* Checkbox click effect */
    .stCheckbox > label:active {
        transform: scale(0.98);
    }
    
    .stCheckbox [data-testid="stCheckbox"] > label > div:first-child {
        transition: all 0.2s ease !important;
    }
    
    .stCheckbox [data-testid="stCheckbox"]:has(input:checked) > label > div:first-child {
        box-shadow: 0 0 10px rgba(0, 212, 170, 0.5) !important;
    }
    
    /* Select box click effect */
    .stSelectbox > div > div:focus-within {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(0, 212, 170, 0.3), 0 0 15px rgba(0, 212, 170, 0.2) !important;
    }
    
    /* Radio button click effect */
    .stRadio > div > label:active {
        transform: scale(0.98);
    }
    
    .stRadio [data-testid="stRadio"] > div > label > div:first-child {
        transition: all 0.2s ease !important;
    }
    
    /* Data source toggle special styling */
    .data-source-toggle {
        background: linear-gradient(135deg, rgba(0, 212, 170, 0.1) 0%, rgba(99, 102, 241, 0.1) 100%);
        border: 2px solid var(--primary);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================================
# DATA LOADING & PREPROCESSING
# ============================================================================
import os

@st.cache_data
def load_data():
    """Load and preprocess the WHOOP fitness data."""
    # Check multiple possible paths for compatibility with Docker and Streamlit Cloud
    possible_paths = [
        'whoop_fitness.csv',                    # Current directory (Streamlit Cloud)
        'data/whoop_fitness.csv',               # Data subdirectory
        '/app/data/whoop_fitness.csv',          # Docker mount path
        os.path.join(os.path.dirname(__file__), 'whoop_fitness.csv'),  # Same dir as script
    ]
    
    df = None
    for path in possible_paths:
        if os.path.exists(path):
            df = pd.read_csv(path)
            break
    
    if df is None:
        st.error("❌ Could not find whoop_fitness.csv. Please ensure the data file is in the correct location.")
        st.stop()
    
    # Convert date column
    df['date'] = pd.to_datetime(df['date'])
    
    # Extract temporal features
    df['month'] = df['date'].dt.month
    df['month_name'] = df['date'].dt.month_name()
    df['week'] = df['date'].dt.isocalendar().week
    df['quarter'] = df['date'].dt.quarter
    df['year_month'] = df['date'].dt.to_period('M').astype(str)
    
    # Calculate derived metrics
    df['sleep_quality_index'] = (df['sleep_efficiency'] * 0.4 + 
                                  df['sleep_performance'] * 0.3 + 
                                  (df['deep_sleep_hours'] / df['sleep_hours'] * 100) * 0.3)
    
    df['strain_to_recovery_ratio'] = df['day_strain'] / (df['recovery_score'] + 1)
    
    df['workout_intensity'] = np.where(df['workout_completed'] == 1, 
                                        df['activity_strain'] / (df['activity_duration_min'] + 1) * 60, 
                                        0)
    
    # Season mapping
    season_map = {12: 'Winter', 1: 'Winter', 2: 'Winter',
                  3: 'Spring', 4: 'Spring', 5: 'Spring',
                  6: 'Summer', 7: 'Summer', 8: 'Summer',
                  9: 'Fall', 10: 'Fall', 11: 'Fall'}
    df['season'] = df['month'].map(season_map)
    
    # Age groups
    df['age_group'] = pd.cut(df['age'], bins=[0, 25, 35, 45, 55, 100], 
                             labels=['18-25', '26-35', '36-45', '46-55', '55+'])
    
    # BMI calculation
    df['bmi'] = df['weight_kg'] / (df['height_cm'] / 100) ** 2
    df['bmi_category'] = pd.cut(df['bmi'], bins=[0, 18.5, 25, 30, 100],
                                labels=['Underweight', 'Normal', 'Overweight', 'Obese'])
    
    # Recovery categories
    df['recovery_category'] = pd.cut(df['recovery_score'], bins=[0, 33, 66, 100],
                                     labels=['Red (Low)', 'Yellow (Moderate)', 'Green (High)'])
    
    return df


# Load data
df = load_data()


# ============================================================================
# SIDEBAR CONFIGURATION
# ============================================================================
with st.sidebar:
    # Animated Logo Header
    st.markdown("""
    <div style='text-align: center; padding: 1.5rem; background: linear-gradient(135deg, #0a0f1a 0%, #1a2035 100%); border-radius: 16px; margin-bottom: 1rem; border: 1px solid rgba(0, 212, 170, 0.3);'>
        <div style='font-size: 3rem; margin-bottom: 0.5rem;'>🏋️</div>
        <h2 style='color: #00D4AA; margin: 0; font-weight: 700; letter-spacing: 2px;'>WHOOP</h2>
        <p style='color: #00D4AA; font-size: 0.75rem; margin: 0; letter-spacing: 3px;'>ANALYTICS PRO</p>
        <div style='margin-top: 0.75rem; padding: 0.5rem; background: rgba(0, 212, 170, 0.1); border-radius: 8px;'>
            <span style='color: #888; font-size: 0.7rem;'>📊 100K+ Records | 39 Metrics</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ═══════════════════════════════════════════════════════════════════════
    # � DATA SOURCE TOGGLE
    # ═══════════════════════════════════════════════════════════════════════
    st.markdown("""
    <div style='background: linear-gradient(90deg, #6366F1 0%, transparent 100%); padding: 0.5rem 1rem; border-radius: 8px; margin-bottom: 0.75rem;'>
        <span style='font-weight: 600; font-size: 0.95rem;'>🔀 DATA SOURCE</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize data source in session state
    if 'data_source' not in st.session_state:
        st.session_state.data_source = "📁 Fixed Dataset"
    
    data_source = st.radio(
        "Choose data source:",
        options=["📁 Fixed Dataset", "🔴 Live Feed"],
        index=0 if st.session_state.data_source == "📁 Fixed Dataset" else 1,
        key="data_source_radio",
        horizontal=True,
        help="Switch between your fixed CSV dataset and live streaming data"
    )
    st.session_state.data_source = data_source
    
    # Show data source status
    if data_source == "🔴 Live Feed":
        live_data_path = '/app/data/live_data.csv'
        if os.path.exists(live_data_path):
            st.markdown("""
            <div style='background: rgba(34, 197, 94, 0.1); border: 1px solid rgba(34, 197, 94, 0.3); 
                        padding: 0.5rem; border-radius: 8px; margin-top: 0.5rem;'>
                <span style='color: #22C55E; font-size: 0.8rem;'>🟢 Live data connected</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.3); 
                        padding: 0.5rem; border-radius: 8px; margin-top: 0.5rem;'>
                <span style='color: #EF4444; font-size: 0.8rem;'>🔴 Live data not available</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='background: rgba(59, 130, 246, 0.1); border: 1px solid rgba(59, 130, 246, 0.3); 
                    padding: 0.5rem; border-radius: 8px; margin-top: 0.5rem;'>
            <span style='color: #3B82F6; font-size: 0.8rem;'>📁 Using fixed dataset (100K records)</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='margin: 1rem 0; border-top: 1px solid rgba(255,255,255,0.1);'></div>", unsafe_allow_html=True)
    
    # ═══════════════════════════════════════════════════════════════════════
    # �📅 ADVANCED DATE RANGE FILTER
    # ═══════════════════════════════════════════════════════════════════════
    st.markdown("""
    <div style='background: linear-gradient(90deg, #00D4AA 0%, transparent 100%); padding: 0.5rem 1rem; border-radius: 8px; margin-bottom: 0.75rem;'>
        <span style='font-weight: 600; font-size: 0.95rem;'>📅 TIME RANGE</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Calculate date boundaries
    min_date = df['date'].min().date()
    max_date = df['date'].max().date()
    total_days = (max_date - min_date).days
    
    # Quick Date Presets with visual buttons
    st.markdown("<p style='color: #888; font-size: 0.8rem; margin-bottom: 0.5rem;'>⚡ Quick Select:</p>", unsafe_allow_html=True)
    
    preset_col1, preset_col2 = st.columns(2)
    with preset_col1:
        last_7d = st.button("📆 Last 7D", use_container_width=True, key="7d")
        last_30d = st.button("📅 Last 30D", use_container_width=True, key="30d")
        last_90d = st.button("🗓️ Last 90D", use_container_width=True, key="90d")
    with preset_col2:
        last_6m = st.button("📊 Last 6M", use_container_width=True, key="6m")
        last_1y = st.button("📈 Last 1Y", use_container_width=True, key="1y")
        all_time = st.button("🌐 All Time", use_container_width=True, key="all")
    
    # Initialize session state for date range
    if 'start_date' not in st.session_state:
        st.session_state.start_date = min_date
    if 'end_date' not in st.session_state:
        st.session_state.end_date = max_date
    
    # Handle preset button clicks with immediate rerun
    from datetime import timedelta
    date_changed = False
    if last_7d:
        st.session_state.start_date = max_date - timedelta(days=7)
        st.session_state.end_date = max_date
        date_changed = True
    elif last_30d:
        st.session_state.start_date = max_date - timedelta(days=30)
        st.session_state.end_date = max_date
        date_changed = True
    elif last_90d:
        st.session_state.start_date = max_date - timedelta(days=90)
        st.session_state.end_date = max_date
        date_changed = True
    elif last_6m:
        st.session_state.start_date = max_date - timedelta(days=180)
        st.session_state.end_date = max_date
        date_changed = True
    elif last_1y:
        st.session_state.start_date = max_date - timedelta(days=365)
        st.session_state.end_date = max_date
        date_changed = True
    elif all_time:
        st.session_state.start_date = min_date
        st.session_state.end_date = max_date
        date_changed = True
    
    # Force rerun if date preset was clicked
    if date_changed:
        st.rerun()
    
    # Custom date range picker
    st.markdown("<p style='color: #888; font-size: 0.8rem; margin: 0.75rem 0 0.25rem 0;'>🎯 Custom Range:</p>", unsafe_allow_html=True)
    
    date_col1, date_col2 = st.columns(2)
    with date_col1:
        start_date = st.date_input(
            "From",
            value=st.session_state.start_date,
            min_value=min_date,
            max_value=max_date,
            key="start_picker",
            on_change=lambda: setattr(st.session_state, 'start_date', st.session_state.start_picker)
        )
    with date_col2:
        end_date = st.date_input(
            "To",
            value=st.session_state.end_date,
            min_value=min_date,
            max_value=max_date,
            key="end_picker",
            on_change=lambda: setattr(st.session_state, 'end_date', st.session_state.end_picker)
        )
    
    # Sync session state with picker values for immediate reactivity
    st.session_state.start_date = start_date
    st.session_state.end_date = end_date
    
    # Store the final date range
    date_range = (start_date, end_date)
    
    # Display selected range info
    selected_days = (end_date - start_date).days + 1
    st.markdown(f"""
    <div style='background: rgba(0, 212, 170, 0.1); padding: 0.6rem; border-radius: 8px; margin-top: 0.5rem; text-align: center;'>
        <span style='color: #00D4AA; font-weight: 600; font-size: 0.85rem;'>📊 {selected_days:,} days selected</span><br/>
        <span style='color: #666; font-size: 0.7rem;'>{start_date.strftime('%b %d, %Y')} → {end_date.strftime('%b %d, %Y')}</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='margin: 1rem 0; border-top: 1px solid rgba(255,255,255,0.1);'></div>", unsafe_allow_html=True)
    
    # ═══════════════════════════════════════════════════════════════════════
    # 👤 DEMOGRAPHICS FILTERS (Collapsible)
    # ═══════════════════════════════════════════════════════════════════════
    with st.expander("👤 DEMOGRAPHICS", expanded=True):
        # Gender with icons
        gender_options = df['gender'].unique().tolist()
        gender_icons = {'Male': '👨', 'Female': '👩', 'Other': '🧑'}
        
        # Gender All/Clear buttons
        gcol1, gcol2 = st.columns(2)
        with gcol1:
            if st.button("✅ All", key="gender_all", use_container_width=True):
                st.session_state.gender_selection = gender_options
                st.rerun()
        with gcol2:
            if st.button("❌ Clear", key="gender_clear", use_container_width=True):
                st.session_state.gender_selection = []
                st.rerun()
        
        # Initialize gender selection in session state
        if 'gender_selection' not in st.session_state:
            st.session_state.gender_selection = gender_options
        
        selected_gender = st.multiselect(
            "Gender",
            options=gender_options,
            default=st.session_state.gender_selection,
            format_func=lambda x: f"{gender_icons.get(x, '👤')} {x}",
            key="gender_select"
        )
        st.session_state.gender_selection = selected_gender
        
        # Fitness Level with color coding
        fitness_options = df['fitness_level'].unique().tolist()
        fitness_order = ['Beginner', 'Intermediate', 'Advanced', 'Elite']
        fitness_options = [f for f in fitness_order if f in fitness_options]
        
        # Fitness All/Clear buttons
        fcol1, fcol2 = st.columns(2)
        with fcol1:
            if st.button("✅ All", key="fitness_all", use_container_width=True):
                st.session_state.fitness_selection = fitness_options
                st.rerun()
        with fcol2:
            if st.button("❌ Clear", key="fitness_clear", use_container_width=True):
                st.session_state.fitness_selection = []
                st.rerun()
        
        if 'fitness_selection' not in st.session_state:
            st.session_state.fitness_selection = fitness_options
        
        selected_fitness = st.multiselect(
            "Fitness Level",
            options=fitness_options,
            default=st.session_state.fitness_selection,
            format_func=lambda x: f"{'🌱' if x=='Beginner' else '🌿' if x=='Intermediate' else '🌳' if x=='Advanced' else '🏆'} {x}",
            key="fitness_select"
        )
        st.session_state.fitness_selection = selected_fitness
        
        # Age Groups
        age_options = df['age_group'].unique().tolist()
        # Sort age groups properly
        age_order = ['18-25', '26-35', '36-45', '46-55', '55+']
        age_options = [a for a in age_order if a in age_options]
        
        # Age All/Clear buttons
        acol1, acol2 = st.columns(2)
        with acol1:
            if st.button("✅ All", key="age_all", use_container_width=True):
                st.session_state.age_selection = age_options
                st.rerun()
        with acol2:
            if st.button("❌ Clear", key="age_clear", use_container_width=True):
                st.session_state.age_selection = []
                st.rerun()
        
        if 'age_selection' not in st.session_state:
            st.session_state.age_selection = age_options
        
        selected_age = st.multiselect(
            "Age Group",
            options=age_options,
            default=st.session_state.age_selection,
            format_func=lambda x: f"{'👶' if x=='18-25' else '🧑' if x=='26-35' else '👨' if x=='36-45' else '👴' if x=='46-55' else '🎖️'} {x}",
            key="age_select"
        )
        st.session_state.age_selection = selected_age
    
    # ═══════════════════════════════════════════════════════════════════════
    # 🏃 ACTIVITY FILTERS (Collapsible)
    # ═══════════════════════════════════════════════════════════════════════
    with st.expander("🏃 ACTIVITIES", expanded=True):
        activity_types = df[df['activity_type'] != 'Rest Day']['activity_type'].unique().tolist()
        activity_icons = {
            'Running': '🏃', 'Cycling': '🚴', 'Swimming': '🏊', 'Weightlifting': '🏋️',
            'HIIT': '⚡', 'Yoga': '🧘', 'CrossFit': '💪', 'Cardio': '❤️',
            'Stretching': '🤸', 'Walking': '🚶', 'Sports': '⚽'
        }
        
        # Activity All/Clear buttons
        atcol1, atcol2 = st.columns(2)
        with atcol1:
            if st.button("✅ All", key="activity_all", use_container_width=True):
                st.session_state.activity_selection = activity_types
                st.rerun()
        with atcol2:
            if st.button("❌ Clear", key="activity_clear", use_container_width=True):
                st.session_state.activity_selection = []
                st.rerun()
        
        if 'activity_selection' not in st.session_state:
            st.session_state.activity_selection = activity_types
        
        selected_activities = st.multiselect(
            "Activity Type",
            options=activity_types,
            default=st.session_state.activity_selection,
            format_func=lambda x: f"{activity_icons.get(x, '🎯')} {x}",
            key="activity_select"
        )
        st.session_state.activity_selection = selected_activities
        
        # Primary Sports
        sport_options = df['primary_sport'].unique().tolist()
        
        # Sport All/Clear buttons
        spcol1, spcol2 = st.columns(2)
        with spcol1:
            if st.button("✅ All", key="sport_all", use_container_width=True):
                st.session_state.sport_selection = sport_options
                st.rerun()
        with spcol2:
            if st.button("❌ Clear", key="sport_clear", use_container_width=True):
                st.session_state.sport_selection = []
                st.rerun()
        
        if 'sport_selection' not in st.session_state:
            st.session_state.sport_selection = sport_options
        
        selected_sports = st.multiselect(
            "Primary Sport",
            options=sport_options,
            default=st.session_state.sport_selection,
            format_func=lambda x: f"🏅 {x}",
            key="sport_select"
        )
        st.session_state.sport_selection = selected_sports
    
    # ═══════════════════════════════════════════════════════════════════════
    # 🌤️ SEASON & PERFORMANCE FILTERS (Collapsible)
    # ═══════════════════════════════════════════════════════════════════════
    with st.expander("🌤️ SEASONS & MORE", expanded=False):
        season_icons = {'Winter': '❄️', 'Spring': '🌸', 'Summer': '☀️', 'Fall': '🍂'}
        season_options = ['Winter', 'Spring', 'Summer', 'Fall']
        
        # Season All/Clear buttons
        secol1, secol2 = st.columns(2)
        with secol1:
            if st.button("✅ All", key="season_all", use_container_width=True):
                st.session_state.season_selection = season_options
                st.rerun()
        with secol2:
            if st.button("❌ Clear", key="season_clear", use_container_width=True):
                st.session_state.season_selection = []
                st.rerun()
        
        if 'season_selection' not in st.session_state:
            st.session_state.season_selection = season_options
        
        selected_seasons = st.multiselect(
            "Season",
            options=season_options,
            default=st.session_state.season_selection,
            format_func=lambda x: f"{season_icons.get(x, '🌍')} {x}",
            key="season_select"
        )
        st.session_state.season_selection = selected_seasons
        
        st.markdown("<p style='color: #888; font-size: 0.75rem; margin-top: 1rem;'>🎚️ Recovery Filter:</p>", unsafe_allow_html=True)
        recovery_range = st.slider(
            "Recovery Score Range",
            min_value=0,
            max_value=100,
            value=(0, 100),
            format="%d%%"
        )
        
        st.markdown("<p style='color: #888; font-size: 0.75rem; margin-top: 0.5rem;'>💪 Strain Filter:</p>", unsafe_allow_html=True)
        strain_range = st.slider(
            "Day Strain Range",
            min_value=0.0,
            max_value=float(df['day_strain'].max()),
            value=(0.0, float(df['day_strain'].max())),
            format="%.1f"
        )
    
    st.markdown("<div style='margin: 1rem 0; border-top: 1px solid rgba(255,255,255,0.1);'></div>", unsafe_allow_html=True)
    
    # ═══════════════════════════════════════════════════════════════════════
    # 📊 FILTER SUMMARY & ACTIONS
    # ═══════════════════════════════════════════════════════════════════════
    st.markdown("""
    <div style='background: linear-gradient(135deg, #1a2035 0%, #0a0f1a 100%); padding: 1rem; border-radius: 12px; border: 1px solid rgba(0, 212, 170, 0.2);'>
        <p style='color: #00D4AA; font-weight: 600; font-size: 0.85rem; margin-bottom: 0.5rem;'>📋 FILTER SUMMARY</p>
    </div>
    """, unsafe_allow_html=True)


# Apply filters (including new recovery and strain filters)
mask = (
    (df['date'].dt.date >= date_range[0]) &
    (df['date'].dt.date <= date_range[1]) &
    (df['gender'].isin(selected_gender)) &
    (df['fitness_level'].isin(selected_fitness)) &
    (df['age_group'].isin(selected_age)) &
    (df['primary_sport'].isin(selected_sports)) &
    (df['season'].isin(selected_seasons)) &
    (df['recovery_score'] >= recovery_range[0]) &
    (df['recovery_score'] <= recovery_range[1]) &
    (df['day_strain'] >= strain_range[0]) &
    (df['day_strain'] <= strain_range[1])
)
filtered_df = df[mask].copy()

# Activity filter for workout data
workout_df = filtered_df[
    (filtered_df['workout_completed'] == 1) & 
    (filtered_df['activity_type'].isin(selected_activities))
]

# Update sidebar with live filter stats
with st.sidebar:
    total_records = len(df)
    filtered_records = len(filtered_df)
    filter_pct = (filtered_records / total_records) * 100
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, rgba(0, 212, 170, 0.15) 0%, rgba(0, 160, 128, 0.1) 100%); padding: 1rem; border-radius: 10px; margin-top: 0.5rem; text-align: center; border: 1px solid rgba(0, 212, 170, 0.3);'>
        <div style='display: flex; justify-content: space-around; margin-bottom: 0.5rem;'>
            <div>
                <span style='color: #888; font-size: 0.7rem;'>TOTAL</span><br/>
                <span style='color: #fff; font-size: 1.1rem; font-weight: 700;'>{total_records:,}</span>
            </div>
            <div style='border-left: 1px solid rgba(255,255,255,0.2); padding-left: 1rem;'>
                <span style='color: #888; font-size: 0.7rem;'>FILTERED</span><br/>
                <span style='color: #00D4AA; font-size: 1.1rem; font-weight: 700;'>{filtered_records:,}</span>
            </div>
        </div>
        <div style='background: #1a1f2e; border-radius: 4px; height: 6px; margin: 0.5rem 0;'>
            <div style='background: linear-gradient(90deg, #00D4AA, #00A080); width: {filter_pct}%; height: 100%; border-radius: 4px;'></div>
        </div>
        <span style='color: #00D4AA; font-size: 0.8rem; font-weight: 600;'>{filter_pct:.1f}% of data</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Unique users and workouts stats
    unique_users = filtered_df['user_id'].nunique()
    total_workouts = len(workout_df)
    
    st.markdown(f"""
    <div style='display: flex; justify-content: space-around; margin-top: 1rem; text-align: center;'>
        <div style='background: rgba(0, 212, 170, 0.1); padding: 0.75rem; border-radius: 8px; flex: 1; margin-right: 0.5rem;'>
            <span style='color: #888; font-size: 0.65rem;'>USERS</span><br/>
            <span style='color: #00D4AA; font-size: 1rem; font-weight: 600;'>👤 {unique_users:,}</span>
        </div>
        <div style='background: rgba(0, 212, 170, 0.1); padding: 0.75rem; border-radius: 8px; flex: 1;'>
            <span style='color: #888; font-size: 0.65rem;'>WORKOUTS</span><br/>
            <span style='color: #00D4AA; font-size: 1rem; font-weight: 600;'>🏋️ {total_workouts:,}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div style='margin-top: 2rem; padding-top: 1rem; border-top: 1px solid rgba(255,255,255,0.1); text-align: center;'>
        <p style='color: #666; font-size: 0.7rem; margin: 0;'>Built with ❤️ for University Project</p>
        <p style='color: #444; font-size: 0.6rem; margin: 0.25rem 0 0 0;'>Streamlit • Plotly • scikit-learn</p>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# MAIN HEADER
# ============================================================================
st.markdown("""
<div class="main-header">
    <h1>🏋️ WHOOP Fitness Analytics Dashboard</h1>
    <p>Comprehensive Data Visualization & Advanced Analytics Platform</p>
</div>
""", unsafe_allow_html=True)


# ============================================================================
# KEY METRICS ROW
# ============================================================================
st.markdown("### 📊 Key Performance Indicators")

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    avg_recovery = filtered_df['recovery_score'].mean()
    st.metric("Avg Recovery", f"{avg_recovery:.1f}%", 
              delta=f"{avg_recovery - 65:.1f}% vs baseline")

with col2:
    avg_strain = filtered_df['day_strain'].mean()
    st.metric("Avg Day Strain", f"{avg_strain:.1f}", 
              delta=f"{avg_strain - 10:.1f} vs baseline")

with col3:
    avg_sleep = filtered_df['sleep_hours'].mean()
    st.metric("Avg Sleep", f"{avg_sleep:.1f}h", 
              delta=f"{avg_sleep - 7:.1f}h vs recommended")

with col4:
    avg_hrv = filtered_df['hrv'].mean()
    st.metric("Avg HRV", f"{avg_hrv:.0f}ms", 
              delta=f"{avg_hrv - 50:.0f}ms vs baseline")

with col5:
    workout_rate = (filtered_df['workout_completed'].sum() / len(filtered_df)) * 100
    st.metric("Workout Rate", f"{workout_rate:.1f}%", 
              delta=f"{workout_rate - 50:.1f}%")

with col6:
    total_users = filtered_df['user_id'].nunique()
    st.metric("Active Users", f"{total_users:,}", 
              delta=f"{len(filtered_df):,} records")


# ============================================================================
# NAVIGATION TABS
# ============================================================================
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "🟢 Live Feed",
    "🌳 Overview & Treemap",
    "📈 Trends & Dual-Axis", 
    "🔥 Heatmaps & Seasons",
    "🎯 Advanced Charts",
    "🧠 ML & Clustering",
    "🔮 What-If Analysis",
    "📊 Association Mining"
])


# ============================================================================
# TAB 0: LIVE DATA FEED
# ============================================================================
with tab1:
    # Check data source selection
    if st.session_state.get('data_source', '📁 Fixed Dataset') == "🔴 Live Feed":
        st.markdown("### 🔴 Real-Time WHOOP Data Feed")
        st.markdown("> **Live streaming data from WHOOP devices** - Updates every 3 seconds with synthetic fitness metrics")
        
        # Auto-refresh settings
        live_col1, live_col2, live_col3 = st.columns([2, 1, 1])
        with live_col1:
            auto_refresh = st.checkbox("🔄 Enable Auto-Refresh", value=False, key="auto_refresh")
        with live_col2:
            refresh_rate = st.selectbox("Refresh Rate (sec)", [3, 5, 10, 30], index=1, key="refresh_rate")
        with live_col3:
            if st.button("🔄 Refresh Now", key="manual_refresh"):
                st.rerun()
        
        # Load live data
        live_data_path = '/app/data/live_data.csv'
        
        if os.path.exists(live_data_path):
            try:
                live_df = pd.read_csv(live_data_path)
                
                if len(live_df) > 0:
                    # Convert timestamp
                    live_df['timestamp'] = pd.to_datetime(live_df['timestamp'])
                    
                    # ═══════════════════════════════════════════════════════════════
                    # LIVE METRICS HEADER
                    # ═══════════════════════════════════════════════════════════════
                    st.markdown("---")
                    st.markdown("### 📊 Live Metrics Dashboard")
                    
                    lm1, lm2, lm3, lm4, lm5 = st.columns(5)
                    
                    with lm1:
                        st.markdown("""
                        <div style='background: linear-gradient(135deg, #1a2035 0%, #0d1117 100%); 
                                    padding: 1.2rem; border-radius: 12px; text-align: center;
                                    border: 1px solid rgba(0, 212, 170, 0.3);'>
                            <p style='color: #888; margin: 0; font-size: 0.75rem;'>🟢 LIVE RECORDS</p>
                            <h2 style='color: #00D4AA; margin: 0.3rem 0;'>{:,}</h2>
                            <p style='color: #00D4AA; margin: 0; font-size: 0.8rem;'>⚡ Streaming</p>
                        </div>
                        """.format(len(live_df)), unsafe_allow_html=True)
                    
                    with lm2:
                        active_users = live_df['user_id'].nunique()
                        st.markdown("""
                        <div style='background: linear-gradient(135deg, #1a2035 0%, #0d1117 100%); 
                                    padding: 1.2rem; border-radius: 12px; text-align: center;
                                    border: 1px solid rgba(59, 130, 246, 0.3);'>
                            <p style='color: #888; margin: 0; font-size: 0.75rem;'>👥 ACTIVE USERS</p>
                            <h2 style='color: #3B82F6; margin: 0.3rem 0;'>{}</h2>
                            <p style='color: #3B82F6; margin: 0; font-size: 0.8rem;'>Connected</p>
                        </div>
                        """.format(active_users), unsafe_allow_html=True)
                    
                    with lm3:
                        avg_recovery_live = live_df['recovery_score'].mean()
                        st.markdown("""
                        <div style='background: linear-gradient(135deg, #1a2035 0%, #0d1117 100%); 
                                    padding: 1.2rem; border-radius: 12px; text-align: center;
                                    border: 1px solid rgba(34, 197, 94, 0.3);'>
                            <p style='color: #888; margin: 0; font-size: 0.75rem;'>💚 AVG RECOVERY</p>
                            <h2 style='color: #22C55E; margin: 0.3rem 0;'>{:.1f}%</h2>
                            <p style='color: #22C55E; margin: 0; font-size: 0.8rem;'>Real-time</p>
                        </div>
                        """.format(avg_recovery_live), unsafe_allow_html=True)
                    
                    with lm4:
                        avg_strain_live = live_df['day_strain'].mean()
                        st.markdown("""
                        <div style='background: linear-gradient(135deg, #1a2035 0%, #0d1117 100%); 
                                    padding: 1.2rem; border-radius: 12px; text-align: center;
                                    border: 1px solid rgba(239, 68, 68, 0.3);'>
                            <p style='color: #888; margin: 0; font-size: 0.75rem;'>💪 AVG STRAIN</p>
                            <h2 style='color: #EF4444; margin: 0.3rem 0;'>{:.1f}</h2>
                            <p style='color: #EF4444; margin: 0; font-size: 0.8rem;'>Intensity</p>
                        </div>
                        """.format(avg_strain_live), unsafe_allow_html=True)
                    
                    with lm5:
                        workouts_now = live_df[live_df['workout_completed'] == 1]['user_id'].nunique()
                        st.markdown("""
                        <div style='background: linear-gradient(135deg, #1a2035 0%, #0d1117 100%); 
                                    padding: 1.2rem; border-radius: 12px; text-align: center;
                                    border: 1px solid rgba(168, 85, 247, 0.3);'>
                            <p style='color: #888; margin: 0; font-size: 0.75rem;'>🏋️ WORKOUTS</p>
                            <h2 style='color: #A855F7; margin: 0.3rem 0;'>{}</h2>
                            <p style='color: #A855F7; margin: 0; font-size: 0.8rem;'>In Progress</p>
                        </div>
                        """.format(workouts_now), unsafe_allow_html=True)
                    
                    st.markdown("---")
                    
                    # ═══════════════════════════════════════════════════════════════
                    # LIVE CHARTS ROW 1
                    # ═══════════════════════════════════════════════════════════════
                    live_chart1, live_chart2 = st.columns(2)
                    
                    with live_chart1:
                        st.markdown("#### 📈 Recovery Score Stream")
                        live_sorted = live_df.sort_values('timestamp').tail(100)
                        
                        fig_live_recovery = go.Figure()
                        fig_live_recovery.add_trace(go.Scatter(
                            x=live_sorted['timestamp'],
                            y=live_sorted['recovery_score'],
                            mode='lines+markers',
                            name='Recovery',
                            line=dict(color='#00D4AA', width=2),
                            marker=dict(size=6),
                            fill='tozeroy',
                            fillcolor='rgba(0, 212, 170, 0.1)'
                        ))
                        fig_live_recovery.add_hline(y=66, line_dash="dash", line_color="green", annotation_text="Green Zone")
                        fig_live_recovery.add_hline(y=33, line_dash="dash", line_color="red", annotation_text="Red Zone")
                        fig_live_recovery.update_layout(template='plotly_dark', height=350, margin=dict(l=20, r=20, t=30, b=20), xaxis_title="Time", yaxis_title="Recovery %", yaxis_range=[0, 100])
                        st.plotly_chart(fig_live_recovery, use_container_width=True)
                    
                    with live_chart2:
                        st.markdown("#### 💪 Day Strain Stream")
                        fig_live_strain = go.Figure()
                        fig_live_strain.add_trace(go.Scatter(
                            x=live_sorted['timestamp'],
                            y=live_sorted['day_strain'],
                            mode='lines+markers',
                            name='Strain',
                            line=dict(color='#FF6B6B', width=2),
                            marker=dict(size=6),
                            fill='tozeroy',
                            fillcolor='rgba(255, 107, 107, 0.1)'
                        ))
                        fig_live_strain.update_layout(template='plotly_dark', height=350, margin=dict(l=20, r=20, t=30, b=20), xaxis_title="Time", yaxis_title="Strain", yaxis_range=[0, 21])
                        st.plotly_chart(fig_live_strain, use_container_width=True)
                    
                    # ═══════════════════════════════════════════════════════════════
                    # LIVE CHARTS ROW 2
                    # ═══════════════════════════════════════════════════════════════
                    live_chart3, live_chart4 = st.columns(2)
                    
                    with live_chart3:
                        st.markdown("#### ❤️ HRV Distribution (Live)")
                        fig_hrv_dist = px.histogram(live_df, x='hrv', nbins=30, color_discrete_sequence=['#9B59B6'], title='Heart Rate Variability Distribution')
                        fig_hrv_dist.update_layout(template='plotly_dark', height=300, showlegend=False, margin=dict(l=20, r=20, t=40, b=20))
                        st.plotly_chart(fig_hrv_dist, use_container_width=True)
                    
                    with live_chart4:
                        st.markdown("#### 🏋️ Activity Breakdown (Live)")
                        activity_counts = live_df['activity_type'].value_counts()
                        fig_activity_pie = px.pie(values=activity_counts.values, names=activity_counts.index, title='Current Activity Distribution', hole=0.4, color_discrete_sequence=px.colors.qualitative.Set2)
                        fig_activity_pie.update_layout(template='plotly_dark', height=300, margin=dict(l=20, r=20, t=40, b=20))
                        st.plotly_chart(fig_activity_pie, use_container_width=True)
                    
                    st.markdown("---")
                    st.markdown("#### 📝 Latest Records (Live Stream)")
                    display_cols = ['timestamp', 'user_id', 'fitness_level', 'recovery_score', 'day_strain', 'hrv', 'activity_type', 'workout_completed']
                    latest_records = live_df.sort_values('timestamp', ascending=False).head(20)[display_cols]
                    st.dataframe(latest_records, use_container_width=True, height=300)
                    
                else:
                    st.info("⏳ Waiting for live data... The data generator is initializing.")
            
            except Exception as e:
                st.error(f"❌ Error loading live data: {e}")
                st.info("Make sure the data generator service is running.")
        
        else:
            st.warning("""
            ### 🟠 Live Data Service Not Running
            
            The live data generator service is not active. To start it:
            
            ```bash
            docker-compose up -d
            ```
            
            This will start both the dashboard and the live data generator.
            """)
        
        # Auto-refresh at end of tab (after content loads)
        if auto_refresh:
            st.markdown(f"<p style='color: #00D4AA; font-size: 0.8rem;'>⏱️ Auto-refresh enabled - refreshing every {refresh_rate}s</p>", unsafe_allow_html=True)
            import time as time_module
            time_module.sleep(refresh_rate)
            st.rerun()
    
    else:
        # FIXED DATASET VIEW
        st.markdown("### 📁 Fixed Dataset Overview")
        st.markdown("> **Viewing your fixed synthetic dataset** - 100K+ records from whoop_fitness.csv")
        
        # Dataset stats
        st.markdown("---")
        st.markdown("### 📊 Dataset Statistics")
        
        ds1, ds2, ds3, ds4, ds5 = st.columns(5)
        
        with ds1:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #1a2035 0%, #0d1117 100%); 
                        padding: 1.2rem; border-radius: 12px; text-align: center;
                        border: 1px solid rgba(59, 130, 246, 0.3);'>
                <p style='color: #888; margin: 0; font-size: 0.75rem;'>📁 TOTAL RECORDS</p>
                <h2 style='color: #3B82F6; margin: 0.3rem 0;'>{len(filtered_df):,}</h2>
                <p style='color: #3B82F6; margin: 0; font-size: 0.8rem;'>Filtered</p>
            </div>
            """, unsafe_allow_html=True)
        
        with ds2:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #1a2035 0%, #0d1117 100%); 
                        padding: 1.2rem; border-radius: 12px; text-align: center;
                        border: 1px solid rgba(0, 212, 170, 0.3);'>
                <p style='color: #888; margin: 0; font-size: 0.75rem;'>👥 UNIQUE USERS</p>
                <h2 style='color: #00D4AA; margin: 0.3rem 0;'>{filtered_df['user_id'].nunique():,}</h2>
                <p style='color: #00D4AA; margin: 0; font-size: 0.8rem;'>In dataset</p>
            </div>
            """, unsafe_allow_html=True)
        
        with ds3:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #1a2035 0%, #0d1117 100%); 
                        padding: 1.2rem; border-radius: 12px; text-align: center;
                        border: 1px solid rgba(34, 197, 94, 0.3);'>
                <p style='color: #888; margin: 0; font-size: 0.75rem;'>💚 AVG RECOVERY</p>
                <h2 style='color: #22C55E; margin: 0.3rem 0;'>{filtered_df['recovery_score'].mean():.1f}%</h2>
                <p style='color: #22C55E; margin: 0; font-size: 0.8rem;'>Score</p>
            </div>
            """, unsafe_allow_html=True)
        
        with ds4:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #1a2035 0%, #0d1117 100%); 
                        padding: 1.2rem; border-radius: 12px; text-align: center;
                        border: 1px solid rgba(239, 68, 68, 0.3);'>
                <p style='color: #888; margin: 0; font-size: 0.75rem;'>💪 AVG STRAIN</p>
                <h2 style='color: #EF4444; margin: 0.3rem 0;'>{filtered_df['day_strain'].mean():.1f}</h2>
                <p style='color: #EF4444; margin: 0; font-size: 0.8rem;'>Intensity</p>
            </div>
            """, unsafe_allow_html=True)
        
        with ds5:
            workout_count = filtered_df[filtered_df['workout_completed'] == 1].shape[0]
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #1a2035 0%, #0d1117 100%); 
                        padding: 1.2rem; border-radius: 12px; text-align: center;
                        border: 1px solid rgba(168, 85, 247, 0.3);'>
                <p style='color: #888; margin: 0; font-size: 0.75rem;'>🏋️ WORKOUTS</p>
                <h2 style='color: #A855F7; margin: 0.3rem 0;'>{workout_count:,}</h2>
                <p style='color: #A855F7; margin: 0; font-size: 0.8rem;'>Completed</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Quick overview charts
        st.markdown("### 📈 Data Overview")
        
        ov1, ov2 = st.columns(2)
        
        with ov1:
            # Recovery distribution
            fig_rec = px.histogram(filtered_df, x='recovery_score', nbins=30,
                                  color_discrete_sequence=['#00D4AA'],
                                  title='Recovery Score Distribution')
            fig_rec.update_layout(template='plotly_dark', height=350)
            st.plotly_chart(fig_rec, use_container_width=True)
        
        with ov2:
            # Activity breakdown
            activity_counts = filtered_df['activity_type'].value_counts().head(10)
            fig_act = px.bar(x=activity_counts.index, y=activity_counts.values,
                            color_discrete_sequence=['#6366F1'],
                            title='Top 10 Activity Types')
            fig_act.update_layout(template='plotly_dark', height=350, 
                                 xaxis_title='Activity', yaxis_title='Count')
            st.plotly_chart(fig_act, use_container_width=True)
        
        # Data sample table
        st.markdown("### 📋 Data Sample (Last 20 Records)")
        display_cols = ['date', 'user_id', 'fitness_level', 'recovery_score', 
                       'day_strain', 'hrv', 'activity_type', 'workout_completed']
        sample_records = filtered_df.sort_values('date', ascending=False).head(20)[display_cols]
        st.dataframe(sample_records, use_container_width=True, height=400)
        
        # Tip to switch to live
        st.markdown("---")
        st.info("💡 **Tip:** Switch to '🔴 Live Feed' in the sidebar to see real-time streaming data!")


# ============================================================================
# TAB 2: OVERVIEW & TREEMAP (was Tab 1)
# ============================================================================
with tab2:
    st.markdown("### 🌳 Hierarchical Activity Breakdown")
    st.markdown("> **Insight:** This treemap reveals the hierarchical distribution of workout activities, showing which sports and activity types dominate user behavior patterns.")
    
    # Prepare treemap data
    treemap_data = workout_df.groupby(['fitness_level', 'primary_sport', 'activity_type']).agg({
        'activity_calories': 'sum',
        'activity_duration_min': 'sum',
        'user_id': 'count'
    }).reset_index()
    treemap_data.columns = ['Fitness Level', 'Primary Sport', 'Activity Type', 'Total Calories', 'Total Duration', 'Sessions']
    
    fig_tree = px.treemap(
        treemap_data,
        path=['Fitness Level', 'Primary Sport', 'Activity Type'],
        values='Total Calories',
        color='Sessions',
        color_continuous_scale='Emrld',
        title='Activity Hierarchy by Calories Burned & Session Count',
        hover_data={'Total Duration': True, 'Sessions': True}
    )
    fig_tree.update_layout(height=600, template='plotly_dark')
    st.plotly_chart(fig_tree, use_container_width=True)
    
    st.markdown("---")
    
    # Sunburst Chart - Multi-level
    st.markdown("### 🌞 Multi-Level Sunburst: User Behavior Patterns")
    st.markdown("> **Insight:** The sunburst chart displays nested categorical relationships, helping identify which demographic segments prefer specific workout types and times.")
    
    if len(workout_df) > 0:
        sunburst_data = workout_df.groupby(['gender', 'age_group', 'workout_time_of_day', 'activity_type']).agg({
            'activity_strain': 'mean',
            'user_id': 'count'
        }).reset_index()
        sunburst_data.columns = ['Gender', 'Age Group', 'Time of Day', 'Activity', 'Avg Strain', 'Count']
        
        # Filter out rows with zero counts to avoid division errors
        sunburst_data = sunburst_data[sunburst_data['Count'] > 0]
        
        if len(sunburst_data) > 0:
            fig_sunburst = px.sunburst(
                sunburst_data,
                path=['Gender', 'Age Group', 'Time of Day', 'Activity'],
                values='Count',
                color='Avg Strain',
                color_continuous_scale='RdYlGn_r',
                title='Workout Patterns: Demographics → Time → Activity Type'
            )
            fig_sunburst.update_layout(height=600, template='plotly_dark')
            st.plotly_chart(fig_sunburst, use_container_width=True)
        else:
            st.info("📊 Not enough data for sunburst chart with current filters. Try expanding your date range or filter selections.")
    else:
        st.info("📊 No workout data available for sunburst chart. Try adjusting your filters.")
    
    # Recovery Distribution Doughnut
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🍩 Recovery Score Distribution")
        st.markdown("> **Insight:** Shows the proportion of users in each recovery zone (Green/Yellow/Red), critical for understanding overall fitness readiness.")
        
        recovery_dist = filtered_df['recovery_category'].value_counts()
        colors = {'Green (High)': '#00D4AA', 'Yellow (Moderate)': '#FFD700', 'Red (Low)': '#FF4444'}
        
        fig_doughnut = go.Figure(data=[go.Pie(
            labels=recovery_dist.index,
            values=recovery_dist.values,
            hole=0.6,
            marker_colors=[colors.get(x, '#888') for x in recovery_dist.index],
            textinfo='percent+label',
            textposition='outside'
        )])
        fig_doughnut.update_layout(
            title='Recovery Zone Distribution',
            template='plotly_dark',
            height=400,
            annotations=[dict(text='Recovery', x=0.5, y=0.5, font_size=16, showarrow=False)]
        )
        st.plotly_chart(fig_doughnut, use_container_width=True)
    
    with col2:
        st.markdown("### 🎯 Fitness Level Distribution")
        st.markdown("> **Insight:** Pie chart showing the breakdown of users across beginner, intermediate, and advanced fitness levels.")
        
        fitness_dist = filtered_df['fitness_level'].value_counts()
        
        fig_pie = px.pie(
            values=fitness_dist.values,
            names=fitness_dist.index,
            color_discrete_sequence=px.colors.sequential.Emrld,
            title='User Fitness Level Breakdown'
        )
        fig_pie.update_traces(textposition='outside', textinfo='percent+label')
        fig_pie.update_layout(template='plotly_dark', height=400)
        st.plotly_chart(fig_pie, use_container_width=True)


# ============================================================================
# TAB 2: TRENDS & DUAL-AXIS CHARTS
# ============================================================================
with tab2:
    st.markdown("### 📈 Dual-Axis Analysis: Recovery vs Strain Over Time")
    st.markdown("> **Insight:** This dual-axis chart reveals the inverse relationship between recovery and strain, showing how pushing harder leads to lower recovery scores the following day.")
    
    # Weekly aggregation for cleaner trends
    weekly_data = filtered_df.groupby('week').agg({
        'recovery_score': 'mean',
        'day_strain': 'mean',
        'hrv': 'mean',
        'sleep_hours': 'mean'
    }).reset_index()
    
    # Dual Axis Chart
    fig_dual = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig_dual.add_trace(
        go.Scatter(x=weekly_data['week'], y=weekly_data['recovery_score'],
                   name="Recovery Score", line=dict(color='#00D4AA', width=3),
                   fill='tozeroy', fillcolor='rgba(0, 212, 170, 0.1)'),
        secondary_y=False
    )
    
    fig_dual.add_trace(
        go.Scatter(x=weekly_data['week'], y=weekly_data['day_strain'],
                   name="Day Strain", line=dict(color='#FF6B6B', width=3),
                   fill='tozeroy', fillcolor='rgba(255, 107, 107, 0.1)'),
        secondary_y=True
    )
    
    fig_dual.update_xaxes(title_text="Week of Year", gridcolor='#333')
    fig_dual.update_yaxes(title_text="Recovery Score (%)", secondary_y=False, gridcolor='#333')
    fig_dual.update_yaxes(title_text="Day Strain", secondary_y=True)
    fig_dual.update_layout(
        title='Weekly Recovery Score vs Day Strain Trend',
        template='plotly_dark',
        height=500,
        hovermode='x unified',
        legend=dict(orientation='h', yanchor='bottom', y=1.02)
    )
    st.plotly_chart(fig_dual, use_container_width=True)
    
    st.markdown("---")
    
    # HRV vs Sleep Dual Axis
    st.markdown("### 💓 HRV & Sleep Quality Correlation")
    st.markdown("> **Insight:** Heart Rate Variability (HRV) strongly correlates with sleep quality - better sleep leads to higher HRV, indicating better recovery and fitness.")
    
    fig_hrv_sleep = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig_hrv_sleep.add_trace(
        go.Scatter(x=weekly_data['week'], y=weekly_data['hrv'],
                   name="HRV (ms)", line=dict(color='#9B59B6', width=3)),
        secondary_y=False
    )
    
    fig_hrv_sleep.add_trace(
        go.Scatter(x=weekly_data['week'], y=weekly_data['sleep_hours'],
                   name="Sleep Hours", line=dict(color='#3498DB', width=3)),
        secondary_y=True
    )
    
    fig_hrv_sleep.update_layout(
        title='Weekly HRV vs Sleep Hours',
        template='plotly_dark',
        height=450,
        hovermode='x unified'
    )
    st.plotly_chart(fig_hrv_sleep, use_container_width=True)
    
    st.markdown("---")
    
    # Waterfall Chart - Calorie Burn Breakdown
    st.markdown("### 💧 Waterfall: Cumulative Calorie Burn by Activity")
    st.markdown("> **Insight:** Waterfall chart breaks down how each activity type contributes to total calorie expenditure, showing the cumulative impact of workout choices.")
    
    calorie_by_activity = workout_df.groupby('activity_type')['activity_calories'].sum().sort_values(ascending=False).head(10)
    
    fig_waterfall = go.Figure(go.Waterfall(
        name="Calories",
        orientation="v",
        x=calorie_by_activity.index.tolist() + ['Total'],
        y=calorie_by_activity.values.tolist() + [calorie_by_activity.sum()],
        connector={"line": {"color": "#00D4AA"}},
        increasing={"marker": {"color": "#00D4AA"}},
        decreasing={"marker": {"color": "#FF6B6B"}},
        totals={"marker": {"color": "#3498DB"}},
        text=[f"{x:,.0f}" for x in calorie_by_activity.values.tolist()] + [f"{calorie_by_activity.sum():,.0f}"],
        textposition="outside"
    ))
    
    fig_waterfall.update_layout(
        title='Cumulative Calorie Burn by Activity Type',
        template='plotly_dark',
        height=500,
        showlegend=False
    )
    st.plotly_chart(fig_waterfall, use_container_width=True)


# ============================================================================
# TAB 4: HEATMAPS & SEASONAL ANALYSIS (was Tab 3)
# ============================================================================
with tab4:
    st.markdown("### 🔥 Seasonal Activity Heatmap")
    st.markdown("> **Insight:** This heatmap reveals workout intensity patterns across seasons and days of the week, showing when users push hardest and when they recover.")
    
    # Day of week order
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    # Seasonal heatmap
    season_day_strain = filtered_df.groupby(['season', 'day_of_week'])['day_strain'].mean().reset_index()
    season_pivot = season_day_strain.pivot(index='season', columns='day_of_week', values='day_strain')
    season_pivot = season_pivot.reindex(columns=day_order)
    
    fig_season_heat = px.imshow(
        season_pivot,
        labels=dict(x="Day of Week", y="Season", color="Avg Strain"),
        color_continuous_scale='RdYlGn_r',
        aspect='auto',
        title='Average Day Strain by Season & Day of Week'
    )
    fig_season_heat.update_layout(template='plotly_dark', height=400)
    st.plotly_chart(fig_season_heat, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 😴 Sleep Quality Heatmap")
        st.markdown("> **Insight:** Shows sleep efficiency patterns - identifying which days and months users achieve optimal sleep quality.")
        
        monthly_day_sleep = filtered_df.groupby(['month_name', 'day_of_week'])['sleep_efficiency'].mean().reset_index()
        month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                       'July', 'August', 'September', 'October', 'November', 'December']
        monthly_pivot = monthly_day_sleep.pivot(index='month_name', columns='day_of_week', values='sleep_efficiency')
        monthly_pivot = monthly_pivot.reindex(index=month_order, columns=day_order)
        
        fig_sleep_heat = px.imshow(
            monthly_pivot,
            labels=dict(x="Day", y="Month", color="Sleep Eff %"),
            color_continuous_scale='Blues',
            aspect='auto',
            title='Sleep Efficiency by Month & Day'
        )
        fig_sleep_heat.update_layout(template='plotly_dark', height=450)
        st.plotly_chart(fig_sleep_heat, use_container_width=True)
    
    with col2:
        st.markdown("### 💚 Recovery Score Heatmap")
        st.markdown("> **Insight:** Recovery patterns by time reveal when users are best prepared for intense training.")
        
        recovery_heatmap = filtered_df.groupby(['month_name', 'day_of_week'])['recovery_score'].mean().reset_index()
        recovery_pivot = recovery_heatmap.pivot(index='month_name', columns='day_of_week', values='recovery_score')
        recovery_pivot = recovery_pivot.reindex(index=month_order, columns=day_order)
        
        fig_recovery_heat = px.imshow(
            recovery_pivot,
            labels=dict(x="Day", y="Month", color="Recovery %"),
            color_continuous_scale='Greens',
            aspect='auto',
            title='Recovery Score by Month & Day'
        )
        fig_recovery_heat.update_layout(template='plotly_dark', height=450)
        st.plotly_chart(fig_recovery_heat, use_container_width=True)
    
    st.markdown("---")
    
    # Heart Rate Zone Heatmap
    st.markdown("### ❤️ Heart Rate Zone Distribution by Activity")
    st.markdown("> **Insight:** Shows which activities push users into high-intensity zones (Zone 4-5), useful for training periodization.")
    
    hr_zones = workout_df.groupby('activity_type')[['hr_zone_1_min', 'hr_zone_2_min', 'hr_zone_3_min', 
                                                     'hr_zone_4_min', 'hr_zone_5_min']].mean()
    hr_zones.columns = ['Zone 1 (Rest)', 'Zone 2 (Easy)', 'Zone 3 (Aerobic)', 'Zone 4 (Threshold)', 'Zone 5 (Max)']
    
    fig_hr_heat = px.imshow(
        hr_zones.T,
        labels=dict(x="Activity Type", y="HR Zone", color="Minutes"),
        color_continuous_scale='YlOrRd',
        aspect='auto',
        title='Average Time in Heart Rate Zones by Activity Type'
    )
    fig_hr_heat.update_layout(template='plotly_dark', height=400)
    st.plotly_chart(fig_hr_heat, use_container_width=True)


# ============================================================================
# TAB 5: ADVANCED CHARTS (was Tab 4)
# ============================================================================
with tab5:
    st.markdown("### 🎻 Violin Plot: Recovery Distribution by Fitness Level")
    st.markdown("> **Insight:** Violin plots show the full distribution shape - advanced athletes have tighter recovery distributions, while beginners show more variability.")
    
    fig_violin = px.violin(
        filtered_df, x='fitness_level', y='recovery_score',
        color='fitness_level', box=True, points='outliers',
        color_discrete_sequence=['#00D4AA', '#FFD700', '#FF6B6B'],
        title='Recovery Score Distribution by Fitness Level'
    )
    fig_violin.update_layout(template='plotly_dark', height=500, showlegend=False)
    st.plotly_chart(fig_violin, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📦 Box Plot: Sleep Metrics Comparison")
        st.markdown("> **Insight:** Box plots reveal median values and outliers - deep sleep hours show the most variability across users.")
        
        sleep_melt = filtered_df[['light_sleep_hours', 'rem_sleep_hours', 'deep_sleep_hours', 'fitness_level']].melt(
            id_vars='fitness_level', var_name='Sleep Stage', value_name='Hours'
        )
        sleep_melt['Sleep Stage'] = sleep_melt['Sleep Stage'].str.replace('_hours', '').str.replace('_', ' ').str.title()
        
        fig_box = px.box(
            sleep_melt, x='Sleep Stage', y='Hours', color='fitness_level',
            color_discrete_sequence=['#00D4AA', '#FFD700', '#FF6B6B'],
            title='Sleep Stage Duration by Fitness Level'
        )
        fig_box.update_layout(template='plotly_dark', height=450)
        st.plotly_chart(fig_box, use_container_width=True)
    
    with col2:
        st.markdown("### 🎯 Radar Chart: Activity Profile Comparison")
        st.markdown("> **Insight:** Radar charts compare multiple metrics simultaneously - see how different sports create unique physiological profiles.")
        
        radar_data = workout_df.groupby('activity_type').agg({
            'activity_strain': 'mean',
            'avg_heart_rate': 'mean',
            'activity_duration_min': 'mean',
            'activity_calories': 'mean',
            'hr_zone_5_min': 'mean'
        }).reset_index()
        
        # Normalize for radar
        scaler = MinMaxScaler()
        radar_scaled = pd.DataFrame(
            scaler.fit_transform(radar_data.iloc[:, 1:]),
            columns=radar_data.columns[1:]
        )
        radar_scaled['activity_type'] = radar_data['activity_type']
        
        categories = ['Strain', 'Avg HR', 'Duration', 'Calories', 'Zone 5 Time']
        
        fig_radar = go.Figure()
        colors = px.colors.qualitative.Set2
        
        for i, activity in enumerate(radar_scaled['activity_type'].unique()[:6]):
            values = radar_scaled[radar_scaled['activity_type'] == activity].iloc[0, :-1].tolist()
            values += values[:1]  # Close the radar
            
            fig_radar.add_trace(go.Scatterpolar(
                r=values,
                theta=categories + [categories[0]],
                fill='toself',
                name=activity,
                line_color=colors[i % len(colors)]
            ))
        
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
            template='plotly_dark',
            title='Activity Type Performance Profiles',
            height=450
        )
        st.plotly_chart(fig_radar, use_container_width=True)
    
    st.markdown("---")
    
    # Pareto Chart
    st.markdown("### 📊 Pareto Chart: Activity Calorie Contribution (80/20 Rule)")
    st.markdown("> **Insight:** Pareto analysis reveals which activities contribute most to total calorie burn - typically 20% of activities drive 80% of results.")
    
    pareto_data = workout_df.groupby('activity_type')['activity_calories'].sum().sort_values(ascending=False).reset_index()
    pareto_data['cumulative_pct'] = pareto_data['activity_calories'].cumsum() / pareto_data['activity_calories'].sum() * 100
    
    fig_pareto = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig_pareto.add_trace(
        go.Bar(x=pareto_data['activity_type'], y=pareto_data['activity_calories'],
               name='Calories', marker_color='#00D4AA'),
        secondary_y=False
    )
    
    fig_pareto.add_trace(
        go.Scatter(x=pareto_data['activity_type'], y=pareto_data['cumulative_pct'],
                   name='Cumulative %', line=dict(color='#FF6B6B', width=3),
                   mode='lines+markers'),
        secondary_y=True
    )
    
    # Add 80% line
    fig_pareto.add_hline(y=80, line_dash="dash", line_color="yellow", 
                         annotation_text="80% Line", secondary_y=True)
    
    fig_pareto.update_layout(
        title='Pareto Analysis: Activity Calorie Contribution',
        template='plotly_dark',
        height=500,
        xaxis_tickangle=-45
    )
    fig_pareto.update_yaxes(title_text="Total Calories", secondary_y=False)
    fig_pareto.update_yaxes(title_text="Cumulative %", secondary_y=True)
    st.plotly_chart(fig_pareto, use_container_width=True)
    
    st.markdown("---")
    
    # Growth-Share Matrix (BCG Matrix Style)
    st.markdown("### 📈 Growth-Share Matrix: Activity Performance Analysis")
    st.markdown("> **Insight:** BCG-style matrix categorizes activities by strain intensity (growth) and calorie efficiency (market share) to identify 'star' vs 'dog' activities.")
    
    growth_data = workout_df.groupby('activity_type').agg({
        'activity_strain': 'mean',
        'activity_calories': 'mean',
        'user_id': 'count'
    }).reset_index()
    growth_data.columns = ['Activity', 'Avg Strain', 'Avg Calories', 'Frequency']
    
    median_strain = growth_data['Avg Strain'].median()
    median_calories = growth_data['Avg Calories'].median()
    
    fig_bcg = px.scatter(
        growth_data, x='Avg Calories', y='Avg Strain',
        size='Frequency', color='Activity',
        title='Activity Growth-Share Matrix',
        labels={'Avg Calories': 'Calorie Efficiency (Share)', 'Avg Strain': 'Intensity (Growth)'}
    )
    
    fig_bcg.add_hline(y=median_strain, line_dash="dash", line_color="gray")
    fig_bcg.add_vline(x=median_calories, line_dash="dash", line_color="gray")
    
    # Add quadrant labels
    fig_bcg.add_annotation(x=growth_data['Avg Calories'].max() * 0.9, y=growth_data['Avg Strain'].max() * 0.95,
                           text="⭐ Stars", showarrow=False, font=dict(size=14, color='gold'))
    fig_bcg.add_annotation(x=growth_data['Avg Calories'].min() * 1.1, y=growth_data['Avg Strain'].max() * 0.95,
                           text="❓ Question Marks", showarrow=False, font=dict(size=14, color='orange'))
    fig_bcg.add_annotation(x=growth_data['Avg Calories'].max() * 0.9, y=growth_data['Avg Strain'].min() * 1.1,
                           text="🐄 Cash Cows", showarrow=False, font=dict(size=14, color='green'))
    fig_bcg.add_annotation(x=growth_data['Avg Calories'].min() * 1.1, y=growth_data['Avg Strain'].min() * 1.1,
                           text="🐕 Dogs", showarrow=False, font=dict(size=14, color='red'))
    
    fig_bcg.update_layout(template='plotly_dark', height=550)
    st.plotly_chart(fig_bcg, use_container_width=True)


# ============================================================================
# TAB 6: MACHINE LEARNING & CLUSTERING (was Tab 5)
# ============================================================================
with tab6:
    st.markdown("### 🧠 RFM Analysis with K-Means Clustering")
    st.markdown("> **Insight:** RFM (Recency, Frequency, Monetary) analysis segments users by workout behavior - identifying 'Champions' who train consistently with high intensity.")
    
    # Calculate RFM metrics per user
    max_date = filtered_df['date'].max()
    
    rfm = filtered_df.groupby('user_id').agg({
        'date': lambda x: (max_date - x.max()).days,  # Recency
        'workout_completed': 'sum',  # Frequency
        'calories_burned': 'sum'  # Monetary (Energy Investment)
    }).reset_index()
    rfm.columns = ['user_id', 'Recency', 'Frequency', 'Monetary']
    
    # Handle any infinite or NaN values
    rfm = rfm.replace([np.inf, -np.inf], np.nan).dropna()
    
    # Normalize for clustering
    scaler = StandardScaler()
    rfm_scaled = scaler.fit_transform(rfm[['Recency', 'Frequency', 'Monetary']])
    
    # K-Means Clustering
    n_clusters = st.slider("Select Number of Clusters", 2, 8, 4, key='rfm_clusters')
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    rfm['Cluster'] = kmeans.fit_predict(rfm_scaled)
    
    # Cluster naming based on characteristics
    cluster_means = rfm.groupby('Cluster')[['Recency', 'Frequency', 'Monetary']].mean()
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 3D Scatter for RFM
        fig_rfm_3d = px.scatter_3d(
            rfm, x='Recency', y='Frequency', z='Monetary',
            color='Cluster', opacity=0.7,
            title='RFM Segments - 3D Visualization',
            labels={'Recency': 'Recency (Days)', 'Frequency': 'Workout Count', 'Monetary': 'Total Calories'},
            color_continuous_scale='Viridis'
        )
        fig_rfm_3d.update_layout(template='plotly_dark', height=500)
        st.plotly_chart(fig_rfm_3d, use_container_width=True)
    
    with col2:
        # Cluster Summary
        st.markdown("#### 📊 Cluster Characteristics")
        cluster_summary = rfm.groupby('Cluster').agg({
            'user_id': 'count',
            'Recency': 'mean',
            'Frequency': 'mean',
            'Monetary': 'mean'
        }).round(2)
        cluster_summary.columns = ['Users', 'Avg Recency', 'Avg Frequency', 'Avg Calories']
        st.dataframe(cluster_summary.style.background_gradient(cmap='Greens'), use_container_width=True)
        
        # Cluster Distribution Pie
        fig_cluster_pie = px.pie(
            rfm, names='Cluster', title='User Distribution by Cluster',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_cluster_pie.update_layout(template='plotly_dark', height=300)
        st.plotly_chart(fig_cluster_pie, use_container_width=True)
    
    st.markdown("---")
    
    # Confusion Matrix Style - Recovery Prediction Accuracy
    st.markdown("### 🎯 Recovery Category Confusion Matrix")
    st.markdown("> **Insight:** Cross-tabulation shows how sleep quality categories align with recovery zones - revealing the predictive power of sleep on next-day recovery.")
    
    # Create sleep quality categories
    filtered_df['sleep_quality_cat'] = pd.cut(
        filtered_df['sleep_efficiency'], 
        bins=[0, 60, 75, 90, 100],
        labels=['Poor', 'Fair', 'Good', 'Excellent']
    )
    
    # Cross-tabulation (confusion matrix style)
    confusion = pd.crosstab(
        filtered_df['sleep_quality_cat'], 
        filtered_df['recovery_category'],
        normalize='index'
    ) * 100
    
    fig_confusion = px.imshow(
        confusion,
        labels=dict(x="Recovery Category", y="Sleep Quality", color="Percentage"),
        color_continuous_scale='RdYlGn',
        text_auto='.1f',
        title='Sleep Quality vs Recovery Category (% Distribution)'
    )
    fig_confusion.update_layout(template='plotly_dark', height=400)
    st.plotly_chart(fig_confusion, use_container_width=True)
    
    st.markdown("---")
    
    # Customer Retention Cohort Analysis
    st.markdown("### 📅 User Retention Cohort Map")
    st.markdown("> **Insight:** Cohort analysis tracks workout consistency over time - showing how many users maintain their training habits month over month.")
    
    # Create cohort data
    filtered_df['cohort_month'] = filtered_df.groupby('user_id')['date'].transform('min').dt.to_period('M')
    filtered_df['activity_month'] = filtered_df['date'].dt.to_period('M')
    filtered_df['cohort_index'] = (filtered_df['activity_month'].astype(int) - 
                                    filtered_df['cohort_month'].astype(int))
    
    cohort_data = filtered_df[filtered_df['workout_completed'] == 1].groupby(
        ['cohort_month', 'cohort_index']
    )['user_id'].nunique().reset_index()
    
    cohort_pivot = cohort_data.pivot(index='cohort_month', columns='cohort_index', values='user_id')
    
    # Calculate retention percentages
    cohort_size = cohort_pivot.iloc[:, 0]
    retention = cohort_pivot.divide(cohort_size, axis=0) * 100
    
    # Limit to first 12 months for readability
    retention = retention.iloc[:12, :12]
    
    # Convert Period index to string for JSON serialization
    retention.index = retention.index.astype(str)
    retention.columns = retention.columns.astype(str)
    
    fig_retention = px.imshow(
        retention,
        labels=dict(x="Months Since First Workout", y="Cohort", color="Retention %"),
        color_continuous_scale='Blues',
        title='User Retention Cohort Analysis'
    )
    fig_retention.update_layout(template='plotly_dark', height=450)
    st.plotly_chart(fig_retention, use_container_width=True)


# ============================================================================
# TAB 7: WHAT-IF ANALYSIS (was Tab 6)
# ============================================================================
with tab7:
    st.markdown("### 🔮 What-If Scenario Analysis")
    st.markdown("> **Insight:** Interactive what-if analysis lets you explore how changing key variables might impact fitness outcomes based on historical patterns.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 💤 Sleep Impact Simulator")
        target_sleep = st.slider("Target Sleep Hours", 4.0, 10.0, 7.0, 0.5)
        target_efficiency = st.slider("Target Sleep Efficiency %", 50, 100, 80)
        
        # Calculate expected outcomes based on correlations
        sleep_recovery_corr = filtered_df['sleep_hours'].corr(filtered_df['recovery_score'])
        eff_recovery_corr = filtered_df['sleep_efficiency'].corr(filtered_df['recovery_score'])
        
        avg_recovery = filtered_df['recovery_score'].mean()
        avg_sleep = filtered_df['sleep_hours'].mean()
        avg_eff = filtered_df['sleep_efficiency'].mean()
        
        predicted_recovery = avg_recovery + (target_sleep - avg_sleep) * sleep_recovery_corr * 5 + \
                            (target_efficiency - avg_eff) * eff_recovery_corr * 0.3
        predicted_recovery = np.clip(predicted_recovery, 0, 100)
        
        st.markdown(f"""
        <div class="insight-box">
            <h4>🎯 Predicted Recovery Score: {predicted_recovery:.1f}%</h4>
            <p>Based on {target_sleep}h sleep at {target_efficiency}% efficiency</p>
            <p>Change from baseline: <strong>{predicted_recovery - avg_recovery:+.1f}%</strong></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 🏋️ Training Load Simulator")
        target_strain = st.slider("Target Daily Strain", 0.0, 21.0, 12.0, 0.5)
        rest_days = st.slider("Rest Days per Week", 0, 4, 2)
        
        # Calculate impact
        strain_hrv_corr = filtered_df['day_strain'].corr(filtered_df['hrv'])
        avg_hrv = filtered_df['hrv'].mean()
        avg_strain = filtered_df['day_strain'].mean()
        
        weekly_strain = target_strain * (7 - rest_days)
        predicted_hrv = avg_hrv + (target_strain - avg_strain) * strain_hrv_corr * 2
        predicted_hrv = max(20, predicted_hrv)
        
        st.markdown(f"""
        <div class="insight-box">
            <h4>💓 Predicted Weekly HRV: {predicted_hrv:.0f}ms</h4>
            <p>Weekly strain load: {weekly_strain:.1f} (across {7-rest_days} training days)</p>
            <p>Change from baseline: <strong>{predicted_hrv - avg_hrv:+.1f}ms</strong></p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # What-If Visualization
    st.markdown("### 📊 Scenario Comparison Visualization")
    
    scenarios = pd.DataFrame({
        'Scenario': ['Current Baseline', 'Sleep Optimized', 'High Intensity', 'Recovery Focus'],
        'Recovery Score': [avg_recovery, min(95, avg_recovery + 15), max(35, avg_recovery - 12), min(90, avg_recovery + 8)],
        'HRV': [avg_hrv, avg_hrv + 10, avg_hrv - 8, avg_hrv + 12],
        'Daily Strain': [avg_strain, avg_strain, avg_strain + 5, avg_strain - 3],
        'Sleep Hours': [avg_sleep, 8.5, avg_sleep, avg_sleep + 0.5]
    })
    
    fig_scenario = go.Figure()
    
    for col in ['Recovery Score', 'HRV', 'Daily Strain']:
        fig_scenario.add_trace(go.Bar(
            name=col,
            x=scenarios['Scenario'],
            y=scenarios[col] / scenarios[col].max() * 100,  # Normalize
            text=scenarios[col].round(1),
            textposition='outside'
        ))
    
    fig_scenario.update_layout(
        title='What-If Scenario Comparison (Normalized)',
        template='plotly_dark',
        barmode='group',
        height=450
    )
    st.plotly_chart(fig_scenario, use_container_width=True)
    
    st.markdown("---")
    
    # Interactive Optimization
    st.markdown("### 🎮 Interactive Goal Optimizer")
    
    goal = st.selectbox("Select Your Optimization Goal", [
        "Maximize Recovery Score",
        "Maximize Calorie Burn",
        "Optimize HRV",
        "Balance Training & Recovery"
    ])
    
    if goal == "Maximize Recovery Score":
        top_recovery = filtered_df.nlargest(1000, 'recovery_score')
        recommendations = f"""
        **📋 Recommendations for Maximum Recovery:**
        - 🛏️ Target Sleep: {top_recovery['sleep_hours'].mean():.1f} hours
        - 💪 Optimal Strain: {top_recovery['day_strain'].mean():.1f}
        - ⏰ Fall Asleep in: {top_recovery['time_to_fall_asleep_min'].mean():.0f} minutes
        - 🌡️ Ideal Skin Temp Deviation: {top_recovery['skin_temp_deviation'].mean():.2f}°C
        """
    elif goal == "Maximize Calorie Burn":
        top_calories = workout_df.nlargest(1000, 'activity_calories')
        recommendations = f"""
        **📋 Recommendations for Maximum Calorie Burn:**
        - 🏃 Best Activity: {top_calories['activity_type'].mode().values[0]}
        - ⏱️ Optimal Duration: {top_calories['activity_duration_min'].mean():.0f} minutes
        - 💓 Target Avg HR: {top_calories['avg_heart_rate'].mean():.0f} bpm
        - 🔥 Expected Strain: {top_calories['activity_strain'].mean():.1f}
        """
    elif goal == "Optimize HRV":
        top_hrv = filtered_df.nlargest(1000, 'hrv')
        recommendations = f"""
        **📋 Recommendations for Optimal HRV:**
        - 😴 Deep Sleep Target: {top_hrv['deep_sleep_hours'].mean():.1f} hours
        - 🧘 REM Sleep Target: {top_hrv['rem_sleep_hours'].mean():.1f} hours
        - 🛏️ Sleep Efficiency: {top_hrv['sleep_efficiency'].mean():.0f}%
        - 💨 Respiratory Rate: {top_hrv['respiratory_rate'].mean():.1f} breaths/min
        """
    else:
        balanced = filtered_df[(filtered_df['recovery_score'] > 60) & (filtered_df['day_strain'] > 10)]
        recommendations = f"""
        **📋 Recommendations for Balanced Training:**
        - 🎯 Recovery Target: 60-75%
        - 💪 Strain Range: 10-16
        - 🛏️ Sleep: {balanced['sleep_hours'].mean():.1f} hours minimum
        - 📅 Workout Days: 4-5 per week
        """
    
    st.markdown(recommendations)


# ============================================================================
# TAB 8: ASSOCIATION MINING (was Tab 7)
# ============================================================================
with tab8:
    st.markdown("### 🛒 Association Rule Mining (Apriori Algorithm)")
    st.markdown("> **Insight:** Market basket analysis discovers hidden patterns - like which workout behaviors frequently occur together, similar to finding 'if you bought X, you'll like Y' patterns.")
    
    # Create transactional data for association mining
    st.markdown("#### 📊 Behavior Pattern Discovery")
    
    # Create binary features for association mining
    assoc_df = filtered_df.copy()
    
    # Discretize continuous variables into categories
    assoc_df['high_recovery'] = (assoc_df['recovery_score'] >= 66).astype(int)
    assoc_df['good_sleep'] = (assoc_df['sleep_hours'] >= 7).astype(int)
    assoc_df['high_strain'] = (assoc_df['day_strain'] >= 14).astype(int)
    assoc_df['high_hrv'] = (assoc_df['hrv'] >= assoc_df['hrv'].median()).astype(int)
    assoc_df['deep_sleep_good'] = (assoc_df['deep_sleep_hours'] >= 1.0).astype(int)
    assoc_df['morning_workout'] = (assoc_df['workout_time_of_day'] == 'Morning').astype(int)
    assoc_df['evening_workout'] = (assoc_df['workout_time_of_day'] == 'Evening').astype(int)
    
    # Calculate support and confidence manually for key patterns
    patterns = []
    
    # Pattern 1: Good Sleep → High Recovery
    support_good_sleep_high_recovery = ((assoc_df['good_sleep'] == 1) & (assoc_df['high_recovery'] == 1)).mean()
    confidence_sleep_recovery = ((assoc_df['good_sleep'] == 1) & (assoc_df['high_recovery'] == 1)).sum() / (assoc_df['good_sleep'] == 1).sum()
    patterns.append({'Rule': 'Good Sleep (≥7h) → High Recovery', 'Support': support_good_sleep_high_recovery, 'Confidence': confidence_sleep_recovery})
    
    # Pattern 2: Deep Sleep → High HRV
    support_deep_hrv = ((assoc_df['deep_sleep_good'] == 1) & (assoc_df['high_hrv'] == 1)).mean()
    confidence_deep_hrv = ((assoc_df['deep_sleep_good'] == 1) & (assoc_df['high_hrv'] == 1)).sum() / (assoc_df['deep_sleep_good'] == 1).sum() if (assoc_df['deep_sleep_good'] == 1).sum() > 0 else 0
    patterns.append({'Rule': 'Deep Sleep (≥1h) → High HRV', 'Support': support_deep_hrv, 'Confidence': confidence_deep_hrv})
    
    # Pattern 3: Morning Workout → High Strain
    if (assoc_df['morning_workout'] == 1).sum() > 0:
        support_morning_strain = ((assoc_df['morning_workout'] == 1) & (assoc_df['high_strain'] == 1)).mean()
        confidence_morning_strain = ((assoc_df['morning_workout'] == 1) & (assoc_df['high_strain'] == 1)).sum() / (assoc_df['morning_workout'] == 1).sum()
        patterns.append({'Rule': 'Morning Workout → High Strain', 'Support': support_morning_strain, 'Confidence': confidence_morning_strain})
    
    # Pattern 4: High Recovery + Good Sleep → Workout Completed
    cond = (assoc_df['high_recovery'] == 1) & (assoc_df['good_sleep'] == 1)
    if cond.sum() > 0:
        support_combo = (cond & (assoc_df['workout_completed'] == 1)).mean()
        confidence_combo = (cond & (assoc_df['workout_completed'] == 1)).sum() / cond.sum()
        patterns.append({'Rule': 'High Recovery + Good Sleep → Workout', 'Support': support_combo, 'Confidence': confidence_combo})
    
    # Pattern 5: High Strain Day → Low Recovery Next (simulated correlation)
    support_strain_low = ((assoc_df['high_strain'] == 1) & (assoc_df['high_recovery'] == 0)).mean()
    confidence_strain_low = ((assoc_df['high_strain'] == 1) & (assoc_df['high_recovery'] == 0)).sum() / (assoc_df['high_strain'] == 1).sum() if (assoc_df['high_strain'] == 1).sum() > 0 else 0
    patterns.append({'Rule': 'High Strain → Moderate/Low Recovery', 'Support': support_strain_low, 'Confidence': confidence_strain_low})
    
    patterns_df = pd.DataFrame(patterns)
    patterns_df['Lift'] = patterns_df['Confidence'] / patterns_df['Support'].mean()  # Simplified lift
    patterns_df = patterns_df.sort_values('Confidence', ascending=False)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📋 Discovered Association Rules")
        st.dataframe(
            patterns_df.style.format({
                'Support': '{:.2%}',
                'Confidence': '{:.2%}',
                'Lift': '{:.2f}'
            }).background_gradient(subset=['Confidence'], cmap='Greens'),
            use_container_width=True,
            height=300
        )
    
    with col2:
        # Visualize rules
        fig_rules = px.bar(
            patterns_df, x='Confidence', y='Rule',
            orientation='h', color='Support',
            color_continuous_scale='Emrld',
            title='Association Rule Confidence',
            text=patterns_df['Confidence'].apply(lambda x: f'{x:.1%}')
        )
        fig_rules.update_layout(template='plotly_dark', height=300)
        st.plotly_chart(fig_rules, use_container_width=True)
    
    st.markdown("---")
    
    # Activity Co-occurrence Matrix
    st.markdown("### 🔗 Activity Co-occurrence Analysis")
    st.markdown("> **Insight:** Shows which activities users commonly combine in their weekly routines - useful for designing balanced training programs.")
    
    # Create weekly activity profiles
    weekly_activities = workout_df.groupby(['user_id', 'week'])['activity_type'].apply(list).reset_index()
    
    # Count co-occurrences
    activities = workout_df['activity_type'].unique()
    cooccurrence = pd.DataFrame(0, index=activities, columns=activities, dtype=float)
    
    for _, row in weekly_activities.iterrows():
        activity_list = list(set(row['activity_type']))
        for i, act1 in enumerate(activity_list):
            for act2 in activity_list[i:]:
                cooccurrence.loc[act1, act2] += 1
                if act1 != act2:
                    cooccurrence.loc[act2, act1] += 1
    
    # Normalize
    cooccurrence_norm = cooccurrence / cooccurrence.max().max()
    
    fig_cooccur = px.imshow(
        cooccurrence_norm,
        labels=dict(x="Activity", y="Activity", color="Co-occurrence"),
        color_continuous_scale='Blues',
        title='Weekly Activity Co-occurrence Matrix'
    )
    fig_cooccur.update_layout(template='plotly_dark', height=500)
    st.plotly_chart(fig_cooccur, use_container_width=True)
    
    st.markdown("---")
    
    # Network Graph of Relationships
    st.markdown("### 🕸️ Metric Correlation Network")
    st.markdown("> **Insight:** Network visualization shows which fitness metrics are strongly correlated, helping identify key drivers of performance.")
    
    # Calculate correlations
    corr_cols = ['recovery_score', 'day_strain', 'sleep_hours', 'sleep_efficiency', 
                 'hrv', 'resting_heart_rate', 'deep_sleep_hours', 'rem_sleep_hours', 'calories_burned']
    corr_matrix = filtered_df[corr_cols].corr()
    
    # Create network edges (only strong correlations)
    edges = []
    for i, col1 in enumerate(corr_cols):
        for j, col2 in enumerate(corr_cols):
            if i < j and abs(corr_matrix.loc[col1, col2]) > 0.3:
                edges.append({
                    'source': col1,
                    'target': col2,
                    'weight': abs(corr_matrix.loc[col1, col2]),
                    'correlation': corr_matrix.loc[col1, col2]
                })
    
    edges_df = pd.DataFrame(edges).sort_values('weight', ascending=False)
    
    # Display as interactive table
    st.dataframe(
        edges_df.style.format({
            'weight': '{:.3f}',
            'correlation': '{:.3f}'
        }).background_gradient(subset=['correlation'], cmap='RdYlGn', vmin=-1, vmax=1),
        use_container_width=True
    )


# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2rem; color: #888;'>
    <h4>🏋️ WHOOP Fitness Analytics Dashboard</h4>
    <p>Built with Streamlit, Plotly, and Scikit-learn</p>
    <p>University Final Project - Data Visualization</p>
    <p style='font-size: 0.8rem; margin-top: 1rem;'>
        📊 {total_records:,} Records | 👥 {total_users:,} Users | 📅 {date_range}
    </p>
</div>
""".format(
    total_records=len(filtered_df),
    total_users=filtered_df['user_id'].nunique(),
    date_range=f"{filtered_df['date'].min().strftime('%Y-%m-%d')} to {filtered_df['date'].max().strftime('%Y-%m-%d')}"
), unsafe_allow_html=True)
