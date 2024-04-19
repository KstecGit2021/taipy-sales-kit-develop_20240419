from string import Template
import taipy as tp
import pandas as pd
import random, textwrap
import numpy as np
import datetime as dt

PRIMARY_COLOR = "#347683"

pdct_pos_clrmap = {
    "Volatile": "indicator-warning",
    "Safe": "indicator-success",
    "Abnormal": "indicator-failure",
}

def multiline_lstrip(string: str) -> str:
    return "\n".join(map(str.lstrip, string.split("\n")))


def positive_negative_cell_style(state, value, index, row, column_name,) -> str:
    """Passed to the style property of Taipy tables."""

    value = float(value)
    if value > 0:
        return "green-bg"
    elif value < 0:
        return "red-bg"
    else:
        return ""


def positive_negative_cell_style_0_1(state, value, index, row, column_name,) -> str:
    """Passed to the style property of Taipy tables."""

    value = float(value)
    if value > 0.5:
        return "green-bg"
    else:
        return "red-bg"


def get_indicator_success_failure_class(value):
    if value > 0:
        return "indicator-success"
    elif value < 0:
        return "indicator-failure"
    else:
        return ""
