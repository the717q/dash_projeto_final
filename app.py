import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# streamlit run app.py
st.set_page_config(page_title='Dashboard', layout='wide')

st.title('Amazon Dashboard')
st.markdown('Dashboard de produtos')

@st.cache_data 
def load_data():
    file_name = "clean_output.parquet"
    df = pd.read_parquet(file_name)
    return df

df = load_data()

# --------------------------------------------------
# Parte superior com KPIs
# --------------------------------------------------

total_rating =  df["rating_count"].sum()
total_category =  df["category"].sum()

# Vamos dividir a área em 3 colunas para mostrar os KPIs lado a lado
#col1, col2, col3 = st.columns(3)
#col1.metric("💰 Nº de ratings", f"{total_rating}")
#col2.metric("📈 Lucro Total", f"${total_category:,.0f}")

st.subheader('Top Produtos com Mais Avaliações')

top_rated = (
    df
    .nlargest(10, 'rating_count')
    .assign(short_name=lambda x: x['product_name'].str[:40] + "...")
    .set_index('short_name')['rating_count']
)

st.bar_chart(top_rated)


st.subheader('Top Produtos com Melhores avaliações')

top_rated = (
    df
    .nlargest(10, 'rating')
    .assign(short_name=lambda x: x['product_name'].str[:40] + "...")
    .set_index('short_name')['rating']
)

st.bar_chart(top_rated)

# Distribuição de preços após desconto:
st.divider()


# Create price bins (like grouping)
st.subheader("Distribuição de Preços após desconto")

price_dist = (
    df
    .assign(price_bin=pd.cut(df['discounted_price'], bins=5).astype(str))
    .groupby('price_bin')
    .size()
)

st.bar_chart(price_dist)

st.divider()

#####

st.subheader("Distribuição da percentagem de desconto")

dist = (
    df['discount_percentage']
    .value_counts(bins=20)
    .sort_index()
)

st.bar_chart(dist)


st.divider()

st.subheader("Distribuição da variável rating")

dist = (
    df['rating']
    .value_counts(bins=20)
    .sort_index()
)

st.bar_chart(dist)

####
