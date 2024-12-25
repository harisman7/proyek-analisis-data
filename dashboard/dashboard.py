import pandas as pd
import altair as alt
import streamlit as st

hour_df = pd.read_csv("https://raw.githubusercontent.com/harisman7/proyek-analisis-data/refs/heads/main/data/hour.csv")
day_df = pd.read_csv("https://raw.githubusercontent.com/harisman7/proyek-analisis-data/refs/heads/main/data/day.csv")

hour_df.sort_values(by="dteday", inplace=True)
hour_df.reset_index(inplace=True)
hour_df["date"] = pd.to_datetime(hour_df["dteday"])
min_date = hour_df["date"].min()
max_date = hour_df["date"].max()

def usecase1():
    st.title('Pengguna rental sepeda berdasarkan jam tertentu')
    
    # Group by hour and calculate mean values
    hourly_grouped = hour_df.groupby(by="hr").agg({
        "casual": "mean",
        "registered": "mean",
        "cnt": "mean"
    }).reset_index()

    # Melt data for easier plotting of multiple lines
    melted_df = hourly_grouped.melt(id_vars="hr", 
                                    value_vars=["casual", "registered", "cnt"], 
                                    var_name="User Type", 
                                    value_name="Average Count")
    
    # Create line chart
    line_chart = alt.Chart(melted_df).mark_line().encode(
        x=alt.X('hr:O', title='Hour of the Day'),
        y=alt.Y('Average Count:Q', title='Average Count of Users'),
        color=alt.Color('User Type:N', title='Type of User'),
        tooltip=['hr:O', 'User Type:N', 'Average Count:Q']
    ).interactive()

    # Display the chart
    st.altair_chart(line_chart, use_container_width=True)

def usecase2():
    st.subheader("Pilih Rentang Waktu")
    # Date selection
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    # Filter data
    main_hour_df = hour_df[(hour_df["date"] >= str(start_date)) & 
                           (hour_df["date"] <= str(end_date))]
    
    # Group by season and temperature, then aggregate average rentals
    temp_season_grouped = main_hour_df.groupby(by=["season", "temp"]).agg({
        "cnt": "mean"
    }).reset_index().sort_values(by="cnt", ascending=False)

    # Map season numbers to names
    season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    temp_season_grouped['season'] = temp_season_grouped['season'].map(season_map)

    # Create line chart
    line_chart = alt.Chart(temp_season_grouped).mark_line(point=True).encode(
        x=alt.X('temp:Q', title='Normalized Temperature'),
        y=alt.Y('cnt:Q', title='Average Rentals'),
        color=alt.Color('season:N', title='Season'),
        tooltip=['season:N', 'temp:Q', 'cnt:Q']
    ).interactive()

    # Display chart
    st.subheader("Penggunaan Rental Sepeda Berdasarkan Temperature dan Musim")
    st.altair_chart(line_chart, use_container_width=True)

navigation = st.sidebar.radio("Navigation", ["Usecase 1", "Usecase 2"])

if navigation == "Usecase 1":
    usecase1()
elif navigation == "Usecase 2":
    usecase2()

st.sidebar.text('Copyright (c) Harisman Arif 2024')
