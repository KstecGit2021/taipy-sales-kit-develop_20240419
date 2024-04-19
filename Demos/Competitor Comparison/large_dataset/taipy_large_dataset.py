from taipy.gui import Gui
from taipy.gui.data.decimator import MinMaxDecimator
from math import cos, exp
import pandas as pd

n_out = 500
decimator_instance = MinMaxDecimator(n_out=n_out)

values = 1000
decay = 0.01

data = [cos(i / 6000) * exp(-i * decay / 600) for i in range(1000000)]
data = pd.DataFrame({"x": range(len(data)), "y": data})

page = """
# 1M Points Data in **Taipy**{: .color-primary}
## Number of points:
<|{values}|slider|min=1000|max=1000000|>
<|{compute_data(values)}|chart|decimator=decimator_instance|x=x|y=y|>
"""


def compute_data(values: int) -> pd.DataFrame:
    return data.iloc[:values]


Gui(page).run(use_reloader=True, port=5015)
