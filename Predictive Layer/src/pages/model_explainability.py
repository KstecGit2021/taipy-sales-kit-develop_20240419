import itertools
import random
from taipy.gui import Markdown
from icecream import ic
import pandas as pd
import numpy as np
import datetime as dt
from dateutil.tz import tzutc

from .utils import PRIMARY_COLOR

feature_group_list = [
    "API2", "API2_DYN", "COAL_FLOW", "COAL_FLOW_DYN", "CRUDE_FLOW", "CRUDE_FLOW_DYN", "CRUDE_OFFSHORE_STORAGE", 
    "CRUDE_OFFSHORE_STORAGE_DYN", "CSPI", "CSPI_DYN", "DA", "EUA",
]
suffix_list = ["E_AS_D1", "E_AS_D2", "E_AS_D1_FRACDIFF_dmin20_E10", "E_AS_D2_FRACDIFF_dmin20_E10"]
contribution_dct = {grp: [f"{grp}_{suffix}" for suffix in suffix_list] for grp in feature_group_list}

selected_feature_group = "CRUDE_FLOW"
contribution_list = contribution_dct[selected_feature_group]
selected_contribution = f"{selected_feature_group}_{suffix_list[0]}"

full_contribution_list = list(itertools.chain.from_iterable(contribution_dct.values()))
df = pd.concat([pd.DataFrame({
    "Contribution": contribution,
    "Feature Value": np.random.randint(low=0, high=1_000_000, size=len(full_contribution_list)),
    "Contribution Value": np.random.random(size=len(full_contribution_list)), 
    "Status": np.random.choice(["Successful", "Missed"], len(full_contribution_list)),
}) for contribution in full_contribution_list], axis=0)
df = df.pivot_table(index=["Contribution", "Feature Value"], columns="Status").reset_index().droplevel(0, axis=1)
df.columns = ["Contribution", "Feature Value", *df.columns[2:]]

def create_chart_properties():
    properties = {
        "height": "65vh",
        "y[1]": "Successful",
        "y[2]": "Missed",
        "marker[1]": dict(color="DodgerBlue", size=12),
        "marker[2]": dict(color="LightCoral", size=12),
        "layout": {
            "yaxis": dict(title=dict(text="Contribution Value")),
            "title": dict(text=f"Feature rules", font=dict(size=20, color=PRIMARY_COLOR)),
        },
    }
    return properties

start_datetime = dt.datetime(2023, 8, 1, tzinfo=tzutc())
end_datetime = dt.datetime(2023, 8, 31, tzinfo=tzutc())

selected_feature_filter_pair = [10, 20]

model_explainability_md = Markdown(
"""
# Contribution - <|{selected_contribution}|text|raw|>

<|layout|columns=3 1|

<lhs|

<|{df[df.Contribution == selected_contribution]}|chart|mode=markers|rebuild|x=Feature Value|properties={create_chart_properties()}|>

<br/>

Historical scatter plot of an input data/feature contribution. X-axis: value of the data/feature. Y-axis: forecast contribution.

**Successful**{: style='color: DodgerBlue'} / **Missed**{: style='color: LightCoral'}
{: .h5}

|lhs>

<rhs|

### Product

<|{selected_product}|selector|lov={product_list}|dropdown|>

### Date

<|{start_datetime}|date|>

<|{end_datetime}|date|>

### Group Contribution

<|{selected_feature_group}|selector|lov={feature_group_list}|dropdown|>

### Contribution

<|{selected_contribution}|selector|lov={contribution_list}|dropdown|>

### Feature Filter

<|{selected_feature_filter_pair}|slider|continuous=False|> <|{str(selected_feature_filter_pair)}|>

|rhs>

|>
""")

def model_explainability_on_init(state):
    ...

root_var_update_list = []
def model_explainability_on_navigate(state):
    for var_name in root_var_update_list:
        model_explainability_on_change(state, var_name, getattr(state, var_name))

def model_explainability_on_change(state, var_name, var_value):
    # root variables
    if var_name == "":
        ...

    # module variables
    elif var_name == "selected_feature_group":
        state.contribution_list = contribution_dct[var_value]
        state.selected_contribution = state.contribution_list[0]
