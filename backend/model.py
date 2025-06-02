import pandas as pd 
import numpy as np
import dask.dataframe as dd
from prophet import Prophet
from prophet.plot import plot_components_plotly

def load_data():
    df = dd.read_csv("merged_hour_preprocessed.csv")
    # convert column to datetime object 
    # df['timestamp_conv'] = dd.to_datetime(df['timestamp_conv'], format="%Y-%m-%d %H:%M:%S")
    df['timestamp_conv'] = dd.to_datetime(df['timestamp'], format="%m/%d/%Y %H:%M:%S")
    return df

# dask dataframe -> filtered pandas dataframe 
def filter_dataset_by_station(df, station_id):
    # print(df['timestamp_conv'].compute())
    df_filtered = df[df['station_id'] == station_id]
    # print(df_filtered.head())
    df_filtered_pd = df_filtered.compute()
    return df_filtered_pd

def build_prophet_model(df_filtered):
    df_prophet = df_filtered[['timestamp_conv', 'avg_speed']]
    df_prophet.columns = ['ds', 'y'] # rename columns for Prophet

    # create and fit model
    model = Prophet()
    model.fit(df_prophet)
    return model

# take prophet model, number of periods, and frequency -> make predictions and create visualization file
def make_predictions(model, periods, freq):
    # future predictions for 24 hours
    future = model.make_future_dataframe(periods, freq)
    forecast = model.predict(future)

    fig = plot_components_plotly(model, forecast) 
    fig.write_image("prophet_components.png") 
    # return model.plot_components(forecast) # trend and seasonality components