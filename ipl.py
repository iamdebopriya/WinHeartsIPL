import streamlit as st
import pickle
from sklearn import pipeline
import pandas as pd

# Enhanced IPL-themed styling
page_styling = '''
<style>
    /* Main background with gradient */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    
    /* Header styling */
    [data-testid="stHeader"] {
        background-color: rgba(0,0,0,0);
    }
    
    /* Custom title styling */
    .main-title {
        text-align: center;
        font-size: 3.5rem;
        font-weight: 900;
        background: linear-gradient(120deg, #ff6b6b, #4ecdc4, #ffe66d, #ff6b6b);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 3s linear infinite;
        text-shadow: 0 0 20px rgba(255,107,107,0.5);
        margin-bottom: 0.5rem;
        font-family: 'Arial Black', sans-serif;
    }
    
    @keyframes shine {
        to {
            background-position: 200% center;
        }
    }
    
    .subtitle {
        text-align: center;
        color: #4ecdc4;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        font-weight: 600;
    }
    
    /* Card-like containers */
    .stSelectbox, .stNumberInput {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 10px;
        backdrop-filter: blur(10px);
    }
    
    /* Labels */
    label {
        color: #ffe66d !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    
    /* Input fields */
    input, select {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: 2px solid #4ecdc4 !important;
        border-radius: 8px !important;
    }
    
    /* Button styling */
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-size: 1.3rem;
        font-weight: bold;
        padding: 0.8rem 2rem;
        border-radius: 50px;
        border: none;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    .stButton button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.6);
    }
    
    /* Table styling */
    .stDataFrame {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 15px;
        backdrop-filter: blur(10px);
    }
    
    /* Header results */
    h1, h2, h3 {
        color: white !important;
    }
    
    /* Custom result cards */
    .result-card {
        background: linear-gradient(135deg, rgba(255,107,107,0.2), rgba(255,107,107,0.05));
        border-left: 5px solid #ff6b6b;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
    }
    
    .result-card h2 {
        margin: 0;
        font-size: 2rem;
        font-weight: 900;
    }
    
    /* Section divider */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #4ecdc4, transparent);
        margin: 2rem 0;
    }
    
    /* Cricket ball emoji animation */
    .cricket-emoji {
        text-align: center;
        font-size: 3rem;
        animation: bounce 2s infinite;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-20px); }
    }
</style>
'''

st.markdown(page_styling, unsafe_allow_html=True)

# Title with IPL vibe
st.markdown('<h1 class="main-title">WinHeartsIPL</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">IPL Win Probability Predictor</p>', unsafe_allow_html=True)

teams = ['Royal Challengers Bangalore', 'Mumbai Indians',
         'Kolkata Knight Riders', 'Chennai Super Kings',
         'Sunrisers Hyderabad', 'Gujarat Lions',
         'Rising Pune Supergiant', 'Delhi Capitals',
         'Lucknow Super Giants']

cities = ['Bangalore', 'Mumbai', 'Kolkata', 'Hyderabad', 'Chennai', 'Delhi',
          'Cape Town', 'Port Elizabeth', 'Durban', 'Centurion',
          'East London', 'Johannesburg', 'Cuttack', 'Nagpur',
          'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi',
          'Rajkot', 'Kanpur', 'Bengaluru', 'Ahmedabad', 'Dubai', 'Sharjah',
          'Navi Mumbai', 'Lucknow']

pipe = pickle.load(open('pipe2.pkl', 'rb'))

st.markdown("---")
st.markdown("### 🎯 Match Setup")

c1, c2 = st.columns(2)
with c1:
    batting_team = st.selectbox('Select the batting team', sorted(teams))
with c2:
    bowling_team = st.selectbox('Select the bowling team', sorted(teams))

selected_city = st.selectbox('Select the host city', sorted(cities))

st.markdown("---")
st.markdown("### 📊 Match Stats")

target = st.number_input('Target', min_value=0, step=1)

c3, c4, c5 = st.columns(3)
with c3:
    score = st.number_input('Score', min_value=0, step=1)
with c4:
    overs = st.number_input('Overs completed (1-19)', min_value=0.0, max_value=19.0, step=0.1)
with c5:
    wickets = st.number_input('Wickets out (0-10)', min_value=0, max_value=10, step=1)

st.markdown("---")

if st.button('🔮 PREDICT PROBABILITY'):
    runs_left = target - score
    balls_left = 120 - (overs * 6)
    wickets_remaining = 10 - wickets
    crr = score / overs if overs > 0 else 0
    rrr = (runs_left * 6) / balls_left if balls_left > 0 else 0
    
    input_df = pd.DataFrame({
        'batting_team': [batting_team],
        'bowling_team': [bowling_team],
        'city': [selected_city],
        'runs_left': [runs_left],
        'balls_left': [balls_left],
        'wickets': [wickets_remaining],
        'total_runs_x': [target],
        'crr': [crr],
        'rrr': [rrr]
    })
    
    st.markdown("### 📋 Match Analysis")
    st.dataframe(input_df, use_container_width=True)
    
    result = pipe.predict_proba(input_df)
    loss = result[0][0]
    win = result[0][1]
    
    st.markdown("---")
    st.markdown("### 🏆 Win Probability")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(78,205,196,0.3), rgba(78,205,196,0.1)); 
                    border-left: 5px solid #4ecdc4; padding: 1.5rem; border-radius: 10px; 
                    text-align: center; backdrop-filter: blur(10px);">
            <h3 style="color: #4ecdc4; margin: 0;">🎯 {batting_team}</h3>
            <h1 style="color: #ffe66d; font-size: 3rem; margin: 10px 0; font-weight: 900;">
                {round(win * 100)}%
            </h1>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(255,107,107,0.3), rgba(255,107,107,0.1)); 
                    border-left: 5px solid #ff6b6b; padding: 1.5rem; border-radius: 10px; 
                    text-align: center; backdrop-filter: blur(10px);">
            <h3 style="color: #ff6b6b; margin: 0;">🛡️ {bowling_team}</h3>
            <h1 style="color: #ffe66d; font-size: 3rem; margin: 10px 0; font-weight: 900;">
                {round(loss * 100)}%
            </h1>
        </div>
        """, unsafe_allow_html=True)
    
    # Progress bar for visual representation
    st.markdown("### 📈 Probability Distribution")
    st.progress(win)
