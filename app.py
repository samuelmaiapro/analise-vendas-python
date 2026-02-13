# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scripts.analise_crescimento import calcular_crescimento
import os

# Configuração da página
st.set_page_config(
    page_title="Análise de Vendas",
    page_icon="📊",
    layout="wide"
)

# Título
st.title("📊 Dashboard de Análise de Vendas")
st.markdown("---")


# Função para carregar dados
@st.cache_data
def carregar_dados():
    # Procurar arquivo de vendas
    possiveis_caminhos = [
        'dados_processados/fato_vendas.csv',
        'dados/fato_vendas.csv',
        'dados_processados/vendas.csv',
        'dados/vendas.csv'
    ]

    for caminho in possiveis_caminhos:
        if os.path.exists(caminho):
            return pd.read_csv(caminho)

    # Se não encontrar, usar dados de exemplo
    st.warning("Arquivo de dados não encontrado. Usando dados de exemplo.")
    return pd.DataFrame({
        'DATE_ID': pd.date_range('2023-01-01', periods=100, freq='D'),
        'SALES': np.random.randint(1000, 10000, 100),
        'PRODUCT_ID': np.random.randint(1, 10, 100),
        'CUSTOMER_ID': np.random.randint(1, 20, 100)
    })


# Sidebar
with st.sidebar:
    st.header("⚙️ Configurações")

    # Carregar dados
    df = carregar_dados()

    # Mostrar informações dos dados
    st.subheader("📋 Informações do Dataset")
    st.write(f"**Registros:** {len(df)}")
    st.write(f"**Colunas:** {list(df.columns)}")

    # Seleção de colunas
    st.subheader("🔧 Colunas para Análise")

    # Identificar colunas de data
    colunas_data = [col for col in df.columns if any(
        termo in col.lower() for termo in ['date', 'data', 'id']
    )]
    coluna_data = st.selectbox(
        "Coluna de Data",
        colunas_data,
        index=0 if colunas_data else 0
    )

    # Identificar colunas de valor
    colunas_valor = [col for col in df.columns if any(
        termo in col.lower() for termo in ['sales', 'venda', 'price', 'total']
    )]
    coluna_valor = st.selectbox(
        "Coluna de Valor",
        colunas_valor,
        index=0 if colunas_valor else 0
    )

    # Período de análise
    periodo = st.selectbox(
        "Período de Análise",
        ["Mensal", "Trimestral", "Anual"],
        index=0
    )

    periodo_map = {
        "Mensal": "M",
        "Trimestral": "T",
        "Anual": "A"
    }

# Main content
try:
    # Preparar dados
    df_analise = df.copy()

    # Converter data
    df_analise[coluna_data] = pd.to_datetime(df_analise[coluna_data])

    # Calcular crescimento
    periodo_sel = periodo_map[periodo]
    resultado = calcular_crescimento(
        df_analise,
        coluna_data=coluna_data,
        coluna_valor=coluna_valor,
        periodo=periodo_sel
    )

    # Layout com colunas
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "📈 Crescimento Médio",
            f"{resultado['crescimento_%'].mean():.1f}%",
            delta=f"{resultado['crescimento_%'].iloc[-1]:.1f}% (último período)"
        )

    with col2:
        st.metric(
            "🏆 Melhor Crescimento",
            f"{resultado['crescimento_%'].max():.1f}%"
        )

    with col3:
        st.metric(
            "📉 Pior Crescimento",
            f"{resultado['crescimento_%'].min():.1f}%"
        )

    st.markdown("---")

    # Gráficos
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("💰 Vendas por Período")
        fig_vendas = px.line(
            resultado,
            x=coluna_data,
            y='total_vendas',
            markers=True,
            title=f"Vendas {periodo}"
        )
        fig_vendas.update_layout(
            xaxis_title="Período",
            yaxis_title="Valor Total (R$)"
        )
        st.plotly_chart(fig_vendas, use_container_width=True)

    with col2:
        st.subheader("📊 Taxa de Crescimento")
        cores = ['green' if x > 0 else 'red' for x in resultado['crescimento_%'].fillna(0)]
        fig_cresc = px.bar(
            resultado,
            x=coluna_data,
            y='crescimento_%',
            title=f"Crescimento {periodo} (%)",
            color=cores
        )
        fig_cresc.update_layout(
            xaxis_title="Período",
            yaxis_title="Crescimento (%)"
        )
        st.plotly_chart(fig_cresc, use_container_width=True)

    st.markdown("---")

    # Tabela de resultados
    st.subheader("📋 Detalhamento dos Resultados")

    # Formatar tabela
    tabela = resultado.copy()
    tabela['total_vendas'] = tabela['total_vendas'].apply(lambda x: f"R$ {x:,.2f}")
    tabela['crescimento_%'] = tabela['crescimento_%'].apply(lambda x: f"{x:.2f}%" if pd.notna(x) else "-")

    st.dataframe(tabela, use_container_width=True)

    # Download dos resultados
    csv = resultado.to_csv(index=False)
    st.download_button(
        label="📥 Download Resultados (CSV)",
        data=csv,
        file_name=f"crescimento_{periodo.lower()}.csv",
        mime="text/csv"
    )

except Exception as e:
    st.error(f"Erro na análise: {str(e)}")
    st.write("Verifique se as colunas selecionadas são apropriadas para a análise.")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center'>"
    "Desenvolvido com ❤️ usando Streamlit | Dados de Vendas"
    "</div>",
    unsafe_allow_html=True
)