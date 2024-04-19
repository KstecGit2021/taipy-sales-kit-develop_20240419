from taipy.gui import Markdown
from icecream import ic
from .utils import get_indicator_success_failure_class, positive_negative_cell_style
import pandas as pd
import numpy as np
import datetime as dt
from dateutil.tz import tzutc

feature_group_list = [
    "CSPI_DYN", "CSPI", "LNG_FLOW_DYN", "CRUDE_OFFSHORE_STORAGE_DYN", "EUA_DYN", "TTF_DYN", "POWER_TA", "EUA", "OTHERS",
    "DA", "WEATHER_WIND", "CRUDE_FLOW_DYN", "POWER_OHLC", "COAL_FLOW", "COAL_FLOW_DYN", "TTF", "LNG_STORAGE",
    "LNG_FLOW", "CRUDE_OFFSHORE_STORAGE", "IMBALANCE", "GAS_EU", "POWER_Q", "POWER_Y", "WEATHER_OTHERS", "POWER_M",
]
df = pd.DataFrame({"Feature Groups": feature_group_list})
df["Contribution 1"] = np.random.uniform(low=-1, high=1, size=len(df)).round(3)
df["Contribution 2"] = np.random.uniform(low=-1, high=1, size=len(df)).round(3)
df["Contribution 2 - Contribution 1"] = (df["Contribution 2"] - df["Contribution 1"])

table_properties = {
    "style[Contribution 1]": positive_negative_cell_style,
    "style[Contribution 2]": positive_negative_cell_style,
    "style[Contribution 2 - Contribution 1]": positive_negative_cell_style,
    "height": "65vh",
}

measure_list = ["Absolute",  "Relative"]
selected_measure = measure_list[1]

predictive_value_1 = -0.22
predictive_value_1_class = get_indicator_success_failure_class(predictive_value_1)
start_datetime_1 = dt.datetime(2019, 1, 4, tzinfo=tzutc())
end_datetime_1 = dt.datetime(2019, 12, 15, tzinfo=tzutc())

predictive_value_2 = -0.24
predictive_value_2_class = get_indicator_success_failure_class(predictive_value_2)
start_datetime_2 = dt.datetime(2019, 1, 4, tzinfo=tzutc())
end_datetime_2 = dt.datetime(2019, 10, 27, tzinfo=tzutc())


period_comparison_md = Markdown(
"""
# Period Comparison

<|layout|columns=3 1|

<lhs|
<|{df}|table|number_format=%.3f|properties={table_properties}|class_name=rows-bordered|>

<bottom_bar|layout|columns=2 2 2 1 2 2 2|

<predictive_value_1|h5 text-center|
**Predictive Value**{: .color-primary}

<|{predictive_value_1}|text|raw=True|class_name={predictive_value_1_class} h2|>
|predictive_value_1>

<start_datetime_1|h5|
**Start Date:**{: .color-primary} 

<|{start_datetime_1}|date|>
|start_datetime_1>

<end_datetime_1|h5|
**End Date:**{: .color-primary} 

<|{end_datetime_1}|date|>
|end_datetime_1>

<|part|>

<predictive_value_2|h5 text-center|
**Predictive Value**{: .color-primary}

<|{predictive_value_2}|text|raw=True|class_name={predictive_value_2_class} h2|>
|predictive_value_2>

<start_datetime_2|h5|
**Start Date:**{: .color-primary} 

<|{start_datetime_2}|date|>
|start_datetime_2>

<end_datetime_2|h5|
**End Date:**{: .color-primary} 

<|{end_datetime_2}|date|>
|end_datetime_2>

|bottom_bar>
|lhs>

<|rhs|

### Product

<|{selected_product}|selector|lov={product_list}|dropdown|>

### Measure

<|{selected_measure}|selector|lov={measure_list}|>

Average contributions of features on the Product market evolution over 2 specific periods. 
Monitor market drivers on desired time windows.

|>

|>
""")

def period_comparison_on_init(state):
    ...

root_var_update_list = []
def period_comparison_on_navigate(state):
    for var_name in root_var_update_list:
        period_comparison_on_change(state, var_name, getattr(state, var_name))

def period_comparison_on_change(state, var_name, var_value):
    # root variables
    if var_name == "":
        ...

    # module variables
    elif var_name == "predictive_value_1":
        state.predictive_value_1_class = get_indicator_success_failure_class(var_value)
    elif var_name == "predictive_value_2":
        state.predictive_value_2_class = get_indicator_success_failure_class(var_value)
