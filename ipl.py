import streamlit as st
import pickle
from sklearn import pipeline
import pandas as pd

# Enhanced IPL-themed styling with better contrast
page_styling = '''
<style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@600;700&family=Exo+2:wght@400;600;800&display=swap');
    
    /* Main background */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(180deg, #0a0e27 0%, #1a1f3a 50%, #0f1419 100%);
    }
    
    /* Header styling */
    [data-testid="stHeader"] {
        background-color: rgba(0,0,0,0);
    }
    
    /* Main title */
    .main-title {
        text-align: center;
        font-size: 4rem;
        font-weight: 800;
        color: #00d9ff;
        text-shadow: 0 0 30px rgba(0, 217, 255, 0.6), 0 0 60px rgba(0, 217, 255, 0.4);
        margin-bottom: 0.5rem;
        font-family: 'Rajdhani', sans-serif;
        letter-spacing: 3px;
    }
    
    .subtitle {
        text-align: center;
        color: #ffd93d;
        font-size: 1.4rem;
        margin-bottom: 3rem;
        font-weight: 600;
        font-family: 'Exo 2', sans-serif;
    }
    
    /* Section headers */
    .section-header {
        color: #00d9ff;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 2rem 0 1rem 0;
        font-family: 'Rajdhani', sans-serif;
        border-bottom: 3px solid #00d9ff;
        padding-bottom: 0.5rem;
    }
    
    /* Labels - HIGH CONTRAST */
    label {
        color: #ffd93d !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        font-family: 'Exo 2', sans-serif !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.5);
    }
    
    /* Input fields - DARK BACKGROUND WITH LIGHT TEXT */
    input, select {
        background-color: #1a1f3a !important;
        color: #ffffff !important;
        border: 2px solid #00d9ff !important;
        border-radius: 8px !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        padding: 0.5rem !important;
    }
    
    input:focus, select:focus {
        border-color: #ffd93d !important;
        box-shadow: 0 0 15px rgba(255, 217, 61, 0.4) !important;
    }
    
    /* Dropdown arrow visibility */
    select option {
        background-color: #1a1f3a !important;
        color: #ffffff !important;
    }
    
    /* Number input buttons */
    input[type="number"]::-webkit-inner-spin-button,
    input[type="number"]::-webkit-outer-spin-button {
        opacity: 1;
    }
    
    /* Button styling */
    .stButton button {
        background: linear-gradient(135deg, #ff006e 0%, #8338ec 50%, #3a86ff 100%);
        color: #ffffff;
        font-size: 1.5rem;
        font-weight: 800;
        padding: 1rem 3rem;
        border-radius: 50px;
        border: none;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 10px 40px rgba(255, 0, 110, 0.5);
        text-transform: uppercase;
        letter-spacing: 3px;
        font-family: 'Rajdhani', sans-serif;
        margin-top: 2rem;
    }
    
    .stButton button:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 50px rgba(255, 0, 110, 0.7);
    }
    
    /* Table styling */
    .stDataFrame {
        background-color: rgba(26, 31, 58, 0.8);
        border-radius: 15px;
        padding: 20px;
        border: 2px solid #00d9ff;
    }
    
    /* DataFrame text */
    [data-testid="stDataFrame"] {
        color: #ffffff !important;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #00d9ff !important;
        font-family: 'Rajdhani', sans-serif !important;
    }
    
    /* Divider */
    hr {
        border: none;
        height: 3px;
        background: linear-gradient(90deg, transparent, #00d9ff, #ffd93d, #ff006e, transparent);
        margin: 2rem 0;
    }
    
    /* Column containers */
    [data-testid="column"] {
        background-color: rgba(26, 31, 58, 0.4);
        border-radius: 12px;
        padding: 1rem;
        border: 1px solid rgba(0, 217, 255, 0.3);
    }
</style>
'''

st.markdown(page_styling, unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-title">WINHEARTSІPL</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Live Match Win Probability Engine</p>', unsafe_allow_html=True)

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

st.markdown('<p class="section-header">TEAM SELECTION</p>', unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    batting_team = st.selectbox('Batting Team', sorted(teams), key='batting')
with c2:
    bowling_team = st.selectbox('Bowling Team', sorted(teams), key='bowling')

selected_city = st.selectbox('Host City', sorted(cities), key='city')

st.markdown("---")
st.markdown('<p class="section-header">MATCH SITUATION</p>', unsafe_allow_html=True)

target = st.number_input('Target Score', min_value=0, step=1, key='target')

c3, c4, c5 = st.columns(3)
with c3:
    score = st.number_input('Current Score', min_value=0, step=1, key='score')
with c4:
    overs = st.number_input('Overs Completed', min_value=0.0, max_value=19.0, step=0.1, key='overs')
with c5:
    wickets = st.number_input('Wickets Lost', min_value=0, max_value=10, step=1, key='wickets')

st.markdown("---")

if st.button('CALCULATE WIN PROBABILITY'):
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
    
    st.markdown('<p class="section-header">MATCH ANALYSIS</p>', unsafe_allow_html=True)
    st.dataframe(input_df, use_container_width=True)
    
    result = pipe.predict_proba(input_df)
    loss = result[0][0]
    win = result[0][1]
    
    st.markdown("---")
    st.markdown('<p class="section-header">WIN PROBABILITY</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #00d9ff 0%, #0096c7 100%); 
                    padding: 2rem; border-radius: 15px; 
                    text-align: center; box-shadow: 0 10px 40px rgba(0, 217, 255, 0.4);
                    border: 3px solid #00d9ff;">
            <h3 style="color: #0a0e27; margin: 0; font-weight: 800; font-size: 1.3rem;">
                {batting_team}
            </h3>
            <h1 style="color: #ffffff; font-size: 4rem; margin: 15px 0; font-weight: 900; text-shadow: 0 4px 8px rgba(0,0,0,0.3);">
                {round(win * 100)}%
            </h1>
            <p style="color: #0a0e27; margin: 0; font-weight: 700; font-size: 1rem;">WIN CHANCE</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #ff006e 0%, #d00060 100%); 
                    padding: 2rem; border-radius: 15px; 
                    text-align: center; box-shadow: 0 10px 40px rgba(255, 0, 110, 0.4);
                    border: 3px solid #ff006e;">
            <h3 style="color: #ffffff; margin: 0; font-weight: 800; font-size: 1.3rem;">
                {bowling_team}
            </h3>
            <h1 style="color: #ffffff; font-size: 4rem; margin: 15px 0; font-weight: 900; text-shadow: 0 4px 8px rgba(0,0,0,0.3);">
                {round(loss * 100)}%
            </h1>
            <p style="color: #ffffff; margin: 0; font-weight: 700; font-size: 1rem;">WIN CHANCE</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p class="section-header">PROBABILITY METER</p>', unsafe_allow_html=True)
    st.progress(win)
