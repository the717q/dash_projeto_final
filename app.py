import streamlit as st
import pandas as pd

st.set_page_config(page_title='Dashboard', layout='wide')

st.title('Amazon Dashboard')
st.markdown('Dashboard de produtos')

@st.cache_data 
def load_data():
    file_name = "clean_output.parquet"
    df = pd.read_csv(file_name, parse_dates=["Order Date"])
    return df

df = load_data()

st.sidebar.header("Filtros")

sorted_categories = sorted(df["Category"].unique())
categories = st.sidebar.multiselect(
    "Categoria",
    options=sorted_categories,
    default=sorted_categories
)

years = sorted(df["rating"].unique())
year_range = st.sidebar.slider(
    "Rating",
)

# --------------------------------------------------
# Parte superior com KPIs
# --------------------------------------------------

total_rating =  df["rating_count"].sum()
total_category =  df["category"].sum()

# Vamos dividir a área em 3 colunas para mostrar os KPIs lado a lado
col1, col2, col3 = st.columns(3)
col1.metric("💰 Vendas Totais", f"${total_rating:,.0f}")
col2.metric("📈 Lucro Total", f"${total_category:,.0f}")