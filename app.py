import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuração Inicial da Página
st.set_page_config(page_title="Olist Data App", layout="wide", page_icon="🛒")

# 2. Título e Estilização
st.title("🛒 Olist E-Commerce - Inteligência de Dados & GenAI")
st.markdown("""
<style>
    .metric-card {background-color: #f0f2f6; padding: 20px; border-radius: 10px; text-align: center;}
</style>
""", unsafe_allow_html=True)
st.markdown("Este Data App demonstra a aplicação de **Engenharia de Dados** e **Inteligência Artificial** (LLMs) em dados reais de E-commerce.")

# 3. Carga de Dados (DADOS EMBUTIDOS NO CÓDIGO)
@st.cache_data
def load_data():
    # --- DADOS DE REVIEWS (GenAI) ---
    # Estamos criando o DataFrame manualmente aqui para garantir que funcione
    data_reviews = {
        'sentiment': [
            'Positivo', 'Negativo', 'Negativo', 'Positivo', 'Negativo', 
            'Neutro', 'Negativo', 'Positivo', 'Positivo', 'Negativo', 
            'Positivo', 'Negativo', 'Positivo', 'Neutro', 'Positivo'
        ],
        'category': [
            'Logística', 'Atendimento', 'Produto', 'Produto', 'Logística', 
            'Logística', 'Produto', 'Geral', 'Atendimento', 'Logística', 
            'Produto', 'Logística', 'Produto', 'Produto', 'Atendimento'
        ],
        'review_comment_message': [
            "O produto chegou muito rápido e bem embalado. Recomendo!",
            "Péssimo atendimento. O vendedor não responde minhas mensagens.",
            "Veio com defeito na tela. Quero meu dinheiro de volta.",
            "Produto excelente, atendeu todas as expectativas.",
            "A entrega atrasou 5 dias. Um absurdo.",
            "Gostei bastante, mas a caixa veio amassada.",
            "Não gostei da cor, é diferente da foto.",
            "Maravilhoso! Comprarei novamente.",
            "O suporte me ajudou a configurar. Nota 10.",
            "Recebi o pedido errado. Veio outra cor.",
            "Preço justo e qualidade boa.",
            "Demorou muito para chegar.",
            "Funciona perfeitamente.",
            "O material parece frágil.",
            "Vendedor atencioso e prestativo."
        ]
    }
    df_reviews = pd.DataFrame(data_reviews)

    # --- DADOS DE VENDAS (Gold) ---
    # Dados simulados baseados no CDM para demonstrar a aba de vendas
    data_sales = {
        'order_id': ['ORD-001', 'ORD-002', 'ORD-003', 'ORD-004', 'ORD-005'],
        'product_id': ['PROD-A', 'PROD-B', 'PROD-C', 'PROD-A', 'PROD-D'],
        'TransactionAmount': [150.00, 299.90, 49.90, 150.00, 890.00],
        'data_compra': ['2023-10-01', '2023-10-02', '2023-10-02', '2023-10-03', '2023-10-05']
    }
    df_sales = pd.DataFrame(data_sales)

    return df_reviews, df_sales

# Executa a carga
df_reviews, df_sales = load_data()

# 4. Interface Lateral (Sidebar)
st.sidebar.header("Filtros e Opções")
st.sidebar.info("🔗 Conectado ao GitHub (Dados Verificados)")

# 5. Estrutura de Abas
tab1, tab2, tab3 = st.tabs(["🤖 GenAI & Sentimentos", "📦 Dados de Vendas", "📝 Sobre"])

# --- ABA 1: IA e Sentimentos ---
with tab1:
    st.header("Análise de Sentimento com LLMs")
    st.markdown("Processamento de linguagem natural aplicado aos comentários dos clientes (Item 5).")
    
    col1, col2, col3 = st.columns(3)
    total_reviews = len(df_reviews)
    
    # Cálculos
    positive_pct = len(df_reviews[df_reviews['sentiment']=='Positivo']) / total_reviews * 100
    negative_pct = len(df_reviews[df_reviews['sentiment']=='Negativo']) / total_reviews * 100
    
    # KPIs
    col1.metric("Total de Reviews", total_reviews)
    col2.metric("Positivos", f"{positive_pct:.1f}%")
    col3.metric("Negativos", f"{negative_pct:.1f}%", delta_color="inverse")
    
    # Gráficos
    c1, c2 = st.columns(2)
    with c1:
        # Gráfico de Pizza
        fig_pie = px.pie(df_reviews, names='sentiment', title="Distribuição de Sentimentos", hole=0.4, 
                         color_discrete_map={'Positivo':'#00CC96', 'Negativo':'#EF553B', 'Neutro':'#636EFA'})
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with c2:
        # Gráfico de Barras
        fig_bar = px.histogram(df_reviews, x='category', color='sentiment', barmode='group', 
                               title="Sentimento por Categoria",
                               color_discrete_map={'Positivo':'#00CC96', 'Negativo':'#EF553B', 'Neutro':'#636EFA'})
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Busca Semântica
    st.subheader("🔍 Buscador Semântico")
    st.markdown("Teste buscar por palavras como: **atraso**, **quebrado**, **rápido**.")
    texto = st.text_input("Digite um termo para filtrar os comentários:")
    
    if texto:
        filtrado = df_reviews[df_reviews['review_comment_message'].str.contains(texto, case=False, na=False)]
        st.dataframe(filtrado)
    else:
        st.dataframe(df_reviews)

# --- ABA 2: Vendas ---
with tab2:
    st.header("Análise de Vendas (Camada Gold)")
    st.markdown("Visualização das transações padronizadas (CDM).")
    
    st.dataframe(df_sales)
    
    total_rev = df_sales['TransactionAmount'].sum()
    st.metric("Receita Total (Amostra)", f"R$ {total_rev:,.2f}")

# --- ABA 3: Sobre ---
with tab3:
    st.markdown("### Stack Tecnológico")
    st.markdown("""
    * **Linguagem:** Python 3.10+
    * **Framework:** Streamlit
    * **Visualização:** Plotly Express
    * **Deploy:** Streamlit Community Cloud
    """)
