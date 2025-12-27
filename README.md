# 🚀 Case Técnico Dadosfera - Engenharia de Dados

**Candidata:** Amanda Aiko
**Data:** Dezembro/2025
**Objetivo:** Construção de uma Plataforma de Dados E2E (End-to-End) para E-commerce.

---

## 🗄️ Item 1 - Seleção da Base de Dados

* **Base Escolhida:** Brazilian E-Commerce Public Dataset by Olist
* **Fonte:** [Kaggle - Olist Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

### Justificativa da Escolha
Para atender ao desafio de construir uma Plataforma de Dados robusta, selecionei o dataset da Olist. Esta escolha foi estratégica por três motivos principais:

1.  **Volumetria e Robustez:** Contém mais de **100.000 pedidos** (2016-2018), superando o requisito técnico e permitindo análises temporais densas.
2.  **Aderência à Narrativa:** Cobre todos os desafios sugeridos:
    * *Logística:* Dados de geolocalização, CEP e prazos (Estimado vs Real).
    * *Desempenho:* Avaliação de vendedores e produtos.
    * *Dados Desestruturados:* Tabela de reviews com comentários reais para NLP/IA.
3.  **Estrutura Relacional:** Dados normalizados em 9 tabelas, ideais para demonstrar modelagem (Star Schema) e SQL complexo.

---

## ⚙️ Item 2.1 - Integração e Ingestão de Dados

Realizei a ingestão dos dados na plataforma Dadosfera, focando na tabela fato principal (`olist_order_items`) e nas dimensões satélites.

* **Status da Carga:** Sucesso ✅
* **Volumetria:** 112.650 registros (Requisito > 100k atingido).

### Estratégia de Data Quality na Origem
Para garantir a integridade do schema (*Schema-on-Write*), identifiquei que a ingestão padrão de CSV poderia falhar na tipagem. Realizei um **pré-processamento via Google Sheets**:
* Formatação nativa de `shipping_limit_date` para **Datetime**.
* Formatação de `price` e `freight_value` para **Decimal**.

Isso eliminou a necessidade de *casting* complexo e acelerou a disponibilidade dos dados na camada Silver.

**Evidência do Pipeline:**
![Pipeline de Ingestão](assets/image_pipeline_sucesso.png)

---

## 📚 Item 3 - Exploração e Governança (Data Lake)

Organizei o Data Lake seguindo a **Arquitetura Medalhão (Medallion Architecture)** e os princípios FAIR (Findable, Accessible, Interoperable, Reusable).

### 1. Zonas de Dados
Classifiquei os ativos utilizando Tags na plataforma:

* 🥉 **Camada Bronze (Landing Zone):** Dados brutos em formato original.
    * *Tags:* `LAKE:LANDING`, `BRONZE`.
* 🥈 **Camada Silver (Standardized):** Dados tipados e limpos.
    * *Tag Planejada:* `LAKE:SILVER`.
* 🥇 **Camada Gold (Curated):** Dados modelados (Star Schema) para BI.
    * *Tag Planejada:* `LAKE:GOLD`.

### 2. Dicionário de Dados
Cataloguei manualmente os ativos na Dadosfera:

* **`PUBLIC.OLIST_ORDER_ITEMS_DATASET` (Fato):** Documentação de colunas financeiras e conversão de tipos.
* **`PUBLIC.OLIST_PRODUCTS_DATASET` (Dimensão):** Mapeamento de categorias e dados logísticos (peso/medidas).
* **`PUBLIC.OLIST_CUSTOMERS_DATASET` (Dimensão):** Identificação de chaves geográficas para análise espacial.
* **`PUBLIC.OLIST_ORDER_REVIEWS_DATASET` (Desestruturado):** Identificação de texto livre para GenAI.

---

## ✅ Item 4 - Data Quality & CDM

**Estratégia:** Utilizei a biblioteca **Great Expectations** para validar a camada Bronze antes da promoção para Silver, garantindo confiabilidade para os modelos de IA.

### Regras Implementadas (Expectation Suite)
* **Completeness:** `order_id` e `product_id` não podem ser nulos.
* **Validity:** `price` e `freight_value` devem ser positivos (> 0).
* **Consistency:** `seller_id` deve ser do tipo string.

**Resultado:** Sucesso na validação (100%).

### Evidências Técnicas
* 📄 **Notebook:** [Ver Código de Validação](notebooks/data
