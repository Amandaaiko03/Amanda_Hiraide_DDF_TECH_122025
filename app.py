import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuração da Página
st.set_page_config(page_title="Olist Data App", layout="wide", page_icon="🛒")

# 2. Título e Header
st.title("🛒 Olist E-Commerce - Inteligência de Dados & GenAI")
st.markdown("""
<style>
    .metric-card {background-color: #f0f2f6; padding: 20px; border-radius: 10px; text-align: center;}
</style>
""", unsafe_allow_html=True)

st.markdown("Este Data App demonstra a aplicação de **Engenharia de Dados** e **Inteligência Artificial** (LLMs) em dados reais de E-commerce.")

# 3. Carregamento de Dados (Com Cache para ser rápido)
@st.cache_data
def load_data():
    # Tenta carregar o arquivo de Reviews (Item 5)
    try:
 
        df_reviews = pd.read_csv("GOLD_SALES_ORDER_CDM.csv")
    except:
        # Dados Fakes para não quebrar o app se o arquivo não estiver lá
        st.warning("Arquivo de Reviews não encontrado. Usando dados de exemplo.")
        df_reviews = pd.DataFrame({
            'sentiment': ['Positivo', 'Negativo', 'Neutro', 'Positivo', 'Negativo'] * 20,
            'category': ['Logística', 'Produto', 'Atendimento', 'Logística', 'Produto'] * 20,
            'review_comment_message': ['Chegou rápido', 'Veio quebrado', 'Ok', 'Adorei', 'Péssimo'] * 20
        })

    # Tenta carregar o arquivo Gold (Item 4/6)
    try:
        df_sales = pd.read_csv("GOLD_SALES_ORDER_CDM.csv")
    except:
        df_sales = None

    return df_reviews, df_sales

df_reviews, df_sales = load_data()

# --- SIDEBAR ---
st.sidebar.header("Filtros")
st.sidebar.info("Este app conecta-se ao GitHub para CI/CD automático.")

# --- ABAS ---
tab1, tab2, tab3 = st.tabs(["🤖 GenAI & Sentimentos", "📦 Dados de Vendas", "📝 Sobre"])

#  INTELIGÊNCIA ARTIFICIAL
with tab1:
    st.header("Análise de Sentimento com LLMs")
    st.markdown("Processamento de linguagem natural aplicado aos comentários dos clientes.")
    
    col1, col2, col3 = st.columns(3)
    total_reviews = len(df_reviews)
    positive_pct = len(df_reviews[df_reviews['sentiment']=='Positivo']) / total_reviews * 100
    negative_pct = len(df_reviews[df_reviews['sentiment']=='Negativo']) / total_reviews * 100
    
    col1.metric("Total de Reviews Analisados", total_reviews)
    col2.metric("Sentimento Positivo", f"{positive_pct:.1f}%")
    col3.metric("Sentimento Negativo", f"{negative_pct:.1f}%", delta_color="inverse")
    
    # Gráficos
    c1, c2 = st.columns(2)
    with c1:
        fig_pie = px.pie(df_reviews, names='sentiment', title="Distribuição de Sentimentos", hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with c2:
        fig_bar = px.histogram(df_reviews, x='category', color='sentiment', barmode='group', title="Sentimento por Categoria", color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_bar, use_container_width=True)
        
    st.subheader("🔍 Buscador Semântico")
    texto = st.text_input("Digite um termo (ex: entrega, quebrado):")
    if texto:
        filtrado = df_reviews[df_reviews['review_comment_message'].str.contains(texto, case=False, na=False)]
        st.dataframe(filtrado[['category', 'sentiment', 'review_comment_message']].head(10))

#  DADOS DE VENDAS
with tab2:
    if df_sales is not None:
        st.header("Análise de Vendas (Camada Gold)")
        st.dataframe(df_sales.head())
        
        # Exemplo de gráfico se tiver dados numéricos
        if 'TransactionAmount' in df_sales.columns:
            st.metric("Receita Total (Amostra)", f"R$ {df_sales['TransactionAmount'].sum():,.2f}")
    else:
        st.info("Arquivo GOLD_SALES_ORDER_CDM.csv não encontrado. Suba o arquivo para ver esta aba.")

# SOBRE
with tab3:
    st.markdown("### Stack Tecnológico")
    st.markdown("""
    * **Linguagem:** Python 3.10+
    * **Framework Web:** Streamlit
    * **Visualização:** Plotly Express
    * **Hospedagem:** Streamlit Community Cloud (via GitHub)
    """)
