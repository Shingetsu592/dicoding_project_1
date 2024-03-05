import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

names = []
month_name = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
data_path = "Dashboard/all_data.csv"

def intro():
    st.title('Welcome to the Dashboard')
    st.write('This is a simple dashboard show the distribution of CO for each station.')

def clean_data(df):
    # remove the rows with missing values
    df = df.dropna()
    df = df.drop(columns='No')
    return df

def data_date(df):
    # change the year, month, and day into one column and convert it to datetime format
    df['date'] = pd.to_datetime(df[['year', 'month', 'day']])
    return df

def station_and_date_select(df):
    st.write('CO, PM 2.5, and PM 10 distribution for each station')
    station = st.selectbox('Select Station', df['station'].unique())
    st.write('Year')
    year = st.slider('Select Year', 2013, 2017)
    st.write('Month')
    if year == 2013:
        month = st.slider('Select Month', 3, 12)
    elif year == 2017:
        month = st.slider('Select Month', 1, 2)
    else:
        month = st.slider('Select Month', 1, 12)
    df_selected = df[(df['station'] == station) & (df['year'] == year) & (df['month'] == month)]
    return df_selected, station, year, month

def plot_distribution(df, parameter, station, year, month):
    # plot CO or PM2.5 distribution for each station towards x with year and month parameter in different plots and selectbox
    plt.bar(df['date'], df[parameter])
    plt.xlabel('Day')
    plt.ylabel(parameter)
    plt.title('{} distribution for station {} in {} {}'.format(parameter, station, month_name[month-1], year))
    plt.xticks(rotation=90)  # This will skew the x values
    plt.tight_layout()  # This will fit the plot to the available space
    st.pyplot(plt)
    plt.clf()

intro()
df = pd.read_csv(data_path)
df = clean_data(df)
df = data_date(df)
st.dataframe(df, use_container_width=True)
df_selected, station, year, month = station_and_date_select(df)
plot_distribution(df_selected, parameter='CO', station=station, year=year, month=month)
plot_distribution(df_selected, parameter='PM2.5', station=station, year=year, month=month)
plot_distribution(df_selected, parameter='PM10', station=station, year=year, month=month)
