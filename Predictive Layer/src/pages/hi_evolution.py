from string import Template
from taipy.gui import Markdown
from icecream import ic
import datetime as dt
import pandas as pd
import numpy as np
from dateutil.tz import tzutc

from .utils import PRIMARY_COLOR


# Date range slider
date_format = "%Y-%m-%d"
min_date = dt.date(2023, 8, 1)
max_date = dt.date(2023, 8, 31)
date_list = [min_date + dt.timedelta(days=i) for i in range((max_date - min_date).days+1)]
date_list_str = [date.strftime(date_format) for date in date_list]
selected_datetime_str_pair = [date_list_str[0], date_list_str[-1]]

# Derived from the date range slider and internally used for filtering the df
start_datetime = dt.datetime.strptime(selected_datetime_str_pair[0], date_format).replace(tzinfo=tzutc())
end_datetime = dt.datetime.strptime(selected_datetime_str_pair[1], date_format).replace(tzinfo=tzutc())

df = pd.DataFrame({"datetime": pd.date_range(start=start_datetime, end=end_datetime, freq="D", tz=tzutc())})
df["AV_CHI2"] = np.random.uniform(low=0.9, high=2.1, size=len(df))
df["AV_CHI2_PCA80"] = np.random.uniform(low=0.9, high=2.1, size=len(df))
df["AV_CHI2_PCA95"] = np.random.uniform(low=0.9, high=2.1, size=len(df))
df["AV_CHI2W"] = np.random.uniform(low=0.9, high=2.1, size=len(df))
df["AV_OOR"] = np.random.uniform(low=0.0, high=0.02, size=len(df))

hi_evo_cols = ["AV_CHI2", "AV_CHI2_PCA80", "AV_CHI2_PCA95", "AV_CHI2W",]
hi_oor_cols = ["AV_OOR",]

def create_chart_df(df: pd.DataFrame, start_datetime: dt.datetime, end_datetime: dt.datetime,):
    """Used by hi_evo chart and hi_evo_oor chart.
    
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

hi_evo_layout = {"title": dict(text="HI Evolution", font=dict(size=20, color=PRIMARY_COLOR)), "hovermode": "x unified"}
hi_oor_layout = {"title": dict(text="HI Evolution (OOR)", font=dict(size=20, color=PRIMARY_COLOR)), "hovermode": "x unified"}


hi_evolution_template = Template(
"""
# HI Evolution

<|layout|columns=3 1|

<|lhs|

<|{create_chart_df(df, start_datetime, end_datetime)}|chart|rebuild|height=35vh|layout={hi_evo_layout}|properties={create_chart_properties(hi_evo_cols)}|>

<br/>

<|{create_chart_df(df, start_datetime, end_datetime)}|chart|rebuild|height=35vh|layout={hi_oor_layout}|properties={create_chart_properties(hi_oor_cols)}|>

|>


<|rhs|

### Date

<|{selected_datetime_str_pair}|slider|lov={date_list_str}|continuous=False|> 

**<|{selected_datetime_str_pair[0]}|text|class_name=color-primary|> to <|{selected_datetime_str_pair[1]}|text|class_name=color-primary|>**

### Product

<|{selected_product}|selector|lov={product_list}|dropdown|>

|>


|>

""")

hi_evolution_md = Markdown(hi_evolution_template.substitute())

def hi_evolution_on_init(state):
    ...

root_var_update_list = ["selected_product",]
def hi_evolution_on_navigate(state):
    for var_name in root_var_update_list:
        hi_evolution_on_change(state, var_name, getattr(state, var_name))

def hi_evolution_on_change(state, var_name, var_value):
    # root variables
    if var_name == "":
        ...

    # module variables
    elif var_name == "selected_datetime_str_pair":
        state.start_datetime = dt.datetime.strptime(var_value[0], date_format).replace(tzinfo=tzutc())
        state.end_datetime = dt.datetime.strptime(var_value[1], date_format).replace(tzinfo=tzutc())
