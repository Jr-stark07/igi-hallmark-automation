import streamlit as st
import pandas as pd

st.set_page_config(page_title="IGI Hallmark Automation", layout="wide")

st.title("IGI Hallmark Automation App")
st.write("Upload your IGI Excel file to generate automatic summaries.")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx", "xls"])

def map_item(sku):
    if "MN" in sku.upper():
        return "Necklace"
    elif "ER" in sku.upper():
        return "Earring"
    elif "RG" in sku.upper():
        return "Ring"
    elif "BR" in sku.upper():
        return "Bracelet"
    else:
        return "Other"

def map_stone(sku):
    if "BB" in sku.upper():
        return "Black Beads"
    else:
        return "Other"

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    st.subheader("Raw Data Preview")
    st.dataframe(df.head())

    # Expected columns:
    # SKU, KT, Category, PCS

    df["Item"] = df["SKU"].astype(str).apply(map_item)
    df["Stone"] = df["SKU"].astype(str).apply(map_stone)

    # Ignore stone qty & weight as per your rule
    df["Stone_Qty"] = 0
    df["Stone_Wt"] = 0

    st.subheader("Processed Data")
    st.dataframe(df)

    # 14KT summary
    summary_14 = df[df["KT"] == 14].groupby("Category")["PCS"].sum().reset_index()
    summary_14["KT"] = "14KT"

    # 18KT summary
    summary_18 = df[df["KT"] == 18].groupby("Category")["PCS"].sum().reset_index()
    summary_18["KT"] = "18KT"

    final_summary = pd.concat([summary_14, summary_18])

    total_pcs = df["PCS"].sum()

    st.subheader("Category Wise Summary")
    st.dataframe(final_summary)

    st.success(f"Total PCS: {total_pcs}")

    # Download Excel
    output_file = "IGI_Summary.xlsx"
    with pd.ExcelWriter(output_file, engine="xlsxwriter") as writer:
        df.to_excel(writer, sheet_name="Processed_Data", index=False)
        final_summary.to_excel(writer, sheet_name="Summary", index=False)

    with open(output_file, "rb") as f:
        st.download_button(
            label="Download Summary Excel",
            data=f,
            file_name="IGI_Summary.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
