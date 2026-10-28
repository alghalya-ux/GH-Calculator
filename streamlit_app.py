import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# =========================
# PAGE TITLE
# =========================

st.title("Green Hydrogen Design Optimizer")

st.write(
    "Upload your renewable generation Excel file to analyze "
    "solar, wind, and combined generation."
)


# =========================
# FILE UPLOAD
# =========================

uploaded_file = st.file_uploader(
    "Upload Renewable Generation Excel File",
    type=["xlsx"]
)


# Everything that uses df MUST be inside this section
if uploaded_file is not None:

    # =========================
    # READ EXCEL FILE
    # =========================

    df = pd.read_excel(uploaded_file)

    st.success("File uploaded successfully!")

    st.subheader("Detected Columns")

    st.write(df.columns.tolist())


    # =========================
    # RENAME COLUMNS
    # =========================

    df = df.rename(columns={
        'PV (2000 MW)': 'Solar',
        'Wind MW (60MW) ': 'Wind',
        'Total MWh ': 'Total'
    })


    # Create hour index
    df['Hour Index'] = range(len(df))


    # =========================
    # CHECK REQUIRED COLUMNS
    # =========================

    required_columns = ['Solar', 'Wind', 'Total']

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

    else:

        # =========================
        # RESOURCE ANALYSIS
        # =========================

        st.header("Renewable Energy Analysis")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Maximum Generation",
            f"{df['Total'].max():,.2f} MW"
        )

        col2.metric(
            "Minimum Generation",
            f"{df['Total'].min():,.2f} MW"
        )

        col3.metric(
            "Average Generation",
            f"{df['Total'].mean():,.2f} MW"
        )


        # =========================
        # SOLAR FIGURE
        # =========================

        st.subheader("Solar Generation Profile")

        fig1, ax1 = plt.subplots(figsize=(16, 5))

        ax1.bar(
            df['Hour Index'],
            df['Solar'],
            color='orange',
            width=1.0,
            label='Solar'
        )

        ax1.set_title(
            'Solar-only Generation Profile',
            fontweight='bold'
        )

        ax1.set_xlabel(
            'Hour Index',
            fontweight='bold'
        )

        ax1.set_ylabel(
            'Solar Power (MW)',
            fontweight='bold'
        )

        ax1.legend()

        ax1.grid(
            True,
            axis='y',
            linestyle='--',
            alpha=0.7
        )

        st.pyplot(fig1)

        plt.close(fig1)


        # =========================
        # WIND FIGURE
        # =========================

        st.subheader("Wind Generation Profile")

        fig2, ax2 = plt.subplots(figsize=(16, 5))

        ax2.bar(
            df['Hour Index'],
            df['Wind'],
            color='#AEC6CF',
            width=1.0,
            label='Wind'
        )

        ax2.set_title(
            'Wind-only Generation Profile',
            fontweight='bold'
        )

        ax2.set_xlabel(
            'Hour Index',
            fontweight='bold'
        )

        ax2.set_ylabel(
            'Wind Power (MW)',
            fontweight='bold'
        )

        ax2.legend()

        ax2.grid(
            True,
            axis='y',
            linestyle='--',
            alpha=0.7
        )

        st.pyplot(fig2)

        plt.close(fig2)


        # =========================
        # COMBINED FIGURE
        # =========================

        st.subheader("Combined Renewable Generation Profile")

        fig3, ax3 = plt.subplots(figsize=(16, 5))

        ax3.bar(
            df['Hour Index'],
            df['Total'],
            color='green',
            width=1.0,
            label='Solar + Wind'
        )

        ax3.set_title(
            'Combined Renewable Generation Profile',
            fontweight='bold'
        )

        ax3.set_xlabel(
            'Hour Index',
            fontweight='bold'
        )

        ax3.set_ylabel(
            'Total Power (MW)',
            fontweight='bold'
        )

        ax3.legend()

        ax3.grid(
            True,
            axis='y',
            linestyle='--',
            alpha=0.7
        )

        st.pyplot(fig3)

        plt.close(fig3)
    # ==========================================
    # ELECTROLYZER SIZE OPTIMIZATION
    # ==========================================

    st.header("Electrolyzer Size Optimization")

    st.write(
        "The electrolyzer capacity is optimized based on the "
        "highest calculated annual profit."
    )

    # Renewable energy available each hour
    E_h = pd.to_numeric(
        df["Total"],
        errors="coerce"
    ).fillna(0).to_numpy(dtype=float)

    h_h = np.ones_like(E_h)


    # ==========================================
    # OPTIMIZATION INPUTS
    # ==========================================

    st.subheader("Optimization Parameters")

    col1, col2, col3 = st.columns(3)

    with col1:
        min_size = st.number_input(
            "Minimum Electrolyzer Size (MW)",
            min_value=1,
            value=500,
            step=50
        )

    with col2:
        max_size = st.number_input(
            "Maximum Electrolyzer Size (MW)",
            min_value=1,
            value=1000,
            step=50
        )

    with col3:
        size_step = st.number_input(
            "Size Step (MW)",
            min_value=1,
            value=50,
            step=10
        )


    # ==========================================
    # ECONOMIC PARAMETERS
    # ==========================================

    st.subheader("Economic Parameters")

    econ1, econ2, econ3 = st.columns(3)

    with econ1:
        capex_per_MW = st.number_input(
            "Electrolyzer CAPEX (OMR/MW)",
            value=1026230.0
        )

        opex_per_MW = st.number_input(
            "Annual OPEX (OMR/MW)",
            value=20520.0
        )

    with econ2:
        elec_price = st.number_input(
            "Electricity Price (OMR/MWh)",
            value=15.964,
            format="%.3f"
        )

        H2_price = st.number_input(
            "Hydrogen Selling Price (OMR/kg)",
            value=2.5
        )

    with econ3:
        wacc_percent = st.number_input(
            "WACC (%)",
            value=5.0
        )

        life_years = st.number_input(
            "Project Lifetime (years)",
            value=25
        )

    wacc = wacc_percent / 100


    # ==========================================
    # SPECIFIC ENERGY CONSUMPTION
    # ==========================================

    def sec_kwh_per_kg(Uf):

        return (
            50
            + 12 * np.maximum(0, 0.7 - Uf)**2
            + 8 * np.maximum(0, Uf - 0.9)**2
        )


    # ==========================================
    # EVALUATE EACH ELECTROLYZER SIZE
    # ==========================================

    def eval_size(P_el_MW):

        # Maximum energy electrolyzer can accept each hour
        E_max = P_el_MW * h_h

        # Renewable energy actually used
        E_used = np.minimum(E_h, E_max)

        # Renewable energy above electrolyzer capacity
        E_excess = np.maximum(0, E_h - E_max)

        E_excess_annual = E_excess.sum()


        # ------------------------------
        # Utilization
        # ------------------------------

        Uf_h = E_used / (E_max + 1e-9)


        # ------------------------------
        # SEC
        # ------------------------------

        SEC_h = sec_kwh_per_kg(Uf_h)


        # ------------------------------
        # Hydrogen Production
        # ------------------------------

        H_hour = (E_used * 1000) / SEC_h

        H_total = H_hour.sum()

        H_tonnes = H_total / 1000


        # ------------------------------
        # Capital Recovery Factor
        # ------------------------------

        if wacc == 0:

            CRF = 1 / life_years

        else:

            CRF = (
                wacc * (1 + wacc)**life_years
            ) / (
                (1 + wacc)**life_years - 1
            )


        # ------------------------------
        # Annual Costs
        # ------------------------------

        C_capex_annual = (
            capex_per_MW
            * P_el_MW
            * CRF
        )

        C_opex = (
            opex_per_MW
            * P_el_MW
        )

        C_elec = (
            elec_price
            * E_used.sum()
        )

        C_total = (
            C_capex_annual
            + C_opex
            + C_elec
        )


        # ------------------------------
        # Economics
        # ------------------------------

        if H_total > 0:

            LCOH = C_total / H_total

        else:

            LCOH = np.nan


        Revenue = (
            H_total
            * H2_price
        )

        Profit = (
            Revenue
            - C_total
        )


        # ------------------------------
        # Annual Utilization Factor
        # ------------------------------

        Uf_year = (
            E_used.sum()
            / (
                P_el_MW
                * h_h.sum()
                + 1e-9
            )
        )


        return {

            "Size_MW": P_el_MW,

            "Hydrogen_tonnes": H_tonnes,

            "Revenue_OMR": Revenue,

            "Profit_OMR": Profit,

            "LCOH_OMR_per_kg": LCOH,

            "UF_year": Uf_year,

            "Excess_MWh": E_excess_annual
        }


    # ==========================================
    # OPTIMIZATION BUTTON
    # ==========================================

    if st.button("Optimize Electrolyzer Size"):

        if max_size < min_size:

            st.error(
                "Maximum size must be greater than "
                "the minimum size."
            )

        else:

            # Test all capacities in selected range
            tested_sizes = range(
                int(min_size),
                int(max_size) + 1,
                int(size_step)
            )

            results = [
                eval_size(size)
                for size in tested_sizes
            ]

            results_df = pd.DataFrame(results)


            # ==========================================
            # FIND MAXIMUM-PROFIT SIZE
            # ==========================================

            optimal_index = (
                results_df["Profit_OMR"].idxmax()
            )

            optimal = (
                results_df.loc[optimal_index]
            )


            # ==========================================
            # OPTIMUM RESULT
            # ==========================================

            st.subheader(
                "Recommended Electrolyzer Size"
            )

            st.success(
                f"Maximum-profit electrolyzer size: "
                f"{optimal['Size_MW']:.0f} MW"
            )


            # ==========================================
            # MAIN RESULTS
            # ==========================================

            r1, r2, r3 = st.columns(3)

            r1.metric(
                "Optimal Size",
                f"{optimal['Size_MW']:.0f} MW"
            )

            r2.metric(
                "Annual Profit",
                f"{optimal['Profit_OMR']:,.0f} OMR"
            )

            r3.metric(
                "H₂ Production",
                f"{optimal['Hydrogen_tonnes']:,.1f} tonnes/year"
            )


            r4, r5, r6 = st.columns(3)

            r4.metric(
                "LCOH",
                f"{optimal['LCOH_OMR_per_kg']:.3f} OMR/kg"
            )

            r5.metric(
                "Utilization Factor",
                f"{optimal['UF_year'] * 100:.2f}%"
            )

            r6.metric(
                "Excess Renewable Energy",
                f"{optimal['Excess_MWh']:,.0f} MWh"
            )


            # ==========================================
            # PROFIT GRAPH
            # ==========================================

            st.subheader(
                "Profit vs Electrolyzer Size"
            )

            fig4, ax4 = plt.subplots(
                figsize=(12, 6)
            )

            ax4.plot(
                results_df["Size_MW"],
                results_df["Profit_OMR"],
                marker="o",
                linestyle="-",
                color="teal",
                linewidth=2
            )


            # Optimal point
            ax4.scatter(
                optimal["Size_MW"],
                optimal["Profit_OMR"],
                color="red",
                s=120,
                zorder=5,
                label="Maximum Profit"
            )


            # Vertical optimum line
            ax4.axvline(
                x=optimal["Size_MW"],
                color="red",
                linestyle="--",
                alpha=0.7
            )


            # Label optimum
            ax4.annotate(
                (
                    f"Optimal = "
                    f"{optimal['Size_MW']:.0f} MW\n"
                    f"Profit = "
                    f"{optimal['Profit_OMR']:,.0f} OMR"
                ),

                xy=(
                    optimal["Size_MW"],
                    optimal["Profit_OMR"]
                ),

                xytext=(15, 20),

                textcoords="offset points",

                fontweight="bold",

                arrowprops=dict(
                    arrowstyle="->",
                    color="red"
                )
            )


            ax4.set_title(
                "Profit vs Electrolyzer Size",
                fontweight="bold"
            )

            ax4.set_xlabel(
                "Electrolyzer Size (MW)",
                fontweight="bold"
            )

            ax4.set_ylabel(
                "Annual Profit (OMR)",
                fontweight="bold"
            )

            ax4.grid(
                True,
                linestyle="--",
                alpha=0.7
            )

            ax4.legend()

            st.pyplot(fig4)

            plt.close(fig4)


            # ==========================================
            # COMPARISON TABLE
            # ==========================================

            st.subheader(
                "Electrolyzer Size Comparison"
            )

            table_df = results_df.copy()

            table_df["UF_year"] = (
                table_df["UF_year"] * 100
            )

            table_df = table_df.rename(
                columns={

                    "Size_MW":
                        "Electrolyzer Size (MW)",

                    "Hydrogen_tonnes":
                        "H₂ Production (tonnes/year)",

                    "Revenue_OMR":
                        "Revenue (OMR/year)",

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

            st.dataframe(
                table_df.round(3),
                width="stretch"
            )

else:

    st.info(
        "Please upload an Excel file to begin the analysis."
    )