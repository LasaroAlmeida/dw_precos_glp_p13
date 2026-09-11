# Diretrizes do Repositório

## Estrutura do Projeto e Organização dos Módulos

- `src/glp_dw/` contém módulos Python reutilizáveis; não coloque essa lógica em notebooks.
- `notebooks/profiling.py` é uma fonte de notebook Databricks para analisar os CSVs de GLP P13 da ANP com Spark.
- `docs/` contém a documentação. Atualize `docs/01_profiling.md` ao mudar premissas, resultados ou regras de qualidade.
- `pyproject.toml` e `uv.lock` definem o ambiente Python. Não edite `uv.lock` manualmente.

## Desenvolvimento Local e Execução no Databricks

O Databricks é o ambiente de execução. Configure nele o cluster, o acesso aos volumes e as dependências do notebook ou pipeline. Não há comando de execução local.

Use Python 3.12 e `uv` apenas para desenvolvimento local:

```bash
uv sync                         # Cria ou atualiza o ambiente virtual local
uv run python -m compileall src # Verifica a compilação dos módulos do pacote
uv lock                         # Atualiza o lockfile após mudar dependências
```

O notebook requer workspace Databricks/Spark, `dbutils` e o caminho de volume configurado; não o execute localmente sem adaptações. Ainda não há suíte automatizada de testes ou formatador. Ao introduzir módulos de produção, adicione testes com `pytest` em `tests/` e execute `uv run pytest` localmente.

## Estilo de Código e Convenções de Nomenclatura

Siga a PEP 8: indentação de quatro espaços, `snake_case` para funções, variáveis e módulos, e `PascalCase` para classes. Adicione anotações de tipo a funções reutilizáveis e docstrings curtas a transformações não óbvias. Ao ler dados brutos, preserve os nomes de colunas da ANP; renomeie-os somente em uma camada explícita de transformação. Prefira `raw_prices_df` e `collection_date` a `df1`.

Use títulos e tabelas Markdown de forma consistente na documentação. Registre resultados medidos, escopo e regras de limpeza; mantenha SQL exploratório no notebook, salvo quando ele for necessário à lógica reproduzível do pipeline.

## Testes e Validação de Dados

Teste transformações determinísticas e regras de qualidade, incluindo remoção de linhas integralmente nulas e a unicidade de `CNPJ da Revenda` mais `Data da Coleta` no conjunto mensal de GLP P13. Nomeie testes como `test_<comportamento>.py`, por exemplo, `tests/test_cleaning.py`.

## Diretrizes para Commits e Pull Requests

Use assuntos de commit curtos e no imperativo, em português, seguindo o histórico: `Adiciona validação de linhas nulas`. Mantenha cada commit focado. Pull requests devem resumir a alteração, indicar arquivos afetados, descrever validações e vincular a issue, quando houver. Inclua saídas de exemplo ou capturas de tela para mudanças relevantes no notebook Databricks ou na documentação.
