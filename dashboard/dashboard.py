import pandas as pd
import altair as alt
import streamlit as st

# Load the data
df = pd.read_csv("data/player_stats_2000_2025.csv")
# Clean the datas
df['Team'] = df['Team'].replace({
    'New York': 'New York Yankees',
    'Boston': 'Boston Red Sox',
    'Chicago': 'Chicago White Sox',
    'Cleveland': 'Cleveland Guardians',
    'Cleveland Indians': 'Cleveland Guardians',
    'Detroit': 'Detroit Tigers',
    'Houston': 'Houston Astros',
    'Kansas City': 'Kansas City Royals',
    'Los Angeles': 'Los Angeles Angels',
    'Anaheim': 'Los Angeles Angels',
    'Minnesota': 'Minnesota Twins',
    'Oakland': 'Oakland Athletics',
    'Seattle': 'Seattle Mariners',
    'Tampa Bay': 'Tampa Bay Rays',
    'Texas': 'Texas Rangers',
    'Toronto': 'Toronto Blue Jays',
    'Baltimore': 'Baltimore Orioles'
})
st.title("Baseball Player Stats Dashboard (2000–2025)")

# Top 10 Players by Selected Category
st.header("Top 10 Players by Category:")
categories = df['Category'].unique()
selected_category = st.selectbox("Category", categories)
top_10 = df[df['Category'] == selected_category].sort_values(by='Value', ascending=False).head(10)
st.dataframe(top_10[['Year', 'Player', 'Team', 'Value']])

# Team Participation Heatmap by Year and Category
st.header("Team Category Heatmap")
heat_df = df[df['Category'] == selected_category]
heat_grouped = heat_df.groupby(["Team", "Year"]).agg({"Value": "sum"}).reset_index()

heatmap = alt.Chart(heat_grouped).mark_rect().encode(
    x=alt.X("Year:O", title="Year"),
    y=alt.Y("Team:N", title="Team"),
    color=alt.Color("Value:Q", scale=alt.Scale(scheme='greens'), title="Total Value"),
    tooltip=["Team", "Year", "Value"]
).properties(height=600, width=900)

st.altair_chart(heatmap, use_container_width=True)

#  Average Value per Category
st.header("Average Value ")
avg_per_category = df.groupby("Category")["Value"].mean().reset_index()
bar_chart = alt.Chart(avg_per_category).mark_bar().encode(
    x=alt.X("Category", sort="-y"),
    y=alt.Y("Value", title="Average Value"),
    tooltip=["Category", "Value"]
).properties(width=800)
st.altair_chart(bar_chart, use_container_width=True)

# Average Stat per Year
st.header("Average Metric Value per Year (All Categories Combined)")
avg_per_year = df.groupby("Year")["Value"].mean().reset_index()
line_chart = alt.Chart(avg_per_year).mark_line(point=True).encode(
    x=alt.X("Year:O", title="Year"),
    y=alt.Y("Value", title="Average Value"),
    tooltip=["Year", "Value"]
).properties(height=300, width=800)
st.altair_chart(line_chart, use_container_width=True)

# Top 10 Players by Average Stat
st.header("Top 10 Players by Average Value")
avg_by_player = df.groupby("Player")["Value"].mean().reset_index()
top_players = avg_by_player.sort_values(by="Value", ascending=False).head(10)
bar_top_players = alt.Chart(top_players).mark_bar().encode(
    x=alt.X("Player", sort="-y"),
    y=alt.Y("Value", title="Average Value"),
    color="Player",
    tooltip=["Player", "Value"]
).properties(width=800)
st.altair_chart(bar_top_players, use_container_width=True)

# Top Teams by Average Stat
st.header("Top 10 Teams by Average Value")
avg_by_team = df.groupby("Team")["Value"].mean().reset_index()
top_teams = avg_by_team.sort_values(by="Value", ascending=False).head(10)
bar_top_teams = alt.Chart(top_teams).mark_bar().encode(
    x=alt.X("Team", sort="-y"),
    y=alt.Y("Value", title="Average Value"),
    color="Team",
    tooltip=["Team", "Value"]
).properties(width=800)
st.altair_chart(bar_top_teams, use_container_width=True)

