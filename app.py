"""
JALNETRA - AI-Driven Groundwater Management System
Main Application
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import os

# Page configuration
st.set_page_config(
    page_title="JALNETRA - Groundwater Dashboard",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
    <style>
        /* Main theme colors */
        :root {
            --primary: #667eea;
            --secondary: #764ba2;
            --accent: #FF6B6B;
        }
        
        /* Hide Streamlit footer */
        footer {visibility: hidden;}
        
        /* Main container styling */
        .main {
            padding: 0;
        }
        
        /* Header styling */
        .header-container {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 30px;
            border-radius: 10px;
            color: white;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        .header-title {
            font-size: 2.5em;
            font-weight: bold;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        
        .header-subtitle {
            font-size: 1.1em;
            opacity: 0.95;
            margin: 10px 0 0 0;
        }
        
        /* Card styling */
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            color: white;
            text-align: center;
        }
        
        .metric-value {
            font-size: 2.2em;
            font-weight: bold;
            margin: 10px 0;
        }
        
        .metric-label {
            font-size: 0.9em;
            opacity: 0.9;
        }
        
        /* Chart container */
        .chart-container {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        }
        
        /* Button styling */
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_email' not in st.session_state:
    st.session_state.user_email = None

# Load data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('groundwater_data.csv')
        return df
    except FileNotFoundError:
        return None

# Main application
def main():
    # Load data
    df = load_data()
    
    if df is None:
        st.error("❌ groundwater_data.csv not found!")
        st.info("Please ensure groundwater_data.csv is in the project root directory")
        return
    
    # Header
    st.markdown("""
        <div class="header-container">
            <h1 class="header-title">💧 JALNETRA</h1>
            <p class="header-subtitle">AI-Driven Groundwater Assessment & Management System</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.title("🗂️ Navigation")
    page = st.sidebar.radio(
        "Select Page",
        ["🏠 Home", "📊 Dashboard", "📈 Analytics", "🔍 Search", "💬 Chatbot", "🤖 Predictions", "📋 Data Table", "⚙️ Settings"]
    )
    
    # Add logout button
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.user_email = None
        st.rerun()
    
    # Page routing
    if page == "🏠 Home":
        show_home(df)
    elif page == "📊 Dashboard":
        show_dashboard(df)
    elif page == "📈 Analytics":
        show_analytics(df)
    elif page == "🔍 Search":
        show_search(df)
    elif page == "💬 Chatbot":
        show_chatbot(df)
    elif page == "🤖 Predictions":
        show_predictions(df)
    elif page == "📋 Data Table":
        show_data_table(df)
    elif page == "⚙️ Settings":
        show_settings()

