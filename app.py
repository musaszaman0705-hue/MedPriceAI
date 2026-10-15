
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="MedPrice AI",
    page_icon="💊",
    layout="wide"
)

# ---------------------------------
# Demo medication dataset
# All prices are fictional.
# ---------------------------------


# Load medication data from the CSV file
import pandas as pd

df = pd.read_csv(
    "medications.csv",
    dtype={"zip_code": str}
)

# Clean medication data
df["medication"] = df["medication"].str.strip().str.title()
df["strength"] = df["strength"].str.strip()
df["pharmacy"] = df["pharmacy"].str.strip()
df["zip_code"] = df["zip_code"].str.strip()
df["price"] = pd.to_numeric(df["price"], errors="coerce")

# Remove incomplete or invalid records
df = df.dropna(
    subset=[
        "medication", "strength", "quantity",
        "pharmacy", "zip_code", "price"
    ]
)

df = df[
    (df["price"] > 0) &
    (df["quantity"] > 0)
].drop_duplicates().reset_index(drop=True)


# ---------------------------------
# Website design
# ---------------------------------

st.title("💊 MedPrice AI")
st.subheader("Prescription Price Comparison Assistant")

st.write(
    "Compare sample prescription prices across pharmacies "
    "and explore lower-cost options."
)

st.warning(
    "Prototype only: all prices are fictional examples, "
    "not actual pharmacy quotes. Do not use them to make "
    "prescription or treatment decisions."
)

st.divider()

# ---------------------------------
# Search form
# ---------------------------------

st.header("Find a Medication")

medication_list = sorted(df["medication"].unique())

with st.form("medication_search"):
    medication = st.selectbox(
        "Select medication",
        medication_list
    )

    zip_code = st.text_input(
        "ZIP code",
        value="77002",
        max_chars=5
    )

    available_quantities = sorted(
        df[df["medication"] == medication]["quantity"].unique()
    )

    quantity = st.selectbox(
        "Prescription quantity",
        available_quantities
    )

    submitted = st.form_submit_button(
        "Compare Prices",
        type="primary"
    )

# ---------------------------------
# Results
# ---------------------------------

if submitted:
    if not zip_code.isdigit() or len(zip_code) != 5:
        st.error("Enter a valid five-digit ZIP code.")
    else:
        results = df[
            (df["medication"] == medication) &
            (df["zip_code"] == zip_code) &
            (df["quantity"] == quantity)
        ].copy()

        if results.empty:
            st.info(
                "No sample price records were found for this "
                "medication and ZIP code."
            )
        else:
            results = results.sort_values("price")

            st.header("Price Comparison")

            cheapest = results.iloc[0]
            highest = results["price"].max()
            difference = highest - cheapest["price"]

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Lowest demo price",
                f"${cheapest['price']:.2f}"
            )

            col2.metric(
                "Highest demo price",
                f"${highest:.2f}"
            )

            col3.metric(
                "Price difference",
                f"${difference:.2f}"
            )

            st.success(
                f"Lowest listed demo price: "
                f"{cheapest['pharmacy']}"
            )

            st.dataframe(
                results[
                    ["pharmacy", "medication", "strength",
                     "quantity", "price"]
                ].rename(
                    columns={
                        "pharmacy": "Pharmacy",
                        "medication": "Medication",
                        "strength": "Strength",
                        "quantity": "Quantity",
                        "price": "Demo Price ($)"
                    }
                ),
                use_container_width=True,
                hide_index=True
            )

            st.caption(
                "The price difference is not guaranteed savings. "
                "Real costs depend on insurance, discounts, "
                "eligibility, and pharmacy pricing."
            )

st.divider()

st.subheader("About MedPrice AI")

st.write(
    "MedPrice AI is a student project prototype designed to "
    "demonstrate how prescription price comparison can work. "
    "It does not provide medical advice or live pharmacy prices."
)

st.caption(
    "Always confirm prescription prices directly with a pharmacy. "
    "Never change or stop a medication based on this demo."
)

