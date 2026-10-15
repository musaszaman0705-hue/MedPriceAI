
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="MedPrice AI",
    page_icon="💊",
    layout="wide"
)

NADAC_URL = (
    "https://download.medicaid.gov/data/"
    "nadac-national-average-drug-acquisition-cost-09-23-2026.csv"
)


@st.cache_data(ttl=86400)
def load_nadac_data():
    columns = [
        "NDC Description",
        "NDC",
        "NADAC Per Unit",
        "Effective Date",
        "Pricing Unit",
        "As of Date"
    ]

    df = pd.read_csv(
        NADAC_URL,
        usecols=columns,
        dtype={"NDC": str},
        low_memory=False
    )

    # Convert costs and dates into usable formats
    df["NADAC Per Unit"] = pd.to_numeric(
        df["NADAC Per Unit"],
        errors="coerce"
    )

    df["As of Date"] = pd.to_datetime(
        df["As of Date"],
        errors="coerce"
    )

    df["Effective Date"] = pd.to_datetime(
        df["Effective Date"],
        errors="coerce"
    )

    # Remove incomplete or invalid records
    df = df.dropna(
        subset=[
            "NDC Description",
            "NADAC Per Unit",
            "As of Date"
        ]
    )

    df = df[df["NADAC Per Unit"] >= 0].copy()

    # Keep only records from the newest available snapshot
    if not df.empty:
        latest_date = df["As of Date"].max()
        df = df[df["As of Date"] == latest_date].copy()

    return df

st.title("💊 MedPrice AI")
st.subheader("Government Drug Cost Explorer")

st.info(
    "This version uses CMS NADAC acquisition-cost data. "
    "These values are not pharmacy-specific retail prices "
    "or guaranteed patient costs."
)

try:
    nadac = load_nadac_data()

if not nadac.empty:
    latest_date = nadac["As of Date"].max()

    st.caption(
        f"CMS data snapshot: {latest_date:%B %d, %Y}"
    )



    query = st.text_input(
        "Search for a medication",
        placeholder="For example, Metformin"
    )

    if query.strip():
        results = nadac[
            nadac["NDC Description"].str.contains(
                query.strip(),
                case=False,
                na=False,
                regex=False
            )
        ].copy()

        if results.empty:
            st.warning("No matching drug records found.")
        else:
            results = results.sort_values(
                "Effective Date",
                ascending=False
            )

            st.write(f"Matching records: {len(results)}")

            st.dataframe(
                results.head(100),
                use_container_width=True,
                hide_index=True
            )

    st.caption(
        "Source: CMS National Average Drug Acquisition Cost "
        "(NADAC). Confirm retail prescription prices directly "
        "with pharmacies."
    )

except Exception as error:
    st.error(
        "The CMS data could not be loaded. "
        "Please try again later."
    )
    st.caption(f"Technical details: {error}")