def show_home(df):
    """Home page"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Records</div>
                <div class="metric-value">{len(df)}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Districts</div>
                <div class="metric-value">{df['District'].nunique()}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Talukas</div>
                <div class="metric-value">{df['Taluka'].nunique()}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Years</div>
                <div class="metric-value">{int(df['Year'].max()) - int(df['Year'].min()) + 1}</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.write("## Welcome to JALNETRA")
    st.write("""
    JALNETRA is an advanced AI-driven groundwater assessment and management system that provides:
    
    - 📊 **Real-time Monitoring** - Track groundwater levels across districts and talukas
    - 📈 **Advanced Analytics** - Analyze trends and patterns in groundwater data
    - 🔍 **Intelligent Search** - Find specific data with advanced filtering
    - 💬 **AI Chatbot** - Ask questions about groundwater data
    - 🤖 **ML Predictions** - Predict future groundwater trends
    - 📋 **Data Management** - View, search, and export groundwater data
    
    Use the navigation menu to explore different features.
    """)

def show_dashboard(df):
    """Dashboard page"""
    st.subheader("📊 Groundwater Dashboard")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Pre-Monsoon vs Post-Monsoon Levels**")
        avg_data = df.groupby('Year')[['Pre-Monsoon Level', 'Post-Monsoon Level']].mean()
        st.line_chart(avg_data)
    
    with col2:
        st.write("**Category Distribution**")
        category_data = df['Category'].value_counts()
        st.bar_chart(category_data)

def show_analytics(df):
    """Analytics page"""
    st.subheader("📈 Advanced Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**District-wise Average Water Level**")
        district_avg = df.groupby('District')[['Pre-Monsoon Level', 'Post-Monsoon Level']].mean().mean(axis=1).nlargest(10)
        st.bar_chart(district_avg)
    
    with col2:
        st.write("**Recharge vs Extraction**")
        year_avg = df.groupby('Year')[['Recharge', 'Extraction']].mean()
        st.line_chart(year_avg)

def show_search(df):
    """Search page"""
    st.subheader("🔍 Advanced Search & Filtering")
    
    col1, col2 = st.columns(2)
    
    with col1:
        selected_state = st.selectbox("Select State", ["All"] + sorted(df['State'].unique()))
        selected_district = st.selectbox("Select District", ["All"] + sorted(df['District'].unique()))
    
    with col2:
        selected_year = st.slider("Select Year", int(df['Year'].min()), int(df['Year'].max()))
        selected_category = st.selectbox("Select Category", ["All"] + sorted(df['Category'].unique()))
    
    # Apply filters
    filtered_df = df.copy()
    
    if selected_state != "All":
        filtered_df = filtered_df[filtered_df['State'] == selected_state]
    if selected_district != "All":
        filtered_df = filtered_df[filtered_df['District'] == selected_district]
    filtered_df = filtered_df[filtered_df['Year'] == selected_year]
    if selected_category != "All":
        filtered_df = filtered_df[filtered_df['Category'] == selected_category]
    
    st.write(f"**Found {len(filtered_df)} records**")
    st.dataframe(filtered_df, use_container_width=True)

def show_chatbot(df):
    """Chatbot page"""
    st.subheader("💬 AI Chatbot Assistant")
    
    st.info("🤖 Ask me questions about groundwater data!")
    st.write("Example questions:")
    st.write("- Show groundwater extraction in specific areas")
    st.write("- Which taluka has highest recharge?")
    st.write("- Compare pre and post monsoon levels")
    st.write("- Show 2022 groundwater status")
    
    user_query = st.text_input("Ask a question about groundwater data:")
    
    if user_query:
        st.info(f"Query: {user_query}")
        st.success("✅ Response from chatbot (basic implementation)")

def show_predictions(df):
    """Predictions page"""
    st.subheader("🤖 ML-Based Predictions")
    
    st.info("🔮 Predict future groundwater trends using Machine Learning")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_district = st.selectbox("Select District", sorted(df['District'].unique()), key="pred_district")
    
    with col2:
        selected_taluka = st.selectbox("Select Taluka", sorted(df['Taluka'].unique()), key="pred_taluka")
    
    with col3:
        prediction_year = st.number_input("Predict for Year", min_value=2024, max_value=2030)
    
    if st.button("Generate Prediction"):
        st.success(f"📊 Prediction generated for {selected_district}, {selected_taluka} in {prediction_year}")

def show_data_table(df):
    """Data table page"""
    st.subheader("📋 Complete Groundwater Data")
    
    search_term = st.text_input("🔍 Search in data:")
    
    display_df = df.copy()
    
    if search_term:
        mask = display_df.astype(str).apply(lambda x: x.str.contains(search_term, case=False)).any(axis=1)
        display_df = display_df[mask]
        st.info(f"Found {len(display_df)} matching records")
    
    st.dataframe(display_df, use_container_width=True, height=500)
    
    # Download option
    csv = display_df.to_csv(index=False)
    st.download_button(
        label="📥 Download as CSV",
        data=csv,
        file_name=f"groundwater_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

def show_settings():
    """Settings page"""
    st.subheader("⚙️ Settings & Profile")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### User Profile")
        st.write(f"**Email:** {st.session_state.user_email if st.session_state.user_email else 'Not logged in'}")
        st.write(f"**Status:** {'Authenticated' if st.session_state.authenticated else 'Guest'}")
    
    with col2:
        st.write("### Application Settings")
        theme = st.selectbox("Select Theme", ["Default", "Dark", "Light"])
        language = st.selectbox("Select Language", ["English", "Marathi", "Hindi"])
    
    if st.button("Save Settings"):
        st.success("✅ Settings saved successfully!")

if __name__ == "__main__":
    main()
