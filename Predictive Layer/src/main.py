from icecream import ic
import datetime as dt
from dateutil.tz import tzutc, tzlocal


def dt_prefix():
    return f"{dt.datetime.now().strftime('%H:%M:%S')} |> "


ic.configureOutput(prefix=dt_prefix, includeContext=True)
ic.lineWrapWidth = 150

from taipy.gui import Gui, Markdown, navigate, notify, Icon
import pandas as pd
from pages.market_forecast import (
    market_forecast_md,
    market_forecast_on_init,
    market_forecast_on_change,
    market_forecast_on_navigate,
)
from pages.health_indicators import (
    health_indicators_md,
    health_indicators_on_init,
    health_indicators_on_change,
    health_indicators_on_navigate,
)
from pages.detailed_hi import (
    detailed_hi_md,
    detailed_hi_on_init,
    detailed_hi_on_change,
    detailed_hi_on_navigate,
)
from pages.hi_evolution import (
    hi_evolution_md,
    hi_evolution_on_init,
    hi_evolution_on_change,
    hi_evolution_on_navigate,
)
from pages.feature_accuracies import (
    feature_accuracies_md,
    feature_accuracies_on_init,
    feature_accuracies_on_change,
    feature_accuracies_on_navigate,
)
from pages.group_contributions import (
    group_contributions_md,
    group_contributions_on_init,
    group_contributions_on_change,
    group_contributions_on_navigate,
)
from pages.feature_contributions import (
    feature_contributions_md,
    feature_contributions_on_init,
    feature_contributions_on_change,
    feature_contributions_on_navigate,
)
from pages.feature_ranking import (
    feature_ranking_md,
    feature_ranking_on_init,
    feature_ranking_on_change,
    feature_ranking_on_navigate,
)
from pages.period_comparison import (
    period_comparison_md,
    period_comparison_on_init,
    period_comparison_on_change,
    period_comparison_on_navigate,
)
from pages.model_explainability import (
    model_explainability_md,
    model_explainability_on_init,
    model_explainability_on_change,
    model_explainability_on_navigate,
)

# used in market forecast, HI and DHI
selected_datetime = dt.datetime(2023, 8, 11, tzinfo=tzutc())
valid_datetimes: list[dt.datetime] = (
    pd.date_range(
        start=dt.datetime(2023, 8, 11),
        end=dt.datetime(2023, 11, 26),
        freq="D",
        tz=tzutc(),
    )
    .to_pydatetime()
    .tolist()
)

product_list = [
    "DEBMK22",
    "DEBMM22",
    "DEBQN22",
    "DEBQV22",
    "DEBYF23",
    "FDBMK22",
    "FDBMM22",
    "FDBQN22",
    "FDBQV22",
    "FDBYF23",
    "F7BMK22",
    "F7BMM22",
    "F7BQN22",
    "F7BQV22",
    "F7BYF23",
]
selected_product = product_list[0]

root_md = Markdown(
    """
<|menu|lov={page_list}|on_action=menu_navigate|>


"""
)


def on_init(state):
    market_forecast_on_init(state)
    health_indicators_on_init(state)
    detailed_hi_on_init(state)
    hi_evolution_on_init(state)
    feature_accuracies_on_init(state)
    group_contributions_on_init(state)
    feature_contributions_on_init(state)
    feature_ranking_on_init(state)
    period_comparison_on_init(state)
    model_explainability_on_init(state)


def menu_navigate(state, var_name, var_value):
    """Any navigate logic should be in on_navigate."""

    navigate(state, var_value["args"][0])


def on_navigate(state, page_name):
    """
    NOTE: When the application first starts, Taipy calls this function with the
    root page (TaiPy_root_page) and the first page.
    """

    # This logic is in an if block because this function is also called where page_name is a partial or root page
    if page_name in list(pages.keys())[1:]:
        state.page = page_name
        ic("Navigating to", page_name)
        if page_name == "market_forecast":
            market_forecast_on_navigate(state)
        elif page_name == "health_indicators":
            health_indicators_on_navigate(state)
        elif page_name == "detailed_hi":
            detailed_hi_on_navigate(state)
        elif page_name == "hi_evolution":
            hi_evolution_on_navigate(state)
        elif page_name == "feature_accuracies":
            feature_accuracies_on_navigate(state)
        elif page_name == "group_contributions":
            group_contributions_on_navigate(state)
        elif page_name == "feature_contributions":
            feature_contributions_on_navigate(state)
        elif page_name == "feature_ranking":
            feature_ranking_on_navigate(state)
        elif page_name == "period_comparison":
            period_comparison_on_navigate(state)
        elif page_name == "model_explainability":
            model_explainability_on_navigate(state)
    return page_name


