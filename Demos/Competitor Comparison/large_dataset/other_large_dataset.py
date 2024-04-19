import streamlit as st
from math import cos, exp

decay = 0.01


def compute_data(values: int) -> list:
    return [cos(i / 6000) * exp(-i * decay / 600) for i in range(values)]


st.title("In Other Libraries")

value = st.slider("", 1000, 1000000, 1000)

st.line_chart(compute_data(value))
