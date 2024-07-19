
import streamlit as st
import pickle
from sklearn import pipeline
import pandas as pd
page_bg_color = '''
<style>
[data-testid="stAppViewContainer"] {
background-color: #ADD8E6; /* Light Blue */
}
</style>
'''

# Apply the CSS to the Streamlit app
st.markdown(page_bg_color, unsafe_allow_html=True)


teams=['Royal Challengers Bangalore', 'Mumbai Indians',
       'Kolkata Knight Riders',
        'Chennai Super Kings',
       'Sunrisers Hyderabad',
       'Gujarat Lions',
       'Rising Pune Supergiant', 'Delhi Capitals',
       'Lucknow Super Giants']

cities=['Bangalore', 'Mumbai', 'Kolkata', 'Hyderabad', 'Chennai', 'Delhi',
       'Cape Town', 'Port Elizabeth', 'Durban', 'Centurion',
       'East London', 'Johannesburg', 'Cuttack', 'Nagpur',
       'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi',
       'Rajkot', 'Kanpur', 'Bengaluru', 'Ahmedabad', 'Dubai', 'Sharjah',
       'Navi Mumbai', 'Lucknow']
pipe=pickle.load(open('pipe2.pkl','rb'))

st.title('WinHeartsIPL: IPL Win Predictor')
c1,c2= st.columns(2)
with c1:
       batting_team= st.selectbox('select the batting team',sorted(teams))
with c2:
       bowling_team = st.selectbox('select the bowling team', sorted(teams))
selected_city=st.selectbox('select the host city',sorted(cities))

target=st.number_input('target')

c3,c4,c5=st.columns(3)
with c3:
       score=st.number_input('score')
with c4:
       overs=st.number_input('overs completed(1-19)')
with c5:
       wickets=st.number_input('wickets out(0-10)')

if st.button('predict probability'):
   runs_left= target-score
   balls_left=120-(overs*6)
   wickets=10-wickets
   crr=score/overs
   rrr=(runs_left*6)/balls_left

   input_df = pd.DataFrame({
       'batting_team': [batting_team],
       'bowling_team': [bowling_team],
       'city': [selected_city],
       'runs_left': [runs_left],
       'balls_left': [balls_left],
       'wickets': [wickets],
       'total_runs_x': [target],
       'crr': [crr],
       'rrr': [rrr]
   })
   st.table(input_df)
   result=pipe.predict_proba(input_df)
   loss = result[0][0]
   win = result[0][1]
   st.header(batting_team + "-" + str(round(win* 100)) + "%")
   st.header(bowling_team + "-" + str(round(loss* 100)) + "%")


