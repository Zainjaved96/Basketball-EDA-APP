import streamlit as st
import pandas as pd
import base64
from math import pi

st.title("BASKETBALL EDA APP")
st.markdown("""
- Find the basketball stats from different year
- The  Source of all this data is [Basketball Reference](https://www.basketball-reference.com/)
""")

st.sidebar.header("Side Bar")
year_selected = st.sidebar.selectbox("SELECT YEAR", list(reversed(range(1950, 2021))))


def load_data(year):
    url = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_per_game.html"
    html = pd.read_html(url, header=0)
    df = html[0]
    raw = df.drop(df[df.Age == 'Age'].index)  # Deletes repeating headers in content
    raw = raw.fillna(0)
    playerstats = raw.drop(['Rk'], axis=1)
    return playerstats


st.markdown(
    f'''
        <style>
            .sidebar .sidebar-content {{
                width: 500px;
            }}
        </style>
    ''',
    unsafe_allow_html=True
)
playerstats = load_data(year_selected)

unique_teams = sorted(playerstats.Tm.unique())
selected_teams = st.sidebar.multiselect("Teams", unique_teams, unique_teams)

# Sidebar - Position selection
unique_pos = ['C', 'PF', 'SF', 'PG', 'SG']
selected_pos = st.sidebar.multiselect('Position', unique_pos, unique_pos)

# Filtering data
df_selected_team = playerstats[(playerstats.Tm.isin(selected_teams)) & (playerstats.Pos.isin(selected_pos))]

# Load Data
st.header('Display Player Stats of Selected Team(s)')
st.write(
    'Data Dimension: ' + str(df_selected_team.shape[0]) + ' rows and ' + str(df_selected_team.shape[1]) + ' columns.')
test = df_selected_team.astype(str)
st.dataframe(test)


# Download NBA player stats data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href


st.markdown(filedownload(df_selected_team), unsafe_allow_html=True)
pi
