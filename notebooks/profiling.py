# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
# MAGIC %md
# MAGIC ## Download samples

# COMMAND ----------

download_url = "https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/shpc/dsan/2026/03-dados-abertos-precos-glp.csv"
path_volume = "/Volumes/anp_glp/00_landing/anp_files/"
file_name = download_url.split('/')[-1]


dbutils.fs.cp(f"{download_url}", f"{path_volume}" + "/" + f"{file_name}")

# COMMAND ----------

files = dbutils.fs.ls(path_volume)
print(f"Available files {files}")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Janeiro/2026

# COMMAND ----------

df01 = spark.read.csv(
    f"{path_volume}/{files[0].name}", header=True, inferSchema=True, sep=";"
)

schema01 = {name: dtype for name, dtype in df01.dtypes}
print(f"Schema {schema01}")

# COMMAND ----------

display(df01)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Fevereiro/2026

# COMMAND ----------

df02 = spark.read.csv(f"{path_volume}/{files[1].name}",
        header=True,
        inferSchema=True,
        sep=";"
    )

# COMMAND ----------

display(df02)

# COMMAND ----------

# MAGIC %md
# MAGIC %md
# MAGIC ### Março/2026

# COMMAND ----------

df03 = spark.read.csv(f"{path_volume}/{files[2].name}",
        header=True,
        inferSchema=True,
        sep=";"
    )

# COMMAND ----------

display(df03)