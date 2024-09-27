import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit as st

# Load dataset
df = pd.read_csv("dashboard/data.csv")
df['date'] = pd.to_datetime(df['date'])

st.set_page_config(page_title="Bike-sharing Dashboard :bike:", page_icon=":bike:")

# Helper functions
def create_monthly_users_df(df):
    monthly_users_df = df.resample(rule='M', on='date').agg({
        "casual_user": "sum",
        "registered_user": "sum",
        "total_user": "sum"
    })
    monthly_users_df.index = monthly_users_df.index.strftime('%b-%y')
    monthly_users_df = monthly_users_df.reset_index()
    monthly_users_df.rename(columns={
        "date": "yearmonth",
        "total_user": "total_rides",
        "casual_user": "casual_rides",
        "registered_user": "registered_rides"
    }, inplace=True)
    
    return monthly_users_df

def create_seasonly_users_df(df):
    seasonly_users_df = df.groupby("season").agg({
        "casual_user": "sum",
        "registered_user": "sum",
        "total_user": "sum"
    })
    seasonly_users_df = seasonly_users_df.reset_index()
    seasonly_users_df.rename(columns={
        "total_user": "total_rides",
        "casual_user": "casual_rides",
        "registered_user": "registered_rides"
    }, inplace=True)
    seasonly_users_df = pd.melt(
        seasonly_users_df,
        id_vars=['season'],
        value_vars=['casual_rides', 'registered_rides'],
        var_name='type_of_rides',
        value_name='count_rides'
    )
    seasonly_users_df['season'] = pd.Categorical(seasonly_users_df['season'], categories=['Spring', 'Summer', 'Fall', 'Winter'])
    seasonly_users_df = seasonly_users_df.sort_values('season')
    return seasonly_users_df

def create_weekday_users_df(df):
    weekday_users_df = df.groupby("weekday").agg({
        "casual_user": "sum",
        "registered_user": "sum",
        "total_user": "sum"
    })
    weekday_users_df = weekday_users_df.reset_index()
    weekday_users_df.rename(columns={
        "total_user": "total_rides",
        "casual_user": "casual_rides",
        "registered_user": "registered_rides"
    }, inplace=True)
    
    weekday_users_df = pd.melt(
        weekday_users_df,
        id_vars=['weekday'],
        value_vars=['casual_rides', 'registered_rides'],
        var_name='type_of_rides',
        value_name='count_rides'
    )
    weekday_users_df['weekday'] = pd.Categorical(weekday_users_df['weekday'], categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    weekday_users_df = weekday_users_df.sort_values('weekday')
    return weekday_users_df

def create_weather_users_df(df):
    weather_users_df = df.groupby("weather").agg({
        "casual_user": "sum",
        "registered_user": "sum",
        "total_user": "sum"
    })
    weather_users_df = weather_users_df.reset_index()
    weather_users_df.rename(columns={
        "total_user": "total_rides",
        "casual_user": "casual_rides",
        "registered_user": "registered_rides"
    }, inplace=True)
    
    weather_users_df['weather'] = pd.Categorical(weather_users_df['weather'], categories=['Clear', 'Mist', 'Light Snow', 'Heavy Rain'])
    weather_users_df = weather_users_df.sort_values('weather')
    return weather_users_df

def create_workingday_users_df(df):
    workingday_users_df = df.groupby("workingday").agg({
        "casual_user": "sum",
        "registered_user": "sum",
        "total_user": "sum"
    })
    workingday_users_df = workingday_users_df.reset_index()
    workingday_users_df.rename(columns={
        "total_user": "total_rides",
        "casual_user": "casual_rides",
        "registered_user": "registered_rides"
    }, inplace=True)
    
    workingday_users_df = pd.melt(
        workingday_users_df,
        id_vars=['workingday'],
        value_vars=['casual_rides', 'registered_rides'],
        var_name='type_of_rides',
        value_name='count_rides'
    )
    workingday_users_df['workingday'] = pd.Categorical(workingday_users_df['workingday'], categories=[0, 1])
    workingday_users_df = workingday_users_df.sort_values('workingday')
    return workingday_users_df

# Sidebar
min_date = df["date"].min()
max_date = df["date"].max()

with st.sidebar:
    st.image("image/Bike.png")
    
    # Date range slider
    start_date, end_date = st.slider(
        "Select Date Range:",
        min_value=min_date.to_pydatetime(),
        max_value=max_date.to_pydatetime(),
        value=(min_date.to_pydatetime(), max_date.to_pydatetime()),
        format="MM/DD/YY"
    )

start_date = pd.Timestamp(start_date)
end_date = pd.Timestamp(end_date)

# Filter dataframe based on date range
main_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

# Data aggregation
monthly_users_df = create_monthly_users_df(main_df)
weekday_users_df = create_weekday_users_df(main_df)
seasonly_users_df = create_seasonly_users_df(main_df)
weather_users_df = create_weather_users_df(main_df)
workingday_users_df = create_workingday_users_df(main_df)

# Main dashboard title
st.title("Bike-Sharing Dashboard :bike:")

# Ride metrics
col1, col2, col3 = st.columns(3)

if st.checkbox("Show detailed ride statistics"):
    with col1:
        total_all_rides = main_df['total_user'].sum()
        st.metric("Total Rides", value=total_all_rides)
    with col2:
        total_casual_rides = main_df['casual_user'].sum()
        st.metric("Total Casual Rides", value=total_casual_rides)
    with col3:
        total_registered_rides = main_df['registered_user'].sum()
        st.metric("Total Registered Rides", value=total_registered_rides)

st.markdown("---")

# Monthly Rides Line Chart
fig, ax = plt.subplots()
sns.lineplot(data=monthly_users_df, x='yearmonth', y='casual_rides', ax=ax, label='Casual Rides', color='skyblue')
sns.lineplot(data=monthly_users_df, x='yearmonth', y='registered_rides', ax=ax, label='Registered Rides', color='orange')
sns.lineplot(data=monthly_users_df, x='yearmonth', y='total_rides', ax=ax, label='Total Rides', color='red')
ax.set_title("Monthly Count of Bikeshare Rides")
ax.set_xlabel('')
ax.set_ylabel('Total Rides')
ax.legend()
st.pyplot(fig)

# Season Rides Pie Chart
st.subheader("Distribution of Bikeshare Rides by Season")
fig1, ax1 = plt.subplots()
season_colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99']
ax1.pie(seasonly_users_df['count_rides'], labels=seasonly_users_df['season'], autopct='%1.1f%%', startangle=90, colors=season_colors)
ax1.set_title('Season Count of Bikeshare Rides')
plt.legend(title="Seasons", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
st.pyplot(fig1)

# Weekday Rides Area Chart
st.subheader("Count of Bikeshare Rides by Weekday")
weekday_users_df_pivot = weekday_users_df.pivot_table(index='weekday', columns='type_of_rides', values='count_rides')
fig2, ax2 = plt.subplots(figsize=(10, 6))
weekday_users_df_pivot.plot(kind='bar', ax=ax2)
ax2.set_title('Count of Bikeshare Rides by Weekday')
ax2.set_xlabel('Weekday')
ax2.set_ylabel('Total Rides')
ax2.legend(title='Type of Rides')
plt.xticks(rotation=45, ha='right')
st.pyplot(fig2)

# Weather-Based Rides Visualization
st.subheader("Count of Bikeshare Rides by Weather")

weather_options = weather_users_df['weather'].unique().tolist()
selected_weather = st.multiselect("Select Weather Conditions", weather_options, default=weather_options)

filtered_weather_df = weather_users_df[weather_users_df['weather'].isin(selected_weather)]

chart_type = st.radio("Select Chart Type", ("Bar Chart", "Pie Chart"))

if chart_type == "Bar Chart":
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=filtered_weather_df, x='weather', y='total_rides', ax=ax, palette='viridis')
    ax.set_xlabel("Weather Condition")
    ax.set_ylabel("Total Rides")
    ax.set_title("Count of Bikeshare Rides by Weather")
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)

