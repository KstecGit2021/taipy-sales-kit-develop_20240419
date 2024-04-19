import streamlit as st
import pandas as pd
import numpy as np

initial_data = pd.DataFrame(
    np.random.randn(100, 2) / [50, 50] + [37.76, -122.4], columns=["lat", "lon"]
)

st.title("In Other Libraries")

values = st.slider("", 0, 100, 50)

df = initial_data[:values]

st.map(df)
