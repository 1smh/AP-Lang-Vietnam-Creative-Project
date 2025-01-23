import streamlit as st
import pandas as pd
import pydeck as pdk
import altair as alt

def load_data():
    df = pd.read_csv("data/vietnam_bombing_trimmed.csv", usecols=[
        "TGTLATDD_DDD_WGS84",
        "TGTLONDDD_DDD_WGS84",
        "NUMWEAPONSDELIVERED"
    ])

    df.dropna(subset=["TGTLATDD_DDD_WGS84", "TGTLONDDD_DDD_WGS84"], inplace=True)
    df["TGTLATDD_DDD_WGS84"] = pd.to_numeric(df["TGTLATDD_DDD_WGS84"], errors="coerce")
    df["TGTLONDDD_DDD_WGS84"] = pd.to_numeric(df["TGTLONDDD_DDD_WGS84"], errors="coerce")
    df.dropna(subset=["TGTLATDD_DDD_WGS84", "TGTLONDDD_DDD_WGS84"], inplace=True)
    df = df.iloc[::10].copy()

    return df

def main():
    st.set_page_config(page_title="Vietnam War Bombing Map", layout="wide")
    st.title("3D Visualization of Vietnam War Bombing (Stratified downsample by 50x)")

    st.markdown(""" 
    During the Vietnam War, U.S. bombing campaigns, like Operation Rolling Thunder,
    targeted regions believed to host significant enemy presence or supply lines (mainly the Ho Chi Minh Trail). 
    In contrast, remote mountainous areas with low population density often saw fewer bombing runs. 
    The visualizations below indicate the intensity and location of strikes. The topographical map 
    provides geographical context, showing how terrain influenced bombing strategies.
    """)

    # -------------------------------------------------------------
    # Side-by-Side Layout: Topographical Map and 3D Bombing Map
    # -------------------------------------------------------------
    col1, col2 = st.columns([1, 2])

    with col1:
        st.image(
            "https://preview.redd.it/4ovwkaqdqfg61.jpg?auto=webp&s=5fc960c9b4d813cceafc2a71665fe0e2b06f0dff", 
            caption="Topographical Map of Vietnam", 
            width=400
        )

    with col2:
        df = load_data()

        view_state = pdk.ViewState(
            latitude=15.0,
            longitude=105.0,
            zoom=5,
            pitch=45
        )

        hex_layer = pdk.Layer(
            "HexagonLayer",
            data=df,
            get_position='[TGTLONDDD_DDD_WGS84, TGTLATDD_DDD_WGS84]',
            radius=2000,
            elevation_scale=50,
            elevation_range=[0, 3000],
            extruded=True,
            pickable=True
        )

        deck = pdk.Deck(
            initial_view_state=view_state,
            layers=[hex_layer],
            tooltip={"text": "Weapons Delivered: {NUMWEAPONSDELIVERED}"}
        )

        st.pydeck_chart(deck)

    # --------------------------------------------------------------
    # Additional 2D Charts: Histogram and Scatter Plot
    # --------------------------------------------------------------
    st.subheader("Additional 2D Visuals")

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("**Distribution of Weapons Delivered**")
        hist_chart = (
            alt.Chart(df)
            .mark_bar()
            .encode(
                x=alt.X("NUMWEAPONSDELIVERED:Q", bin=alt.Bin(maxbins=40), title="Number of Weapons Delivered (binned)"),
                y=alt.Y("count()", title="Frequency"),
                tooltip=["count()"]
            )
            .properties(width="container", height=400)
            .interactive()
        )
        st.altair_chart(hist_chart, use_container_width=True)

    with col4:
        st.markdown("**Geographic Distribution (2D Scatter)**")
        scatter_chart = (
            alt.Chart(df.sample(n=1000, random_state=1))  # sample to avoid the site freezing (still takes like 10 seconds)
            .mark_circle(size=60, opacity=0.5)
            .encode(
                x=alt.X("TGTLONDDD_DDD_WGS84:Q", title="Longitude"),
                y=alt.Y("TGTLATDD_DDD_WGS84:Q", title="Latitude"),
                color=alt.Color("NUMWEAPONSDELIVERED:Q", scale=alt.Scale(scheme="reds"), title="Weapons Delivered"),
                tooltip=["TGTLATDD_DDD_WGS84", "TGTLONDDD_DDD_WGS84", "NUMWEAPONSDELIVERED"]
            )
            .properties(width="container", height=400)
            .interactive()
        )
        st.altair_chart(scatter_chart, use_container_width=True)

    # --------------------------------------------------------------
    # Combined Analysis Paragraph for 2D Charts
    # --------------------------------------------------------------
    st.markdown(""" 
    The histogram shows the distribution of weapons delivered per strike. It reveals that 
    most missions involved small payloads, while a smaller subset delivered large quantities. This pattern aligns with 
    the US tactical strategies: smaller strikes aimed at impeding and
    disrupting supply lines, and larger ones targeting area bombardment near key supply hubs or troop concentrations.
    """)

if __name__ == "__main__":
    main()
