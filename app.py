import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração Inicial
st.set_page_config(page_title="Olist Data App", layout="wide", page_icon="🛒")

# Título e Estilo CSS
st.title("🛒 Olist E-Commerce - Inteligência de Dados & GenAI")
st.markdown("""
<style>
    .metric-card {background-color: #f0f2f6; padding: 20px; border-radius: 10px; text-align: center;}
</style>
""", unsafe_allow_html=True)

st.markdown("Este Data App demonstra a aplicação de **Engenharia de Dados** e **Inteligência Artificial** (LLMs) em dados reais de E-commerce.")

# Função de Carga de Dados (Cache)
@st.cache_data
def load_data():
    # 1. Carregar Reviews (Prioridade: Raiz)
    df_reviews = None
    # Lista de caminhos: Tenta na raiz primeiro, depois na pasta data
    paths_reviews = ["REVIEWS_ENRICHED_GENAI.csv", "data/REVIEWS_ENRICHED_GENAI.csv"]
    
    for path in paths_reviews:
        try:
            df_reviews = pd.read_csv(path)
            # Verifica se carregou certo (se tem colunas)
            if not df_reviews.empty:
                break 
        except FileNotFoundError:
            continue
            
    # Fallback (Dados fictícios caso arquivo não seja encontrado)
    if df_reviews is None:
        st.warning("⚠️ Arquivo de Reviews não encontrado. Usando dados de exemplo.")
        df_reviews = pd.DataFrame({
            'sentiment': ['Positivo', 'Negativo', 'Neutro', 'Positivo', 'Negativo'] * 20,
            'category': ['Logística', 'Produto', 'Atendimento', 'Logística', 'Produto'] * 20,
            'review_comment_message': ['Chegou rápido', 'Veio quebrado', 'Ok', 'Adorei', 'Péssimo'] * 20
        })

    # 2. Carregar Vendas Gold
    df_sales = None
    paths_sales = ["data/gold/GOLD_SALES_ORDER_CDM.csv", "GOLD_SALES_ORDER_CDM.csv"]
    
    for path in paths_sales:
        try:
            df_sales = pd.read_csv(path)
            if not df_sales.empty:
                break
        except FileNotFoundError:
            continue

    return df_reviews, df_sales

# Execução da Carga
df_reviews, df_sales = load_data()

# Sidebar
st.sidebar.header("Filtros e Opções")
st.sidebar.info("🔗 Conectado ao GitHub")

# Estrutura de Abas
tab1, tab2, tab3 = st.tabs(["🤖 GenAI & Sentimentos", "📦 Dados de Vendas", "📝 Sobre"])

# Aba 1: IA e Sentimentos
with tab1:
    st.header("Análise de Sentimento com LLMs")
    st.markdown("Processamento de linguagem natural aplicado aos comentários dos clientes (Item 5).")
    
    if df_reviews is not None:
        col1, col2, col3 = st.columns(3)
        total_reviews = len(df_reviews)
        
        # Verifica se a coluna 'sentiment' existe
        if 'sentiment' in df_reviews.columns:
            # Métricas
            positive_pct = len(df_reviews[df_reviews['sentiment']=='Positivo']) / total_reviews * 100
            negative_pct = len(df_reviews[df_reviews['sentiment']=='Negativo']) / total_reviews * 100
            
            col1.metric("Total de Reviews", total_reviews)
            col2.metric("Positivos", f"{positive_pct:.1f}%")
            col3.metric("Negativos", f"{negative_pct:.1f}%", delta_color="inverse")
            
            # Gráficos
            c1, c2 = st.columns(2)
            with c1:
                fig_pie = px.pie(df_reviews, names='sentiment', title="Distribuição de Sentimentos", hole=0.4)
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with c2:
                if 'category' in df_reviews.columns:
                    fig_bar = px.histogram(df_reviews, x='category', color='sentiment', barmode='group', title="Sentimento por Categoria")
                    st.plotly_chart(fig_bar, use_container_width=True)
            
            # Busca Semântica
            st.subheader("🔍 Buscador Semântico")
            texto = st.text_input("Digite um termo (ex: entrega, prazo):")
            if texto:
                # Tratamento para garantir que a busca não quebre com valores nulos
                filtrado = df_reviews[df_reviews['review_comment_message'].fillna('').str.contains(texto, case=False)]
                st.dataframe(filtrado[['category', 'sentiment', 'review_comment_message']].head(10))
        else:
            st.error("A coluna 'sentiment' não foi encontrada no CSV carregado. Verifique o arquivo.")

# Aba 2: Vendas (Gold)
with tab2:
    st.header("Análise de Vendas (Camada Gold)")
    if df_sales is not None:
        st.markdown("Visualizando as últimas transações padronizadas (CDM).")
        st.dataframe(df_sales.head(10))
        
        if 'TransactionAmount' in df_sales.columns:
            total_rev = df_sales['TransactionAmount'].sum()
            st.metric("Receita Total (Amostra)", f"R$ {total_rev:,.2f}")
    else:
        st.info("⚠️ Arquivo GOLD_SALES_ORDER_CDM.csv não encontrado.")

# Aba 3: Sobre o Projeto
with tab3:
    st.markdown("### Stack Tecnológico")
    st.markdown("""
    * **Linguagem:** Python 3.10+
    * **Framework:** Streamlit
    * **Visualização:** Plotly Express
    * **Origem:** Repositório GitHub (CI/CD)
    """)


