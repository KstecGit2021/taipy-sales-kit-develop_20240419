import requests
import pickle
import time
import streamlit as st
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
logs = "No forecasting logs yet."


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

st.title("In Other Libraries")

# Create a dropdown selector for selected_year
selected_year = st.selectbox("Select Year", [2021, 2022, 2023])

st.plotly_chart(map_fig)

counter = 0

button = st.button("Run Forecasting")

logs = st.title("No Forecast")

# Create a button that triggers long_callback
if button:
    for _ in range(60):
        time.sleep(1)
        counter += 1
        logtext = f"Forecasting... ({counter}s)"
        logs.title(logtext)
