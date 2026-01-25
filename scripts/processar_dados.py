"""
📊 SCRIPT DE PROCESSAMENTO PARA POWER BI
Processa dados de vendas e exporta formatos otimizados
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os
import json


def configurar_ambiente():
    """Cria estrutura de pastas necessária"""
    pastas = ['../dados_processados', '../powerbi/queries']
    for pasta in pastas:
        os.makedirs(pasta, exist_ok=True)
    print("✅ Ambiente configurado")


def carregar_dados():
    """Carrega e limpa os dados originais"""
    print("📥 Carregando dados...")
    df = pd.read_csv('../dados/sales_data_sample.csv', encoding='latin-1')

    # Converter datas
    df['ORDERDATE'] = pd.to_datetime(df['ORDERDATE'])

    # Criar colunas derivadas
    df['ANO'] = df['ORDERDATE'].dt.year
    df['MES'] = df['ORDERDATE'].dt.month
    df['MES_NOME'] = df['ORDERDATE'].dt.strftime('%B')
    df['TRIMESTRE'] = df['ORDERDATE'].dt.quarter
    df['DIA_SEMANA'] = df['ORDERDATE'].dt.day_name()
    df['SEMANA_ANO'] = df['ORDERDATE'].dt.isocalendar().week

    print(f"✅ Dados carregados: {df.shape[0]} linhas, {df.shape[1]} colunas")
    return df


def criar_tabelas_dimensao(df):
    """Cria tabelas de dimensão para modelo estrela"""
    print("🔷 Criando tabelas de dimensão...")

    # Dimensão Produtos
    dim_produtos = df[['PRODUCTCODE', 'PRODUCTLINE', 'MSRP']].drop_duplicates()
    dim_produtos['PRODUCT_ID'] = range(1, len(dim_produtos) + 1)

    # Dimensão Clientes
    dim_clientes = df[[
        'CUSTOMERNAME', 'COUNTRY', 'CITY', 'STATE',
        'POSTALCODE', 'TERRITORY', 'PHONE'
    ]].drop_duplicates()
    dim_clientes['CUSTOMER_ID'] = range(1, len(dim_clientes) + 1)

    # Dimensão Tempo
    datas_unicas = df['ORDERDATE'].drop_duplicates()
    dim_tempo = pd.DataFrame({
        'DATA': datas_unicas,
        'ANO': datas_unicas.dt.year,
        'MES': datas_unicas.dt.month,
        'MES_NOME': datas_unicas.dt.strftime('%B'),
        'TRIMESTRE': datas_unicas.dt.quarter,
        'DIA': datas_unicas.dt.day,
        'DIA_SEMANA': datas_unicas.dt.day_name(),
        'SEMANA_ANO': datas_unicas.dt.isocalendar().week,
        'FIM_SEMANA': datas_unicas.dt.dayofweek >= 5
    })
    dim_tempo['DATE_ID'] = range(1, len(dim_tempo) + 1)

    return dim_produtos, dim_clientes, dim_tempo


def criar_tabela_fato(df, dim_produtos, dim_clientes, dim_tempo):
    """Cria tabela fato com chaves estrangeiras"""
    print("🔶 Criando tabela fato...")

    # Criar dicionários de mapeamento
    produto_map = dict(zip(dim_produtos['PRODUCTCODE'], dim_produtos['PRODUCT_ID']))
    cliente_map = dict(zip(dim_clientes['CUSTOMERNAME'], dim_clientes['CUSTOMER_ID']))
    tempo_map = dict(zip(dim_tempo['DATA'], dim_tempo['DATE_ID']))

    # Criar tabela fato
    fato_vendas = df.copy()

    # Adicionar chaves estrangeiras
    fato_vendas['PRODUCT_ID'] = fato_vendas['PRODUCTCODE'].map(produto_map)
    fato_vendas['CUSTOMER_ID'] = fato_vendas['CUSTOMERNAME'].map(cliente_map)
    fato_vendas['DATE_ID'] = fato_vendas['ORDERDATE'].map(tempo_map)

    # Selecionar colunas relevantes
    colunas_fato = [
        'ORDERNUMBER', 'ORDERLINENUMBER', 'DATE_ID', 'PRODUCT_ID', 'CUSTOMER_ID',
        'QUANTITYORDERED', 'PRICEEACH', 'SALES', 'STATUS', 'DEALSIZE'
    ]

    return fato_vendas[colunas_fato]


def exportar_para_powerbi(fato_vendas, dim_produtos, dim_clientes, dim_tempo):
    """Exporta dados em formatos compatíveis com Power BI"""
    print("💾 Exportando dados para Power BI...")

    # 1. CSV (formato universal)
    fato_vendas.to_csv('../dados_processados/fato_vendas.csv', index=False)
    dim_produtos.to_csv('../dados_processados/dim_produtos.csv', index=False)
    dim_clientes.to_csv('../dados_processados/dim_clientes.csv', index=False)
    dim_tempo.to_csv('../dados_processados/dim_tempo.csv', index=False)

    # 2. Excel (opcional)
    with pd.ExcelWriter('../dados_processados/modelo_vendas.xlsx') as writer:
        fato_vendas.to_excel(writer, sheet_name='FATO_VENDAS', index=False)
        dim_produtos.to_excel(writer, sheet_name='DIM_PRODUTOS', index=False)
        dim_clientes.to_excel(writer, sheet_name='DIM_CLIENTES', index=False)
        dim_tempo.to_excel(writer, sheet_name='DIM_TEMPO', index=False)

    # 3. Parquet (formato otimizado)
    fato_vendas.to_parquet('../dados_processados/fato_vendas.parquet', index=False)

    # 4. JSON com metadados
    metadata = {
        "gerado_em": datetime.now().isoformat(),
        "tabelas": {
            "fato_vendas": len(fato_vendas),
            "dim_produtos": len(dim_produtos),
            "dim_clientes": len(dim_clientes),
            "dim_tempo": len(dim_tempo)
        },
        "periodo": {
            "inicio": str(dim_tempo['DATA'].min()),
            "fim": str(dim_tempo['DATA'].max())
        }
    }

    with open('../dados_processados/metadata.json', 'w') as f:
        json.dump(metadata, f, indent=4)

    print("✅ Dados exportados com sucesso!")


def criar_queries_powerbi():
    """Cria queries M (Power Query) para automatizar importação"""
    print("⚡ Criando queries Power BI...")

    query_template = """
