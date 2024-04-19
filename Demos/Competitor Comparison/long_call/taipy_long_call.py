import requests
import pickle
import time
from taipy.gui import Gui, notify, invoke_long_callback
import plotly.express as px
import numpy as np
import pandas as pd

DATA_PATH = "long_call/industry_df.pkl"

df = pickle.load(open(DATA_PATH, "rb"))

df_2021 = df.copy()
df_2021["PA-LQ_Data"] = df_2021["PA-LQ_Data"] + np.random.normal(0, 1, len(df_2021))
df_2022 = df.copy()
df_2022["PA-LQ_Data"] = df_2022["PA-LQ_Data"] + np.random.normal(0, 1, len(df_2022))
df_2023 = df.copy()
df_2023["PA-LQ_Data"] = df_2023["PA-LQ_Data"] + np.random.normal(0, 1, len(df_2023))

counties = requests.get(
    "https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json"
).json()

selected_indices = []
mean_value = 0
selected_year = 2023
year = 2024
logs = "No Forecast"


def on_change(state, var_name, var_value):
    if var_name == "selected_indices":
        indices = state.selected_indices
        if indices:
            state.mean_value = df.iloc[indices]["PA-LQ_Data"].mean()
        else:
            state.mean_value = 0
    if var_name == "selected_year":
        if int(state.selected_year) == 2021:
            state.map_fig = create_map_fig(df_2021)
        elif int(state.selected_year) == 2022:
            state.map_fig = create_map_fig(df_2022)
        elif int(state.selected_year) == 2023:
            state.map_fig = create_map_fig(df_2023)


def create_map_fig(data):
    fig = px.choropleth_mapbox(
        data,
        geojson=counties,
        locations="IBRC_Geo_ID",
        color="PA-LQ_Data",
        color_continuous_scale="Reds",
        mapbox_style="carto-positron",
        zoom=3,
        center={"lat": 37.0902, "lon": -95.7129},
        opacity=0.5,
        hover_data="Description",
    )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig


map_fig = create_map_fig(df_2023)


def long_forecast():
    time.sleep(60)
    return "Forecasting completed."


counter = 0


def long_forecast_status(state, status):
    if isinstance(status, bool):
        if status:
            notify(state, "success", f"Forecasting completed.")
        else:
            notify(state, "error", f"Forecasting failed.")
    else:
        state.counter += 1
        state.logs = f"Forecasting... ({state.counter}s)"


def predict(state):
    notify(state, "info", "Predicting... (this may take a while)")
    state.logs = "Forecasting started."
    invoke_long_callback(state, long_forecast, [], long_forecast_status, [], 1000)


page = """
<|card|
# Recreation Industry Agglomeration 🗺️
<|{selected_year}|selector|dropdown|lov=2021;2022;2023|>
### Mean CLQ of Selection: <|{round(mean_value,2)}|text|raw|>
<|chart|figure={map_fig}|selected={selected_indices}|>
|>
<br/>
<|layout|columns=1 1|
<|card|
## Forecasting
<|{year}|selector|dropdown|lov=2024;2025;2026|>
<|Run Forecasting|button|on_action=predict|>
|>
<|card|
## Logs
###<|{logs}|text|raw|>
|>
|>
"""

Gui(page).run(port=5015, dark_mode=False, debug=True)
