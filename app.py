# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np  # 👈 IMPORTANTE: Adicionar esta linha!
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
    # No Streamlit Cloud, o caminho é diferente
    # Primeiro, tenta encontrar o arquivo em vários locais possíveis
    possiveis_caminhos = [
        'dados_processados/fato_vendas.csv',
        'dados/fato_vendas.csv',
        'dados_processados/vendas.csv',
        'dados/vendas.csv',
        './dados_processados/fato_vendas.csv',
        './dados/fato_vendas.csv'
    ]

    for caminho in possiveis_caminhos:
        if os.path.exists(caminho):
            st.success(f"✅ Dados carregados de: {caminho}")
            return pd.read_csv(caminho)

    # Se não encontrar, mostrar aviso e usar dados de exemplo
    st.warning("""
    ⚠️ **Arquivo de dados não encontrado!** 

    Para usar seus dados reais, faça upload do arquivo `fato_vendas.csv` usando o botão abaixo.
    """)

    # Criar dados de exemplo para demonstração
    st.info("📊 **Usando dados de exemplo para demonstração**")

    # Criar datas de 2023-01-01 a 2023-04-10 (100 dias)
    datas = pd.date_range('2023-01-01', periods=100, freq='D')

    dados_exemplo = pd.DataFrame({
        'DATE_ID': datas,
        'SALES': np.random.randint(1000, 10000, 100),
        'QUANTITYORDERED': np.random.randint(1, 50, 100),
        'PRODUCT_ID': np.random.randint(1, 11, 100),
        'CUSTOMER_ID': np.random.randint(1, 21, 100)
    })

    return dados_exemplo


