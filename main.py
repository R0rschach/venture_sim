"""
A Streamlit app to simulate venture capital investment allocation
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

EXPENSES_PERCENTAGE = 0.10

st.set_page_config(layout="wide")
st.header("VC Fund Construction Simulator")

parameter_container = st.container(border=True)

col1, col2 = parameter_container.columns(2)
col3, col4 = parameter_container.columns(2)
# Input for fund capital committed, make it slider
tile1 = col1.container(height=120)
fund_capital_committed_amount = tile1.slider(
    "Fund Capital Committed ($M)", min_value=20, max_value=100, value=50, step=5
)
# Investment Period in years (1 to 5), use a drop down
tile2 = col2.container(height=120)
investment_period_years = tile2.selectbox(
    "Investment Period (Years)", options=[1, 2, 3, 4, 5], index=2
)
# Management Fee in percentage, use a slider
tile3 = col3.container(height=120)
management_fee_percentage = (
    tile3.slider("Management Fee (%)", min_value=10, max_value=25, value=20, step=1)
    / 100
)
management_fee_amount = management_fee_percentage * fund_capital_committed_amount
# Carry in percentage, use a slider
tile4 = col4.container(height=120)
carry = (
    tile4.slider("Carry (%)", min_value=10.0, max_value=30.0, value=20.0, step=1.0)
    / 100
)

investable_capital_amount = fund_capital_committed_amount * (
    1 - EXPENSES_PERCENTAGE - management_fee_percentage
)

## use plotly to draw a waterfall cahrt of the investable capital
st.subheader("Investable Capital Waterfall")
fig = go.Figure(
    go.Waterfall(
        name="",
        orientation="v",
        measure=["relative", "relative", "relative", "total"],
        x=["Committed", "Management Fee", "Fund Expenses", "Investable Capital"],
        textposition="inside",
        text=[
            f"${fund_capital_committed_amount:.2f}M",
            f"${management_fee_amount:.2f}M",
            f"${fund_capital_committed_amount*EXPENSES_PERCENTAGE:.2f}M",
            f"${investable_capital_amount:.2f}M",
        ],
        y=[
            fund_capital_committed_amount,
            -management_fee_amount,
            -fund_capital_committed_amount * EXPENSES_PERCENTAGE,
            investable_capital_amount,
        ],
        increasing={"marker": {"color": "RoyalBlue"}},
        decreasing={"marker": {"color": "RoyalBlue"}},
        totals={"marker": {"color": "green"}},
    )
)
st.plotly_chart(fig)

# Create a editable round profile
# References:
# 1. https://info.carta.com/rs/214-BTD-103/images/Q1%202024%20State%20of%20Private%20Markets%20Industry%20Addendum.pdf
# 2. https://carta.com/blog/state-of-pre-seed-q1-2024/
# 3. https://carta.com/blog/state-of-private-markets-q1-2024/
# 4. https://info.carta.com/rs/214-BTD-103/images/Carta%20State%20of%20Pre-Seed%2C%20Q1%202024%20%281%29.pdf?version=0

round_profile_df = pd.DataFrame(
    {
        "Round": [
            "Pre-Seed",
            "Seed",
            "Series A",
        ],
        "Pre-Money Val.": [1_500_000, 16_000_000, 40_000_000],
        "Post-Money Val.": [12_000_000, 20_000_000, 50_000_000],
        "Opetion Pool(%)": [10, 10, 10],
        "Ascension Rate(%)": [70, 50, 50],
        "Exit Rate(%)": [1, 2, 5],
        "Years to Ascension": [1.5, 1.5, 1.5],
        "Years to Exit": [1.5, 1.5, 1.5],
        "Exit Val.": [15_000_000, 40_000_000, 100_000_000],
    }
)

edit_round_profile_df = st.data_editor(round_profile_df)


# Create a input chart to put down deals to invest in each of the rounds and average check size
col_round_params, col_vis = st.columns([0.4, 0.6])
tile_round_params = col_round_params.container(border=True)
tile_vis = col_vis.container(border=True    )

round_params_df = pd.DataFrame({
    "Round": ["Pre-Seed", "Seed", "Series A"],
    "Deals": [30, 20, 10],
    "Avg. Check": [750_000, 1_500_000, 3_000_000]
})

edit_round_params_df = tile_round_params.data_editor(round_params_df)

# Create a chart to visualize the fund allocation
fig = go.Figure()
fig.add_trace(
    # use a pie chart
    go.Pie(
        labels=edit_round_params_df["Round"],
        values=edit_round_params_df["Deals"],
        hole=0.3,
        name="Deals",
        marker_colors=["#FFA07A", "#FFD700", "#FF6347"],
    )
)

fig.update_layout(barmode="group")
tile_round_params.plotly_chart(fig)

# Create a chart to visualize the investment amount
fig = go.Figure()
fig.add_trace(
    # use a bar chart, to show total investment for each round
    # Each bar shows the total investment amount
    go.Bar(
        x=edit_round_params_df["Round"],
        y=edit_round_params_df["Deals"] * edit_round_params_df["Avg. Check"],
        name="Investment",
        marker_color="RoyalBlue",
    )
)
# add total investment amount on each bar, in the middle of the bar
for i, value in enumerate(edit_round_params_df["Deals"] * edit_round_params_df["Avg. Check"]):
    fig.add_annotation(
        x=edit_round_params_df["Round"][i],
        y=value/2,
        text=f"${value/1_000_000:.2f}M",
        showarrow=False,
        font=dict(size=12),
    )


fig.update_layout(barmode="group")
tile_vis.plotly_chart(fig)


# Create a input chart to put fund construction parameters: Fund Size, Investment Period, Management Fee, Carry

# meta_parameters_df = pd.DataFrame(
#     [
#         {"Parameter": "Fund Size ($M)", "Value": 50_000_000},
#         {"Parameter": "Investment Period (years)", "Value": 5},
#         {"Parameter": "Management Fee (%)", "Value": 2.0},
#         {"Parameter": "Carry (%)", "Value": 20.0},
#     ]
# )

# edit_meta_parameters_df = st.data_editor(meta_parameters_df)

# fund_size = edit_meta_parameters_df[
#     edit_meta_parameters_df["Parameter"] == "Fund Size ($M)"
# ]["Value"].values[0]
# investment_period_years = edit_meta_parameters_df[
#     edit_meta_parameters_df["Parameter"] == "Investment Period (years)"
# ]["Value"].values[0]
# management_fee_percentage = edit_meta_parameters_df[
#     edit_meta_parameters_df["Parameter"] == "Management Fee (%)"
# ]["Value"].values[0]
# carry = edit_meta_parameters_df[edit_meta_parameters_df["Parameter"] == "Carry (%)"][
#     "Value"
# ].values[0]