def on_change(state, var_name, var_value):
    ic(state.page, var_name, var_value)

    if var_name == "selected_datetime":
        if var_value not in valid_datetimes:
            state.selected_datetime = valid_datetimes[0]
            notify(
                state,
                "warning",
                f"Invalid date: {var_value.date()}. Resetting to {state.selected_datetime.date()}.",
            )

    if state.page == "market_forecast":
        market_forecast_on_change(state, var_name, var_value)
    elif state.page == "health_indicators":
        health_indicators_on_change(state, var_name, var_value)
    elif state.page == "detailed_hi":
        detailed_hi_on_change(state, var_name, var_value)
    elif state.page == "hi_evolution":
        hi_evolution_on_change(state, var_name, var_value)
    elif state.page == "feature_accuracies":
        feature_accuracies_on_change(state, var_name, var_value)
    elif state.page == "group_contributions":
        group_contributions_on_change(state, var_name, var_value)
    elif state.page == "feature_contributions":
        feature_contributions_on_change(state, var_name, var_value)
    elif state.page == "feature_ranking":
        feature_ranking_on_change(state, var_name, var_value)
    elif state.page == "period_comparison":
        period_comparison_on_change(state, var_name, var_value)
    elif state.page == "model_explainability":
        model_explainability_on_change(state, var_name, var_value)


pages = {
    "/": root_md,
    "market_forecast": market_forecast_md,
    "health_indicators": health_indicators_md,
    "detailed_hi": detailed_hi_md,
    "hi_evolution": hi_evolution_md,
    "feature_accuracies": feature_accuracies_md,
    "group_contributions": group_contributions_md,
    "feature_contributions": feature_contributions_md,
    "feature_ranking": feature_ranking_md,
    "period_comparison": period_comparison_md,
    "model_explainability": model_explainability_md,
}
page_list = [
    (
        "market_forecast",
        Icon("assets/images/insights_white_24dp.svg", "Market Forecast"),
    ),
    (
        "health_indicators",
        Icon("assets/images/search_white_24dp.svg", "Health Indicators"),
    ),
    (
        "detailed_hi",
        Icon("assets/images/zoom_in_white_24dp.svg", "Detailed Health Indicators"),
    ),
    ("hi_evolution", Icon("assets/images/troubleshoot_white_24dp.svg", "HI Evolution")),
    (
        "feature_accuracies",
        Icon("assets/images/track_changes_white_24dp.svg", "Feature Accuracies"),
    ),
    (
        "group_contributions",
        Icon("assets/images/group_white_24dp.svg", "Group Contributions"),
    ),
    (
        "feature_contributions",
        Icon("assets/images/hub_white_24dp.svg", "Feature Contributions"),
    ),
    (
        "feature_ranking",
        Icon("assets/images/leaderboard_white_24dp.svg", "Feature Ranking"),
    ),
    (
        "period_comparison",
        Icon("assets/images/date_range_white_24dp.svg", "Period Comparison"),
    ),
    (
        "model_explainability",
        Icon("assets/images/lightbulb_white_24dp.svg", "Model Explainability"),
    ),
]
page = page_list[0]


if __name__ == "__main__":
    stylekit = {
        "color_primary": "#347683",
        "color_secondary": "#5c6163",
    }

    gui_properties = {
        "dark_mode": False,
        "title": "Predictive Layer",
        "run_browser": False,
        "use_reloader": True,
        "stylekit": stylekit,
        "favicon": "assets/images/PredictiveLayerLogo.png",
        "time_zone": "Etc/UTC",
    }

    gui = Gui(pages=pages)
    mkt_fcst_card_partial = gui.add_partial("")
    health_indicator_card_partial = gui.add_partial("")
    detailed_hi_card_partial = gui.add_partial("")
    gui.run(**gui_properties)
