import pandas as pd 
import numpy as np
import dask.dataframe as dd
from neuralprophet import NeuralProphet
from neuralprophet.configure import ConfigSeasonality
import matplotlib.pyplot as plt
import matplotlib
import torch.serialization
import logging

logging.basicConfig(level=logging.INFO)  # or DEBUG
logger = logging.getLogger(__name__)
torch.serialization.add_safe_globals([ConfigSeasonality])
logger.info("Added ConfigSeasonality to safe globals")


def load_data():
    df = dd.read_csv("merged_hour_preprocessed_small.csv")
    # convert column to datetime object 
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
    print(df_prophet['ds'].dtype)  # should be datetime64[ns]
    print(type(df_prophet))
    # prophet version
    # model = Prophet()
    # model.fit(df_prophet)

    # create and fit model
    torch.serialization.add_safe_globals([ConfigSeasonality])
    safe_globals = torch.serialization.get_safe_globals()
    logger.info("Safe globals: %s", safe_globals)
    print("Safe globals:", safe_globals)

    # print("ConfigSeasonality in safe globals?", "neuralprophet.configure.ConfigSeasonality" in safe_globals)
    # neuralprophet version
    model = NeuralProphet(learning_rate=1.0)
    model.set_plotting_backend("matplotlib")

    metrics = model.fit(df_prophet)
    return model

# take prophet model, number of periods, and frequency -> make predictions and create visualization file
def make_predictions(model, df, periods, freq):
    matplotlib.use("Agg")

    df_prophet = df[['timestamp_conv', 'avg_speed']]
    df_prophet.columns = ['ds', 'y'] # rename columns for Prophet

    # prophet version:
    # future = model.make_future_dataframe(periods, freq)
    # forecast = model.predict(future)
    # fig = plot_components(model, forecast)  
    # fig.write_image("prophet_components.png") 

    # neuralprophet version:
    forecast = model.predict(df_prophet)
    model.plot(forecast)
    plt.savefig("np_forecast_plot.png")
    # model.plot_components(forecast)
    model.plot_parameters()
    plt.savefig("np_parameters_plot.png")
    plt.close()


    # forecast = model.predict(df)
    # fig_forecast = plot(forecast, quantiles=model.config_train.quantiles)
    # fig_forecast.write_image("MYTESTER_forecast_plot.png")

    # fig = plot_components_plotly(model, forecast) 
    # fig = plot_components(model, forecast)  
    # fig.write_image("prophet_components.png") 

    # return model.plot_components(forecast) # trend and seasonality components