elif chart_type == "Pie Chart":
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.pie(filtered_weather_df['total_rides'], labels=filtered_weather_df['weather'], autopct='%1.1f%%', startangle=90, colors=plt.cm.Spectral(np.linspace(0, 1, len(filtered_weather_df))))
    ax.set_title('Distribution of Bikeshare Rides by Weather')
    st.pyplot(fig)

# Casual vs Registered Rides by Weather
st.subheader("Comparison of Casual and Registered Rides by Weather")

fig, ax = plt.subplots(figsize=(12, 6))
x = range(len(filtered_weather_df))
width = 0.35

ax.bar(x, filtered_weather_df['casual_rides'], width, label='Casual Rides', color='skyblue')
ax.bar([i + width for i in x], filtered_weather_df['registered_rides'], width, label='Registered Rides', color='orange')

ax.set_xlabel('Weather Condition')
ax.set_ylabel('Number of Rides')
ax.set_title('Casual vs Registered Rides by Weather')
ax.set_xticks([i + width/2 for i in x])
ax.set_xticklabels(filtered_weather_df['weather'])
ax.legend()

plt.xticks(rotation=45, ha='right')
st.pyplot(fig)

# Workingday vs Non-Workingday Rides Bar Chart
workingday_map = {0: 'Non-Working Day', 1: 'Working Day'}
workingday_users_df['day_type'] = workingday_users_df['workingday'].map(workingday_map)

st.subheader("Count of Bikeshare Rides on Working Days vs Non-Working Days")

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=workingday_users_df, x='day_type', y='count_rides', hue='type_of_rides', ax=ax, palette='viridis')
ax.set_xlabel("Day Type")
ax.set_ylabel("Total Rides")
ax.set_title("Count of Bikeshare Rides on Working Days vs Non-Working Days")
plt.legend(title='Type of Rides')
plt.xticks(rotation=0)
st.pyplot(fig)

st.caption('Copyright (c), created by Alvin Astradinata')