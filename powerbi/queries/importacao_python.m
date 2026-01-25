
let
    // Configuração
    caminho_base = "C:\\Users\\samue\\PycharmProjects\\analise-vendas-python\\dados_processados",

    // Carregar tabela FATO
    FonteFato = Csv.Document(
        File.Contents(caminho_base & "\fato_vendas.csv"),
        [Delimiter=",", Columns=10, Encoding=65001, QuoteStyle=QuoteStyle.None]
    ),
    #"Promoted Headers" = Table.PromoteHeaders(FonteFato, [PromoteAllScalars=true]),

    // Carregar DIMENSÕES
    Produtos = Csv.Document(
        File.Contents(caminho_base & "\dim_produtos.csv"),
        [Delimiter=",", Columns=4, Encoding=65001]
    ),
    #"ProdutosHeaders" = Table.PromoteHeaders(Produtos, [PromoteAllScalars=true]),

    Clientes = Csv.Document(
        File.Contents(caminho_base & "\dim_clientes.csv"),
        [Delimiter=",", Columns=8, Encoding=65001]
    ),
    #"ClientesHeaders" = Table.PromoteHeaders(Clientes, [PromoteAllScalars=true]),

    Tempo = Csv.Document(
        File.Contents(caminho_base & "\dim_tempo.csv"),
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
