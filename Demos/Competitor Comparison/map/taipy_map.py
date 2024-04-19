from taipy import Gui
import pandas as pd
import numpy as np

values = 50

initial_data = pd.DataFrame(
    np.random.randn(100, 2) / [50, 50] + [37.76, -122.4], columns=["lat", "lon"]
)

df = initial_data[:values]


def update_map(state):
    state.df = initial_data[: state.values]


layout_map = {
    "mapbox": {
        "style": "open-street-map",
        "center": {"lat": 37.76, "lon": -122.4},
        "zoom": 11,
    },
    "margin": {"l": 0, "r": 0, "b": 0, "t": 0},
}

marker_map = {"size": 12, "color": "red", "opacity": 0.5}

page = """
# In **Taipy**{: .color-primary}

<|{values}|slider|min=0|max=100|on_change=update_map|>

<|{df}|chart|type=scattermapbox|lat=lat|lon=lon|layout={layout_map}|mode=markers|marker={marker_map}|>
"""

Gui(page).run(dark_mode=False, port=5015)
