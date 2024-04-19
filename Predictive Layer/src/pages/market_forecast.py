from taipy.gui import Markdown
from string import Template
from icecream import ic
import numpy as np

from pages.utils import multiline_lstrip


product_list = [
    "DEBMK22 53.77% Short",
    "DEBMM22 52.91% Short",
    "DEBQN22 51.35% Short",
    "DEBQV22 50.86% Long",
    "DEBYF23 55.07% Long",
    "FDBMK22 53.77% Short",
    "FDBMM22 52.80% Short",
    "FDBQN22 51.69% Short",
    "FDBQN22 51.69% Short",
    "FDBYF23 53.74% Long",
    "F7BMK22 54.37% Short",
    "F7BMM22 53.82% Short",
    "F7BQN22 52.10% Short",
    "F7BQN22 52.10% Short",
    "F7BYF23 53.34% Long",
]

product_names, product_values, product_positions = list(zip(*list(map(str.split, product_list))))
product_values = list(map(lambda s: s.replace("%", ""), product_values))


def _create_mkt_fcst_card_1col(content: list[tuple[str, str, str]]) -> str:
    """Creates 1 column of the market forecast card."""

    mds = []
    for name, value, position in content:
        indicator_class = 'indicator-success' if position == "Long" else 'indicator-failure'
        _md = f"""
        <|card card-bg m1 p2 h5|
        
        {name} **{value}% {position}**{{: .floatright .{indicator_class}}}
        
        |>
        """
        mds.append(_md)
    return "\n".join(mds)

def create_whole_mkt_fcst_card(content: list[tuple[str, str, str]], n_cols: int) -> str:
    """Create card md.

    Args
    ----
    content : list[tuple[str, str, str]]
        List of tuple content. E.g. ("DEBMK22", "53.77", "Short"). 
        The value of the triples correspond to the product name, value and position (short/long).
    n_cols : int
        Number of columns
    """
    assert len(content) > n_cols

    mds = []
    for part_content in np.array_split(content, n_cols):
        _md = f"""
        <|part|

        {_create_mkt_fcst_card_1col(part_content)}

        |>
        """
        mds.append(_md)

    md = multiline_lstrip(f"<|layout|columns={'1 ' * n_cols}|\n" + "\n".join(mds) + "\n|>")

    return md


market_forecast_template = Template(
"""
# Market Forecast

<|layout|columns=3 1|

<|part|partial={mkt_fcst_card_partial}|>

<|rhs|

### Date

<|{selected_datetime}|date|>

|>

|>

""")

market_forecast_md = Markdown(market_forecast_template.substitute())

def market_forecast_on_init(state):
    state.mkt_fcst_card_partial.update_content(state, create_whole_mkt_fcst_card(content=list(zip(product_names, product_values, product_positions)), n_cols=3))

root_var_update_list = ["selected_datetime"]
def market_forecast_on_navigate(state):
    for var_name in root_var_update_list:
        market_forecast_on_change(state, var_name, getattr(state, var_name))

def market_forecast_on_change(state, var_name, var_value):
    # root variables
    ...

    # module variables
    ...
