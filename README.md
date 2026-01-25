📈 Análise de Dados de Vendas

https://img.shields.io/badge/Status-Conclu%C3%ADdo-brightgreen
https://img.shields.io/badge/Python-3.8%252B-blue
https://img.shields.io/badge/Licen%C3%A7a-MIT-green
https://img.shields.io/badge/%C3%9Altimo_Commit-Outubro_2023-orange
📋 Sobre o Projeto

Análise exploratória completa de dados de vendas de uma empresa, utilizando Python e bibliotecas de Data Science.

Objetivo: Demonstrar habilidades em análise de dados, limpeza, visualização e storytelling com dados para tomada de decisões estratégicas.
👤 Autor

Samuel Maia
https://img.shields.io/badge/GitHub-samuelmaiapro-black
https://img.shields.io/badge/LinkedIn-Perfil-blue
🚀 Tecnologias Utilizadas

    Python 3.8+

    Pandas 1.5.3 - Manipulação de dados

    Matplotlib 3.7.1 & Seaborn 0.12.2 - Visualização

    Jupyter Notebook 1.0.0 - Análise interativa

    NumPy 1.24.3 - Cálculos numéricos

📊 Conjunto de Dados
📋 Metadados
Item	Valor
Fonte	Kaggle - Sales Data Sample
Período analisado	06/01/2003 a 31/05/2005
Total de registros	2.823 vendas
Número de atributos	25 colunas
Países atendidos	19 países
Clientes únicos	92 clientes
Produtos diferentes	109 códigos
Volume total	$10.032.443,34
💰 Métricas Financeiras

    Ticket médio: $3.553,82 por venda

    Venda máxima: $140.555,00

    Venda mínima: $482,13

    Mediana de venda: $3.081,60

    Desvio padrão: $3.293,53

🏆 Top 3 Categorias de Produtos

    Classic Cars: $3.919.158,08 (39,1% do total)

    Vintage Cars: $1.805.934,84 (18,0% do total)

    Motorcycles: $1.117.135,14 (11,1% do total)

🌎 Distribuição Geográfica

    América do Norte: EUA (53,7%), Canadá (2,1%)

    Europa: França (12,3%), Alemanha (8,5%), Reino Unido (4,2%)

    Ásia-Pacífico: Japão (5,4%), Austrália (4,9%), Singapura (3,1%)

    Escandinávia: Finlândia, Noruega, Suécia, Dinamarca

📈 Principais Análises Realizadas
1. 📅 Análise Temporal

    Crescimento anual: 2003 ($3.9M) → 2004 ($4.0M) → 2005 ($2.1M*)

    Sazonalidade: Pico de vendas em Novembro (Black Friday/Natal)

    Tendência: Crescimento de 2,6% de 2003 para 2004

*Dados parciais de 2005 (apenas 5 meses)
2. 🏆 Análise de Produtos

    Classic Cars dominam o portfólio (39,1% das vendas)

    Ships e Trains são categorias de nicho (< 5% cada)

    Vintage Cars tem o maior ticket médio ($4.856,73)

3. 🌍 Análise Geográfica

    EUA é o maior mercado (53,7% das vendas)

    Europa representa 32,4% do faturamento

    APAC (Ásia-Pacífico) mostra maior potencial de crescimento

4. 🎯 Insights Estratégicos

    Oportunidade: Expandir linha de Classic Cars (demanda consistente)

    Alerta: Diversificar mercado americano (muito concentrado)

    Recomendação: Investir em marketing no último trimestre (pico sazonal)

    Sugestão: Desenvolver mais produtos na categoria Vintage Cars (alta margem)

📁 Estrutura do Projeto
text

analise-vendas-python/
├── dados/                   # Arquivos de dados
│   └── sales_data_sample.csv
├── notebooks/              # Análises em Jupyter
│   └── analise_vendas.ipynb
├── scripts/                # Scripts Python (opcional)
├── README.md              # Esta documentação
├── requirements.txt       # Dependências do projeto
└── .gitignore            # Arquivos ignorados pelo Git

📊 Visualizações Implementadas
Gráfico 1: Vendas por Ano

https://via.placeholder.com/800x400/4A90E2/FFFFFF?text=Vendas+por+Ano
Análise de crescimento anual e performance por período
Gráfico 2: Distribuição por Categoria

https://via.placeholder.com/800x400/50E3C2/FFFFFF?text=Top+Categorias+de+Produtos
Participação de cada categoria no faturamento total
Gráfico 3: Tendência Mensal

https://via.placeholder.com/800x400/F5A623/FFFFFF?text=Tend%C3%AAncia+Mensal+de+Vendas
Sazonalidade e padrões mensais de vendas
Gráfico 4: Distribuição Geográfica