# Sidebar
with st.sidebar:
    st.header("⚙️ Configurações")

    # Upload de arquivo (opcional)
    uploaded_file = st.file_uploader(
        "📤 Ou faça upload do seu arquivo CSV",
        type=['csv']
    )

    if uploaded_file is not None:
        # Se o usuário fez upload, usar esse arquivo
        df = pd.read_csv(uploaded_file)
        st.success(f"✅ Arquivo carregado: {uploaded_file.name}")
    else:
        # Caso contrário, usar o carregamento padrão
        df = carregar_dados()

    # Mostrar informações dos dados
    st.subheader("📋 Informações do Dataset")
    st.write(f"**Registros:** {len(df)}")
    st.write(f"**Colunas:** {list(df.columns)}")

    # Pré-visualização dos dados
    with st.expander("👀 Pré-visualização dos dados"):
        st.dataframe(df.head())

    # Seleção de colunas
    st.subheader("🔧 Colunas para Análise")

    # Identificar colunas de data
    colunas_data = [col for col in df.columns if any(
        termo in col.lower() for termo in ['date', 'data', 'id', 'order']
    )]

    if not colunas_data:
        colunas_data = df.select_dtypes(include=['datetime64']).columns.tolist()

    coluna_data = st.selectbox(
        "📅 Coluna de Data",
        colunas_data if colunas_data else df.columns,
        index=0 if colunas_data else 0
    )

    # Identificar colunas de valor
    colunas_valor = [col for col in df.columns if any(
        termo in col.lower() for termo in ['sales', 'venda', 'price', 'total', 'quant']
    )]

    if not colunas_valor:
        colunas_valor = df.select_dtypes(include=['float64', 'int64']).columns.tolist()

    coluna_valor = st.selectbox(
        "💰 Coluna de Valor",
        colunas_valor if colunas_valor else df.columns,
        index=0 if colunas_valor else 0
    )

    # Período de análise
    periodo = st.selectbox(
        "📊 Período de Análise",
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

    # Converter data (tentativa inteligente)
    try:
        df_analise[coluna_data] = pd.to_datetime(df_analise[coluna_data])
    except:
        st.error(f"Não foi possível converter a coluna '{coluna_data}' para data.")
        st.stop()

    # Calcular crescimento
    periodo_sel = periodo_map[periodo]
    with st.spinner('🔄 Calculando crescimento...'):
        resultado = calcular_crescimento(
            df_analise,
            coluna_data=coluna_data,
            coluna_valor=coluna_valor,
            periodo=periodo_sel
        )

    st.success("✅ Análise concluída!")

    # Layout com colunas para métricas
    st.subheader("📈 Métricas de Crescimento")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        crescimento_medio = resultado['crescimento_%'].mean()
        st.metric(
            "📊 Crescimento Médio",
            f"{crescimento_medio:.1f}%" if not pd.isna(crescimento_medio) else "N/A"
        )

    with col2:
        ultimo_cresc = resultado['crescimento_%'].iloc[-1] if len(resultado) > 0 else None
        st.metric(
            "🔄 Último Período",
            f"{ultimo_cresc:.1f}%" if ultimo_cresc and not pd.isna(ultimo_cresc) else "N/A"
        )

    with col3:
        melhor_cresc = resultado['crescimento_%'].max()
        st.metric(
            "🏆 Melhor Período",
            f"{melhor_cresc:.1f}%" if not pd.isna(melhor_cresc) else "N/A"
        )

    with col4:
        pior_cresc = resultado['crescimento_%'].min()
        st.metric(
            "📉 Pior Período",
            f"{pior_cresc:.1f}%" if not pd.isna(pior_cresc) else "N/A"
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
            yaxis_title="Valor Total (R$)",
            hovermode='x unified'
        )
        st.plotly_chart(fig_vendas, use_container_width=True)

    with col2:
        st.subheader("📊 Taxa de Crescimento")
        # Criar coluna de cores baseada no valor
        resultado['cor'] = resultado['crescimento_%'].apply(
            lambda x: 'green' if x > 0 else 'red' if x < 0 else 'gray'
        )

        fig_cresc = px.bar(
            resultado.dropna(subset=['crescimento_%']),
            x=coluna_data,
            y='crescimento_%',
            title=f"Crescimento {periodo} (%)",
            color='cor',
            color_discrete_map={'green': '#2ecc71', 'red': '#e74c3c', 'gray': '#95a5a6'}
        )
        fig_cresc.update_layout(
            xaxis_title="Período",
            yaxis_title="Crescimento (%)",
            showlegend=False,
            hovermode='x unified'
        )
        st.plotly_chart(fig_cresc, use_container_width=True)

    st.markdown("---")

    # Tabela de resultados
    st.subheader("📋 Detalhamento dos Resultados")

    # Formatar tabela
    tabela = resultado.copy()
    tabela['total_vendas'] = tabela['total_vendas'].apply(lambda x: f"R$ {x:,.2f}")
    tabela['crescimento_%'] = tabela['crescimento_%'].apply(
        lambda x: f"{x:.2f}%" if pd.notna(x) else "-"
    )

    # Renomear colunas para melhor visualização
    tabela = tabela.rename(columns={
        coluna_data: 'Período',
        'total_vendas': 'Vendas Totais',
        'crescimento_%': 'Crescimento (%)'
    })

    st.dataframe(tabela, use_container_width=True, hide_index=True)

    # Download dos resultados
    csv = resultado.to_csv(index=False)
    st.download_button(
        label="📥 Download Resultados (CSV)",
        data=csv,
        file_name=f"crescimento_{periodo.lower()}.csv",
        mime="text/csv"
    )

    # Estatísticas adicionais
    with st.expander("📊 Estatísticas Detalhadas"):
        stats = resultado['crescimento_%'].describe()
        st.dataframe(stats.to_frame().T)

        # Melhor e pior período
        melhor_idx = resultado['crescimento_%'].idxmax()
        pior_idx = resultado['crescimento_%'].idxmin()

        st.write(f"**🏆 Melhor período:** {resultado.iloc[melhor_idx][coluna_data]} - "
                 f"Crescimento: {resultado.iloc[melhor_idx]['crescimento_%']:.2f}%")
        st.write(f"**📉 Pior período:** {resultado.iloc[pior_idx][coluna_data]} - "
                 f"Crescimento: {resultado.iloc[pior_idx]['crescimento_%']:.2f}%")

except Exception as e:
    st.error(f"❌ Erro na análise: {str(e)}")
    st.exception(e)  # Isso vai mostrar o erro completo para debug
    st.write("Verifique se as colunas selecionadas são apropriadas para a análise.")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        Desenvolvido com ❤️ usando Streamlit | 
        <a href='https://github.com/samuelmaiapro/analise-vendas-python' target='_blank'>GitHub</a>
    </div>
    """,
    unsafe_allow_html=True
)