let
    // Configuração
    caminho_base = "{caminho_absoluto}",

    // Carregar tabela FATO
    FonteFato = Csv.Document(
        File.Contents(caminho_base & "\\fato_vendas.csv"),
        [Delimiter=",", Columns=10, Encoding=65001, QuoteStyle=QuoteStyle.None]
    ),
    #"Promoted Headers" = Table.PromoteHeaders(FonteFato, [PromoteAllScalars=true]),

    // Carregar DIMENSÕES
    Produtos = Csv.Document(
        File.Contents(caminho_base & "\\dim_produtos.csv"),
        [Delimiter=",", Columns=4, Encoding=65001]
    ),
    #"ProdutosHeaders" = Table.PromoteHeaders(Produtos, [PromoteAllScalars=true]),

    Clientes = Csv.Document(
        File.Contents(caminho_base & "\\dim_clientes.csv"),
        [Delimiter=",", Columns=8, Encoding=65001]
    ),
    #"ClientesHeaders" = Table.PromoteHeaders(Clientes, [PromoteAllScalars=true]),

    Tempo = Csv.Document(
        File.Contents(caminho_base & "\\dim_tempo.csv"),
        [Delimiter=",", Columns=9, Encoding=65001]
    ),
    #"TempoHeaders" = Table.PromoteHeaders(Tempo, [PromoteAllScalars=true]),

    // Criar relacionamentos
    #"Modelo Estrela" = 
        Table.NestedJoin(
            #"Promoted Headers", "PRODUCT_ID", 
            #"ProdutosHeaders", "PRODUCT_ID", 
            "Produtos", JoinKind.LeftOuter
        )
in
    #"Modelo Estrela"
"""

    # Substituir caminho absoluto
    caminho_absoluto = os.path.abspath('../dados_processados').replace('\\', '\\\\')
    query_final = query_template.format(caminho_absoluto=caminho_absoluto)

    with open('../powerbi/queries/importacao_python.m', 'w', encoding='utf-8') as f:
        f.write(query_final)

    print("✅ Query Power BI criada!")


def main():
    """Função principal"""
    print("=" * 50)
    print("🚀 PROCESSAMENTO PARA POWER BI")
    print("=" * 50)

    try:
        # 1. Configurar ambiente
        configurar_ambiente()

        # 2. Carregar dados
        df = carregar_dados()

        # 3. Criar modelo estrela
        dim_produtos, dim_clientes, dim_tempo = criar_tabelas_dimensao(df)
        fato_vendas = criar_tabela_fato(df, dim_produtos, dim_clientes, dim_tempo)

        # 4. Exportar
        exportar_para_powerbi(fato_vendas, dim_produtos, dim_clientes, dim_tempo)

        # 5. Criar queries
        criar_queries_powerbi()

        # 6. Resumo
        print("\n" + "=" * 50)
        print("📊 RESUMO DO PROCESSAMENTO")
        print("=" * 50)
        print(f"📁 Pasta de dados: {os.path.abspath('../dados_processados')}")
        print(f"📈 Total de vendas: ${fato_vendas['SALES'].sum():,.2f}")
        print(f"📦 Transações: {len(fato_vendas):,}")
        print(f"👥 Clientes únicos: {len(dim_clientes):,}")
        print(f"🏷️  Produtos únicos: {len(dim_produtos):,}")
        print("=" * 50)
        print("✅ PRONTO PARA IMPORTAR NO POWER BI!")

    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()