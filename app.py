
import streamlit as st
import pandas as pd

# Load the dataset
@st.cache_data
def load_data():
    return pd.read_excel("Gitesi_Tax_WebApp_Final.xlsx")

df = load_data()

st.title("📊 Gitesi Taxpayer Arrears Management")

# Search bar
search_option = st.selectbox("Search by", ["TIN", "Tax Payer Name", "Upi No"])
search_query = st.text_input(f"Enter {search_option}")

if search_query:
    results = df[df[search_option].astype(str).str.contains(search_query, case=False, na=False)]

    if not results.empty:
        for idx, row in results.iterrows():
            st.markdown("---")
            st.subheader(f"👤 {row['Tax Payer Name']} | 🏷️ TIN: {row['TIN']}")
            st.write(f"**UPI:** {row['Upi No']}")
            st.write(f"**Total Balance:** {row['Balance']} RWF")

            # Input for new payment and commitment
            amount_paid = st.number_input("💰 Amount Paid", min_value=0, step=1000, key=f"amount_{idx}")
            commitment = st.text_area("📝 Commitment (if any)", key=f"commitment_{idx}")

            if st.button("💾 Save Entry", key=f"save_{idx}"):
                df.at[idx, 'Amount Paid (New)'] = amount_paid
                df.at[idx, 'Commitment'] = commitment
                df.at[idx, 'Remaining Balance (Auto)'] = row['Balance'] - amount_paid

                st.success("✔️ Entry saved (note: changes are not persistent in this demo)")

    else:
        st.warning("🔍 No matching records found.")
else:
    st.info("👈 Please enter a search query to begin.")
