import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

names = []
month_name = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
direc = "Dashboard/main_data/"

def intro():
    st.title('Welcome to the Dashboard')
    st.write('This is a simple dashboard show the distribution of CO for each station.')

def import_data():
    for files in os.listdir(direc):
        names.append(direc + files)
    # concat all the files into one dataframe
    df = pd.concat([pd.read_csv(f) for f in names], ignore_index=True)
    return df

def clean_data(df):
    # remove the rows with missing values
    df = df.dropna()
    df = df.drop(columns='No')
    return df

def data_date(df):
    # change the year, month, and day into one column and convert it to datetime format
    df['date'] = pd.to_datetime(df[['year', 'month', 'day']])
    return df

def plot_CO(df, parameter):
    # plot CO distribution for each station towards x with year and month parameter in different plots and selectbox
    st.write('CO distribution for each station')
    station = df['station'].unique()
    station_select = st.selectbox('Select Station', station)
    st.write('Year')
    year = st.slider('Select Year', 2013, 2017)
    st.write('Month')
    if year == 2013:
        month = st.slider('Select Month', 3, 12)
    elif year == 2017:
        month = st.slider('Select Month', 1, 2)
    else:
        month = st.slider('Select Month', 1, 12)
    df_selected = df[(df['station'] == station_select) & (df['year'] == year) & (df['month'] == month)]
    plt.bar(df_selected['date'], df_selected[parameter])
    plt.xlabel('Day')
    plt.ylabel('CO')
    plt.title('CO distribution for station {} in {} {}'.format(station_select, month_name[month-1], year))
    plt.xticks(rotation=90)  # This will skew the x values
    plt.tight_layout()  # This will fit the plot to the available space
    st.pyplot(plt)
    plt.clf()

intro()
df = import_data()
df = clean_data(df)
df = data_date(df)
st.dataframe(df, use_container_width=True)
plot_CO(df, parameter='CO')