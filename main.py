"""
A Streamlit app to simulate venture capital investment allocation
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

EXPENSES_PERCENTAGE = 0.08

st.set_page_config(layout="wide")
st.header("Fund Construction Simulator")

parameter_container = st.container(border=True)

col1, col2 = parameter_container.columns(2)
col3, col4 = parameter_container.columns(2)
# Input for fund capital committed, make it slider
tile1 = col1.container(height=120)
fund_capital_committed_amount = tile1.slider(
    "Fund Capital Committed ($M)", min_value=20, max_value=100, value=75, step=5
)
# Investment Period in years (1 to 5), use a drop down
tile2 = col2.container(height=120)
fund_expense_percentage = (
    tile2.slider(
        "Annual Fund Expense(%)", min_value=0.4, max_value=1.2, value=0.6, step=0.1
    )
    / 10
)
# Management Fee in percentage, use a slider
tile3 = col3.container(height=120)
management_fee_percentage = (
    tile3.slider(
        "Annual Management Fee (%)", min_value=1.0, max_value=3.0, value=2.0, step=0.5
    )
    / 10
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

## use plotly to draw a waterfall chart of the investable capital
st.subheader("Investable Capital Waterfall")
fig_allocation_pie = go.Figure(
    go.Waterfall(
        name="",
        orientation="v",
        measure=["relative", "relative", "relative", "total"],
        x=["Committed", "Management Fee", "Fund Expenses", "Investable Capital"],
        textposition="inside",
        text=[
            f"${fund_capital_committed_amount:.2f}M",
            f"${management_fee_amount:.2f}M",
            f"${fund_capital_committed_amount*fund_expense_percentage:.2f}M",
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
st.plotly_chart(fig_allocation_pie)

# Create a editable round profile
# References:
# 1. https://info.carta.com/rs/214-BTD-103/images/Q1%202024%20State%20of%20Private%20Markets%20Industry%20Addendum.pdf
# 2. https://carta.com/blog/state-of-pre-seed-q1-2024/
# 3. https://carta.com/blog/state-of-private-markets-q1-2024/
# 4. https://info.carta.com/rs/214-BTD-103/images/Carta%20State%20of%20Pre-Seed%2C%20Q1%202024%20%281%29.pdf?version=0
# 5. https://jamesin.substack.com/p/a-deep-dive-into-q3-2023s-funding

st.subheader("Round Profile Settings")
st.markdown(
    """
    Edit the round profile settings to be used in the simulation.

    *Default settings are based on the industry average from Q1 2024. Data sources: [Carta](https://carta.com/) and [NVCA](https://nvca.org/)*.
    """
)
round_profile_df = pd.DataFrame(
    {
        "Round": [
            "Pre-Seed",
            "Seed",
            "Series A",
        ],
        "Pre-Money Val.": [10_500_000, 16_000_000, 40_000_000],
        "Post-Money Val.": [12_000_000, 20_000_000, 50_000_000],
        "Opetion Pool(%)": [10, 10, 10],
        # YC has a 40% companies ascended to Series A
        "Ascension Rate(%)": [60, 40, 20],
        "Exit Rate(%)": [1, 2, 5],
        "Years to Ascension": [1.5, 1.5, 1.5],
        "Years to Exit": [1.5, 1.5, 1.5],
        "Exit Val.": [15_000_000, 40_000_000, 100_000_000],
    }
)

edit_round_profile_df = st.data_editor(round_profile_df, hide_index=True)
avg_post_money_pre_seed = edit_round_profile_df["Post-Money Val."][0]
avg_post_money_seed = edit_round_profile_df["Post-Money Val."][1]
avg_post_money_series_a = edit_round_profile_df["Post-Money Val."][2]

# Create a 2 row 3 column layout to let user input the fund allocation, number of deals, and avg check size
st.subheader("Fund Allocation Settings")
st.markdown(
    """
    Edit the fund allocation settings to be used in the simulation.
    """
)

parameter_container = st.container(border=True)

col_pre_seed, col_seed, col_series_a = parameter_container.columns(3)

tile_pre_seed = col_pre_seed.container()
tile_seed = col_seed.container()
tile_series_a = col_series_a.container()

# Pre-Seed
deals_pre_seed = tile_pre_seed.slider(
    "Number of Deals (Pre-Seed)", min_value=10, max_value=50, value=30, step=1
)
avg_check_pre_seed = tile_pre_seed.slider(
    "Avg. Check Size (Pre-Seed)",
    min_value=250_000,
    max_value=1_500_000,
    value=750_000,
    step=50_000,
)

# Seed
deals_seed = tile_seed.slider(
    "Number of Deals (Seed)", min_value=5, max_value=20, value=10, step=1
)
avg_check_seed = tile_seed.slider(
    "Avg. Check Size (Seed)",
    min_value=500_000,
    max_value=2_500_000,
    value=1_500_000,
    step=100_000,
)

# Series A
deals_series_a = tile_series_a.slider(
    "Number of Deals (Series A)", min_value=0, max_value=10, value=2, step=1
)
avg_check_series_a = tile_series_a.slider(
    "Avg. Check Size (Series A)",
    min_value=1_000_000,
    max_value=5_000_000,
    value=3_000_000,
    step=1_000_000,
)


st.subheader("Initial Investment Allocation")
# Show the round allocation chart based on the input
round_params_df = (
    pd.DataFrame(
        {
            "Round": ["Pre-Seed", "Seed", "Series A"],
            "Deals": [deals_pre_seed, deals_seed, deals_series_a],
            "Avg. Check": [avg_check_pre_seed, avg_check_seed, avg_check_series_a],
            "Initial Ownership(%)": [
                avg_check_pre_seed / avg_post_money_pre_seed * 100,
                avg_check_seed / avg_post_money_seed * 100,
                avg_check_series_a / avg_post_money_series_a * 100,
            ],
            "Total Investment($M)": [
                deals_pre_seed * avg_check_pre_seed / 1_000_000,
                deals_seed * avg_check_seed / 1_000_000,
                deals_series_a * avg_check_series_a / 1_000_000,
            ],
        }
    )
    .join(
        edit_round_profile_df.set_index("Round"),
        on="Round",
    )
    .assign(
        **{
            "Investable Capital Allocated(%)": lambda x: (
                x["Total Investment($M)"] / investable_capital_amount * 100
            ).round(2),
            "Initial Ownership(%)": lambda x: x["Initial Ownership(%)"].round(2),
            "Ascended Deals": lambda x: (
                x["Deals"] * x["Ascension Rate(%)"] / 100
            ).round(0),
            "Exited Deals": lambda x: (x["Deals"] * x["Exit Rate(%)"] / 100).round(0),
        }
    )
)

# Append a subtotal row
round_params_with_total_df = pd.concat(
    [
        round_params_df,
        pd.DataFrame(
            [
                {
                    "Round": "Total",
                    "Deals": round_params_df["Deals"].sum(),
                    "Avg. Check": (
                        round_params_df["Total Investment($M)"].sum()
                        / round_params_df["Deals"].sum()
                        * 1_000_000
                    ).round(0),
                    "Initial Ownership(%)": None,
                    "Total Investment($M)": round_params_df[
                        "Total Investment($M)"
                    ].sum(),
                    "Investable Capital Allocated(%)": round_params_df[
                        "Investable Capital Allocated(%)"
                    ].sum(),
                    "Ascended Deals": round_params_df["Ascended Deals"].sum(),
                    "Exited Deals": round_params_df["Exited Deals"].sum(),
                }
            ]
        ),
    ],
    ignore_index=True,
)

edit_round_params_df = st.data_editor(
    round_params_with_total_df.drop(
        columns=[
            "Pre-Money Val.",
            "Post-Money Val.",
            "Opetion Pool(%)",
            "Years to Ascension",
            "Years to Exit",
            "Exit Val.",
            "Ascension Rate(%)",
            "Exit Rate(%)",
        ]
    ),
    hide_index=True,
    disabled=[
        "Total Investment($M)",
        "Initial Ownership(%)",
        "Allocation fo Investable Capital(%)",
    ],
)



# Create a input chart to put down deals to invest in each of the rounds and average check size
col_round_params, col_vis = st.columns([0.5, 0.5])
tile_round_params = col_round_params.container(border=True)
tile_vis = col_vis.container(border=True)


# Create a chart to visualize the fund allocation
fig_allocation_pie = go.Figure()
fig_allocation_pie.add_trace(
    # use a pie chart
    go.Pie(
        labels=round_params_df["Round"],
        values=round_params_df["Deals"],
        hole=0.3,
        name="Deals",
        marker_colors=["#FFA07A", "#FFD700", "#FF6347"],
    )
)
# Add a title to the fig
fig_allocation_pie.update_layout(title_text="Number of Deals Allocated")

fig_allocation_pie.update_layout(barmode="group")
tile_round_params.plotly_chart(fig_allocation_pie, theme=None)

# Create a chart to visualize the investment amount
fig_allocation_bar = go.Figure()
fig_allocation_bar.add_trace(
    # use a bar chart, to show total investment for each round
    # Each bar shows the total investment amount
    go.Bar(
        x=round_params_df["Round"],
        y=round_params_df["Deals"] * edit_round_params_df["Avg. Check"],
        name="Investment",
        marker_color="RoyalBlue",
    )
)
# add total investment amount on each bar, in the middle of the bar
for i, value in enumerate(
    edit_round_params_df["Deals"] * edit_round_params_df["Avg. Check"]
):
    fig_allocation_bar.add_annotation(
        x=edit_round_params_df["Round"][i],
        y=value / 2,
        text=f"${value/1_000_000:.2f}M",
        showarrow=False,
        font=dict(size=12, color = "#242526"),
    )

fig_allocation_bar.update_layout(title_text="Capital Allocated for initial Investment")
fig_allocation_bar.update_layout(barmode="group")
tile_vis.plotly_chart(fig_allocation_bar, theme=None)


st.subheader("Follow-on Investment Allocation")
st.markdown(
    f"After initial investment, :green[{100 - round_params_df['Investable Capital Allocated(%)'].sum():.2f}%] of capital reamins for follow-on investments."
)

 
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
