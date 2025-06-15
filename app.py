import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
@st.cache_data
def load_data():
    World_cup = pd.read_csv("World_cup_2023.csv")
    results = pd.read_csv("results.csv")
    return World_cup, results

World_cup, results = load_data()

# Sidebar for navigation
st.sidebar.title("Navigation")
options = st.sidebar.radio("Go to", ["Home", "World Cup Data", "Team Analysis"])

# Apply custom CSS for dark theme
st.markdown("""
    <style>
        body {
            background-color: #121212;
            color: #e0e0e0;
        }
        .sidebar .sidebar-content {
            background-color: #1e1e1e;
        }
        .main .block-container {
            background-color: #121212;
        }
        .header {
            font-size: 3em;
            color: #f57c00;
            text-align: center;
            margin-bottom: 20px;
        }
        .subheader {
            font-size: 1.5em;
            color: #03a9f4;
        }
        .description {
            font-size: 1.2em;
            color: #e0e0e0;
            margin-top: 20px;
        }
        .css-1v3fvcr .css-1y4p8pa {
            color: #e0e0e0;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="header">🏆 Welcome to the World Cup 2023 Data Analysis App!</div>', unsafe_allow_html=True)

# Home Page
if options == "Home":
    st.image("image.jpg", use_column_width=True)  # Display the image in a larger size
    st.markdown("""
        <div class="description">
            This app provides a detailed analysis of the World Cup 2023 data, including team performance, match results, and more.
            Use the navigation menu to explore different sections of the app.
        </div>
    """, unsafe_allow_html=True)

# Display data
if options == "World Cup Data":
    st.header('World Cup 2023 Data')
    
    if st.checkbox('Show World Cup data'):
        st.subheader('World Cup 2023 Data')
        st.write(World_cup)
    
    if st.checkbox('Show Results data'):
        st.subheader('Results Data')
        st.write(results)

# Plotting function
def plot_bar(data, x, y, title):
    sns.set(rc={'figure.figsize':(20, 5)})
    plt.figure(figsize=(20, 5))
    sns.barplot(x=x, y=y, data=data)
    plt.title(title)
    st.pyplot(plt)

# Visualize data
if options == "World Cup Data":
    with st.expander("Visualize Data"):
        if st.checkbox('Show Team Titles'):
            plot_bar(World_cup, 'Team_name', 'Titles', 'Team Titles')

        if st.checkbox('Show Win Percentage ODI'):
            plot_bar(World_cup, 'Team_name', 'Win_percentage_ODI', 'Win Percentage ODI')

        if st.checkbox('Show WC Matches Won'):
            plot_bar(World_cup, 'Team_name', 'WC_match_won', 'World Cup Matches Won')

        if st.checkbox('Show Ratings'):
            plot_bar(World_cup, 'Team_name', 'Rating', 'Team Ratings')

# Drop 'Match abandoned' and 'No result' from results
results.drop(results[(results['Winner'] == 'Match abandoned') | (results['Winner'] == 'No result')].index, inplace=True)

# Team-specific analysis
if options == "Team Analysis":
    st.header("Team Analysis")
    team = st.selectbox('Select a team for analysis', ['India', 'Australia', 'Pakistan', 'New Zealand', 'England'])

    if team:
        team_df = results[(results['Team_1'] == team) | (results['Team_2'] == team)]
        st.subheader(f'{team} Match Results')
        st.write(team_df)
        
        # Filter wins
        team_wins = team_df[team_df['Winner'] == team]
        
        with st.expander(f"{team} Match Statistics"):
            st.write(f"Number of matches played: {team_df.shape[0]}")
            st.write(f"Number of matches won: {team_wins.shape[0]}")
            st.write(f"Winning percentage: {team_wins.shape[0] / team_df.shape[0] * 100:.2f}%")
