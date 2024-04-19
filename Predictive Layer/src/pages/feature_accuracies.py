from string import Template
from taipy.gui import Markdown
from icecream import ic
import pandas as pd
import numpy as np

from .utils import positive_negative_cell_style, positive_negative_cell_style_0_1

df = pd.DataFrame({
    "Group of features": ["FUND_CORRELATION", "WEATHER_CLOUD", "API2", "OIL", "CRUDE_FLOW", "CRUDE_FLOW_DYN", "CSPI", "WEATHER_WIND", "OTHERS", "DA", "COAL_FLOW", "POWER_Y", "TTF", "LNG_STORAGE", "EUA_DYN", "POWER_FWC", "WEATHER_TEMP", "LNG_FLOW", "API2_DYN", "CSPI_DYN", "POWER_M", "POWER_TA", "TTF_DYN", ],
})
df["SUCCESS 1M [%]"] = np.random.random(size=len(df))
df["SUCCESS 3M [%]"] = np.random.random(size=len(df))
df["SUCCESS 6M [%]"] = np.random.random(size=len(df))
df["GAIN 1M [€/MWh]"] = np.random.uniform(low=-1, high=1, size=len(df))
df["GAIN 3M [€/MWh]"] = np.random.uniform(low=-3, high=3, size=len(df))
df["GAIN 6M [€/MWh]"] = np.random.uniform(low=-6, high=6, size=len(df))
df["CAP VALUE 1M [%]"] = np.random.uniform(low=-1, high=1, size=len(df))

table_properties = {
    "style[SUCCESS 1M [%]]": positive_negative_cell_style_0_1,
    "style[SUCCESS 3M [%]]": positive_negative_cell_style_0_1,
    "style[SUCCESS 6M [%]]": positive_negative_cell_style_0_1,
    "style[GAIN 1M [€/MWh]]": positive_negative_cell_style,
    "style[GAIN 3M [€/MWh]]": positive_negative_cell_style,
    "style[GAIN 6M [€/MWh]]": positive_negative_cell_style,
    "style[CAP VALUE 1M [%]]": positive_negative_cell_style,
}

product_name_list = ["DEM", "DEQ", "DEY"]
selected_product_name = product_name_list[0]

feature_accuracies_template = Template(
"""
# Feature Accuracies

<|layout|columns=3 1|

<|{df}|table|number_format=%.3f|width=fit-content|properties={table_properties}|class_name=rows-bordered|filter|>

<|rhs|

### Product

<|{selected_product_name}|selector|lov={product_name_list}|dropdown|>

### Date

<|{selected_datetime}|date|>

|>

|>
""")

feature_accuracies_md = Markdown(feature_accuracies_template.substitute())

def feature_accuracies_on_init(state):
    ...

root_var_update_list = ["selected_datetime",]
def feature_accuracies_on_navigate(state):
    for var_name in root_var_update_list:
        feature_accuracies_on_change(state, var_name, getattr(state, var_name))

def feature_accuracies_on_change(state, var_name, var_value):
    # root variables
    ...

    # module variables
    ...
