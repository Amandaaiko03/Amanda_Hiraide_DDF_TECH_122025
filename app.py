import streamlit as st
import pandas as pd
import plotly.express as px
import os # Biblioteca para ver arquivos do sistema

# Configuração Inicial
st.set_page_config(page_title="Olist Data App", layout="wide", page_icon="🛒")

# Título
st.title("🛒 Olist E-Commerce - Inteligência de Dados & GenAI")

# --- MODO DEBUG (RAIO-X) ---
st.sidebar.header("🛠️ Debug de Arquivos")
st.sidebar.write("Arquivos encontrados na pasta:")
# Lista tudo que tem na pasta atual
arquivos = os.listdir('.')
st.sidebar.code("\n".join(arquivos))

# Se tiver pasta data, lista também
if 'data' in arquivos:
    st.sidebar.write("Dentro de /data:")
    st.sidebar.code("\n".join(os.listdir('data')))
# ---------------------------

# Função de Carga de Dados
@st.cache_data
def load_data():
    df_reviews = None
    
    # Tenta ler o arquivo com flexibilidade de nome
    # Adicionei variações comuns de nome aqui
    possiveis_nomes = [
        "REVIEWS_ENRICHED_GENAI.csv", 
        "reviews_enriched_genai.csv", 
        "Reviews_Enriched_Genai.csv",
        "data/REVIEWS_ENRICHED_GENAI.csv",
        "data/reviews_enriched_genai.csv"
    ]
    
    arquivo_encontrado = ""
    
    for nome in possiveis_nomes:
        if os.path.exists(nome):
            try:
                df_reviews = pd.read_csv(nome)
                arquivo_encontrado = nome
                break
            except:
                continue
            
    # Fallback
    if df_reviews is None:
        st.warning(f"⚠️ Arquivo não encontrado. O App procurou por: {possiveis_nomes}")
        # Dados fake para não quebrar
        df_reviews = pd.DataFrame({
            'sentiment': ['Positivo', 'Negativo'] * 10,
            'category': ['Logística', 'Produto'] * 10,
            'review_comment_message': ['Teste', 'Teste'] * 10
        })
    else:
        st.success(f"✅ Arquivo carregado: {arquivo_encontrado}")

    # Carregar Vendas (simplificado para focar no erro)
    df_sales = None
    if os.path.exists("GOLD_SALES_ORDER_CDM.csv"):
        df_sales = pd.read_csv("GOLD_SALES_ORDER_CDM.csv")
    elif os.path.exists("data/gold/GOLD_SALES_ORDER_CDM.csv"):
         df_sales = pd.read_csv("data/gold/GOLD_SALES_ORDER_CDM.csv")

    return df_reviews, df_sales

df_reviews, df_sales = load_data()

# --- Visualização Rápida ---
tab1, tab2 = st.tabs(["IA & Reviews", "Vendas"])

with tab1:
    if df_reviews is not None and 'sentiment' in df_reviews.columns:
        fig = px.pie(df_reviews, names='sentiment', title="Sentimentos")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("CSV carregado mas sem coluna 'sentiment'.")

with tab2:
    if df_sales is not None:
        st.dataframe(df_sales.head())
    else:
        st.info("Sem dados de vendas.")
