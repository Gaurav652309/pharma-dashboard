import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Pharma Dashboard", layout="wide")

st.title("💊 Pharma Market Performance Dashboard")

uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Clean column names
    df.columns = df.columns.str.strip()

    # Convert numeric columns safely
    for col in df.columns:
        try:
            df[col] = pd.to_numeric(df[col])
        except:
            pass

    # Fill missing values ONLY for numeric columns
    numeric_cols = df.select_dtypes(include=['number']).columns
    df[numeric_cols] = df[numeric_cols].fillna(0)

    # Sidebar filter
    st.sidebar.header("Filters")
    company_filter = st.sidebar.multiselect(
        "Select Company",
        options=df["COMPANY"].dropna().unique(),
        default=df["COMPANY"].dropna().unique()
    )

    df = df[df["COMPANY"].isin(company_filter)]

    # KPIs
    total_market = df["Sum of MAT FEB'26"].sum()
    total_units = df["Sum of UNIT MAT FEB'26"].sum()

    overall_growth = (
        (df["Sum of MAT FEB'26"].sum() - df["Sum of MAT FEB'25"].sum())
        / df["Sum of MAT FEB'25"].sum()
    ) * 100

    top_brand = df.loc[df["Sum of MAT FEB'26"].idxmax()]["BRANDS"]
    fastest_growth = df.loc[df["Sum of % GROWTH 25-26"].idxmax()]["BRANDS"]

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Market", f"₹ {total_market:,.0f}")
    col2.metric("Growth %", f"{overall_growth:.2f}%")
    col3.metric("Total Units", f"{total_units:,.0f}")
    col4.metric("Top Brand", top_brand)
    col5.metric("Fastest Growth", fastest_growth)

    # Top 10 brands
    st.subheader("Top 10 Brands")
    top10 = df.sort_values(by="Sum of MAT FEB'26", ascending=False).head(10)
    fig1 = px.bar(top10, x="BRANDS", y="Sum of MAT FEB'26")
    st.plotly_chart(fig1, use_container_width=True)

    # Market share
    st.subheader("Company Market Share")
    share = df.groupby("COMPANY")["Sum of MAT FEB'26"].sum().reset_index()
    fig2 = px.pie(share, names="COMPANY", values="Sum of MAT FEB'26", hole=0.4)
    st.plotly_chart(fig2, use_container_width=True)

    # Scatter
    st.subheader("Growth Analysis")
    fig3 = px.scatter(
        df,
        x="Sum of % UNIT GROWTH 25-26",
        y="Sum of % GROWTH 25-26",
        size="Sum of MAT FEB'26",
        color="COMPANY",
        hover_name="BRANDS"
    )
    st.plotly_chart(fig3, use_container_width=True)

else:
    st.info("Please upload your Excel file.")
