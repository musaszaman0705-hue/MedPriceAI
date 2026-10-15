
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

data = {
    "medication": [
        "Metformin", "Metformin", "Metformin",
        "Amoxicillin", "Amoxicillin", "Amoxicillin",
        "Atorvastatin", "Atorvastatin", "Atorvastatin",
        "Lisinopril", "Lisinopril", "Lisinopril",
        "Sertraline", "Sertraline", "Sertraline"
    ],
    "strength": [
        "500 mg", "500 mg", "500 mg",
        "500 mg", "500 mg", "500 mg",
        "20 mg", "20 mg", "20 mg",
        "10 mg", "10 mg", "10 mg",
        "50 mg", "50 mg", "50 mg"
    ],
    "quantity": [
        30, 30, 30, 21, 21, 21, 30, 30, 30,
        30, 30, 30, 30, 30, 30
    ],
    "pharmacy": [
        "Community Pharmacy", "City Pharmacy",
        "Neighborhood Drugs",
        "Community Pharmacy", "City Pharmacy",
        "Neighborhood Drugs",
        "Community Pharmacy", "City Pharmacy",
        "Neighborhood Drugs",
        "Community Pharmacy", "City Pharmacy",
        "Neighborhood Drugs",
        "Community Pharmacy", "City Pharmacy",
        "Neighborhood Drugs"
    ],
    "zip_code": ["77002"] * 15,
    "price": [
        8.50, 6.25, 7.10,
        12.00, 9.50, 10.25,
        11.75, 8.00, 9.25,
        7.50, 5.99, 6.75,
        13.50, 10.00, 11.25
    ]
}

df = pd.DataFrame(data)

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

