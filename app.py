# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from scripts.analise_crescimento import calcular_crescimento
import os
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Análise de Vendas - Samuel Maia",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #FF4B4B;
        text-align: center;
        margin-bottom: 0;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-top: 0;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #FF4B4B;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #666;
        text-transform: uppercase;
    }
    .info-text {
        background-color: #e7f3ff;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #0066cc;
    }
</style>
""", unsafe_allow_html=True)

# Cabeçalho
st.markdown("<h1 class='main-header'>📊 Análise de Vendas</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>Dashboard interativo para análise de crescimento e performance</p>",
            unsafe_allow_html=True)


# Função para criar dados de exemplo MAIS REALISTAS
@st.cache_data
def criar_dados_exemplo():
    """Cria dados de exemplo que parecem reais"""
    np.random.seed(42)  # Para reprodutibilidade

    # Criar datas de 2023-01-01 a 2024-12-31 (2 anos)
    datas = pd.date_range('2023-01-01', '2024-12-31', freq='D')

    # Tendência de crescimento + sazonalidade
    tendencia = np.linspace(1000, 2000, len(datas))
    sazonalidade = 500 * np.sin(2 * np.pi * np.arange(len(datas)) / 365)  # Ciclo anual
    ruido = np.random.normal(0, 100, len(datas))

    vendas = tendencia + sazonalidade + ruido
    vendas = np.maximum(vendas, 500)  # Não permitir valores negativos

    # Produtos e clientes
    produtos = [f'PROD_{i:03d}' for i in range(1, 21)]
    clientes = [f'CLI_{i:03d}' for i in range(1, 51)]

    dados_exemplo = pd.DataFrame({
        'DATA': datas,
        'VENDAS': vendas.astype(int),
        'QUANTIDADE': np.random.randint(1, 50, len(datas)),
        'PRODUTO': np.random.choice(produtos, len(datas)),
        'CLIENTE': np.random.choice(clientes, len(datas)),
        'CATEGORIA': np.random.choice(['Eletrônicos', 'Móveis', 'Roupas', 'Livros'], len(datas))
    })

    return dados_exemplo


@st.cache_data
def carregar_dados():
    """Carrega dados do arquivo ou usa exemplo"""

    # Tentar encontrar dados reais
    possiveis_caminhos = [
        'dados_processados/fato_vendas.csv',
        'dados/fato_vendas.csv',
        './dados_processados/fato_vendas.csv',
        './dados/fato_vendas.csv'
    ]

    for caminho in possiveis_caminhos:
        if os.path.exists(caminho):
            df = pd.read_csv(caminho)
            st.sidebar.success(f"✅ Dados reais carregados: {len(df)} registros")
            return df, True

    # Se não encontrar, usar dados de exemplo REALISTAS
    st.sidebar.info("ℹ️ Usando dados de exemplo (simulados)")
    return criar_dados_exemplo(), False


# Sidebar
with st.sidebar:
    st.markdown("## ⚙️ Configurações")

    # Upload de arquivo
    uploaded_file = st.file_uploader(
        "📤 Upload seu CSV",
        type=['csv'],
        help="Faça upload do seu arquivo de vendas"
    )

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        dados_reais = True
        st.success(f"✅ Arquivo carregado: {uploaded_file.name}")
    else:
        df, dados_reais = carregar_dados()

    st.markdown("---")

    # Informações do dataset
    st.markdown("### 📋 Sobre os dados")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Registros", f"{len(df):,}")
    with col2:
        st.metric("Colunas", len(df.columns))

    # Tipo de dados
    tipo_dados = "**Dados Reais**" if dados_reais else "**Dados de Exemplo**"
    st.markdown(f"Tipo: {tipo_dados}")

    st.markdown("---")

    # Configurações de análise
    st.markdown("### 🔧 Análise")

    # Identificar colunas automaticamente
    colunas = df.columns.tolist()

    # Coluna de data
    data_options = [col for col in colunas if any(
        termo in col.lower() for termo in ['date', 'data', 'dia', 'mes']
    )] or colunas

    coluna_data = st.selectbox(
        "📅 Coluna de data",
        data_options,
        index=0
    )

    # Coluna de valor
    valor_options = [col for col in colunas if any(
        termo in col.lower() for termo in ['sales', 'venda', 'price', 'total', 'valor']
    )] or df.select_dtypes(include=[np.number]).columns.tolist()

    coluna_valor = st.selectbox(
        "💰 Coluna de valor",
        valor_options,
        index=0 if valor_options else 0
    )

    # Período
    periodo = st.selectbox(
        "📊 Período",
        ["Mensal", "Trimestral", "Anual"],
        index=0
    )

    periodo_map = {
        "Mensal": "M",
        "Trimestral": "T",
        "Anual": "A"
    }

# MAIN CONTENT
try:
    # Preparar dados
    df_analise = df.copy()

    # Converter data
    df_analise[coluna_data] = pd.to_datetime(df_analise[coluna_data], errors='coerce')
    df_analise = df_analise.dropna(subset=[coluna_data])

    # Calcular crescimento
    with st.spinner('🔄 Calculando análise...'):
        resultado = calcular_crescimento(
            df_analise,
            coluna_data=coluna_data,
            coluna_valor=coluna_valor,
            periodo=periodo_map[periodo]
        )

    st.success("✅ Análise concluída!")

    # Métricas principais
    st.markdown("## 📈 Métricas de Crescimento")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        crescimento_medio = resultado['crescimento_%'].mean()
        delta = resultado['crescimento_%'].iloc[-1] - resultado['crescimento_%'].iloc[-2] if len(resultado) > 1 else 0
        st.metric(
            "Crescimento Médio",
            f"{crescimento_medio:.1f}%" if not pd.isna(crescimento_medio) else "N/A",
            delta=f"{delta:.1f} pp" if not pd.isna(delta) else None
        )

    with col2:
        ultimo_valor = resultado['total_vendas'].iloc[-1] if len(resultado) > 0 else 0
        st.metric(
            "Último Período",
            f"R$ {ultimo_valor:,.0f}".replace(',', '.')
        )

    with col3:
        melhor_cresc = resultado['crescimento_%'].max()
        melhor_periodo = resultado.loc[resultado['crescimento_%'].idxmax(), coluna_data] if not pd.isna(
            melhor_cresc) else "N/A"
        st.metric(
            "Melhor Período",
            f"{melhor_cresc:.1f}%" if not pd.isna(melhor_cresc) else "N/A",
            delta=f"em {melhor_periodo}" if melhor_periodo != "N/A" else None
        )

    with col4:
        pior_cresc = resultado['crescimento_%'].min()
        pior_periodo = resultado.loc[resultado['crescimento_%'].idxmin(), coluna_data] if not pd.isna(
            pior_cresc) else "N/A"
        st.metric(
            "Pior Período",
            f"{pior_cresc:.1f}%" if not pd.isna(pior_cresc) else "N/A",
            delta=f"em {pior_periodo}" if pior_periodo != "N/A" else None
        )

    st.markdown("---")

    # Gráficos
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 💰 Evolução das Vendas")

        fig_vendas = px.line(
            resultado,
            x=coluna_data,
            y='total_vendas',
            markers=True,
            line_shape='spline',
            template='plotly_white'
        )

        # Adicionar área sob a linha
        fig_vendas.add_trace(
            go.Scatter(
                x=resultado[coluna_data],
                y=resultado['total_vendas'],
                fill='tozeroy',
                fillcolor='rgba(255, 75, 75, 0.1)',
                line=dict(color='rgba(255, 75, 75, 0)'),
                showlegend=False,
                hoverinfo='skip'
            )
        )

        fig_vendas.update_layout(
            xaxis_title="Período",
            yaxis_title="Valor Total (R$)",
            hovermode='x unified',
            height=400
        )

        st.plotly_chart(fig_vendas, use_container_width=True)

    with col2:
        st.markdown("### 📊 Taxa de Crescimento")

        # Cores baseadas no valor
        resultado['cor'] = resultado['crescimento_%'].apply(
            lambda x: '#2ecc71' if x > 0 else '#e74c3c' if x < 0 else '#95a5a6'
        )

        fig_cresc = px.bar(
            resultado.dropna(subset=['crescimento_%']),
            x=coluna_data,
            y='crescimento_%',
            color='cor',
            color_discrete_map='identity',
            template='plotly_white'
        )

        fig_cresc.update_layout(
            xaxis_title="Período",
            yaxis_title="Crescimento (%)",
            showlegend=False,
            height=400
        )

        # Adicionar linha em zero
        fig_cresc.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)

        st.plotly_chart(fig_cresc, use_container_width=True)

    st.markdown("---")

    # Análises adicionais
    tab1, tab2, tab3 = st.tabs(["📋 Dados Detalhados", "📊 Estatísticas", "ℹ️ Sobre"])

    with tab1:
        st.markdown("### Tabela de Resultados")

        # Formatar tabela
        tabela = resultado.copy()
        tabela['total_vendas'] = tabela['total_vendas'].apply(
            lambda x: f"R$ {x:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
        tabela['crescimento_%'] = tabela['crescimento_%'].apply(
            lambda x: f"{x:.2f}%" if pd.notna(x) else "-"
        )

        # Renomear colunas
        tabela = tabela.rename(columns={
            coluna_data: 'Período',
            'total_vendas': 'Vendas Totais',
            'crescimento_%': 'Crescimento'
        })

        st.dataframe(
            tabela,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Período": st.column_config.DateColumn("Período"),
                "Vendas Totais": st.column_config.TextColumn("Vendas Totais"),
                "Crescimento": st.column_config.TextColumn("Crescimento")
            }
        )

        # Download
        csv = resultado.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"analise_vendas_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

    with tab2:
        st.markdown("### Estatísticas Descritivas")

        stats = resultado['crescimento_%'].describe()
        stats_df = pd.DataFrame({
            'Estatística': ['Média', 'Desvio Padrão', 'Mínimo', '25%', '50%', '75%', 'Máximo'],
            'Valor': [
                f"{stats['mean']:.2f}%" if not pd.isna(stats['mean']) else "N/A",
                f"{stats['std']:.2f}%" if not pd.isna(stats['std']) else "N/A",
                f"{stats['min']:.2f}%" if not pd.isna(stats['min']) else "N/A",
                f"{stats['25%']:.2f}%" if not pd.isna(stats['25%']) else "N/A",
                f"{stats['50%']:.2f}%" if not pd.isna(stats['50%']) else "N/A",
                f"{stats['75%']:.2f}%" if not pd.isna(stats['75%']) else "N/A",
                f"{stats['max']:.2f}%" if not pd.isna(stats['max']) else "N/A"
            ]
        })

        st.dataframe(stats_df, hide_index=True, use_container_width=True)

        # Períodos extremos
        st.markdown("### Períodos de Destaque")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**🏆 Top 3 Melhores Crescimentos**")
            top3 = resultado.nlargest(3, 'crescimento_%')[['total_vendas', 'crescimento_%']]
            st.dataframe(top3, use_container_width=True)

        with col2:
            st.markdown("**📉 Top 3 Piores Crescimentos**")
            bottom3 = resultado.nsmallest(3, 'crescimento_%')[['total_vendas', 'crescimento_%']]
            st.dataframe(bottom3, use_container_width=True)

    with tab3:
        st.markdown("### Sobre esta Análise")

        st.markdown("""
        **Dashboard desenvolvido para análise de vendas**

        **Funcionalidades:**
        - 📈 Cálculo automático de crescimento periódico
        - 📊 Visualizações interativas
        - 📋 Exportação de dados
        - 🔄 Suporte a diferentes períodos (mensal, trimestral, anual)

        **Como usar:**
        1. Faça upload do seu arquivo CSV ou use dados de exemplo
        2. Selecione as colunas corretas para data e valor
        3. Escolha o período de análise
        4. Explore os resultados!

        **Autor:** Samuel Maia
        **Projeto:** [GitHub](https://github.com/samuelmaiapro/analise-vendas-python)
        """)

        if not dados_reais:
            st.info("💡 **Dica:** Para uma análise mais precisa, faça upload do seu arquivo de vendas real!")

except Exception as e:
    st.error(f"❌ Erro na análise: {str(e)}")
    st.exception(e)

# Footer
st.markdown("---")
st.markdown(
    f"""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        Desenvolvido por <a href='https://github.com/samuelmaiapro' target='_blank'>Samuel Maia</a> | 
        Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M')}
    </div>
    """,
    unsafe_allow_html=True
)