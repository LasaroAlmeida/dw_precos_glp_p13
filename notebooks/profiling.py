# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
# MAGIC %md
# MAGIC ## Download samples

# COMMAND ----------

download_url = "https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/shpc/dsan/2026/08-dados-abertos-precos-2026-08-glp.csv"
path_volume = "/Volumes/anp_glp/00_landing/anp_files/"
file_name = download_url.split('/')[-1]

volume_path = f"{path_volume}" + "/" + f"{file_name}"
print(volume_path)

# dbutils.fs.cp(f"{download_url}", volume_path)

# COMMAND ----------

files = {file.name : file.path for file in dbutils.fs.ls(path_volume)}
print(files)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Profiling

# COMMAND ----------

# MAGIC %md
# MAGIC ### Jan/2026

# COMMAND ----------

df01 = spark.read.csv(
    files["01-dados-abertos-precos-glp.csv"], header=True, inferSchema=True, sep=";"
)

schema01 = {name: dtype for name, dtype in df01.dtypes}
print(f"Schema {schema01}")

# COMMAND ----------

df01.createOrReplaceTempView("base_202601")
display(df01)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Feb/2026

# COMMAND ----------

df02 = spark.read.csv(files["02-dados-abertos-precos-glp.csv"],
        header=True,
        inferSchema=True,
        sep=";"
    )

schema02 = {name: dtype for name, dtype in df02.dtypes}
print(f"Schema {schema02}")

# COMMAND ----------

df02.createOrReplaceTempView("base_202602")
display(df02)

# COMMAND ----------

# MAGIC %md
# MAGIC %md
# MAGIC ### Mar/2026

# COMMAND ----------

df03 = spark.read.csv(files["03-dados-abertos-precos-glp.csv"],
        header=True,
        inferSchema=True,
        sep=";"
    )

schema03 = {name: dtype for name, dtype in df03.dtypes}
print(f"Schema {schema03}")

# COMMAND ----------

df03.createOrReplaceTempView("base_202603")
display(df03)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Jan/2023

# COMMAND ----------

df04 = spark.read.csv(files["precos-glp-01.csv"],
        header=True,
        inferSchema=True,
        sep=";"
    )

schema04 = {name: dtype for name, dtype in df04.dtypes}
print(f"Schema {schema04}")

# COMMAND ----------

df04.createOrReplaceTempView("base_202301")
display(df04)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Aug/2026

# COMMAND ----------

df05 = spark.read.csv(files["08-dados-abertos-precos-2026-08-glp.csv"],
        header=True,
        inferSchema=True,
        sep=";"
    )

schema05 = {name: dtype for name, dtype in df05.dtypes}
print(f"Schema {schema05}")

# COMMAND ----------

df05.createOrReplaceTempView("base_202608")
display(df05)

# COMMAND ----------

# Comparing dicts
print(schema01 == schema02 == schema03 == schema04 == schema05)
# A partir dos arquivos de 01/2023, 01, 02 e 03 de 2026 e 08/2026, é possível inferir que o schema é o mesmo.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Análise da granularida usada nas tabelas

# COMMAND ----------

# MAGIC %sql
# MAGIC select 
# MAGIC     *
# MAGIC from base_202601

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     'Contagem de linhas' AS `métrica`,
# MAGIC     (select count(*) from base_202601) as `202601`,
# MAGIC     (select count(*) from base_202602) as `202602`,
# MAGIC     (select count(*) from base_202603) as `202603`,
# MAGIC     (select count(*) from base_202608) as `202608`,
# MAGIC     (select count(*) from base_202301) as `202301`
# MAGIC UNION ALL
# MAGIC SELECT
# MAGIC     'Contagem distinta CNPJ da Revenda + Data da Coleta' AS `métrica`,
# MAGIC     (select count(distinct `CNPJ da Revenda`, `Data da Coleta`) from base_202601) as `202601`,
# MAGIC     (select count(distinct `CNPJ da Revenda`, `Data da Coleta`) from base_202602) as `202602`,
# MAGIC     (select count(distinct `CNPJ da Revenda`, `Data da Coleta`) from base_202603) as `202603`,
# MAGIC     (select count(distinct `CNPJ da Revenda`, `Data da Coleta`) from base_202608) as `202608`,
# MAGIC     (select count(distinct `CNPJ da Revenda`, `Data da Coleta`) from base_202301) as `202301`
# MAGIC UNION ALL
# MAGIC SELECT
# MAGIC     'Contagem de linhas com CNPJ da Revenda nulos' AS `métrica`,
# MAGIC     (select count(*) from base_202601 where `CNPJ da Revenda` is NULL) as `202601`,
# MAGIC     (select count(*) from base_202602 where `CNPJ da Revenda` is NULL) as `202602`,
# MAGIC     (select count(*) from base_202603 where `CNPJ da Revenda` is NULL) as `202603`,
# MAGIC     (select count(*) from base_202608 where `CNPJ da Revenda` is NULL) as `202608`,
# MAGIC     (select count(*) from base_202301 where `CNPJ da Revenda` is NULL) as `202301`
# MAGIC UNION ALL
# MAGIC SELECT
# MAGIC     'Contagem linhas duplicadas completas' AS `métrica`,
# MAGIC     (SELECT COUNT(*) - (SELECT COUNT(*) FROM (SELECT DISTINCT * FROM base_202601)) AS total_duplicadas FROM base_202601) as `202601`,
# MAGIC     (SELECT COUNT(*) - (SELECT COUNT(*) FROM (SELECT DISTINCT * FROM base_202602)) AS total_duplicadas FROM base_202602) as `202602`,
# MAGIC     (SELECT COUNT(*) - (SELECT COUNT(*) FROM (SELECT DISTINCT * FROM base_202603)) AS total_duplicadas FROM base_202603) as `202603`,
# MAGIC     (SELECT COUNT(*) - (SELECT COUNT(*) FROM (SELECT DISTINCT * FROM base_202608)) AS total_duplicadas FROM base_202608) as `202608`,
# MAGIC     (SELECT COUNT(*) - (SELECT COUNT(*) FROM (SELECT DISTINCT * FROM base_202301)) AS total_duplicadas FROM base_202301) as `202301`

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM base_202608
# MAGIC WHERE `Data da Coleta` is null

# COMMAND ----------

# MAGIC %sql
# MAGIC select 
# MAGIC     `CNPJ da Revenda`,
# MAGIC     count(distinct `Nome da Rua`)
# MAGIC from base_202601
# MAGIC group by all
# MAGIC order by 2 desc

# COMMAND ----------

# MAGIC %sql
# MAGIC select 
# MAGIC     *
# MAGIC from base_202601
# MAGIC --where `Bandeira` is null
# MAGIC order by 
# MAGIC     `CNPJ da Revenda`,
# MAGIC     `Data da Coleta`

# COMMAND ----------

# MAGIC %sql
# MAGIC select 
# MAGIC     count(*),
# MAGIC     count(distinct `CNPJ da Revenda`, `Data da Coleta`)
# MAGIC from base_202301
# MAGIC -- where `Bandeira` is null
# MAGIC -- 12561

# COMMAND ----------

# MAGIC %md
# MAGIC