
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="MedPrice AI",
    page_icon="💊",
    layout="wide"
)

# ---------- Styling ----------
st.markdown("""
<style>
.stApp {
    background-color: #F5F9F7;
}
h1, h2, h3 {
    color: #145C4B;
}
div.stButton > button {
    background-color: #167D68;
    color: white;
    border-radius: 10px;
    border: none;
    min-height: 42px;
}
div.stButton > button:hover {
    background-color: #105747;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ---------- Demo dataset ----------
# All prices below are fictional.
# Do not present them as real pharmacy prices.

data = [
    ["Atorvastatin", "20 mg", 30, "Community Pharmacy", "77002", 8.50],
    ["Atorvastatin", "20 mg", 30, "City Pharmacy", "77002", 12.75],
    ["Atorvastatin", "20 mg", 30, "Neighborhood Drugs", "77002", 6.99],
    ["Metformin", "500 mg", 60, "Community Pharmacy", "77002", 7.25],
    ["Metformin", "500 mg", 60, "Neighborhood Drugs", "77002", 5.50],
    ["Lisinopril", "10 mg", 30, "City Pharmacy", "77002", 8.25],
    ["Lisinopril", "10 mg", 30, "Neighborhood Drugs", "77002", 6.75],
    ["Amoxicillin", "500 mg", 21, "Community Pharmacy", "77002", 9.00],
    ["Amoxicillin", "500 mg", 21, "City Pharmacy", "77002", 13.50],
    ["Sertraline", "50 mg", 30, "Community Pharmacy", "77002", 10.00],
]

df = pd.DataFrame(
    data,
    columns=[
        "Medication", "Strength", "Quantity",
        "Pharmacy", "ZIP", "Price"
    ]
)

# ---------- Header ----------
st.title("💊 MedPrice AI")
st.caption("Prescription price comparison assistant")

st.markdown(
    "### Your prescription. A better price.\n"
    "Search for a medication and compare example prices "
    "to understand how pharmacy costs can differ."
)

st.info(
    "DEMO MODE: All prices shown are fictional examples. "
    "They are not live quotes or verified savings."
)

# ---------- Search ----------
st.subheader("Find your medication")

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    medication = st.text_input(
        "Medication name",
        placeholder="e.g. Atorvastatin"
    )

with col2:
    zip_code = st.text_input(
        "ZIP code",
        placeholder="e.g. 77002",
        max_chars=5
    )

with col3:
    quantity = st.number_input(
        "Prescription quantity",
        min_value=1,
        max_value=1000,
        value=30,
        step=1
    )

search = st.button("🔎 Compare prices", use_container_width=True)

# ---------- Results ----------
if search:
    if not medication.strip():
        st.warning("Enter a medication name to search.")
    elif zip_code and (
        len(zip_code) != 5 or not zip_code.isdigit()
    ):
        st.warning("Enter a valid five-digit ZIP code.")
    else:
        results = df[
            df["Medication"].str.contains(
                medication.strip(),
                case=False,
                regex=False
            )
        ].copy()

        if zip_code:
            results = results[results["ZIP"] == zip_code]

        results = results[
            results["Quantity"] == quantity
        ]

        if results.empty:
            st.warning(
                "No matching demo records were found. "
                "Try Atorvastatin, Metformin, Lisinopril, "
                "Amoxicillin, or Sertraline. "
                "The sample dataset only includes ZIP code 77002 "
                "and specific quantities."
            )
        else:
            results = results.sort_values("Price")

            st.subheader("Price comparison results")

            cheapest = results.iloc[0]
            highest = results["Price"].max()
            lowest = results["Price"].min()

            a, b, c = st.columns(3)

            a.metric("Lowest demo price", f"${lowest:.2f}")
            b.metric("Highest demo price", f"${highest:.2f}")
            c.metric(
                "Price difference",
                f"${highest - lowest:.2f}"
            )

            st.success(
                f"Lowest example price: "
                f"{cheapest['Pharmacy']} — "
                f"${cheapest['Price']:.2f}"
            )

            display_df = results.rename(
                columns={
                    "Medication": "Medication",
                    "Strength": "Strength",
                    "Quantity": "Quantity",
                    "Pharmacy": "Pharmacy",
                    "ZIP": "ZIP Code",
                    "Price": "Demo Price"
                }
            )

            st.dataframe(
                display_df,
                hide_index=True,
                use_container_width=True,
                column_config={
                    "Demo Price": st.column_config.NumberColumn(
                        format="$%.2f"
                    )
                }
            )

            st.caption(
                "The price difference is calculated from the "
                "sample records only. It is not a guaranteed saving."
            )

# ---------- Additional information ----------
st.divider()

left, right = st.columns(2)

with left:
    st.subheader("How it works")
    st.write(
        "1. Search for a medication.\n\n"
        "2. Enter a ZIP code and quantity.\n\n"
        "3. Review matching sample prices."
    )

with right:
    st.subheader("About MedPrice AI")
    st.write(
        "Our goal is to help people understand prescription "
        "cost differences and find ways to explore affordable "
        "medication options."
    )

st.caption(
    "MedPrice AI is an educational prototype, not a pharmacy "
    "or medical provider. Confirm current prices, availability, "
    "insurance coverage, and discount terms with the pharmacy. "
    "Ask a pharmacist or prescriber about medication alternatives."
)
