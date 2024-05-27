"""
A Streamlit app to simulate venture capital investment allocation
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

EXPENSES_PERCENTAGE = 0.10
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
    "Investment Period (years)", options=[1, 2, 3, 4, 5], index=2
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

investable_capital_amount = fund_capital_committed_amount * (1 - EXPENSES_PERCENTAGE - management_fee_percentage)

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
            f"${fund_capital_committed_amount}M",
            f"${management_fee_amount}M",
            f"${-fund_capital_committed_amount*EXPENSES_PERCENTAGE:.2f}M",
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
