from string import Template
from taipy.gui import Markdown
from icecream import ic
import dataclasses
import numpy as np
from pages.utils import multiline_lstrip, pdct_pos_clrmap

@dataclasses.dataclass
class DetailedHi:
    product_name: str
    indicators: list[tuple[str, str, str]]  # (name, value, position)
    footer: list[tuple[str, str, str]]  # (name, value, position)


dhi_list = [
    DetailedHi(
        product_name="DEBMK22", 
        indicators=[
            ("AV_CHI2", "1.30", "Safe"),
            ("AV_CHI2_PCA80", "1.17", "Safe"),
            ("AV_CHI2_PCA95", "1.70", "Volatile"),
            ("AV_CHI2W", "1.28", "Safe"),
        ],
        footer=[("AV_OOR", "1.06%", "Safe"),]
    ),
    DetailedHi(
        product_name="DEBMM22", 
        indicators=[
            ("AV_CHI2", "1.29", "Safe"),
            ("AV_CHI2_PCA80", "1.17", "Safe"),
            ("AV_CHI2_PCA95", "1.70", "Volatile"),
            ("AV_CHI2W", "1.27", "Safe"),
        ],
        footer=[("AV_OOR", "1.09%", "Safe"),]
    ),
    DetailedHi(
        product_name="DEBQN22", 
        indicators=[
            ("AV_CHI2", "1.26", "Safe"),
            ("AV_CHI2_PCA80", "1.13", "Safe"),
            ("AV_CHI2_PCA95", "1.65", "Volatile"),
            ("AV_CHI2W", "1.23", "Safe"),
        ],
        footer=[("AV_OOR", "1.04%", "Safe"),]
    ),
    DetailedHi(
        product_name="DEBQV22", 
        indicators=[
            ("AV_CHI2", "1.24", "Safe"),
            ("AV_CHI2_PCA80", "1.12", "Safe"),
            ("AV_CHI2_PCA95", "1.63", "Volatile"),
            ("AV_CHI2W", "1.21", "Safe"),
        ],
        footer=[("AV_OOR", "1.04%", "Safe"),]
    ),
    DetailedHi(
        product_name="DEBYF23", 
        indicators=[
            ("AV_CHI2", "1.31", "Safe"),
            ("AV_CHI2_PCA80", "1.15", "Safe"),
            ("AV_CHI2_PCA95", "1.62", "Volatile"),
            ("AV_CHI2W", "1.28", "Safe"),
        ],
        footer=[("AV_OOR", "1.04%", "Safe"),]
    ),
]


def _create_dhi_card_1col(content: list[DetailedHi]) -> str:
    """Creates 1 column of the market forecast card."""
    name, value, position = (1,2, 'Safe')

    card_template = Template(
    """
    <|card card-bg m1 p2 h5|

    **$product_name**{: .h2}

    ---------------

    $body

    ---------------

    $footer

    |>
    """)

    card_mds = []
    for detailed_hi in content:
        body_mds = []
        for name, value, position in detailed_hi.indicators:
            indicator_class = pdct_pos_clrmap[position]
            body_mds.append(f"\n{name} **{value}**{{: .floatright .{indicator_class}}}\n")
        
        footer_mds = []
        for name, value, position in detailed_hi.footer:
            indicator_class = pdct_pos_clrmap[position]
            footer_mds.append(f"\n{name} **{value}**{{: .floatright .{indicator_class}}}\n")
        
        _card_md = card_template.substitute(
            product_name=detailed_hi.product_name,
            body="\n".join(body_mds), 
            footer="\n".join(footer_mds)
        )
        card_mds.append(_card_md)
    return "\n".join(card_mds)


def create_whole_dhi_card(content: list[DetailedHi], n_cols: int) -> str:
    """Create card md.

    Args
    ----
    content : list[DetailedHI]
    n_cols : int
        Number of columns
    """

    assert len(content) > n_cols

    mds = []
    for part_content in np.array_split(content, n_cols):
        _md = f"""
        <|part|

        {_create_dhi_card_1col(part_content)}

        |>
        """
        mds.append(_md)

    md = multiline_lstrip(f"<|layout|columns={'1 ' * n_cols}|\n" + "\n".join(mds) + "\n|>")

    return md


country_list = ["DE", "F7", "FD"]
selected_country = country_list[0]

detailed_hi_template = Template(
"""
# Health Indicators

<|layout|columns=3 1|

<|part|partial={detailed_hi_card_partial}|>

<|part|

<|h5|
**Safe condition**{: .indicator-success}

**Volatile condition**{: .indicator-warning}

**Abnormal condition**{: .indicator-failure}
|>

<|rhs|

### Country

<|{selected_country}|selector|lov={country_list}|>

### Date

<|{selected_datetime}|date|>

|>

|>

|>

""")

detailed_hi_md = Markdown(detailed_hi_template.substitute())


def detailed_hi_on_init(state):
    state.detailed_hi_card_partial.update_content(state, create_whole_dhi_card(content=dhi_list, n_cols=3))

root_var_update_list = ["selected_datetime"]
def detailed_hi_on_navigate(state):
    for var_name in root_var_update_list:
        detailed_hi_on_change(state, var_name, getattr(state, var_name))

def detailed_hi_on_change(state, var_name, var_value):
    # root variables
    ...

    # module variables
    ...
