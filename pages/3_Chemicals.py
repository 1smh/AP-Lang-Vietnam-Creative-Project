import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

def main():
    st.set_page_config(
        page_title="Chemical Agents in Vietnam",
        layout="wide"
    )
    st.title("Chemical Agents Used in the Vietnam War")

    st.markdown("""
    Tactical herbicides were used by the U.S. to strip away dense foliage that provided cover for enemy forces. 
    Below are visual representations of their usage, contamination levels, 
    and timelines.
    """)

    # ---------------------------------------------------------------------
    # DATA SETUP FROM THE TABLE (3-1), FOCUSING ON USAGE & TCDD CONTAMINATION
    # ---------------------------------------------------------------------
    data = [
        {
            "Name": "Agent Green",
            "Formulation": "2,4,5-T",
            "AmountSprayedLiters": 75920,
            "PeriodStart": 1962,
            "PeriodEnd": 1964,
            "TCDDppmMin": 65.6,
            "TCDDppmMax": 65.6
        },
        {
            "Name": "Agent Pink",
            "Formulation": "2,4,5-T",
            "AmountSprayedLiters": 273520,
            "PeriodStart": 1962,
            "PeriodEnd": 1964,
            "TCDDppmMin": 65.6,
            "TCDDppmMax": 65.6
        },
        {
            "Name": "Agent Purple",
            "Formulation": "2,4-D, 2,4,5-T",
            "AmountSprayedLiters": 2594800,
            "PeriodStart": 1962,
            "PeriodEnd": 1964,
            "TCDDppmMin": 0,
            "TCDDppmMax": 45
        },
        {
            "Name": "Agent Blue",
            "Formulation": "Cacodylic acid, sodium cacodylate",
            "AmountSprayedLiters": 6100640,
            "PeriodStart": 1962,
            "PeriodEnd": 1971,
            "TCDDppmMin": 0,
            "TCDDppmMax": 0
        },
        {
            "Name": "Agent Orange",
            "Formulation": "2,4-D (50%), 2,4,5-T (50%)",
            "AmountSprayedLiters": 43332640,
            "PeriodStart": 1965,
            "PeriodEnd": 1970,
            "TCDDppmMin": 0.05,
            "TCDDppmMax": 50
        },
        {
            "Name": "Agent White",
            "Formulation": "2,4-D (39.6%), picloram (10.2%)",
            "AmountSprayedLiters": 21798400,
            "PeriodStart": 1965,
            "PeriodEnd": 1971,
            "TCDDppmMin": 0,
            "TCDDppmMax": 0
        },
    ]
    df = pd.DataFrame(data)

    # --------------------------------------------------------------
    # 1) BAR CHART & PIE CHART SIDE-BY-SIDE
    # --------------------------------------------------------------
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Herbicide Usage (Liters)")
        bar_chart = (
            alt.Chart(df, title="Total Liters Sprayed by Herbicide")
            .mark_bar()
            .encode(
                x=alt.X("Name:N", sort=None, title="Herbicide"),
                y=alt.Y("AmountSprayedLiters:Q", title="Liters Sprayed"),
                color=alt.Color("Name:N", scale=alt.Scale(scheme="dark2")),
                tooltip=["Name", "AmountSprayedLiters"]
            )
            .properties(width="container", height=400)
        )
        st.altair_chart(bar_chart, use_container_width=True)

    with col2:
        st.subheader("Proportion of Total Spray")
        total_sum = df["AmountSprayedLiters"].sum()
        df_pie = df.copy()
        df_pie["PercentOfTotal"] = round(
            (df_pie["AmountSprayedLiters"] / total_sum) * 100, 2
        )

        fig_pie = px.pie(
            df_pie,
            names="Name",
            values="AmountSprayedLiters",
            title="Proportional Distribution of Sprayed Herbicides",
            hover_data=["PercentOfTotal"],
            color_discrete_sequence=px.colors.qualitative.Dark2
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("""
    The bar chart shows that **Agent Orange** accounted for the 
    vast majority of sprayed herbicide volume. Much of this occurred during **Operation Ranch Hand** (1962–1971), 
    a large scale defoliation effort that targetted the Ho Chi Minh Trail and other 
    dense regions suspected of harboring Viet Cong or North Vietnamese forces. 
    Even though lesser known agents like **Green, Pink, and Purple** were used in 
    earlier years, these contributed smaller amounts overall.
    """)

    # --------------------------------------------------------------
    # 2) BUBBLE CHART: TCDD RANGES VS. VOLUME
    # --------------------------------------------------------------
    st.subheader("TCDD Contamination vs. Amount Sprayed")

    df_bubble = df.copy()
    df_bubble["TCDDppmAvg"] = (df_bubble["TCDDppmMin"] + df_bubble["TCDDppmMax"]) / 2

    fig_bubble = px.scatter(
        df_bubble,
        x="TCDDppmAvg",
        y="AmountSprayedLiters",
        size="AmountSprayedLiters",
        color="Name",
        hover_name="Name",
        hover_data={
            "TCDDppmAvg": True,
            "AmountSprayedLiters": True,
            "Formulation": True
        },
        labels={
            "TCDDppmAvg": "Avg TCDD (ppm)",
            "AmountSprayedLiters": "Liters Sprayed"
        },
        title="TCDD Contamination vs. Total Herbicide Usage",
        size_max=60,
        color_discrete_sequence=px.colors.qualitative.Dark2,
    )
    st.plotly_chart(fig_bubble, use_container_width=True)

    st.markdown(""" 
    The bubble chart combines TCDD concentration with total spray volume. 
    Although Agent Orange sometimes contained lower or moderate TCDD 
    concentrations (relative to extremes in Agent Purple or Pink), its massive 
    deployment resulted in widespread dioxin spread. Contrastingly, Agents Blue 
    and White lacked TCDD contamination but still had significant ecological 
    impact (killing crops and other vegetation critical to local 
    ecosystems). Over the conflict’s peak years (1965–1968), large scale 
    spraying ensured broad geographic dispersion of these chemicals.
    """)

    # --------------------------------------------------------------
    # 3) GANTT-STYLE BAR CHART: PERIOD OF USE
    # --------------------------------------------------------------
    st.subheader("Periods of Use")

    df_gantt = df[["Name", "PeriodStart", "PeriodEnd"]].copy()

    gantt_chart = (
        alt.Chart(df_gantt, title="Timeline of Herbicide Usage")
        .mark_bar()
        .encode(
            y=alt.Y("Name:N", sort=None, title="Herbicide"),
            x=alt.X("PeriodStart:O", title="Start Year"),
            x2="PeriodEnd:O",
            color=alt.Color("Name:N", scale=alt.Scale(scheme="dark2"), legend=None),
            tooltip=["Name", "PeriodStart", "PeriodEnd"]
        )
        .properties(width="container", height=300)
    )
    st.altair_chart(gantt_chart, use_container_width=True)

    st.markdown(""" 
    This chart shows each agent's primary usage window. 
    Agents Green, Pink, and Purple appeared briefly from 1962–1964, 
    which were likely early test phases. By 1965, larger scale adoption of 
    Agent Orange and Agent White began, matching the escalation of 
    US involvement under President Johnson. Meanwhile, Agent Blue 
    stretched from 1962 through 1971, as its targeted effect on food crops 
    (specifically rice) remained crucial to starving opposition forces. 
    Together, these timelines show how defoliation and crop destruction 
    strategies changed throughout the war, demonstrating the heavy reliance 
    on Agent Orange before its discontinuation in 1970.
    """)

if __name__ == "__main__":
    main()
