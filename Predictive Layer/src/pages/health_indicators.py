from string import Template
from taipy.gui import Markdown
from icecream import ic
import numpy as np
from pages.utils import multiline_lstrip, pdct_pos_clrmap


product_list = [
    "DEBMK22 1.70 Volatile",
    "DEBMM22 1.70 Volatile",
    "DEBQN22 1.65 Volatile",
    "DEBQV22 1.63 Volatile",
    "DEBYF23 1.62 Volatile",
    "FDBMK22 1.64 Volatile",
    "FDBMM22 1.64 Volatile",
    "FDBQN22 1.65 Volatile",
    "FDBQV22 1.63 Volatile",
    "FDBYF23 1.29 Safe",
    "F7BMK22 1.65 Volatile",
    "F7BMM22 1.63 Volatile",
    "F7BQN22 1.62 Volatile",
    "F7BQV22 1.55 Volatile",
    "F7BYF23 1.26 Safe",
]
product_names, product_values, product_positions = list(zip(*list(map(str.split, product_list))))

def _create_hlth_idctr_card_1col(content: list[tuple[str, str, str]]) -> str:
    """Creates 1 column of the health indicators card."""

    mds = []
    for name, value, position in content:
        indicator_class = pdct_pos_clrmap[position]
        _md = f"""
        <|card card-bg m1 p2 h5|

        {name} **{value}**{{: .floatright .{indicator_class}}}

        |>
        """
        mds.append(_md)
    return "\n".join(mds)


def create_whole_hlth_idctr_card(content: list[tuple[str, str, str]], n_cols: int) -> str:
    """Create card md.

    Args
    ----
    content : list[tuple[str, str, str]]
        List of tuple content. E.g. ("DEBMK22", "1.70", "Volatile"). 
        The value of the triples correspond to the product name, value and position (Safe/Volatile/Abnormal).
    n_cols : int
        Number of columns
    """

    assert len(content) > n_cols

    mds = []
    for part_content in np.array_split(content, n_cols):
        _md = f"""
        <|part|

        {_create_hlth_idctr_card_1col(part_content)}

        |>
        """
        mds.append(_md)

    md = multiline_lstrip(f"<|layout|columns={'1 ' * n_cols}|\n" + "\n".join(mds) + "\n|>")

    return md


health_indicators_template = Template(
"""
# Health Indicators

<|layout|columns=3 1|

<|part|partial={health_indicator_card_partial}|>

<|rhs|

### Date

<|{selected_datetime}|date|>

|>

|>

<|h5|
**Safe condition**{: .indicator-success}

**Volatile condition**{: .indicator-warning}

**Abnormal condition**{: .indicator-failure}
|>

""")

health_indicators_md = Markdown(health_indicators_template.substitute())

def health_indicators_on_init(state):
    state.health_indicator_card_partial.update_content(state, create_whole_hlth_idctr_card(content=list(zip(product_names, product_values, product_positions)), n_cols=3))

root_var_update_list = ["selected_datetime"]
def health_indicators_on_navigate(state):
    for var_name in root_var_update_list:
        health_indicators_on_change(state, var_name, getattr(state, var_name))

def health_indicators_on_change(state, var_name, var_value):
    # root variables
    ...

    # module variables
    ...
