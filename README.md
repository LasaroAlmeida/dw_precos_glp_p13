# Data Warehouse de Preços de GLP P13

Projeto de engenharia de dados para construir um data warehouse voltado à análise dos preços do botijão de gás GLP P13 no Brasil. O projeto usa os dados abertos da Agência Nacional do Petróleo, Gás Natural e Biocombustíveis (ANP) e tem como foco praticar ingestão, qualidade de dados, modelagem dimensional e disponibilização de dados analíticos.

## Fonte dos dados

Os dados são provenientes da [Série Histórica de Preços de Combustíveis da ANP](https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/serie-historica-de-precos-de-combustiveis), no recorte de **GLP P13**. Há arquivos mensais disponíveis a partir de janeiro de 2023.

Cada observação representa o preço pesquisado em uma revenda em uma data de coleta. Entre os principais atributos estão a identificação e localização da revenda, produto, data, valor de venda, valor de compra e bandeira.

## Estado atual

O projeto está na etapa de profiling dos arquivos de origem. Foram comparados os arquivos de 2023/01, 2026/01, 2026/02, 2026/03 e 2026/08; o schema é consistente entre eles.

Para os registros válidos, a combinação abaixo é única no recorte analisado e será usada como chave de negócio:

```text
CNPJ da Revenda + Data da Coleta
```

O arquivo de 2023/01 contém 1.236 linhas integralmente nulas, que devem ser descartadas durante a limpeza. Os detalhes de schema, volume, qualidade e granularidade estão em [docs/01_profiling.md](docs/01_profiling.md).

## Estrutura do repositório

```text
.
├── docs/                 # Documentação e metadados da fonte
├── notebooks/
│   └── profiling.py      # Notebook Databricks de exploração
├── src/
│   └── glp_dw/           # Módulos Python reutilizáveis do pipeline
├── pyproject.toml        # Configuração do ambiente Python local
└── uv.lock               # Versões bloqueadas das dependências
```

## Ambiente e execução

O ambiente de execução é o **Databricks**. O notebook de profiling depende de Spark, `dbutils` e de um volume configurado para os arquivos da ANP; portanto, não é executado localmente sem adaptações.

Para desenvolvimento local e verificação dos módulos Python, use Python 3.12 ou superior e `uv`:

```bash
uv sync
uv run python -m compileall src
```

## Próximos passos

1. Concluir o profiling: completude, domínios dos atributos, cobertura temporal e validações de preço.
2. Implementar ingestão dos arquivos mensais e limpeza de registros integralmente nulos.
3. Modelar as camadas analíticas e a estrutura dimensional.
4. Criar `databricks.yml` e arquivos em `resources/` para versionar Jobs e automatizar deploys com Databricks Asset Bundles.
5. Adicionar testes para transformações e regras de qualidade.

## Contribuição

Consulte [AGENTS.md](AGENTS.md) para convenções de código, documentação, testes e commits.
