"""
📊 PROCESSADOR FINAL - USA PASTA DA RAIZ
Gera dados NA pasta dados_processados da raiz
"""
import pandas as pd
import os
from datetime import datetime

print("=" * 60)
print("🚀 PROCESSADOR PARA POWER BI - VERSÃO FINAL")
print("=" * 60)

# 1. DEFINIR CAMINHOS CORRETOS
print("\n📍 DEFININDO CAMINHOS...")

# Raiz do projeto (onde está README.md)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(f"Raiz do projeto: {PROJECT_ROOT}")

# Caminhos de entrada/saída
INPUT_CSV = os.path.join(PROJECT_ROOT, 'dados', 'sales_data_sample.csv')
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'dados_processados')

print(f"Arquivo de entrada: {INPUT_CSV}")
print(f"Pasta de saída: {OUTPUT_DIR}")

# 2. CRIAR PASTA SE NÃO EXISTIR
os.makedirs(OUTPUT_DIR, exist_ok=True)
print("✅ Pasta dados_processados pronta")

# 3. CARREGAR DADOS ORIGINAIS
print("\n📥 CARREGANDO DADOS ORIGINAIS...")
df = pd.read_csv(INPUT_CSV, encoding='latin-1')

print(f"📊 Dataset: {df.shape[0]:,} linhas, {df.shape[1]} colunas")
print(f"💰 Total de vendas original: ${df['SALES'].sum():,.2f}")

# 4. PREPARAR DADOS BÁSICOS (SEM COMPLICAÇÕES)
print("\n⚙️ PREPARANDO DADOS...")

# Converter datas
df['ORDERDATE'] = pd.to_datetime(df['ORDERDATE'])
df['ANO'] = df['ORDERDATE'].dt.year
df['MES'] = df['ORDERDATE'].dt.month
df['MES_NOME'] = df['ORDERDATE'].dt.strftime('%B')
df['TRIMESTRE'] = df['ORDERDATE'].dt.quarter

# 5. SALVAR VERSÃO SIMPLIFICADA (RECOMENDADO PARA INICIANTE)
print("\n💾 SALVANDO ARQUIVO SIMPLIFICADO...")

# Arquivo único e simples
simple_path = os.path.join(OUTPUT_DIR, 'vendas_simples.csv')
df.to_csv(simple_path, index=False, encoding='utf-8')

print(f"✅ Arquivo único salvo: vendas_simples.csv")
print(f"   Local: {simple_path}")

# 6. SALVAR VERSÃO COM MODELO ESTRELA (PARA AVANÇADOS)
print("\n💾 SALVANDO MODELO ESTRELA...")

# Criar IDs simples
df['PRODUCT_ID'] = pd.factorize(df['PRODUCTCODE'])[0] + 1
df['CUSTOMER_ID'] = pd.factorize(df['CUSTOMERNAME'])[0] + 1
df['DATE_ID'] = pd.factorize(df['ORDERDATE'])[0] + 1

# Tabela FATO
fato_cols = ['ORDERNUMBER', 'ORDERLINENUMBER', 'DATE_ID', 'PRODUCT_ID', 'CUSTOMER_ID',
             'QUANTITYORDERED', 'PRICEEACH', 'SALES', 'STATUS', 'DEALSIZE']
fato_vendas = df[fato_cols].copy()

# Tabela PRODUTOS
produtos = df[['PRODUCT_ID', 'PRODUCTCODE', 'PRODUCTLINE', 'MSRP']].drop_duplicates()

# Tabela CLIENTES
clientes = df[['CUSTOMER_ID', 'CUSTOMERNAME', 'COUNTRY', 'CITY', 'STATE',
               'POSTALCODE', 'TERRITORY', 'PHONE']].drop_duplicates()

# Tabela TEMPO
tempo = df[['DATE_ID', 'ORDERDATE', 'ANO', 'MES', 'MES_NOME', 'TRIMESTRE']].drop_duplicates()
tempo = tempo.rename(columns={'ORDERDATE': 'DATA'})

# Salvar CSVs
fato_vendas.to_csv(os.path.join(OUTPUT_DIR, 'fato_vendas.csv'), index=False)
produtos.to_csv(os.path.join(OUTPUT_DIR, 'dim_produtos.csv'), index=False)
clientes.to_csv(os.path.join(OUTPUT_DIR, 'dim_clientes.csv'), index=False)
tempo.to_csv(os.path.join(OUTPUT_DIR, 'dim_tempo.csv'), index=False)

print("✅ 4 arquivos do modelo estrela salvos")

# 7. CRIAR INSTRUÇÕES
print("\n📝 CRIANDO INSTRUÇÕES...")

instrucoes = f"""
# 📋 INSTRUÇÕES PARA POWER BI

## 📁 ARQUIVOS DISPONÍVEIS em {OUTPUT_DIR}

### OPÇÃO 1: ARQUIVO ÚNICO (RECOMENDADO PARA INICIANTES)
**vendas_simples.csv** - {df.shape[0]:,} linhas
- Mais fácil de importar
- Não precisa de relacionamentos
- Use este primeiro!

### OPÇÃO 2: MODELO ESTRELA (PARA AVANÇADOS)
4 arquivos separados:
1. fato_vendas.csv - Transações
2. dim_produtos.csv - Produtos
3. dim_clientes.csv - Clientes
4. dim_tempo.csv - Datas

## 🚀 COMO IMPORTAR:

### Para vendas_simples.csv (FÁCIL):
1. Abra Power BI Desktop
2. "Obter Dados" → "Texto/CSV"
3. Navegue até: {OUTPUT_DIR}
4. Selecione "vendas_simples.csv"
5. Clique em "Carregar"

### Para modelo estrela:
1. Importe os 4 arquivos separadamente
2. Vá para "Modelo" (ícone 🔗)
3. Crie relacionamentos:
   - fato_vendas[PRODUCT_ID] → dim_produtos[PRODUCT_ID]
   - fato_vendas[CUSTOMER_ID] → dim_clientes[CUSTOMER_ID]
   - fato_vendas[DATE_ID] → dim_tempo[DATE_ID]

## 📊 DADOS:
- Total de vendas: ${df['SALES'].sum():,.2f}
- Ticket médio: ${df['SALES'].mean():,.2f}
- Período: {df['ORDERDATE'].min().strftime('%d/%m/%Y')} a {df['ORDERDATE'].max().strftime('%d/%m/%Y')}

## 🎯 TESTE RÁPIDO:
Crie uma tabela com:
- PRODUCTLINE
- SALES (Soma)

Deve mostrar total: ${df['SALES'].sum():,.2f}

Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
"""

with open(os.path.join(OUTPUT_DIR, 'LEIAME.txt'), 'w', encoding='utf-8') as f:
    f.write(instrucoes)

print("✅ Instruções salvas em LEIAME.txt")

# 8. RESUMO FINAL
print("\n" + "=" * 60)
print("✅ PROCESSAMENTO CONCLUÍDO!")
print("=" * 60)
print(f"\n📁 ARQUIVOS SALVOS EM:")
print(f"   {OUTPUT_DIR}")
print(f"\n📊 RESUMO:")
print(f"   • Total de vendas: ${df['SALES'].sum():,.2f}")
print(f"   • Transações: {df.shape[0]:,}")
print(f"   • Período: {df['ORDERDATE'].min().strftime('%d/%m/%Y')} a {df['ORDERDATE'].max().strftime('%d/%m/%Y')}")
print(f"\n🎯 RECOMENDAÇÃO:")
print(f"   Use 'vendas_simples.csv' primeiro (mais fácil)!")
print("=" * 60)