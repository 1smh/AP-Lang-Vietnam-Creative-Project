import streamlit as st
import pandas as pd
import altair as alt

def main():
    st.set_page_config(page_title="Vietnam War", layout="wide")
    st.title("Weapon Comparisons")

    # ============================================================
    # SECTION 1: ARTILLERY - 105mm HOWITZER vs. 122mm D-74
    # ============================================================
    st.header("Artillery Comparison")

    artillery_data = {
        "Spec": [
            "Mass (kg)",
            "Barrel Length (m)",
            "Muzzle Velocity (m/s)",
            "Rate of Fire (rpm)",
            "Max Range (m)",
        ],
        "105mm Howitzer": [2260, 2.31, 472, 6, 11270],
        "122mm D-74": [5620, 6.45, 885, 9, 24000],
    }
    artillery_df = pd.DataFrame(artillery_data)
    melted_artillery = artillery_df.melt("Spec", var_name="Artillery", value_name="Value")

    col1, col2 = st.columns(2)

    with col1:
        bar_chart_artillery = (
            alt.Chart(melted_artillery, title="Specifications (Grouped Bar)")
            .mark_bar()
            .encode(
                x=alt.X("Spec:N", sort=None, title="Specification"),
                xOffset="Artillery:N",
                y=alt.Y("Value:Q", title="Measured Value", stack=None),
                color=alt.Color("Artillery:N", scale=alt.Scale(scheme="tableau10")),
                tooltip=["Artillery", "Spec", "Value"],
            )
            .properties(width="container", height=300)
        )
        st.altair_chart(bar_chart_artillery, use_container_width=True)

    with col2:
        artillery_bubble_df = pd.DataFrame(
            [
                {
                    "Name": "105mm Howitzer",
                    "BarrelLength": 2.31,
                    "MuzzleVelocity": 472,
                    "Mass": 2260,
                    "MaxRange": 11270,
                },
                {
                    "Name": "122mm D-74",
                    "BarrelLength": 6.45,
                    "MuzzleVelocity": 885,
                    "Mass": 5620,
                    "MaxRange": 24000,
                },
            ]
        )

        bubble_artillery_chart = (
            alt.Chart(artillery_bubble_df, title="Barrel Length vs. Muzzle Velocity")
            .mark_circle()
            .encode(
                x=alt.X("BarrelLength:Q", title="Barrel Length (m)"),
                y=alt.Y("MuzzleVelocity:Q", title="Muzzle Velocity (m/s)"),
                size=alt.Size("Mass:Q", scale=alt.Scale(range=[100, 2000]), title="Mass (kg)"),
                color=alt.Color("Name:N", legend=alt.Legend(title="Artillery Type")),
                tooltip=["Name", "BarrelLength", "MuzzleVelocity", "Mass", "MaxRange"],
            )
            .properties(width="container", height=300)
        )
        st.altair_chart(bubble_artillery_chart, use_container_width=True)

    st.markdown(
        """ 
        The **105mm Howitzer** was used mainly by the US and South Vietnamese forces. 
        It provided a dynamic artillery solution for smaller-scale battles 
        and quick deployment. During key operations like Operation Junction City or 
        the Tet Offensive, the lighter mass of the weapon allowed it 
        to be quickly airlifted or transported by truck into remote firebases. 
        Its moderate muzzle velocity and range were generally sufficient enough for these local missions.

        On the other hand, the **122mm D-74** was employed by North Vietnam forces. 
        Heavier and with a much longer barrel, the D-74 had nearly 
        double the firing range (up to 24 km) and a higher muzzle velocity. These traits 
        proved useful for the North's strategy of long-range bombardment, specifically 
        along the Ho Chi Minh Trail supply network. Despite needing a higher 
        towing capacity and setup time, these guns were extremely powerful and often 
        forced U.S. or South Vietnam units to spread out defensive perimeters or conduct lengthy search-and-destroy 
        operations. As the conflict escalated, the D-74's extended range and tough shells enabled the North to strike strategic targets 
        with less risk of immediate retaliation.
        """
    )

    # ============================================================
    # SECTION 2: MACHINE GUNS - M60 vs. DP 7.62mm
    # ============================================================
    st.header("Machine Gun Comparison")

    mg_data = {
        "Spec": ["Rate of Fire (rpm)", "Effective Range (m)", "Weight (kg)"],
        "M60": [550, 1800, 10],
        "DP 7.62mm": [550, 1100, 8],
    }
    mg_df = pd.DataFrame(mg_data)
    melted_mg = mg_df.melt("Spec", var_name="MachineGun", value_name="Value")

    col3, col4 = st.columns(2)

    with col3:
        mg_bar_chart = (
            alt.Chart(melted_mg, title="MG Specifications")
            .mark_bar()
            .encode(
                x=alt.X("Spec:N", sort=None, title="Specification"),
                xOffset="MachineGun:N",
                y=alt.Y("Value:Q", title="Measured Value", stack=None),
                color=alt.Color("MachineGun:N", scale=alt.Scale(scheme="set1")),
                tooltip=["MachineGun", "Spec", "Value"],
            )
            .properties(width="container", height=300)
        )
        st.altair_chart(mg_bar_chart, use_container_width=True)

    # with col4:
    #     usage_data = pd.DataFrame(
    #         {
    #             "Year": [1965, 1966, 1967, 1968, 1969, 1970],
    #             "M60_in_service": [1000, 5000, 9000, 15000, 18000, 20000],
    #             "DP_in_service": [2000, 7000, 12000, 16000, 19000, 21000],
    #         }
    #     )
    #     mg_melted = usage_data.melt("Year", var_name="MachineGun", value_name="Units")

    #     mg_line_chart = (
    #         alt.Chart(mg_melted, title="Estimated MGs in Service Over Time")
    #         .mark_line(point=True)
    #         .encode(
    #             x=alt.X("Year:O", title="Year"),
    #             y=alt.Y("Units:Q", title="No. of Guns in Service"),
    #             color=alt.Color("MachineGun:N", scale=alt.Scale(scheme="category20b")),
    #             tooltip=["Year:O", "MachineGun:N", "Units:Q"],
    #         )
    #         .properties(width="container", height=300)
    #     )
    #     st.altair_chart(mg_line_chart, use_container_width=True)

    st.markdown(
        """
        Used mainly by US and South Vietnamese forces, the **M60** machine gun was excellent at 
        sustained direct-fire support thanks to an innovative belt-fed design and a range 
        of about 1,800 meters. In ambushes along the Ho Chi Minh Trail, the M60’s suppressive fire could scare enemy 
        advances. However, its heavy ammunition belts sometimes slowed down units in jungle patrols.

        In contrast, the **DP 7.62mm** was a Soviet-based gun used a lot by the North Vietnamese forces and the
        Viet Cong. It matched the M60’s rate of fire and also weighed slightly less. 
        This lighter overall load made mobility easier in the thick vegetation. Over the mid-to-late 1960s, both sides 
        scaled up their machine gun deployments. While the M60’s longer range 
        offered an advantage in open terrain, the DP’s reliability and lighter weight 
        was better for hit-and-run tactics in dense jungles or tunnel systems, which was important becuase 
        of the North's dependence on guerilla warfare.
        """
    )

    # ============================================================
    # SECTION 3: RIFLES - M16 vs. AK-47
    # ============================================================
    st.header("Infantry Rifles Comparison")

    rifle_data = {
        "Spec": ["Rate of Fire (rpm)", "Effective Range (m)", "Weight (kg)", "Muzzle Velocity (m/s)"],
        "M16": [800, 500, 3.4, 948],
        "AK-47": [600, 400, 4.3, 715],
    }
    rifle_df = pd.DataFrame(rifle_data)
    melted_rifle = rifle_df.melt("Spec", var_name="Rifle", value_name="Value")

    col5, col6 = st.columns(2)

    with col5:
        rifle_bar_chart = (
            alt.Chart(melted_rifle, title="Rifle Specifications")
            .mark_bar()
            .encode(
                x=alt.X("Spec:N", sort=None, title="Specification"),
                xOffset="Rifle:N",
                y=alt.Y("Value:Q", title="Measured Value", stack=None),
                color=alt.Color("Rifle:N", scale=alt.Scale(scheme="accent")),
                tooltip=["Rifle", "Spec", "Value"],
            )
            .properties(width="container", height=300)
        )
        st.altair_chart(rifle_bar_chart, use_container_width=True)

    # with col6:
    #     distribution_data = pd.DataFrame(
    #         {
    #             "Rifle": ["M16", "AK-47"],
    #             "Count_in_1968": [150000, 220000],
    #         }
    #     )

    #     rifle_pie_chart = (
    #         alt.Chart(distribution_data, title="Field Distribution (1968)")
    #         .mark_arc()
    #         .encode(
    #             theta=alt.Theta(field="Count_in_1968", type="quantitative"),
    #             color=alt.Color(
    #                 field="Rifle",
    #                 type="nominal",
    #                 scale=alt.Scale(scheme="pastel2"),
    #                 legend=alt.Legend(title="Rifle"),
    #             ),
    #             tooltip=["Rifle", "Count_in_1968"],
    #         )
    #         .properties(width="container", height=300)
    #     )
    #     st.altair_chart(rifle_pie_chart, use_container_width=True)

    # -- Analysis paragraph
    st.markdown(
        """  
        For U.S. and Southern forces, the **M16** rifle’s high rate of fire and 
        lighter weight helped form a more agile search-and-destroy 
        strategy. In large operations, the M16s allowed quick follow up shots and easier ammo transport, despite 
        initial reliability issues when it was first introduced.

        The **AK-47** on the other hand, employed by the Northern forces, fired heavier rounds. Known for its ability to function under waterlogged 
        conditions, it aligned perfectly with guerilla strategies, especially in the VC tunnel systems. 
        By 1968, both rifles were widespread. While the M16’s fast velocity (948 m/s) gave 
        better midrange accuracy, the AK-47’s lower muzzle velocity (715 m/s) still delivered 
        a strong stopping power. This difference in design highlights the prioritization of modernization versus mass producible reliability.
        """
    )

    # try and find data for gun counts

if __name__ == "__main__":
    main()
