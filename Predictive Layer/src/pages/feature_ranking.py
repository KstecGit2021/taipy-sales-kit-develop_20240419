from taipy.gui import Markdown
from icecream import ic
import datetime as dt
from dateutil.tz import tzutc
import pandas as pd
import numpy as np
from .utils import PRIMARY_COLOR

start_datetime = dt.datetime(2023, 8, 1, tzinfo=tzutc())
end_datetime = dt.datetime(2023, 8, 31, tzinfo=tzutc())

feature_group_list = [
    "API2", "API2_DYN", "COAL_FLOW", "COAL_FLOW_DYN", "CRUDE_FLOW", "CRUDE_FLOW_DYN", "CRUDE_OFFSHORE_STORAGE", 
    "CRUDE_OFFSHORE_STORAGE_DYN", "CSPI", "CSPI_DYN", "DA", "EUA",
]
df = pd.DataFrame({"datetime": pd.date_range(start=start_datetime, end=end_datetime, freq="D", tz=tzutc())})
df = pd.concat([df] + [pd.Series(np.random.uniform(low=-1.0, high=0.5, size=len(df)), name=feature) for feature in feature_group_list], axis=1)

ranking_cols = feature_group_list
linear_contributions_cols = feature_group_list

def create_chart_df(df: pd.DataFrame, start_datetime: dt.datetime, end_datetime: dt.datetime,):
    """Used by ranking chart and linear_contributions chart.
    
    Args
    ----
    start_datetime and end_datetime : dt.datetime
        Datetime object in UTC as returned by the Taipy date selector.
    """

    df = df.set_index("datetime")[start_datetime:end_datetime].reset_index()
    return df

def create_chart_properties(cols: list[str]):
    properties = {f"y[{i+1}]": col for i, col in enumerate(cols)}
    properties["x"] = "datetime"
    properties["mode"] = "lines"
    properties["line"] = dict(width=3)
    return properties

ranking_layout = {"title": dict(text="Ranking", font=dict(size=20, color=PRIMARY_COLOR)), "hovermode": "x unified"}
linear_contributions_layout = {"title": dict(text="Linear contributions", font=dict(size=20, color=PRIMARY_COLOR)), "hovermode": "x unified"}

ranking_options = {"stackgroup": "rankings"}

measure_list = ["Absolute",  "Relative"]
selected_measure = measure_list[1]

feature_ranking_md = Markdown(
"""
# Feature Ranking

<|layout|columns=3 1|

<|lhs|

<|{create_chart_df(df, start_datetime, end_datetime)}|chart|rebuild|mode=none|height=35vh|layout={ranking_layout}|options={ranking_options}|properties={create_chart_properties(ranking_cols)}|>

<br/>

<|{create_chart_df(df, start_datetime, end_datetime)}|chart|rebuild|height=35vh|layout={linear_contributions_layout}|properties={create_chart_properties(linear_contributions_cols)}|>

|>


<rhs|

### Start Date

<|{start_datetime}|date|>

### End Date

<|{end_datetime}|date|>

### Product

<|{selected_product}|selector|lov={product_list}|dropdown|>

### Measure

<|{selected_measure}|selector|lov={measure_list}|>

Feature contributions over time. Follow specific market drivers evolution over time.

|rhs>


|>

""")

def feature_ranking_on_init(state):
    ...

root_var_update_list = []
def feature_ranking_on_navigate(state):
    for var_name in root_var_update_list:
        feature_ranking_on_change(state, var_name, getattr(state, var_name))

def feature_ranking_on_change(state, var_name, var_value):
    # root variables
    ...

    # module variables
    ...
