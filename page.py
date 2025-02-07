import streamlit as st
import mysql.connector
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Function to establish a database connection
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "Snvgv@6090"),
        database=os.getenv("DB_NAME", "sports_data")
    )

# Function to fetch data from MySQL
def fetch_data(query):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return pd.DataFrame(result)

# Load CSV data
def load_csv_data():
    competitors = pd.read_csv("D:/GUVI/GUVI-Prj01/Competitors_Table.csv")
    complex_details = pd.read_csv("D:/GUVI/GUVI-Prj01/complex_details.csv")
    venue_details = pd.read_csv("D:/GUVI/GUVI-Prj01/venue_details.csv")
    category_details = pd.read_csv("D:/GUVI/GUVI-Prj01/category_details.csv")
    competition_details = pd.read_csv("D:/GUVI/GUVI-Prj01/competition_details.csv")
    rankings = pd.read_csv("D:/GUVI/GUVI-Prj01/Competitor_Rankings_Table.csv")
    return competitors, complex_details, venue_details, category_details, competition_details, rankings

# Load CSV data
competitors, complex_details, venue_details, category_details, competition_details, rankings = load_csv_data()

# Sidebar Navigation
tag = st.sidebar.selectbox(
    '# **ExploreSports** 🎾',
    ['Home', 'Competitor Lookup', 'Leader Board', 'Conclusion']
)

if tag == 'Home':
    st.title("🎾 TENNIS COMPETITIONS EXPLORER 🎾")
    st.caption("## - Game Analytics: Unlocking Tennis Data with SportRadar")
    st.markdown("### **Welcome!** 🌟 Explore tennis competition data. 🎾✨")
    
    # Display Key Metrics
    st.subheader("Game Analytics: Key Metrics")
    st.metric("Overall Competitor Count", len(competitors))
    st.metric("Countries Represented", competitors['country'].nunique())
    
    # Show top 5 ranked competitors
    top_5_rank = rankings.nsmallest(5, 'rank')
    top_5_merged = top_5_rank.merge(competitors, on="competitor_id")[["name", "country", "rank", "points"]]
    
    st.write("### **Top 5 Ranked Competitors**")
    st.dataframe(top_5_merged)

if tag == "Competitor Lookup":
    st.title("Competitor Lookup and Filtering")
    
    countries = ["All"] + sorted(competitors['country'].unique().tolist())
    selected_country = st.selectbox("Filter by Country", countries)
    search_name = st.text_input("Search by Name")
    rank_min, rank_max = st.slider("Rank Range", 1, 1000, (1, 100))
    points = st.number_input("Minimum Points", min_value=0, value=0, step=10)
    
    # Filter competitors and rankings data
    filtered_data = rankings.copy()
    if selected_country != "All":
        filtered_data = filtered_data[filtered_data['competitor_id'].isin(competitors[competitors['country'] == selected_country]['competitor_id'])]
    if search_name:
        filtered_data = filtered_data[filtered_data['competitor_id'].isin(competitors[competitors['name'].str.contains(search_name, case=False)]['competitor_id'])]
    filtered_data = filtered_data[(filtered_data['rank'] >= rank_min) & (filtered_data['rank'] <= rank_max)]
    if points:
        filtered_data = filtered_data[filtered_data['points'] >= points]
    
    # Merge and display filtered results
    result = filtered_data.merge(competitors, on="competitor_id")[["name", "country", "rank", "points"]]
    
    if not result.empty:
        st.dataframe(result)
    else:
        st.write("No competitors found.")

if tag == "Leader Board":
    st.title("Leaderboards")
    
    tab1, tab2 = st.tabs(["Top-Ranked Competitors", "Highest Points"])
    
    with tab1:
        top_ranked = rankings.nsmallest(10, 'rank').merge(competitors, on="competitor_id")[["name", "country", "rank", "points"]]
        st.dataframe(top_ranked)
    
    with tab2:
        highest_points = rankings.nlargest(10, 'points').merge(competitors, on="competitor_id")[["name", "country", "rank", "points"]]
        st.dataframe(highest_points)

if tag == "Conclusion":
    st.markdown("""
    ### Conclusion
    Thank you for exploring the Competitor Performance Dashboard! 🎉  

    - Gain deep insights into player rankings and performance.  
    - Filter competitors by country, rank, and points.  
    - View top-ranked players and highest point leaders.  
    - Analyze competition trends with interactive visuals.  
    - Unlock valuable, data-driven insights for tennis analytics! 🚀  
    """)

