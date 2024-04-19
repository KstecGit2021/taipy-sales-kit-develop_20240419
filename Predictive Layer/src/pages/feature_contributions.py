from taipy.gui import Markdown
from icecream import ic
import pandas as pd
import numpy as np

from .utils import PRIMARY_COLOR, get_indicator_success_failure_class

group_list = ["OIL", "FUND_CORRELATION", "WEATHER_CLOUD", "API2", "CRUDE_FLOW", "CRUDE_FLOW_DYN", "CSPI", "WEATHER_WIND", "OTHERS", "DA", "COAL_FLOW", "POWER_Y", "TTF", "LNG_STORAGE", "EUA_DYN", "POWER_FWC", "WEATHER_TEMP", "LNG_FLOW", "API2_DYN", "CSPI_DYN", "POWER_M", "POWER_TA", "TTF_DYN", ]
group_and_feature_list = [(grp, f"{grp}_{i}") for grp in group_list for i in range(15)]
df = pd.DataFrame(data=group_and_feature_list, columns=["Group", "Feature"])
df["Value"] = np.random.uniform(low=-1, high=1, size=len(df))
df["Measure"] = ["relative" for _ in range(len(df))]
df["Absolute Value"] = df["Value"].abs()
df["Positive"] = df.Value > 0
df = df.sort_values(by=["Group", "Positive", "Value", "Absolute Value"], ascending=[True, False, True, True]).reset_index(drop=True)

selected_group = group_list[0]

def create_feature_df(df: pd.DataFrame, group):
    return df[df["Group"] == group]

feature_df = create_feature_df(df, selected_group)

group_contribution = -0.08
group_contribution_class = get_indicator_success_failure_class(group_contribution)

waterfall_options = {
    "decreasing": {"marker" : {"color": "red"}},
    "increasing": {"marker" : {"color": "green"}},
    "texttemplate": "%{delta:.3f}",
    "textposition": "outside",
}
waterfall_config = {
    "displayModeBar": False,
}
waterfall_layout = {
    "xaxis": {"fixedrange": True},
    "yaxis": {"fixedrange": True},
    "title": dict(text="Waterfall Contributions", font=dict(size=20, color=PRIMARY_COLOR)),
}

treemap_options_positive = dict(
    texttemplate="%{label}<br>%{value:.3f}",
    hoverinfo="label+value"
)
treemap_options_negative = dict(
    texttemplate="%{label}<br>-%{value:.3f}",
    # "extra" tags are used to hide the secondary box
    # https://plotly.com/javascript/reference/#treemap-hovertemplate
    hovertemplate="%{label}<br>-%{value}<extra></extra>"
)
treemap_config = {"displayModeBar": False}
treemap_layout_base = {"margin": dict(t=50, l=0, r=0, b=0)}
treemap_layout_positive = dict(treemap_layout_base, title=dict(text="Positive Contributions", font=dict(size=20, color="Green")))
treemap_layout_negative = dict(treemap_layout_base, title=dict(text="Negative Contributions", font=dict(size=20, color="Red")))

feature_contributions_md = Markdown(
"""
# Feature Contributions

<charts|layout|columns=1 5 1|

<|{feature_df[feature_df["Value"] > 0]}|chart|type=treemap|labels=Feature|values=Value|layout={treemap_layout_positive}|plot_config={treemap_config}|options={treemap_options_positive}|>

<|{feature_df}|chart|type=waterfall|x=Feature|y=Value|measure=Measure|layout={waterfall_layout}|plot_config={waterfall_config}|options={waterfall_options}|>

<|{feature_df[feature_df["Value"] < 0]}|chart|type=treemap|labels=Feature|values=Absolute Value|layout={treemap_layout_negative}|plot_config={treemap_config}|options={treemap_options_negative}|>

|charts>

<br/>

<bottom_bar|layout|columns=2 1 1 1 1|

<legend|part|
Daily forecasts contributions of all the input data/features, in a selected group

**Positive = bullish**{: .indicator-success}

**Negative = bearish**{: .indicator-failure}
|legend>

<group_contribution|h5 text-center|
**Group Contribution**{: .color-primary}

<|{group_contribution}|text|raw=True|class_name={group_contribution_class} h2|>
|group_contribution>

<date_selector|h5|
**Date:**{: .color-primary}

<|{selected_datetime}|date|>
|date_selector>

<product_selector|h5|
**Product:**{: .color-primary}

<|{selected_product}|selector|lov={product_list}|dropdown|>
|product_selector>

<feature_group_selector|h5|
**Features group:**{: .color-primary}

<|{selected_group}|selector|lov={group_list}|dropdown|>
|feature_group_selector>

|bottom_bar>

""")

def feature_contributions_on_init(state):
    ...

root_var_update_list = ["selected_datetime", "selected_product",]
# "selected_group" may be modified by group_contributions_on_navigate
root_var_update_list.append("selected_group")
def feature_contributions_on_navigate(state):
    for var_name in root_var_update_list:
        feature_contributions_on_change(state, var_name, getattr(state, var_name))

def feature_contributions_on_change(state, var_name, var_value):
    # root variables
    if var_name == "":
        ...

    # module variables
    elif var_name == "selected_group":
        state.feature_df = create_feature_df(df, var_value)
