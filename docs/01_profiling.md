## Entendimento dos dados

A primeira etapa do projeto é o _profiling_. Nesta etapa vamos analisar alguns dos datasets para tentar identificar schemas, chaves primárias e grão das tabelas.

## Schema

A partir da comparação entre os schemas das bases de 2023/01, 2026/01, 2026/02, 2026/03 e 2026/08, é possível inferir que o schema se mantém igual. Os campos e tipos abaixo foram documentados pela ANP no arquivo de metadados da Série Histórica de Preços de Combustíveis.

| Campo | Tipo informado | Descrição |
| --- | --- | --- |
| `Regiao - Sigla` | alfanumérico | Sigla da região da revenda pesquisada. |
| `Estado - Sigla` | alfanumérico | Sigla da Unidade Federativa (UF) da revenda pesquisada. |
| `Municipio` | alfanumérico | Nome do município da revenda pesquisada. |
| `Revenda` | alfanumérico | Nome da revenda pesquisada. |
| `CNPJ da Revenda` | numérico | Número do Cadastro Nacional de Pessoa Jurídica da revenda pesquisada. |
| `Nome da Rua` | alfanumérico | Nome do logradouro da revenda pesquisada. |
| `Numero Rua` | alfanumérico | Número do logradouro da revenda pesquisada. |
| `Complemento` | alfanumérico | Complemento do logradouro da revenda pesquisada. |
| `Bairro` | alfanumérico | Nome do bairro da revenda pesquisada. |
| `Cep` | alfanumérico | Endereço Postal (CEP) do logradouro da revenda pesquisada. |
| `Produto` | alfanumérico | Nome do combustível pesquisado. |
| `Data da Coleta` | data | Data da coleta dos preços. |
| `Valor de Venda` | numérico | Preço de venda ao consumidor final praticado pelo revendedor na data da coleta. |
| `Valor de Compra` | numérico | Preço de distribuição, isto é, o preço de venda da distribuidora ao posto revendedor. Série disponível até agosto de 2020. |
| `Unidade de Medida` | alfanumérico | Unidade de medida do combustível. |
| `Bandeira` | alfanumérico | Nome da bandeira da revenda. |

> O levantamento da ANP abrange, entre outros combustíveis, o GLP P13 e é atualizado em periodicidades semanal, mensal e semestral.

## Cobertura e volume

Foram analisados os arquivos mensais de 2023/01, 2026/01, 2026/02, 2026/03 e 2026/08, no recorte de GLP P13.

| Métrica | 2023/01 | 2026/01 | 2026/02 | 2026/03 | 2026/08 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Contagem de linhas | 18.101 | 12.561 | 12.609 | 14.461 | 14.355 |
| Chaves distintas (`CNPJ da Revenda` + `Data da Coleta`) | 16.865 | 12.561 | 12.609 | 14.461 | 14.355 |
| Linhas com `CNPJ da Revenda` nulo | 1.236 | 0 | 0 | 0 | 0 |
| Linhas duplicadas completas | 1.235 | 0 | 0 | 0 | 0 |

O arquivo de 2023/01 contém 1.236 linhas integralmente nulas. Uma delas é o registro vazio distinto e as outras 1.235 são repetições desse registro. Essas linhas não representam observações de preço e devem ser descartadas na etapa de limpeza.

Após a exclusão das linhas integralmente nulas, o arquivo de 2023/01 possui 16.865 registros, sem CNPJ nulo e sem duplicidades completas.

## Chave primária

Após a exclusão de linhas integralmente nulas, a combinação `CNPJ da Revenda` + `Data da Coleta` é única em todos os arquivos analisados. Portanto, ela pode ser utilizada como chave primária para os conjuntos mensais no recorte de GLP P13.

## Grão

Cada arquivo contém uma linha para cada revenda para cada data de coleta. A coleta é feita, aproximadamente, uma vez por semana.