https://via.placeholder.com/800x400/9013FE/FFFFFF?text=Distribui%C3%A7%C3%A3o+Geogr%C3%A1fica+das+Vendas
Concentração de vendas por país/região
🛠️ Como Executar
Pré-requisitos

    Python 3.8 ou superior

    Git instalado

    500MB de espaço livre

Passo a Passo

    Clonar repositório
    bash

    git clone https://github.com/samuelmaiapro/analise-vendas-python.git
    cd analise-vendas-python

    Criar ambiente virtual (recomendado)
    bash

    python -m venv venv

    # Windows:
    venv\Scripts\activate

    # Mac/Linux:
    source venv/bin/activate

    Instalar dependências
    bash

    pip install -r requirements.txt

    Executar análise
    bash

    jupyter notebook notebooks/analise_vendas.ipynb

Execução Rápida (Google Colab)

https://colab.research.google.com/assets/colab-badge.svg
📝 Próximos Passos (Melhorias Futuras)
🚀 Fase 2 (Próximas 2 semanas)

    Adicionar análise de RFM (Recência, Frequência, Valor Monetário)

    Implementar dashboard interativo com Streamlit

    Criar API REST para consulta dos dados

🔮 Fase 3 (Próximos 2 meses)

    Adicionar previsão de vendas com Machine Learning

    Análise de cohort para retenção de clientes

    Sistema de recomendação de produtos

    Integração com Power BI/Tableau

🎯 Melhorias Técnicas

    Adicionar testes unitários com pytest

    Configurar CI/CD com GitHub Actions

    Dockerizar a aplicação

    Documentação automática com Sphinx

📄 Metodologia
1. Coleta e Importação

    Download do dataset do Kaggle

    Verificação de encoding e delimitadores

    Carregamento com tratamento de erros

2. Limpeza e Preparação

    Verificação de valores nulos

    Conversão de tipos de dados

    Criação de features derivadas

    Tratamento de outliers

3. Análise Exploratória (EDA)

    Estatísticas descritivas

    Correlações entre variáveis

    Identificação de padrões

    Testes de hipóteses

4. Visualização e Storytelling

    Seleção de gráficos adequados

    Customização estética

    Anotações e insights

    Exportação para relatórios

🤝 Contribuição

Contribuições são bem-vindas! Siga estes passos:

    Fork o projeto

    Crie uma branch (git checkout -b feature/nova-feature)

    Commit suas mudanças (git commit -m 'Adiciona nova feature')

    Push para a branch (git push origin feature/nova-feature)

    Abra um Pull Request

Padrões de Código

    Use nomes descritivos para variáveis

    Comente código complexo

    Mantenha o notebook organizado com markdown

    Siga o PEP 8 para Python

❓ FAQ
P: Posso usar este projeto no meu portfólio?

R: Sim! Este projeto foi desenvolvido especificamente para fins educacionais e de portfólio.
P: Preciso ter experiência em Python?

R: O projeto é acessível para iniciantes, mas conhecimentos básicos de Python são recomendados.
P: Os dados são reais?

R: Os dados são de uma empresa fictícia, mas representam cenários realistas de negócios.
P: Como posso adaptar para meus próprios dados?

R: Basta substituir o arquivo CSV e ajustar os nomes das colunas no notebook.
📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.
text

MIT License

Copyright (c) 2023 Samuel Maia

Permissão é concedida, gratuitamente, a qualquer pessoa que obtenha uma cópia
deste software e arquivos de documentação associados (o "Software"), para lidar
no Software sem restrição, incluindo sem limitação os direitos de usar, copiar,
modificar, mesclar, publicar, distribuir, sublicenciar e/ou vender cópias do
Software, e permitir que as pessoas a quem o Software é fornecido o façam, 
sujeito às seguintes condições:

O aviso de direitos autorais acima e este aviso de permissão devem ser incluídos
em todas as cópias ou partes substanciais do Software.

🙏 Agradecimentos

    Dataset fornecido por Kaggle

    Comunidade Python Brasil

    Tutoriais e documentação das bibliotecas utilizadas

    Todos que contribuíram com feedback e sugestões

📞 Contato

Samuel Maia

    GitHub: @samuelmaiapro

    Email: [smaia2@gmail.com]

    LinkedIn: [linkedin.com/in/samuelmaiapro]

⭐ Se este projeto foi útil, considere dar uma estrela no repositório!

https://api.star-history.com/svg?repos=samuelmaiapro/analise-vendas-python&type=Date

Última atualização: 01/2026
Versão do projeto: 1.0.0
