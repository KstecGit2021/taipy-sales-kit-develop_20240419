from string import Template
from taipy.gui import Markdown, navigate
from icecream import ic
import numpy as np
import pandas as pd
from .utils import PRIMARY_COLOR, get_indicator_success_failure_class

df = pd.DataFrame({
    "Group": ["FUND_CORRELATION", "WEATHER_CLOUD", "API2", "OIL", "CRUDE_FLOW", "CRUDE_FLOW_DYN", "CSPI", "WEATHER_WIND", "OTHERS", "DA", "COAL_FLOW", "POWER_Y", "TTF", "LNG_STORAGE", "EUA_DYN", "POWER_FWC", "WEATHER_TEMP", "LNG_FLOW", "API2_DYN", "CSPI_DYN", "POWER_M", "POWER_TA", "TTF_DYN", ],
})
df["Value"] = np.random.uniform(low=-1, high=1, size=len(df))
df["Measure"] = ["relative" for _ in range(len(df))]
df["Absolute Value"] = df["Value"].abs()
df["Positive"] = df.Value > 0
df = df.sort_values(by=["Positive", "Value", "Absolute Value"], ascending=[False, True, True]).reset_index(drop=True)

current_price = 103.35
realised_price_change = 0.98
current_price_class = ""
realised_price_change_class = get_indicator_success_failure_class(realised_price_change)


# ai prediction
def get_proba_class(proba):
    if proba > 50:
        return "indicator-success"
    elif proba < 50:
        return "indicator-failure"
    else:
        return ""
long_proba = 46
short_proba = 54
long_proba_class = get_proba_class(long_proba)
short_proba_class = get_proba_class(short_proba)

# total contribution
total_contribution = -0.14
total_contribution_class = get_indicator_success_failure_class(total_contribution)

success_filtering_list = ["All features", "Successful features last 3 months"]
selected_success_filtering = success_filtering_list[0]

measure_list = ["Absolute", "Relative"]
selected_measure = measure_list[0]

grp_ctrb_card = """
<|layout|columns=30rem 30rem|

<market_info|card card-bg m1 p1 h5|

<|text-center|
MARKET INFORMATION
|>

--------------------

<|layout|columns=1 1|

<|text-center|
<|Current Price|text|raw=True|class_name=color-primary|>

<|{current_price} €|text|raw=True|class_name={current_price_class} h2|>
|>

<|text-center|
<|Realised Price Change|text|raw=True|class_name=color-primary|>

<|{realised_price_change} €|text|raw=True|class_name={realised_price_change_class} h2|>
|>

|>

|market_info>

<ai_prediction|card card-bg m1 p1 h5|

<|text-center|
AI PREDICTION
|>

--------------------

<|layout|columns=1 1|

<|text-center|
<|Long Proba|text|raw=True|class_name=color-primary|>

<|{long_proba} %|text|raw=True|class_name={long_proba_class} h2|>
|>

<|text-center|
<|Short Proba|text|raw=True|class_name=color-primary|>

<|{short_proba} %|text|raw=True|class_name={short_proba_class} h2|>
|>

|>

|ai_prediction>

|>
"""

waterfall_options = {
    "decreasing": {"marker" : {"color": "red"}},
    "increasing": {"marker" : {"color": "green"}},
    "texttemplate": "%{delta:.3f}",
    "textposition": "outside",
}

waterfall_config = {
    "displayModeBar": False,
    # "responsive": True,
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

selected_trace = []

group_contributions_template = Template(
"""
# Group Contributions
<top_bar|layout|columns=1 4 1|

<|part|><|part|>

<|m-auto|
$grp_ctrb_card
|>

<|part|

|>

|top_bar>

<charts|layout|columns=1 4 1|

<|{df[df["Value"] > 0]}|chart|type=treemap|labels=Group|values=Value|layout={treemap_layout_positive}|plot_config={treemap_config}|options={treemap_options_positive}|>

<|{df}|chart|type=waterfall|x=Group|y=Value|measure=Measure|layout={waterfall_layout}|plot_config={waterfall_config}|options={waterfall_options}|on_change=chart_on_change|selected={selected_trace}|>

<|{df[df["Value"] < 0]}|chart|type=treemap|labels=Group|values=Absolute Value|layout={treemap_layout_negative}|plot_config={treemap_config}|options={treemap_options_negative}|>

|charts>

<br/>

<bottom_bar|layout|columns=2 1 1 1 1 1|

<legend|part|
Daily forecasts contributions of all the input data/features, aggregated by groups

**Positive = bullish**{: .indicator-success}

**Negative = bearish**{: .indicator-failure}
|legend>

<total_contribution|h5 text-center|
**Total Contribution**{: .color-primary}

<|{total_contribution}|text|raw=True|class_name={total_contribution_class} h2|>
|total_contribution>

<success_filtering|h5|
**Success Filtering**{: .color-primary}

<|{selected_success_filtering}|selector|lov={success_filtering_list}|dropdown|>
|success_filtering>

<date_selector|h5|
**Date:**{: .color-primary} 

<|{selected_datetime}|date|>
|date_selector>

<product_selector|h5|
**Product:**{: .color-primary}
<|{selected_product}|selector|lov={product_list}|dropdown|>
|product_selector>

<measure_selector|h5|
**Measure:**{: .color-primary}
<|{selected_measure}|selector|lov={measure_list}|>
|measure_selector>

|bottom_bar>
""")


def chart_on_change(state):
    state["feature_contributions"].selected_group = state.df.loc[state.selected_trace[0], 'Group']
    state.selected_trace = []
    navigate(state, "feature_contributions")


group_contributions_md = Markdown(group_contributions_template.substitute(grp_ctrb_card=grp_ctrb_card))

def group_contributions_on_init(state):
    ...

root_var_update_list = ["selected_datetime", "selected_product",]
def group_contributions_on_navigate(state):
    for var_name in root_var_update_list:
        group_contributions_on_change(state, var_name, getattr(state, var_name))

def group_contributions_on_change(state, var_name, var_value):
    # root variables
    if var_name == "":
        ...

    # module variables
    elif var_name == "realised_price_change":
        state.realised_price_change_class = get_indicator_success_failure_class(var_value)
    elif var_name == "long_proba":
        state.long_proba_class = get_proba_class(var_value)
    elif var_name == "short_proba":
        state.short_proba_class = get_proba_class(var_value)
