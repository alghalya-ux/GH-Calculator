import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="GreenH2 Optimizer",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM DASHBOARD STYLE
# =========================================================

st.markdown(
    """
    <style>

    /* -----------------------------------------
       MAIN APP
    ----------------------------------------- */

    .stApp {
        background-color: #FFFFFF;
        color: #17211D;
    }


    /* -----------------------------------------
       MAIN CONTENT WIDTH
    ----------------------------------------- */

    .block-container {
        padding-top: 2rem;
        padding-bottom: 4rem;
        max-width: 1450px;
    }


    /* -----------------------------------------
       HEADINGS
    ----------------------------------------- */

    h1 {
        color: #123D2F;
        font-weight: 700;
        letter-spacing: -0.5px;
    }

    h2 {
        color: #123D2F;
        font-weight: 650;
        margin-top: 1.4rem;
    }

    h3 {
        color: #235D49;
        font-weight: 600;
    }


    /* -----------------------------------------
       NORMAL TEXT
    ----------------------------------------- */

    p {
        color: #58655F;
    }


    /* -----------------------------------------
       SIDEBAR
    ----------------------------------------- */

    [data-testid="stSidebar"] {
        background-color: #F7FAF8;
        border-right: 1px solid #E4ECE7;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #123D2F;
    }


    /* -----------------------------------------
       METRIC CARDS
    ----------------------------------------- */

    [data-testid="stMetric"] {
        background-color: #F8FBF9;
        border: 1px solid #E2ECE6;
        padding: 18px;
        border-radius: 14px;
    }

    [data-testid="stMetricLabel"] {
        color: #68766F;
        font-weight: 500;
    }

    [data-testid="stMetricValue"] {
        color: #136F4A;
        font-weight: 700;
    }


    /* -----------------------------------------
       INPUT BOXES
    ----------------------------------------- */

    [data-testid="stNumberInput"] input {
        border-radius: 10px;
    }

    [data-testid="stTextInput"] input {
        border-radius: 10px;
    }


    /* -----------------------------------------
       BUTTONS
    ----------------------------------------- */

    .stButton > button {
        background-color: #167D5A;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.65rem 1.4rem;
        font-weight: 600;
        transition: 0.2s;
    }

    .stButton > button:hover {
        background-color: #0D5C42;
        color: white;
        border: none;
    }


    /* -----------------------------------------
       FILE UPLOADER
    ----------------------------------------- */

    [data-testid="stFileUploader"] {
        background-color: #F8FBF9;
        border: 1px dashed #A8CABB;
        border-radius: 14px;
        padding: 12px;
    }


    /* -----------------------------------------
       SUCCESS BOXES
    ----------------------------------------- */

    [data-testid="stAlert"] {
        border-radius: 12px;
    }


    /* -----------------------------------------
       DATAFRAMES
    ----------------------------------------- */

    [data-testid="stDataFrame"] {
        border: 1px solid #E2ECE6;
        border-radius: 12px;
        overflow: hidden;
    }


    /* -----------------------------------------
       DIVIDERS
    ----------------------------------------- */

    hr {
        border-color: #E7EEE9;
        margin-top: 2.5rem;
        margin-bottom: 2.5rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        """
        ## GreenH₂ Optimizer

        **Design • Optimize • Evaluate**
        """
    )

    st.divider()

    st.caption("WORKFLOW")

    st.markdown(
        """
        **01 · Renewable Analysis**

        **02 · Electrolyzer Optimization**

        **03 · Battery Integration**

        **04 · Final System Design**
        """
    )

    st.divider()

    st.caption("ABOUT")

    st.write(
        "A green hydrogen system design and techno-economic "
        "optimization tool developed from an engineering research project."
    )


# =========================================================
# DASHBOARD HEADER
# =========================================================

st.html(
    """
    <div style="
        background: linear-gradient(
            135deg,
            #F4FAF7 0%,
            #FFFFFF 100%
        );
        border: 1px solid #E1ECE6;
        border-radius: 20px;
        padding: 34px 38px;
        margin-bottom: 25px;
    ">

        <div style="
            font-size: 13px;
            color: #167D5A;
            font-weight: 700;
            letter-spacing: 1.5px;
            margin-bottom: 8px;
        ">
            GREEN HYDROGEN SYSTEM DESIGN
        </div>

        <div style="
            font-size: 38px;
            color: #123D2F;
            font-weight: 750;
            margin-bottom: 10px;
        ">
            GreenH₂ Design Optimizer
        </div>

        <div style="
            font-size: 17px;
            color: #65736C;
            max-width: 750px;
            line-height: 1.6;
        ">
            Analyze renewable generation profiles, optimize electrolyzer
            capacity, evaluate battery integration, and assess the
            techno-economic performance of green hydrogen systems.
        </div>

</div>
"""
)


# =========================================================
# WORKFLOW STRIP
# =========================================================

step1, step2, step3, step4 = st.columns(4)

with step1:
    st.markdown(
        """
        **01**

        ### Renewables
        Upload & analyze
        """
    )

with step2:
    st.markdown(
        """
        **02**

        ### Electrolyzer
        Optimize capacity
        """
    )

with step3:
    st.markdown(
        """
        **03**

        ### Battery
        Optimize storage
        """
    )

with step4:
    st.markdown(
        """
        **04**

        ### Final Design
        Review configuration
        """
    )

st.divider()

# =========================================================
# FILE UPLOAD
# =========================================================

uploaded_file = st.file_uploader(
    "Upload Renewable Generation Excel File",
    type=["xlsx"]
)


# Everything that uses df MUST be inside this section
if uploaded_file is not None:

    # =====================================================
    # READ EXCEL FILE
    # =====================================================

    try:
        df = pd.read_excel(uploaded_file)

    except Exception as error:
        st.error(f"The Excel file could not be read: {error}")
        st.stop()

    st.success("Excel file uploaded successfully.")

    st.subheader("Detected Columns")

    st.write(df.columns.tolist())


    # =====================================================
    # CLEAN AND RENAME COLUMNS
    # =====================================================

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.replace("\xa0", "", regex=False)
    )

    df = df.rename(
        columns={
            "PV (2000 MW)": "Solar",
            "Wind MW (60MW)": "Wind",
            "Wind MW (60MW) ": "Wind",
            "Total MWh": "Total",
            "Total MWh ": "Total",
            "Total_MWh": "Total"
        }
    )


    # =====================================================
    # CHECK REQUIRED COLUMNS
    # =====================================================

    required_columns = ["Solar", "Wind", "Total"]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:

        st.error(
            "The following required columns were not found: "
            + ", ".join(missing_columns)
        )

        st.write(
            "The uploaded Excel file must contain solar, wind, "
            "and total renewable-generation columns."
        )

        st.stop()


    # =====================================================
    # CONVERT GENERATION COLUMNS TO NUMERIC
    # =====================================================

    for column in required_columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        ).fillna(0)

    df["Hour Index"] = range(len(df))


    # =====================================================
    # DATA PREVIEW
    # =====================================================

    with st.expander("Preview Uploaded Dataset"):

        st.dataframe(
            df.head(20),
            width="stretch"
        )


    # =====================================================
    # RENEWABLE RESOURCE ANALYSIS
    # =====================================================

    st.header("1. Renewable Energy Analysis")

    metric1, metric2, metric3, metric4 = st.columns(4)

    metric1.metric(
        "Maximum Generation",
        f"{df['Total'].max():,.2f} MW"
    )

    metric2.metric(
        "Minimum Generation",
        f"{df['Total'].min():,.2f} MW"
    )

    metric3.metric(
        "Average Generation",
        f"{df['Total'].mean():,.2f} MW"
    )

    metric4.metric(
        "Annual Renewable Energy",
        f"{df['Total'].sum():,.0f} MWh"
    )


    # =====================================================
    # FIGURE STYLE
    # =====================================================

    plt.rcParams.update({
        "font.size": 12,
        "axes.labelsize": 14,
        "axes.titlesize": 16,
        "legend.fontsize": 12,
        "font.weight": "bold"
    })


    # =====================================================
    # SOLAR GENERATION FIGURE
    # =====================================================

    st.subheader("Solar Generation Profile")

    fig_solar, ax_solar = plt.subplots(figsize=(16, 5))

    ax_solar.bar(
        df["Hour Index"],
        df["Solar"],
        color="orange",
        label="Solar Generation",
        width=1.0
    )

    ax_solar.set_title(
        "Solar-only Generation Profile",
        fontweight="bold"
    )

    ax_solar.set_xlabel(
        "Hour Index",
        fontweight="bold"
    )

    ax_solar.set_ylabel(
        "Solar Power (MW)",
        fontweight="bold"
    )

    ax_solar.legend()

    ax_solar.grid(
        True,
        axis="y",
        linestyle="--",
        alpha=0.7
    )

    st.pyplot(fig_solar)
    plt.close(fig_solar)


    # =====================================================
    # WIND GENERATION FIGURE
    # =====================================================

    st.subheader("Wind Generation Profile")

    fig_wind, ax_wind = plt.subplots(figsize=(16, 5))

    ax_wind.bar(
        df["Hour Index"],
        df["Wind"],
        color="#AEC6CF",
        label="Wind Generation",
        width=1.0
    )

    ax_wind.set_title(
        "Wind-only Generation Profile",
        fontweight="bold"
    )

    ax_wind.set_xlabel(
        "Hour Index",
        fontweight="bold"
    )

    ax_wind.set_ylabel(
        "Wind Power (MW)",
        fontweight="bold"
    )

    ax_wind.legend()

    ax_wind.grid(
        True,
        axis="y",
        linestyle="--",
        alpha=0.7
    )

    st.pyplot(fig_wind)
    plt.close(fig_wind)


    # =====================================================
    # COMBINED GENERATION FIGURE
    # =====================================================

    st.subheader("Combined Renewable Generation Profile")

    fig_combined, ax_combined = plt.subplots(figsize=(16, 5))

    ax_combined.bar(
        df["Hour Index"],
        df["Total"],
        color="green",
        label="Solar + Wind",
        width=1.0
    )

    ax_combined.set_title(
        "Combined Renewable Generation Profile",
        fontweight="bold"
    )

    ax_combined.set_xlabel(
        "Hour Index",
        fontweight="bold"
    )

    ax_combined.set_ylabel(
        "Total Renewable Power (MW)",
        fontweight="bold"
    )

    ax_combined.legend()

    ax_combined.grid(
        True,
        axis="y",
        linestyle="--",
        alpha=0.7
    )

    st.pyplot(fig_combined)
    plt.close(fig_combined)


    # =====================================================
    # ELECTROLYZER OPTIMIZATION
    # =====================================================

    st.divider()

    st.header("2. Electrolyzer Size Optimization")

    st.write(
        "The optimizer evaluates a range of electrolyzer capacities "
        "and recommends the capacity that produces the highest "
        "calculated annual profit."
    )

    E_h = df["Total"].to_numpy(dtype=float)
    h_h = np.ones_like(E_h, dtype=float)


    # =====================================================
    # ELECTROLYZER SIZE SETTINGS
    # =====================================================

    st.subheader("Electrolyzer Size Range")

    size_col1, size_col2, size_col3 = st.columns(3)

    with size_col1:

        minimum_size = st.number_input(
            "Minimum Electrolyzer Size (MW)",
            min_value=1,
            value=500,
            step=50,
            key="minimum_electrolyzer_size"
        )

    with size_col2:

        maximum_size = st.number_input(
            "Maximum Electrolyzer Size (MW)",
            min_value=1,
            value=1000,
            step=50,
            key="maximum_electrolyzer_size"
        )

    with size_col3:

        size_step = st.number_input(
            "Electrolyzer Size Step (MW)",
            min_value=1,
            value=50,
            step=10,
            key="electrolyzer_size_step"
        )


    # =====================================================
    # ELECTROLYZER ECONOMIC PARAMETERS
    # =====================================================

    st.subheader("Electrolyzer Economic Parameters")

    economic_col1, economic_col2, economic_col3 = st.columns(3)

    with economic_col1:

        capex_per_MW = st.number_input(
            "Electrolyzer CAPEX (OMR/MW)",
            min_value=0.0,
            value=1026230.0,
            step=10000.0,
            key="electrolyzer_capex"
        )

        opex_per_MW = st.number_input(
            "Annual Electrolyzer OPEX (OMR/MW)",
            min_value=0.0,
            value=20520.0,
            step=1000.0,
            key="electrolyzer_opex"
        )

    with economic_col2:

        electricity_price = st.number_input(
            "Electricity Price (OMR/MWh)",
            min_value=0.0,
            value=15.964,
            step=0.1,
            format="%.3f",
            key="electricity_price"
        )

        hydrogen_price = st.number_input(
            "Hydrogen Selling Price (OMR/kg)",
            min_value=0.0,
            value=2.5,
            step=0.1,
            key="hydrogen_price"
        )

    with economic_col3:

        wacc_percent = st.number_input(
            "WACC (%)",
            min_value=0.0,
            max_value=100.0,
            value=5.0,
            step=0.5,
            key="electrolyzer_wacc"
        )

        project_lifetime = st.number_input(
            "Project Lifetime (years)",
            min_value=1,
            value=25,
            step=1,
            key="electrolyzer_lifetime"
        )

    wacc = wacc_percent / 100


    # =====================================================
    # VARIABLE SEC FUNCTION
    # =====================================================

    def sec_kwh_per_kg(utilization_fraction):

        return (
            50
            + 12
            * np.maximum(
                0,
                0.7 - utilization_fraction
            ) ** 2
            + 8
            * np.maximum(
                0,
                utilization_fraction - 0.9
            ) ** 2
        )


    # =====================================================
    # ELECTROLYZER EVALUATION FUNCTION
    # =====================================================

    def evaluate_electrolyzer_size(P_el_MW):

        # Maximum energy electrolyzer can accept each hour
        E_max = P_el_MW * h_h

        E_used = np.minimum(
            E_h,
            E_max
        )

        E_excess = np.maximum(
            0,
            E_h - E_max
        )

        annual_excess_energy = E_excess.sum()

        utilization_hourly = (
            E_used
            / (E_max + 1e-9)
        )

        SEC_hourly = sec_kwh_per_kg(
            utilization_hourly
        )

        hydrogen_hourly_kg = (
            E_used
            * 1000
            / SEC_hourly
        )

        hydrogen_annual_kg = (
            hydrogen_hourly_kg.sum()
        )

        hydrogen_annual_tonnes = (
            hydrogen_annual_kg / 1000
        )

        if wacc == 0:

            capital_recovery_factor = (
                1 / project_lifetime
            )

        else:

            capital_recovery_factor = (
                wacc
                * (1 + wacc) ** project_lifetime
            ) / (
                (1 + wacc) ** project_lifetime
                - 1
            )

        annualized_capex = (
            capex_per_MW
            * P_el_MW
            * capital_recovery_factor
        )

        annual_opex = (
            opex_per_MW
            * P_el_MW
        )

        annual_electricity_cost = (
            electricity_price
            * E_used.sum()
        )

        total_annual_cost = (
            annualized_capex
            + annual_opex
            + annual_electricity_cost
        )

        if hydrogen_annual_kg > 0:

            LCOH = (
                total_annual_cost
                / hydrogen_annual_kg
            )

        else:

            LCOH = np.nan

        annual_revenue = (
            hydrogen_annual_kg
            * hydrogen_price
        )

        annual_profit = (
            annual_revenue
            - total_annual_cost
        )

        annual_utilization = (
            E_used.sum()
            / (
                P_el_MW
                * h_h.sum()
                + 1e-9
            )
        )


        return {
            "Size_MW":
                P_el_MW,

            "Hydrogen_tonnes":
                hydrogen_annual_tonnes,

            "Revenue_OMR":
                annual_revenue,

            "Annual_Cost_OMR":
                total_annual_cost,

            "Profit_OMR":
                annual_profit,

            "LCOH_OMR_per_kg":
                LCOH,

            "UF_year":
                annual_utilization,

            "Excess_MWh":
                annual_excess_energy
        }


    # =====================================================
    # RUN ELECTROLYZER OPTIMIZATION
    # =====================================================

    if st.button(
        "Optimize Electrolyzer Size",
        key="run_electrolyzer_optimization"
    ):

        if maximum_size < minimum_size:

            st.error(
                "Maximum electrolyzer size must be greater than "
                "or equal to the minimum electrolyzer size."
            )

        else:

            # Test all capacities in selected range
            tested_sizes = range(
                int(minimum_size),
                int(maximum_size) + 1,
                int(size_step)
            )

            electrolyzer_results = [
                evaluate_electrolyzer_size(size)
                for size in tested_sizes
            ]

            electrolyzer_results_df = pd.DataFrame(
                electrolyzer_results
            )

            optimal_index = (
                electrolyzer_results_df[
                    "Profit_OMR"
                ].idxmax()
            )

            optimal_electrolyzer = (
                electrolyzer_results_df.loc[
                    optimal_index
                ]
            )

            st.session_state[
                "electrolyzer_results"
            ] = electrolyzer_results_df

            st.session_state[
                "optimal_electrolyzer"
            ] = optimal_electrolyzer.to_dict()

            st.session_state[
                "optimal_electrolyzer_size"
            ] = float(
                optimal_electrolyzer["Size_MW"]
            )

            st.session_state[
                "optimal_electrolyzer_result"
            ] = optimal_electrolyzer.to_dict()

            # Old battery results are no longer valid
            # if the electrolyzer optimum changes.
            st.session_state.pop(
                "battery_results",
                None
            )

            st.session_state.pop(
                "optimal_battery",
                None
            )


    # =====================================================
    # DISPLAY ELECTROLYZER RESULTS
    # =====================================================

    if (
        "electrolyzer_results" in st.session_state
        and "optimal_electrolyzer" in st.session_state
    ):

        electrolyzer_results_df = (
            st.session_state[
                "electrolyzer_results"
            ]
        )

        optimal_electrolyzer = (
            st.session_state[
                "optimal_electrolyzer"
            ]
        )

        st.subheader(
            "Recommended Electrolyzer Size"
        )

        st.success(
            "Maximum-profit electrolyzer size: "
            f"{optimal_electrolyzer['Size_MW']:,.0f} MW"
        )

        result_col1, result_col2, result_col3 = (
            st.columns(3)
        )

        result_col1.metric(
            "Optimal Size",
            f"{optimal_electrolyzer['Size_MW']:,.0f} MW"
        )

        result_col2.metric(
            "Annual Profit",
            f"{optimal_electrolyzer['Profit_OMR']:,.0f} OMR"
        )

        result_col3.metric(
            "Annual Hydrogen Production",
            (
                f"{optimal_electrolyzer['Hydrogen_tonnes']:,.1f} "
                "tonnes/year"
            )
        )

        result_col4, result_col5, result_col6 = (
            st.columns(3)
        )

        result_col4.metric(
            "LCOH",
            (
                f"{optimal_electrolyzer['LCOH_OMR_per_kg']:.3f} "
                "OMR/kg"
            )
        )

        result_col5.metric(
            "Utilization Factor",
            (
                f"{optimal_electrolyzer['UF_year'] * 100:.2f}%"
            )
        )

        result_col6.metric(
            "Excess Renewable Energy",
            (
                f"{optimal_electrolyzer['Excess_MWh']:,.0f} MWh"
            )
        )


        # =================================================
        # ELECTROLYZER PROFIT FIGURE
        # =================================================

        st.subheader(
            "Profit vs Electrolyzer Size"
        )

        fig_profit, ax_profit = plt.subplots(
            figsize=(12, 6)
        )

        ax_profit.plot(
            electrolyzer_results_df["Size_MW"],
            electrolyzer_results_df["Profit_OMR"],
            marker="o",
            linestyle="-",
            color="teal",
            linewidth=2,
            label="Annual Profit"
        )

        ax_profit.scatter(
            optimal_electrolyzer["Size_MW"],
            optimal_electrolyzer["Profit_OMR"],
            color="red",
            s=120,
            zorder=5,
            label="Maximum Profit"
        )

        ax_profit.axvline(
            x=optimal_electrolyzer["Size_MW"],
            color="red",
            linestyle="--",
            alpha=0.7
        )

        ax_profit.annotate(
            (
                f"Optimal = "
                f"{optimal_electrolyzer['Size_MW']:,.0f} MW\n"
                f"Profit = "
                f"{optimal_electrolyzer['Profit_OMR']:,.0f} OMR"
            ),

            xy=(
                optimal_electrolyzer["Size_MW"],
                optimal_electrolyzer["Profit_OMR"]
            ),

            xytext=(15, 20),
            textcoords="offset points",
            fontweight="bold",

            arrowprops={
                "arrowstyle": "->",
                "color": "red"
            }
        )

        ax_profit.set_title(
            "Profit vs Electrolyzer Size",
            fontweight="bold"
        )

        ax_profit.set_xlabel(
            "Electrolyzer Size (MW)",
            fontweight="bold"
        )

        ax_profit.set_ylabel(
            "Annual Profit (OMR)",
            fontweight="bold"
        )

        ax_profit.grid(
            True,
            linestyle="--",
            alpha=0.7
        )

        ax_profit.legend()

        st.pyplot(fig_profit)
        plt.close(fig_profit)


        # =================================================
        # ELECTROLYZER RESULTS TABLE
        # =================================================

        st.subheader(
            "Electrolyzer Size Comparison"
        )

        electrolyzer_table = (
            electrolyzer_results_df.copy()
        )

        electrolyzer_table[
            "UF_year"
        ] = (
            electrolyzer_table["UF_year"]
            * 100
        )

        electrolyzer_table = (
            electrolyzer_table.rename(
                columns={

                    "Size_MW":
                        "Electrolyzer Size (MW)",

                    "Hydrogen_tonnes":
                        "H₂ Production (tonnes/year)",

                    "Revenue_OMR":
                        "Revenue (OMR/year)",

                    "Annual_Cost_OMR":
                        "Annual Cost (OMR/year)",

                    "Profit_OMR":
                        "Profit (OMR/year)",

                    "LCOH_OMR_per_kg":
                        "LCOH (OMR/kg)",

                    "UF_year":
                        "Utilization Factor (%)",

                    "Excess_MWh":
                        "Excess Energy (MWh)"
                }
            )
        )

        st.dataframe(
            electrolyzer_table.round(3),
            width="stretch"
        )


    # =====================================================
    # BATTERY INTEGRATION
    # =====================================================

    st.divider()

    st.header(
        "3. Battery Energy Storage Optimization"
    )

    st.write(
        "The battery module evaluates different storage capacities "
        "and identifies the tested capacity that produces the "
        "highest calculated annual profit."
    )


    if (
        "optimal_electrolyzer_size"
        not in st.session_state
    ):

        st.info(
            "Run the electrolyzer optimization first. "
            "The optimized electrolyzer size will then be "
            "transferred automatically to the battery module."
        )

    else:

        P_EL_max = float(
            st.session_state[
                "optimal_electrolyzer_size"
            ]
        )

        st.success(
            "Electrolyzer capacity used in battery analysis: "
            f"{P_EL_max:,.0f} MW"
        )


        # =================================================
        # BATTERY TECHNICAL PARAMETERS
        # =================================================

        st.subheader(
            "Battery Technical Parameters"
        )

        battery_col1, battery_col2 = (
            st.columns(2)
        )

        with battery_col1:

            P_EL_min = st.number_input(
                "Minimum Electrolyzer Load (MW)",
                min_value=0.0,
                max_value=float(P_EL_max),
                value=min(
                    60.0,
                    float(P_EL_max)
                ),
                step=10.0,
                key="battery_minimum_electrolyzer_load"
            )

            battery_SEC = st.number_input(
                "Electrolyzer SEC (kWh/kg H₂)",
                min_value=1.0,
                value=52.0,
                step=1.0,
                key="battery_sec"
            )

        with battery_col2:

            charging_efficiency_percent = (
                st.number_input(
                    "Battery Charging Efficiency (%)",
                    min_value=1.0,
                    max_value=100.0,
                    value=86.0,
                    step=1.0,
                    key="battery_charging_efficiency"
                )
            )

            discharging_efficiency_percent = (
                st.number_input(
                    "Battery Discharging Efficiency (%)",
                    min_value=1.0,
                    max_value=100.0,
                    value=86.0,
                    step=1.0,
                    key="battery_discharging_efficiency"
                )
            )


        # =================================================
        # SOC RANGE
        # =================================================

        st.write("#### Battery SOC Operating Range")

        soc_option = st.radio(
            "Select an SOC operating range",
            options=[
                "5% - 95%",
                "10% - 90%",
                "15% - 85%",
                "20% - 80%",
                "Custom"
            ],
            index=0,
            horizontal=True,
            key="battery_soc_range"
        )

        if soc_option == "5% - 95%":

            minimum_SOC_percent = 5.0
            maximum_SOC_percent = 95.0

        elif soc_option == "10% - 90%":

            minimum_SOC_percent = 10.0
            maximum_SOC_percent = 90.0

        elif soc_option == "15% - 85%":

            minimum_SOC_percent = 15.0
            maximum_SOC_percent = 85.0

        elif soc_option == "20% - 80%":

            minimum_SOC_percent = 20.0
            maximum_SOC_percent = 80.0

        else:

            soc_col1, soc_col2 = st.columns(2)

            with soc_col1:

                minimum_SOC_percent = st.number_input(
                    "Custom Minimum SOC (%)",
                    min_value=0.0,
                    max_value=99.0,
                    value=5.0,
                    step=1.0,
                    key="custom_minimum_SOC"
                )

            with soc_col2:

                maximum_SOC_percent = st.number_input(
                    "Custom Maximum SOC (%)",
                    min_value=1.0,
                    max_value=100.0,
                    value=95.0,
                    step=1.0,
                    key="custom_maximum_SOC"
                )

        st.caption(
            f"Selected SOC operating range: "
            f"{minimum_SOC_percent:.0f}% to "
            f"{maximum_SOC_percent:.0f}%"
        )

        charging_efficiency = (
            charging_efficiency_percent / 100
        )

        discharging_efficiency = (
            discharging_efficiency_percent / 100
        )

        minimum_SOC = (
            minimum_SOC_percent / 100
        )

        maximum_SOC = (
            maximum_SOC_percent / 100
        )

        interval_h = 1.0


        # =================================================
        # CANDIDATE BATTERY SIZES
        # =================================================

        st.subheader(
            "Candidate Battery Capacities"
        )

        candidate_battery_text = st.text_input(
            "Battery capacities separated by commas (MWh)",
            value=(
                "0, 500, 1000, 2000, 3000, "
                "4000, 5000, 6000, 8000"
            ),
            key="candidate_battery_sizes"
        )


        # =================================================
        # BATTERY ECONOMIC PARAMETERS
        # =================================================

        st.subheader(
            "Battery Economic Parameters"
        )

        battery_econ1, battery_econ2, battery_econ3 = (
            st.columns(3)
        )

        with battery_econ1:

            battery_hydrogen_price = st.number_input(
                "Hydrogen Price for Battery Analysis (OMR/kg)",
                min_value=0.0,
                value=2.5,
                step=0.1,
                key="battery_hydrogen_price"
            )

            usd_to_omr = st.number_input(
                "USD to OMR Conversion",
                min_value=0.0,
                value=0.38,
                step=0.01,
                format="%.3f",
                key="battery_currency_conversion"
            )

        with battery_econ2:

            battery_capex_usd_per_kWh = st.number_input(
                "Battery CAPEX (USD/kWh)",
                min_value=0.0,
                value=127.0,
                step=1.0,
                key="battery_capex"
            )

            battery_opex_percent = st.number_input(
                "Battery Annual OPEX (% of CAPEX)",
                min_value=0.0,
                max_value=100.0,
                value=2.0,
                step=0.5,
                key="battery_opex"
            )

        with battery_econ3:

            battery_lifetime = st.number_input(
                "Battery Lifetime (years)",
                min_value=1,
                value=15,
                step=1,
                key="battery_lifetime"
            )

            battery_wacc_percent = (
                st.number_input(
                    "Battery Analysis WACC (%)",
                    min_value=0.0,
                    max_value=100.0,
                    value=5.0,
                    step=0.5,
                    key="battery_wacc"
                )
            )


        # =================================================
        # ELECTROLYZER COST PARAMETERS FOR BATTERY ANALYSIS
        # =================================================

        st.subheader(
            "Electrolyzer Cost Parameters for Battery Analysis"
        )

        system_col1, system_col2, system_col3 = (
            st.columns(3)
        )

        with system_col1:

            system_capex_per_MW = st.number_input(
                "Electrolyzer CAPEX (OMR/MW)",
                min_value=0.0,
                value=1025640.0,
                step=10000.0,
                key="battery_module_electrolyzer_capex"
            )

        with system_col2:

            system_opex_per_MW = st.number_input(
                "Electrolyzer OPEX (OMR/MW/year)",
                min_value=0.0,
                value=20520.0,
                step=1000.0,
                key="battery_module_electrolyzer_opex"
            )

        with system_col3:

            system_lifetime = st.number_input(
                "Electrolyzer Lifetime (years)",
                min_value=1,
                value=25,
                step=1,
                key="battery_module_system_lifetime"
            )


        battery_cost_per_MWh = (
            battery_capex_usd_per_kWh
            * usd_to_omr
            * 1000
        )

        battery_opex_fraction = (
            battery_opex_percent / 100
        )

        battery_wacc = (
            battery_wacc_percent / 100
        )


        # =================================================
        # PREPARE RENEWABLE DATA
        # =================================================

        battery_df = df.copy()

        battery_df["P_ren"] = (
            battery_df["Total"]
            / interval_h
        )


        # =================================================
        # CAPITAL RECOVERY FACTOR
        # =================================================

        def calculate_crf(rate, years):

            if rate == 0:
                return 1 / years

            return (
                rate
                * (1 + rate) ** years
            ) / (
                (1 + rate) ** years
                - 1
            )


        battery_CRF = calculate_crf(
            battery_wacc,
            battery_lifetime
        )

        system_CRF = calculate_crf(
            battery_wacc,
            system_lifetime
        )


        # =================================================
        # BATTERY SIMULATION
        # =================================================

        def simulate_battery_with_bounds(
            data,
            Q_b
        ):

            SOC = maximum_SOC * Q_b

            hydrogen_energy_MWh = 0.0

            full_load_hours = 0
            partial_load_hours = 0
            idle_hours = 0

            SOC_history = []

            curtailed_energy_MWh = 0.0

            battery_charge_input_MWh = 0.0
            battery_discharge_MWh = 0.0


            for P_renewable in (
                data["P_ren"].to_numpy()
            ):

                P_input = min(
                    P_renewable,
                    P_EL_max
                )


                # -----------------------------------------
                # DISCHARGE TO MINIMUM LOAD
                # -----------------------------------------

                if (
                    Q_b > 0
                    and P_input < P_EL_min
                    and SOC > minimum_SOC * Q_b
                ):

                    required_electrolyzer_output = (
                        P_EL_min - P_input
                    )

                    required_battery_discharge = (
                        required_electrolyzer_output
                        / discharging_efficiency
                    )

                    available_battery_energy = max(
                        0,
                        SOC - minimum_SOC * Q_b
                    )

                    actual_battery_discharge = min(
                        required_battery_discharge,
                        available_battery_energy
                    )

                    SOC -= actual_battery_discharge

                    P_input += (
                        actual_battery_discharge
                        * discharging_efficiency
                    )

                    battery_discharge_MWh += (
                        actual_battery_discharge
                    )


                # -----------------------------------------
                # DISCHARGE TOWARD MAXIMUM LOAD
                # -----------------------------------------

                if (
                    Q_b > 0
                    and P_input < P_EL_max
                    and SOC > minimum_SOC * Q_b
                ):

                    required_electrolyzer_output = (
                        P_EL_max - P_input
                    )

                    required_battery_discharge = (
                        required_electrolyzer_output
                        / discharging_efficiency
                    )

                    available_battery_energy = max(
                        0,
                        SOC - minimum_SOC * Q_b
                    )

                    actual_battery_discharge = min(
                        required_battery_discharge,
                        available_battery_energy
                    )

                    SOC -= actual_battery_discharge

                    P_input += (
                        actual_battery_discharge
                        * discharging_efficiency
                    )

                    battery_discharge_MWh += (
                        actual_battery_discharge
                    )


                P_input = min(
                    P_input,
                    P_EL_max
                )


                # -----------------------------------------
                # CHARGE FROM RENEWABLE SURPLUS
                # -----------------------------------------

                renewable_surplus = max(
                    0,
                    P_renewable - P_input
                )

                if Q_b > 0:

                    available_storage_space = max(
                        0,
                        maximum_SOC * Q_b - SOC
                    )

                    possible_stored_energy = (
                        renewable_surplus
                        * charging_efficiency
                    )

                    actual_stored_energy = min(
                        possible_stored_energy,
                        available_storage_space
                    )

                    SOC += actual_stored_energy

                    renewable_charge_input = (
                        actual_stored_energy
                        / charging_efficiency
                    )

                    battery_charge_input_MWh += (
                        renewable_charge_input
                    )

                    curtailed_energy_MWh += max(
                        0,
                        renewable_surplus
                        - renewable_charge_input
                    )

                else:

                    curtailed_energy_MWh += (
                        renewable_surplus
                    )


                # -----------------------------------------
                # OPERATING STATUS
                # -----------------------------------------

                if P_input >= P_EL_max - 1e-9:

                    full_load_hours += 1

                elif P_input > 0:

                    partial_load_hours += 1

                else:

                    idle_hours += 1


                hydrogen_energy_MWh += (
                    P_input
                    * interval_h
                )


                if Q_b > 0:

                    SOC_history.append(
                        SOC / Q_b
                    )

                else:

                    SOC_history.append(0.0)


            hydrogen_output_kg = (
                hydrogen_energy_MWh
                * 1000
                / battery_SEC
            )


            return {
                "H2_output_kg":
                    hydrogen_output_kg,

                "Full_load_hours":
                    full_load_hours,

                "Partial_load_hours":
                    partial_load_hours,

                "Idle_hours":
                    idle_hours,

                "Average_SOC":
                    np.mean(SOC_history),

                "Curtailed_energy_MWh":
                    curtailed_energy_MWh,

                "Battery_charge_input_MWh":
                    battery_charge_input_MWh,

                "Battery_discharge_MWh":
                    battery_discharge_MWh
            }


        # =================================================
        # BATTERY ECONOMIC EVALUATION
        # =================================================

        def evaluate_battery_economics(
            battery_capacity_MWh,
            hydrogen_output_kg
        ):

            annual_revenue = (
                hydrogen_output_kg
                * battery_hydrogen_price
            )

            battery_capex = (
                battery_capacity_MWh
                * battery_cost_per_MWh
            )

            annualized_battery_capex = (
                battery_capex
                * battery_CRF
            )

            annual_battery_opex = (
                battery_opex_fraction
                * battery_capex
            )

            electrolyzer_capex = (
                system_capex_per_MW
                * P_EL_max
            )

            annualized_electrolyzer_capex = (
                electrolyzer_capex
                * system_CRF
            )

            annual_electrolyzer_opex = (
                system_opex_per_MW
                * P_EL_max
            )

            total_annual_cost = (
                annualized_electrolyzer_capex
                + annual_electrolyzer_opex
                + annualized_battery_capex
                + annual_battery_opex
            )

            annual_profit = (
                annual_revenue
                - total_annual_cost
            )

            if hydrogen_output_kg > 0:

                LCOH = (
                    total_annual_cost
                    / hydrogen_output_kg
                )

            else:

                LCOH = np.nan


            return {
                "Revenue_OMR":
                    annual_revenue,

                "Annual_Cost_OMR":
                    total_annual_cost,

                "Profit_OMR":
                    annual_profit,

                "LCOH_OMR_per_kg":
                    LCOH,

                "Battery_CAPEX_OMR":
                    battery_capex
            }


        # =================================================
        # RUN BATTERY OPTIMIZATION
        # =================================================

        if st.button(
            "Optimize Battery Capacity",
            key="run_battery_optimization"
        ):

            if minimum_SOC >= maximum_SOC:

                st.error(
                    "Maximum SOC must be greater than minimum SOC."
                )

            elif P_EL_min > P_EL_max:

                st.error(
                    "Minimum electrolyzer load cannot exceed "
                    "the electrolyzer maximum capacity."
                )

            else:

                try:

                    candidate_battery_sizes = sorted(
                        set(
                            float(value.strip())
                            for value
                            in candidate_battery_text.split(",")
                            if value.strip() != ""
                        )
                    )

                    if not candidate_battery_sizes:

                        st.error(
                            "Enter at least one battery capacity."
                        )

                    elif min(candidate_battery_sizes) < 0:

                        st.error(
                            "Battery capacities cannot be negative."
                        )

                    else:

                        battery_results = []

                        for Q_b in candidate_battery_sizes:

                            simulation = (
                                simulate_battery_with_bounds(
                                    battery_df,
                                    Q_b
                                )
                            )

                            economics = (
                                evaluate_battery_economics(
                                    Q_b,
                                    simulation[
                                        "H2_output_kg"
                                    ]
                                )
                            )

                            battery_results.append({
                                "BatterySize_MWh":
                                    Q_b,

                                "H2_output_tonnes":
                                    (
                                        simulation[
                                            "H2_output_kg"
                                        ]
                                        / 1000
                                    ),

                                "Revenue_OMR":
                                    economics[
                                        "Revenue_OMR"
                                    ],

                                "Annual_Cost_OMR":
                                    economics[
                                        "Annual_Cost_OMR"
                                    ],

                                "Profit_OMR":
                                    economics[
                                        "Profit_OMR"
                                    ],

                                "LCOH_OMR_per_kg":
                                    economics[
                                        "LCOH_OMR_per_kg"
                                    ],

                                "Full_load_hours":
                                    simulation[
                                        "Full_load_hours"
                                    ],

                                "Partial_load_hours":
                                    simulation[
                                        "Partial_load_hours"
                                    ],

                                "Idle_hours":
                                    simulation[
                                        "Idle_hours"
                                    ],

                                "Average_SOC_percent":
                                    (
                                        simulation[
                                            "Average_SOC"
                                        ]
                                        * 100
                                    ),

                                "Curtailed_energy_MWh":
                                    simulation[
                                        "Curtailed_energy_MWh"
                                    ],

                                "Battery_charge_MWh":
                                    simulation[
                                        "Battery_charge_input_MWh"
                                    ],

                                "Battery_discharge_MWh":
                                    simulation[
                                        "Battery_discharge_MWh"
                                    ]
                            })

                        battery_results_df = pd.DataFrame(
                            battery_results
                        )

                        best_battery_index = (
                            battery_results_df[
                                "Profit_OMR"
                            ].idxmax()
                        )

                        optimal_battery = (
                            battery_results_df.loc[
                                best_battery_index
                            ]
                        )

                        st.session_state[
                            "battery_results"
                        ] = battery_results_df

                        st.session_state[
                            "optimal_battery"
                        ] = optimal_battery.to_dict()

                except ValueError:

                    st.error(
                        "Enter battery capacities as numbers "
                        "separated by commas. Example: "
                        "0, 500, 1000, 2000"
                    )


        # =================================================
        # DISPLAY BATTERY RESULTS
        # =================================================

        if (
            "battery_results" in st.session_state
            and "optimal_battery" in st.session_state
        ):

            battery_results_df = (
                st.session_state[
                    "battery_results"
                ]
            )

            optimal_battery = (
                st.session_state[
                    "optimal_battery"
                ]
            )

            st.subheader(
                "Recommended Battery Capacity"
            )

            st.success(
                "Maximum-profit battery capacity: "
                f"{optimal_battery['BatterySize_MWh']:,.0f} MWh"
            )

            battery_result1, battery_result2, battery_result3 = (
                st.columns(3)
            )

            battery_result1.metric(
                "Optimal Battery Capacity",
                (
                    f"{optimal_battery['BatterySize_MWh']:,.0f} "
                    "MWh"
                )
            )

            battery_result2.metric(
                "Annual Profit",
                (
                    f"{optimal_battery['Profit_OMR']:,.0f} "
                    "OMR"
                )
            )

            battery_result3.metric(
                "Annual Hydrogen Production",
                (
                    f"{optimal_battery['H2_output_tonnes']:,.1f} "
                    "tonnes/year"
                )
            )

            battery_result4, battery_result5, battery_result6 = (
                st.columns(3)
            )

            battery_result4.metric(
                "LCOH",
                (
                    f"{optimal_battery['LCOH_OMR_per_kg']:.3f} "
                    "OMR/kg"
                )
            )

            battery_result5.metric(
                "Average Battery SOC",
                (
                    f"{optimal_battery['Average_SOC_percent']:.2f}%"
                )
            )

            battery_result6.metric(
                "Curtailed Energy",
                (
                    f"{optimal_battery['Curtailed_energy_MWh']:,.0f} "
                    "MWh"
                )
            )


            # =============================================
            # BATTERY PROFIT FIGURE
            # =============================================

            st.subheader(
                "Profit vs Battery Capacity"
            )

            fig_battery, ax_battery = plt.subplots(
                figsize=(12, 6)
            )

            ax_battery.plot(
                battery_results_df[
                    "BatterySize_MWh"
                ],
                battery_results_df[
                    "Profit_OMR"
                ],
                marker="o",
                linestyle="-",
                color="teal",
                linewidth=2,
                label="Annual Profit"
            )

            ax_battery.scatter(
                optimal_battery[
                    "BatterySize_MWh"
                ],
                optimal_battery[
                    "Profit_OMR"
                ],
                color="red",
                s=120,
                zorder=5,
                label="Maximum Profit"
            )

            ax_battery.axvline(
                x=optimal_battery[
                    "BatterySize_MWh"
                ],
                color="red",
                linestyle="--",
                alpha=0.7
            )

            ax_battery.annotate(
                (
                    f"Optimal = "
                    f"{optimal_battery['BatterySize_MWh']:,.0f} MWh\n"
                    f"Profit = "
                    f"{optimal_battery['Profit_OMR']:,.0f} OMR"
                ),

                xy=(
                    optimal_battery[
                        "BatterySize_MWh"
                    ],
                    optimal_battery[
                        "Profit_OMR"
                    ]
                ),

                xytext=(15, 20),
                textcoords="offset points",
                fontweight="bold",

                arrowprops={
                    "arrowstyle": "->",
                    "color": "red"
                }
            )

            ax_battery.set_title(
                "Profit vs Battery Capacity",
                fontweight="bold"
            )

            ax_battery.set_xlabel(
                "Battery Capacity (MWh)",
                fontweight="bold"
            )

            ax_battery.set_ylabel(
                "Annual Profit (OMR)",
                fontweight="bold"
            )

            ax_battery.grid(
                True,
                linestyle="--",
                alpha=0.7
            )

            ax_battery.legend()

            st.pyplot(fig_battery)
            plt.close(fig_battery)


            # =============================================
            # BATTERY COMPARISON TABLE
            # =============================================

            st.subheader(
                "Battery Capacity Comparison"
            )

            battery_table = (
                battery_results_df.copy()
            )

            battery_table = battery_table.rename(
                columns={
                    "BatterySize_MWh":
                        "Battery Capacity (MWh)",

                    "H2_output_tonnes":
                        "H₂ Production (tonnes/year)",

                    "Revenue_OMR":
                        "Revenue (OMR/year)",

                    "Annual_Cost_OMR":
                        "Annual Cost (OMR/year)",

                    "Profit_OMR":
                        "Profit (OMR/year)",

                    "LCOH_OMR_per_kg":
                        "LCOH (OMR/kg)",

                    "Full_load_hours":
                        "Full-Load Hours",

                    "Partial_load_hours":
                        "Partial-Load Hours",

                    "Idle_hours":
                        "Idle Hours",

                    "Average_SOC_percent":
                        "Average SOC (%)",

                    "Curtailed_energy_MWh":
                        "Curtailed Energy (MWh)",

                    "Battery_charge_MWh":
                        "Battery Charge Input (MWh)",

                    "Battery_discharge_MWh":
                        "Battery Discharge (MWh)"
                }
            )

            st.dataframe(
                battery_table.round(3),
                width="stretch"
            )


            # =================================================
            # FINAL OPTIMIZED SYSTEM SUMMARY
            # =================================================

            st.divider()

            st.header(
                "4. Final Optimized System Summary"
            )

            st.write(
                "The table below summarizes the selected renewable "
                "generation capacity and the results of the "
                "electrolyzer and battery optimization."
            )


            optimal_electrolyzer_result = (
                st.session_state[
                    "optimal_electrolyzer_result"
                ]
            )


            # =================================================
            # RENEWABLE GENERATION CAPACITY
            # =================================================

            renewable_generation_capacity = (
                st.number_input(
                    "Installed Renewable Generation Capacity (MW)",
                    min_value=0.0,
                    value=2060.0,
                    step=10.0,
                    help=(
                        "Enter the total installed solar and wind "
                        "capacity represented by the uploaded "
                        "generation profile."
                    ),
                    key="final_renewable_generation_capacity"
                )
            )


            # =================================================
            # FINAL SUMMARY TABLE
            # =================================================

            final_summary = pd.DataFrame({

                "Parameter": [
                    "Renewable Generation Capacity",
                    "Optimal Electrolyzer Capacity",
                    "Optimal Battery Capacity",
                    "Annual Hydrogen Production",
                    "Hydrogen Selling Price",
                    "LCOH",
                    "Annual Revenue",
                    "Annual System Cost",
                    "Annual Profit",
                    "Electrolyzer Utilization Factor",
                    "Battery Average SOC",
                    "Battery SOC Operating Range",
                    "Full-Load Operating Hours",
                    "Partial-Load Operating Hours",
                    "Idle Hours",
                    "Curtailed Renewable Energy"
                ],

                "Value": [
                    f"{renewable_generation_capacity:,.0f}",

                    f"{P_EL_max:,.0f}",

                    (
                        f"{optimal_battery['BatterySize_MWh']:,.0f}"
                    ),

                    (
                        f"{optimal_battery['H2_output_tonnes']:,.1f}"
                    ),

                    f"{battery_hydrogen_price:.2f}",

                    (
                        f"{optimal_battery['LCOH_OMR_per_kg']:.3f}"
                    ),

                    (
                        f"{optimal_battery['Revenue_OMR']:,.0f}"
                    ),

                    (
                        f"{optimal_battery['Annual_Cost_OMR']:,.0f}"
                    ),

                    (
                        f"{optimal_battery['Profit_OMR']:,.0f}"
                    ),

                    (
                        f"{optimal_electrolyzer_result['UF_year'] * 100:.2f}"
                    ),

                    (
                        f"{optimal_battery['Average_SOC_percent']:.2f}"
                    ),

                    (
                        f"{minimum_SOC_percent:.0f}% - "
                        f"{maximum_SOC_percent:.0f}%"
                    ),

                    (
                        f"{optimal_battery['Full_load_hours']:,.0f}"
                    ),

                    (
                        f"{optimal_battery['Partial_load_hours']:,.0f}"
                    ),

                    (
                        f"{optimal_battery['Idle_hours']:,.0f}"
                    ),

                    (
                        f"{optimal_battery['Curtailed_energy_MWh']:,.0f}"
                    )
                ],

                "Unit": [
                    "MW",
                    "MW",
                    "MWh",
                    "tonnes/year",
                    "OMR/kg H₂",
                    "OMR/kg H₂",
                    "OMR/year",
                    "OMR/year",
                    "OMR/year",
                    "%",
                    "%",
                    "",
                    "hours/year",
                    "hours/year",
                    "hours/year",
                    "MWh/year"
                ]
            })


            st.dataframe(
                final_summary,
                width="stretch",
                hide_index=True
            )


            # =================================================
            # FINAL DESIGN CARDS
            # =================================================

            st.subheader(
                "Recommended System Configuration"
            )

            summary1, summary2, summary3 = (
                st.columns(3)
            )

            with summary1:

                st.metric(
                    "Renewable Capacity",
                    (
                        f"{renewable_generation_capacity:,.0f} "
                        "MW"
                    )
                )

                st.metric(
                    "Electrolyzer",
                    f"{P_EL_max:,.0f} MW"
                )

            with summary2:

                st.metric(
                    "Battery",
                    (
                        f"{optimal_battery['BatterySize_MWh']:,.0f} "
                        "MWh"
                    )
                )

                st.metric(
                    "Hydrogen Production",
                    (
                        f"{optimal_battery['H2_output_tonnes']:,.1f} "
                        "tonnes/year"
                    )
                )

            with summary3:

                st.metric(
                    "LCOH",
                    (
                        f"{optimal_battery['LCOH_OMR_per_kg']:.3f} "
                        "OMR/kg"
                    )
                )

                st.metric(
                    "Annual Profit",
                    (
                        f"{optimal_battery['Profit_OMR']:,.0f} "
                        "OMR/year"
                    )
                )


            # =================================================
            # FINAL DESIGN STATEMENT
            # =================================================

            st.success(
                f"Recommended configuration: "
                f"{renewable_generation_capacity:,.0f} MW of "
                f"installed renewable generation capacity, a "
                f"{P_EL_max:,.0f} MW electrolyzer, and a "
                f"{optimal_battery['BatterySize_MWh']:,.0f} MWh "
                f"battery. The modeled configuration produces "
                f"approximately "
                f"{optimal_battery['H2_output_tonnes']:,.1f} "
                f"tonnes of hydrogen per year at an LCOH of "
                f"{optimal_battery['LCOH_OMR_per_kg']:.3f} "
                f"OMR/kg, with an estimated annual profit of "
                f"{optimal_battery['Profit_OMR']:,.0f} OMR/year."
            )


else:

    st.info(
        "Upload an Excel file to begin the renewable-energy analysis."
    )